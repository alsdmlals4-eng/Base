from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v1.schema.json"
OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v1.schema.json"
MANIFEST = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
CONTRACT = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md"
SECURITY = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md"
ADAPTER = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
AGENTS_FRAGMENT = ROOT / "templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


def valid_manifest() -> dict:
    return {
        "schema_version": 1,
        "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
        "configuration_state": "CONFIGURED",
        "contract_version": "1.0.0",
        "adapter_version": "1.0.0",
        "project_identity": {
            "normalized_project_path": "/workspace/game",
            "project_godot_sha256": "a" * 64,
            "project_fingerprint": "godot-project-a",
        },
        "engine_compatibility": {
            "minimum_version": "4.3",
            "maximum_exclusive_version": "5.0",
        },
        "transport": {
            "kind": "LOCAL_HTTP",
            "enabled": True,
            "bind_host": "127.0.0.1",
            "endpoint_identity": "adapter-a",
        },
        "catalog": {
            "generated_at": "2026-08-05T00:00:00Z",
            "sha256": "b" * 64,
            "freshness_state": "FRESH",
        },
        "project_test_framework": {
            "state": "CONFIGURED",
            "runner_capability_id": "test.project",
        },
        "capabilities": [
            {
                "capability_id": "scene.inspect",
                "description": "Inspect a bounded scene summary.",
                "execution_path": "EDITOR_PLUGIN",
                "operation_class": "READ_ONLY",
                "idempotency_key_required": False,
                "approval_required": False,
                "arguments_schema": {"type": "object", "additionalProperties": False},
                "timeout_policy": {
                    "milliseconds": 10000,
                    "unknown_outcome": "RECONCILE_BEFORE_RETRY",
                },
                "retry_policy": {
                    "automatic": True,
                    "maximum_attempts": 2,
                    "requires_ledger": False,
                },
                "evidence_outputs": ["ENGINE_STATE"],
                "unsupported_states": ["IMPORTING"],
            }
        ],
        "validation": {
            "contract_state": "CONTRACT_PASS",
            "execution_state": "NOT_RUN",
            "runtime_state": "NOT_RUN",
            "physical_input_state": "NOT_RUN",
            "human_state": "HUMAN_NOT_RUN",
        },
    }


def valid_operation() -> dict:
    return {
        "schema_version": 1,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": "op-20260805-001",
        "project_fingerprint": "godot-project-a",
        "capability_id": "scene.inspect",
        "operation_class": "READ_ONLY",
        "request_hash": "c" * 64,
        "approval": {
            "state": "NOT_REQUIRED",
            "token_binding": None,
            "expires_at": None,
        },
        "task": {
            "task_id": None,
            "state": "NOT_APPLICABLE",
            "result_binding": None,
        },
        "result": {
            "success": True,
            "code": "OK",
            "message": "Inspection completed.",
            "data": {},
            "evidence": [
                {
                    "kind": "ENGINE_STATE",
                    "state": "EXECUTION_PASS",
                    "path": "artifacts/scene-summary.json",
                }
            ],
        },
    }


