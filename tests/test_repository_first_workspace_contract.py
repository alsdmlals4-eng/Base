from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
ACTIVE_POLICY = ROOT / "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md"
MIGRATION_CHECKLIST = ROOT / "templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md"


def text(path: str | Path) -> str:
    candidate = path if isinstance(path, Path) else ROOT / path
    return candidate.read_text(encoding="utf-8")


class RepositoryFirstWorkspaceContractTests(unittest.TestCase):
    def test_machine_contract_is_repository_first_and_notion_optional(self) -> None:
        contract = json.loads(text(ACTIVE_CONTRACT))

        self.assertEqual(4, contract["schema_version"])
        self.assertEqual("ACTIVE_DEFAULT", contract["status"])
        self.assertEqual(
            "REPOSITORY_PRIMARY_CANON_WITH_DERIVED_HUMAN_PDF",
            contract["authority_model"],
        )
        self.assertEqual(
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            contract["project_workspace"],
        )
        self.assertEqual("REPOSITORY_PRIMARY_CANON", contract["project_canon"])
        self.assertEqual("HUMAN_GDD_PDF_DERIVED_VIEW", contract["human_facing_view"])
        self.assertEqual(
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            contract["work_surface"],
        )
        self.assertEqual(
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            contract["library_surface"],
        )
        self.assertTrue(contract["no_new_notion_write_by_default"])
        self.assertEqual(
            "LEGACY_OPTIONAL_READ_ONLY_MIGRATION_SOURCE",
            contract["notion"],
        )

    def test_codex_and_visual_handoff_use_exact_repository_evidence(self) -> None:
        contract = json.loads(text(ACTIVE_CONTRACT))

        self.assertEqual(
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            contract["codex_rehydration"],
        )
        self.assertEqual(
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            contract["codex_visual_input"],
        )
        self.assertEqual(
            "GPT_CREATE_REVIEW_APPROVE_THEN_REPOSITORY_MANIFEST",
            contract["missing_visual_route"],
        )
        self.assertTrue(
            {
                "asset_id",
                "consumer",
                "repository_path",
                "sha256",
                "approval_status",
                "implementation_status",
                "provenance",
            }.issubset(set(contract["required_asset_manifest_fields"]))
        )

    def test_agents_routes_repository_first_owner_without_erasing_legacy_evidence(self) -> None:
        agents = text("AGENTS.md")

        for token in (
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
            "POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP",
        ):
            with self.subTest(token=token):
                self.assertIn(token, agents)

        # Existing tests and historical documents may still mention the former token.
        # The active root must explicitly mark it retired rather than silently treating it as current.
        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED", agents)

    def test_active_policy_defines_two_artifacts_and_noncanon_surfaces(self) -> None:
        policy = text(ACTIVE_POLICY)

        for token in (
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "AI_PRODUCTION_SPEC_MARKDOWN",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "PDF_IS_DERIVED_SNAPSHOT_NOT_CANON",
        ):
            with self.subTest(token=token):
                self.assertIn(token, policy)

        master_gdd = text("docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md")
        self.assertIn("EXACTLY_TWO_DELIVERABLES", master_gdd)
        self.assertIn("HUMAN_MASTER_GDD_PDF", master_gdd)
        self.assertIn("AI_PRODUCTION_SPEC_MARKDOWN", master_gdd)

    def test_migration_requires_zero_unique_canon_and_no_destructive_shortcut(self) -> None:
        policy = text(ACTIVE_POLICY)
        checklist = text(MIGRATION_CHECKLIST)

        for token in (
            "NOTION_UNIQUE_CANON_COUNT = 0",
            "CODEX_NOTION_DEPENDENCY_COUNT = 0",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
            "LEGACY_READ_ONLY",
            "NO_DELETE_REQUIRED_FOR_RETIREMENT",
        ):
            with self.subTest(token=token):
                self.assertIn(token, policy)
                self.assertIn(token, checklist)

        self.assertIn("원본 binary", checklist)
        self.assertIn("SHA-256", checklist)
        self.assertIn("readback", checklist)


if __name__ == "__main__":
    unittest.main()
