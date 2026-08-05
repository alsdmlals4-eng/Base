from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from jsonschema import Draft202012Validator

try:
    from tools import godot_live_editor_contract_v2_core as core
except ModuleNotFoundError:  # Direct execution: python tools/validate_...py
    import godot_live_editor_contract_v2_core as core


ContractKind = Literal["V1_AUDIT_ONLY", "V2"]
ROOT = Path(__file__).resolve().parents[1]
V1_CAPABILITY_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v1.schema.json"
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
_TERMINAL_TASK_STATES = {"COMPLETED", "FAILED", "CANCELLED", "STALE"}

canonical_json_sha256 = core.canonical_json_sha256
classify_contract_document = core.classify_contract_document
operation_request_material = core.operation_request_material


def _unique(errors: list[str]) -> list[str]:
    return list(dict.fromkeys(errors))


def _transport_is_safe(transport: Any) -> bool:
    if not isinstance(transport, Mapping):
        return False
    if transport.get("kind") != "PROJECT_DEFINED":
        return core._original_transport_is_safe(transport)

    access = transport.get("access_control")
    return (
        transport.get("enabled") is True
        and transport.get("bind_host") is None
        and isinstance(transport.get("endpoint_identity"), str)
        and bool(transport.get("endpoint_identity"))
        and isinstance(access, Mapping)
        and access.get("authentication_mode")
        in {"OS_PEER_CREDENTIAL", "NOT_APPLICABLE"}
        and access.get("origin_policy") == "NOT_APPLICABLE"
        and access.get("session_binding") == "NOT_APPLICABLE"
        and access.get("os_access_control") == "CURRENT_USER_ONLY"
    )


if not hasattr(core, "_original_transport_is_safe"):
    core._original_transport_is_safe = core._transport_is_safe
core._transport_is_safe = _transport_is_safe


def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]:
    return core.validate_manifest_semantics(manifest)


def validate_operation_semantics(
    manifest: Mapping[str, Any],
    envelope: Mapping[str, Any],
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    now: datetime | None = None,
) -> list[str]:
    errors = core.validate_operation_semantics(
        manifest,
        envelope,
        prior_operations=prior_operations,
        now=now,
    )

    task = envelope.get("task")
    result = envelope.get("result")
    instance = envelope.get("instance_identity")
    if (
        isinstance(task, Mapping)
        and task.get("state") in _TERMINAL_TASK_STATES
        and isinstance(result, Mapping)
        and isinstance(instance, Mapping)
    ):
        binding = task.get("result_binding")
        expected_identity = {
            "operation_id": envelope.get("operation_id"),
            "project_identity": envelope.get("project_identity"),
            "automation_service_instance_id": instance.get(
                "automation_service_instance_id"
            ),
            "task_id": task.get("task_id"),
        }
        identity_matches = isinstance(binding, Mapping) and all(
            binding.get(key) == value for key, value in expected_identity.items()
        )
        if identity_matches and binding.get("result_hash") != result.get("result_hash"):
            errors = [error for error in errors if error != "TASK_RESULT_STALE"]
            errors.append("TASK_RESULT_HASH_MISMATCH")

    return _unique(errors)


def _schema_errors(
    schema_path: Path,
    document: Mapping[str, Any],
    code: str,
) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [code] if list(validator.iter_errors(document)) else []


def validate_contract_pair(
    manifest: Mapping[str, Any],
    operation: Mapping[str, Any] | None = None,
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    mode: Literal["AUDIT", "AUTHORIZE"] = "AUTHORIZE",
    now: datetime | None = None,
) -> list[str]:
    kind = classify_contract_document(manifest)
    if kind == "V1_AUDIT_ONLY":
        if mode != "AUDIT" or operation is not None:
            return ["V1_MUTATION_AUTHORITY_REJECTED"]
        return _schema_errors(
            V1_CAPABILITY_SCHEMA,
            manifest,
            "V1_AUDIT_SCHEMA_INVALID",
        )

    errors = _schema_errors(
        CAPABILITY_SCHEMA_V2,
        manifest,
        "MANIFEST_SCHEMA_INVALID",
    )
    if not errors:
        errors.extend(validate_manifest_semantics(manifest))

    if operation is not None:
        operation_schema_errors = _schema_errors(
            OPERATION_SCHEMA_V2,
            operation,
            "OPERATION_SCHEMA_INVALID",
        )
        errors.extend(operation_schema_errors)
        if not operation_schema_errors:
            errors.extend(
                validate_operation_semantics(
                    manifest,
                    operation,
                    prior_operations=prior_operations,
                    now=now,
                )
            )
    return _unique(errors)


def _load_mapping(path: Path) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("JSON root must be an object")
    return payload


def _parse_now(value: str | None) -> datetime | None:
    if value is None:
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamp requires timezone")
    return parsed


def _emit(errors: list[str]) -> int:
    print(
        json.dumps(
            {"status": "PASS" if not errors else "FAIL", "errors": errors},
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Godot live-editor v2 contracts."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--operation", type=Path)
    parser.add_argument("--prior-operation", type=Path, action="append", default=[])
    parser.add_argument("--mode", choices=("AUDIT", "AUTHORIZE"), default="AUTHORIZE")
    parser.add_argument("--now")
    args = parser.parse_args()

    try:
        manifest = _load_mapping(args.manifest)
        operation = (
            _load_mapping(args.operation) if args.operation is not None else None
        )
        prior_operations = [
            _load_mapping(path) for path in args.prior_operation
        ]
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return _emit(["INPUT_JSON_INVALID"])

    try:
        now = _parse_now(args.now)
    except ValueError:
        return _emit(["INVALID_NOW_TIMESTAMP"])

    try:
        errors = validate_contract_pair(
            manifest,
            operation,
            prior_operations=prior_operations,
            mode=args.mode,
            now=now,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return _emit(["INPUT_CONTRACT_INVALID"])
    return _emit(errors)


if __name__ == "__main__":
    raise SystemExit(main())
