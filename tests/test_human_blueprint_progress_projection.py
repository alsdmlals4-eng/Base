from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
PROJECTION_CONTRACT = (
    ROOT
    / "docs/operations/project-workspace/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_CONTRACT.md"
)
PROJECTION_TEMPLATE = (
    ROOT / "templates/project-operations/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_TEMPLATE.md"
)
PROJECTION_TOOL = ROOT / "tools/human_blueprint_progress_projection.py"
SOURCE = "0123456789abcdef0123456789abcdef01234567"
OTHER_SOURCE = "abcdef0123456789abcdef0123456789abcdef01"


def valid_board() -> dict:
    return {
        "goal_or_slice_issue_ref": "https://github.com/example/project/issues/1",
        "source_main_sha": SOURCE,
        "work_item_refs": ["WORK-01"],
        "active_work_item_ref": "WORK-01",
        "next_action": "Run the normal-path runtime verification",
        "work_items": [
            {
                "work_item_id": "WORK-01",
                "title": "Verify normal clash in Godot",
                "status": "IN_PROGRESS",
                "canon_owner": "docs/design/PROJECT_AI_PRODUCTION_SPEC.md#SYS-01",
                "actual_consumers": ["scenes/combat/combat.tscn"],
                "depends_on": [],
                "acceptance_criteria": ["AC-01"],
                "required_evidence": ["E3_RUNTIME"],
                "checklist": [
                    {
                        "id": "AC-01",
                        "text": "Run the normal clash and observe the expected result",
                        "status": "NOT_RUN",
                        "evidence": [],
                    }
                ],
                "verification": [
                    {
                        "level": "E3_RUNTIME",
                        "status": "NOT_RUN",
                        "evidence": [],
                    }
                ],
                "next_action": "Run the normal-path runtime verification",
            }
        ],
    }


