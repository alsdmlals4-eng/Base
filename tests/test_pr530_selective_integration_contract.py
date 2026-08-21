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
SHEET_CONTROL = ROOT / "docs" / "operations" / "SHEET_CONTROL_CONTRACT.json"
DECISIONS = ROOT / "docs" / "operations" / "BASE_V9_DECISION_REGISTRY.json"
GENERATOR = ROOT / "tools" / "build_base_v9_artifacts.py"
FRESHNESS_CONFIG = ROOT / ".github" / "reference-freshness.json"
ROUTING_TEST = ROOT / "tests" / "test_skill_routing_governance.py"
BASE_RULES_VERSION = ROOT / "docs" / "BASE_RULES_VERSION.md"


class Pr530SelectiveIntegrationContractTests(unittest.TestCase):
    def registry_rows(self) -> dict[str, dict]:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        return {row["skill_id"]: row for row in data["skills"]}

    def test_retirement_policy_retires_qa_studio_from_active_validation_routing(self) -> None:
        text = RETIREMENT.read_text(encoding="utf-8")
        for term in (
            "DEPRECATED_PROJECT_SURFACE_ABSORB_THEN_REMOVE",
            "PROJECT_MANAGEMENT_LOCAL_SURFACE_RETIRED",
            "EXTERNAL_HTML_WORKSPACE_RETIRED",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY",
            "QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW",
            "REPOSITORY_NATIVE_EVIDENCE_CAPTURE",
        ):
            self.assertIn(term, text)
        self.assertIn("QA Evidence Studio", text)
        self.assertIn("검증", text)
        self.assertNotIn("QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED", text)
        self.assertNotIn("별도 QA Evidence Studio 앱을 기본 경로로 유지할 필요는 없지만", text)

    def test_planning_policy_uses_notion_and_repository_not_active_sheets(self) -> None:
        text = PLANNING.read_text(encoding="utf-8")
        for term in (
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
            "docs/knowledge/game-development/README.md",
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        ):
            self.assertIn(term, text)
        for stale in (
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
        self.assertEqual("QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW", data["qa_evidence_studio"])
        self.assertTrue(any(
            "REPOSITORY_NATIVE_EVIDENCE_CAPTURE" in invariant
            for invariant in data["invariants"]
        ))

    def test_active_registry_removes_sheet_workspace_routing_and_preserves_decision_checkpoints(self) -> None:
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

        design = rows["managing-design-documents"]
        self.assertIn("하위 시스템 checkpoint", design["use_when"][0])

        dashboard = rows["building-project-visual-dashboards"]
        self.assertEqual("ACTIVE", dashboard["status"])
        self.assertTrue(any("notion" in text.lower() for text in dashboard["use_when"]))
        self.assertFalse(any("standalone HTML" in text for text in dashboard["use_when"]))
        self.assertNotIn("html-dashboard", dashboard["trigger_tags"])
        self.assertNotIn("standalone-dashboard", dashboard["trigger_tags"])
        self.assertIn("standalone HTML", " ".join(dashboard["do_not_use_when"] + dashboard["review_triggers"]))

    def test_dashboard_skill_is_notion_home_visual_map_owner_not_html_builder(self) -> None:
        text = DASHBOARD.read_text(encoding="utf-8")
        for token in (
            "NOTION_PROJECT_HOME_AND_VISUAL_MAP",
            "Notion Project Home",
            "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN",
            "dashboard-information-architecture.md",
            "## Output contract",
            "## Quality gate",
            "standalone HTML",
            "금지",
        ):
            self.assertIn(token, text)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
        self.assertIn("building-project-visual-dashboards", p05["owned_skill_ids"])

    def test_frozen_sheet_history_is_preserved_while_current_authority_is_migration_only(self) -> None:
        generator = GENERATOR.read_text(encoding="utf-8")
        self.assertIn('"project_sheet_role": "MIGRATION_ONLY_LEGACY_SOURCE"', generator)
        self.assertIn('"sheet_only_change_status": "MIGRATION_PROPOSAL_ONLY"', generator)
        self.assertIn('"id": "BASE-V9-004"', generator)
        self.assertIn('"id": "BASE-V9-002", "status": "SUPERSEDED"', generator)

        frozen = json.loads(SHEET_CONTROL.read_text(encoding="utf-8"))
        self.assertEqual("BASE_EXCLUDED", frozen["base_sheet_status"])
        self.assertEqual("USER_FACING_GDD_WORKSPACE", frozen["project_sheet_role"])
        self.assertEqual("PROPOSED_SHEET_CHANGE", frozen["sheet_only_change_status"])
        self.assertFalse(frozen["external_sheet_writes_authorized"])
        self.assertNotIn("active_project_workspace", frozen)

        version = BASE_RULES_VERSION.read_text(encoding="utf-8")
        self.assertIn("Frozen v9.0 release derivatives", version)
        self.assertIn("not a current projection", version)
        self.assertIn("Project GDD Google Sheets policy", version)

        decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
        old = next(row for row in decisions if row["id"] == "BASE-V9-002")
        current = next(row for row in decisions if row["id"] == "BASE-V9-004")
        self.assertEqual("SUPERSEDED", old["status"])
        self.assertEqual("BASE-V9-004", old["superseded_by"])
        self.assertEqual("CONFIRMED", current["status"])
        self.assertIn("migration-only", current["decision"].lower())
        self.assertFalse(any(
            row["status"] == "CONFIRMED" and "USER_FACING_GDD_WORKSPACE" in row["decision"]
            for row in decisions
        ))

    def test_skill_freshness_requires_meaningful_routing_companion_not_any_part_test(self) -> None:
        data = json.loads(FRESHNESS_CONFIG.read_text(encoding="utf-8"))
        rule = next(
            item for item in data["coupled_change_rules"]
            if item["name"] == "skill-description-learning-test-sync"
        )
        companions = rule["require_any_changed"]
        self.assertIn("tests/test_skill_routing_governance.py", companions)
        self.assertNotIn("tests/test_p0[1-9]_*.py", companions)
        self.assertNotIn("tests/test_bca_visual_sheet_workflow.py", companions)
        routing_test = ROUTING_TEST.read_text(encoding="utf-8")
        self.assertIn("test_base_visual_dashboard_routes_to_notion_home_not_html", routing_test)

    def test_qa_evidence_studio_files_remain_present(self) -> None:
        for relative in (
            "tools/qa-evidence-studio/README.md",
            "tools/qa-evidence-studio/src/qa_evidence_studio/service.py",
            "tools/qa-evidence-studio/tests/test_service.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
