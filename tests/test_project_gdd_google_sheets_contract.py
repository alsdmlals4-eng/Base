from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsRetirementTests(unittest.TestCase):
    def test_current_policy_is_retired_migration_only(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        retirement = read("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md")
        for token in (
            "RETIRED_MIGRATION_ONLY",
            "GOOGLE_SHEETS_MIGRATE_THEN_REMOVE",
            "unique",
            "duplicate",
            "obsolete",
            "Project",
            "readback",
        ):
            self.assertIn(token, policy)
        self.assertIn("GOOGLE_SHEETS_MIGRATE_THEN_REMOVE", retirement)
        self.assertNotIn("USER_FACING_GDD_WORKSPACE", policy)
        self.assertNotIn("PROJECT_SHEET_CONFIGURED", policy)

    def test_active_planning_and_operating_policies_do_not_make_sheets_default(self) -> None:
        paths = (
            "AGENTS.md",
            "START_HERE.md",
            "docs/OPERATING_MODEL.md",
            "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
            "docs/GPT_FIRST_PROJECT_WORKFLOW.md",
            "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
        )
        for path in paths:
            text = read(path)
            self.assertNotIn("USER_FACING_GDD_WORKSPACE", text, path)
            self.assertNotIn("PROJECT_SHEET_CONFIGURED", text, path)

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

    def test_v2_adapter_keeps_only_legacy_migration_compatibility(self) -> None:
        template = json.loads(read("templates/project-operations/PROJECT_BASE_ADAPTER_V2.json"))
        self.assertEqual(
            template["gdd_sheet"]["role"],
            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
        )
        self.assertEqual(template["gdd_sheet"]["sync_status"], "NOT_CONFIGURED")
        self.assertNotEqual(template["gdd_sheet"]["role"], "USER_FACING_GDD_WORKSPACE")

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
        current_map = read("docs/DOCUMENTATION_MAP.md")
        self.assertIn("RETIRED_MIGRATION_ONLY", current_map)
        self.assertIn("historical", current_map.lower())


if __name__ == "__main__":
    unittest.main()