from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
LONG_HORIZON = ROOT / "docs" / "LONG_HORIZON_WORK_EXECUTION_POLICY.md"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"


class FullAdversarialLoopSemanticsTests(unittest.TestCase):
    def authoritative_text(self) -> str:
        return "\n".join(
            path.read_text(encoding="utf-8")
            for path in (AGENTS, LONG_HORIZON, OPERATING_MODEL)
        )

    def test_full_loop_is_not_a_review_lens(self) -> None:
        text = self.authoritative_text()
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("관점 하나", text)
        self.assertIn("최소 5회", text)

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
        self.assertIn("full loop", text)
        self.assertIn("계수", text)

    def test_p03_active_workstream_is_not_required_for_governance_contract(self) -> None:
        # The current governance PR must be able to establish the global rule
        # without rewriting the still-open P03 implementation workstream.
        agents = AGENTS.read_text(encoding="utf-8")
        long_horizon = LONG_HORIZON.read_text(encoding="utf-8")
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", agents)
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", long_horizon)


if __name__ == "__main__":
    unittest.main()
