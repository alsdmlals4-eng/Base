#!/usr/bin/env python3
"""Manage a project-local image vault, local Godot workspace, and explicit promotions."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CONFIG = {
    "schema_version": 2,
    "vault_root": ".asset-vault",
    "library_dir": "library",
    "archive_dir": "archive",
    "inbox_dir": "inbox",
    "workspace_root": "assets/_vault_local",
    "sync_manifest": ".asset-vault/sync.json",
    "promotion_root": "assets",
    "supported_extensions": [".png", ".jpg", ".jpeg", ".webp", ".svg"],
}
CONFIG_NAME = "PROJECT_ASSET_VAULT.json"
STATE_NAME = "state.json"
PARTIAL_SUFFIXES = (".crdownload", ".part", ".tmp")
GODOT_TEXT_SUFFIXES = {
    ".cfg",
    ".cs",
    ".gd",
    ".gdshader",
    ".godot",
    ".material",
    ".shader",
    ".theme",
    ".tres",
    ".tscn",
}


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


def _inside(root: Path, candidate: Path) -> bool:
    root_resolved = root.resolve(strict=False)
    candidate_resolved = candidate.resolve(strict=False)
    return candidate_resolved == root_resolved or candidate_resolved.is_relative_to(root_resolved)


def load_config(project_root: Path) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    config_path = project_root / CONFIG_NAME
    if config_path.is_file():
        supplied = _read_json(config_path)
        legacy_v1 = "managed_root" in supplied and "workspace_root" not in supplied
        for key in DEFAULT_CONFIG:
            if key in supplied:
                config[key] = supplied[key]
        # v1 mirrored every vault file into a tracked output. Fail safe during migration:
        # old configs inherit the v2 local workspace and local manifest instead.
        if legacy_v1:
            config["schema_version"] = 2
            config["workspace_root"] = DEFAULT_CONFIG["workspace_root"]
            config["sync_manifest"] = DEFAULT_CONFIG["sync_manifest"]

    for key in (
        "vault_root",
        "library_dir",
        "archive_dir",
        "inbox_dir",
        "workspace_root",
        "sync_manifest",
        "promotion_root",
    ):
        if not isinstance(config[key], str) or not config[key]:
            raise VaultError(f"Config field {key} must be a non-empty string")

    for key in ("vault_root", "workspace_root", "sync_manifest", "promotion_root"):
        _safe_relative(config[key], key)
    for key in ("library_dir", "archive_dir", "inbox_dir"):
        nested = _safe_relative(config[key], key)
        if len(nested.parts) != 1:
            raise VaultError(f"{key} must be one folder name inside the vault")

    extensions = config.get("supported_extensions")
    if not isinstance(extensions, list) or not extensions or not all(
        isinstance(item, str) and item.startswith(".") for item in extensions
    ):
        raise VaultError("supported_extensions must be a non-empty list such as ['.png', '.webp']")
    config["supported_extensions"] = sorted({item.casefold() for item in extensions})
    return config


def paths(project_root: Path, config: dict[str, Any]) -> dict[str, Path]:
    root = project_root.resolve()
    vault = root / _safe_relative(config["vault_root"], "vault_root")
    workspace = root / _safe_relative(config["workspace_root"], "workspace_root")
    manifest = root / _safe_relative(config["sync_manifest"], "sync_manifest")
    promotion = root / _safe_relative(config["promotion_root"], "promotion_root")

    for label, candidate in (("vault_root", vault), ("workspace_root", workspace), ("promotion_root", promotion)):
        if not _inside(root, candidate):
            raise VaultError(f"{label} resolves outside the project: {candidate}")
    if _paths_overlap(vault, workspace):
        raise VaultError("vault_root and workspace_root must be separate")
    if not _inside(vault, manifest):
        raise VaultError("sync_manifest must stay inside vault_root because synchronization state is local only")
    if _inside(vault, promotion):
        raise VaultError("promotion_root must stay outside vault_root")

    return {
        "project": root,
        "vault": vault,
        "library": vault / config["library_dir"],
        "archive": vault / config["archive_dir"],
        "inbox": vault / config["inbox_dir"],
        "state": vault / STATE_NAME,
        "workspace": workspace,
        "manifest": manifest,
        "promotion": promotion,
    }


def _default_state() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "download_sources": {},
        "seen_download_events": [],
        "last_workspace_assets": {},
        "rejected_hashes": [],
    }


def load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.is_file():
        return _default_state()
    state = _read_json(state_path)
    default = _default_state()
    for key, value in default.items():
        state.setdefault(key, value)
    if not isinstance(state.get("download_sources"), dict):
        state["download_sources"] = {}
    if not isinstance(state.get("seen_download_events"), list):
        state["seen_download_events"] = []
    if not isinstance(state.get("last_workspace_assets"), dict):
        state["last_workspace_assets"] = {}
    if not isinstance(state.get("rejected_hashes"), list):
        state["rejected_hashes"] = []
    state["schema_version"] = 2
    return state


def ensure_gitignore(project_root: Path, relative_roots: Iterable[str]) -> None:
    ignore_path = project_root / ".gitignore"
    existing = ignore_path.read_text(encoding="utf-8") if ignore_path.is_file() else ""
    rules = {line.strip() for line in existing.splitlines()}
    missing = []
    for value in relative_roots:
        rule = Path(value).as_posix().rstrip("/") + "/"
        if rule not in rules:
            missing.append(rule)
    if not missing:
        return
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    block = prefix + "\n# Project-local asset vault/workspace (never commit local candidates/state)\n"
    block += "\n".join(missing) + "\n"
    ignore_path.write_text(existing + block, encoding="utf-8")


def init_project(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    config = load_config(project_root)
    p = paths(project_root, config)
    for key in ("library", "archive", "inbox", "workspace"):
        p[key].mkdir(parents=True, exist_ok=True)
    if not p["state"].exists():
        _write_json(p["state"], _default_state())
    ensure_gitignore(p["project"], (config["vault_root"], config["workspace_root"]))


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


def _safe_target_under(root: Path, relative: Path, label: str) -> Path:
    target = root / relative
    root_resolved = root.resolve(strict=False)
    target_resolved = target.resolve(strict=False)
    if target_resolved == root_resolved or not target_resolved.is_relative_to(root_resolved):
        raise VaultError(f"{label} escapes through a symlink/reparse point: {target}")
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise VaultError(f"{label} traverses a symlink/reparse point: {current}")
    if target.is_symlink():
        raise VaultError(f"{label} is a symlink/reparse point: {target}")
    return target


def _paths_overlap(left: Path, right: Path) -> bool:
    left_resolved = left.resolve(strict=False)
    right_resolved = right.resolve(strict=False)
    return (
        left_resolved == right_resolved
        or left_resolved.is_relative_to(right_resolved)
        or right_resolved.is_relative_to(left_resolved)
    )


def _safe_workspace_candidate(project: Path, workspace_root: Path, relative_text: str) -> Path | None:
    try:
        relative = _safe_relative(relative_text, "workspace_path")
    except VaultError:
        return None
    candidate = project / relative
    try:
        resolved = candidate.resolve(strict=False)
        workspace_resolved = workspace_root.resolve(strict=False)
        if resolved == workspace_resolved or not resolved.is_relative_to(workspace_resolved):
            return None
    except OSError:
        return None
    return candidate


def _previous_workspace_assets(p: dict[str, Path], state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    raw_state = state.get("last_workspace_assets", {})
    if isinstance(raw_state, dict):
        for key, item in raw_state.items():
            if isinstance(key, str) and isinstance(item, dict):
                values[key] = dict(item)
    if p["manifest"].is_file():
        try:
            manifest = _read_json(p["manifest"])
        except VaultError:
            manifest = {}
        for asset in manifest.get("assets", []):
            if not isinstance(asset, dict):
                continue
            source_key = asset.get("source_key")
            workspace_path = asset.get("workspace_path")
            content_hash = asset.get("sha256")
            if isinstance(source_key, str) and isinstance(workspace_path, str) and isinstance(content_hash, str):
                values[source_key] = {"workspace_path": workspace_path, "sha256": content_hash}
    return values


def sync_project(project_root: Path) -> dict[str, int]:
    init_project(project_root)
    config = load_config(project_root)
    p = paths(project_root, config)
    state = load_state(p["state"])
    extensions = set(config["supported_extensions"])
    previous_assets = _previous_workspace_assets(p, state)
    rejected_hashes = {item for item in state.get("rejected_hashes", []) if isinstance(item, str)}
    assets: list[dict[str, Any]] = []
    current_assets: dict[str, dict[str, Any]] = {}
    current_paths: set[str] = set()
    current_hashes: set[str] = set()
    copied = 0

    for source in _asset_files(p["library"], extensions):
        relative = source.relative_to(p["library"])
        target = _safe_target_under(p["workspace"], relative, "Workspace asset path")
        target.parent.mkdir(parents=True, exist_ok=True)
        source_hash = sha256_file(source)
        should_copy = not target.is_file() or sha256_file(target) != source_hash
        if should_copy:
            shutil.copy2(source, target)
            copied += 1
        workspace_path = target.relative_to(p["project"]).as_posix()
        source_key = relative.as_posix()
        current_paths.add(workspace_path)
        current_hashes.add(source_hash)
        current_assets[source_key] = {"workspace_path": workspace_path, "sha256": source_hash}
        assets.append(
            {
                "source_key": source_key,
                "workspace_path": workspace_path,
                "sha256": source_hash,
                "size_bytes": source.stat().st_size,
            }
        )

    # A removed or replaced vault entry records its old bytes as rejected so a renamed
    # download event cannot silently resurrect it. Any bytes currently present in the
    # library win and clear the tombstone, which makes manual re-addition explicit.
    for source_key, previous in previous_assets.items():
        previous_hash = previous.get("sha256")
        current_hash = current_assets.get(source_key, {}).get("sha256")
        if isinstance(previous_hash, str) and previous_hash != current_hash:
            rejected_hashes.add(previous_hash)
    rejected_hashes.difference_update(current_hashes)

    removed = 0
    previous_paths = {
        item.get("workspace_path")
        for item in previous_assets.values()
        if isinstance(item, dict) and isinstance(item.get("workspace_path"), str)
    }
    for previous in sorted(previous_paths - current_paths):
        candidate = _safe_workspace_candidate(p["project"], p["workspace"], previous)
        if candidate is not None and candidate.is_file():
            candidate.unlink()
            removed += 1

    if p["workspace"].is_dir():
        for directory in sorted(
            (item for item in p["workspace"].rglob("*") if item.is_dir()),
            key=lambda item: len(item.parts),
            reverse=True,
        ):
            try:
                directory.rmdir()
            except OSError:
                pass

    manifest = {
        "schema_version": 2,
        "authority": "local-vault-filesystem",
        "vault_local_only": True,
        "workspace_local_only": True,
        "workspace_root": _safe_relative(config["workspace_root"], "workspace_root").as_posix(),
        "assets": assets,
    }
    _write_json(p["manifest"], manifest)
    state["last_workspace_assets"] = current_assets
    state["rejected_hashes"] = sorted(rejected_hashes)
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
    rejected_hashes = {item for item in state.get("rejected_hashes", []) if isinstance(item, str)}
    source_state = state.get("download_sources")
    if not isinstance(source_state, dict):
        source_state = {}
    imported = 0
    baselined = 0
    rejected = 0

    for source_arg in sources:
        source = source_arg.expanduser().resolve()
        if _paths_overlap(source, p["library"]) or _paths_overlap(source, p["workspace"]):
            raise VaultError(
                f"Download source overlaps the active vault library or local workspace and could recurse: {source}"
            )
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
            seen.add(event_id)
            if content_hash in rejected_hashes:
                rejected += 1
                continue
            day = datetime.now().astimezone().date().isoformat()
            import_root = p["library"] / "gpt-imports" / day
            import_root.mkdir(parents=True, exist_ok=True)
            destination = _import_destination(import_root, candidate, content_hash)
            if not destination.exists():
                shutil.copy2(candidate, destination)
                imported += 1
        source_state[source_key] = {"initialized": True}

    state["download_sources"] = source_state
    state["seen_download_events"] = sorted(seen)
    state["rejected_hashes"] = sorted(rejected_hashes)
    _write_json(p["state"], state)
    sync_project(project_root)
    return {"imported": imported, "baselined": baselined, "rejected": rejected}


def promote_asset(project_root: Path, source_key_text: str, target_text: str) -> dict[str, str]:
    init_project(project_root)
    config = load_config(project_root)
    p = paths(project_root, config)
    extensions = set(config["supported_extensions"])
    source_key = _safe_relative(source_key_text, "source_key")
    target_relative = _safe_relative(target_text, "target")
    source = p["library"] / source_key
    if source.is_symlink() or not source.is_file():
        raise VaultError(f"Vault source does not exist as a regular file: {source_key.as_posix()}")
    if not _supported(source, extensions):
        raise VaultError(f"Vault source uses an unsupported extension: {source_key.as_posix()}")

    destination = _safe_target_under(p["promotion"], target_relative, "Promoted asset path")
    if _inside(p["workspace"], destination) or _inside(p["vault"], destination):
        raise VaultError("Promoted asset target must stay outside local-only vault/workspace paths")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_hash = sha256_file(source)
    if destination.exists():
        if not destination.is_file() or sha256_file(destination) != source_hash:
            raise VaultError(f"Promotion target already exists with different content: {destination}")
    else:
        shutil.copy2(source, destination)
    return {
        "source_key": source_key.as_posix(),
        "promoted_path": destination.relative_to(p["project"]).as_posix(),
        "sha256": source_hash,
    }


def _git_path_list(project: Path, *args: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(project), *args, "-z"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise VaultError(f"Cannot inspect project files with git: {error}") from error
    if result.returncode != 0:
        raise VaultError(f"Cannot inspect project files with git: {result.stderr.strip()}")
    return [item for item in result.stdout.split("\0") if item]


def _project_reference_candidates(p: dict[str, Path]) -> list[Path]:
    project = p["project"]
    git_marker = project / ".git"
    if git_marker.exists():
        tracked = _git_path_list(project, "ls-files")
        untracked = _git_path_list(project, "ls-files", "--others", "--exclude-standard")
        candidates = [project / item for item in sorted(set(tracked + untracked))]
    else:
        candidates = [item for item in project.rglob("*") if item.is_file()]

    result_paths: list[Path] = []
    for candidate in candidates:
        if candidate.suffix.casefold() not in GODOT_TEXT_SUFFIXES:
            continue
        if _inside(p["vault"], candidate) or _inside(p["workspace"], candidate):
            continue
        result_paths.append(candidate)
    return result_paths


def check_repo_references(project_root: Path) -> list[str]:
    config = load_config(project_root)
    p = paths(project_root, config)
    workspace_ref = "res://" + Path(config["workspace_root"]).as_posix().rstrip("/") + "/"
    violations: list[str] = []
    for candidate in _project_reference_candidates(p):
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if workspace_ref in text:
            violations.append(candidate.relative_to(p["project"]).as_posix())
    if violations:
        joined = ", ".join(sorted(violations))
        raise VaultError(
            f"Project Godot files reference the local-only workspace {workspace_ref}: {joined}. "
            "Promote the asset first and reference the promoted path."
        )
    return violations


def watch_downloads(project_root: Path, sources: list[Path], interval: float, include_existing: bool, once: bool) -> None:
    first = True
    while True:
        result = pull_downloads(project_root, sources, include_existing=include_existing if first else True)
        print(
            f"download scan: imported={result['imported']} baselined={result['baselined']} rejected={result['rejected']}",
            flush=True,
        )
        if once:
            return
        first = False
        time.sleep(interval)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create the project-local vault/workspace and gitignore rules")
    init.add_argument("--project-root", type=Path, required=True)

    sync = sub.add_parser("sync", help="Mirror the current vault library into the local Godot workspace")
    sync.add_argument("--project-root", type=Path, required=True)

    pull = sub.add_parser("pull-downloads", help="Import new downloads into the local vault, then sync")
    pull.add_argument("--project-root", type=Path, required=True)
    pull.add_argument("--source", type=Path, action="append", required=True)
    pull.add_argument("--include-existing", action="store_true", help="Import files already present on the first scan")

    watch = sub.add_parser("watch", help="Continuously bridge newly downloaded images into the local vault")
    watch.add_argument("--project-root", type=Path, required=True)
    watch.add_argument("--source", type=Path, action="append", required=True)
    watch.add_argument("--interval", type=float, default=2.0)
    watch.add_argument("--include-existing", action="store_true")
    watch.add_argument("--once", action="store_true", help=argparse.SUPPRESS)

    promote = sub.add_parser("promote", help="Explicitly copy one vault asset into the tracked project asset area")
    promote.add_argument("--project-root", type=Path, required=True)
    promote.add_argument("--source-key", required=True, help="Path relative to .asset-vault/library")
    promote.add_argument("--target", required=True, help="Path relative to promotion_root (default: assets)")

    check = sub.add_parser("check", help="Reject project Godot references to the local-only workspace")
    check.add_argument("--project-root", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "init":
            init_project(args.project_root)
            print("Project asset vault initialized")
        elif args.command == "sync":
            result = sync_project(args.project_root)
            print(
                f"Asset vault synced: assets={result['assets']} copied={result['copied']} removed={result['removed']}"
            )
        elif args.command == "pull-downloads":
            result = pull_downloads(args.project_root, args.source, include_existing=args.include_existing)
            print(
                "Downloaded images processed: "
                f"imported={result['imported']} baselined={result['baselined']} rejected={result['rejected']}"
            )
        elif args.command == "watch":
            if args.interval <= 0:
                raise VaultError("--interval must be greater than zero")
            watch_downloads(args.project_root, args.source, args.interval, args.include_existing, args.once)
        elif args.command == "promote":
            result = promote_asset(args.project_root, args.source_key, args.target)
            print(
                f"Promoted asset: {result['source_key']} -> {result['promoted_path']} sha256={result['sha256']}"
            )
        elif args.command == "check":
            check_repo_references(args.project_root)
            print("Asset vault reference check: PASS")
        return 0
    except (OSError, VaultError) as error:
        print(f"Project asset vault failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
