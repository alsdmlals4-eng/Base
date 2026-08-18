from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
UI_SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
UI_METHOD = ROOT / "skills" / "auditing-and-refining-ui-art" / "references" / "ux-ui-design-system-method.md"
LEARNING_LOG = ROOT / "skills" / "SKILL_LEARNING_LOG.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class UiUxExternalReferenceAbsorptionTests(unittest.TestCase):
    def test_huddling_figmapedia_is_a_weekly_discovery_source(self) -> None:
        watchlist = WATCHLIST.read_text(encoding="utf-8")
        for required in (
            "Huddling Figmapedia",
            "https://huddling.ai/figma-info",
            "DISCOVERY_FEED",
            "Figma 공식",
            "original source",
        ):
            self.assertIn(required, watchlist)

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        matches = [row for row in ledger["sources"] if row["source_id"] == "huddling-figmapedia"]
        self.assertEqual(1, len(matches))
        source = matches[0]
        self.assertEqual(["DISCOVERY_FEED"], source["roles"])
        self.assertEqual("weekly", source["recommended_cadence"])
        self.assertEqual("ACTIVE", source["status"])
        self.assertIn("figma-info", source["scan_surfaces"])

    def test_existing_ui_owner_absorbs_design_read_and_resilience_principles(self) -> None:
        skill = UI_SKILL.read_text(encoding="utf-8")
        method = UI_METHOD.read_text(encoding="utf-8")

        for required in (
            "design intent",
            "specific reference",
            "visual variance",
            "motion intensity",
            "information density",
            "essential text",
            "semantic state",
        ):
            self.assertIn(required, method.lower())

        for required in (
            "design intent",
            "visual variance",
            "information density",
            "essential text",
        ):
            self.assertIn(required, skill.lower())

    def test_external_sources_are_pinned_as_learning_inputs_without_new_active_skill(self) -> None:
        learning = LEARNING_LOG.read_text(encoding="utf-8")
        for required in (
            "nextlevelbuilder/ui-ux-pro-max-skill",
            "a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5",
            "google-labs-code/design.md",
            "9bf8eae67128b6cc55ad9bf86665767deb4c11cd",
            "https://huddling.ai/figma-info",
            "ADAPT",
            "ALREADY_COVERED",
        ):
            self.assertIn(required, learning)

        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn('"id": "ui-ux-pro-max"', registry)
        self.assertNotIn('"id": "design-md"', registry)


if __name__ == "__main__":
    unittest.main()
