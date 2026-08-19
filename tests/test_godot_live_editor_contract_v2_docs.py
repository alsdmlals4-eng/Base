from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_CONTRACT = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md"
SECURITY_CONTRACT = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md"
READINESS = ROOT / "docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md"
MULTI_PROJECT_PILOT = ROOT / "docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md"
ADAPTER = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
AGENTS_FRAGMENT = ROOT / "templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md"
HIGODOT_POLICY = ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
HISTORICAL_STATUS = "HISTORICAL_BASE_ADAPTER_REFERENCE_ONLY"
CURRENT_AUTHORITY_ROUTE = "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GodotLiveEditorContractV2DocsTests(unittest.TestCase):
    maxDiff = None

    def test_v2_contracts_remain_auditable_while_project_routes_higodot(self) -> None:
        automation = read(AUTOMATION_CONTRACT)
        security = read(SECURITY_CONTRACT)
        readiness = read(READINESS)
        adapter = read(ADAPTER)
        fragment = read(AGENTS_FRAGMENT)
        policy = read(HIGODOT_POLICY)
        historical = automation + security + readiness + fragment

        for term in (
            "effect_kind",
            "idempotency",
            "approval_policy",
            "execution_mode",
            "rollback_policy",
            "contract_snapshot",
            "capability_input_schema_sha256",
            "capability_output_schema_sha256",
            "TARGET_STATE_CONFLICT",
            "OUTPUT_SCHEMA_MISMATCH",
            "MIGRATION_REQUIRED_V1",
            "V1_AUDIT_ONLY",
            "EditorUndoRedoManager",
            "--recovery-mode",
        ):
            self.assertIn(term, historical)

        for canonical_path in (
            "schemas/godot-live-editor-capability-manifest-v2.schema.json",
            "schemas/godot-live-editor-operation-envelope-v2.schema.json",
            "tools/validate_godot_live_editor_contract_v2.py",
        ):
            self.assertIn(canonical_path, historical)

        self.assertIn("hi-godot/godot-ai", adapter)
        self.assertIn("SOLE_GODOT_EXECUTION_AUTHORITY", adapter)
        self.assertIn("ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION", policy)
        self.assertNotIn("base_live_editor_adapter/", adapter)
        self.assertNotIn("| `READ_ONLY` |", adapter)
        self.assertNotIn("operation_class:", adapter)

    def test_legacy_base_adapter_docs_are_explicitly_historical(self) -> None:
        for path in (
            AUTOMATION_CONTRACT,
            SECURITY_CONTRACT,
            READINESS,
            MULTI_PROJECT_PILOT,
        ):
            body = read(path)
            with self.subTest(path=path.name):
                self.assertIn(HISTORICAL_STATUS, body)
                self.assertIn(CURRENT_AUTHORITY_ROUTE, body)
                self.assertIn("현재 Godot persistent authoring 실행 경로가 아니다", body)

        self.assertNotIn("## 활성 v2 권위", read(AUTOMATION_CONTRACT))

    def test_readiness_stays_not_ready_until_editor_transaction_gates_pass(self) -> None:
        readiness = read(READINESS)
        for gate in (
            "v2_schema_validation",
            "v2_semantic_validation",
            "v1_mutation_authority",
            "editor_main_thread_queue",
            "editor_undo_redo_transaction",
            "NOT_IMPLEMENTED",
            "NOT_READY",
        ):
            self.assertIn(gate, readiness)


if __name__ == "__main__":
    unittest.main()