class GodotLiveEditorContractTests(unittest.TestCase):
    maxDiff = None

    def test_required_contract_and_project_adapter_paths_exist(self) -> None:
        required = (
            CONTRACT,
            SECURITY,
            CAPABILITY_SCHEMA,
            OPERATION_SCHEMA,
            MANIFEST,
            ADAPTER,
            AGENTS_FRAGMENT,
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

    def test_template_manifest_and_representative_configured_manifest_validate(self) -> None:
        schema = load(CAPABILITY_SCHEMA)
        validator = Draft202012Validator(schema)
        self.assertEqual([], list(validator.iter_errors(load(MANIFEST))))
        self.assertEqual([], list(validator.iter_errors(valid_manifest())))

    def test_capability_schema_rejects_port_only_identity_and_unsafe_retry(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))

        port_only = valid_manifest()
        port_only["project_identity"] = {
            "normalized_project_path": "",
            "project_godot_sha256": None,
            "project_fingerprint": "",
        }
        self.assertTrue(list(validator.iter_errors(port_only)))

        unsafe_retry = valid_manifest()
        capability = unsafe_retry["capabilities"][0]
        capability["operation_class"] = "NON_RETRYABLE_MUTATION"
        capability["approval_required"] = True
        capability["retry_policy"]["automatic"] = True
        self.assertTrue(list(validator.iter_errors(unsafe_retry)))

    def test_operation_schema_binds_approval_and_long_running_results(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA))
        self.assertEqual([], list(validator.iter_errors(valid_operation())))

        approval_gap = valid_operation()
        approval_gap["operation_class"] = "APPROVAL_REQUIRED_MUTATION"
        approval_gap["approval"] = {
            "state": "APPROVED",
            "token_binding": None,
            "expires_at": "2026-08-05T01:00:00Z",
        }
        self.assertTrue(list(validator.iter_errors(approval_gap)))

        task_gap = valid_operation()
        task_gap["operation_class"] = "LONG_RUNNING_TASK"
        task_gap["task"] = {
            "task_id": None,
            "state": "COMPLETED",
            "result_binding": None,
        }
        self.assertTrue(list(validator.iter_errors(task_gap)))

    def test_contract_defines_bootstrap_identity_recovery_and_evidence_boundaries(self) -> None:
        combined = read(CONTRACT) + read(SECURITY)
        for term in (
            "doctor → status → catalog --compact",
            "project.godot",
            "PROJECT_IDENTITY_MISMATCH",
            "CAPABILITY_NOT_DECLARED",
            "CATALOG_STALE",
            "APPROVAL_TOKEN_MISMATCH",
            "UNSAFE_RETRY_BLOCKED",
            "TASK_PENDING",
            "PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED",
            "PHYSICAL_INPUT_EVIDENCE_BLOCKED",
            "EditorUndoRedoManager",
            "EditorDebuggerPlugin",
            "EngineDebugger",
            "CONTRACT_PASS",
            "EXECUTION_PASS",
            "RUNTIME_PASS",
            "ENGINE_INPUT_PASS",
            "PHYSICAL_INPUT_PASS",
            "HUMAN_PASS",
            "BLOCKED_ENVIRONMENT",
        ):
            self.assertIn(term, combined)

        for unity_only in (
            "UnityEngine.Object",
            "Unity Package Manager",
            "EventSystem input QA",
            "hera-agent-unity exec",
            "[HeraTool]",
        ):
            self.assertNotIn(unity_only, combined)

    def test_project_adapter_routes_existing_owners_without_new_base_skill(self) -> None:
        adapter = read(ADAPTER)
        agents_fragment = read(AGENTS_FRAGMENT)
        start = read(ROOT / "START_HERE.md")
        project_router = read(
            ROOT / "templates/project-operations/.agents/skills/base-project-router/SKILL.md"
        )
        registry = load(ROOT / "skills/SKILL_REGISTRY.json")

        for mode in ("bootstrap", "observe", "mutate", "validate", "resume", "recover"):
            self.assertIn(f"`{mode}`", adapter)
        for owner in (
            "managing-game-project-operating-system",
            "diagnosing-game-engine-runtime-failures",
            "reviewing-and-validating-project-changes",
            "auditing-and-refining-ui-art",
            "maintaining-long-running-task-continuity",
            "auditing-canonical-reference-freshness",
            "evolving-project-discipline-skills",
        ):
            self.assertIn(owner, adapter)
        for term in (
            "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json",
            "NOT_CONFIGURED",
            "automatic approval",
            "unsafe retry",
        ):
            self.assertIn(term, adapter + agents_fragment)
        self.assertIn("godot-live-editor-operations", start)
        self.assertIn("godot-live-editor-operations", project_router)
        self.assertNotIn(
            "godot-live-editor-operations",
            {item["skill_id"] for item in registry["skills"]},
        )

    def test_evidence_states_cannot_be_promoted_by_contract_file_existence(self) -> None:
        template = load(MANIFEST)
        validation = template["validation"]
        self.assertEqual("CONTRACT_PASS", validation["contract_state"])
        self.assertEqual("NOT_RUN", validation["execution_state"])
        self.assertEqual("NOT_RUN", validation["runtime_state"])
        self.assertEqual("NOT_RUN", validation["physical_input_state"])
        self.assertEqual("HUMAN_NOT_RUN", validation["human_state"])
        self.assertEqual("NOT_CONFIGURED", template["project_test_framework"]["state"])


if __name__ == "__main__":
    unittest.main()
