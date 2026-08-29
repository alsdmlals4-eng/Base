from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsContractTests(unittest.TestCase):
    def test_policy_is_compatibility_only_and_routes_to_notion(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "COMPATIBILITY_ONLY",
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "MIGRATION_PENDING",
            "MIGRATED_READBACK_VERIFIED",
            "PROJECT_RELATION_REQUIRED",
            "ASSET_KNOWLEDGE_MASTER",
        ):
            self.assertIn(term, policy)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", policy)

    def test_policy_requires_unique_material_migration_not_bulk_copy(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "unique material",
            "classify unique / duplicate / obsolete",
            "Project identity",
            "read back",
        ):
            self.assertIn(term, policy)
        self.assertIn("Do not bulk-copy", policy)

    def test_legacy_tab_template_is_migration_inventory_not_new_install(self) -> None:
        template = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        for term in ("COMPATIBILITY_ONLY", "DO_NOT_INSTALL_NEW", "migration inventory"):
            self.assertIn(term, template)
        self.assertNotIn("새 Sheet에 설치하는 권장 핵심 tab", template)

    def test_visual_policy_uses_notion_project_boundary(self) -> None:
        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for term in (
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "PROJECT_RELATION_REQUIRED",
            "ASSET_KNOWLEDGE_MASTER",
            "VISUAL_MAP_DERIVED",
        ):
            self.assertIn(term, visual)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", visual)

    def test_image_generation_routes_through_visual_asset_coverage_without_second_canon(self) -> None:
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        coverage = read("docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md")

        for term in (
            "Visual Asset Coverage Preflight",
            "GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md",
            "NEED_DRIVEN_GENERATE_THEN_LOCK",
            "CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED",
            "NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS",
            "GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED",
        ):
            self.assertIn(term, policy)
        self.assertIn("GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md", skill)
        for term in (
            "COVERAGE_CHECK_ONLY",
            "NOT_A_SECOND_ASSET_CANON",
            "NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS",
            "STATE_FAMILY_COMPLETENESS",
            "PLATFORM_SPEC_RECHECK_REQUIRED",
        ):
            self.assertIn(term, coverage)
        self.assertIn("NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS", skill)

    def test_entrypoints_use_registry_derived_active_skill_view(self) -> None:
        for path in ("README.md", "AGENTS.md", "docs/OPERATING_MODEL.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("SKILL_REGISTRY.json", text, path)
            self.assertIn("BASE_ACTIVE_SKILLS.md", text, path)
            self.assertNotIn("전체 ACTIVE Skill은 27개", text, path)

    def test_frozen_v9_sheet_control_remains_historical(self) -> None:
        frozen = json.loads(read("docs/operations/SHEET_CONTROL_CONTRACT.json"))
        self.assertEqual(frozen["project_sheet_role"], "USER_FACING_GDD_WORKSPACE")
        self.assertNotIn("visual_workspace", frozen)


if __name__ == "__main__":
    unittest.main()
