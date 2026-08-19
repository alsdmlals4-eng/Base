from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
AGENTS = ROOT / "AGENTS.md"


class FullAdversarialLoopSemanticsTests(unittest.TestCase):
    def authoritative_text(self) -> str:
        return POLICY.read_text(encoding="utf-8") + "\n" + OPERATING_MODEL.read_text(encoding="utf-8")

    def test_base_still_requires_minimum_five_full_loops(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", agents)
        self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", agents)

    def test_full_loop_is_not_a_review_lens(self) -> None:
        text = self.authoritative_text()
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("관점 하나", text)
        self.assertIn("최소 5", text)

    def test_each_counted_loop_repeats_the_complete_lifecycle(self) -> None:
        text = self.authoritative_text()
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
        text = self.authoritative_text()
        self.assertIn("Loop 1=scope", text)
        self.assertIn("Loop 2=UX", text)
        self.assertIn("Loop 3=CI", text)
        self.assertIn("계수하지 않는다", text)


if __name__ == "__main__":
    unittest.main()
