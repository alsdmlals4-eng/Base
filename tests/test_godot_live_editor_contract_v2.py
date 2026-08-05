from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.validate_godot_live_editor_contract_v2 import (
    canonical_json_sha256,
    classify_contract_document,
    operation_request_material,
    validate_contract_pair,
    validate_manifest_semantics,
    validate_operation_semantics,
)


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
SEMANTIC_VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract_v2.py"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md"
V2_TEMPLATE = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
V1_PILOT_MANIFEST = ROOT / "examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


def make_valid_manifest() -> dict:
    input_schema = {
        "type": "object",
        "properties": {"scene_path": {"type": "string", "pattern": "^res://"}},
        "required": ["scene_path"],
        "additionalProperties": False,
    }
    output_schema = {
        "type": "object",
        "properties": {"node_count": {"type": "integer", "minimum": 0}},
        "required": ["node_count"],
        "additionalProperties": False,
    }
    capability = {
        "capability_id": "scene.inspect",
        "description": "Inspect a bounded scene summary.",
        "execution_path": "CLI_HEADLESS",
        "effect_kind": "READ_ONLY",
        "idempotency": "NOT_APPLICABLE",
        "approval_policy": "NOT_REQUIRED",
        "execution_mode": "SYNCHRONOUS",
        "rollback_policy": "NOT_APPLICABLE",
        "input_schema": input_schema,
        "output_schema": output_schema,
        "input_schema_sha256": canonical_json_sha256(input_schema),
        "output_schema_sha256": canonical_json_sha256(output_schema),
        "path_access": {
            "read_roots": ["res://"],
            "write_roots": [],
            "artifact_root": "artifacts/",
        },
        "precondition_policy": "NONE",
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
        "unsupported_states": ["IMPORTING"],
    }
    return {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
        "configuration_state": "CONFIGURED",
        "contract_version": "2.0.0",
        "adapter_version": "2.0.0",
        "project_identity": {
            "normalized_project_path": "/workspace/game",
            "project_godot_sha256": "a" * 64,
            "project_fingerprint": "godot-project-a",
        },
        "engine_compatibility": {
            "detected_version": "4.7.1",
            "minimum_version": "4.3",
            "maximum_exclusive_version": "5.0",
        },
        "tool_adoption": {
            "source": "project-owned",
            "exact_version": "2.0.0",
            "telemetry_policy": "DISABLED",
            "external_data_policy": "DENY_BY_DEFAULT",
            "uninstall_procedure": "docs/operations/remove-godot-live-editor.md",
            "rollback_reference": "docs/operations/restore-godot-live-editor.md",
        },
        "transport": {
            "kind": "CLI",
            "enabled": True,
            "bind_host": None,
            "endpoint_identity": "cli-current-process",
            "protocol_profile": "GENERIC",
            "protocol_version": "1.0",
            "access_control": {
                "authentication_mode": "NOT_APPLICABLE",
                "origin_policy": "NOT_APPLICABLE",
                "session_binding": "NOT_APPLICABLE",
                "os_access_control": "CURRENT_USER_ONLY",
            },
        },
        "catalog": {
            "generated_at": "2026-08-05T00:00:00Z",
            "sha256": "b" * 64,
            "freshness_state": "FRESH",
        },
        "project_test_framework": {
            "state": "NOT_CONFIGURED",
            "runner_capability_id": None,
        },
        "capabilities": [capability],
        "validation": {
            "contract_state": "CONTRACT_PASS",
            "execution_state": "NOT_RUN",
            "runtime_state": "NOT_RUN",
            "physical_input_state": "NOT_RUN",
            "human_state": "HUMAN_NOT_RUN",
        },
    }


