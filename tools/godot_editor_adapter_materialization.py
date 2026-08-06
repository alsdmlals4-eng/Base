from __future__ import annotations

import hashlib
import inspect
import shutil
from pathlib import Path
from typing import Any

from tools.validate_godot_live_editor_contract_v2 import (
    canonical_json_sha256,
    validate_contract_pair,
)


ADDON_RELATIVE = Path(
    "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"
)
HISTORICAL_PILOT_ONLY = "HISTORICAL_BASE_ADAPTER_PILOT_ONLY"
_ACTIVE_ADOPTION_ERROR = "BASE_ADAPTER_ACTIVE_ADOPTION_FORBIDDEN"
_ALLOWED_HISTORICAL_CALLERS = frozenset(
    {
        "materialize_godot_editor_adapter_pilot.py",
        "godot_project_pilot_workspace.py",
    }
)


def _require_historical_pilot_caller() -> None:
    """Fail closed outside the retained historical Pilot harnesses.

    This is an accidental-adoption guard, not an authentication boundary. Current
    projects route Godot authoring through HiGodot; these helpers remain only so
    previously recorded Base adapter evidence can still be reproduced.
    """

    callers = {
        Path(frame.filename).name
        for frame in inspect.stack()[2:8]
    }
    if callers.isdisjoint(_ALLOWED_HISTORICAL_CALLERS):
        raise RuntimeError(f"{_ACTIVE_ADOPTION_ERROR}: {HISTORICAL_PILOT_ONLY}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _closed_schema(
    properties: dict[str, Any],
    required: list[str],
) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def build_capabilities() -> list[dict[str, Any]]:
    inspect_input = _closed_schema({}, [])
    inspect_output = _closed_schema(
        {
            "scene_path": {"type": "string", "pattern": "^res://"},
            "root_name": {"type": "string", "minLength": 1},
            "child_count": {"type": "integer", "minimum": 0},
            "dirty_state": {"enum": ["CLEAN", "DIRTY"]},
            "target_revision": {"type": "string", "minLength": 1},
            "target_content_sha256": {
                "anyOf": [
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    {"type": "null"},
                ]
            },
        },
        [
            "scene_path",
            "root_name",
            "child_count",
            "dirty_state",
            "target_revision",
            "target_content_sha256",
        ],
    )
    rename_input = _closed_schema(
        {
            "node_path": {"type": "string", "minLength": 1},
            "new_name": {"type": "string", "minLength": 1, "maxLength": 128},
            "save_mode": {"enum": ["KEEP_DIRTY", "SAVE_CURRENT_SCENE"]},
        },
        ["node_path", "new_name", "save_mode"],
    )
    rename_output = _closed_schema(
        {
            "scene_path": {"type": "string", "pattern": "^res://"},
            "node_path": {"type": "string", "minLength": 1},
            "old_name": {"type": "string", "minLength": 1},
            "new_name": {"type": "string", "minLength": 1},
            "save_mode": {"enum": ["KEEP_DIRTY", "SAVE_CURRENT_SCENE"]},
            "dirty_state": {"enum": ["CLEAN", "DIRTY"]},
            "saved_scene_sha256": {
                "anyOf": [
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    {"type": "null"},
                ]
            },
        },
        [
            "scene_path",
            "node_path",
            "old_name",
            "new_name",
            "save_mode",
            "dirty_state",
            "saved_scene_sha256",
        ],
    )
    inspect_capability = {
        "capability_id": "scene.inspect",
        "description": "Inspect the active edited scene without mutation.",
        "execution_path": "EDITOR_PLUGIN",
        "effect_kind": "READ_ONLY",
        "idempotency": "NOT_APPLICABLE",
        "approval_policy": "NOT_REQUIRED",
        "execution_mode": "SYNCHRONOUS",
        "rollback_policy": "NOT_APPLICABLE",
        "input_schema": inspect_input,
        "output_schema": inspect_output,
        "input_schema_sha256": canonical_json_sha256(inspect_input),
        "output_schema_sha256": canonical_json_sha256(inspect_output),
        "path_access": {
            "read_roots": ["res://"],
            "write_roots": [],
            "artifact_root": "artifacts/",
        },
        "precondition_policy": "REQUIRED",
        "retry_policy": {
            "automatic": True,
            "maximum_attempts": 2,
            "requires_ledger": False,
        },
        "timeout_policy": {
            "milliseconds": 10000,
            "unknown_outcome": "SAFE_TO_RETRY",
        },
        "evidence_outputs": ["ENGINE_STATE"],
        "unsupported_states": ["IMPORTING", "NO_EDITED_SCENE"],
    }
    rename = {
        "capability_id": "node.rename",
        "description": "Rename one node under the active edited scene root.",
        "execution_path": "EDITOR_PLUGIN",
        "effect_kind": "MUTATION",
        "idempotency": "IDEMPOTENT",
        "approval_policy": "REQUIRED",
        "execution_mode": "SYNCHRONOUS",
        "rollback_policy": "EDITOR_UNDO_REDO",
        "input_schema": rename_input,
        "output_schema": rename_output,
        "input_schema_sha256": canonical_json_sha256(rename_input),
        "output_schema_sha256": canonical_json_sha256(rename_output),
        "path_access": {
            "read_roots": ["res://"],
            "write_roots": ["res://"],
            "artifact_root": "artifacts/",
        },
        "precondition_policy": "REQUIRED",
        "retry_policy": {
            "automatic": False,
            "maximum_attempts": 1,
            "requires_ledger": True,
        },
        "timeout_policy": {
            "milliseconds": 10000,
            "unknown_outcome": "RECONCILE_BEFORE_RETRY",
        },
        "evidence_outputs": ["ENGINE_STATE", "LOG"],
        "unsupported_states": ["IMPORTING", "NO_EDITED_SCENE"],
    }
    return [inspect_capability, rename]


