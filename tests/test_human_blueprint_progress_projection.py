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


def valid_projection() -> dict:
    return {
        "project": "Example Project",
        "source_commit": SOURCE,
        "generated_at": "2026-09-03T12:00:00+09:00",
        "included_scope": "Current vertical slice",
        "approval_status": "AWAITING_USER_FINAL_REVIEW_APPROVAL",
        "evidence_ceiling": "E4_VISUAL",
        "active_work_item_ref": "WORK-01",
        "next_action": "Run the normal-path runtime verification",
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
        "work_items": [
            {
                "work_item_id": "WORK-01",
                "title": "Verify normal clash in Godot",
                "status": "IN_PROGRESS",
                "source_ref": "https://github.com/example/project/issues/1",
                "goal_refs": ["GOAL-01"],
                "system_refs": ["SYS-01"],
                "case_refs": ["CASE-01"],
                "next_action": "Run the normal-path runtime verification",
            }
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

    def test_workspace_contract_routes_the_single_pdf_projection(self) -> None:
        self.assertTrue(WORKSPACE_CONTRACT.exists())
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
        for section in (
            "PROJECT_STATUS_DASHBOARD",
            "PROJECT_GOAL_MAP",
            "GOAL_STATUS_CARD",
            "SYSTEM_STATUS_CARD",
            "CASE_VERIFICATION_MATRIX",
            "GOAL_SYSTEM_CASE_WORK_TRACEABILITY",
        ):
            self.assertIn(
                section, contract["human_blueprint_progress_required_sections"]
            )

    def test_contract_preserves_one_pdf_and_separates_status_axes(self) -> None:
        self.assertTrue(PROJECTION_CONTRACT.exists())
        text = PROJECTION_CONTRACT.read_text(encoding="utf-8")
        for token in (
            "HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION",
            "BLUEPRINT_IS_SINGLE_HUMAN_PM_SURFACE",
            "NO_SEPARATE_PM_PDF",
            "NO_HTML_DASHBOARD",
            "DERIVED_SNAPSHOT_NOT_STATUS_OWNER",
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
            "GOAL_ID",
            "SYSTEM_ID",
            "CASE_ID",
            "WORK_ITEM_ID",
        ):
            self.assertIn(token, text)

    def test_template_contains_goal_system_case_and_work_views(self) -> None:
        self.assertTrue(PROJECTION_TEMPLATE.exists())
        text = PROJECTION_TEMPLATE.read_text(encoding="utf-8")
        for token in (
            "PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON",
            "프로젝트 작업 현황",
            "현재 작업과 다음 행동",
            "목표별 체크리스트",
            "시스템 기획별 체크리스트",
            "케이스별 검증 현황",
            "목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적",
            "source_commit",
            "generated_at",
            "evidence_ceiling",
            "NOT_APPLICABLE",
        ):
            self.assertIn(token, text)
        self.assertNotIn("<html", text.lower())

    def test_valid_projection_and_non_averaged_summary(self) -> None:
        projection = valid_projection()
        self.assertEqual(
            self.module.validate_projection(
                projection, expected_source_sha=SOURCE
            ),
            [],
        )
        summary = self.module.summarize_projection(projection)
        self.assertEqual(summary["goals"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["systems"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["cases"], {"completed": 1, "applicable": 1})
        self.assertEqual(summary["work_items"], {"completed": 0, "applicable": 1})
        self.assertEqual(summary["blocked"], 0)
        self.assertEqual(summary["user_decisions"], 0)

    def test_renderer_exposes_all_human_blueprint_sections(self) -> None:
        rendered = self.module.render_projection(
            valid_projection(), expected_source_sha=SOURCE
        )
        for token in (
            "프로젝트 작업 현황",
            "목표별 체크리스트",
            "시스템 기획별 체크리스트",
            "케이스별 검증 현황",
            "목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적",
            "0 / 1",
            "1 / 1",
            SOURCE,
        ):
            self.assertIn(token, rendered)
        self.assertNotIn("<html", rendered.lower())

    def test_source_mismatch_fails_closed(self) -> None:
        errors = self.module.validate_projection(
            valid_projection(),
            expected_source_sha="abcdef0123456789abcdef0123456789abcdef01",
        )
        self.assertTrue(any("source_commit" in error for error in errors))

    def test_unresolved_reference_is_rejected(self) -> None:
        projection = valid_projection()
        projection["systems"][0]["goal_refs"] = ["GOAL-MISSING"]
        errors = self.module.validate_projection(
            projection, expected_source_sha=SOURCE
        )
        self.assertTrue(any("GOAL-MISSING" in error for error in errors))

    def test_pass_without_evidence_is_rejected(self) -> None:
        projection = valid_projection()
        projection["cases"][0]["verification"][0]["evidence"] = []
        errors = self.module.validate_projection(
            projection, expected_source_sha=SOURCE
        )
        self.assertTrue(any("evidence" in error for error in errors))

    def test_not_applicable_requires_reason_and_is_excluded(self) -> None:
        projection = valid_projection()
        del projection["cases"][1]["reason"]
        errors = self.module.validate_projection(
            projection, expected_source_sha=SOURCE
        )
        self.assertTrue(any("reason" in error for error in errors))

    def test_blocked_work_requires_blocker_and_resume_condition(self) -> None:
        projection = valid_projection()
        projection["work_items"][0]["status"] = "BLOCKED_UNVERIFIED"
        projection["active_work_item_ref"] = None
        errors = self.module.validate_projection(
            projection, expected_source_sha=SOURCE
        )
        self.assertTrue(any("blocker" in error for error in errors))
        self.assertTrue(any("resume_condition" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
