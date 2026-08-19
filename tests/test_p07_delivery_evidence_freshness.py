from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PC_ANDROID_GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)


class P07DeliveryEvidenceFreshnessTests(unittest.TestCase):
    def test_pc_android_base_contract_is_not_left_as_draft_after_merge(self) -> None:
        guide = PC_ANDROID_GUIDE.read_text(encoding="utf-8")
        self.assertIn("base_contract: ACTIVE_IN_MAIN", guide)
        self.assertNotIn("base_contract: PROPOSED_IN_DRAFT_PR", guide)


if __name__ == "__main__":
    unittest.main()
