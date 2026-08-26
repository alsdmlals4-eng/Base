from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class FreshReadProjectBootstrapContractTests(unittest.TestCase):
    def test_handoff_method_defines_github_notion_only_reconstruction_gate(self) -> None:
        text = read("docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md")
        for term in (
            "FRESH_READ_PROJECT_BOOTSTRAP",
            "PROJECT_GITHUB_NOTION_ONLY",
            "PAST_CONVERSATION_NOT_REQUIRED",
            "CONTEXT_DRIFT_RECHECK_REQUIRED",
            "project_identity",
            "current_goal",
            "current_quality_and_stage",
            "protected_scope",
            "next_safe_action",
            "evidence_ceiling",
            "instruction_surface",
        ):
            self.assertIn(term, text)

    def test_existing_handoff_skill_resume_consumes_fresh_read_bootstrap(self) -> None:
        text = read("skills/maintaining-project-context-and-handoff/SKILL.md")
        self.assertIn("FRESH_READ_PROJECT_BOOTSTRAP", text)
        self.assertIn("PROJECT_GITHUB_NOTION_ONLY", text)
        self.assertIn("resume", text)
        self.assertIn("과거 대화", text)
        self.assertIn("next_safe_action", text)
        self.assertIn("evidence_ceiling", text)

    def test_project_start_here_is_a_cold_start_router_not_second_canon(self) -> None:
        text = read("templates/project-operations/PROJECT_START_HERE.md")
        for term in (
            "Fresh-Read Bootstrap",
            "PAST_CONVERSATION_NOT_REQUIRED",
            "GitHub + Notion",
            "현재 품질·단계",
            "보호 범위",
            "다음 안전 작업",
            "Evidence ceiling",
        ):
            self.assertIn(term, text)
        self.assertIn("두 번째 활성 현재 상태 원본", text)

    def test_notion_human_home_contract_supports_fresh_read_reconstruction(self) -> None:
        text = read("docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md")
        for term in (
            "FRESH_READ_HOME_BOOTSTRAP_REQUIRED",
            "PROJECT_GITHUB_NOTION_ONLY",
            "current quality",
            "protected scope",
            "next safe action",
            "evidence ceiling",
        ):
            self.assertIn(term, text)

    def test_portfolio_audit_receipt_covers_all_ten_human_homes(self) -> None:
        text = read("docs/operations/notion-project-ia/2026-08-26_FRESH_READ_PORTFOLIO_AUDIT.md")
        for project in (
            "COC-Fiction",
            "괴이기록국",
            "오멘워드",
            "GRIMOIRE",
            "닌자 서바이벌",
            "블랙스미스",
            "십보강호",
            "Tetris",
            "Switchy Express",
            "마이 리틀 보트",
        ):
            self.assertIn(project, text)
        for term in (
            "LIVE_NOTION_READBACK_2026_08_26",
            "PHYSICAL_IA_REUSE_NO_REMIGRATION",
            "FRESH_READ_RECONSTRUCTION_AUDITED",
            "Implementation Reality Gate",
            "HUMAN_USABILITY_NOT_RUN",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
