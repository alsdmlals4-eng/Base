from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "docs/AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING_POLICY.md"
CURRENT = ROOT / "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md"


class AutonomousPolicyCompatibilityRouterTests(unittest.TestCase):
    def test_legacy_path_is_a_thin_non_authoritative_router(self) -> None:
        self.assertTrue(ROUTER.exists())
        self.assertTrue(CURRENT.exists())

        text = ROUTER.read_text(encoding="utf-8")
        for token in (
            "SUPERSEDED_COMPATIBILITY_ROUTER",
            "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md",
            "NOT_A_SECOND_POLICY_OWNER",
            "NO_PROJECT_SHOULD_PIN_THIS_LEGACY_NAME_FOR_NEW_WORK",
            "CURRENT_OWNER_READBACK_REQUIRED",
        ):
            self.assertIn(token, text)

        self.assertNotIn("## 1. Machine contract", text)
        self.assertNotIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT", text)
        self.assertLess(len(text.splitlines()), 40)


if __name__ == "__main__":
    unittest.main()
