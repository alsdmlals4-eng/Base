import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"
INSTRUCTION = (
    ROOT
    / "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md"
)
WORK_POLICY = ROOT / "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md"
WORK_TEMPLATE = ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md"
V4_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class BlueprintProgressIncrementalRevisionContractTests(unittest.TestCase):
    def test_human_blueprint_contains_goal_system_case_progress_projection(self):
        policy = text(POLICY)
        for token in (
            "BLUEPRINT_GOAL_SYSTEM_CASE_PROGRESS_PROJECTION",
            "PROJECT_GOAL_STATUS_SUMMARY",
            "GOAL_LEVEL_CHECKLIST",
            "SYSTEM_LEVEL_CHECKLIST",
            "CASE_LEVEL_STATUS_MATRIX",
            "BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION",
            "PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION",
            "NO_SEPARATE_PM_PDF_OR_HTML",
            "PASS_ONLY_COUNTS_COMPLETE",
        ):
            self.assertIn(token, policy)

    def test_existing_blueprint_is_incrementally_revised_without_silent_loss(self):
        required = (
            "EXISTING_BLUEPRINT_INCREMENTAL_REVISION_REQUIRED",
            "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS",
            "PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY",
            "STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION",
            "SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED",
            "UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN",
            "BLUEPRINT_LOSS_REGRESSION_GATE",
            "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED",
        )
        for path in (POLICY, INSTRUCTION):
            content = text(path)
            for token in required:
                self.assertIn(token, content, f"{path} must contain {token}")

    def test_pm_receipt_is_the_projection_source_not_a_parallel_canon(self):
        required = (
            "BLUEPRINT_PDF_PROGRESS_PROJECTION",
            "PROJECT_WORK_KANBAN_IS_PROGRESS_SOURCE",
            "GOAL_SYSTEM_CASE_TRACEABILITY",
            "NO_PARALLEL_BLUEPRINT_STATUS_CANON",
        )
        for path in (WORK_POLICY, WORK_TEMPLATE):
            content = text(path)
            for token in required:
                self.assertIn(token, content, f"{path} must contain {token}")

    def test_v4_machine_contract_routes_incremental_revision_and_progress_views(self):
        contract = json.loads(text(V4_CONTRACT))
        revision = contract["blueprint_revision_contract"]
        self.assertEqual(
            "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS",
            revision["mode"],
        )
        self.assertIn(
            "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS",
            revision["forbidden_modes"],
        )
        self.assertEqual(
            [
                "predecessor_blueprint_ref",
                "predecessor_source_commit",
                "predecessor_inventory",
                "successor_inventory",
                "semantic_delta_summary",
                "removal_or_downgrade_justifications",
            ],
            revision["required_receipts"],
        )

        projection = contract["human_blueprint_progress_projection"]
        self.assertEqual(
            "PROJECT_WORK_KANBAN_AND_REPOSITORY_EVIDENCE",
            projection["source"],
        )
        self.assertEqual(
            [
                "PROJECT_GOAL_STATUS_SUMMARY",
                "GOAL_LEVEL_CHECKLIST",
                "SYSTEM_LEVEL_CHECKLIST",
                "CASE_LEVEL_STATUS_MATRIX",
                "BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION",
            ],
            projection["required_views"],
        )
        self.assertEqual(
            [
                "DOCUMENTED",
                "IMPLEMENTED",
                "AUTOMATED_TEST_PASS",
                "RUNTIME_VERIFIED",
                "UX_VERIFIED",
                "USER_APPROVED",
            ],
            projection["evidence_dimensions"],
        )
        for metadata in (
            "predecessor_blueprint_ref",
            "predecessor_source_commit",
            "revision_mode",
            "semantic_delta_summary",
            "work_status_snapshot_at",
        ):
            self.assertIn(metadata, contract["human_pdf_required_metadata"])

    def test_existing_two_artifact_and_evidence_boundaries_remain_intact(self):
        policy = text(POLICY)
        instruction = text(INSTRUCTION)
        for token in (
            "EXACTLY_TWO_DELIVERABLES",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            "REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION",
            "NO_MASS_BLUEPRINT_BACKFILL",
            "RUNTIME_TRUTH_SEPARATE",
            "NO_AUTOMATIC_IMAGE_GENERATION",
        ):
            self.assertIn(token, policy)
        for token in (
            "정확히 2개",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            "REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION",
            "NO_MASS_BLUEPRINT_BACKFILL",
            "NO_AUTOMATIC_IMAGE_GENERATION",
        ):
            self.assertIn(token, instruction)


if __name__ == "__main__":
    unittest.main()
