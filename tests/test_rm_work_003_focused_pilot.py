from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/knowledge/game-development/reuse/HUMAN_FACING_ARTIFACT_SYNTHESIS.md"
REGISTRY = ROOT / "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md"
PILOT = ROOT / "docs/knowledge/game-development/reuse/RM_WORK_003_IMPLEMENTATION_PILOT.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def registry_row(text: str, module_id: str) -> str:
    for line in text.splitlines():
        if line.startswith("|") and f"`{module_id}`" in line:
            return line
    raise AssertionError(f"missing Registry row for {module_id}")


class RmWork003FocusedPilotTests(unittest.TestCase):
    def test_pilot_records_real_notion_consumer_and_fail_closed_evidence(self) -> None:
        text = read(PILOT)
        for marker in (
            "RM-WORK-003",
            "NOTION_ARTIFACT_CREATED_AND_READBACK",
            "SOURCE_FIDELITY_PASS",
            "OUTLINE_BEFORE_LAYOUT_PASS",
            "CLAIM_GAP_REVIEW_PASS",
            "PARENT_HUMAN_SURFACE_FRESHNESS_REPAIRED",
            "PROVIDER_DEPENDENCY: NONE",
            "HUMAN_EDIT_DELTA: NOT_RUN_USER_REVIEW_PENDING",
            "HUMAN_VISUAL_REVIEW: NOT_RUN_USER_REVIEW_PENDING",
            "VALIDATION_CEILING: FOCUSED_VERIFIED",
            "BASE_ACTIVE_METHOD_NOT_CLAIMED",
        ):
            self.assertIn(marker, text)

    def test_contract_and_registry_promote_only_to_focused_verified(self) -> None:
        contract = read(CONTRACT)
        registry = read(REGISTRY)
        self.assertIn("validation_state: `FOCUSED_VERIFIED`", contract)
        self.assertIn("HUMAN_EDIT_DELTA: NOT_RUN_USER_REVIEW_PENDING", contract)
        self.assertIn("HUMAN_VISUAL_REVIEW: NOT_RUN_USER_REVIEW_PENDING", contract)

        row = registry_row(registry, "RM-WORK-003")
        self.assertIn("FOCUSED_VERIFIED", row)
        self.assertNotIn("VALIDATION_NOT_RUN", row)
        self.assertNotIn("BASE_ACTIVE_METHOD", row)
        self.assertNotIn("PLAYER_OR_USER_VERIFIED", row)


if __name__ == "__main__":
    unittest.main()
