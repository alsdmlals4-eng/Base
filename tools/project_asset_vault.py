#!/usr/bin/env python3
"""Manage a project-local image vault and mirror its active library into a Godot repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CONFIG = {
    "schema_version": 1,
    "vault_root": ".asset-vault",
    "library_dir": "library",
    "archive_dir": "archive",
    "inbox_dir": "inbox",
    "managed_root": "assets/_managed",
    "sync_manifest": "assets/ASSET_VAULT_SYNC.json",
    "supported_extensions": [".png", ".jpg", ".jpeg", ".webp", ".svg"],
}
CONFIG_NAME = "PROJECT_ASSET_VAULT.json"
STATE_NAME = "state.json"
PARTIAL_SUFFIXES = (".crdownload", ".part", ".tmp")


class VaultError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise VaultError(f"Cannot read JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise VaultError(f"JSON root must be an object: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_relative(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise VaultError(f"{label} must stay inside the project: {value!r}")
    return path


def load_config(project_root: Path) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    config_path = project_root / CONFIG_NAME
    if config_path.is_file():
        supplied = _read_json(config_path)
        for key in DEFAULT_CONFIG:
            if key in supplied:
                config[key] = supplied[key]
    for key in ("vault_root", "library_dir", "archive_dir", "inbox_dir", "managed_root", "sync_manifest"):
        if not isinstance(config[key], str) or not config[key]:
            raise VaultError(f"Config field {key} must be a non-empty string")
    _safe_relative(config["vault_root"], "vault_root")
    _safe_relative(config["managed_root"], "managed_root")
    _safe_relative(config["sync_manifest"], "sync_manifest")
    for key in ("library_dir", "archive_dir", "inbox_dir"):
        nested = _safe_relative(config[key], key)
        if len(nested.parts) != 1:
            raise VaultError(f"{key} must be one folder name inside the vault")
    extensions = config.get("supported_extensions")
    if not isinstance(extensions, list) or not extensions or not all(isinstance(item, str) and item.startswith(".") for item in extensions):
        raise VaultError("supported_extensions must be a non-empty list such as ['.png', '.webp']")
    config["supported_extensions"] = sorted({item.casefold() for item in extensions})
    return config


def paths(project_root: Path, config: dict[str, Any]) -> dict[str, Path]:
    root = project_root.resolve()
    vault = root / _safe_relative(config["vault_root"], "vault_root")
    managed = root / _safe_relative(config["managed_root"], "managed_root")
    manifest = root / _safe_relative(config["sync_manifest"], "sync_manifest")
    if managed == vault or managed.is_relative_to(vault) or vault.is_relative_to(managed):
        raise VaultError("vault_root and managed_root must be separate")
    return {
        "project": root,
        "vault": vault,
        "library": vault / config["library_dir"],
        "archive": vault / config["archive_dir"],
        "inbox": vault / config["inbox_dir"],
        "state": vault / STATE_NAME,
        "managed": managed,
        "manifest": manifest,
    }


def _default_state() -> dict[str, Any]:
    return {"schema_version": 1, "download_sources": {}, "seen_download_events": [], "last_managed_paths": []}


def load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.is_file():
        return _default_state()
    state = _read_json(state_path)
    default = _default_state()
    for key, value in default.items():
        state.setdefault(key, value)
    return state


def ensure_gitignore(project_root: Path, vault_root: str) -> None:
    ignore_path = project_root / ".gitignore"
    existing = ignore_path.read_text(encoding="utf-8") if ignore_path.is_file() else ""
    rule = Path(vault_root).as_posix().rstrip("/") + "/"
    rules = {line.strip() for line in existing.splitlines()}
    if rule in rules:
        return
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    block = f"{prefix}\n# Project-local asset vault (never commit originals/local state)\n{rule}\n"
    ignore_path.write_text(existing + block, encoding="utf-8")


def init_project(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    config = load_config(project_root)
    p = paths(project_root, config)
    for key in ("library", "archive", "inbox"):
        p[key].mkdir(parents=True, exist_ok=True)
    if not p["state"].exists():
        _write_json(p["state"], _default_state())
    ensure_gitignore(p["project"], config["vault_root"])


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _supported(path: Path, extensions: set[str]) -> bool:
    name = path.name.casefold()
    if any(name.endswith(suffix) for suffix in PARTIAL_SUFFIXES):
        return False
    return path.suffix.casefold() in extensions


def _asset_files(library: Path, extensions: set[str]) -> Iterable[Path]:
    if not library.exists():
        return []
    result: list[Path] = []
    for candidate in library.rglob("*"):
        if candidate.is_symlink():
            raise VaultError(f"Symlinks are not allowed in the active vault library: {candidate}")
        if candidate.is_file() and _supported(candidate, extensions):
            result.append(candidate)
    return sorted(result, key=lambda item: item.relative_to(library).as_posix().casefold())


def _safe_managed_candidate(project: Path, managed_root: Path, relative_text: str) -> Path | None:
    try:
        relative = _safe_relative(relative_text, "managed_path")
    except VaultError:
        return None
    candidate = project / relative
    try:
        resolved = candidate.resolve(strict=False)
        managed_resolved = managed_root.resolve(strict=False)
        if resolved == managed_resolved or not resolved.is_relative_to(managed_resolved):
            return None
    except OSError:
        return None
    return candidate


def _previous_managed_paths(p: dict[str, Path], state: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for item in state.get("last_managed_paths", []):
        if isinstance(item, str):
            values.add(item)
    if p["manifest"].is_file():
        try:
            manifest = _read_json(p["manifest"])
        except VaultError:
            manifest = {}
        for asset in manifest.get("assets", []):
            if isinstance(asset, dict) and isinstance(asset.get("managed_path"), str):
                values.add(asset["managed_path"])
    return values


def sync_project(project_root: Path) -> dict[str, int]:
    init_project(project_root)
    config = load_config(project_root)
    p = paths(project_root, config)
    state = load_state(p["state"])
    extensions = set(config["supported_extensions"])
    assets: list[dict[str, Any]] = []
    current_paths: set[str] = set()
    copied = 0

    for source in _asset_files(p["library"], extensions):
        relative = source.relative_to(p["library"])
        target = p["managed"] / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        source_hash = sha256_file(source)
        should_copy = not target.is_file() or sha256_file(target) != source_hash
        if should_copy:
            shutil.copy2(source, target)
            copied += 1
        managed_path = target.relative_to(p["project"]).as_posix()
        current_paths.add(managed_path)
        assets.append(
            {
                "source_key": relative.as_posix(),
                "managed_path": managed_path,
                "sha256": source_hash,
                "size_bytes": source.stat().st_size,
            }
        )

    removed = 0
    for previous in sorted(_previous_managed_paths(p, state) - current_paths):
        candidate = _safe_managed_candidate(p["project"], p["managed"], previous)
        if candidate is not None and candidate.is_file():
            candidate.unlink()
            removed += 1

    # Clean only empty directories beneath the managed root; never delete untracked files.
    if p["managed"].is_dir():
        for directory in sorted((item for item in p["managed"].rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass

    manifest = {
        "schema_version": 1,
        "authority": "local-vault-filesystem",
        "vault_local_only": True,
        "managed_root": _safe_relative(config["managed_root"], "managed_root").as_posix(),
        "assets": assets,
    }
    _write_json(p["manifest"], manifest)
    state["last_managed_paths"] = sorted(current_paths)
    _write_json(p["state"], state)
    return {"assets": len(assets), "copied": copied, "removed": removed}


def _source_event(source_root: Path, file_path: Path) -> tuple[str, str]:
    relative = file_path.relative_to(source_root).as_posix()
    stat = file_path.stat()
    content_hash = sha256_file(file_path)
    raw = f"{source_root.resolve()}\n{relative}\n{stat.st_size}\n{stat.st_mtime_ns}\n{content_hash}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest(), content_hash


def _iter_download_candidates(source: Path, extensions: set[str]) -> list[Path]:
    if not source.is_dir():
        raise VaultError(f"Download source is not a directory: {source}")
    result: list[Path] = []
    for candidate in source.rglob("*"):
        if candidate.is_symlink():
            continue
        if candidate.is_file() and _supported(candidate, extensions):
            result.append(candidate)
    return sorted(result, key=lambda item: item.relative_to(source).as_posix().casefold())


def _import_destination(import_root: Path, source: Path, content_hash: str) -> Path:
    destination = import_root / source.name
    if not destination.exists():
        return destination
    if destination.is_file() and sha256_file(destination) == content_hash:
        return destination
    return import_root / f"{source.stem}__{content_hash[:8]}{source.suffix.lower()}"


def pull_downloads(project_root: Path, sources: list[Path], include_existing: bool = False) -> dict[str, int]:
    init_project(project_root)
    config = load_config(project_root)
    p = paths(project_root, config)
    state = load_state(p["state"])
    extensions = set(config["supported_extensions"])
    seen = {item for item in state.get("seen_download_events", []) if isinstance(item, str)}
    source_state = state.get("download_sources")
    if not isinstance(source_state, dict):
        source_state = {}
    imported = 0
    baselined = 0

    for source_arg in sources:
        source = source_arg.expanduser().resolve()
        source_key = str(source)
        candidates = _iter_download_candidates(source, extensions)
        first_scan = source_key not in source_state
        if first_scan and not include_existing:
            for candidate in candidates:
                event_id, _ = _source_event(source, candidate)
                seen.add(event_id)
                baselined += 1
            source_state[source_key] = {"initialized": True}
            continue

        for candidate in candidates:
            event_id, content_hash = _source_event(source, candidate)
            if event_id in seen:
                continue
            day = datetime.now().astimezone().date().isoformat()
            import_root = p["library"] / "gpt-imports" / day
            import_root.mkdir(parents=True, exist_ok=True)
            destination = _import_destination(import_root, candidate, content_hash)
            if not destination.exists():
                shutil.copy2(candidate, destination)
                imported += 1
            seen.add(event_id)
        source_state[source_key] = {"initialized": True}

    state["download_sources"] = source_state
    state["seen_download_events"] = sorted(seen)
    _write_json(p["state"], state)
    sync_project(project_root)
    return {"imported": imported, "baselined": baselined}


def watch_downloads(project_root: Path, sources: list[Path], interval: float, include_existing: bool, once: bool) -> None:
    first = True
    while True:
        result = pull_downloads(project_root, sources, include_existing=include_existing if first else True)
        print(f"download scan: imported={result['imported']} baselined={result['baselined']}", flush=True)
        if once:
            return
        first = False
        time.sleep(interval)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create the project-local vault and gitignore rule")
    init.add_argument("--project-root", type=Path, required=True)

    sync = sub.add_parser("sync", help="Mirror the current vault library into the managed Godot asset area")
    sync.add_argument("--project-root", type=Path, required=True)

    pull = sub.add_parser("pull-downloads", help="Import newly downloaded images into the local vault, then sync")
    pull.add_argument("--project-root", type=Path, required=True)
    pull.add_argument("--source", type=Path, action="append", required=True)
    pull.add_argument("--include-existing", action="store_true", help="Import files already present on the first scan")

    watch = sub.add_parser("watch", help="Continuously bridge newly downloaded images into the local vault")
    watch.add_argument("--project-root", type=Path, required=True)
    watch.add_argument("--source", type=Path, action="append", required=True)
    watch.add_argument("--interval", type=float, default=2.0)
    watch.add_argument("--include-existing", action="store_true")
    watch.add_argument("--once", action="store_true", help=argparse.SUPPRESS)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "init":
            init_project(args.project_root)
            print("Project asset vault initialized")
        elif args.command == "sync":
            result = sync_project(args.project_root)
            print(f"Asset vault synced: assets={result['assets']} copied={result['copied']} removed={result['removed']}")
        elif args.command == "pull-downloads":
            result = pull_downloads(args.project_root, args.source, include_existing=args.include_existing)
            print(f"Downloaded images processed: imported={result['imported']} baselined={result['baselined']}")
        elif args.command == "watch":
            if args.interval <= 0:
                raise VaultError("--interval must be greater than zero")
            watch_downloads(args.project_root, args.source, args.interval, args.include_existing, args.once)
        return 0
    except (OSError, VaultError) as error:
        print(f"Project asset vault failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
