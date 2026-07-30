#!/usr/bin/env python3
"""Base v9.1 canonical project adapter generation and fail-closed validation."""

from __future__ import annotations

import fnmatch
import hashlib
import html
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator


BASE_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SCHEMA = BASE_ROOT / "schemas/project-base-adapter-v1.schema.json"
SNAPSHOT_SCHEMA = BASE_ROOT / "schemas/project-skill-snapshot-v1.schema.json"
HEALTH_SCHEMA = BASE_ROOT / "schemas/project-operating-health-v1.schema.json"
CANONICAL_ADAPTER = Path("skills/PROJECT_BASE_ADAPTER.json")
HEALTH_PATH = Path("docs/PROJECT_OPERATING_HEALTH.json")
SNAPSHOT_PATH = Path("skills/PROJECT_SKILL_SNAPSHOT.json")
DASHBOARD_PATH = Path("docs/PROJECT_OPERATING_DASHBOARD.html")
COMPATIBILITY_VIEWS = (
    Path("skills/BASE_V9_ADAPTER.json"),
    Path("skills/PROJECT_BASE_SKILL_ADAPTER.json"),
    Path("skills/PROJECT_PATH_ADAPTER.json"),
)


class ContractError(ValueError):
    """A fail-closed project operating-contract violation."""


def canonical_json(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"Cannot read JSON object {path}: {error}") from error
    if not isinstance(data, dict):
        raise ContractError(f"JSON root must be an object: {path}")
    return data


