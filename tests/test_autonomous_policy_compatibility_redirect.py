from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REDIRECT = ROOT / "docs/AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING_POLICY.md"
CURRENT = ROOT / "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md"


class AutonomousPolicyCompatibilityRedirectTests(unittest.TestCase):
    def test_legacy_path_is_a_thin_redirect_to_current_owner(self) -> None:
        self.assertTrue(REDIRECT.exists())
        self.assertTrue(CURRENT.exists())
        text = REDIRECT.read_text(encoding="utf-8")
        for token in (
            "COMPATIBILITY_REDIRECT_ONLY",
            "NO_SECOND_POLICY_CANON",
            "CURRENT_OWNER_FRESH_READ_REQUIRED",
            "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md",
        ):
            self.assertIn(token, text)
        self.assertNotIn("## 1. Machine contract", text)
        self.assertLess(len(text.splitlines()), 40)


if __name__ == "__main__":
    unittest.main()
