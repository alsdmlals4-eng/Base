from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"
CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
V49 = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"


class WorkProjectStartCanonChecklistContractTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"required Work contract must exist: {path}")
        return path.read_text(encoding="utf-8")

    def test_starter_routes_startup_canon_checklist_before_new_work(self) -> None:
        text = self._read(STARTER)
        for token in (
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST",
            "PROJECT_START_CANON_CHECKLIST_REQUIRED",
            "NO_NEW_SLICE_WORK_BEFORE_STARTUP_CORRECTION_OR_EXPLICIT_DEFER",
        ):
            self.assertIn(token, text)
        self.assertLess(
            text.index("STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST"),
            text.index("WORK_PRODUCTION_INPUT_PACKET"),
        )

    def test_checklist_surfaces_core_fun_core_systems_remaining_work_and_order(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "PROJECT_START_CANON_CHECKLIST",
            "project_goal:",
            "player_promise:",
            "pointed_fun:",
            "core_loop:",
            "core_systems:",
            "meaningful_choices:",
            "reward_and_failure_learning:",
            "current_stage:",
            "roadmap_or_milestones:",
            "accepted_frontier:",
            "active_playable_slice:",
            "next_playable_slice_candidate:",
            "remaining_required_work:",
            "work_order:",
            "next_safe_action:",
            "STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_swot_is_evidence_based_and_not_a_generic_marketing_fill_in(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "SWOT_IS_CURRENT_EVIDENCE_BASED_NOT_GENERIC_MARKETING",
            "strengths:",
            "weaknesses:",
            "opportunities:",
            "threats:",
            "evidence_and_owner:",
            "NOT_RUN",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
        ):
            self.assertIn(token, text)

    def test_canon_correction_precedes_new_planning_production_or_implementation(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST",
            "CORRECTION_BEFORE_PRODUCTION",
            "CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON",
            "CURRENT / HISTORICAL / SUPERSEDED / CONFLICT / UNKNOWN_UNVERIFIED",
            "GitHub structured canon",
            "Notion human canon",
            "destination readback",
            "USER_DECISION_REQUIRED",
            "READY_AFTER_CORRECTION | BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, text)

    def test_previous_v48_v49_capabilities_remain_discoverable_in_current_bundle(self) -> None:
        files = (STARTER, CHECKLIST, V49, APPENDIX, PROFILE)
        bundle = "\n".join(self._read(path) for path in files)
        for token in (
            "REVISION_NON_REGRESSION_GATE",
            "WHOLE_PROJECT_AUDIT_FIRST",
            "REUSE_FIRST_PREFLIGHT_REQUIRED",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "VISUAL_REQUIREMENT_DELETE_TEST_GATE",
            "IMPLEMENTATION_REALITY_GATE",
            "PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY",
            "RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE",
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE",
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "CURRENT_SKILL_REGISTRY_COVERAGE_GATE",
            "DOMAIN_SPLIT_CANON",
            "TEXT_BRIEF_STOP_REQUIRED",
            "VISUAL_ASSET_COVERAGE",
            "ART_STYLE_LOCK",
            "DECISION_SCREEN_COMPREHENSION_GATE",
            "MULTI_PLATFORM_SHARED_CORE_GATE",
            "AUDIO_VISUAL_POC_EVIDENCE",
            "CANONICAL_REFLECTION_AFTER_PLAY",
            "EVIDENCE_EQUIVALENT_FALLBACK_ONLY",
            "INCIDENT_SOLUTION_LESSON_LOOP",
            "REQUIRED_WORK_REMAINING: 0",
            "COMPLETION_CANDIDATE",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "REMOTE_HEAD_READBACK_AFTER_PUSH",
            "NO_DIRECT_MAIN_PUSH",
            "NO_FORCE_PUSH",
            "LOCAL_COMPUTER_CONTROL_DELEGATED",
            "AUTO_LAUNCH_GODOT_WHEN_CALLABLE",
        ):
            self.assertIn(token, bundle)

    def test_checklist_defines_receipt_format_without_becoming_project_canon(self) -> None:
        text = self._read(CHECKLIST)
        self.assertIn("project-specific 실행 receipt의 형식과 Gate", text)
        self.assertIn("CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON", text)
        self.assertIn("durable 사실과 결정은 분야별 GitHub structured canon과 Notion human canon이 소유", text)

    def test_work_order_is_dependency_and_player_value_driven(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "priority:",
            "status:",
            "why_now:",
            "dependency:",
            "player_value:",
            "risk_or_blocker:",
            "owner:",
            "acceptance:",
            "verification:",
            "fallback_or_defer:",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