def valid_projection() -> dict:
    return {
        "project": "Example Project",
        "source_commit": SOURCE,
        "generated_at": "2026-09-03T12:00:00+09:00",
        "included_scope": "Current vertical slice",
        "approval_status": "AWAITING_USER_FINAL_REVIEW_APPROVAL",
        "evidence_ceiling": "E4_VISUAL",
        "work_status_snapshot_source": "receipts/current-work-contract.json#project_work_kanban",
        "work_status_snapshot_generated_at": "2026-09-03T11:59:00+09:00",
        "work_status_snapshot_staleness": "CURRENT_AT_SOURCE_SHA",
        "progress_calculation_basis": "INDEPENDENT_GOAL_SYSTEM_CASE_WORK_COUNTS",
        "project_work_kanban": valid_board(),
        "work_item_links": [
            {
                "work_item_id": "WORK-01",
                "goal_refs": ["GOAL-01"],
                "system_refs": ["SYS-01"],
                "case_refs": ["CASE-01"],
            }
        ],
        "goals": [
            {
                "goal_id": "GOAL-01",
                "title": "Complete one understandable battle",
                "player_value": "The player can predict, choose, and understand the result.",
                "maturity_status": "IMPLEMENTED",
                "target_status": "RUNTIME_VERIFIED",
                "system_refs": ["SYS-01"],
                "case_refs": ["CASE-01", "CASE-02"],
                "work_item_refs": ["WORK-01"],
                "checklist": [
                    {
                        "id": "GOAL-CHECK-01",
                        "text": "Player value and completion boundary are confirmed",
                        "status": "PASS",
                        "evidence": ["docs/design/PROJECT_AI_PRODUCTION_SPEC.md#GOAL-01"],
                    },
                    {
                        "id": "GOAL-CHECK-02",
                        "text": "The complete battle flow is runtime verified",
                        "status": "NOT_RUN",
                        "evidence": [],
                    },
                ],
                "next_action": "Verify the battle in the actual runtime",
            }
        ],
        "systems": [
            {
                "system_id": "SYS-01",
                "title": "Clash resolution",
                "player_value": "The result follows visible choices and rules.",
                "maturity_status": "IMPLEMENTED",
                "target_status": "RUNTIME_VERIFIED",
                "goal_refs": ["GOAL-01"],
                "case_refs": ["CASE-01", "CASE-02"],
                "work_item_refs": ["WORK-01"],
                "canon_owner": "docs/design/PROJECT_AI_PRODUCTION_SPEC.md#SYS-01",
                "actual_consumers": ["scenes/combat/combat.tscn"],
                "checklist": [
                    {
                        "id": "SYS-CHECK-01",
                        "text": "Inputs, outputs, state, data owner, and consumers are specified",
                        "status": "PASS",
                        "evidence": ["docs/design/PROJECT_AI_PRODUCTION_SPEC.md#SYS-01"],
                    },
                    {
                        "id": "SYS-CHECK-02",
                        "text": "Runtime, visual, and play evidence are complete",
                        "status": "NOT_RUN",
                        "evidence": [],
                    },
                ],
                "next_action": "Verify the normal clash path",
            }
        ],
        "cases": [
            {
                "case_id": "CASE-01",
                "title": "Player wins a normal clash",
                "case_type": "NORMAL",
                "system_ref": "SYS-01",
                "goal_refs": ["GOAL-01"],
                "work_item_refs": ["WORK-01"],
                "applicability": "APPLICABLE",
                "maturity_status": "RUNTIME_VERIFIED",
                "target_status": "RUNTIME_VERIFIED",
                "required_evidence": ["E2_TEST", "E3_RUNTIME"],
                "verification": [
                    {
                        "level": "E2_TEST",
                        "status": "PASS",
                        "evidence": ["pytest tests/test_clash.py"],
                    },
                    {
                        "level": "E3_RUNTIME",
                        "status": "PASS",
                        "evidence": ["evidence/clash-normal-runtime.txt"],
                    },
                ],
                "next_action": "No remaining action in the current scope",
            },
            {
                "case_id": "CASE-02",
                "title": "Save and reload during clash",
                "case_type": "SAVE_LOAD",
                "system_ref": "SYS-01",
                "goal_refs": ["GOAL-01"],
                "work_item_refs": [],
                "applicability": "NOT_APPLICABLE",
                "reason": "The current vertical slice excludes mid-battle save/load.",
                "maturity_status": "DOCUMENTED",
                "target_status": "RUNTIME_VERIFIED",
                "required_evidence": [],
                "verification": [],
                "next_action": "Re-evaluate when save/load enters the approved scope",
            },
        ],
    }


class HumanBlueprintProgressProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PROJECTION_TOOL.exists():
            raise AssertionError(f"projection validator must exist: {PROJECTION_TOOL}")
        spec = importlib.util.spec_from_file_location(
            "human_blueprint_progress_projection", PROJECTION_TOOL
        )
        if spec is None or spec.loader is None:
            raise AssertionError("projection validator could not be loaded")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_workspace_contract_routes_single_pdf_and_direct_pm_source(self) -> None:
        contract = json.loads(WORKSPACE_CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(
            contract["human_blueprint_progress_projection_contract"],
            "docs/operations/project-workspace/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_CONTRACT.md",
        )
        self.assertEqual(
            contract["human_blueprint_progress_projection_template"],
            "templates/project-operations/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_TEMPLATE.md",
        )
        self.assertEqual(
            contract["human_blueprint_progress_projection_validator"],
            "tools/human_blueprint_progress_projection.py",
        )
        self.assertEqual(
            contract["human_blueprint_progress_source"],
            "REPOSITORY_OWNER_PLUS_PROJECT_WORK_KANBAN",
        )
        self.assertTrue(contract["human_blueprint_project_work_kanban_direct_source"])
        for section in (
            "PROJECT_STATUS_DASHBOARD",
            "CURRENT_WORK_AND_NEXT_ACTION",
            "PROJECT_GOAL_MAP",
            "GOAL_STATUS_CARD",
            "SYSTEM_STATUS_CARD",
            "CASE_VERIFICATION_MATRIX",
            "GOAL_SYSTEM_CASE_WORK_TRACEABILITY",
        ):
            self.assertIn(section, contract["human_blueprint_progress_required_sections"])

    def test_contract_preserves_one_pdf_and_separates_status_axes(self) -> None:
        text = PROJECTION_CONTRACT.read_text(encoding="utf-8")
        for token in (
            "HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION",
            "BLUEPRINT_IS_SINGLE_HUMAN_PM_SURFACE",
            "NO_SEPARATE_PM_PDF",
            "NO_HTML_DASHBOARD",
            "DERIVED_SNAPSHOT_NOT_STATUS_OWNER",
            "PROJECT_WORK_KANBAN_DIRECT_SOURCE_NO_STATUS_COPY",
            "GOAL_AND_SYSTEM_EVIDENCE_BACKED_CHECKLISTS",
            "REPOSITORY_OWNER_PLUS_PROJECT_WORK_KANBAN",
            "PROJECT_STATUS_DASHBOARD",
            "CURRENT_WORK_AND_NEXT_ACTION",
            "PROJECT_GOAL_MAP",
            "GOAL_STATUS_CARD",
            "SYSTEM_STATUS_CARD",
            "CASE_VERIFICATION_MATRIX",
            "GOAL_SYSTEM_CASE_WORK_TRACEABILITY",
            "MATURITY_WORK_EVIDENCE_AXES_SEPARATE",
            "PASS_ONLY_COUNTS_COMPLETE",
            "NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR",
            "DO_NOT_AVERAGE_CHILD_PERCENTAGES",
            "SOURCE_SHA_MATCH_REQUIRED",
            "STALE_SNAPSHOT_VISIBLE",
            "EVIDENCE_CEILING_ENFORCED",
            "GOAL_ID",
            "SYSTEM_ID",
            "CASE_ID",
            "WORK_ITEM_ID",
        ):
            self.assertIn(token, text)

    def test_template_contains_goal_system_case_and_work_views(self) -> None:
        text = PROJECTION_TEMPLATE.read_text(encoding="utf-8")
        for token in (
            "PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON",
            "프로젝트 작업 현황",
            "현재 작업과 다음 행동",
            "목표별 체크리스트",
            "시스템 기획별 체크리스트",
            "케이스별 검증 현황",
            "목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적",
            "work_status_snapshot_source",
            "work_status_snapshot_staleness",
            "progress_calculation_basis",
            "NOT_APPLICABLE",
        ):
            self.assertIn(token, text)
        self.assertNotIn("<html", text.lower())

    def test_valid_projection_and_non_averaged_summary(self) -> None:
        projection = valid_projection()
        self.assertEqual(
            self.module.validate_projection(projection, expected_source_sha=SOURCE),
            [],
        )
        summary = self.module.summarize_projection(projection)
        self.assertEqual(summary["goals"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["systems"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["cases"], {"completed": 1, "applicable": 1})
        self.assertEqual(summary["work_items"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["blocked"], 0)
        self.assertEqual(summary["user_decisions"], 0)

    def test_renderer_exposes_checklists_case_evidence_and_pm_status(self) -> None:
        rendered = self.module.render_projection(
            valid_projection(), expected_source_sha=SOURCE
        )
        for token in (
            "프로젝트 작업 현황",
            "목표별 체크리스트",
            "시스템 기획별 체크리스트",
            "케이스별 검증 현황",
            "목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적",
            "Player value and completion boundary are confirmed",
            "Inputs, outputs, state, data owner, and consumers are specified",
            "E2_TEST: PASS",
            "E3_RUNTIME: PASS",
            "IN_PROGRESS",
            "0 / 1",
            "1 / 1",
            SOURCE,
        ):
            self.assertIn(token, rendered)
        self.assertNotIn("<html", rendered.lower())

    def test_legacy_standalone_work_item_copy_is_rejected(self) -> None:
        projection = valid_projection()
        projection["work_items"] = projection.pop("project_work_kanban")["work_items"]
        projection.pop("work_item_links")
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("project_work_kanban" in error for error in errors))

    def test_board_source_sha_mismatch_fails_closed(self) -> None:
        projection = valid_projection()
        projection["project_work_kanban"]["source_main_sha"] = OTHER_SOURCE
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("source_main_sha" in error for error in errors))

    def test_work_link_ids_must_match_board_ids_exactly(self) -> None:
        projection = valid_projection()
        projection["work_item_links"] = []
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("work_item_links" in error for error in errors))

    def test_source_mismatch_fails_closed(self) -> None:
        errors = self.module.validate_projection(
            valid_projection(), expected_source_sha=OTHER_SOURCE
        )
        self.assertTrue(any("source_commit" in error for error in errors))

    def test_current_publication_rejects_stale_snapshot_flag(self) -> None:
        projection = valid_projection()
        projection["work_status_snapshot_staleness"] = "STALE_SNAPSHOT"
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("staleness" in error for error in errors))

    def test_timestamps_require_timezone_and_snapshot_cannot_be_future(self) -> None:
        projection = valid_projection()
        projection["generated_at"] = "2026-09-03T12:00:00"
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("generated_at" in error for error in errors))

        projection = valid_projection()
        projection["work_status_snapshot_generated_at"] = "2026-09-03T12:01:00+09:00"
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("later than" in error for error in errors))

    def test_unresolved_reference_is_rejected(self) -> None:
        projection = valid_projection()
        projection["systems"][0]["goal_refs"] = ["GOAL-MISSING"]
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("GOAL-MISSING" in error for error in errors))

    def test_goal_or_system_pass_without_evidence_is_rejected(self) -> None:
        projection = valid_projection()
        projection["goals"][0]["checklist"][0]["evidence"] = []
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("checklist" in error and "evidence" in error for error in errors))

    def test_case_pass_without_evidence_is_rejected(self) -> None:
        projection = valid_projection()
        projection["cases"][0]["verification"][0]["evidence"] = []
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("verification" in error and "evidence" in error for error in errors))

    def test_applicable_case_requires_nonempty_required_evidence(self) -> None:
        projection = valid_projection()
        projection["cases"][0]["required_evidence"] = []
        projection["cases"][0]["verification"] = []
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("applicable case" in error for error in errors))

    def test_evidence_ceiling_is_known_and_enforced(self) -> None:
        projection = valid_projection()
        projection["evidence_ceiling"] = "E9_UNKNOWN"
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("evidence_ceiling" in error for error in errors))

        projection = valid_projection()
        projection["evidence_ceiling"] = "E2_TEST"
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("exceeds evidence ceiling" in error for error in errors))

    def test_not_applicable_requires_reason_and_is_excluded(self) -> None:
        projection = valid_projection()
        del projection["cases"][1]["reason"]
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("reason" in error for error in errors))

    def test_no_applicable_case_count_is_not_zero_over_zero(self) -> None:
        projection = valid_projection()
        projection["cases"][0]["applicability"] = "NOT_APPLICABLE"
        projection["cases"][0]["reason"] = "Runtime cases are outside this planning-only snapshot."
        projection["cases"][0]["required_evidence"] = []
        projection["cases"][0]["verification"] = []
        rendered = self.module.render_projection(projection, expected_source_sha=SOURCE)
        self.assertIn("NO_APPLICABLE_CHECKLIST", rendered)
        self.assertNotIn("| 플레이 케이스 | 0 / 0 |", rendered)

    def test_blocked_work_requires_blocker_and_resume_condition(self) -> None:
        projection = valid_projection()
        work = projection["project_work_kanban"]["work_items"][0]
        work["status"] = "BLOCKED_UNVERIFIED"
        projection["project_work_kanban"]["active_work_item_ref"] = None
        errors = self.module.validate_projection(projection, expected_source_sha=SOURCE)
        self.assertTrue(any("blocker" in error for error in errors))
        self.assertTrue(any("resume_condition" in error for error in errors))

    def test_renderer_escapes_embedded_html_and_table_controls(self) -> None:
        projection = valid_projection()
        projection["goals"][0]["title"] = "Goal <script>alert(1)</script> | unsafe"
        rendered = self.module.render_projection(projection, expected_source_sha=SOURCE)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("\\|", rendered)


if __name__ == "__main__":
    unittest.main()
