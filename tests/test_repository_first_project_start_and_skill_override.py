from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class RepositoryFirstProjectStartAndSkillOverrideTests(unittest.TestCase):
    def test_project_agents_template_uses_repository_first_authority(self) -> None:
        agents = text("templates/AGENTS.project.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "PDF_ONLY_USER_DOWNLOAD",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "EXACT_REPOSITORY_COMMIT",
            "GPT_VISUAL_REQUEST",
            "POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP",
            "NOTION_UNIQUE_CANON_COUNT = 0",
            "CODEX_NOTION_DEPENDENCY_COUNT = 0",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
        ):
            self.assertIn(token, agents)
        self.assertIn(
            "신규 Notion page/database/write/upload/sync/readback은 기본 workspace, 승인 Gate, Codex 인계 또는 완료 조건이 아니다",
            agents,
        )
        self.assertIn("LEGACY_DISCOVERY_ONLY", agents)
        self.assertNotIn("## DOMAIN_SPLIT_CANON", agents)
        self.assertNotIn("사람용 비교·시각 표면은 Notion", agents)
        self.assertNotIn("프로젝트 고유 결정·수치·구현 상태를 올바른 Notion/repository owner", agents)

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

    def test_confirmed_decision_template_syncs_repository_first(self) -> None:
        decisions = text("templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "COMPATIBILITY_ONLY",
            "repository_readback",
            "consumer_readback",
            "STALE_DERIVED_VIEW",
            "APPROVED_PENDING_MERGE",
            "SYNCED_TO_MAIN",
            "LEGACY_DISCOVERY_ONLY",
        ):
            self.assertIn(token, decisions)
        self.assertIn("신규 Notion page/database/write/upload/sync/readback은 승인 Decision 완료 조건이 아니다", decisions)
        self.assertIn("Notion을 현재 Decision write destination이나 완료 조건으로 복원하지 않는다", decisions)
        self.assertNotIn("프로젝트 사람용 결정이 바뀌면 정확한 Project relation의 Notion record를 갱신", decisions)
        self.assertNotIn("적용 가능한 Notion 사람용 record", decisions)
        self.assertNotIn("적용 가능한 Notion Project record 재조회", decisions)

    def test_grill_record_persists_decision_without_notion_write_gate(self) -> None:
        grill = text("templates/project-operations/GRILL_ME_DECISION_RECORD.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "COMPATIBILITY_ONLY",
            "repository_readback",
            "consumer_readback",
            "STALE_DERIVED_VIEW",
            "APPROVED_PENDING_MERGE",
            "SYNCED_TO_MAIN",
            "LEGACY_DISCOVERY_ONLY",
        ):
            self.assertIn(token, grill)
        self.assertIn("신규 Notion record 작성·갱신·readback은 기본 Decision sync 단계가 아니다", grill)
        self.assertIn("current Decision write destination이나 완료 Gate가 아니다", grill)
        self.assertNotIn("적용 가능한 Notion 사람용 record 반영", grill)
        self.assertNotIn("main readback + 적용 가능한 Notion readback", grill)
        self.assertNotIn("적용 가능한 Project Notion record를 갱신했다", grill)

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

    def test_planning_design_visual_and_engine_policies_are_partially_superseded(self) -> None:
        data = json.loads(
            text("docs/operations/REPOSITORY_FIRST_WORKSPACE_SUPERSESSION_MAP.json")
        )
        by_path = {entry["path"]: entry for entry in data["entries"]}

        expectations = {
            "skills/managing-design-documents/SKILL.md": (
                "content-modeling, UX-flow and data-owner checks",
                "Notion Project Home as the mandatory human-facing publishing destination",
                "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            ),
            "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md": (
                "one-question Grill Me discipline",
                "NOTION_HUMAN_FACING_CANON as required Decision destination",
                "repository CURRENT_CONFIRMED_DECISIONS and domain-owner update",
            ),
            "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md": (
                "planning sequence and evidence tiers",
                "NOTION_HUMAN_FACING_CANON as the default planning surface",
                "REPOSITORY_PRIMARY_PROJECT_CANON baseline recovery",
            ),
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md": (
                "explicit image-request approval gate",
                "Notion attachment or Asset record as implementation readiness",
                "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            ),
            "docs/VISUAL_COLLABORATION_TOOL_POLICY.md": (
                "intermediate visual checkpoint state semantics",
                "NOTION_DEFAULT_PROJECT_WORKSPACE as the current default surface",
                "HUMAN_GDD_PDF_DERIVED_VIEW",
            ),
            "docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md": (
                "stable engine baseline and no automatic latest following",
                "NOTION_HUMAN_FACING_CANON token as the current human authority",
                "REPOSITORY_PRIMARY_PROJECT_CANON",
            ),
        }

        for path, (retained, superseded, replacement) in expectations.items():
            entry = by_path[path]
            self.assertEqual("PARTIAL_SUPERSESSION", entry["status"])
            self.assertIn(retained, entry["retained_use"])
            self.assertIn(superseded, entry["superseded"])
            self.assertIn(replacement, entry["replacement"])

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
