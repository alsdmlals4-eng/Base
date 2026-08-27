from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
POLICY = ROOT / "templates/project-operations/WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md"
CASE = ROOT / "docs/knowledge/cases/WORK_INSTRUCTION_SUPERSET_RECONCILIATION_CASE.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"
CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"


class WorkInstructionSupersetReconciliationContractTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"required contract file must exist: {path}")
        return path.read_text(encoding="utf-8")

    def test_current_router_is_thin_and_routes_all_current_owners(self) -> None:
        text = self._read(ROUTER)
        for token in (
            "WORK_PROJECT_EXECUTION_CURRENT_ROUTER",
            "THIN_ROUTER_NOT_SECOND_CANON",
            "WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md",
            "CURRENT_BASE_OWNER_WINS_ON_DRIFT",
            "PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST",
        ):
            self.assertIn(token, text)
        self.assertLess(len(text.splitlines()), 180, "router must remain concise")

    def test_existing_core_work_bundle_is_preserved(self) -> None:
        for path in (STARTER, CHECKLIST, PROFILE):
            self.assertTrue(path.exists(), f"current owner must remain present: {path}")
        checklist = self._read(CHECKLIST)
        for token in (
            "PROJECT_START_CANON_CHECKLIST",
            "CORE_FUN_AND_SYSTEM_ALIGNMENT_REQUIRED",
            "SWOT_IS_CURRENT_EVIDENCE_BASED_NOT_GENERIC_MARKETING",
            "REMAINING_WORK_AND_ORDER_DERIVED_FROM_CURRENT_CANON",
            "STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST",
        ):
            self.assertIn(token, checklist)

    def test_product_and_router_identity_are_not_conflated(self) -> None:
        text = self._read(POLICY)
        for token in (
            "PRODUCT_BASELINE_AND_ROUTER_SYNC_IDENTITY_SEPARATION",
            "current_completed_product_main",
            "latest_router_or_documentation_sync",
            "current_validation_head",
            "candidate_product_head",
            "DOCUMENTATION_ONLY_MERGE_DOES_NOT_REWRITE_PRODUCT_BASELINE",
        ):
            self.assertIn(token, text)

    def test_exact_candidate_freshness_is_product_byte_aware(self) -> None:
        text = self._read(POLICY)
        for token in (
            "EXACT_CANDIDATE_FRESHNESS_RULE",
            "PLAYER_FACING_BYTE_CHANGE_INVALIDATES_CANDIDATE",
            "HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE",
            "TOOLING_DOC_TEST_ONLY_CHANGE_DOES_NOT_AUTO_INVALIDATE",
            "CANON_DRIFT_FAIL_CLOSED",
            "CONTEXT_DRIFT_RECHECK_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_ci_result_chain_is_stronger_than_test_logic_only(self) -> None:
        text = self._read(POLICY)
        for token in (
            "TEST_LOGIC_PASS_IS_NOT_CI_GATE_PASS",
            "CI_RESULT_CHAIN_INTEGRITY_REQUIRED",
            "EXACT_VALIDATOR_IDENTITY_REQUIRED",
            "test runner exit status",
            "formal result",
            "summary/parser",
            "required diagnostic/build artifact",
            "exact current HEAD",
            "NO_TEST_OR_WORKFLOW_WEAKENING_TO_FORCE_GREEN",
        ):
            self.assertIn(token, text)

    def test_godot_generated_output_is_version_and_adoption_aware(self) -> None:
        text = self._read(POLICY)
        for token in (
            "GENERATED_IMPORT_OUTPUT_CLASSIFICATION_REQUIRED",
            "IMPORT_CACHE_DIFF_IS_NOT_PRODUCT_SOURCE_DIFF",
            "NEVER_STAGE_GENERATED_IMPORT_NOISE",
            "NO_BLANKET_UID_OR_ADOPTED_ADDON_IGNORE",
            ".godot/",
            ".uid",
            "addons/gut",
            "exact engine version",
            "adoption record",
        ):
            self.assertIn(token, text)

    def test_visual_candidate_and_runtime_promotion_delegate_to_current_local_owner(self) -> None:
        text = self._read(POLICY)
        for token in (
            "VISUAL_CANDIDATE_RUNTIME_PROMOTION_SEPARATION",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "LOCAL_VISUAL_CANDIDATE",
            "PROJECT_ASSET_APPROVED",
            "RUNTIME_PROMOTED",
            "NO_NOTION_BINARY_UPLOAD_REQUIRED",
            "SHA-256",
            "actual consumer",
            "runtime evidence",
            "NO_VISUAL_GENERATION_AUTHORITY_EXPANSION",
        ):
            self.assertIn(token, text)
        self.assertNotIn("Notion direct attachment", text)

    def test_remote_sync_and_completed_automation_cleanup_are_explicit(self) -> None:
        text = self._read(POLICY)
        for token in (
            "REMOTE_SYNC_STATE_EXPLICIT_IN_CANON_LINKS",
            "LOCAL_ONLY_NOT_REMOTE_SYNCED",
            "REMOTE_HEAD_READBACK_REQUIRED",
            "COMPLETED_AUTOMATION_HEARTBEAT_CLEANUP",
            "merge",
            "post-merge main readback",
            "Notion",
            "durable completion receipt",
        ):
            self.assertIn(token, text)

    def test_project_specific_values_are_excluded_and_evidence_ceiling_preserved(self) -> None:
        combined = self._read(POLICY) + "\n" + self._read(CASE)
        for token in (
            "PROJECT_SPECIFIC_VALUES_EXCLUDED",
            "PROJECT_SPECIFIC_PR_AND_PATH_STAY_IN_PROJECT_CANON",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "NO_PUBLIC_RELEASE_AUTHORITY",
            "ZERO_INCREMENTAL_COST_REQUIRED",
        ):
            self.assertIn(token, combined)

    def test_case_records_preserved_improved_delegated_rejected_and_corrected_items(self) -> None:
        text = self._read(CASE)
        for token in (
            "PRESERVED",
            "IMPROVED",
            "DELEGATED_TO_CURRENT_OWNER",
            "REJECTED_AS_PROJECT_SPECIFIC",
            "CORRECTED_AS_UNSAFE_GENERALIZATION",
            "BCP-2026-039",
            "PR #735",
            "PR #736",
            "official evidence",
            "rollback",
        ):
            self.assertIn(token, text)
        self.assertNotIn("Notion direct attachment", text)


if __name__ == "__main__":
    unittest.main()
