from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ContractKind = Literal["V1_AUDIT_ONLY", "V2"]
_ALLOWED_ROOT_PREFIXES = ("res://", "artifacts/")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_NON_FILE_STATES = {"NOT_RUN", "NOT_CONFIGURED", "BLOCKED_ENVIRONMENT"}
ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"

_EVIDENCE_STATES = {
    "CONTRACT": {"CONTRACT_PASS", "CONTRACT_FAIL"},
    "ENGINE_STATE": {"EXECUTION_PASS", "EXECUTION_FAIL"},
    "RUNTIME_STATE": {"RUNTIME_PASS", "RUNTIME_FAIL"},
    "ENGINE_INPUT": {"ENGINE_INPUT_PASS", "ENGINE_INPUT_FAIL"},
    "PHYSICAL_INPUT": {"PHYSICAL_INPUT_PASS", "PHYSICAL_INPUT_FAIL"},
    "SCREENSHOT": {"SCREENSHOT_PASS", "SCREENSHOT_FAIL"},
    "TEST_RESULT": {"TEST_PASS", "TEST_FAIL"},
    "HUMAN": {"HUMAN_PASS", "HUMAN_FAIL"},
    "LOG": {"LOG_CAPTURED"},
}


def _unique(errors: list[str]) -> list[str]:
    return list(dict.fromkeys(errors))


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classify_contract_document(document: Mapping[str, Any]) -> ContractKind:
    version = document.get("schema_version")
    if version == 1:
        return "V1_AUDIT_ONLY"
    if version == 2:
        return "V2"
    raise ValueError("UNSUPPORTED_SCHEMA_VERSION")


def operation_request_material(envelope: Mapping[str, Any]) -> dict[str, Any]:
    request = envelope.get("request")
    arguments = request.get("arguments") if isinstance(request, Mapping) else None
    return {
        "capability_id": envelope.get("capability_id"),
        "project_identity": envelope.get("project_identity"),
        "instance_identity": envelope.get("instance_identity"),
        "contract_snapshot": envelope.get("contract_snapshot"),
        "policy": envelope.get("policy"),
        "preconditions": envelope.get("preconditions"),
        "arguments": arguments,
    }


def _schema_is_valid(schema: Any) -> bool:
    if not isinstance(schema, Mapping):
        return False
    try:
        Draft202012Validator.check_schema(dict(schema))
    except SchemaError:
        return False
    return schema.get("type") == "object" and schema.get("additionalProperties") is False


def _path_is_confined(value: Any) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(_ALLOWED_ROOT_PREFIXES)
        and ".." not in value.replace("\\", "/").split("/")
    )


def _transport_is_safe(transport: Any) -> bool:
    if not isinstance(transport, Mapping):
        return False
    kind = transport.get("kind")
    enabled = transport.get("enabled")
    bind_host = transport.get("bind_host")
    access = transport.get("access_control")
    if not isinstance(access, Mapping):
        return False
    if kind == "DISABLED":
        return enabled is False and bind_host is None
    if kind == "CLI":
        return (
            enabled is True
            and bind_host is None
            and access.get("authentication_mode") == "NOT_APPLICABLE"
            and access.get("origin_policy") == "NOT_APPLICABLE"
            and access.get("session_binding") == "NOT_APPLICABLE"
            and access.get("os_access_control") == "CURRENT_USER_ONLY"
        )
    if kind == "LOCAL_HTTP":
        return (
            enabled is True
            and bind_host in {"127.0.0.1", "::1"}
            and access.get("authentication_mode") in {"SESSION_TOKEN", "OAUTH_2_1"}
            and access.get("origin_policy") == "EXPLICIT_ALLOWLIST"
            and access.get("session_binding") == "PROJECT_CLIENT_SESSION"
            and access.get("os_access_control") == "CURRENT_USER_ONLY"
        )
    if kind == "NAMED_PIPE":
        return (
            enabled is True
            and bind_host is None
            and access.get("os_access_control") == "CURRENT_USER_ONLY"
            and access.get("origin_policy") == "NOT_APPLICABLE"
        )
    if kind == "STDIO_BRIDGE":
        return (
            enabled is True
            and bind_host is None
            and access.get("origin_policy") == "NOT_APPLICABLE"
            and access.get("session_binding") == "NOT_APPLICABLE"
            and access.get("os_access_control") == "CURRENT_USER_ONLY"
        )
    return False


