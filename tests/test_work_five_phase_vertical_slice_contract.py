from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md"


class WorkFivePhaseVerticalSliceContractTests(unittest.TestCase):
    def test_five_phase_owner_exists_and_orders_the_approved_flow(self) -> None:
        self.assertTrue(CONTRACT.exists(), "approved five-phase owner must exist")
        text = CONTRACT.read_text(encoding="utf-8")
        phases = (
            "PHASE_1_PLANNING_CO_DESIGN",
            "PHASE_2_PREPRODUCTION_REVIEW",
            "PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION",
            "PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "PHASE_5_USER_VERTICAL_SLICE_VALIDATION",
        )
        for phase in phases:
            self.assertIn(phase, text)
        self.assertEqual([text.index(p) for p in phases], sorted(text.index(p) for p in phases))


if __name__ == "__main__":
    unittest.main()
