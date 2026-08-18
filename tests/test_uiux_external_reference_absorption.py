from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
SEEDS = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
AGENTS = ROOT / "AGENTS.md"
LONG_HORIZON = ROOT / "docs" / "LONG_HORIZON_WORK_EXECUTION_POLICY.md"
VISUAL_POLICY = ROOT / "docs" / "VISUAL_COLLABORATION_TOOL_POLICY.md"
DOCUMENTATION_MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
SHEET_POLICY = ROOT / "docs" / "PROJECT_GDD_GOOGLE_SHEETS_POLICY.md"
ART_SKILL = ROOT / "skills" / "designing-art-prompts-and-technique-cards" / "SKILL.md"
UI_SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
UI_METHOD = ROOT / "skills" / "auditing-and-refining-ui-art" / "references" / "ux-ui-design-system-method.md"
LEARNING_LOG = ROOT / "skills" / "auditing-and-refining-ui-art" / "LEARNING_LOG.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class UiUxExternalReferenceAbsorptionTests(unittest.TestCase):
    def test_notion_official_replaces_figma_sources_in_periodic_loop(self) -> None:
        watchlist = WATCHLIST.read_text(encoding="utf-8")
        seeds = SEEDS.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")

        for retired in (
            "Huddling Figmapedia",
            "https://huddling.ai/figma-info",
        ):
            self.assertNotIn(retired, watchlist)
        self.assertNotIn("figma-practical-design-workflow", seeds)
        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", agents)

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

    def test_figma_legacy_references_cannot_reactivate_default_routing(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        long_horizon = LONG_HORIZON.read_text(encoding="utf-8")
        visual_policy = VISUAL_POLICY.read_text(encoding="utf-8")

        for text in (agents, long_horizon, visual_policy):
            self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", text)
            self.assertIn("LEGACY_FIGMA_REFERENCE", text)

        self.assertNotIn("새 시각 작업의 기본 협업면은 프로젝트별 Figma", agents)
        self.assertNotIn("새 프로젝트·새 시각 기획의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다.", agents)
        self.assertNotIn("시각 협업은 프로젝트 Figma", agents)
        self.assertNotIn(
            "새 프로젝트와 새 기획 작업의 **시각 협업 기본 작업면**은 프로젝트별 Figma다.",
            long_horizon,
        )
        self.assertNotIn(
            "새 프로젝트와 새 시각 작업의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다.",
            visual_policy,
        )

    def test_active_owners_do_not_reintroduce_figma_after_top_level_retirement(self) -> None:
        documentation_map = DOCUMENTATION_MAP.read_text(encoding="utf-8")
        sheet_policy = SHEET_POLICY.read_text(encoding="utf-8")
        art_skill = ART_SKILL.read_text(encoding="utf-8")

        for text in (documentation_map, sheet_policy, art_skill):
            self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", text)
            self.assertIn("LEGACY_FIGMA_REFERENCE", text)

        self.assertNotIn("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json", documentation_map)
        self.assertNotIn("새 프로젝트와 새 시각 작업의 기본 협업면은 Figma", sheet_policy)
        self.assertNotIn("migration 뒤 책임 surface는 GitHub/Figma/repo-native", sheet_policy)
        self.assertIn("Legacy Figma-direct visual modules — inactive", art_skill)
        self.assertNotIn(
            "프로젝트가 Figma Visual Bible을 구성했거나 Visual Artifact Registry가 Figma Artifact를 가리키면 `references/figma-visual-bible-continuity-gate.md`를 적용한다.",
            art_skill,
        )
        self.assertNotIn("Mermaid·Figma 대체안을 쓴다", art_skill)

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

        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn('"id": "ui-ux-pro-max"', registry)
        self.assertNotIn('"id": "design-md"', registry)


if __name__ == "__main__":
    unittest.main()