def build_configured_manifest(
    destination: Path,
    project_godot_sha256: str,
) -> dict[str, Any]:
    _require_historical_pilot_caller()
    normalized_project_path = Path(destination).resolve().as_posix()
    fingerprint = hashlib.sha256(
        f"{normalized_project_path}\n{project_godot_sha256}".encode("utf-8")
    ).hexdigest()
    capabilities = build_capabilities()
    manifest = {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
        "configuration_state": "CONFIGURED",
        "contract_version": "2.0.0",
        "adapter_version": "2.0.0",
        "project_identity": {
            "normalized_project_path": normalized_project_path,
            "project_godot_sha256": project_godot_sha256,
            "project_fingerprint": fingerprint,
        },
        "engine_compatibility": {
            "detected_version": "4.7.1.stable.official.a13da4feb",
            "minimum_version": "4.7.0",
            "maximum_exclusive_version": "4.8.0",
        },
        "tool_adoption": {
            "source": "base-project-local-historical-pilot",
            "exact_version": "2.0.0",
            "telemetry_policy": "DISABLED",
            "external_data_policy": "DENY_BY_DEFAULT",
            "uninstall_procedure": "addons/base_live_editor_adapter/README.md",
            "rollback_reference": "addons/base_live_editor_adapter/README.md",
        },
        "transport": {
            "kind": "PROJECT_DEFINED",
            "enabled": True,
            "bind_host": None,
            "endpoint_identity": "in-process-editor-plugin",
            "protocol_profile": "GENERIC",
            "protocol_version": "in-process-1.0",
            "access_control": {
                "authentication_mode": "NOT_APPLICABLE",
                "origin_policy": "NOT_APPLICABLE",
                "session_binding": "NOT_APPLICABLE",
                "os_access_control": "CURRENT_USER_ONLY",
            },
        },
        "catalog": {
            "generated_at": "2026-08-05T00:00:00Z",
            "sha256": canonical_json_sha256(capabilities),
            "freshness_state": "FRESH",
        },
        "project_test_framework": {
            "state": "NOT_CONFIGURED",
            "runner_capability_id": None,
        },
        "capabilities": capabilities,
        "validation": {
            "contract_state": "CONTRACT_PASS",
            "execution_state": "NOT_RUN",
            "runtime_state": "NOT_RUN",
            "physical_input_state": "NOT_RUN",
            "human_state": "HUMAN_NOT_RUN",
        },
    }
    errors = validate_contract_pair(manifest, mode="AUTHORIZE")
    if errors:
        raise ValueError(f"materialized manifest invalid: {errors}")
    return manifest


def copy_canonical_addon(base_root: Path, destination_project: Path) -> Path:
    _require_historical_pilot_caller()
    source = Path(base_root).resolve() / ADDON_RELATIVE
    destination = (
        Path(destination_project).resolve()
        / "addons/base_live_editor_adapter"
    )
    if not source.is_dir():
        raise FileNotFoundError(f"missing canonical addon: {source}")
    if destination.exists():
        raise FileExistsError(f"adapter destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("*.uid"))
    for generated in destination.rglob("*.uid"):
        generated.unlink()
    return destination


__all__ = [
    "HISTORICAL_PILOT_ONLY",
    "build_capabilities",
    "build_configured_manifest",
    "copy_canonical_addon",
    "sha256_file",
]
