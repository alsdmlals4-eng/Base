from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
LOCK_REL_PATH = Path(".base-reuse/adoption-lock.json")
ALLOWED_STATES = {"enabled", "planned", "not_applicable", "deferred"}
MODULE_SOURCES = {
    "RM-TOOL-001": "tools/reuse_modules/data_schema_crossref_validator.py",
    "RM-SYS-001": "templates/reuse-modules/godot/grid_placement_rule_engine.gd",
    "RM-SYS-003": "templates/reuse-modules/godot/candidate_draft_weight_engine.gd",
    "RM-VIS-001": "templates/reuse-modules/godot/semantic_ui_skin_kit.gd",
    "RM-VIS-002": "templates/reuse-modules/godot/gameplay_symbol_atlas.gd",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative(value: str, *, field: str) -> str:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts or path.parts[0] == ".git":
        raise ValueError(f"unsafe {field}: {value!r}")
    return path.as_posix()


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    base_commit = manifest.get("base_source_commit")
    if not isinstance(base_commit, str) or not base_commit.strip():
        raise ValueError("base_source_commit must be a non-empty string")
    modules = manifest.get("modules")
    if not isinstance(modules, dict):
        raise ValueError("modules must be an object")

    normalized: dict[str, dict[str, Any]] = {}
    for module_id, raw_config in modules.items():
        if module_id not in MODULE_SOURCES:
            raise ValueError(f"unknown reusable module: {module_id}")
        if not isinstance(raw_config, dict):
            raise ValueError(f"module config must be an object: {module_id}")
        state = raw_config.get("state")
        if state not in ALLOWED_STATES:
            raise ValueError(f"invalid module state for {module_id}: {state!r}")

        config = dict(raw_config)
        config["state"] = state
        if state == "enabled":
            canonical_source = MODULE_SOURCES[module_id]
            source = _safe_relative(str(config.get("source", canonical_source)), field="source")
            if source != canonical_source:
                raise ValueError(
                    f"source for {module_id} must match Base canonical source {canonical_source!r}"
                )
            destination = _safe_relative(str(config.get("destination", "")), field="destination")
            config["source"] = source
            config["destination"] = destination
        normalized[module_id] = config

    return {
        "schema_version": SCHEMA_VERSION,
        "base_source_commit": base_commit.strip(),
        "modules": normalized,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("manifest root must be an object")
    return validate_manifest(document)


def _read_lock(project_root: Path) -> dict[str, Any] | None:
    lock_path = project_root / LOCK_REL_PATH
    if not lock_path.is_file():
        return None
    document = json.loads(lock_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return None
    return document


def _violation(module_id: str, code: str, message: str) -> dict[str, str]:
    return {"module_id": module_id, "code": code, "message": message}


def check_adoption(
    base_root: Path,
    project_root: Path,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    base_root = Path(base_root)
    project_root = Path(project_root)
    normalized = validate_manifest(manifest)
    lock = _read_lock(project_root)
    violations: list[dict[str, str]] = []
    checked: list[str] = []

    for module_id, config in sorted(normalized["modules"].items()):
        if config["state"] != "enabled":
            continue
        checked.append(module_id)
        source_path = base_root / config["source"]
        destination_path = project_root / config["destination"]
        if not source_path.is_file():
            violations.append(_violation(module_id, "SOURCE_MISSING", config["source"]))
            continue
        if not destination_path.is_file():
            violations.append(_violation(module_id, "DESTINATION_MISSING", config["destination"]))
            continue

        lock_entry = None
        if isinstance(lock, dict):
            lock_entry = lock.get("modules", {}).get(module_id)
        if not isinstance(lock_entry, dict):
            violations.append(_violation(module_id, "LOCK_ENTRY_MISSING", config["destination"]))
            continue

        current_hash = _sha256(destination_path)
        if current_hash != lock_entry.get("installed_sha256"):
            violations.append(
                _violation(module_id, "LOCAL_MODIFICATION", config["destination"])
            )
        source_hash = _sha256(source_path)
        if source_hash != lock_entry.get("source_sha256"):
            violations.append(_violation(module_id, "SOURCE_DRIFT", config["source"]))
        if config["destination"] != lock_entry.get("destination"):
            violations.append(
                _violation(module_id, "DESTINATION_DRIFT", config["destination"])
            )

    if isinstance(lock, dict) and lock.get("base_source_commit") != normalized["base_source_commit"]:
        violations.append(
            _violation(
                "_manifest",
                "BASE_COMMIT_DRIFT",
                f"lock={lock.get('base_source_commit')} manifest={normalized['base_source_commit']}",
            )
        )

    return {
        "ok": not violations,
        "mode": "check",
        "checked_modules": checked,
        "violations": violations,
    }


def apply_adoption(
    base_root: Path,
    project_root: Path,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    base_root = Path(base_root)
    project_root = Path(project_root)
    normalized = validate_manifest(manifest)
    existing_lock = _read_lock(project_root) or {}
    existing_entries = existing_lock.get("modules", {}) if isinstance(existing_lock, dict) else {}
    violations: list[dict[str, str]] = []
    operations: list[tuple[str, Path, Path, str]] = []

    for module_id, config in sorted(normalized["modules"].items()):
        if config["state"] != "enabled":
            continue
        source_path = base_root / config["source"]
        destination_path = project_root / config["destination"]
        if not source_path.is_file():
            violations.append(_violation(module_id, "SOURCE_MISSING", config["source"]))
            continue

        source_hash = _sha256(source_path)
        if destination_path.exists():
            lock_entry = existing_entries.get(module_id) if isinstance(existing_entries, dict) else None
            if not isinstance(lock_entry, dict):
                violations.append(
                    _violation(
                        module_id,
                        "REFUSE_OVERWRITE_UNTRACKED_FILE",
                        config["destination"],
                    )
                )
                continue
            current_hash = _sha256(destination_path)
            if current_hash != lock_entry.get("installed_sha256"):
                violations.append(
                    _violation(
                        module_id,
                        "REFUSE_OVERWRITE_LOCAL_MODIFICATION",
                        config["destination"],
                    )
                )
                continue
            if config["destination"] != lock_entry.get("destination"):
                violations.append(
                    _violation(module_id, "REFUSE_DESTINATION_CHANGE", config["destination"])
                )
                continue
        operations.append((module_id, source_path, destination_path, source_hash))

    if violations:
        return {
            "ok": False,
            "mode": "apply",
            "applied_modules": [],
            "violations": violations,
        }

    lock_entries: dict[str, dict[str, str]] = {}
    for module_id, source_path, destination_path, source_hash in operations:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        installed_hash = _sha256(destination_path)
        lock_entries[module_id] = {
            "source": source_path.relative_to(base_root).as_posix(),
            "destination": destination_path.relative_to(project_root).as_posix(),
            "source_sha256": source_hash,
            "installed_sha256": installed_hash,
        }

    lock_document = {
        "schema_version": SCHEMA_VERSION,
        "base_source_commit": normalized["base_source_commit"],
        "modules": lock_entries,
    }
    lock_path = project_root / LOCK_REL_PATH
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps(lock_document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "mode": "apply",
        "applied_modules": sorted(lock_entries),
        "lock_path": LOCK_REL_PATH.as_posix(),
        "violations": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply/check Base reusable-module adoption safely")
    parser.add_argument("action", choices=("apply", "check"))
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--base-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    manifest = load_manifest(args.manifest)
    if args.action == "apply":
        report = apply_adoption(args.base_root, args.project_root, manifest)
    else:
        report = check_adoption(args.base_root, args.project_root, manifest)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
