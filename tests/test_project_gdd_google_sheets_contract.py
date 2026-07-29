from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsContractTests(unittest.TestCase):
    def test_policy_defines_workspace_authority_and_proposal_statuses(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "SHEET_GITHUB_CONFLICT",
            "BASE_EXCLUDED",
            "GitHub",
            "Google Sheets",
        ):
            self.assertIn(term, policy)

    def test_policy_and_templates_cover_visual_living_quantified_gdd(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        workbook = read("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md")
        for term in ("Visual", "Decision ID", "Commit SHA", "PROPOSED_SHEET_CHANGE"):
            self.assertIn(term, policy)
        self.assertIn("05_GDD", tabs)
        self.assertIn("15_", tabs)
        self.assertIn("USER_FACING_GDD_WORKSPACE", workbook)

    def test_entrypoints_use_registry_derived_active_skill_view(self) -> None:
        for path in ("README.md", "AGENTS.md", "docs/OPERATING_MODEL.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("SKILL_REGISTRY.json", text, path)
            self.assertIn("BASE_ACTIVE_SKILLS.md", text, path)
            self.assertNotIn("전체 ACTIVE Skill은 27개", text, path)
        summary = read("docs/generated/BASE_ACTIVE_SKILLS.md")
        self.assertIn("Current active Skill count", summary)

    def test_existing_foundation_skills_consume_project_gdd_sheet(self) -> None:
        for path in (
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
        ):
            text = read(path)
            self.assertIn("PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", text, path)
            self.assertIn("PROPOSED_SHEET_CHANGE", text, path)
            self.assertIn("USER_FACING_GDD_WORKSPACE", text, path)

    def test_sync_policy_preserves_sheet_edits_as_proposals(self) -> None:
        sync_policy = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for term in (
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "GITHUB_UPDATE_PENDING_SHEET",
            "SHEET_UPDATE_PENDING_GITHUB",
            "SHEET_GITHUB_CONFLICT",
        ):
            self.assertIn(term, sync_policy)

    def test_planning_policy_routes_gdd_sheet_contract(self) -> None:
        planning = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in (
            "PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
        ):
            self.assertIn(term, planning)


if __name__ == "__main__":
    unittest.main()