def _policy_axes_valid(capability: Mapping[str, Any]) -> bool:
    effect = capability.get("effect_kind")
    idempotency = capability.get("idempotency")
    approval = capability.get("approval_policy")
    execution = capability.get("execution_mode")
    rollback = capability.get("rollback_policy")
    retry = capability.get("retry_policy")
    timeout = capability.get("timeout_policy")
    if not isinstance(retry, Mapping) or not isinstance(timeout, Mapping):
        return False
    if effect == "READ_ONLY":
        if idempotency != "NOT_APPLICABLE" or rollback != "NOT_APPLICABLE":
            return False
    elif effect == "MUTATION":
        if idempotency not in {"IDEMPOTENT", "NON_IDEMPOTENT"}:
            return False
        if rollback not in {"EDITOR_UNDO_REDO", "SNAPSHOT", "MANUAL", "IRREVERSIBLE"}:
            return False
        if retry.get("requires_ledger") is not True:
            return False
    else:
        return False
    if idempotency == "NON_IDEMPOTENT" and (
        retry.get("automatic") is not False or retry.get("maximum_attempts") != 1
    ):
        return False
    if rollback == "IRREVERSIBLE" and (
        approval != "REQUIRED"
        or retry.get("automatic") is not False
        or retry.get("maximum_attempts") != 1
    ):
        return False
    if execution == "LONG_RUNNING_TASK" and (
        retry.get("requires_ledger") is not True
        or timeout.get("unknown_outcome") != "RESUME_BY_TASK_ID"
    ):
        return False
    return approval in {"NOT_REQUIRED", "REQUIRED"} and execution in {
        "SYNCHRONOUS",
        "LONG_RUNNING_TASK",
    }


def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list):
        return ["CAPABILITY_CATALOG_INVALID"]

    indexed: dict[str, list[Mapping[str, Any]]] = {}
    for capability in capabilities:
        if not isinstance(capability, Mapping):
            errors.append("CAPABILITY_CATALOG_INVALID")
            continue
        capability_id = capability.get("capability_id")
        if not isinstance(capability_id, str) or not capability_id:
            errors.append("CAPABILITY_ID_INVALID")
            continue
        indexed.setdefault(capability_id, []).append(capability)

        if not _policy_axes_valid(capability):
            errors.append("POLICY_AXIS_COMBINATION_INVALID")

        input_schema = capability.get("input_schema")
        output_schema = capability.get("output_schema")
        if not _schema_is_valid(input_schema):
            errors.append("CAPABILITY_INPUT_SCHEMA_INVALID")
        elif capability.get("input_schema_sha256") != canonical_json_sha256(input_schema):
            errors.append("CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH")
        if not _schema_is_valid(output_schema):
            errors.append("CAPABILITY_OUTPUT_SCHEMA_INVALID")
        elif capability.get("output_schema_sha256") != canonical_json_sha256(output_schema):
            errors.append("CAPABILITY_OUTPUT_SCHEMA_HASH_MISMATCH")

        path_access = capability.get("path_access")
        if not isinstance(path_access, Mapping):
            errors.append("CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT")
        else:
            paths = [
                *(path_access.get("read_roots") if isinstance(path_access.get("read_roots"), list) else [None]),
                *(path_access.get("write_roots") if isinstance(path_access.get("write_roots"), list) else [None]),
                path_access.get("artifact_root"),
            ]
            if any(not _path_is_confined(path) for path in paths):
                errors.append("CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT")

    if any(len(matches) > 1 for matches in indexed.values()):
        errors.append("DUPLICATE_CAPABILITY_ID")

    framework = manifest.get("project_test_framework")
    if isinstance(framework, Mapping) and framework.get("state") == "CONFIGURED":
        runner_id = framework.get("runner_capability_id")
        matches = indexed.get(runner_id, []) if isinstance(runner_id, str) else []
        if not matches:
            errors.append("PROJECT_TEST_RUNNER_NOT_DECLARED")
        elif len(matches) > 1:
            errors.append("PROJECT_TEST_RUNNER_AMBIGUOUS")
        else:
            runner = matches[0]
            evidence = runner.get("evidence_outputs")
            if not isinstance(evidence, list) or "TEST_RESULT" not in evidence:
                errors.append("PROJECT_TEST_RUNNER_EVIDENCE_INVALID")
            if runner.get("execution_path") not in {"CLI_HEADLESS", "EDITOR_PLUGIN"}:
                errors.append("PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID")

    if not _transport_is_safe(manifest.get("transport")):
        errors.append("TRANSPORT_SECURITY_PROFILE_INVALID")

    return _unique(errors)


