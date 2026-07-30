#!/usr/bin/env python3
"""Base v9.1 canonical project adapter generation and fail-closed validation."""

from __future__ import annotations

import fnmatch
import hashlib
import html
import json
import re
import subprocess
import unicodedata
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
CANDIDATE_LOCK_PATH = Path("base-v9.1.lock.json")
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


def normalized_skill_body_hash(raw: bytes) -> str:
    text = raw.decode("utf-8")
    normalized = "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"))
    return sha256_bytes((normalized.strip() + "\n").encode("utf-8"))


def load_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"Cannot read JSON object {path}: {error}") from error
    if not isinstance(data, dict):
        raise ContractError(f"JSON root must be an object: {path}")
    return data


def safe_repository_path(root: Path, value: str | Path, label: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ContractError(f"Unsafe {label} path escapes its approved repository root: {value}")
    root_resolved = root.resolve()
    current = root_resolved
    for part in relative.parts:
        if part in {"", "."}:
            continue
        current = current / part
        if current.is_symlink():
            raise ContractError(f"Unsafe symlink traversal in {label} path: {value}")
        if current.exists():
            attributes = getattr(current.stat(follow_symlinks=False), "st_file_attributes", 0)
            if attributes & 0x400:
                raise ContractError(f"Unsafe reparse-point traversal in {label} path: {value}")
    resolved = current.resolve(strict=False)
    if not resolved.is_relative_to(root_resolved):
        raise ContractError(f"Unsafe {label} path escapes its approved repository root: {value}")
    return current


def _normalized_path(value: str) -> str:
    return unicodedata.normalize("NFC", value.replace("\\", "/")).casefold()


def _protected_match(path: str, patterns: list[str]) -> bool:
    normalized = _normalized_path(path)
    return any(fnmatch.fnmatchcase(normalized, _normalized_path(pattern)) for pattern in patterns)


def _extract_protected_paths(raw: bytes, pointer: str, label: str) -> list[str]:
    try:
        value: Any = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(f"{label} is not valid UTF-8 JSON: {error}") from error
    if not pointer.startswith("/"):
        raise ContractError(f"{label} protected-path JSON Pointer is invalid: {pointer}")
    for encoded_token in pointer[1:].split("/"):
        token = encoded_token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise ContractError(f"{label} cannot extract protected paths at JSON Pointer {pointer}")
        value = value[token]
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item for item in value)
        or len(value) != len(set(value))
    ):
        raise ContractError(f"{label} protected paths must be a non-empty unique string list")
    return list(value)


def _protected_policy_hash(patterns: list[str]) -> str:
    return sha256_bytes(canonical_json(patterns))


def _commit_blob_bytes(repository: Path, commit: str, relative: str, label: str) -> bytes:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ContractError(f"Unsafe {label} path escapes its approved repository root: {relative}")
    tree = _git(repository, "ls-tree", commit, "--", path.as_posix())
    if tree.returncode or not tree.stdout.strip():
        raise ContractError(f"{label} is unavailable at {commit}:{path.as_posix()}")
    metadata = tree.stdout.split(None, 3)
    if len(metadata) < 3 or metadata[0] == "120000" or metadata[1] != "blob":
        raise ContractError(f"{label} is not a regular Git blob at {commit}:{path.as_posix()}")
    raw = _git_show_bytes(repository, commit, path.as_posix())
    if raw is None:
        raise ContractError(f"{label} is unavailable at {commit}:{path.as_posix()}")
    return raw


