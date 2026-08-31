from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
START_CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
MINIMUM_PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
LOCAL_VISUAL = ROOT / "templates/project-operations/WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md"
EVIDENCE_OWNER = ROOT / "templates/project-operations/WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md"
GRILL_POLICY = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"
GRILL_PROTOCOL = ROOT / "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
VERTICAL_SLICE_SKILL = ROOT / "skills/designing-vertical-slices/SKILL.md"
CASE = ROOT / "docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md"


class WorkFivePhaseVerticalSliceContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_exact_five_phase_names_and_order_are_explicit(self) -> None:
        text = self._read(CONTRACT)
        phase_tokens = (
            "PHASE_1_PLANNING_CO_DESIGN",
            "PHASE_2_PREPRODUCTION_REVIEW",
            "PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "PHASE_5_USER_VERTICAL_SLICE_VALIDATION",
        )
        positions = [text.index(token) for token in phase_tokens]
        self.assertEqual(positions, sorted(positions), "five phases must appear in approved order")
        self.assertIn("FIVE_PHASE_VERTICAL_SLICE_EXECUTION", text)
        self.assertIn("FIVE_PHASE_TRANSITION_GATE_REQUIRED", text)

    def test_phase_one_co_designs_core_product_meaning_with_user(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "CORE_PLANNING_CO_DESIGN_REQUIRED",
            "GRILL_ME_FOR_UNRESOLVED_CORE_PRODUCT_MEANING",
            "DELEGATED_ROUTINE_APPROVAL_IS_NOT_CORE_PRODUCT_MEANING_APPROVAL",
            "CORE_PLANNING_DECISION_PACKET",
            "PHASE_1_USER_CONFIRMED",
            "project_goal:",
            "player_promise:",
            "pointed_fun:",
            "core_loop:",
            "session_loop:",
            "progression_or_meta_loop:",
            "core_systems:",
            "meaningful_choices:",
            "reward_and_failure_learning:",
            "emotional_target:",
            "first_session_memory:",
            "differentiation_and_sales_points:",
            "vertical_slice_hypotheses:",
        ):
            self.assertIn(token, text)

        for current_owner in (START_CHECKLIST, GRILL_POLICY, GRILL_PROTOCOL):
            self.assertTrue(current_owner.exists(), f"current planning owner must remain: {current_owner}")

    def test_phase_one_requires_benchmark_reuse_and_real_alternatives(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "REUSE_FIRST_PREFLIGHT_REQUIRED",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "ADOPT / ADAPT / REJECT",
            "EXISTING_CONFIRMED_DECISION_REUSE_NO_REASK",
            "facts / player reports / inference",
        ):
            self.assertIn(token, text)

    def test_phase_two_is_preproduction_review_before_assets_or_codex(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "PHASE_2_PREPRODUCTION_REVIEW",
            "REVIEWED_SLICE_PRODUCTION_CONTRACT",
            "APPROVED_FOR_INGAME_ELEMENT_PRODUCTION",
            "NO_SERIAL_ELEMENT_PRODUCTION_BEFORE_PHASE_2_PASS",
            "NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_3_READY",
            "CORE_MEANING_FINDING_REOPENS_PHASE_1",
            "implementation_feasibility",
            "actual_consumer_and_asset_coverage",
            "acceptance_test_runtime_and_rollback",
            "work_codex_transition_cost",
            "BLUEPRINT_EFFICIENCY_REUSE_ADAPT_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_phase_three_finishes_work_owned_product_inputs(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "WORK_PRODUCTION_INPUT_PACKET",
            "READY_FOR_SINGLE_CODEX_WINDOW",
            "Visual",
            "Audio",
            "UI/UX",
            "Data",
            "VFX",
            "localization_accessibility",
            "provenance_and_rights",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "project-owned tracked asset",
            "ASSET_MANIFEST",
            "remote HEAD readback",
        ):
            self.assertIn(token, text)
        self.assertTrue(LOCAL_VISUAL.exists())

    def test_phase_four_owns_codex_machine_closeout_and_work_final_review(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "actual code / Scene / Resource / runtime wiring",
            "deterministic / import / parse / runtime / build QA",
            "GUT / Hera / evidence-equivalent machine QA",
            "WORK_FINAL_IMPLEMENTATION_EVIDENCE_REVIEW",
            "exact-head CI",
            "safe merge",
            "post-merge readback",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "AUTOMATED_VERTICAL_SLICE_READY",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertTrue(MINIMUM_PROFILE.exists())
        self.assertTrue(EVIDENCE_OWNER.exists())

    def test_phase_four_is_not_final_vertical_slice_completion(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "AUTOMATED_VERTICAL_SLICE_READY != USER_VALIDATED_VERTICAL_SLICE",
            "AUTOMATED_VERTICAL_SLICE_READY_IS_PHASE_4_ONLY",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "NO_CRITICAL_PLAYER_FACING_PLACEHOLDER",
            "WHOLE_GAME_COMPLETE: false",
            "RELEASE_READY: false",
        ):
            self.assertIn(token, text)

    def test_phase_five_requires_actual_user_play_and_explicit_outcome(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "PHASE_5_USER_VERTICAL_SLICE_VALIDATION",
            "USER_ACTUALLY_PLAYS_EXACT_BUILD",
            "USER_VERTICAL_SLICE_VALIDATION_PACKET",
            "representative action → choice → result → feedback",
            "USER_VALIDATED_VERTICAL_SLICE_PASS",
            "USER_VALIDATED_WITH_FOLLOWUP",
            "REWORK_REQUIRED",
            "BLOCKED_USER_VALIDATION",
            "USER_VALIDATED_VERTICAL_SLICE",
            "CANONICAL_REFLECTION_AFTER_PLAY",
        ):
            self.assertIn(token, text)
        self.assertTrue(VERTICAL_SLICE_SKILL.exists())

    def test_machine_primary_policy_limits_human_review_to_declared_final_candidate(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "PROJECT_DECLARED_FINAL_USER_REVIEW_ONCE",
            "USER_DECLARED_EXACT_CANDIDATE_ONLY",
            "MACHINE_EVIDENCE_DOES_NOT_BECOME_HUMAN_EVIDENCE",
        ):
            self.assertIn(token, text)

    def test_user_feedback_reopens_earliest_affected_phase(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "BOUNDED_PHASE_REOPEN_FROM_USER_EVIDENCE",
            "core meaning / promise / core system → PHASE_1_PLANNING_CO_DESIGN",
            "design / readability / flow / balance intent → PHASE_2_PREPRODUCTION_REVIEW",
            "missing or unsuitable Visual / Audio / UI copy / data input → PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "bug / wiring / runtime / build / performance → PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
        ):
            self.assertIn(token, text)

    def test_project_native_states_are_mapped_not_mass_renamed(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "FIVE_PHASE_PROJECT_MAPPING",
            "PROJECT_PHASE_DRIFT_CORRECTION_REQUIRED",
            "PROJECT_NATIVE_STATE_PRESERVED",
            "NO_PROJECT_STATE_MASS_RENAME_OR_NOTION_REMIGRATION",
            "project_native_state:",
            "phase_1_planning:",
            "phase_2_review:",
            "phase_3_element_production:",
            "phase_4_implementation:",
            "phase_5_user_validation:",
            "mapping_evidence:",
            "ambiguity_or_drift:",
        ):
            self.assertIn(token, text)

    def test_non_game_projects_adapt_without_forcing_godot(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE",
            "NON_GAME_PROJECT_GODOT_EVIDENCE_NOT_APPLICABLE",
            "domain production",
            "NOT_APPLICABLE",
        ):
            self.assertIn(token, text)

    def test_router_and_copy_paste_starter_load_five_phase_owner(self) -> None:
        contract_name = "WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"
        router = self._read(ROUTER)
        starter = self._read(STARTER)
        self.assertIn(contract_name, router)
        self.assertIn(contract_name, starter)
        for token in (
            "PHASE_1_PLANNING_CO_DESIGN",
            "PHASE_2_PREPRODUCTION_REVIEW",
            "PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "PHASE_5_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, starter)
        self.assertIn(CASE.name, CONTRACT.read_text(encoding="utf-8") if CONTRACT.exists() else "")

    def test_current_detailed_owners_remain_composed_not_replaced(self) -> None:
        text = self._read(CONTRACT)
        for owner in (
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md",
            "grill-me-protocol.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md",
            "skills/designing-vertical-slices/SKILL.md",
        ):
            self.assertIn(owner, text)

    def test_active_generic_policy_excludes_project_specific_values(self) -> None:
        combined = self._read(CONTRACT) + "\n" + self._read(ROUTER) + "\n" + self._read(STARTER)
        for project_specific in (
            "Task9",
            "SX-DEC-060",
            "Cheonsul",
            "HANDPAINTED_STORYBOOK_3D_DIORAMA",
            "PR #19",
            "960×540",
        ):
            self.assertNotIn(project_specific, combined)


if __name__ == "__main__":
    unittest.main()