def make_valid_operation(manifest: dict | None = None) -> dict:
    manifest = make_valid_manifest() if manifest is None else copy.deepcopy(manifest)
    capability = manifest["capabilities"][0]
    return {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": "op-v2-001",
        "capability_id": capability["capability_id"],
        "project_identity": copy.deepcopy(manifest["project_identity"]),
        "instance_identity": {
            "automation_service_instance_id": "service-001",
            "editor_instance_id": None,
            "runtime_session_id": None,
            "runtime_session_state": "NOT_APPLICABLE",
        },
        "contract_snapshot": {
            "contract_version": manifest["contract_version"],
            "adapter_version": manifest["adapter_version"],
            "catalog_sha256": manifest["catalog"]["sha256"],
            "capability_input_schema_sha256": capability["input_schema_sha256"],
            "capability_output_schema_sha256": capability["output_schema_sha256"],
            "protocol_profile": manifest["transport"]["protocol_profile"],
            "protocol_version": manifest["transport"]["protocol_version"],
        },
        "policy": {
            "effect_kind": capability["effect_kind"],
            "idempotency": capability["idempotency"],
            "approval_policy": capability["approval_policy"],
            "execution_mode": capability["execution_mode"],
            "rollback_policy": capability["rollback_policy"],
        },
        "request": {"arguments": {"scene_path": "res://main.tscn"}},
        "request_hash": "e" * 64,
        "idempotency_key": None,
        "preconditions": {
            "expected_target_revision": None,
            "observed_target_revision": None,
            "expected_target_content_sha256": None,
            "observed_target_content_sha256": None,
            "expected_dirty_state": "NOT_APPLICABLE",
            "observed_dirty_state": "NOT_APPLICABLE",
            "expected_scene_path": None,
            "observed_scene_path": None,
            "conflict_policy": "FAIL_CLOSED",
        },
        "approval": {
            "state": "NOT_REQUIRED",
            "token_id": None,
            "token_binding": None,
            "expires_at": None,
            "consumed_by_operation_id": None,
        },
        "task": {
            "task_id": None,
            "state": "NOT_APPLICABLE",
            "created_at": None,
            "last_updated_at": None,
            "ttl_ms": None,
            "poll_interval_ms": None,
            "cancellation_policy": "NOT_SUPPORTED",
            "result_binding": None,
        },
        "result": {
            "success": True,
            "code": "OK",
            "message": "Inspection completed.",
            "data": {"node_count": 3},
            "result_hash": "f" * 64,
            "evidence": [
                {
                    "kind": "ENGINE_STATE",
                    "state": "EXECUTION_PASS",
                    "path": "artifacts/scene-summary.json",
                    "artifact_sha256": "1" * 64,
                    "generated_at": "2026-08-05T00:00:01Z",
                    "producer": "scene.inspect@2.0.0",
                }
            ],
        },
    }


def make_mutation_manifest() -> dict:
    manifest = make_valid_manifest()
    capability = manifest["capabilities"][0]
    capability.update(
        {
            "capability_id": "node.set_properties",
            "description": "Set one bounded property transaction.",
            "execution_path": "EDITOR_PLUGIN",
            "effect_kind": "MUTATION",
            "idempotency": "IDEMPOTENT",
            "approval_policy": "REQUIRED",
            "execution_mode": "SYNCHRONOUS",
            "rollback_policy": "EDITOR_UNDO_REDO",
            "input_schema": {
                "type": "object",
                "properties": {
                    "node_path": {"type": "string", "minLength": 1},
                    "property": {"type": "string", "minLength": 1},
                    "value": {},
                },
                "required": ["node_path", "property", "value"],
                "additionalProperties": False,
            },
            "output_schema": {
                "type": "object",
                "properties": {"written": {"type": "boolean"}},
                "required": ["written"],
                "additionalProperties": False,
            },
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
        }
    )
    capability["input_schema_sha256"] = canonical_json_sha256(
        capability["input_schema"]
    )
    capability["output_schema_sha256"] = canonical_json_sha256(
        capability["output_schema"]
    )
    return manifest