def _protected_policy_errors(
    project_root: Path,
    adapter: dict[str, Any],
    protected_base_override: str = "",
) -> list[str]:
    errors: list[str] = []
    patterns = adapter["protected_paths"]
    if not patterns or any(not re.sub(r"[*?\[\]!]", "", pattern).strip("./") for pattern in patterns):
        errors.append("Protected-path policy is nonsensical or has no intended coverage")
        return errors
    for pattern in patterns:
        relative = Path(pattern)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe protected-path pattern: {pattern}")
    tracked = _git(project_root, "ls-files", "-z")
    if tracked.returncode:
        errors.append("Git error while determining protected-path intended coverage")
    else:
        names = [item for item in tracked.stdout.split("\0") if item]
        if not any(_protected_match(name, patterns) for name in names):
            errors.append("Protected-path policy has no intended coverage in the project")
    baseline = adapter["protected_baseline"]
    protected_base = protected_base_override or baseline["commit"]
    if not _commit_exists(project_root, protected_base):
        errors.append(f"Protected baseline is not a valid project commit: {protected_base}")
        return errors
    source_type = baseline["policy_source_type"]
    source_path = baseline["policy_source_path"]
    if source_type == "CANONICAL_ADAPTER_SOURCE" and source_path != CANONICAL_ADAPTER.as_posix():
        errors.append("CANONICAL_ADAPTER_SOURCE must use skills/PROJECT_BASE_ADAPTER.json")
        return errors
    if source_type == "FIRST_MIGRATION_LEGACY_SOURCE" and source_path == CANONICAL_ADAPTER.as_posix():
        errors.append("FIRST_MIGRATION_LEGACY_SOURCE cannot claim the canonical adapter path")
        return errors
    try:
        baseline_raw = _commit_blob_bytes(
            project_root, protected_base, source_path, "Protected baseline policy source"
        )
        baseline_patterns = _extract_protected_paths(
            baseline_raw,
            baseline["protected_paths_pointer"],
            "Protected baseline policy source",
        )
    except ContractError as error:
        errors.append(str(error))
        return errors
    actual_policy_hash = _protected_policy_hash(baseline_patterns)
    if actual_policy_hash != baseline["policy_sha256"]:
        errors.append(
            "Protected baseline policy hash mismatch: "
            f"expected {baseline['policy_sha256']}, got {actual_policy_hash}"
        )
        return errors
    current_normalized = {_normalized_path(pattern) for pattern in patterns}
    missing = sorted(
        pattern for pattern in baseline_patterns if _normalized_path(pattern) not in current_normalized
    )
    if missing:
        errors.append(f"Protected-path policy weakening detected: {', '.join(missing)}")
    changed = _git(project_root, "diff", "--name-only", "--no-renames", "-z", protected_base, "--")
    untracked = _git(project_root, "ls-files", "--others", "--exclude-standard", "-z")
    if changed.returncode or untracked.returncode:
        errors.append("Git error while collecting protected tracked/untracked changes")
        return errors
    names = {item for item in (changed.stdout + untracked.stdout).split("\0") if item}
    violations = sorted(path for path in names if _protected_match(path, patterns))
    if violations:
        errors.append(f"Protected-path changes detected: {', '.join(violations)}")
    return errors


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


