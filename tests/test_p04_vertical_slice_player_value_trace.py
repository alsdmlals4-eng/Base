from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class P04VerticalSlicePlayerValueTraceTests(unittest.TestCase):
    def test_vertical_slice_plan_consumes_required_player_value_trace(self) -> None:
        plan = (ROOT / "templates/planning/VERTICAL_SLICE_PLAN.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("P04_PLAYER_VALUE_TO_EVIDENCE_TRACE", plan)
        for term in (
            "player_promise",
            "meaningful_choice",
            "expected_experience",
            "research_question",
            "observable_signal",
            "evidence_ceiling",
            "slice_acceptance",
        ):
            self.assertIn(term, plan)


if __name__ == "__main__":
    unittest.main()
