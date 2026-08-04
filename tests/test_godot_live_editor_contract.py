from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from types import ModuleType

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v1.schema.json"
OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v1.schema.json"
MANIFEST = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
CONTRACT = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md"
SECURITY = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md"
ADAPTER = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
AGENTS_FRAGMENT = ROOT / "templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md"
SEMANTIC_VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


def load_semantic_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("godot_live_editor_semantics", SEMANTIC_VALIDATOR)
    if spec is None or spec.loader is None:
        raise AssertionError("semantic validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scene_inspect_capability() -> dict:
    return {
        "capability_id": "scene.inspect",
        "description": "Inspect a bounded scene summary.",
        "execution_path": "EDITOR_PLUGIN",
        "effect_class": "READ_ONLY",
        "execution_mode": "SYNCHRONOUS",
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


def project_test_capability() -> dict:
    return {
        "capability_id": "test.project",
        "description": "Run the configured project test suite once and resume by task identity.",
        "execution_path": "CLI_HEADLESS",
        "effect_class": "READ_ONLY",
        "execution_mode": "LONG_RUNNING_TASK",
        "idempotency_key_required": False,
        "approval_required": False,
        "arguments_schema": {"type": "object", "additionalProperties": False},
        "timeout_policy": {
            "milliseconds": 600000,
            "unknown_outcome": "RESUME_BY_TASK_ID",
        },
        "retry_policy": {
            "automatic": False,
            "maximum_attempts": 1,
            "requires_ledger": True,
        },
        "evidence_outputs": ["TEST_RESULT", "LOG"],
        "unsupported_states": ["IMPORTING"],
    }


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
            "detected_version": "4.6.2",
            "minimum_version": "4.3.0",
            "maximum_exclusive_version": "5.0.0",
        },
        "tool_adoption": {
            "source_type": "OPEN_SOURCE",
            "source_reference": "https://github.com/example/godot-live-editor",
            "version_pin": "v1.2.3",
            "telemetry_policy": "DISABLED",
            "external_data_policy": "NO_EXTERNAL_TRANSFER",
            "uninstall_reference": "docs/godot-live-editor.md#uninstall",
            "rollback_reference": "git:baseline-before-adapter",
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
        "capabilities": [scene_inspect_capability(), project_test_capability()],
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
        "effect_class": "READ_ONLY",
        "execution_mode": "SYNCHRONOUS",
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
            "result_hash": "d" * 64,
            "evidence": [
                {
                    "kind": "ENGINE_STATE",
                    "state": "EXECUTION_PASS",
                    "path": "artifacts/scene-summary.json",
                }
            ],
        },
    }