def _git_show_bytes(repository: Path, commit: str, relative: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit}:{relative}"],
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def _release_lock_contract(
    adapter: dict[str, Any], base_repository: Path
) -> tuple[list[str], dict[str, Any] | None, bytes | None]:
    errors: list[str] = []
    try:
        lock_path = safe_repository_path(base_repository, CANDIDATE_LOCK_PATH, "Base v9.1 release lock")
    except ContractError as error:
        return [str(error)], None, None
    try:
        lock = load_object(lock_path)
    except ContractError as error:
        return [f"Base v9.1 release lock unavailable: {error}"], None, None
    base_release = adapter["base_release"]
    expected_identity = {
        "repository": lock.get("repository"),
        "version": str(lock.get("release_line", "")).removeprefix("v"),
        "release_commit": lock.get("candidate_release_commit"),
        "release_evidence_commit": lock.get("candidate_release_evidence_commit"),
    }
    release_pin = expected_identity["release_commit"]
    evidence_pin = expected_identity["release_evidence_commit"]
    if not isinstance(release_pin, str) or not isinstance(evidence_pin, str):
        errors.append("Base v9.1 candidate release/evidence pins are null or inconsistent; refusing execution")
    elif not re.fullmatch(r"[0-9a-f]{40}", release_pin) or not re.fullmatch(r"[0-9a-f]{40}", evidence_pin):
        errors.append("Base v9.1 candidate release/evidence pins are malformed; refusing execution")
    for field, expected in expected_identity.items():
        if base_release.get(field) != expected:
            errors.append(
                f"Adapter {field} does not match Base v9.1 release lock: "
                f"expected {expected!r}, got {base_release.get(field)!r}"
            )
    if isinstance(release_pin, str) and isinstance(evidence_pin, str):
        if not _commit_exists(base_repository, release_pin):
            errors.append(f"Base v9.1 release lock pin is absent: {release_pin}")
        if not _commit_exists(base_repository, evidence_pin):
            errors.append(f"Base v9.1 release lock evidence pin is absent: {evidence_pin}")
        if (
            _commit_exists(base_repository, release_pin)
            and _commit_exists(base_repository, evidence_pin)
            and not _is_ancestor(base_repository, release_pin, evidence_pin)
        ):
            errors.append("Base v9.1 release lock pin is not an ancestor of its evidence pin")
    registry_lock = lock.get("candidate_registry")
    pinned_registry: bytes | None = None
    if not isinstance(registry_lock, dict):
        errors.append("Base v9.1 release lock candidate_registry is missing")
    else:
        path = registry_lock.get("path")
        expected_hash = registry_lock.get("sha256")
        if not isinstance(path, str) or not isinstance(expected_hash, str):
            errors.append("Base v9.1 candidate Registry path/hash is null or inconsistent")
        else:
            adapter_registry = adapter["skill_registry"]["base"]
            if adapter_registry != registry_lock:
                errors.append("Adapter pinned Base Registry path/hash does not match Base v9.1 release lock")
            if isinstance(evidence_pin, str):
                pinned_registry = _git_show_bytes(base_repository, evidence_pin, path)
                if pinned_registry is None:
                    errors.append(f"Pinned Base Registry blob is unavailable: {evidence_pin}:{path}")
                elif sha256_bytes(pinned_registry) != expected_hash:
                    errors.append("Pinned Base Registry hash does not match Base v9.1 release lock")
    return errors, lock, pinned_registry


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
        if route["status"] == "ACTIVE":
            effective[route["route_id"]] = {**route, "source": "BASE_SHARED", "target_route_id": route["route_id"]}
    for route in sorted(routing.get("project_routes", []), key=lambda item: item["route_id"]):
        if route["status"] == "ACTIVE":
            effective[route["route_id"]] = {**route, "source": "PROJECT_LOCAL", "target_route_id": route["route_id"]}
    return effective


def _alias_resolutions(routing: dict[str, Any]) -> dict[str, dict[str, Any]]:
    effective = _effective_routes(routing)
    graph = {item["alias"]: item["target"] for item in routing["aliases"]}
    resolved: dict[str, dict[str, Any]] = {}
    for alias in sorted(graph):
        current = graph[alias]
        seen = {alias}
        while current in graph and current not in seen:
            seen.add(current)
            current = graph[current]
        if current in effective:
            resolved[alias] = dict(effective[current])
    return resolved


def _sorted_routes(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (item.get("route_id", ""), item.get("skill_id", "")))


