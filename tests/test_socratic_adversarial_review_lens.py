from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "SKILL.md"
REFERENCE = (
    ROOT
    / "skills"
    / "running-adversarial-review-and-refinement"
    / "references"
    / "socratic-questioning-lenses.md"
)


class SocraticAdversarialReviewLensTests(unittest.TestCase):
    def test_reference_defines_six_selective_evidence_first_lenses(self) -> None:
        self.assertTrue(REFERENCE.exists(), "Socratic review reference must exist")
        socratic = REFERENCE.read_text(encoding="utf-8")

        for term in (
            "Socratic Review Lens",
            "Clarification",
            "Assumptions",
            "Reasons / Evidence",
            "Viewpoints",
            "Implications / Consequences",
            "Meta-question",
            "관련된 Lens만",
            "가짜 Finding",
            "저장소·정본·실제 구현·도구",
            "사용자 질문은 마지막 수단",
            "BLOCKED_UNVERIFIED",
            "USER_DECISION_REQUIRED",
            "답이 달라지면 실제 결정도 달라지는가",
        ):
            self.assertIn(term, socratic)

        self.assertNotIn("skill_id: socratic-questioning", socratic)

    def test_skill_wires_socratic_lens_without_new_user_question_gate(self) -> None:
        adversarial = SKILL.read_text(encoding="utf-8")

        for term in (
            "Socratic Review Lens",
            "references/socratic-questioning-lenses.md",
            "저장소·정본·실제 구현·도구",
            "사용자에게 묻지 않는다",
            "attack",
            "validate-critique",
            "regression-recheck",
        ):
            self.assertIn(term, adversarial)

        self.assertIn("관련된 Lens만", adversarial)
        self.assertIn("가짜 Finding", adversarial)


if __name__ == "__main__":
    unittest.main()
