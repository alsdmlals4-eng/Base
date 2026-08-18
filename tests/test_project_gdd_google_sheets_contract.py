from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsContractTests(unittest.TestCase):
    def test_policy_defines_legacy_migration_authority_and_proposal_statuses(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
            "USER_FACING_GDD_WORKSPACE_COMPATIBILITY_ALIAS",
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
            "REPO_NATIVE_STRUCTURED_DATA",
            "PROPOSED_SHEET_CHANGE",
            "SHEET_GITHUB_CONFLICT",
            "BASE_EXCLUDED",
            "GitHub",
            "Google Sheets",
        ):
            self.assertIn(term, policy)
        self.assertNotIn("프로젝트 Google Sheets의 역할은 `USER_FACING_GDD_WORKSPACE`다.", policy)

    def test_policy_and_templates_cover_visual_living_quantified_gdd(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        workbook = read("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md")
        for term in ("Visual", "Decision ID", "Commit SHA", "PROPOSED_SHEET_CHANGE"):
            self.assertIn(term, policy)
        self.assertIn("05_GDD", tabs)
        self.assertIn("15_", tabs)
        self.assertIn("GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE", workbook)
        self.assertIn("MIGRATION_COMPATIBILITY_SURFACE", workbook)

    def test_entrypoints_use_registry_derived_active_skill_view(self) -> None:
        for path in ("README.md", "AGENTS.md", "docs/OPERATING_MODEL.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("SKILL_REGISTRY.json", text, path)
            self.assertIn("BASE_ACTIVE_SKILLS.md", text, path)
            self.assertNotIn("전체 ACTIVE Skill은 27개", text, path)
        summary = read("docs/generated/BASE_ACTIVE_SKILLS.md")
        self.assertIn("Current active Skill count", summary)

    def test_existing_foundation_skills_route_sheet_handling_to_the_central_policy(self) -> None:
        for path in (
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
        ):
            text = read(path)
            self.assertIn("PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", text, path)
            self.assertIn("PROPOSED_SHEET_CHANGE", text, path)

    def test_sync_and_planning_policies_route_sheet_semantics_to_the_central_policy(self) -> None:
        for path in (
            "docs/CONFIRMED_DECISION_SYNC_POLICY.md",
            "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md",
        ):
            text = read(path)
            self.assertIn("PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", text, path)
            self.assertIn("PROPOSED_SHEET_CHANGE", text, path)
        sync_policy = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for term in ("GITHUB_UPDATE_PENDING_SHEET", "SHEET_UPDATE_PENDING_GITHUB", "SHEET_GITHUB_CONFLICT"):
            self.assertIn(term, sync_policy)

    def test_visual_policy_uses_figma_first_and_sheet_compatibility_boundary(self) -> None:
        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for term in (
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
            "REPO_NATIVE_STRUCTURED_DATA",
            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
            "MIGRATION_COMPATIBILITY_SURFACE",
        ):
            self.assertIn(term, visual)
        self.assertNotIn("Google Sheets → USER_FACING_GDD_WORKSPACE summary and editable review surface", visual)

    def test_v2_adapter_defaults_new_projects_to_sheet_migration_compatibility(self) -> None:
        adapter = json.loads(read("templates/project-operations/PROJECT_BASE_ADAPTER_V2.json"))
        self.assertEqual(adapter["gdd_sheet"]["role"], "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE")
        self.assertEqual(adapter["gdd_sheet"]["workspace_status"], "MIGRATION_COMPATIBILITY_SURFACE")

    def test_v2_schema_accepts_current_and_legacy_sheet_roles_during_migration(self) -> None:
        schema = json.loads(read("schemas/project-base-adapter-v2.schema.json"))
        roles = schema["properties"]["gdd_sheet"]["properties"]["role"]["enum"]
        self.assertEqual(
            roles,
            ["GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE", "USER_FACING_GDD_WORKSPACE"],
        )

    def test_frozen_v9_sheet_control_remains_historical_and_unchanged_in_meaning(self) -> None:
        frozen = json.loads(read("docs/operations/SHEET_CONTROL_CONTRACT.json"))
        self.assertEqual(frozen["project_sheet_role"], "USER_FACING_GDD_WORKSPACE")
        self.assertNotIn("workspace_status", frozen)
        self.assertNotIn("visual_workspace", frozen)

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
