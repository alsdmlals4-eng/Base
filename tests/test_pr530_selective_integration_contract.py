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
        self.assertNotIn("QA_EVIDENCE_STUDIO_SPECIALIST_VALIDATION_RETAINED", text)

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

    def test_workspace_contract_scopes_codex_to_godot_product_and_keeps_gpt_governance(self) -> None:
        data = json.loads(WORKSPACE.read_text(encoding="utf-8"))
        self.assertEqual(3, data["schema_version"])
        self.assertEqual("docs/GPT_CODEX_WORKFLOW_POLICY.md", data["workflow_policy"])
        self.assertEqual("GPT_NONCODING_PROJECT_OWNER", data["planning_owner"])
        self.assertEqual("GPT_BASE_NOTION_GOVERNANCE_OWNER", data["base_governance_owner"])
        self.assertEqual("CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER", data["codex_role"])
        self.assertTrue(data["codex_not_general_repository_executor"])
        self.assertEqual("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", data["human_home_policy"])
        self.assertEqual("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md", data["retirement_policy"])
        self.assertEqual("MIGRATION_ONLY_UNTIL_REMOVAL", data["google_sheets"])
        self.assertEqual("QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW", data["qa_evidence_studio"])
        self.assertIn("BASE_VALIDATION_CONTRACT", data["gpt_repository_domains"])
        self.assertIn("GODOT_IMPLEMENTATION_TEST", data["codex_product_domains"])

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

        handoff = rows["maintaining-project-context-and-handoff"]
        self.assertIn("godot-product-implementation-handoff", handoff["trigger_tags"])
        self.assertTrue(any("Base 정책" in text for text in handoff["do_not_use_when"]))

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
        frozen = json.loads(SHEET_CONTROL.read_text(encoding="utf-8"))
        self.assertEqual("BASE_EXCLUDED", frozen["base_sheet_status"])
        self.assertEqual("USER_FACING_GDD_WORKSPACE", frozen["project_sheet_role"])
        self.assertFalse(frozen["external_sheet_writes_authorized"])
        version = BASE_RULES_VERSION.read_text(encoding="utf-8")
        self.assertIn("Frozen v9.0 release derivatives", version)
        decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
        old = next(row for row in decisions if row["id"] == "BASE-V9-002")
        current = next(row for row in decisions if row["id"] == "BASE-V9-004")
        self.assertEqual("SUPERSEDED", old["status"])
        self.assertEqual("CONFIRMED", current["status"])

    def test_skill_freshness_requires_meaningful_routing_companion_not_any_part_test(self) -> None:
        data = json.loads(FRESHNESS_CONFIG.read_text(encoding="utf-8"))
        rule = next(
            item for item in data["coupled_change_rules"]
            if item["name"] == "skill-description-learning-test-sync"
        )
        companions = rule["require_any_changed"]
        self.assertIn("tests/test_skill_routing_governance.py", companions)
        self.assertNotIn("tests/test_p0[1-9]_*.py", companions)
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
