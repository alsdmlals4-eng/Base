from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "SKILL.md"
PROTOCOL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "references" / "finding-and-regression-protocol.md"
AGENTS = ROOT / "AGENTS.md"


class FullAdversarialLoopSemanticsTests(unittest.TestCase):
    def test_full_loop_is_not_a_review_lens(self) -> None:
        for path in (SKILL, AGENTS):
            text = path.read_text(encoding="utf-8")
            self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
            self.assertIn("관점 하나", text)
            self.assertIn("최소 5회", text)

    def test_each_counted_loop_repeats_the_complete_lifecycle(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for term in (
            "CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK",
            "MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK",
            "FULL-SCOPE ATTACK",
            "VALIDATE CRITIQUE",
            "FIX / REFINE VERIFIED FINDINGS",
            "EXECUTION / REGRESSION / REFERENCE VERIFICATION",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "RE-ATTACK THE WHOLE RESULTING STATE",
        ):
            self.assertIn(term, text)

    def test_lens_split_examples_are_explicitly_rejected(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Loop 1=scope", text)
        self.assertIn("Loop 2=UX", text)
        self.assertIn("Loop 3=CI", text)
        self.assertIn("full loop로 계수하지 않는다", text)

    def test_loop_evidence_requires_full_scope_coverage(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "full_scope_coverage",
            "alternatives_rechecked",
            "verification_rechecked",
            "better_alternative_rechecked",
            "long_term_fit_rechecked",
            "whole_state_re_attacked",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
