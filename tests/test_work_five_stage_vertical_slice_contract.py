from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
AUDIT = ROOT / "docs/audits/2026-08-27-five-stage-work-project-canon-audit.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-27-five-stage-work-vertical-slice-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-27-five-stage-work-vertical-slice.md"
PROPOSAL = ROOT / "[수정제안서]/BCP-2026-040-work-five-stage-vertical-slice/PROPOSAL.md"


class WorkFiveStageVerticalSliceContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_current_entry_routes_the_five_stage_contract(self) -> None:
        starter = self._read(STARTER)
        router = self._read(ROUTER)
        for token in (
            "WORK_FIVE_STAGE_VERTICAL_SLICE_EXECUTION_CONTRACT.md",
            "FIVE_STAGE_WORK_VERTICAL_SLICE_LIFECYCLE",
        ):
            self.assertIn(token, starter)
            self.assertIn(token, router)

    def test_contract_has_exactly_five_named_stages_in_required_order(self) -> None:
        text = self._read(CONTRACT)
        ordered = (
            "STAGE_1_PLANNING",
            "STAGE_2_REVIEW",
            "STAGE_3_ASSET_AND_INPUT_PRODUCTION",
            "STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_VERIFICATION",
            "STAGE_5_USER_VALIDATION",
        )
        positions = [text.index(token) for token in ordered]
        self.assertEqual(positions, sorted(positions))
        stage_headings = re.findall(r"^## Stage [1-5] —", text, flags=re.MULTILINE)
        self.assertEqual(len(stage_headings), 5)
        self.assertIn("FIVE_STAGE_CONTRACT_SUPERSEDES_THREE_STAGE_LABELS_ONLY", text)
        self.assertIn("THREE_STAGE_PROFILE_REMAINS_DETAIL_OWNER", text)
        self.assertTrue(PROFILE.exists())

    def test_stage_one_is_collaborative_grill_me_and_benchmark_planning(self) -> None:
        text = self._read(CONTRACT)
        section = text.split("## Stage 1 —", 1)[1].split("## Stage 2 —", 1)[0]
        for token in (
            "CORE_PLANNING_GRILL_ME_AND_BENCHMARK_REQUIRED",
            "GRILL_ME_REQUIRED_FOR_CORE_PRODUCT_MEANING",
            "CORE_PLANNING_DECISIONS_EXCLUDED_FROM_ROUTINE_AUTO_APPROVAL",
            "USER_AND_GPT_CO_DESIGN_DECISION_PACKET",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "ADOPT / ADAPT / REJECT",
            "PLANNING_CONFIRMED_BY_USER",
        ):
            self.assertIn(token, section)
        self.assertIn("Grill Me", section)
        self.assertIn("benchmark", section.lower())

    def test_each_stage_has_distinct_output_and_exit_gate(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "STAGE_1_OUTPUT: USER_AND_GPT_CO_DESIGN_DECISION_PACKET",
            "STAGE_1_EXIT: PLANNING_CONFIRMED_BY_USER",
            "STAGE_2_OUTPUT: REVIEWED_SLICE_SPEC",
            "STAGE_2_EXIT: REVIEW_GATE_PASSED",
            "STAGE_3_OUTPUT: WORK_PRODUCTION_INPUT_PACKET",
            "STAGE_3_EXIT: READY_FOR_SINGLE_CODEX_WINDOW",
            "STAGE_4_OUTPUT: AUTOMATED_VERTICAL_SLICE_PACKAGE",
            "STAGE_4_EXIT: AUTOMATED_VERTICAL_SLICE_READY_FOR_USER_VALIDATION",
            "STAGE_5_OUTPUT: USER_VALIDATION_DECISION_PACKET",
            "STAGE_5_EXIT: USER_VALIDATED_VERTICAL_SLICE_COMPLETE",
        ):
            self.assertIn(token, text)

    def test_stage_boundaries_prevent_planning_review_assets_and_codex_from_collapsing(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "NO_FINAL_ASSET_PRODUCTION_IN_STAGE_1",
            "NO_CODEX_PRODUCT_IMPLEMENTATION_IN_STAGE_1",
            "NO_UNREVIEWED_SCOPE_EXPANSION_IN_STAGE_2",
            "NO_PRODUCT_CODE_IMPLEMENTATION_IN_STAGE_3",
            "NO_CORE_PLANNING_REINTERPRETATION_IN_STAGE_4",
            "NO_NEXT_SLICE_EXPANSION_IN_STAGE_5",
        ):
            self.assertIn(token, text)

    def test_vertical_slice_is_not_complete_at_machine_ready(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "STAGE_4_IS_NOT_VERTICAL_SLICE_COMPLETE",
            "VERTICAL_SLICE_COMPLETE_REQUIRES_STAGE_5",
            "AUTOMATED_VERTICAL_SLICE_READY_FOR_USER_VALIDATION",
            "USER_VALIDATED_VERTICAL_SLICE_COMPLETE",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
        ):
            self.assertIn(token, text)

    def test_vertical_slice_completion_requires_representative_end_to_end_quality(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "player promise",
            "meaningful choice",
            "observable result",
            "reward or failure learning",
            "core systems integrated",
            "production-candidate UI / image / audio / VFX",
            "actual runtime build",
            "downloadable artifact",
            "user actually played",
            "canonical reflection",
        ):
            self.assertIn(token, text)

    def test_user_findings_return_to_the_correct_stage(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "STAGE_5_TO_STAGE_1_FOR_CORE_DESIGN_FINDING",
            "STAGE_5_TO_STAGE_2_FOR_SPEC_OR_ACCEPTANCE_FINDING",
            "STAGE_5_TO_STAGE_3_FOR_ASSET_OR_FEEDBACK_FINDING",
            "STAGE_5_TO_STAGE_4_FOR_IMPLEMENTATION_OR_TUNING_FINDING",
            "NO_AUTOMATIC_NEXT_SLICE_BEFORE_USER_DECISION",
        ):
            self.assertIn(token, text)

    def test_existing_project_statuses_are_mapped_without_mass_renaming(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "FIVE_STAGE_PROJECT_STATE_MAPPING",
            "PLAN",
            "PLANNING_COMPLETE",
            "IMPLEMENTATION_READY",
            "AUTOMATED_VERTICAL_SLICE_READY",
            "USER_VALIDATION_PENDING",
            "NO_MASS_PROJECT_CANON_RENAME",
        ):
            self.assertIn(token, text)

    def test_project_canon_audit_is_real_and_separate_from_active_policy(self) -> None:
        audit = self._read(AUDIT)
        for project in (
            "OMENWARD",
            "Blacksmith",
            "GRIMOIRE",
            "Ninja Survival",
            "Urban Legend",
            "Switchy Express",
        ):
            self.assertIn(project, audit)
        for token in (
            "GitHub current canon",
            "Notion Home",
            "observed_at",
            "evidence ceiling",
            "POLICY_OWNER: NO",
        ):
            self.assertIn(token, audit)
        contract = self._read(CONTRACT)
        for project_specific in (
            "OMENWARD",
            "Blacksmith",
            "GRIMOIRE",
            "Ninja Survival",
            "Urban Legend",
            "Switchy Express",
        ):
            self.assertNotIn(project_specific, contract)

    def test_design_plan_and_proposal_exist(self) -> None:
        for path in (SPEC, PLAN, PROPOSAL):
            text = self._read(path)
            self.assertIn("five-stage", text.lower())
        proposal = self._read(PROPOSAL)
        self.assertIn("APPROVED_FOR_IMPLEMENTATION", proposal)
        self.assertIn("BCP-2026-040", proposal)


if __name__ == "__main__":
    unittest.main()