def make_approved_mutation(
    manifest: dict,
    *,
    operation_id: str,
    token_id: str,
) -> dict:
    operation = make_valid_operation(manifest)
    operation["operation_id"] = operation_id
    operation["instance_identity"]["editor_instance_id"] = "editor-001"
    operation["request"]["arguments"] = {
        "node_path": "Root/Target",
        "property": "visible",
        "value": True,
    }
    operation["idempotency_key"] = "idem-visible-true"
    operation["preconditions"] = {
        "expected_target_revision": "revision-1",
        "observed_target_revision": "revision-1",
        "expected_target_content_sha256": "2" * 64,
        "observed_target_content_sha256": "2" * 64,
        "expected_dirty_state": "CLEAN",
        "observed_dirty_state": "CLEAN",
        "expected_scene_path": "res://main.tscn",
        "observed_scene_path": "res://main.tscn",
        "conflict_policy": "FAIL_CLOSED",
    }
    operation["result"]["data"] = {"written": True}
    operation["result"]["result_hash"] = canonical_json_sha256(
        operation["result"]["data"]
    )
    operation["request_hash"] = canonical_json_sha256(
        operation_request_material(operation)
    )
    operation["approval"] = {
        "state": "APPROVED",
        "token_id": token_id,
        "token_binding": {
            "operation_id": operation_id,
            "capability_id": operation["capability_id"],
            "project_identity": copy.deepcopy(operation["project_identity"]),
            "instance_identity": copy.deepcopy(operation["instance_identity"]),
            "contract_snapshot": copy.deepcopy(operation["contract_snapshot"]),
            "policy": copy.deepcopy(operation["policy"]),
            "request_hash": operation["request_hash"],
            "preconditions": copy.deepcopy(operation["preconditions"]),
        },
        "expires_at": "2026-08-05T01:00:00Z",
        "consumed_by_operation_id": operation_id,
    }
    return operation


