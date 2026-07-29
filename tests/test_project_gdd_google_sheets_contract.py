from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsContractTests(unittest.TestCase):
    def test_policy_defines_gdd_workspace_and_authority(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "SHEET_GITHUB_CONFLICT",
            "GitHub 정본을 대체하지 않는다",
            "AI는 GitHub와 Google Sheets를 함께",
        ):
            self.assertIn(term, policy)

    def test_policy_and_templates_cover_visual_living_quantified_gdd(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        workbook = read(
            "templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md"
        )

        for section in (
            "1. 문서 개요",
            "2. 핵심 게임플레이",
            "3. 게임 시스템",
            "4. 스토리 및 세계관",
            "5. 아트 및 사운드",
            "6. 기술 및 로드맵",
        ):
            self.assertIn(section, policy)

        for term in (
            "흐름도",
            "관계도",
            "와이어프레임",
            "마지막 수정 시각",
        ):
            self.assertIn(term, policy)

        for term in (
            "단위",
            "초기 시험값",
            "조정 범위",
            "검증 상태",
        ):
            self.assertIn(term, policy)

        self.assertIn("05_GDD_요약", tabs)
        self.assertIn("15_조작_게임규칙", tabs)
        self.assertIn("USER_FACING_GDD_WORKSPACE", workbook)

    def test_entrypoints_report_skill_counts_and_optional_dashboard(self) -> None:
        for path in (
            "README.md",
            "AGENTS.md",
            "docs/OPERATING_MODEL.md",
            "docs/DOCUMENTATION_MAP.md",
        ):
            text = read(path)
            self.assertIn("전체 ACTIVE Skill", text, path)
            self.assertIn("27개", text, path)
            self.assertIn("핵심 통합", text, path)
            self.assertIn("13개", text, path)
            self.assertIn("지원", text, path)
            self.assertIn("14개", text, path)

        for path in ("README.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("HTML 대시보드", text, path)
            self.assertIn("명시", text, path)
            self.assertIn("프로젝트 GDD Google Sheets", text, path)

    def test_existing_skills_consume_project_gdd_sheet(self) -> None:
        for path in (
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
        ):
            text = read(path)
            self.assertIn("PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", text, path)
            self.assertIn("PROPOSED_SHEET_CHANGE", text, path)
            self.assertIn("USER_FACING_GDD_WORKSPACE", text, path)

    def test_sync_policy_preserves_sheet_edits_as_proposals(self) -> None:
        sync_policy = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for term in (
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "GITHUB_UPDATE_PENDING_SHEET",
            "SHEET_UPDATE_PENDING_GITHUB",
            "SHEET_GITHUB_CONFLICT",
        ):
            self.assertIn(term, sync_policy)

    def test_planning_policy_routes_gdd_sheet_contract(self) -> None:
        planning = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in (
            "PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
            "USER_FACING_GDD_WORKSPACE",
            "시각화 우선",
            "수치화",
            "PROPOSED_SHEET_CHANGE",
        ):
            self.assertIn(term, planning)


if __name__ == "__main__":
    unittest.main()