def _parse_rfc3339(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _capability_index(manifest: Mapping[str, Any]) -> dict[str, list[Mapping[str, Any]]]:
    index: dict[str, list[Mapping[str, Any]]] = {}
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list):
        return index
    for capability in capabilities:
        if isinstance(capability, Mapping) and isinstance(capability.get("capability_id"), str):
            index.setdefault(capability["capability_id"], []).append(capability)
    return index


def _expected_policy(capability: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: capability.get(key)
        for key in (
            "effect_kind",
            "idempotency",
            "approval_policy",
            "execution_mode",
            "rollback_policy",
        )
    }


def _expected_snapshot(manifest: Mapping[str, Any], capability: Mapping[str, Any]) -> dict[str, Any]:
    catalog = manifest.get("catalog")
    transport = manifest.get("transport")
    return {
        "contract_version": manifest.get("contract_version"),
        "adapter_version": manifest.get("adapter_version"),
        "catalog_sha256": catalog.get("sha256") if isinstance(catalog, Mapping) else None,
        "capability_input_schema_sha256": capability.get("input_schema_sha256"),
        "capability_output_schema_sha256": capability.get("output_schema_sha256"),
        "protocol_profile": transport.get("protocol_profile") if isinstance(transport, Mapping) else None,
        "protocol_version": transport.get("protocol_version") if isinstance(transport, Mapping) else None,
    }


def _instance_identity_valid(capability: Mapping[str, Any], identity: Any) -> bool:
    if not isinstance(identity, Mapping):
        return False
    if not isinstance(identity.get("automation_service_instance_id"), str) or not identity.get("automation_service_instance_id"):
        return False
    execution_path = capability.get("execution_path")
    if execution_path == "EDITOR_PLUGIN" and not identity.get("editor_instance_id"):
        return False
    if execution_path == "RUNTIME_DEBUGGER":
        return bool(identity.get("runtime_session_id")) and identity.get("runtime_session_state") == "ACTIVE"
    return True


def _preconditions_conflict(preconditions: Any) -> bool:
    if not isinstance(preconditions, Mapping):
        return True
    pairs = (
        ("expected_target_revision", "observed_target_revision"),
        ("expected_target_content_sha256", "observed_target_content_sha256"),
        ("expected_dirty_state", "observed_dirty_state"),
        ("expected_scene_path", "observed_scene_path"),
    )
    return any(preconditions.get(expected) != preconditions.get(observed) for expected, observed in pairs)


def _approval_binding_material(envelope: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "operation_id": envelope.get("operation_id"),
        "capability_id": envelope.get("capability_id"),
        "project_identity": envelope.get("project_identity"),
        "instance_identity": envelope.get("instance_identity"),
        "contract_snapshot": envelope.get("contract_snapshot"),
        "policy": envelope.get("policy"),
        "request_hash": envelope.get("request_hash"),
        "preconditions": envelope.get("preconditions"),
    }


