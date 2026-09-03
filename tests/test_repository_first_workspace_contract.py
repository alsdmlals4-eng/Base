from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
ACTIVE_POLICY = ROOT / "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md"
CODEX_POLICY = ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md"
MIGRATION_CHECKLIST = ROOT / "templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md"


def text(path: str | Path) -> str:
    candidate = path if isinstance(path, Path) else ROOT / path
    return candidate.read_text(encoding="utf-8")


class RepositoryFirstWorkspaceContractTests(unittest.TestCase):
    def test_active_entrypoints_do_not_restore_v3_as_the_default_workspace(self) -> None:
        legacy_contract = json.loads(
            text("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json")
        )

        self.assertEqual(
            "V3_COMPATIBILITY_AND_HISTORY_ONLY", legacy_contract["status"]
        )
        self.assertFalse(legacy_contract["active_route_for_new_work"])

        active_entrypoints = (
            "docs/DOCUMENTATION_MAP.md",
            "docs/OPERATING_MODEL.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
            "templates/AGENTS.project.md",
            "templates/project-operations/README.md",
        )
        retired_default = (
            "현재 기본 계약은 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`"
        )

        for path in active_entrypoints:
            with self.subTest(path=path):
                source = text(path)
                self.assertIn("PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", source)
                self.assertIn("REPOSITORY_PRIMARY_CANON", source)
                self.assertNotIn(retired_default, source)

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

    def test_active_operating_routes_do_not_require_notion_without_an_explicit_v4_exception(self) -> None:
        active_routes = (
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
            "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md",
            "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md",
            "docs/VISUAL_COLLABORATION_TOOL_POLICY.md",
        )
        for path in active_routes:
            with self.subTest(path=path):
                source = text(path)
                self.assertIn("PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", source)
                self.assertIn("V4_NOTION_EXCEPTION_ONLY", source)
                self.assertIn("NO_NEW_NOTION_WRITE_BY_DEFAULT", source)

        intake = text(active_routes[0])
        self.assertIn("REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK", intake)
        self.assertNotIn("APPROVED_DECISION_GITHUB_NOTION_SYNC_DURING_WORK", intake)

    def test_active_skill_registry_routes_core_work_through_repository_first_receipts(self) -> None:
        registry = json.loads(text("skills/SKILL_REGISTRY.json"))
        rows = {item["skill_id"]: item for item in registry["skills"]}

        for skill_id in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
        ):
            with self.subTest(skill_id=skill_id):
                row = rows[skill_id]
                self.assertIn("repository-first-workspace", row["trigger_tags"])
                self.assertIn("repository-human-projection", row["trigger_tags"])
                self.assertNotIn("notion-project-workspace", row["trigger_tags"])
                self.assertNotIn("Project Notion", "\n".join(row["use_when"]))

        intake = rows["managing-project-intake-and-work-contract"]
        for trigger in (
            "benchmark-preflight",
            "benchmark-reverse-engineering",
            "legacy-context-hygiene",
        ):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, intake["trigger_tags"])

    def test_v4_contract_has_a_single_partition_owner_and_v3_is_compatibility_only(self) -> None:
        manifest = json.loads(text("docs/operations/BASE_PARTITION_MANIFEST.json"))
        p01 = next(part for part in manifest["parts"] if part["part_id"] == "P01")

        self.assertIn(
            "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
            p01["owned_write_paths"],
        )
        self.assertIn("REPOSITORY_PRIMARY_CANON", p01["important_rules"])
        self.assertIn("NO_NEW_NOTION_WRITE_BY_DEFAULT", p01["important_rules"])
        self.assertNotIn("NOTION_DEFAULT_PROJECT_WORKSPACE", p01["important_rules"])

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

    def test_readme_routes_new_workers_to_repository_first_authority(self) -> None:
        readme = text("README.md")

        for token in (
            "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md",
            "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED",
            "POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP",
        ):
            with self.subTest(token=token):
                self.assertIn(token, readme)

        self.assertNotIn(
            "새 프로젝트와 새 기획·시각 작업의 기본 인간 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`",
            readme,
        )

    def test_start_here_cold_start_does_not_require_notion(self) -> None:
        start_here = text("START_HERE.md")

        for token in (
            "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md",
            "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED",
            "ASSET_MANIFEST.json",
        ):
            with self.subTest(token=token):
                self.assertIn(token, start_here)

        self.assertNotIn(
            "→ exact Project Notion Home·filtered human-facing surfaces",
            start_here,
        )
        self.assertNotIn(
            "기본 사람용 프로젝트 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`다",
            start_here,
        )

    def test_codex_policy_rehydrates_exact_repository_and_manifest(self) -> None:
        codex = text(CODEX_POLICY)

        for token in (
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "CODEX_VISUAL_INPUT_REPOSITORY_MANIFEST_ONLY",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "exact_source_sha",
            "asset_manifest",
            "approved_repository_visuals_consumed",
        ):
            with self.subTest(token=token):
                self.assertIn(token, codex)

        self.assertIn("CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION_RETIRED", codex)
        self.assertIn("CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY_RETIRED", codex)
        self.assertNotIn(
            "→ Codex가 해당 프로젝트의 GitHub + Notion을 fresh-read",
            codex,
        )
        self.assertNotIn(
            "Codex가 사용할 수 있는 것은 현재 용도로 승인되고 Notion에 실제 업로드·attach·readback된 Visual뿐이다",
            codex,
        )

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


    def test_migration_export_has_current_format_and_restore_limits(self) -> None:
        checklist = text(MIGRATION_CHECKLIST)
        heading = "### Export·백업의 증거 한계"
        self.assertIn(heading, checklist)
        section = checklist.split(heading, 1)[1].split("## 2.", 1)[0]
        for token in (
            "https://www.notion.com/help/back-up-your-data",
            "2026-08-31",
            "HTML",
            "Markdown",
            "CSV",
            "개별 페이지 PDF",
            "EXPORT_SUCCESS_IS_NOT_MIGRATION_COMPLETE",
            "export/API 요청 성공이나 ZIP 생성만으로 전체 자료 회수·의미 보존·이관 완료를 판정하지 않았다.",
            "export 결과를 다시 올려도 workspace의 **원상 복원**이 보장되지 않음을 확인했다.",
            "일반 프로젝트 작업의 Notion 조회·export 의무를 다시 만들지 않는다.",
            "권한",
            "원상 복원",
        ):
            with self.subTest(token=token):
                self.assertIn(token, section)

    def test_migration_incomplete_inventory_cannot_be_counted_as_zero(self) -> None:
        checklist = text(MIGRATION_CHECKLIST)
        section = checklist.split("## 10. 이관 잔여 카운터", 1)[1].split("## 11.", 1)[0]
        self.assertIn("INVENTORY_INCOMPLETE", section)
        self.assertIn("UNKNOWN", section)
        self.assertIn("UNKNOWN을 0으로 바꾸지 않는다.", section)
        self.assertIn("완료 목표값", section)
        self.assertIn("inventory COMPLETE + 모두 0 + 대상 owner readback 완료", section)
        self.assertLess(section.index("INVENTORY_INCOMPLETE"), section.index("inventory COMPLETE + 모두 0"))
        self.assertIn("NO_DELETE_REQUIRED_FOR_RETIREMENT", section)

    def test_migration_receipt_records_inventory_and_export_evidence(self) -> None:
        checklist = text(MIGRATION_CHECKLIST)
        section = checklist.split("## 12. 완료 receipt", 1)[1]
        self.assertIn("inventory.destination_owner_readback_receipt", section)
        for token in (
            "inventory:",
            "status: NOT_CHECKED | INCOMPLETE | COMPLETE",
            "scope_and_access_receipt:",
            "excluded_or_unreadable:",
            "export_or_read_receipt:",
            "\n  destination_owner_readback_receipt:\n",
        ):
            with self.subTest(token=token):
                self.assertIn(token, section)


    def test_migration_exit_gate_is_aligned_across_active_owners(self) -> None:
        contract = json.loads(text(ACTIVE_CONTRACT))
        gates = contract["migration_exit_gates"]
        self.assertEqual("ALL_OF", contract.get("migration_exit_gate_logic"))
        for name in (
            "NOTION_UNIQUE_CANON_COUNT",
            "CODEX_NOTION_DEPENDENCY_COUNT",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT",
        ):
            with self.subTest(counter=name):
                self.assertIs(int, type(gates.get(name)))
                self.assertEqual(0, gates[name])
        self.assertEqual("COMPLETE", gates.get("inventory.status"))
        self.assertEqual(
            "ALL_SCOPED_ITEMS_VERIFIED",
            gates.get("inventory.destination_owner_readback_receipt"),
        )
        policy = text(ACTIVE_POLICY).split("### 6.2 이관 완료 Gate", 1)[1].split("### 6.3", 1)[0]
        self.assertIn("UNKNOWN을 0으로 바꾸지 않는다.", policy)
        self.assertIn("INVENTORY_INCOMPLETE", policy)
        self.assertIn(
            "다음 세 카운터의 검증된 0, `inventory.status == COMPLETE`, "
            "각 이관 대상의 `inventory.destination_owner_readback_receipt` 검증을 모두 충족한 경우에만 "
            "`NOTION_RETIRED_FROM_ACTIVE_FLOW`로 기록할 수 있다.",
            policy,
        )
        self.assertNotIn("모두 0이 되면 상태를 `NOTION_RETIRED_FROM_ACTIVE_FLOW`로 기록할 수 있다.", policy)



if __name__ == "__main__":
    unittest.main()
