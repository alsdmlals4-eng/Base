from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"missing Base owner: {relative_path}")
    return path.read_text(encoding="utf-8")


class MachinePrimaryFinalUserReviewPolicyTests(unittest.TestCase):
    def test_research_governance_allows_a_project_declared_machine_primary_policy(self) -> None:
        skill = read("skills/governing-game-user-research-coverage/SKILL.md")
        for required in (
            "PROJECT_DECLARED_VALIDATION_POLICY",
            "MACHINE_PRIMARY_FINAL_USER_REVIEW",
            "FIVE_PERSON_COMPREHENSION_NOT_BASE_DEFAULT",
            "PLAYER_EXPERIENCE_STUDY_NOT_BASE_DEFAULT",
            "FINAL_USER_REVIEW",
        ):
            self.assertIn(required, skill)

    def test_evidence_guide_keeps_layers_separate_without_making_human_study_universal(self) -> None:
        guide = read("docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md")
        for required in (
            "EVIDENCE_LAYER_IS_NOT_A_UNIVERSAL_RELEASE_GATE",
            "MACHINE_PRIMARY_FINAL_USER_REVIEW",
            "PROJECT_DECLARED_VALIDATION_POLICY",
            "Machine evidence never becomes human evidence",
        ):
            self.assertIn(required, guide)

    def test_work_five_phase_contract_supports_machine_acceptance_then_final_user_review(self) -> None:
        contract = read("templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md")
        router = read("templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md")
        combined = contract + "\n" + router
        for required in (
            "VALIDATION_POLICY_PROJECT_DECLARED",
            "MACHINE_PRIMARY_FINAL_USER_REVIEW",
            "MACHINE_PRIMARY_ACCEPTANCE_READY",
            "FINAL_USER_REVIEW_ONLY",
            "FIVE_PERSON_COMPREHENSION_NOT_BASE_DEFAULT",
            "PLAYER_EXPERIENCE_STUDY_NOT_BASE_DEFAULT",
        ):
            self.assertIn(required, combined)

        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != USER_VALIDATED_VERTICAL_SLICE", contract)
        self.assertIn("PHASE_5_USER_VERTICAL_SLICE_VALIDATION", contract)


if __name__ == "__main__":
    unittest.main()
