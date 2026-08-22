from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "REUSABLE_MODULE_REGISTRY.md"
PILOT = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "P0_IMPLEMENTATION_PILOT.md"

IMPLEMENTED_IDS = (
    "RM-TOOL-001",
    "RM-SYS-001",
    "RM-SYS-003",
    "RM-VIS-001",
    "RM-VIS-002",
)


class ReusableModuleRegistryFreshnessTests(unittest.TestCase):
    def test_p0_reference_implementations_are_not_reported_as_unbuilt(self) -> None:
        registry = REGISTRY.read_text(encoding="utf-8")
        pilot = PILOT.read_text(encoding="utf-8")

        for module_id in IMPLEMENTED_IDS:
            with self.subTest(module_id=module_id):
                self.assertRegex(
                    pilot,
                    rf"\| `{re.escape(module_id)}(?: [^`]*)?`?[^\n]*BASE_REFERENCE_IMPLEMENTED",
                    f"{module_id} lacks direct Base implementation evidence in P0 pilot",
                )
                row = next(
                    (line for line in registry.splitlines() if f"`{module_id}`" in line and line.startswith("|")),
                    "",
                )
                self.assertTrue(row, f"{module_id} is missing from reusable module registry")
                self.assertIn("REFERENCE_IMPLEMENTATION_EXISTS", row)
                self.assertNotIn("IMPLEMENTATION_NOT_BUILT", row)


if __name__ == "__main__":
    unittest.main()