def _health_semantic_errors(
    project_root: Path, adapter: dict[str, Any], health: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    gates = health["critical_gates"]
    evidence = health["evidence"]
    evidence_lists: dict[str, list[dict[str, Any]]] = {
        "operating": evidence["operating"],
        "product": evidence["product"],
        "sheet": evidence["sheet"],
        **{f"gate:{gate}": records for gate, records in evidence["gates"].items()},
    }
    candidates: list[tuple[str, dict[str, Any], str | None, bool]] = []
    source_counts: dict[str, int] = {}
    id_counts: dict[str, int] = {}
    for category, records in evidence_lists.items():
        for record in records:
            record_id = str(record["id"])
            id_counts[record_id] = id_counts.get(record_id, 0) + 1
            source_key: str | None = None
            valid = True
            try:
                source = safe_repository_path(
                    project_root, str(record["source"]), "health evidence"
                )
            except ContractError as error:
                errors.append(str(error))
                valid = False
            else:
                source_key = _normalized_path(source.relative_to(project_root.resolve()).as_posix())
                source_counts[source_key] = source_counts.get(source_key, 0) + 1
                if not source.is_file():
                    errors.append(f"Health evidence source does not exist as a file: {record['source']}")
                    valid = False
                else:
                    actual_hash = sha256_file(source)
                    if actual_hash != record["sha256"]:
                        errors.append(
                            f"Health evidence raw-byte hash mismatch for {record['source']}: "
                            f"expected {record['sha256']}, got {actual_hash}"
                        )
                        valid = False
            candidates.append((category, record, source_key, valid))
    duplicate_sources = sorted(source for source, count in source_counts.items() if count > 1)
    duplicate_ids = sorted(record_id for record_id, count in id_counts.items() if count > 1)
    if duplicate_sources:
        errors.append(f"Duplicate evidence source records are forbidden: {', '.join(duplicate_sources)}")
    if duplicate_ids:
        errors.append(f"Duplicate evidence IDs are forbidden: {', '.join(duplicate_ids)}")
    verified: dict[str, list[dict[str, Any]]] = {category: [] for category in evidence_lists}
    for category, record, source_key, valid in candidates:
        if (
            valid
            and source_key is not None
            and source_counts.get(source_key) == 1
            and id_counts.get(str(record["id"])) == 1
        ):
            verified[category].append(record)
    statuses = set(gates.values())
    if "FAIL" in statuses:
        derived_verdict = "FAIL"
    elif "BLOCKED" in statuses:
        derived_verdict = "BLOCKED"
    elif "NOT_RUN" in statuses:
        derived_verdict = "PASS_WITH_NOT_RUN_GATES"
    else:
        derived_verdict = "PASS"
    if health["integrity_verdict"] != derived_verdict:
        errors.append(
            f"Integrity verdict must be {derived_verdict} for current gate statuses, "
            f"not {health['integrity_verdict']}"
        )
    for gate, status in gates.items():
        if status in {"PASS", "FAIL", "BLOCKED"} and not verified[f"gate:{gate}"]:
            errors.append(f"Gate {gate} status {status} requires verified unique evidence")
    operating_level = int(health["operating_maturity"].removeprefix("OM-L"))
    product_level = int(health["product_evidence_maturity"].removeprefix("PE-"))
    if operating_level > min(5, len(verified["operating"])):
        errors.append(f"{health['operating_maturity']} exceeds verified operating evidence cap")
    if product_level > min(5, len(verified["product"])):
        errors.append(f"{health['product_evidence_maturity']} exceeds verified product evidence cap")
    if adapter["gdd_sheet"]["sync_status"] == "CURRENT" and not verified["sheet"]:
        errors.append("CURRENT Sheet status requires verified unique Sheet evidence")
    return errors


def _snapshot(adapter: dict[str, Any], adapter_path: Path) -> dict[str, Any]:
    routing = adapter["routing"]
    return {
        "schema_version": 1,
        "artifact_role": "PROJECT_SKILL_SNAPSHOT",
        "generated": True,
        "source_registry": {
            "hash_definition": "RAW_FILE_BYTES_SHA256",
            "path": CANONICAL_ADAPTER.as_posix(),
            "sha256": sha256_file(adapter_path),
        },
        "base_registry": dict(adapter["skill_registry"]["base"]),
        "project_registry": dict(adapter["skill_registry"]["project"]),
        "base_routes": _sorted_routes(routing["base_routes"]),
        "project_routes": _sorted_routes(routing["project_routes"]),
        "inactive_routes": _sorted_routes(routing["inactive_routes"]),
        "aliases": sorted(routing["aliases"], key=lambda item: (item["alias"], item["target"])),
        "alias_resolutions": _alias_resolutions(routing),
        "effective_routes": _effective_routes(routing),
    }


def _compatibility_view(
    adapter: dict[str, Any], adapter_path: Path, view: Path, legacy_path: Path, legacy: dict[str, Any]
) -> dict[str, Any]:
    projection = dict(legacy)
    projection.update({
        "schema_version": 1,
        "artifact_role": "GENERATED_COMPATIBILITY_VIEW",
        "generated": True,
        "lifecycle": "ONE_CYCLE",
        "view_name": view.name,
        "canonical_source": CANONICAL_ADAPTER.as_posix(),
        "canonical_source_sha256": sha256_file(adapter_path),
        "hash_definition": "RAW_FILE_BYTES_SHA256",
        "legacy_source": legacy_path.as_posix(),
        "legacy_source_sha256": sha256_file(adapter_path.parent.parent / legacy_path),
        "base_release": adapter["base_release"],
        "project": adapter["project"],
        "routing_precedence": adapter["routing"]["precedence"],
    })
    return projection


def _dashboard(
    adapter: dict[str, Any], snapshot: dict[str, Any], health: dict[str, Any], release_lock: dict[str, Any]
) -> bytes:
    project = html.escape(str(adapter["project"]["repository"]))
    operating = html.escape(str(health["operating_maturity"]))
    product = html.escape(str(health["product_evidence_maturity"]))
    verdict = html.escape(str(health["integrity_verdict"]))
    gate_items = "".join(
        f'<li><strong>{html.escape(name)}</strong>: {html.escape(str(status))}</li>'
        for name, status in sorted(health["critical_gates"].items())
    )
    source_hash = snapshot["source_registry"]["sha256"]
    release = adapter["base_release"]
    release_items = "".join(
        f"<li><strong>{html.escape(label)}</strong>: {html.escape(str(value))}</li>"
        for label, value in (
            ("Repository", release["repository"]),
            ("Version", release["version"]),
            ("State", release_lock["release_state"]),
            ("Release pin", release["release_commit"]),
            ("Evidence pin", release["release_evidence_commit"]),
        )
    )
    route_counts = "".join(
        f"<li>{label}: {count}</li>"
        for label, count in (
            ("BASE_SHARED", len(snapshot["base_routes"])),
            ("PROJECT_LOCAL", len(snapshot["project_routes"])),
            ("INACTIVE", len(snapshot["inactive_routes"])),
            ("EFFECTIVE", len(snapshot["effective_routes"])),
        )
    )
    provenance = "".join(
        f"<li><strong>{html.escape(owner)}</strong>: {html.escape(source['path'])} @ "
        f"{html.escape(source['sha256'])}</li>"
        for owner, source in (
            ("Base Registry", snapshot["base_registry"]),
            ("Project Registry", snapshot["project_registry"]),
            ("Adapter", snapshot["source_registry"]),
        )
    )
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
    <section aria-labelledby="release"><h2 id="release">Base release identity</h2><ul>{release_items}</ul></section>
    <section aria-labelledby="routes"><h2 id="routes">Route counts</h2><ul>{route_counts}</ul></section>
    <section aria-labelledby="provenance"><h2 id="provenance">Hashes and provenance</h2><ul>{provenance}</ul></section>
    <section id="critical-gates" aria-labelledby="gates"><h2 id="gates">Critical gates</h2><ul>{gate_items}</ul></section>
    <section aria-labelledby="verdict"><h2 id="verdict">Integrity verdict</h2><strong>{verdict}</strong></section>
  </main>
  <footer><small>adapter RAW_FILE_BYTES_SHA256: {source_hash}</small></footer>
</body>
</html>
"""
    return document.encode("utf-8")


def build_artifacts(
    project_root: Path, base_repository: Path, *, prevalidated: bool = False
) -> dict[Path, bytes]:
    if not prevalidated:
        errors = validation_errors(project_root, base_repository, check_generated=False)
        if errors:
            raise ContractError("\n".join(errors))
    adapter_path = safe_repository_path(project_root, CANONICAL_ADAPTER, "canonical adapter")
    adapter = load_object(adapter_path)
    schema_errors = validate_schema(adapter, ADAPTER_SCHEMA, "PROJECT_BASE_ADAPTER")
    if schema_errors:
        raise ContractError("\n".join(schema_errors))
    health_path = safe_repository_path(project_root, HEALTH_PATH, "operating health")
    health = load_object(health_path)
    health_errors = validate_schema(health, HEALTH_SCHEMA, "PROJECT_OPERATING_HEALTH")
    if health_errors:
        raise ContractError("\n".join(health_errors))
    snapshot = _snapshot(adapter, adapter_path)
    snapshot_errors = validate_schema(snapshot, SNAPSHOT_SCHEMA, "PROJECT_SKILL_SNAPSHOT")
    if snapshot_errors:
        raise ContractError("\n".join(snapshot_errors))
    artifacts: dict[Path, bytes] = {
        safe_repository_path(project_root, SNAPSHOT_PATH, "snapshot output"): canonical_json(snapshot),
        safe_repository_path(project_root, DASHBOARD_PATH, "dashboard output"): _dashboard(
            adapter, snapshot, health, load_object(base_repository / CANDIDATE_LOCK_PATH)
        ),
    }
    requested_views = {Path(path) for path in adapter["compatibility"]["views"]}
    legacy_inputs = adapter["compatibility"]["legacy_inputs"]
    if set(legacy_inputs) != {path.as_posix() for path in requested_views}:
        raise ContractError("Compatibility views and real legacy_inputs must have identical keys")
    if not requested_views.issubset(set(COMPATIBILITY_VIEWS)):
        raise ContractError("Unsupported compatibility view requested")
    for view in sorted(requested_views):
        source_value = legacy_inputs[view.as_posix()]
        legacy_path = Path(source_value)
        legacy_absolute = safe_repository_path(project_root, legacy_path, "legacy compatibility input")
        output = safe_repository_path(project_root, view, "legacy compatibility output")
        if legacy_absolute == output:
            raise ContractError(f"Legacy compatibility input cannot equal generated output: {view.as_posix()}")
        legacy = load_object(legacy_absolute)
        artifacts[output] = canonical_json(_compatibility_view(adapter, adapter_path, view, legacy_path, legacy))
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
    try:
        adapter_path = safe_repository_path(project_root, CANONICAL_ADAPTER, "canonical adapter")
    except ContractError as error:
        return [str(error)]
    try:
        adapter = load_object(adapter_path)
    except ContractError as error:
        return [str(error)]
    errors.extend(validate_schema(adapter, ADAPTER_SCHEMA, "PROJECT_BASE_ADAPTER"))
    if errors:
        return errors

    lock_errors, release_lock, pinned_base_registry = _release_lock_contract(adapter, base_repository)
    errors.extend(lock_errors)

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
        try:
            path = safe_repository_path(root, contract["path"], f"{owner} Skill Registry")
        except ContractError as error:
            errors.append(str(error))
            continue
        if owner == "base":
            if pinned_base_registry is None:
                continue
            raw = pinned_base_registry
        else:
            if not path.is_file():
                errors.append(f"{owner} Skill Registry path does not exist: {contract['path']}")
                continue
            raw = path.read_bytes()
        actual = sha256_bytes(raw)
        if actual != contract["sha256"]:
            errors.append(
                f"{owner} Skill Registry hash mismatch: expected {contract['sha256']}, got {actual}; refusing execution"
            )
        try:
            registry_data = json.loads(raw.decode("utf-8"))
            if not isinstance(registry_data, dict):
                raise ContractError(f"JSON root must be an object: {path}")
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
        except (ContractError, UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(f"Cannot read pinned {owner} Registry {contract['path']}: {error}")

    routing = adapter["routing"]
    for key in ("base_routes", "project_routes", "inactive_routes"):
        duplicates = _route_duplicates(routing[key])
        if duplicates:
            errors.append(f"Duplicate route ID in {key}: {', '.join(sorted(duplicates))}")
    active_route_ids = {
        item["route_id"] for item in routing["base_routes"] + routing["project_routes"]
    }
    inactive_collisions = sorted(
        active_route_ids & {item["route_id"] for item in routing["inactive_routes"]}
    )
    if inactive_collisions:
        errors.append(
            f"inactive_routes collide with ACTIVE route IDs: {', '.join(inactive_collisions)}"
        )
    aliases = routing["aliases"]
    alias_names = [item["alias"] for item in aliases]
    if len(alias_names) != len(set(alias_names)):
        errors.append("Duplicate alias ID")
    cycle = _alias_cycle(aliases)
    if cycle:
        errors.append(f"Alias cycle: {' -> '.join(cycle)}")
    effective = _effective_routes(routing)
    alias_graph = {item["alias"]: item["target"] for item in aliases}
    for alias in sorted(alias_graph):
        if alias in effective:
            errors.append(f"Alias {alias} collides with an ACTIVE effective route")
            continue
        current = alias_graph[alias]
        seen = {alias}
        while current in alias_graph and current not in seen:
            seen.add(current)
            current = alias_graph[current]
        if current not in effective:
            errors.append(f"Dangling alias {alias} does not resolve to exactly one ACTIVE effective route")

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
            if entry.get("status") != "ACTIVE":
                errors.append(f"{owner} route {route['route_id']} references non-ACTIVE Skill ID {skill_id}")
            relative_skill = str(entry.get("path", ""))
            try:
                skill_path = safe_repository_path(root, relative_skill, f"{owner} Skill")
            except ContractError as error:
                errors.append(str(error))
                continue
            if owner == "base" and release_lock is not None:
                evidence_pin = release_lock.get("candidate_release_evidence_commit")
                if not isinstance(evidence_pin, str) or _git_show_bytes(root, evidence_pin, relative_skill) is None:
                    errors.append(f"Pinned Base Skill path does not exist: {relative_skill}")
            elif not skill_path.is_file():
                errors.append(f"{owner} Skill path does not exist: {relative_skill}")

    if "base" in registries and "project" in registries and release_lock is not None:
        base_index = _registry_index(registries["base"][1])
        project_index = _registry_index(registries["project"][1])
        duplicate_ids = sorted(set(base_index) & set(project_index))
        if duplicate_ids:
            errors.append(
                f"Duplicate Base/project Skill ID provenance is forbidden: {', '.join(duplicate_ids)}"
            )
        evidence_pin = release_lock.get("candidate_release_evidence_commit")
        base_hashes: dict[str, list[str]] = {}
        if isinstance(evidence_pin, str):
            for skill_id, entry in base_index.items():
                relative = str(entry.get("path", ""))
                raw = _git_show_bytes(base_repository, evidence_pin, relative)
                if raw is None:
                    errors.append(f"Pinned Base Skill body is unavailable: {skill_id} ({relative})")
                    continue
                try:
                    body_hash = normalized_skill_body_hash(raw)
                except UnicodeDecodeError:
                    errors.append(f"Pinned Base Skill body is not UTF-8: {skill_id} ({relative})")
                    continue
                base_hashes.setdefault(body_hash, []).append(skill_id)
        for skill_id, entry in project_index.items():
            try:
                project_body = safe_repository_path(
                    project_root, str(entry.get("path", "")), "project Skill body"
                )
            except ContractError as error:
                errors.append(str(error))
                continue
            if not project_body.is_file():
                continue
            try:
                body_hash = normalized_skill_body_hash(project_body.read_bytes())
            except UnicodeDecodeError:
                errors.append(f"Project Skill body is not UTF-8: {skill_id}")
                continue
            if body_hash in base_hashes:
                errors.append(
                    "Shared Skill body normalized-content duplication is forbidden: "
                    f"project {skill_id} duplicates Base {', '.join(sorted(base_hashes[body_hash]))}"
                )

    try:
        health_path = safe_repository_path(project_root, HEALTH_PATH, "operating health")
    except ContractError as error:
        errors.append(str(error))
        health_path = project_root / "__unsafe_operating_health__"
    if not health_path.is_file():
        errors.append(f"Project operating health path does not exist: {HEALTH_PATH.as_posix()}")
    else:
        try:
            health = load_object(health_path)
            health_schema_errors = validate_schema(health, HEALTH_SCHEMA, "PROJECT_OPERATING_HEALTH")
            errors.extend(health_schema_errors)
            if not health_schema_errors:
                errors.extend(_health_semantic_errors(project_root, adapter, health))
        except ContractError as error:
            errors.append(str(error))

    try:
        project_contract_root = safe_repository_path(project_root, str(adapter["project"]["root"]), "project root")
    except ContractError as error:
        errors.append(str(error))
        project_contract_root = project_root / "__unsafe_project_root__"
    if not project_contract_root.exists():
        errors.append(f"Project root path does not exist: {adapter['project']['root']}")
    for protected_path in adapter["protected_paths"]:
        if not any(token in protected_path for token in ("*", "?", "[")):
            try:
                required = safe_repository_path(project_root, protected_path, "protected")
            except ContractError as error:
                errors.append(str(error))
                continue
            if not required.exists():
                errors.append(f"Protected path does not exist: {protected_path}")
    errors.extend(_protected_policy_errors(project_root, adapter, protected_base))

    if check_generated and not errors:
        try:
            artifacts = build_artifacts(project_root, base_repository, prevalidated=True)
            mismatches = [path for path, content in artifacts.items() if not path.is_file() or path.read_bytes() != content]
            if mismatches:
                names = ", ".join(path.relative_to(project_root).as_posix() for path in mismatches)
                errors.append(f"Generated view manual modification or stale output detected: {names}")
        except ContractError as error:
            errors.append(str(error))
    return errors


def migrated_adapter(
    project_root: Path,
    base_repository: Path,
    legacy: dict[str, Any],
    legacy_source_path: str,
    release_commit: str,
    release_evidence_commit: str,
    protected_baseline_commit: str,
) -> dict[str, Any]:
    if not release_commit or not release_evidence_commit:
        raise ContractError("Explicit v9.1 release and release-evidence pins are required for migration")
    if not protected_baseline_commit:
        raise ContractError("Explicit protected baseline commit is required for migration")
    if not _commit_exists(project_root, protected_baseline_commit):
        raise ContractError("Explicit protected baseline is absent from the project repository")
    baseline_legacy_raw = _commit_blob_bytes(
        project_root,
        protected_baseline_commit,
        legacy_source_path,
        "First-migration legacy policy source",
    )
    baseline_protected_paths = _extract_protected_paths(
        baseline_legacy_raw,
        "/protected_paths",
        "First-migration legacy policy source",
    )
    try:
        baseline_legacy = json.loads(baseline_legacy_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(f"First-migration legacy policy source is invalid: {error}") from error
    if not isinstance(baseline_legacy, dict):
        raise ContractError("First-migration legacy policy source root must be an object")
    lock = load_object(base_repository / CANDIDATE_LOCK_PATH)
    expected_release = lock.get("candidate_release_commit")
    expected_evidence = lock.get("candidate_release_evidence_commit")
    if release_commit != expected_release or release_evidence_commit != expected_evidence:
        raise ContractError("Explicit migration pins do not match the Base v9.1 release lock")
    if not _commit_exists(base_repository, release_commit) or not _commit_exists(base_repository, release_evidence_commit):
        raise ContractError("Explicit migration pin is absent from the Base repository")
    if not _is_ancestor(base_repository, release_commit, release_evidence_commit):
        raise ContractError("Explicit migration release pin is not an ancestor of its evidence pin")
    registry_lock = lock.get("candidate_registry")
    if not isinstance(registry_lock, dict) or not isinstance(registry_lock.get("sha256"), str):
        raise ContractError("Base v9.1 release lock has no pinned candidate Registry")
    project_registry = safe_repository_path(project_root, "skills/SKILL_REGISTRY.json", "project Registry")
    if not project_registry.is_file():
        raise ContractError("Migration requires a project Skill Registry")
    project_info = baseline_legacy.get("project", {})
    return {
        "schema_version": 1,
        "artifact_role": "PROJECT_BASE_ADAPTER",
        "base_release": {
            "repository": str(lock.get("repository")),
            "version": "9.1.0",
            "release_commit": release_commit,
            "release_evidence_commit": release_evidence_commit,
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
            "base": dict(registry_lock),
            "project": {
                "path": "skills/SKILL_REGISTRY.json",
                "sha256": sha256_file(project_registry),
                "hash_definition": "RAW_FILE_BYTES_SHA256",
            },
        },
        "shared_overrides": {},
        "gdd_sheet": {"role": "USER_FACING_GDD_WORKSPACE", "sync_status": "NOT_CONFIGURED"},
        "protected_baseline": {
            "commit": protected_baseline_commit,
            "policy_source_type": "FIRST_MIGRATION_LEGACY_SOURCE",
            "policy_source_path": legacy_source_path,
            "protected_paths_pointer": "/protected_paths",
            "policy_sha256": _protected_policy_hash(baseline_protected_paths),
        },
        "protected_paths": baseline_protected_paths,
        "validators": list(baseline_legacy.get("validators", [])),
        "compatibility": {
            "cycle": "ONE_CYCLE",
            "views": [],
            "legacy_inputs": {},
        },
    }
