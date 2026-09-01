from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
POLICY = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
MANAGING = ROOT / "skills" / "managing-design-documents" / "SKILL.md"
MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
V9_WORKFLOW = ROOT / ".github" / "workflows" / "validate-base-v9-rc.yml"


class NotionProjectIsolationCoreSystemContractTests(unittest.TestCase):
    def test_workspace_authority_declares_project_isolation_and_core_system_master(self) -> None:
        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))

        self.assertEqual("PROJECT_NAMESPACE_ISOLATION", contract["parallel_project_write_model"])
        self.assertEqual("CORE_SYSTEM_MASTER", contract["core_system_master"])
        self.assertEqual("OPTIMISTIC_CONFLICT_DETECTION", contract["same_record_concurrency"])
        self.assertEqual("BOUNDED_RECORD_WRITE", contract["notion_write_mode"])
        self.assertEqual(
            "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md",
            contract["parallel_write_policy"],
        )
        self.assertIn("SYSTEM", contract["required_project_record_types"])
        self.assertIn("Record Key", contract["core_system_identity_fields"])
        self.assertIn("Revision", contract["core_system_identity_fields"])
        self.assertIn("Last Edited", contract["core_system_identity_fields"])
        self.assertIn("CONFLICT_STALE_READ", contract["conflict_states"])
        self.assertIn("CONFLICT_DUPLICATE_KEY", contract["conflict_states"])

        invariants = "\n".join(contract["invariants"])
        for required in (
            "exactly one Project relation",
            "deterministic Record Key",
            "Revision and Last Edited",
            "bounded record-level update",
            "stale read",
            "destination readback",
        ):
            self.assertIn(required, invariants)

    def test_single_policy_owner_has_fail_closed_parallel_write_protocol(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "PROJECT_NAMESPACE_ISOLATION",
            "CORE SYSTEM · Master",
            "08 · 핵심 시스템 · 상세",
            "<ProjectKey>::<RecordType>::<LocalId>",
            "Revision",
            "Last Edited",
            "CONFLICT_STALE_READ",
            "CONFLICT_DUPLICATE_KEY",
            "bounded field-level update",
            "destination readback",
        ):
            self.assertIn(required, text)

        self.assertIn("다른 Project relation", text)
        self.assertIn("전체 `replace_content`", text)

    def test_existing_skill_and_documentation_map_route_to_workspace_authority(self) -> None:
        managing = MANAGING.read_text(encoding="utf-8")
        documentation_map = MAP.read_text(encoding="utf-8")
        for text in (managing, documentation_map):
            self.assertIn("PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", text)
            self.assertIn("REPOSITORY_PRIMARY_CANON", text)

        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        self.assertTrue((ROOT / contract["parallel_write_policy"]).is_file())

    def test_free_plan_path_does_not_require_business_query_data_sources(self) -> None:
        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        self.assertEqual("ZERO_INCREMENTAL_COST", contract["default_cost_boundary"])
        self.assertEqual("OPTIONAL_OPTIMIZATION_NOT_REQUIRED", contract["notion_query_data_sources"])
        self.assertEqual(
            "PROJECT_FILTERED_VIEW_SEARCH_FETCH_READBACK",
            contract["free_plan_fallback"],
        )

        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "QUERY_DATA_SOURCES_OPTIONAL",
            "ZERO_INCREMENTAL_COST",
            "Project-filtered linked view",
            "search/fetch",
            "destination readback",
        ):
            self.assertIn(required, text)

    def test_p01_active_planning_surfaces_use_repository_first_and_legacy_sources_are_compatibility_only(self) -> None:
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        project_os = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        grill_policy = (ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md").read_text(encoding="utf-8")
        continuous = (
            ROOT
            / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
        ).read_text(encoding="utf-8")
        decisions = (ROOT / "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md").read_text(encoding="utf-8")
        grill_record = (ROOT / "templates/project-operations/GRILL_ME_DECISION_RECORD.md").read_text(encoding="utf-8")

        for source in (intake, project_os, decisions, grill_record):
            self.assertIn("REPOSITORY_PRIMARY_CANON", source)
            self.assertIn("COMPATIBILITY_ONLY", source)

        for source in (intake, project_os):
            self.assertIn("PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json", source)
            self.assertIn("DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE", source)
            self.assertIn("google_sheet_compatibility_source", source)
            self.assertIn("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", source)
            self.assertNotIn("USER_FACING_GDD_WORKSPACE", source)
            self.assertNotIn("project_google_sheet:", source)

        for source in (intake, continuous):
            self.assertIn("STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION", source)
            self.assertIn("explicit absorption authorization", source)

        self.assertIn("REPOSITORY_PRIMARY_CANON", decisions)
        self.assertIn("HUMAN_GDD_PDF_DERIVED_VIEW", decisions)
        self.assertNotIn("구성된 Sheet 행을 APPROVED_PENDING_MERGE로 기록·재조회", grill_policy)
        self.assertNotIn("Decision ID·Branch Commit·정본 내용·Sheet 행 불일치", grill_policy)
        self.assertNotIn("Google Sheets의 마지막 Decision ID와 Commit SHA를 확인했다.", decisions)
        self.assertNotIn("Google Sheets의 마지막 Decision ID와 Commit을 확인했다.", grill_record)

    def test_p01_workspace_authority_surfaces_pass_canonical_scope_checker(self) -> None:
        paths = [
            "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md",
            "docs/operations/base-partitions/learning/P01_LEARNING_LOG.md",
            "skills/managing-game-project-operating-system/LEARNING_LOG.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md",
            "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md",
            "templates/project-operations/GRILL_ME_DECISION_RECORD.md",
            "templates/project-operations/README.md",
            "tests/test_gpt_codex_workflow_contract.py",
            "tests/test_notion_project_isolation_core_system_contract.py",
        ]
        result = subprocess.run(
            [
                sys.executable,
                "tools/check_base_partition_scope.py",
                "--part",
                "P01",
                "--files",
                *paths,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for path in paths:
            self.assertIn(f"PASS\tPART_OWNED\t{path}", result.stdout)
        self.assertNotIn("CONTROL_PLANE_WRITE_FORBIDDEN", result.stdout)
        self.assertNotIn("OUT_OF_PARTITION_WRITE", result.stdout)

    def test_permanent_base_v9_suite_runs_this_contract(self) -> None:
        workflow = V9_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tests.test_notion_project_isolation_core_system_contract", workflow)


if __name__ == "__main__":
    unittest.main()
