import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class NotionProjectWorkspaceContractTests(unittest.TestCase):
    def test_v3_machine_workspace_contract_is_retained_for_compatibility_only(self) -> None:
        contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
        self.assertEqual(3, contract["schema_version"])
        self.assertEqual("V3_COMPATIBILITY_AND_HISTORY_ONLY", contract["status"])
        self.assertFalse(contract["active_route_for_new_work"])
        self.assertEqual("NOTION_DEFAULT_PROJECT_WORKSPACE", contract["project_workspace"])
        self.assertEqual("PROJECT_RELATION_REQUIRED", contract["project_relation"])
        self.assertEqual("WORK_MASTER", contract["work_master"])
        self.assertEqual("ASSET_KNOWLEDGE_MASTER", contract["asset_master"])
        self.assertEqual("VISUAL_MAP_DERIVED", contract["visual_map"])
        self.assertEqual("REPOSITORY_RUNTIME_TRUTH", contract["runtime_truth"])

    def test_v3_split_domain_details_are_not_the_active_new_work_route(self) -> None:
        contract = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
        self.assertEqual("DOMAIN_SPLIT_CANON", contract["authority_model"])
        self.assertEqual("NOTION_HUMAN_FACING_CANON", contract["human_facing_canon"])
        self.assertEqual("REPOSITORY_STRUCTURED_CANON", contract["repository_structured_canon"])
        self.assertTrue({
            "PROJECT_OVERVIEW", "VISUAL_DIRECTION", "VISUAL_ASSET_CATALOG",
            "BUDGET_TABLE", "TIER_TABLE", "HUMAN_EDITABLE_FLOW_MAP", "STORYBOARD",
        }.issubset(set(contract["notion_priority_domains"])))
        self.assertTrue({
            "MARKDOWN_SPEC", "JSON_DATA", "GAME_DATA", "CODE", "SCENE",
            "RESOURCE", "TEST", "RUNTIME_EVIDENCE",
        }.issubset(set(contract["repository_priority_domains"])))
        self.assertEqual("SYNC_BEFORE_IMPLEMENTATION", contract["cross_domain_sync"])
        active = json.loads(text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"))
        self.assertEqual("ACTIVE_DEFAULT", active["status"])
        self.assertEqual(
            "FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER",
            active["authority_model"],
        )

    def test_managing_design_documents_uses_repository_first_with_scoped_legacy_notion(self) -> None:
        skill = text("skills/managing-design-documents/SKILL.md")
        for token in (
            "PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", "REPOSITORY_PRIMARY_CANON",
            "APPROVED_HUMAN_BLUEPRINT_PDF_CANON", "PROPOSED_LEGACY_CHANGE",
            "SYNC_BEFORE_IMPLEMENTATION", "COMPATIBILITY_ONLY",
        ):
            self.assertIn(token, skill)
        self.assertNotIn("USER_FACING_GDD_WORKSPACE", skill)
        self.assertNotIn("프로젝트 Google Sheets까지 같은 승인 단위에서 동기화", skill)

    def test_confirmed_decision_sync_uses_repository_first_canon(self) -> None:
        policy = text("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for token in (
            "PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", "REPOSITORY_PRIMARY_CANON",
            "APPROVED_HUMAN_BLUEPRINT_PDF_CANON", "PROPOSED_LEGACY_CHANGE",
            "DERIVED_VIEW_UPDATED", "SYNC_BEFORE_IMPLEMENTATION",
            "COMPATIBILITY_ONLY",
        ):
            self.assertIn(token, policy)
        self.assertNotIn("USER_FACING_GDD_WORKSPACE", policy)
        self.assertNotIn("Google Sheets가 갱신되고 재조회 결과가 일치했다", policy)

    def test_visual_policy_uses_v4_repository_first_authority_and_deprecates_figma_default(self) -> None:
        policy = text("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for token in (
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE", "REPOSITORY_PRIMARY_CANON",
            "APPROVED_HUMAN_BLUEPRINT_PDF_CANON", "V4_NOTION_EXCEPTION_ONLY",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT", "PROJECT_RELATION_REQUIRED",
            "ASSET_KNOWLEDGE_MASTER", "VISUAL_MAP_DERIVED", "Record Type",
            "ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE",
            "source provenance", "version", "readback", "human", "AI / System",
        ):
            self.assertIn(token, policy)
        self.assertNotIn("The default project operating surface is `NOTION_DEFAULT_PROJECT_WORKSPACE`", policy)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", policy)
        self.assertIn("Figma Bridge", policy)
        self.assertIn("not active authorities", policy)
        self.assertIn("Do not restore a deprecated execution surface", policy)

    def test_deprecated_visual_execution_surfaces_are_absent(self) -> None:
        for path in (
            "tools/figma-bridge", "tools/expression-studio", "tools/sprite-animation-studio",
            "tools/tool-hub", "docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json",
            "docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json",
            "docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json",
            "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md",
            "templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md",
            "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md",
        ):
            self.assertFalse((ROOT / path).exists(), path)

    def test_qa_evidence_studio_remains_independent(self) -> None:
        readme = text("tools/qa-evidence-studio/README.md")
        self.assertIn("QA Evidence Studio", readme)
        self.assertIn("DEVELOPER_OWNER", readme)
        self.assertIn("DEFERRED_NOT_CONNECTED", readme)
        self.assertNotIn("Figma", readme)

    def test_google_sheets_is_compatibility_only(self) -> None:
        policy = text("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        self.assertIn("COMPATIBILITY_ONLY", policy)
        self.assertIn("DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE", policy)
        self.assertIn("V4_NOTION_EXCEPTION_ONLY", policy)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", policy)

    def test_active_paid_plan_does_not_require_figma(self) -> None:
        agents = text("AGENTS.md")
        self.assertIn("CURRENT_PAID_PLANS: GPT_PRO", agents)
        self.assertIn("PAID_PLAN_COUNT: 1", agents)
        self.assertNotIn("CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO", agents)


if __name__ == "__main__":
    unittest.main()
