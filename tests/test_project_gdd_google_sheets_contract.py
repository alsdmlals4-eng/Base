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

    def test_gdd_information_architecture_has_single_current_decision_register_and_grouped_domains(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        workbook = read("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        for term in (
            "단일 현재 결정 원장",
            "02_현재_확정결정",
            "Decision ID 참조",
            "중복 금지",
            "경험",
            "시스템·콘텐츠",
            "세계·서사",
            "표현",
            "제작·검증",
        ):
            self.assertIn(term, policy)
        self.assertIn("결정 원장", workbook)
        self.assertIn("GDD 읽기 순서", workbook)
        self.assertIn("10_경험", tabs)
        self.assertIn("20_시스템_콘텐츠", tabs)
        self.assertIn("30_세계_서사", tabs)
        self.assertIn("40_표현", tabs)
        self.assertIn("50_제작_검증", tabs)

    def test_gdd_visual_index_keeps_external_artifacts_linked_not_copied(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        workbook = read("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        for text in (policy, workbook, tabs):
            self.assertIn("06_시각_작업면", text)
            self.assertIn("Artifact ID", text)
            self.assertIn("GDD|EXTERNAL_COLLABORATION|BOTH", text)
        self.assertIn("복사하지 않는다", workbook)
        self.assertIn("Decision ID", tabs)


if __name__ == "__main__":
    unittest.main()