def _is_exact_completed_idempotent_replay(current: Mapping[str, Any], prior: Mapping[str, Any]) -> bool:
    current_policy = current.get("policy")
    prior_policy = prior.get("policy")
    current_result = current.get("result")
    prior_result = prior.get("result")
    return (
        isinstance(current_policy, Mapping)
        and current_policy.get("idempotency") == "IDEMPOTENT"
        and isinstance(prior_policy, Mapping)
        and prior_policy.get("idempotency") == "IDEMPOTENT"
        and current.get("operation_id") == prior.get("operation_id")
        and current.get("capability_id") == prior.get("capability_id")
        and current.get("request_hash") == prior.get("request_hash")
        and current.get("idempotency_key") == prior.get("idempotency_key")
        and isinstance(current_result, Mapping)
        and isinstance(prior_result, Mapping)
        and current_result.get("success") is True
        and prior_result.get("success") is True
        and current_result.get("result_hash") == prior_result.get("result_hash")
    )


def validate_operation_semantics(
    manifest: Mapping[str, Any],
    envelope: Mapping[str, Any],
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    now: datetime | None = None,
) -> list[str]:
    errors: list[str] = []
    capability_id = envelope.get("capability_id")
    matches = _capability_index(manifest).get(capability_id, []) if isinstance(capability_id, str) else []
    if not matches:
        return ["CAPABILITY_NOT_DECLARED"]
    if len(matches) > 1:
        return ["CAPABILITY_AMBIGUOUS"]
    capability = matches[0]

    if envelope.get("policy") != _expected_policy(capability):
        errors.append("POLICY_MISMATCH")
    if envelope.get("project_identity") != manifest.get("project_identity"):
        errors.append("PROJECT_IDENTITY_MISMATCH")
    if not _instance_identity_valid(capability, envelope.get("instance_identity")):
        errors.append("INSTANCE_IDENTITY_INVALID")
    if envelope.get("contract_snapshot") != _expected_snapshot(manifest, capability):
        errors.append("CONTRACT_SNAPSHOT_MISMATCH")

    request = envelope.get("request")
    arguments = request.get("arguments") if isinstance(request, Mapping) else None
    input_schema = capability.get("input_schema")
    if not isinstance(input_schema, Mapping) or not isinstance(arguments, Mapping) or list(Draft202012Validator(dict(input_schema)).iter_errors(arguments)):
        errors.append("REQUEST_SCHEMA_INVALID")
    if envelope.get("request_hash") != canonical_json_sha256(operation_request_material(envelope)):
        errors.append("REQUEST_HASH_MISMATCH")

    precondition_policy = capability.get("precondition_policy")
    preconditions = envelope.get("preconditions")
    if precondition_policy == "REQUIRED":
        if not isinstance(preconditions, Mapping) or (
            preconditions.get("expected_target_revision") is None
            and preconditions.get("expected_target_content_sha256") is None
        ):
            errors.append("PRECONDITION_REQUIRED")
        elif _preconditions_conflict(preconditions):
            errors.append("TARGET_STATE_CONFLICT")

    approval_policy = capability.get("approval_policy")
    approval = envelope.get("approval")
    if approval_policy == "REQUIRED":
        if not isinstance(approval, Mapping) or approval.get("state") != "APPROVED":
            errors.append("APPROVAL_REQUIRED")
        else:
            if approval.get("token_binding") != _approval_binding_material(envelope) or approval.get("consumed_by_operation_id") != envelope.get("operation_id"):
                errors.append("APPROVAL_TOKEN_MISMATCH")
            expiry = _parse_rfc3339(approval.get("expires_at"))
            current_time = now or datetime.now().astimezone()
            if expiry is None or current_time >= expiry:
                errors.append("APPROVAL_EXPIRED")
            token_id = approval.get("token_id")
            for prior in prior_operations:
                prior_approval = prior.get("approval")
                if (
                    isinstance(token_id, str)
                    and isinstance(prior_approval, Mapping)
                    and prior_approval.get("token_id") == token_id
                    and not _is_exact_completed_idempotent_replay(envelope, prior)
                ):
                    errors.append("APPROVAL_TOKEN_REUSED")
                    break

    result = envelope.get("result")
    if not isinstance(result, Mapping):
        return _unique(errors + ["OUTPUT_SCHEMA_MISMATCH", "RESULT_HASH_MISMATCH"])
    output_schema = capability.get("output_schema")
    if not isinstance(output_schema, Mapping) or list(Draft202012Validator(dict(output_schema)).iter_errors(result.get("data"))):
        errors.append("OUTPUT_SCHEMA_MISMATCH")
    if result.get("result_hash") != canonical_json_sha256(result.get("data")):
        errors.append("RESULT_HASH_MISMATCH")

    task = envelope.get("task")
    terminal_states = {"COMPLETED", "FAILED", "CANCELLED", "STALE"}
    if isinstance(task, Mapping) and task.get("state") in terminal_states:
        binding = task.get("result_binding")
        instance = envelope.get("instance_identity")
        expected_binding = {
            "operation_id": envelope.get("operation_id"),
            "project_identity": envelope.get("project_identity"),
            "automation_service_instance_id": (
                instance.get("automation_service_instance_id")
                if isinstance(instance, Mapping)
                else None
            ),
            "task_id": task.get("task_id"),
            "result_hash": result.get("result_hash"),
        }
        if binding != expected_binding:
            errors.append("TASK_RESULT_STALE")
        elif binding.get("result_hash") != result.get("result_hash"):
            errors.append("TASK_RESULT_HASH_MISMATCH")

    evidence_items = result.get("evidence")
    if isinstance(evidence_items, list):
        for evidence in evidence_items:
            if not isinstance(evidence, Mapping):
                errors.append("EVIDENCE_KIND_STATE_INVALID")
                continue
            kind = evidence.get("kind")
            state = evidence.get("state")
            if state not in _NON_FILE_STATES and state not in _EVIDENCE_STATES.get(kind, set()):
                errors.append("EVIDENCE_KIND_STATE_INVALID")
            path = evidence.get("path")
            artifact_hash = evidence.get("artifact_sha256")
            if state in _NON_FILE_STATES:
                if path is not None or artifact_hash is not None:
                    errors.append("EVIDENCE_KIND_STATE_INVALID")
                continue
            if not _path_is_confined(path) or not str(path).startswith("artifacts/"):
                errors.append("EVIDENCE_PATH_OUTSIDE_ARTIFACT_ROOT")
            if not isinstance(artifact_hash, str) or not _SHA256_PATTERN.fullmatch(
                artifact_hash
            ):
                errors.append("EVIDENCE_HASH_MISSING")
    else:
        errors.append("EVIDENCE_KIND_STATE_INVALID")

    return _unique(errors)


