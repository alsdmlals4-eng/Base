from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE = ROOT / "templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md"
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
GRILL = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"


class WorkFiveStageVerticalSliceLifecycleContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_five_stages_are_explicit_and_ordered(self) -> None:
        text = self._read(LIFECYCLE)
        stages = (
            "STAGE_1_PLANNING_WITH_USER",
            "STAGE_2_PREPRODUCTION_REVIEW",
            "STAGE_3_GAME_INPUT_PRODUCTION",
            "STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "STAGE_5_USER_VERTICAL_SLICE_VALIDATION",
        )
        positions = [text.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))

    def test_stage_one_requires_user_grill_me_and_benchmark_for_core_decisions(self) -> None:
        text = self._read(LIFECYCLE) + "\n" + self._read(GRILL)
        for token in (
            "CORE_PRODUCT_DECISIONS_REQUIRE_GRILL_ME_WHEN_UNRESOLVED",
            "ROUTINE_APPROVAL_DOES_NOT_AUTO_APPROVE_CORE_PLANNING",
            "BENCHMARK_BEFORE_MATERIAL_GRILL_ME",
            "player_promise",
            "pointed_fun",
            "meaningful_choice_and_tradeoff",
            "differentiation_and_sales_points",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
        ):
            self.assertIn(token, text)

    def test_review_is_separate_from_asset_production_and_codex(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "REVIEW_IS_NOT_ASSET_PRODUCTION",
            "REVIEW_IS_NOT_CODEX_IMPLEMENTATION",
            "STAGE_2_PREPRODUCTION_REVIEW_PACKET",
            "p0_blockers",
            "p1_blockers",
            "REOPEN_STAGE_1",
        ):
            self.assertIn(token, text)

    def test_stage_three_closes_all_work_owned_inputs_before_codex(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "WORK_PRODUCTION_INPUT_PACKET",
            "READY_FOR_SINGLE_CODEX_WINDOW",
            "blocking_missing_inputs",
            "actual_consumers",
            "provenance_rights_manifest",
        ):
            self.assertIn(token, text)

    def test_automated_ready_is_not_vertical_slice_complete(self) -> None:
        text = self._read(LIFECYCLE)
        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_COMPLETE", text)
        self.assertIn("VERTICAL_SLICE_COMPLETE_REQUIRES_USER_VALIDATION", text)
        self.assertIn("USER_VALIDATED_VERTICAL_SLICE", text)
        self.assertIn("NO_NEXT_SLICE_BEFORE_USER_DECISION_GATE", text)

    def test_stage_four_contains_codex_machine_qa_work_review_build_and_merge(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "WORK_FINAL_EVIDENCE_REVIEW_INSIDE_STAGE_4",
            "runtime_and_screen_evidence",
            "build_export_package_evidence",
            "exact_ci_and_merge",
            "downloadable_build_locator",
        ):
            self.assertIn(token, text)

    def test_stage_five_routes_findings_back_to_the_correct_stage(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "fun/core/choice failure → Stage 1",
            "comprehension/spec failure → Stage 2",
            "Visual/Audio/input failure → Stage 3",
            "implementation defect → Stage 4",
        ):
            self.assertIn(token, text)

    def test_current_entrypoints_route_the_five_stage_owner(self) -> None:
        for path in (ROUTER, STARTER):
            self.assertIn("WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md", self._read(path))
        router = self._read(ROUTER)
        self.assertIn("WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md", router)
        self.assertIn("FIVE_STAGE_LIFECYCLE_IS_PUBLIC_WORK_SEQUENCE", router)
        self.assertIn("EXISTING_WORK_MODES_AND_PROFILES_ARE_INTERNAL_OWNER_MAPPING", router)

    def test_non_game_exception_and_evidence_ceiling_are_preserved(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "GAME_PRODUCT_FIVE_STAGE_LIFECYCLE_ONLY",
            "NON_GAME_PROJECT_REQUIRES_PROJECT_SPECIFIC_ADAPTER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
        ):
            self.assertIn(token, text)

    def test_five_stage_owner_preserves_existing_automation_boundaries(self) -> None:
        combined = "\n".join((self._read(LIFECYCLE), self._read(PROFILE), self._read(STARTER)))
        for token in (
            "PROJECT_LOCAL_VISUAL_BINARY_FIRST",
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "AUTO_LAUNCH_GODOT_WHEN_CALLABLE",
            "MACHINE_QA_FIRST",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "STALL_SIGNAL_ROUTE_SWITCH",
            "SCOPE_BOUNDED_REQUIRED_WORK_ZERO",
            "IMPLEMENTATION_REALITY_GATE",
        ):
            self.assertIn(token, combined)

    def test_starter_is_a_thin_copy_paste_entry(self) -> None:
        starter = self._read(STARTER)
        self.assertLess(len(starter.splitlines()), 90)
        for token in (
            "1. STAGE_1_PLANNING_WITH_USER",
            "2. STAGE_2_PREPRODUCTION_REVIEW",
            "3. STAGE_3_GAME_INPUT_PRODUCTION",
            "4. STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "5. STAGE_5_USER_VERTICAL_SLICE_VALIDATION",
            "ROUTINE_APPROVAL_DOES_NOT_AUTO_APPROVE_CORE_PLANNING",
            "AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_COMPLETE",
        ):
            self.assertIn(token, starter)


if __name__ == "__main__":
    unittest.main()
