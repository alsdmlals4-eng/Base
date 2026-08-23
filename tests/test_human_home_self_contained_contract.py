from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "HUMAN_HOME_SELF_CONTAINED_POLICY.md"
NOTION_CONTRACT = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
BASE_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
DASHBOARD_SKILL = ROOT / "skills" / "building-project-visual-dashboards" / "SKILL.md"


class HumanHomeSelfContainedContractTests(unittest.TestCase):
    def test_project_home_is_self_contained_before_drilldown(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        for term in (
            "프로젝트 한 줄 정의", "핵심 플레이어/사용자 가치", "현재 확정 방향",
            "Core Loop", "핵심 시스템", "UX/UI/Visual", "현재 구현상태", "검증상태",
            "현재 blocker", "다음 작업", "최근 중요한 결정", "주요 위험", "revisit condition",
        ):
            self.assertIn(term, text)
        self.assertIn("drilldown", text)

    def test_notion_contract_routes_to_self_contained_home_policy(self) -> None:
        text = NOTION_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        self.assertIn("docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md", text)

    def test_base_home_contract_is_self_contained_for_learning(self) -> None:
        text = POLICY.read_text(encoding="utf-8") + "\n" + BASE_MODEL.read_text(encoding="utf-8")
        for term in (
            "Skill 목적", "호출 조건", "입력", "처리", "출력", "기대효과",
            "Module", "없으면", "P01~P09",
        ):
            self.assertIn(term, text)

    def test_human_home_allows_rich_project_specific_information_without_ai_metadata_dump(self) -> None:
        text = POLICY.read_text(encoding="utf-8") + "\n" + DASHBOARD_SKILL.read_text(encoding="utf-8")
        for term in (
            "HUMAN_HOME_INFORMATION_RICHNESS_IS_ALLOWED",
            "PROJECT_SPECIFIC_CORE_DATA_INVENTORY",
            "AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW",
            "HOW_TO_CORRECT_AI_UNDERSTANDING",
            "DO_NOT_FORCE_UNIVERSAL_DATA_CATEGORIES",
        ):
            self.assertIn(term, text)
        for human_example in (
            "예산",
            "경제",
            "상대",
            "몬스터",
            "아이템",
            "성장",
            "Route",
        ):
            self.assertIn(human_example, text)

    def test_ai_interpretation_is_human_design_explanation_not_operational_metadata(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        self.assertIn("AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW", text)
        self.assertIn("HUMAN_HOME_EXCLUDES_AI_SYSTEM_METADATA", text)
        self.assertIn("Prompt", text)
        self.assertIn("Repo Main SHA", text)
        self.assertIn("Implementation Path", text)


if __name__ == "__main__":
    unittest.main()
