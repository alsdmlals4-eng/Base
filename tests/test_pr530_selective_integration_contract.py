from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETIREMENT = ROOT / "docs" / "DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md"
PLANNING = ROOT / "docs" / "PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md"
WORKSPACE = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
DASHBOARD = ROOT / "skills" / "building-project-visual-dashboards" / "SKILL.md"
MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"


class Pr530SelectiveIntegrationContractTests(unittest.TestCase):
    def registry_rows(self) -> dict[str, dict]:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        return {row["skill_id"]: row for row in data["skills"]}

    def test_retirement_policy_targets_project_management_surfaces_not_qa_validation(self) -> None:
        text = RETIREMENT.read_text(encoding="utf-8")
        for term in (
            "DEPRECATED_PROJECT_SURFACE_ABSORB_THEN_REMOVE",
            "PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED",
            "EXTERNAL_HTML_WORKSPACE_RETIRED",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY",
            "QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED",
        ):
            self.assertIn(term, text)
        self.assertIn("QA Evidence Studio", text)
        self.assertIn("검증", text)
        self.assertNotIn("별도 QA Evidence Studio 앱을 기본 경로로 유지할 필요는 없지만", text)

    def test_planning_policy_uses_notion_and_repository_not_active_sheets(self) -> None:
        text = PLANNING.read_text(encoding="utf-8")
        for term in (
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN",
            "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM",
        ):
            self.assertIn(term, text)
        for stale in (
            "USER_FACING_GDD_WORKSPACE",
            "PROJECT_SHEET_CONFIGURED",
            "새 Sheet에 설치",
            "Sheet·GitHub 동기화",
        ):
            self.assertNotIn(stale, text)

    def test_workspace_contract_advances_without_duplicate_gpt_workflow_canon(self) -> None:
        data = json.loads(WORKSPACE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(data["schema_version"], 3)
        self.assertEqual("docs/GPT_CODEX_WORKFLOW_POLICY.md", data["workflow_policy"])
        self.assertEqual("GPT_FIRST_PLANNING_AND_REVIEW", data["planning_owner"])
        self.assertEqual("OPTIONAL_CODEX_EXECUTOR", data["codex_role"])
        self.assertEqual("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", data["human_home_policy"])
        self.assertEqual("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md", data["retirement_policy"])
        self.assertEqual("MIGRATION_ONLY_UNTIL_REMOVAL", data["google_sheets"])
        self.assertEqual("QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED", data["qa_evidence_studio"])

    def test_active_registry_removes_sheet_workspace_routing_and_html_dashboard(self) -> None:
        rows = self.registry_rows()
        for skill_id in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
        ):
            row_text = json.dumps(rows[skill_id], ensure_ascii=False)
            for stale in (
                "google-sheets-sync",
                "project-sheet-semantic-tabs",
                "project-gdd-sheet",
                "gdd-workspace",
                "proposed-sheet-change",
                "USER_FACING_GDD_WORKSPACE",
            ):
                self.assertNotIn(stale, row_text, f"{skill_id}: {stale}")
            self.assertIn("notion", row_text.lower())
            self.assertIn("migration", row_text.lower())

        dashboard = rows["building-project-visual-dashboards"]
        self.assertEqual("REMOVAL_CANDIDATE", dashboard["status"])

    def test_dashboard_skill_is_retired_compatibility_locator_and_not_active_part_skill(self) -> None:
        text = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn("RETIRED_COMPATIBILITY_ONLY", text)
        self.assertIn("Notion Project Home", text)
        self.assertIn("새 standalone HTML", text)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
        self.assertNotIn("building-project-visual-dashboards", p05["owned_skill_ids"])

    def test_qa_evidence_studio_files_remain_present(self) -> None:
        for relative in (
            "tools/qa-evidence-studio/README.md",
            "tools/qa-evidence-studio/src/qa_evidence_studio/service.py",
            "tools/qa-evidence-studio/tests/test_service.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
