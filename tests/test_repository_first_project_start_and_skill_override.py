from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class RepositoryFirstProjectStartAndSkillOverrideTests(unittest.TestCase):
    def test_project_start_template_uses_repository_first_cold_start(self) -> None:
        start = text("templates/project-operations/PROJECT_START_HERE.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "PDF_ONLY_USER_DOWNLOAD",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "NOTION_UNIQUE_CANON_COUNT",
            "CODEX_NOTION_DEPENDENCY_COUNT",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT",
        ):
            self.assertIn(token, start)
        self.assertIn("신규 Notion page/database/write/upload/sync/readback은 기본 작업 또는 완료 조건이 아니다", start)
        self.assertIn("과거 `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`, `DOMAIN_SPLIT_CANON`은 `LEGACY_DISCOVERY_ONLY` alias", start)
        self.assertNotIn("POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP", start)
        self.assertNotIn("최근 postmerge GitHub·Notion readback", start)
        self.assertNotIn("적용 가능한 Notion current-state는 GitHub 증거 뒤에 갱신", start)

    def test_active_skill_workspace_clauses_are_partially_superseded(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_WORKSPACE_SUPERSESSION_MAP.json")
        )
        by_path = {entry["path"]: entry for entry in data["entries"]}

        operating_system = by_path[
            "skills/managing-game-project-operating-system/SKILL.md"
        ]
        self.assertEqual("PARTIAL_SUPERSESSION", operating_system["status"])
        self.assertIn(
            "install, audit, reconcile-legacy, migrate and verify modes",
            operating_system["retained_use"],
        )
        self.assertIn(
            "NOTION_DEFAULT_PROJECT_WORKSPACE as default install destination",
            operating_system["superseded"],
        )
        self.assertIn(
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            operating_system["replacement"],
        )

        intake = by_path["skills/managing-project-intake-and-work-contract/SKILL.md"]
        self.assertEqual("PARTIAL_SUPERSESSION", intake["status"])
        self.assertIn("reuse-first preflight", intake["retained_use"])
        self.assertIn(
            "APPROVED_DECISION_GITHUB_NOTION_SYNC_DURING_WORK",
            intake["superseded"],
        )
        self.assertIn(
            "docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json",
            intake["replacement"],
        )

    def test_long_horizon_and_decision_sync_keep_non_workspace_safety(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_WORKSPACE_SUPERSESSION_MAP.json")
        )
        by_path = {entry["path"]: entry for entry in data["entries"]}

        long_horizon = by_path["docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"]
        self.assertIn("long-running task continuity", long_horizon["retained_use"])
        self.assertEqual(
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
            long_horizon["replacement"],
        )

        decisions = by_path["docs/CONFIRMED_DECISION_SYNC_POLICY.md"]
        self.assertIn("stable decision identity", decisions["retained_use"])
        self.assertIn(
            "Notion human-facing write as a mandatory approved-decision destination",
            decisions["superseded"],
        )
        self.assertIn(
            "repository confirmed-decision owner",
            decisions["replacement"],
        )

    def test_legacy_tests_do_not_own_current_workspace_default(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_WORKSPACE_SUPERSESSION_MAP.json")
        )
        by_path = {entry["path"]: entry for entry in data["entries"]}
        for path in (
            "tests/test_notion_project_workspace_contract.py",
            "tests/test_gpt_codex_workflow_contract.py",
            "tests/test_postmerge_github_notion_long_term_contract.py",
        ):
            self.assertIn("LEGACY", by_path[path]["status"])
            self.assertIn("current_default_proof", by_path[path])


if __name__ == "__main__":
    unittest.main()
