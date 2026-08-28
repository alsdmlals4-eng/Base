from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"


class WorkMinimalRestartEntryContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required current owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_one_line_project_restart_is_a_sufficient_routing_input(self) -> None:
        router = self._read(ROUTER)
        for token in (
            "MINIMAL_PROJECT_RESTART_ONE_LINE_ENTRY",
            "BASE_AND_PROJECT_FRESH_READ_IS_ROUTING_INPUT",
            "NO_PROJECT_CHAT_INSTRUCTION_FILE_ATTACHMENT_REQUIRED",
            "CURRENT_BASE_ROUTER_AND_SPECIALIST_OWNERS_PROGRESSIVE_LOAD",
            "EXACT_PROJECT_IDENTITY_REQUIRED",
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
        ):
            self.assertIn(token, router)
        self.assertIn(
            "[프로젝트명] 작업 재개. Base 최신 completed main과 프로젝트 repository exact SHA·actual implementation을 fresh-read하고, 현재 5단계 위치를 복원한 뒤 다음 안전 작업부터 진행해.",
            router,
        )
        self.assertNotIn(
            "[프로젝트명] 작업 재개. Base 최신 main과 프로젝트 고유 GitHub·Notion·actual implementation을 fresh-read",
            router,
        )

    def test_one_line_entry_routes_the_full_current_automation_contract(self) -> None:
        router = self._read(ROUTER)
        starter = self._read(STARTER)
        for routed_owner in (
            "WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md",
        ):
            self.assertIn(routed_owner, router)
        for preserved_capability in (
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "INCIDENT_SOLUTION_LESSON_LOOP",
            "BASE_PROMOTION_DISPOSITION_REQUIRED",
            "DO_NOT_AUTO_ADVANCE_TO_NEXT_SLICE_BEFORE_USER_VALIDATION",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
        ):
            self.assertIn(preserved_capability, starter)

    def test_legacy_instruction_files_are_not_routine_inputs_but_unique_content_is_not_lost(self) -> None:
        router = self._read(ROUTER)
        for token in (
            "LEGACY_INSTRUCTION_ATTACHMENT_NOT_ROUTINE_INPUT",
            "LEGACY_INSTRUCTION_IS_DISCOVERY_ONLY_NOT_CURRENT_CANON",
            "UNMIGRATED_UNIQUE_LEGACY_INSTRUCTION_CONTENT_MUST_BE_RECONCILED",
            "NO_SILENT_DROP_OF_PROJECT_SPECIFIC_UNIQUE_RULES",
        ):
            self.assertIn(token, router)


if __name__ == "__main__":
    unittest.main()
