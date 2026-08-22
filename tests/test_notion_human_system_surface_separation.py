from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUMAN_HOME = ROOT / "docs" / "operations" / "HUMAN_HOME_SELF_CONTAINED_POLICY.md"
NOTION_CONTRACT = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
AUTHORITY = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
VISUAL_WORKFLOW = ROOT / "docs" / "knowledge" / "game-development" / "NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md"


class NotionHumanSystemSurfaceSeparationTests(unittest.TestCase):
    def test_project_registry_is_not_the_human_project_home(self) -> None:
        text = HUMAN_HOME.read_text(encoding="utf-8") + "\n" + NOTION_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_EXCLUDES_AI_SYSTEM_METADATA", text)
        self.assertIn("PROJECT_REGISTRY_IS_SYSTEM_MASTER_NOT_HUMAN_HOME", text)
        self.assertIn("HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW", text)
        for term in (
            "Codex Home",
            "Project Local Path",
            "Godot Port",
            "Repo Main SHA",
            "Record Key",
            "Revision",
            "Prompt",
            "AI Note",
            "Hash",
            "Implementation Path",
        ):
            self.assertIn(term, text)

    def test_workspace_authority_contract_routes_human_and_system_surfaces_separately(self) -> None:
        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        self.assertEqual(contract["project_registry_surface"], "AI_SYSTEM_ONLY")
        self.assertEqual(contract["human_home_surface"], "DEDICATED_HUMAN_PROJECT_HOME")
        self.assertEqual(contract["human_home_registry_boundary"], "PHYSICALLY_SEPARATE")
        self.assertEqual(
            contract["approved_visual_delivery"],
            "UPLOAD_ATTACH_READBACK_AND_APPROVED_RECORD_REQUIRED",
        )

    def test_approved_visual_requires_notion_delivery_and_readback(self) -> None:
        text = HUMAN_HOME.read_text(encoding="utf-8") + "\n" + VISUAL_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("APPROVED_VISUAL_NOTION_DELIVERY_REQUIRED", text)
        self.assertIn("APPROVAL_WITHOUT_NOTION_DELIVERY_IS_INCOMPLETE", text)
        self.assertIn("Visual Bible", text)
        self.assertIn("Asset", text)
        self.assertIn("readback", text.lower())


if __name__ == "__main__":
    unittest.main()
