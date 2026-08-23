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

    def test_project_home_is_rich_not_minimal_and_exposes_human_core_data(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for term in (
            "PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED",
            "PROJECT_SPECIFIC_CORE_DATA",
            "AI_INTERPRETATION_FOR_USER_CORRECTION",
            "HUMAN_EDIT_GUIDE_REQUIRED",
            "FLOW_MAP",
            "CORE_SYSTEMS",
            "VISUAL_ASSET_ANCHORS",
        ):
            self.assertIn(term, text)

    def test_ai_interpretation_is_not_operational_metadata(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        self.assertIn("AI_INTERPRETATION_FOR_USER_CORRECTION", text)
        self.assertIn("AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED", text)
        for required_phrase in (
            "raw PR/commit/CI history",
            "Prompt / AI Note / Asset ID / Hash / Implementation Path",
        ):
            self.assertIn(required_phrase, text)

    def test_dashboard_skill_builds_project_specific_rich_home(self) -> None:
        text = DASHBOARD_SKILL.read_text(encoding="utf-8")
        for term in (
            "PROJECT_SPECIFIC_CORE_DATA",
            "AI_INTERPRETATION_FOR_USER_CORRECTION",
            "HUMAN_EDIT_GUIDE_REQUIRED",
            "NO_UNIVERSAL_GAME_DATA_TEMPLATE",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
