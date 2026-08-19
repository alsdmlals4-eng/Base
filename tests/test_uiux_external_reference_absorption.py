from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
SEEDS = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
UI_SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
UI_METHOD = ROOT / "skills" / "auditing-and-refining-ui-art" / "references" / "ux-ui-design-system-method.md"
LEARNING_LOG = ROOT / "skills" / "auditing-and-refining-ui-art" / "LEARNING_LOG.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class UiUxExternalReferenceAbsorptionTests(unittest.TestCase):
    def test_notion_official_replaces_figma_sources_in_periodic_loop(self) -> None:
        watchlist = WATCHLIST.read_text(encoding="utf-8")
        seeds = SEEDS.read_text(encoding="utf-8")

        for retired in (
            "Huddling Figmapedia",
            "https://huddling.ai/figma-info",
        ):
            self.assertNotIn(retired, watchlist)
        self.assertNotIn("figma-practical-design-workflow", seeds)

        for required in (
            "Notion official Help / Releases / Developers",
            "AUTHORITY_TARGET",
            "Skills for Notion Agent",
            "Custom Agents",
            "Notion MCP",
        ):
            self.assertIn(required, watchlist)
        self.assertIn("notion-skills-work-structure", seeds)

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertFalse(any(row["source_id"] == "huddling-figmapedia" for row in ledger["sources"]))
        matches = [row for row in ledger["sources"] if row["source_id"] == "notion-official"]
        self.assertEqual(1, len(matches))
        source = matches[0]
        self.assertEqual(["AUTHORITY_TARGET"], source["roles"])
        self.assertEqual("weekly", source["recommended_cadence"])
        self.assertEqual("ACTIVE", source["status"])
        self.assertIn("Skills for Notion Agent", source["scan_surfaces"])

    def test_existing_ui_owner_absorbs_design_read_and_resilience_principles(self) -> None:
        skill = UI_SKILL.read_text(encoding="utf-8")
        method = UI_METHOD.read_text(encoding="utf-8")
        self.assertIn("ux-ui-design-system-method.md", skill)

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

    def test_external_sources_are_pinned_as_learning_inputs_without_new_active_skill(self) -> None:
        learning = LEARNING_LOG.read_text(encoding="utf-8")
        for required in (
            "nextlevelbuilder/ui-ux-pro-max-skill",
            "a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5",
            "google-labs-code/design.md",
            "9bf8eae67128b6cc55ad9bf86665767deb4c11cd",
            "ADAPT",
            "ALREADY_COVERED",
        ):
            self.assertIn(required, learning)
        self.assertNotIn("https://huddling.ai/figma-info", learning)

        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn('"id": "ui-ux-pro-max"', registry)
        self.assertNotIn('"id": "design-md"', registry)


if __name__ == "__main__":
    unittest.main()
