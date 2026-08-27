from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"


class WorkCodexMinimumTransitionAutomationContractTests(unittest.TestCase):
    def _profile_text(self) -> str:
        self.assertTrue(PROFILE.exists(), "opt-in minimum-transition profile must exist")
        return PROFILE.read_text(encoding="utf-8")

    def test_profile_is_discoverable_from_the_work_bundle(self) -> None:
        appendix = APPENDIX.read_text(encoding="utf-8")
        self.assertTrue(PROFILE.exists(), "opt-in minimum-transition profile must exist")
        self.assertIn("WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md", appendix)
        self.assertIn("EXPLICIT_USER_DELEGATION_REQUIRED", appendix)

    def test_profile_defines_five_macro_stages_with_one_codex_window(self) -> None:
        text = self._profile_text()
        stages = (
            "STAGE_1_PLANNING",
            "STAGE_2_PRE_PRODUCTION_REVIEW",
            "STAGE_3_ASSET_AND_ELEMENT_PRODUCTION",
            "STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE",
            "STAGE_5_USER_VALIDATION",
        )
        for stage in stages:
            self.assertIn(stage, text)
        positions = [text.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        for token in (
            "WORK_PREP_COMPLETION_BEFORE_CODEX",
            "WORK_PRODUCTION_INPUT_BATCH",
            "MINIMIZE_WORK_CODEX_TRANSITIONS",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "CONSOLIDATED_RETURN_PACKET",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertNotIn("## 1. Three-stage minimum-transition flow", text)
        self.assertLess(text.index("STAGE_1_PLANNING"), text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"))
        self.assertLess(text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"), text.index("STAGE_5_USER_VALIDATION"))

    def test_routine_approval_is_delegated_but_high_risk_remains_deferred(self) -> None:
        text = self._profile_text()
        for token in (
            "DELEGATED_RECOMMENDED_DEFAULT_APPROVAL",
            "NO_ROUTINE_APPROVAL_STOPS",
            "HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE",
            "HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE",
            "NO_AUTOMATIC_SCOPE_EXPANSION",
        ):
            self.assertIn(token, text)
        for risk in (
            "IRREVERSIBLE_DATA_LOSS",
            "ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION",
            "NEW_PAID_COST",
            "LEGAL_OR_RIGHTS_UNCERTAINTY",
            "PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION",
            "FORCE_DIRECT_MAIN_ADMIN_BYPASS",
        ):
            self.assertIn(risk, text)

    def test_stall_recovery_and_scope_bounded_zero_are_explicit(self) -> None:
        text = self._profile_text()
        for token in (
            "STALL_SIGNAL_ROUTE_SWITCH",
            "BOUNDED_RETRY_THEN_FALLBACK",
            "EVIDENCE_EQUIVALENT_FALLBACK_ONLY",
            "DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK",
            "SCOPE_BOUNDED_REQUIRED_WORK_ZERO",
            "AUTOMATION_PHASE_REMAINING_WORK_ZERO",
            "COMPLETION_CANDIDATE_RESCAN",
        ):
            self.assertIn(token, text)

    def test_machine_qa_is_required_without_claiming_human_or_player_pass(self) -> None:
        text = self._profile_text()
        for token in (
            "MACHINE_QA_FIRST",
            "GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED",
            "HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED",
            "HERA_PERSISTENT_AUTHORING_FORBIDDEN",
            "HERA_PHASE_SOURCE_DELTA_NONE",
            "HUMAN_QA_DEFERRED_BY_CURRENT_USER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "AUTOMATED_VERTICAL_SLICE_READY",
        ):
            self.assertIn(token, text)

    def test_automated_readiness_requires_completed_codex_implementation(self) -> None:
        text = self._profile_text()
        self.assertIn("Codex one-window implementation completed", text)
        self.assertNotIn("Codex one-window implementation attempted", text)

    def test_work_final_review_is_stage4_closeout_before_user_validation(self) -> None:
        text = self._profile_text()
        self.assertIn("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION", text)
        self.assertIn("WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT", text)
        self.assertLess(
            text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"),
            text.index("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION"),
        )
        self.assertLess(
            text.index("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION"),
            text.index("STAGE_5_USER_VALIDATION"),
        )

    def test_automated_ready_is_not_validated_vertical_slice_complete(self) -> None:
        text = self._profile_text()
        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE", text)
        self.assertIn("ACTUAL_USER_PLAY_REQUIRED", text)
        self.assertIn("NEXT_SLICE_REQUIRES_STAGE5_DECISION", text)

    def test_missing_adopted_qa_tool_requires_evidence_equivalent_machine_qa(self) -> None:
        text = self._profile_text()
        self.assertIn("EVIDENCE_EQUIVALENT_MACHINE_QA_REQUIRED_WHEN_NOT_ADOPTED", text)
        self.assertIn("BLOCKING_HIGH_RISK_PREVENTS_PHASE_ADVANCE", text)

    def test_profile_composes_current_owners_instead_of_becoming_second_canon(self) -> None:
        text = self._profile_text()
        for token in (
            "COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON",
            "continuous-work-execution.md",
            "docs/GPT_CODEX_WORKFLOW_POLICY.md",
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            "IMAGE_CONVERSATION_APPROVAL_GATE.md",
            "skills/designing-vertical-slices/SKILL.md",
            "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
        ):
            self.assertIn(token, text)

    def test_default_approval_and_owner_boundaries_are_preserved(self) -> None:
        text = self._profile_text()
        for token in (
            "OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT",
            "DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION",
            "WORK_NONPRODUCT_OWNER_PRESERVED",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED",
            "CURRENT_SLICE_ONLY",
            "HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