def valid_long_running_operation(
    effect_class: str = "APPROVAL_REQUIRED_MUTATION",
) -> dict:
    envelope = valid_operation()
    envelope["capability_id"] = "export.project"
    envelope["effect_class"] = effect_class
    envelope["execution_mode"] = "LONG_RUNNING_TASK"
    envelope["approval"] = {
        "state": "APPROVED",
        "token_binding": {
            "token_id": "approval-1",
            "project_fingerprint": envelope["project_fingerprint"],
            "capability_id": envelope["capability_id"],
            "request_hash": envelope["request_hash"],
            "effect_class": effect_class,
        },
        "expires_at": "2026-08-05T01:00:00Z",
    }
    envelope["task"] = {
        "task_id": "task-1",
        "state": "COMPLETED",
        "result_binding": {
            "project_fingerprint": envelope["project_fingerprint"],
            "capability_id": envelope["capability_id"],
            "operation_id": envelope["operation_id"],
            "task_id": "task-1",
            "result_hash": envelope["result"]["result_hash"],
        },
    }
    envelope["result"]["evidence"] = [
        {
            "kind": "EXPORT",
            "state": "EXECUTION_PASS",
            "path": "artifacts/game.zip",
        }
    ]
    return envelope


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
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))
        self.assertEqual([], list(validator.iter_errors(load(MANIFEST))))
        self.assertEqual([], list(validator.iter_errors(valid_manifest())))

    def test_effect_class_and_execution_mode_are_orthogonal(self) -> None:
        capability_validator = Draft202012Validator(load(CAPABILITY_SCHEMA))
        operation_validator = Draft202012Validator(load(OPERATION_SCHEMA))

        for effect_class in (
            "APPROVAL_REQUIRED_MUTATION",
            "NON_RETRYABLE_MUTATION",
        ):
            with self.subTest(effect_class=effect_class):
                manifest = valid_manifest()
                capability = manifest["capabilities"][1]
                capability["effect_class"] = effect_class
                capability["approval_required"] = True
                self.assertEqual([], list(capability_validator.iter_errors(manifest)))

                envelope = valid_long_running_operation(effect_class)
                self.assertEqual([], list(operation_validator.iter_errors(envelope)))

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
        capability["effect_class"] = "NON_RETRYABLE_MUTATION"
        capability["approval_required"] = True
        capability["retry_policy"]["automatic"] = True
        self.assertTrue(list(validator.iter_errors(unsafe_retry)))

    def test_configured_manifest_requires_loopback_transport_and_capabilities(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))

        external_bind = valid_manifest()
        external_bind["transport"]["bind_host"] = "0.0.0.0"
        self.assertTrue(list(validator.iter_errors(external_bind)))

        no_capabilities = valid_manifest()
        no_capabilities["capabilities"] = []
        self.assertTrue(list(validator.iter_errors(no_capabilities)))

        disabled_transport = valid_manifest()
        disabled_transport["transport"] = {
            "kind": "DISABLED",
            "enabled": False,
            "bind_host": None,
            "endpoint_identity": None,
        }
        self.assertTrue(list(validator.iter_errors(disabled_transport)))

    def test_configured_manifest_requires_engine_and_adoption_boundaries(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))

        for field in ("detected_version", "minimum_version", "maximum_exclusive_version"):
            with self.subTest(engine_field=field):
                manifest = valid_manifest()
                manifest["engine_compatibility"][field] = None
                self.assertTrue(list(validator.iter_errors(manifest)))

        for field in (
            "source_reference",
            "version_pin",
            "uninstall_reference",
            "rollback_reference",
        ):
            with self.subTest(adoption_field=field):
                manifest = valid_manifest()
                manifest["tool_adoption"][field] = None
                self.assertTrue(list(validator.iter_errors(manifest)))

    def test_mutation_and_long_running_capabilities_cannot_automatically_retry(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))

        for effect_class in (
            "APPROVAL_REQUIRED_MUTATION",
            "NON_RETRYABLE_MUTATION",
        ):
            with self.subTest(effect_class=effect_class):
                manifest = valid_manifest()
                capability = manifest["capabilities"][1]
                capability["effect_class"] = effect_class
                capability["approval_required"] = True
                capability["retry_policy"]["automatic"] = True
                self.assertTrue(list(validator.iter_errors(manifest)))

        idempotent_without_ledger = valid_manifest()
        capability = idempotent_without_ledger["capabilities"][0]
        capability["effect_class"] = "IDEMPOTENT_MUTATION"
        capability["idempotency_key_required"] = True
        capability["retry_policy"]["requires_ledger"] = False
        self.assertTrue(list(validator.iter_errors(idempotent_without_ledger)))

        long_running_without_ledger = valid_manifest()
        capability = long_running_without_ledger["capabilities"][1]
        capability["retry_policy"]["requires_ledger"] = False
        self.assertTrue(list(validator.iter_errors(long_running_without_ledger)))

    def test_operation_schema_binds_approval_shape_and_long_running_results(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA))
        self.assertEqual([], list(validator.iter_errors(valid_operation())))

        approval_gap = valid_long_running_operation()
        approval_gap["approval"]["token_binding"] = None
        self.assertTrue(list(validator.iter_errors(approval_gap)))

        task_gap = valid_long_running_operation()
        task_gap["task"]["task_id"] = None
        task_gap["task"]["result_binding"] = None
        self.assertTrue(list(validator.iter_errors(task_gap)))

    def test_approval_effect_classes_cannot_claim_not_required(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA))

        for effect_class in (
            "APPROVAL_REQUIRED_MUTATION",
            "NON_RETRYABLE_MUTATION",
        ):
            with self.subTest(effect_class=effect_class):
                envelope = valid_operation()
                envelope["effect_class"] = effect_class
                self.assertTrue(list(validator.iter_errors(envelope)))

    def test_semantic_validator_rejects_mismatched_approval_and_task_bindings(self) -> None:
        self.assertTrue(SEMANTIC_VALIDATOR.is_file(), str(SEMANTIC_VALIDATOR.relative_to(ROOT)))
        semantics = load_semantic_validator()

        valid = valid_long_running_operation()
        self.assertEqual([], semantics.validate_operation_semantics(valid))

        approval_mismatch = valid_long_running_operation()
        approval_mismatch["approval"]["token_binding"]["project_fingerprint"] = "other-project"
        self.assertIn(
            "APPROVAL_TOKEN_MISMATCH",
            semantics.validate_operation_semantics(approval_mismatch),
        )

        task_mismatch = valid_long_running_operation()
        task_mismatch["task"]["result_binding"]["operation_id"] = "other-operation"
        self.assertIn(
            "TASK_RESULT_STALE",
            semantics.validate_operation_semantics(task_mismatch),
        )

        hash_mismatch = valid_long_running_operation()
        hash_mismatch["task"]["result_binding"]["result_hash"] = "e" * 64
        self.assertIn(
            "TASK_RESULT_HASH_MISMATCH",
            semantics.validate_operation_semantics(hash_mismatch),
        )

    def test_semantic_validator_rejects_duplicate_capabilities_and_invalid_test_runner(self) -> None:
        self.assertTrue(SEMANTIC_VALIDATOR.is_file(), str(SEMANTIC_VALIDATOR.relative_to(ROOT)))
        semantics = load_semantic_validator()
        self.assertEqual([], semantics.validate_manifest_semantics(valid_manifest()))

        duplicate = valid_manifest()
        repeated = scene_inspect_capability()
        repeated["description"] = "A second action with the same ID."
        duplicate["capabilities"].append(repeated)
        self.assertIn(
            "DUPLICATE_CAPABILITY_ID",
            semantics.validate_manifest_semantics(duplicate),
        )

        missing_runner = valid_manifest()
        missing_runner["capabilities"] = [scene_inspect_capability()]
        self.assertIn(
            "PROJECT_TEST_RUNNER_NOT_DECLARED",
            semantics.validate_manifest_semantics(missing_runner),
        )

        invalid_runner = valid_manifest()
        invalid_runner["capabilities"][1]["evidence_outputs"] = ["LOG"]
        self.assertIn(
            "PROJECT_TEST_RUNNER_EVIDENCE_INVALID",
            semantics.validate_manifest_semantics(invalid_runner),
        )

    def test_operation_schema_rejects_misleading_evidence_pairings(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA))

        human_contract = valid_operation()
        human_contract["result"]["evidence"] = [
            {"kind": "HUMAN", "state": "CONTRACT_PASS", "path": None}
        ]
        self.assertTrue(list(validator.iter_errors(human_contract)))

        screenshot_physical = valid_operation()
        screenshot_physical["result"]["evidence"] = [
            {
                "kind": "SCREENSHOT",
                "state": "PHYSICAL_INPUT_PASS",
                "path": "artifacts/frame.png",
            }
        ]
        self.assertTrue(list(validator.iter_errors(screenshot_physical)))

        human_valid = valid_operation()
        human_valid["result"]["evidence"] = [
            {"kind": "HUMAN", "state": "HUMAN_PASS", "path": "reviews/human.md"}
        ]
        self.assertEqual([], list(validator.iter_errors(human_valid)))

    def test_contract_defines_bootstrap_identity_recovery_and_evidence_boundaries(self) -> None:
        combined = read(CONTRACT) + read(SECURITY)
        for term in (
            "doctor → status → catalog --compact",
            "project.godot",
            "effect_class",
            "execution_mode",
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
            "effect_class",
            "execution_mode",
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
