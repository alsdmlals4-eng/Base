from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
WORKFLOW = ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md"
PLANNING = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"
STARTUP = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
VERTICAL_SLICE_SKILL = ROOT / "skills/designing-vertical-slices/SKILL.md"


class WorkFiveStageVerticalSliceFlowContractTests(unittest.TestCase):
    def _text(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"required owner must exist: {path}")
        return path.read_text(encoding="utf-8")

    def test_router_exposes_five_macro_stages_in_order(self) -> None:
        text = self._text(ROUTER)
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
        self.assertIn("MACRO_STAGE_IS_NOT_WORK_MODE", text)
        self.assertIn("MINIMIZE_WORK_CODEX_TRANSITIONS", text)

    def test_minimum_transition_profile_means_one_codex_window_not_three_macro_stages(self) -> None:
        text = self._text(PROFILE)
        for stage in (
            "STAGE_1_PLANNING",
            "STAGE_2_PRE_PRODUCTION_REVIEW",
            "STAGE_3_ASSET_AND_ELEMENT_PRODUCTION",
            "STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE",
            "STAGE_5_USER_VALIDATION",
        ):
            self.assertIn(stage, text)
        self.assertIn("CODEX_SINGLE_IMPLEMENTATION_WINDOW", text)
        self.assertIn("WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT", text)
        self.assertNotIn("## 1. Three-stage minimum-transition flow", text)

    def test_stage1_requires_collaborative_core_planning_and_benchmarking(self) -> None:
        planning = self._text(PLANNING)
        workflow = self._text(WORKFLOW)
        for token in (
            "USER_COLLABORATIVE_CORE_PLANNING_REQUIRED",
            "GRILL_ME_FOR_MATERIAL_CORE_DECISIONS",
            "DECISION_RELEVANT_BENCHMARK_REQUIRED",
            "THREE_MATERIALLY_DISTINCT_APPROACHES",
            "ADOPT / ADAPT / REJECT",
        ):
            self.assertIn(token, planning + "\n" + workflow)
        self.assertIn("이미 승인된", planning)
        self.assertIn("다시", planning)

    def test_stage2_clean_gate_precedes_assets_and_codex(self) -> None:
        profile = self._text(PROFILE)
        self.assertIn("PRE_PRODUCTION_REVIEW_CLEAN", profile)
        self.assertIn("NO_ASSET_PRODUCTION_BEFORE_REVIEW_CLEAN", profile)
        self.assertIn("NO_CODEX_PRODUCT_MUTATION_BEFORE_REVIEW_CLEAN", profile)
        self.assertLess(profile.index("STAGE_2_PRE_PRODUCTION_REVIEW"), profile.index("STAGE_3_ASSET_AND_ELEMENT_PRODUCTION"))
        self.assertLess(profile.index("STAGE_3_ASSET_AND_ELEMENT_PRODUCTION"), profile.index("STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE"))

    def test_stage3_requires_actual_consumer_and_durable_input_packet(self) -> None:
        profile = self._text(PROFILE)
        self.assertIn("ACTUAL_CONSUMER_REQUIRED", profile)
        self.assertIn("WORK_PRODUCTION_INPUT_PACKET", profile)
        self.assertIn("READY_FOR_SINGLE_CODEX_WINDOW", profile)

    def test_startup_receipt_records_macro_stage_without_replacing_project_truth(self) -> None:
        text = self._text(STARTUP)
        self.assertIn("macro_stage:", text)
        self.assertIn("stage_gate_state:", text)
        self.assertIn("RESOLVE_FROM_CURRENT_PROJECT_CANON", text)

    def test_automated_ready_is_not_validated_vertical_slice_complete(self) -> None:
        combined = self._text(PROFILE) + "\n" + self._text(VERTICAL_SLICE_SKILL)
        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE", combined)
        self.assertIn("VERTICAL_SLICE_VALIDATED_COMPLETE", combined)
        self.assertIn("ACTUAL_USER_PLAY_REQUIRED", combined)
        self.assertIn("NEXT_SLICE_REQUIRES_STAGE5_DECISION", combined)
        self.assertIn("READY_FOR_USER_VERTICAL_SLICE_VALIDATION", combined)
        self.assertIn("PLAYER_EXPERIENCE_EVIDENCE", combined)

    def test_vertical_slice_skill_preserves_human_play_as_completion_evidence(self) -> None:
        text = self._text(VERTICAL_SLICE_SKILL)
        self.assertIn("VERTICAL_SLICE_VALIDATED_COMPLETE", text)
        self.assertIn("Stage 5", text)
        self.assertIn("EXPAND", text)
        self.assertIn("REWORK", text)
        self.assertIn("REPEAT_SLICE", text)
        self.assertIn("HOLD", text)
        self.assertIn("STOP", text)

    def test_non_game_projects_are_explicit_exception(self) -> None:
        router = self._text(ROUTER)
        self.assertIn("GAME_PROJECT_ONLY", router)
        self.assertIn("NON_GAME_PROJECT_NOT_APPLICABLE", router)


if __name__ == "__main__":
    unittest.main()