class GodotLiveEditorContractV2Tests(unittest.TestCase):
    maxDiff = None

    def test_v2_contract_artifacts_exist(self) -> None:
        required = (
            CAPABILITY_SCHEMA_V2,
            OPERATION_SCHEMA_V2,
            SEMANTIC_VALIDATOR,
            DESIGN,
        )
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_v2_representative_documents_validate_structurally(self) -> None:
        self.assertEqual([], list(Draft202012Validator(load(CAPABILITY_SCHEMA_V2)).iter_errors(make_valid_manifest())))
        self.assertEqual([], list(Draft202012Validator(load(OPERATION_SCHEMA_V2)).iter_errors(make_valid_operation())))

    def test_v2_capability_schema_rejects_mixed_axis_and_unsafe_transport_shapes(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA_V2))
        invalid = make_valid_manifest()
        invalid["capabilities"][0]["rollback_policy"] = "EDITOR_UNDO_REDO"
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = make_valid_manifest()
        invalid["transport"]["kind"] = "LOCAL_HTTP"
        invalid["transport"]["bind_host"] = "0.0.0.0"
        invalid["transport"]["access_control"] = {
            "authentication_mode": "SESSION_TOKEN",
            "origin_policy": "EXPLICIT_ALLOWLIST",
            "session_binding": "PROJECT_CLIENT_SESSION",
            "os_access_control": "CURRENT_USER_ONLY",
        }
        self.assertTrue(list(validator.iter_errors(invalid)))

    def test_v2_operation_schema_rejects_invalid_task_approval_evidence_and_extra_fields(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA_V2))
        invalid = make_valid_operation()
        invalid["task"]["task_id"] = "task-1"
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = make_valid_operation()
        invalid["policy"]["approval_policy"] = "REQUIRED"
        invalid["approval"]["state"] = "APPROVED"
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = make_valid_operation()
        invalid["result"]["evidence"][0]["path"] = None
        invalid["result"]["evidence"][0]["artifact_sha256"] = None
        self.assertTrue(list(validator.iter_errors(invalid)))
        invalid = make_valid_operation()
        invalid["unexpected"] = True
        self.assertTrue(list(validator.iter_errors(invalid)))

    def test_canonical_json_hash_and_version_classification_are_deterministic(self) -> None:
        self.assertEqual(canonical_json_sha256({"a": 1, "b": [2, 3]}), canonical_json_sha256({"b": [2, 3], "a": 1}))
        self.assertEqual("V2", classify_contract_document(make_valid_manifest()))
        self.assertEqual("V1_AUDIT_ONLY", classify_contract_document({"schema_version": 1}))

    def test_manifest_semantics_reject_duplicate_ids_and_schema_hash_mismatch(self) -> None:
        manifest = make_valid_manifest()
        manifest["capabilities"].append(copy.deepcopy(manifest["capabilities"][0]))
        self.assertIn("DUPLICATE_CAPABILITY_ID", validate_manifest_semantics(manifest))
        manifest = make_valid_manifest()
        manifest["capabilities"][0]["input_schema_sha256"] = "0" * 64
        self.assertIn("CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH", validate_manifest_semantics(manifest))
        manifest = make_valid_manifest()
        manifest["capabilities"][0]["output_schema_sha256"] = "0" * 64
        self.assertIn("CAPABILITY_OUTPUT_SCHEMA_HASH_MISMATCH", validate_manifest_semantics(manifest))

    def test_manifest_semantics_reject_invalid_test_runner_path_and_transport(self) -> None:
        manifest = make_valid_manifest()
        manifest["project_test_framework"] = {"state": "CONFIGURED", "runner_capability_id": "test.project"}
        self.assertIn("PROJECT_TEST_RUNNER_NOT_DECLARED", validate_manifest_semantics(manifest))
        manifest = make_valid_manifest()
        manifest["capabilities"][0]["path_access"]["read_roots"] = ["/outside"]
        self.assertIn("CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT", validate_manifest_semantics(manifest))
        manifest = make_valid_manifest()
        manifest["transport"]["kind"] = "PROJECT_DEFINED"
        manifest["transport"]["bind_host"] = "0.0.0.0"
        self.assertIn("TRANSPORT_SECURITY_PROFILE_INVALID", validate_manifest_semantics(manifest))

    def test_operation_semantics_accept_exact_read_and_approved_mutation(self) -> None:
        manifest = make_valid_manifest()
        operation = make_valid_operation(manifest)
        operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
        operation["result"]["result_hash"] = canonical_json_sha256(operation["result"]["data"])
        self.assertEqual([], validate_operation_semantics(manifest, operation))
        manifest = make_mutation_manifest()
        operation = make_approved_mutation(manifest, operation_id="op-v2-mutation-001", token_id="token-1")
        self.assertEqual([], validate_operation_semantics(manifest, operation, now=datetime(2026, 8, 5, 0, 0, 30, tzinfo=UTC)))

    def test_operation_semantics_reject_identity_policy_snapshot_and_input_mismatch(self) -> None:
        manifest = make_valid_manifest()
        operation = make_valid_operation(manifest)
        operation["capability_id"] = "missing.capability"
        self.assertIn("CAPABILITY_NOT_DECLARED", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        operation["policy"]["approval_policy"] = "REQUIRED"
        self.assertIn("POLICY_MISMATCH", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        operation["project_identity"]["project_fingerprint"] = "wrong-project"
        self.assertIn("PROJECT_IDENTITY_MISMATCH", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        operation["contract_snapshot"]["catalog_sha256"] = "0" * 64
        self.assertIn("CONTRACT_SNAPSHOT_MISMATCH", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        operation["request"]["arguments"]["unexpected"] = True
        self.assertIn("REQUEST_SCHEMA_INVALID", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        self.assertIn("REQUEST_HASH_MISMATCH", validate_operation_semantics(manifest, operation))

    def test_operation_semantics_reject_stale_state_approval_and_output_mismatch(self) -> None:
        manifest = make_mutation_manifest()
        operation = make_approved_mutation(manifest, operation_id="op-v2-mutation-001", token_id="token-1")
        operation["preconditions"]["observed_target_revision"] = "revision-2"
        self.assertIn("TARGET_STATE_CONFLICT", validate_operation_semantics(manifest, operation))
        operation = make_approved_mutation(manifest, operation_id="op-v2-mutation-002", token_id="token-2")
        operation["approval"]["token_binding"]["request_hash"] = "0" * 64
        self.assertIn("APPROVAL_TOKEN_MISMATCH", validate_operation_semantics(manifest, operation))
        operation = make_approved_mutation(manifest, operation_id="op-v2-mutation-003", token_id="token-3")
        self.assertIn("APPROVAL_EXPIRED", validate_operation_semantics(manifest, operation, now=datetime(2026, 8, 5, 2, 0, 0, tzinfo=UTC)))
        operation = make_approved_mutation(manifest, operation_id="op-v2-mutation-004", token_id="token-4")
        operation["result"]["data"] = {"written": "yes"}
        self.assertIn("OUTPUT_SCHEMA_MISMATCH", validate_operation_semantics(manifest, operation))

    def test_operation_semantics_reject_cross_operation_approval_reuse(self) -> None:
        manifest = make_mutation_manifest()
        prior = make_approved_mutation(manifest, operation_id="op-v2-mutation-001", token_id="token-1")
        current = make_approved_mutation(manifest, operation_id="op-v2-mutation-002", token_id="token-1")
        errors = validate_operation_semantics(manifest, current, prior_operations=[prior], now=datetime(2026, 8, 5, 0, 0, 30, tzinfo=UTC))
        self.assertIn("APPROVAL_TOKEN_REUSED", errors)
        replay = copy.deepcopy(prior)
        self.assertNotIn("APPROVAL_TOKEN_REUSED", validate_operation_semantics(manifest, replay, prior_operations=[prior], now=datetime(2026, 8, 5, 0, 0, 30, tzinfo=UTC)))

    def test_operation_semantics_reject_task_result_hash_and_evidence_mismatch(self) -> None:
        manifest = make_valid_manifest()
        operation = make_valid_operation(manifest)
        operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
        operation["result"]["result_hash"] = "0" * 64
        self.assertIn("RESULT_HASH_MISMATCH", validate_operation_semantics(manifest, operation))
        operation = make_valid_operation(manifest)
        operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
        operation["result"]["result_hash"] = canonical_json_sha256(operation["result"]["data"])
        operation["result"]["evidence"][0]["path"] = "../outside.json"
        self.assertIn("EVIDENCE_PATH_OUTSIDE_ARTIFACT_ROOT", validate_operation_semantics(manifest, operation))
        manifest = make_valid_manifest()
        capability = manifest["capabilities"][0]
        capability["execution_mode"] = "LONG_RUNNING_TASK"
        capability["retry_policy"]["requires_ledger"] = True
        capability["timeout_policy"]["unknown_outcome"] = "RESUME_BY_TASK_ID"
        operation = make_valid_operation(manifest)
        operation["task"] = {
            "task_id": "task-1",
            "state": "COMPLETED",
            "created_at": "2026-08-05T00:00:00Z",
            "last_updated_at": "2026-08-05T00:00:01Z",
            "ttl_ms": 60000,
            "poll_interval_ms": 1000,
            "cancellation_policy": "NOT_SUPPORTED",
            "result_binding": {
                "operation_id": operation["operation_id"],
                "project_identity": copy.deepcopy(operation["project_identity"]),
                "automation_service_instance_id": "wrong-service",
                "task_id": "task-1",
                "result_hash": operation["result"]["result_hash"],
            },
        }
        operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
        self.assertIn("TASK_RESULT_STALE", validate_operation_semantics(manifest, operation))

    def test_v1_is_audit_readable_but_cannot_authorize_v2_mutation(self) -> None:
        v1 = load(V1_PILOT_MANIFEST)
        self.assertEqual("V1_AUDIT_ONLY", classify_contract_document(v1))
        self.assertEqual([], validate_contract_pair(v1, mode="AUDIT"))
        self.assertIn(
            "V1_MUTATION_AUTHORITY_REJECTED",
            validate_contract_pair(v1, mode="AUTHORIZE"),
        )

    def test_installation_template_is_safe_v2_not_configured(self) -> None:
        template = load(V2_TEMPLATE)
        self.assertEqual(2, template["schema_version"])
        self.assertEqual("NOT_CONFIGURED", template["configuration_state"])
        self.assertEqual([], template["capabilities"])
        self.assertFalse(template["transport"]["enabled"])
        self.assertEqual(
            [],
            list(
                Draft202012Validator(load(CAPABILITY_SCHEMA_V2)).iter_errors(template)
            ),
        )

    def test_cli_audits_v1_but_rejects_v1_authorization(self) -> None:
        audit = subprocess.run(
            [
                sys.executable,
                str(SEMANTIC_VALIDATOR),
                "--manifest",
                str(V1_PILOT_MANIFEST),
                "--mode",
                "AUDIT",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, audit.returncode)
        self.assertEqual({"status": "PASS", "errors": []}, json.loads(audit.stdout))
        self.assertEqual("", audit.stderr)

        authorize = subprocess.run(
            [
                sys.executable,
                str(SEMANTIC_VALIDATOR),
                "--manifest",
                str(V1_PILOT_MANIFEST),
                "--mode",
                "AUTHORIZE",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(1, authorize.returncode)
        self.assertEqual(
            {
                "status": "FAIL",
                "errors": ["V1_MUTATION_AUTHORITY_REJECTED"],
            },
            json.loads(authorize.stdout),
        )
        self.assertEqual("", authorize.stderr)


if __name__ == "__main__":
    unittest.main()