def validate_schema(data: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    schema = load_object(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path))
    return [
        f"{label} {'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def _git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _commit_exists(repository: Path, commit: str) -> bool:
    return _git(repository, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def _is_ancestor(repository: Path, ancestor: str, descendant: str) -> bool:
    return _git(repository, "merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def _registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = registry.get("skills", [])
    if not isinstance(entries, list):
        return {}
    return {
        str(item.get("skill_id")): item
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("skill_id"), str)
    }


def _route_duplicates(routes: Iterable[dict[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for route in routes:
        route_id = str(route.get("route_id", ""))
        if route_id in seen:
            duplicates.add(route_id)
        seen.add(route_id)
    return duplicates


def _alias_cycle(aliases: list[dict[str, Any]]) -> list[str] | None:
    graph = {str(item.get("alias")): str(item.get("target")) for item in aliases}
    for origin in sorted(graph):
        trail: list[str] = []
        current = origin
        while current in graph:
            if current in trail:
                return trail[trail.index(current) :] + [current]
            trail.append(current)
            current = graph[current]
    return None


def _effective_routes(routing: dict[str, Any]) -> dict[str, dict[str, Any]]:
    effective: dict[str, dict[str, Any]] = {}
    for route in sorted(routing.get("base_routes", []), key=lambda item: item["route_id"]):
        effective[route["route_id"]] = {**route, "source": "BASE_SHARED"}
    for route in sorted(routing.get("project_routes", []), key=lambda item: item["route_id"]):
        effective[route["route_id"]] = {**route, "source": "PROJECT_LOCAL"}
    return effective


def _sorted_routes(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (item.get("route_id", ""), item.get("skill_id", "")))


def _snapshot(adapter: dict[str, Any], adapter_path: Path) -> dict[str, Any]:
    routing = adapter["routing"]
    return {
        "schema_version": 1,
        "artifact_role": "PROJECT_SKILL_SNAPSHOT",
        "generated": True,
        "source_registry": {
            "path": CANONICAL_ADAPTER.as_posix(),
            "sha256": sha256_file(adapter_path),
        },
        "base_registry": dict(adapter["skill_registry"]["base"]),
        "project_registry": dict(adapter["skill_registry"]["project"]),
        "base_routes": _sorted_routes(routing["base_routes"]),
        "project_routes": _sorted_routes(routing["project_routes"]),
        "inactive_routes": _sorted_routes(routing["inactive_routes"]),
        "aliases": sorted(routing["aliases"], key=lambda item: (item["alias"], item["target"])),
        "effective_routes": _effective_routes(routing),
    }


def _compatibility_view(adapter: dict[str, Any], adapter_path: Path, view: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_role": "GENERATED_COMPATIBILITY_VIEW",
        "generated": True,
        "lifecycle": "ONE_CYCLE",
        "view_name": view.name,
        "canonical_source": CANONICAL_ADAPTER.as_posix(),
        "canonical_source_sha256": sha256_file(adapter_path),
        "base_release": adapter["base_release"],
        "project": adapter["project"],
        "routing_precedence": adapter["routing"]["precedence"],
    }


def _dashboard(adapter: dict[str, Any], health: dict[str, Any]) -> bytes:
    project = html.escape(str(adapter["project"]["repository"]))
    operating = html.escape(str(health["operating_maturity"]))
    product = html.escape(str(health["product_evidence_maturity"]))
    verdict = html.escape(str(health["integrity_verdict"]))
    gate_items = "".join(
        f'<li><strong>{html.escape(name)}</strong>: {html.escape(str(status))}</li>'
        for name, status in sorted(health["critical_gates"].items())
    )
    source_hash = sha256_bytes(canonical_json(adapter))
    document = f"""<!doctype html>
<html lang="ko" data-generated="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{project} operating health</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
    body {{ margin: 0 auto; max-width: 72rem; padding: 1.5rem; line-height: 1.55; }}
    .axes {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1rem; }}
    section {{ border: 1px solid currentColor; border-radius: .5rem; padding: 1rem; }}
    strong {{ overflow-wrap: anywhere; }}
  </style>
</head>
<body>
  <header><h1>{project}</h1><p>Deterministic generated operating view. Layout review targets: 1280x720 and 1920x1080.</p></header>
  <main>
    <div class="axes" aria-label="Independent maturity axes">
      <section aria-labelledby="om"><h2 id="om">Operating maturity</h2><strong>{operating}</strong></section>
      <section aria-labelledby="pe"><h2 id="pe">Product evidence maturity</h2><strong>{product}</strong></section>
    </div>
    <section id="critical-gates" aria-labelledby="gates"><h2 id="gates">Critical gates</h2><ul>{gate_items}</ul></section>
    <section aria-labelledby="verdict"><h2 id="verdict">Integrity verdict</h2><strong>{verdict}</strong></section>
  </main>
  <footer><small>source sha256: {source_hash}</small></footer>
</body>
</html>
"""
    return document.encode("utf-8")


def build_artifacts(project_root: Path, base_repository: Path) -> dict[Path, bytes]:
    del base_repository  # Source paths and hashes are carried by the canonical adapter.
    adapter_path = project_root / CANONICAL_ADAPTER
    adapter = load_object(adapter_path)
    schema_errors = validate_schema(adapter, ADAPTER_SCHEMA, "PROJECT_BASE_ADAPTER")
    if schema_errors:
        raise ContractError("\n".join(schema_errors))
    health_path = project_root / HEALTH_PATH
    health = load_object(health_path)
    health_errors = validate_schema(health, HEALTH_SCHEMA, "PROJECT_OPERATING_HEALTH")
    if health_errors:
        raise ContractError("\n".join(health_errors))
    snapshot = _snapshot(adapter, adapter_path)
    snapshot_errors = validate_schema(snapshot, SNAPSHOT_SCHEMA, "PROJECT_SKILL_SNAPSHOT")
    if snapshot_errors:
        raise ContractError("\n".join(snapshot_errors))
    artifacts: dict[Path, bytes] = {
        project_root / SNAPSHOT_PATH: canonical_json(snapshot),
        project_root / DASHBOARD_PATH: _dashboard(adapter, health),
    }
    requested_views = {Path(path) for path in adapter["compatibility"]["views"]}
    if requested_views != set(COMPATIBILITY_VIEWS):
        raise ContractError("Compatibility views must be exactly the three one-cycle Base v9 views")
    for view in COMPATIBILITY_VIEWS:
        artifacts[project_root / view] = canonical_json(_compatibility_view(adapter, adapter_path, view))
    return artifacts


def write_or_check_artifacts(
    project_root: Path,
    base_repository: Path,
    *,
    check: bool,
) -> list[Path]:
    artifacts = build_artifacts(project_root, base_repository)
    mismatches = [path for path, content in artifacts.items() if not path.is_file() or path.read_bytes() != content]
    if check and mismatches:
        names = ", ".join(path.relative_to(project_root).as_posix() for path in mismatches)
        raise ContractError(f"Generated view manual modification or stale output detected: {names}")
    if not check:
        for path in mismatches:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(artifacts[path])
    return mismatches


def validation_errors(
    project_root: Path,
    base_repository: Path,
    *,
    protected_base: str = "",
    check_generated: bool = True,
) -> list[str]:
    errors: list[str] = []
    adapter_path = project_root / CANONICAL_ADAPTER
    try:
        adapter = load_object(adapter_path)
    except ContractError as error:
        return [str(error)]
    errors.extend(validate_schema(adapter, ADAPTER_SCHEMA, "PROJECT_BASE_ADAPTER"))
    if errors:
        return errors

    base_release = adapter["base_release"]
    release_commit = base_release["release_commit"]
    evidence_commit = base_release["release_evidence_commit"]
    if not _commit_exists(base_repository, release_commit):
        errors.append(f"Base release pin is stale or absent ({release_commit}); refusing execution")
    if not _commit_exists(base_repository, evidence_commit):
        errors.append(f"Base release evidence pin mismatch ({evidence_commit}); refusing execution")
    if (
        _commit_exists(base_repository, release_commit)
        and _commit_exists(base_repository, evidence_commit)
        and not _is_ancestor(base_repository, release_commit, evidence_commit)
    ):
        errors.append("Base release pin is not an ancestor of release evidence; refusing execution")

    registries: dict[str, tuple[Path, dict[str, Any]]] = {}
    for owner, root in (("base", base_repository), ("project", project_root)):
        contract = adapter["skill_registry"][owner]
        path = root / contract["path"]
        if not path.is_file():
            errors.append(f"{owner} Skill Registry path does not exist: {contract['path']}")
            continue
        actual = sha256_file(path)
        if actual != contract["sha256"]:
            errors.append(
                f"{owner} Skill Registry hash mismatch: expected {contract['sha256']}, got {actual}; refusing execution"
            )
        try:
            registry_data = load_object(path)
            entries = registry_data.get("skills", [])
            if isinstance(entries, list):
                ids = [
                    str(item.get("skill_id"))
                    for item in entries
                    if isinstance(item, dict) and isinstance(item.get("skill_id"), str)
                ]
                duplicate_ids = sorted({skill_id for skill_id in ids if ids.count(skill_id) > 1})
                if duplicate_ids:
                    errors.append(f"Duplicate Skill ID in {owner} Registry: {', '.join(duplicate_ids)}")
            registries[owner] = (path, registry_data)
        except ContractError as error:
            errors.append(str(error))

    routing = adapter["routing"]
    for key in ("base_routes", "project_routes", "inactive_routes"):
        duplicates = _route_duplicates(routing[key])
        if duplicates:
            errors.append(f"Duplicate route ID in {key}: {', '.join(sorted(duplicates))}")
    aliases = routing["aliases"]
    alias_names = [item["alias"] for item in aliases]
    if len(alias_names) != len(set(alias_names)):
        errors.append("Duplicate alias ID")
    cycle = _alias_cycle(aliases)
    if cycle:
        errors.append(f"Alias cycle: {' -> '.join(cycle)}")

    for owner, route_key, root in (
        ("base", "base_routes", base_repository),
        ("project", "project_routes", project_root),
    ):
        if owner not in registries:
            continue
        index = _registry_index(registries[owner][1])
        for route in routing[route_key]:
            skill_id = route["skill_id"]
            entry = index.get(skill_id)
            if entry is None:
                errors.append(f"{owner} route {route['route_id']} references absent Skill ID {skill_id}")
                continue
            skill_path = root / str(entry.get("path", ""))
            if not skill_path.is_file():
                errors.append(f"{owner} Skill path does not exist: {entry.get('path')}")

    if "base" in registries:
        for skill_id, entry in _registry_index(registries["base"][1]).items():
            relative = Path(str(entry.get("path", "")))
            project_copy = project_root / relative
            base_body = base_repository / relative
            if project_copy.is_file() and base_body.is_file() and project_copy.read_bytes() == base_body.read_bytes():
                errors.append(f"Shared Skill body duplication is forbidden: {skill_id} ({relative.as_posix()})")

    health_path = project_root / HEALTH_PATH
    if not health_path.is_file():
        errors.append(f"Project operating health path does not exist: {HEALTH_PATH.as_posix()}")
    else:
        try:
            errors.extend(validate_schema(load_object(health_path), HEALTH_SCHEMA, "PROJECT_OPERATING_HEALTH"))
        except ContractError as error:
            errors.append(str(error))

    project_contract_root = project_root / str(adapter["project"]["root"])
    if not project_contract_root.exists():
        errors.append(f"Project root path does not exist: {adapter['project']['root']}")
    for protected_path in adapter["protected_paths"]:
        if not any(token in protected_path for token in ("*", "?", "[")):
            if not (project_root / protected_path).exists():
                errors.append(f"Protected path does not exist: {protected_path}")

    if protected_base:
        changed = _git(project_root, "diff", "--name-only", protected_base, "--").stdout.splitlines()
        protected = adapter["protected_paths"]
        violations = sorted(
            path for path in changed if any(fnmatch.fnmatch(path.replace("\\", "/"), pattern) for pattern in protected)
        )
        if violations:
            errors.append(f"Protected-path changes detected: {', '.join(violations)}")

    if check_generated:
        try:
            write_or_check_artifacts(project_root, base_repository, check=True)
        except ContractError as error:
            errors.append(str(error))
    return errors


def migrated_adapter(
    project_root: Path,
    base_repository: Path,
    legacy: dict[str, Any],
) -> dict[str, Any]:
    base_registry = base_repository / "skills/SKILL_REGISTRY.json"
    project_registry = project_root / "skills/SKILL_REGISTRY.json"
    if not base_registry.is_file() or not project_registry.is_file():
        raise ContractError("Migration requires both Base and project Skill Registries")
    release_commit = str(legacy.get("base", {}).get("commit", ""))
    if not _commit_exists(base_repository, release_commit):
        raise ContractError("Legacy Base release pin is stale; refusing migration")
    evidence = _git(base_repository, "rev-parse", "HEAD")
    if evidence.returncode:
        raise ContractError("Cannot resolve Base release evidence commit")
    project_info = legacy.get("project", {})
    return {
        "schema_version": 1,
        "artifact_role": "PROJECT_BASE_ADAPTER",
        "base_release": {
            "repository": str(legacy.get("base", {}).get("repository", "alsdmlals4-eng/Base")),
            "version": "9.1.0",
            "release_commit": release_commit,
            "release_evidence_commit": evidence.stdout.strip(),
        },
        "project": {
            "repository": str(project_info.get("repository", "owner/project")),
            "engine": str(project_info.get("engine", "Godot 4.7")),
            "root": ".",
        },
        "routing": {
            "base_routes": [],
            "project_routes": [],
            "inactive_routes": [],
            "aliases": [],
            "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
        },
        "skill_registry": {
            "base": {"path": "skills/SKILL_REGISTRY.json", "sha256": sha256_file(base_registry)},
            "project": {"path": "skills/SKILL_REGISTRY.json", "sha256": sha256_file(project_registry)},
        },
        "shared_overrides": {},
        "gdd_sheet": {"role": "USER_FACING_GDD_WORKSPACE", "sync_status": "NOT_CONFIGURED"},
        "protected_paths": list(legacy.get("protected_paths", [])),
        "validators": list(legacy.get("validators", [])),
        "compatibility": {
            "cycle": "ONE_CYCLE",
            "views": [path.as_posix() for path in COMPATIBILITY_VIEWS],
        },
    }