def _schema_errors(schema_path: Path, document: Mapping[str, Any], code: str) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return [code] if list(Draft202012Validator(schema).iter_errors(document)) else []


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
        if mode == "AUDIT" and operation is None:
            return []
        return ["V1_MUTATION_AUTHORITY_REJECTED"]

    errors = _schema_errors(CAPABILITY_SCHEMA_V2, manifest, "MANIFEST_SCHEMA_INVALID")
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


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_cli_now(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = _parse_rfc3339(value)
    if parsed is None:
        raise argparse.ArgumentTypeError("--now must be an RFC3339 timestamp with timezone")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Godot live-editor v2 contracts."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--operation", type=Path)
    parser.add_argument("--prior-operation", type=Path, action="append", default=[])
    parser.add_argument("--mode", choices=("AUDIT", "AUTHORIZE"), default="AUTHORIZE")
    parser.add_argument("--now", type=str)
    args = parser.parse_args()

    manifest = _load(args.manifest)
    operation = _load(args.operation) if args.operation is not None else None
    prior_operations = [_load(path) for path in args.prior_operation]
    try:
        now = _parse_cli_now(args.now)
    except argparse.ArgumentTypeError:
        print(
            json.dumps(
                {"status": "FAIL", "errors": ["INVALID_NOW_TIMESTAMP"]},
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
        return 1

    errors = validate_contract_pair(
        manifest,
        operation,
        prior_operations=prior_operations,
        mode=args.mode,
        now=now,
    )
    print(
        json.dumps(
            {"status": "PASS" if not errors else "FAIL", "errors": errors},
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
