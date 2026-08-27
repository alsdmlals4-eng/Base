from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"


class WorkFivePhaseThinInterfaceContractTests(unittest.TestCase):
    def test_five_phase_owner_stays_thin_and_blocks_next_slice(self) -> None:
        self.assertTrue(CONTRACT.exists(), f"required contract file missing: {CONTRACT}")
        text = CONTRACT.read_text(encoding="utf-8")

        self.assertLess(
            len(text.splitlines()),
            360,
            "five-phase owner must remain a thin lifecycle interface; detailed algorithms belong to current owners",
        )
        for token in (
            "THIN_PHASE_INTERFACE_NOT_SECOND_CANON",
            "DETAILED_ALGORITHMS_DELEGATED_TO_CURRENT_OWNERS",
            "NO_AUTOMATIC_NEXT_SLICE_BEFORE_USER_DECISION",
            "USER_VALIDATED_VERTICAL_SLICE",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
