from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class FreshReadProjectBootstrapContractTests(unittest.TestCase):
    def test_companion_reference_defines_github_notion_reconstruction_gate(self) -> None:
        path = ROOT / "skills/maintaining-project-context-and-handoff/references/fresh-read-project-bootstrap.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
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
            "HUMAN_USABILITY_NOT_RUN",
        ):
            self.assertIn(term, text)

    def test_existing_handoff_template_routes_to_companion_without_second_canon(self) -> None:
        text = read("templates/project-operations/HANDOFF.md")
        self.assertIn("fresh-read-project-bootstrap.md", text)
        self.assertIn("Fresh-chat resumability test", text)
        self.assertIn("CONTEXT_DRIFT_RECHECK_REQUIRED", text)
        self.assertIn("next_safe_action", text)

    def test_existing_owners_keep_cold_start_and_human_home_semantics(self) -> None:
        method = read("docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md")
        start = read("templates/project-operations/PROJECT_START_HERE.md")
        notion = read("docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md")
        self.assertIn("새 채팅", method)
        self.assertIn("GitHub", method)
        self.assertIn("Notion", method)
        self.assertIn("콜드 스타트", start)
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", notion)
        self.assertIn("evidence ceiling", notion)

    def test_portfolio_audit_receipt_covers_all_ten_human_homes(self) -> None:
        text = read("docs/operations/notion-project-ia/2026-08-26_FRESH_READ_PORTFOLIO_AUDIT.md")
        for project in (
            "COC-Fiction", "괴이기록국", "오멘워드", "GRIMOIRE", "닌자 서바이벌",
            "블랙스미스", "십보강호", "Tetris", "Switchy Express", "마이 리틀 보트",
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
