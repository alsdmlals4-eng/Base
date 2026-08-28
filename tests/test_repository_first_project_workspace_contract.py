from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class RepositoryFirstProjectWorkspaceContractTests(unittest.TestCase):
    def test_machine_contract_uses_repository_primary_canon(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json")
        )
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("REPOSITORY_PRIMARY_CANON", data["authority_model"])
        self.assertEqual("REPOSITORY_PRIMARY_PROJECT_CANON", data["project_workspace"])
        self.assertEqual("HUMAN_GDD_PDF_DERIVED_VIEW", data["human_facing_view"])
        self.assertEqual(
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            data["ai_facing_canon"],
        )
        self.assertEqual("LEGACY_READ_ONLY_MIGRATION_SOURCE", data["notion_status"])
        self.assertEqual("FORBIDDEN_BY_DEFAULT", data["new_notion_write"])
        self.assertEqual("EXACT_REPOSITORY_COMMIT", data["codex_rehydration"])
        self.assertEqual(
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            data["approved_visual_delivery"],
        )
        self.assertEqual(
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
            data["postmerge_readback"],
        )

    def test_machine_contract_limits_default_deliverables_to_human_pdf_and_ai_spec(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json")
        )
        self.assertEqual(
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            data["master_gdd_profile"],
        )
        self.assertEqual(
            [
                "HUMAN_DETAILED_GDD_PDF",
                "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            ],
            data["default_project_deliverables"],
        )
        self.assertEqual("PDF_ONLY_USER_DOWNLOAD", data["user_download_policy"])
        self.assertEqual(
            "REPOSITORY_PATH_BRANCH_COMMIT_PR_VALIDATION_ONLY",
            data["ai_markdown_delivery"],
        )
        self.assertTrue(data["shared_id_and_source_sha_required"])
        self.assertTrue(data["core_system_and_content_implementation_detail_required"])
        self.assertEqual(
            "EXPLICIT_USER_REQUEST_ONLY",
            data["automatic_image_generation"],
        )
        self.assertEqual(
            "NOTION_INPUT_ONLY_NO_OUTPUT",
            data["notion_master_gdd_profile"],
        )
        self.assertEqual(
            "templates/project-operations/DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md",
            data["master_gdd_work_instruction"],
        )
        self.assertEqual("APPROVED_PROFILE_ABSORBED", data["approved_profile_disposition"])
        self.assertFalse(data["human_pdf_is_independent_canon"])
        self.assertFalse(data["chatgpt_work_is_canon"])
        self.assertFalse(data["chatgpt_library_is_canon"])

    def test_machine_contract_requires_deterministic_asset_delivery(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json")
        )
        required = set(data["approved_asset_required_fields"])
        self.assertTrue(
            {
                "asset_id",
                "repository_path",
                "actual_consumer",
                "approval_status",
                "version",
                "sha256",
                "source_or_provenance",
                "rights_or_license_state",
                "implementation_status",
            }.issubset(required)
        )
        self.assertEqual(
            "NOTION_ABSENCE_IS_NOT_A_BLOCKER",
            data["notion_absence_for_codex"],
        )
        self.assertEqual(
            "GPT_VISUAL_REQUEST_THEN_REPOSITORY_DELIVERY",
            data["missing_visual_route"],
        )

    def test_machine_contract_defines_legacy_migration_exit_counts(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json")
        )
        self.assertEqual(
            {
                "NOTION_UNIQUE_CANON_COUNT": 0,
                "CODEX_NOTION_DEPENDENCY_COUNT": 0,
                "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT": 0,
            },
            data["notion_retirement_exit_counts"],
        )
        self.assertEqual(
            ["UNIQUE", "DUPLICATE", "OBSOLETE", "BLOCKED_UNVERIFIED"],
            data["legacy_material_classifications"],
        )
        self.assertEqual("NO_DELETE_IN_BASE_TRANSITION", data["legacy_delete_policy"])

    def test_human_policy_covers_authority_delivery_and_retirement(self) -> None:
        policy = text("docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md")
        for token in (
            "REPOSITORY_PRIMARY_CANON",
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED",
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "PDF_ONLY_USER_DOWNLOAD",
            "NOTION_INPUT_ONLY_NO_OUTPUT",
            "NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX",
            "NO_SEPARATE_IMAGE_BUNDLE",
            "NO_AUTOMATIC_IMAGE_GENERATION",
            "APPROVED_PROFILE_ABSORBED",
            "NOTION_UNIQUE_CANON_COUNT = 0",
            "CODEX_NOTION_DEPENDENCY_COUNT = 0",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
        ):
            self.assertIn(token, policy)
        self.assertIn("PDF는 정본이 아니다", policy)
        self.assertIn("새 Notion 쓰기", policy)
        self.assertIn("금지", policy)

    def test_gpt_codex_handoff_uses_exact_repository_inputs(self) -> None:
        policy = text("docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md")
        for token in (
            "EXACT_REPOSITORY_COMMIT",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "NOTION_ABSENCE_IS_NOT_A_BLOCKER",
            "GPT_VISUAL_REQUEST",
            "READY_FOR_GPT_REVIEW",
            "CANON_SYNC_AFTER_VALIDATION",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
        ):
            self.assertIn(token, policy)
        self.assertNotIn("Notion upload is required", policy)

    def test_project_templates_preserve_two_deliverables_and_safe_migration(self) -> None:
        ai_spec = text("templates/project-operations/AI_PROJECT_CANON_SPEC.md")
        pdf = text("templates/project-operations/HUMAN_GDD_PDF_EXPORT_CHECKLIST.md")
        migration = text(
            "templates/project-operations/NOTION_RETIREMENT_AND_REPOSITORY_MIGRATION_CHECKLIST.md"
        )
        work_instruction = text(
            "templates/project-operations/DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md"
        )
        for token in (
            "player_outcome",
            "meaningful_choices",
            "core_systems_and_content",
            "implementation_contract",
            "actual_asset_consumers",
            "acceptance_and_evidence",
            "explicit_non_scope",
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "shared_id_registry_version",
            "human_pdf_source_commit",
            "SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC",
            "PDF_ONLY_USER_DOWNLOAD",
            "REPOSITORY_PATH_BRANCH_COMMIT_PR_VALIDATION_ONLY",
            "STALE_DERIVED_VIEW",
            "NO_AUTOMATIC_IMAGE_GENERATION",
        ):
            self.assertIn(token, ai_spec)
        for token in (
            "source_branch",
            "source_commit",
            "canon_version",
            "shared_id_registry_version",
            "ai_spec_source_commit",
            "included_scope",
            "evidence_ceiling",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC",
            "STALE_DERIVED_VIEW",
            "PDF_ONLY_USER_DOWNLOAD",
            "REPOSITORY_PATH_BRANCH_COMMIT_PR_VALIDATION_ONLY",
            "NO_AUTOMATIC_IMAGE_GENERATION",
            "NO_NOTION_OUTPUT",
            "user_download_link_count: 1",
        ):
            self.assertIn(token, pdf)
        for token in (
            "UNIQUE",
            "DUPLICATE",
            "OBSOLETE",
            "BLOCKED_UNVERIFIED",
            "NOTION_UNIQUE_CANON_COUNT",
            "CODEX_NOTION_DEPENDENCY_COUNT",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT",
            "destination_readback",
        ):
            self.assertIn(token, migration)
        for token in (
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "PDF_ONLY_USER_DOWNLOAD",
            "NOTION_INPUT_ONLY_NO_OUTPUT",
            "CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED",
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX",
            "NO_SEPARATE_IMAGE_BUNDLE",
            "NO_AUTOMATIC_IMAGE_GENERATION",
            "사용자 다운로드: 사람용 PDF 링크 1개만 제공",
        ):
            self.assertIn(token, work_instruction)

    def test_approved_two_artifact_proposal_is_present_as_absorbed_input(self) -> None:
        proposal_path = (
            "[수정제안서]/BCP-2026-047-desktop-two-artifact-master-gdd/PROPOSAL.md"
        )
        proposal = text(proposal_path)
        self.assertIn("APPROVED_FOR_IMPLEMENTATION", proposal)
        self.assertIn("EXACTLY_TWO_DELIVERABLES", proposal)
        self.assertIn("PDF_ONLY_USER_DOWNLOAD", proposal)
        self.assertIn("NOTION_INPUT_ONLY_NO_OUTPUT", proposal)
        self.assertIn("SHARED_ID_AND_SOURCE_SHA_REQUIRED", proposal)
        self.assertIn("NO_AUTOMATIC_IMAGE_GENERATION", proposal)

    def test_root_entrypoints_route_to_repository_first_owner(self) -> None:
        agents = text("AGENTS.md")
        readme = text("README.md")
        start_here = text("START_HERE.md")
        for token in (
            "docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json",
            "docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md",
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS",
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
        ):
            self.assertIn(token, agents)
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
        ):
            self.assertIn(token, readme)
        for token in (
            "docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json",
            "docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md",
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS",
        ):
            self.assertIn(token, start_here)
        self.assertNotIn("exact Project Notion Home", start_here)
        self.assertNotIn(
            "기본 사람용 프로젝트 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`",
            start_here,
        )
        self.assertNotIn(
            "새 프로젝트와 새 기획·시각 작업의 기본 인간 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`",
            readme,
        )

    def test_partial_supersession_preserves_non_workspace_safety_rules(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_WORKSPACE_SUPERSESSION_MAP.json")
        )
        self.assertEqual(1, data["schema_version"])
        self.assertEqual(
            "CURRENT_SPECIFIC_WORKSPACE_OWNER_OVERRIDES_OLDER_GENERAL_OR_COMPATIBILITY_TEXT",
            data["precedence"],
        )
        by_path = {entry["path"]: entry for entry in data["entries"]}
        operating_model = by_path["docs/OPERATING_MODEL.md"]
        self.assertEqual("PARTIAL_SUPERSESSION", operating_model["status"])
        self.assertIn("Base lifecycle", operating_model["retained_use"])
        self.assertIn(
            "POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP workspace synchronization",
            operating_model["superseded"],
        )
        self.assertIn(
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
            operating_model["replacement"],
        )
        gpt_codex = by_path["docs/GPT_CODEX_WORKFLOW_POLICY.md"]
        self.assertEqual("PARTIAL_SUPERSESSION", gpt_codex["status"])
        self.assertIn(
            "GPT and Codex product-responsibility split",
            gpt_codex["retained_use"],
        )
        self.assertIn(
            "CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY",
            gpt_codex["superseded"],
        )

    def test_legacy_notion_contracts_are_discovery_only_not_current_default(self) -> None:
        policy = text("docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md")
        for legacy_token in (
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "NOTION_HUMAN_FACING_CANON",
            "CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION",
            "CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY",
            "POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP",
        ):
            self.assertIn(legacy_token, policy)
        self.assertIn("LEGACY_DISCOVERY_ONLY", policy)
        self.assertIn("현재 기본값으로 복원하지 않는다", policy)


if __name__ == "__main__":
    unittest.main()
