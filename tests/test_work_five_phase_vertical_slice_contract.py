from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
CASE = ROOT / "docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md"
PLANNING = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"
GRILL = ROOT / "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
SLICE_SKILL = ROOT / "skills/designing-vertical-slices/SKILL.md"


class WorkFivePhaseVerticalSliceContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required five-phase file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_five_phase_owner_exists_and_orders_the_approved_flow(self) -> None:
        text = self._read(CONTRACT)
        phases = (
            "PHASE_1_PLANNING_CO_DESIGN",
            "PHASE_2_PREPRODUCTION_REVIEW",
            "PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "PHASE_5_USER_VERTICAL_SLICE_VALIDATION",
        )
        for phase in phases:
            self.assertIn(phase, text)
        self.assertEqual([text.index(p) for p in phases], sorted(text.index(p) for p in phases))
        self.assertIn("FIVE_PHASE_INTERFACE_OWNER", text)
        self.assertIn("PROJECT_NATIVE_STATE_NAMES_PRESERVED", text)

    def test_phase1_is_user_codesign_for_material_core_decisions(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "CORE_PLANNING_CO_DESIGN_REQUIRED",
            "DECISION_RELEVANT_BENCHMARK_REQUIRED",
            "THREE_MATERIALLY_DISTINCT_ALTERNATIVES_REQUIRED",
            "CORE_PLANNING_DECISION_PACKET",
            "PHASE_1_USER_CONFIRMED",
            "DELEGATED_ROUTINE_APPROVAL != CORE_PRODUCT_MEANING_APPROVAL",
        ):
            self.assertIn(token, text)
        self.assertIn("ADOPT / ADAPT / REJECT", text)
        self.assertIn("Grill Me", text)
        self.assertIn("이미 승인", text)
        self.assertTrue(PLANNING.exists())
        self.assertTrue(GRILL.exists())

    def test_phase2_is_preproduction_review_and_blocks_early_production(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "REVIEWED_SLICE_PRODUCTION_CONTRACT",
            "APPROVED_FOR_INGAME_ELEMENT_PRODUCTION",
            "NO_SERIAL_ASSET_PRODUCTION_BEFORE_PHASE_2_PASS",
            "NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_2_PASS",
        ):
            self.assertIn(token, text)
        self.assertLess(text.index("PHASE_2_PREPRODUCTION_REVIEW"), text.index("PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION"))

    def test_phase3_requires_actual_consumer_and_closes_work_input_packet(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "ACTUAL_CONSUMER_REQUIRED",
            "PROJECT_LOCAL_VISUAL_BINARY_FIRST",
            "WORK_PRODUCTION_INPUT_PACKET",
            "READY_FOR_SINGLE_CODEX_WINDOW",
        ):
            self.assertIn(token, text)
        self.assertIn("actual consumer가 없으면 production asset으로 만들지 않는다", text)

    def test_phase4_is_one_codex_window_plus_work_machine_closeout(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "WORK_FINAL_IMPLEMENTATION_REVIEW_IS_PHASE_4_CLOSEOUT",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "AUTOMATED_VERTICAL_SLICE_READY",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertIn("machine-executable required work = 0", text)

    def test_phase5_is_actual_user_play_and_is_not_phase4_readiness(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "ACTUAL_USER_PLAY_REQUIRED",
            "CANONICAL_REFLECTION_AFTER_PLAY_REQUIRED",
            "AUTOMATED_VERTICAL_SLICE_READY != USER_VALIDATED_VERTICAL_SLICE",
            "USER_VALIDATED_VERTICAL_SLICE_PASS",
            "USER_VALIDATED_WITH_FOLLOWUP",
            "REWORK_REQUIRED",
            "BLOCKED_USER_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertIn("HUMAN_USABILITY_EVIDENCE: NOT_RUN", text)
        self.assertIn("PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN", text)

    def test_vertical_slice_completion_is_representative_not_whole_game_done(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "REPRESENTATIVE_EXPERIENCE_REQUIRED",
            "SHIPPING_INTENT_SLICE_QUALITY_REQUIRED",
            "CRITICAL_PLAYER_FACING_PLACEHOLDER_FORBIDDEN",
            "WHOLE_GAME_COMPLETION_NOT_REQUIRED",
            "FINAL_ALL_PLATFORM_PASS_NOT_REQUIRED",
            "FINAL_STORE_RELEASE_PASS_NOT_REQUIRED",
        ):
            self.assertIn(token, text)
        self.assertTrue(SLICE_SKILL.exists())

    def test_router_and_starter_surface_the_new_owner_without_becoming_second_canons(self) -> None:
        router = self._read(ROUTER)
        starter = self._read(STARTER)
        owner = "WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"
        self.assertIn(owner, router)
        self.assertIn(owner, starter)
        self.assertIn("FIVE_PHASE_INTERFACE_FIRST", router)
        self.assertLess(len(router.splitlines()), 180)
        self.assertLess(len(starter.splitlines()), 90)

    def test_minimum_transition_profile_is_reused_for_details_not_macro_phase_ownership(self) -> None:
        router = self._read(ROUTER)
        profile = self._read(PROFILE)
        self.assertIn("Stage A/B/C 표현은 **5단계를 대체하는 macro flow가 아니라 내부 최소전환 grouping**", router)
        for token in (
            "WORK_PREP_COMPLETION_BEFORE_CODEX",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION",
            "CONSOLIDATED_RETURN_PACKET",
            "MACHINE_QA_FIRST",
        ):
            self.assertIn(token, profile)

    def test_project_native_states_are_mapped_not_renamed_and_non_game_is_adapted(self) -> None:
        text = self._read(CONTRACT) + "\n" + self._read(CASE)
        for token in (
            "FIVE_PHASE_PROJECT_MAPPING",
            "PROJECT_NATIVE_STATE_NAMES_PRESERVED",
            "NO_PROJECT_WIDE_STATE_RENAME",
            "DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE",
            "GODOT_EVIDENCE_NOT_APPLICABLE_FOR_NON_GAME",
        ):
            self.assertIn(token, text)
        self.assertIn("PLAN / BUILD / REVIEW", text)
        self.assertIn("Coc-Fiction", text)


if __name__ == "__main__":
    unittest.main()
