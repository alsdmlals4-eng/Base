from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
PLANNING = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"
GRILL = ROOT / "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
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
        self.assertIn("CODEX_SINGLE_IMPLEMENTATION_WINDOW", text)
        self.assertIn("WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT", text)
        self.assertNotIn("## 1. Three-stage minimum-transition flow", text)

    def test_stage1_routes_collaborative_core_planning_to_existing_grill_owners(self) -> None:
        profile = self._text(PROFILE)
        for token in (
            "USER_COLLABORATIVE_CORE_PLANNING_REQUIRED",
            "GRILL_ME_FOR_MATERIAL_CORE_DECISIONS",
            "DECISION_RELEVANT_BENCHMARK_REQUIRED",
            "THREE_MATERIALLY_DISTINCT_APPROACHES",
            "ADOPT / ADAPT / REJECT",
        ):
            self.assertIn(token, profile)
        self.assertIn("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md", profile)
        self.assertIn("grill-me-protocol.md", profile)
        self.assertTrue(PLANNING.exists())
        self.assertTrue(GRILL.exists())
        self.assertIn("Grill Me", self._text(PLANNING))
        self.assertIn("Grill Me", self._text(GRILL))
        self.assertIn("이미 승인된", profile)
        self.assertIn("다시 묻지 않는다", profile)

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
        self.assertIn("WORK_PRODUCTION_INPUT_PACKET_READY", profile)
        self.assertIn("READY_FOR_SINGLE_CODEX_WINDOW", profile)

    def test_startup_receipt_keeps_project_stage_truth_local(self) -> None:
        startup = self._text(STARTUP)
        profile = self._text(PROFILE)
        self.assertIn("current_stage:", startup)
        self.assertIn("active_playable_slice:", startup)
        self.assertIn("PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON", profile)
        self.assertIn("COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON", profile)

    def test_automated_ready_is_not_validated_vertical_slice_complete(self) -> None:
        profile = self._text(PROFILE)
        skill = self._text(VERTICAL_SLICE_SKILL)
        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE", profile)
        self.assertIn("VERTICAL_SLICE_VALIDATED_COMPLETE", profile)
        self.assertIn("ACTUAL_USER_PLAY_REQUIRED", profile)
        self.assertIn("NEXT_SLICE_REQUIRES_STAGE5_DECISION", profile)
        self.assertIn("READY_FOR_USER_VERTICAL_SLICE_VALIDATION", profile)
        self.assertIn("PLAYER_EXPERIENCE_EVIDENCE", profile + "\n" + skill)

    def test_vertical_slice_skill_remains_human_play_and_decision_evidence_owner(self) -> None:
        skill = self._text(VERTICAL_SLICE_SKILL)
        profile = self._text(PROFILE)
        self.assertIn("실제 플레이 증거", skill)
        self.assertIn("### 4. Playtest evidence", skill)
        self.assertIn("## Definition of Done", skill)
        for decision in ("EXPAND", "REWORK", "REPEAT_SLICE", "HOLD", "STOP"):
            self.assertIn(decision, skill)
            self.assertIn(decision, profile)
        self.assertIn("VERTICAL_SLICE_VALIDATED_COMPLETE_REQUIRES_STAGE5", profile)

    def test_non_game_projects_are_explicit_exception(self) -> None:
        router = self._text(ROUTER)
        profile = self._text(PROFILE)
        self.assertIn("GAME_PROJECT_ONLY", router)
        self.assertIn("NON_GAME_PROJECT_NOT_APPLICABLE", router)
        self.assertIn("NON_GAME_PROJECT_NOT_APPLICABLE", profile)


if __name__ == "__main__":
    unittest.main()
