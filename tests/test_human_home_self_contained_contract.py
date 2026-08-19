from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_OS = ROOT / "skills" / "managing-game-project-operating-system" / "SKILL.md"
AUTHORITY = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
BASE_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"


class HumanHomeSelfContainedContractTests(unittest.TestCase):
    def test_project_home_is_self_contained_before_drilldown(self) -> None:
        text = PROJECT_OS.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        for term in (
            "프로젝트 한 줄 정의",
            "핵심 플레이어/사용자 가치",
            "현재 확정 방향",
            "Core Loop",
            "핵심 시스템",
            "UX/UI/Visual",
            "현재 구현상태",
            "검증상태",
            "현재 blocker",
            "다음 작업",
            "최근 중요한 결정",
            "주요 위험",
            "revisit condition",
        ):
            self.assertIn(term, text)
        self.assertIn("하위 페이지", text)
        self.assertIn("drilldown", text)

    def test_workspace_authority_declares_self_contained_human_home(self) -> None:
        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))
        self.assertEqual(
            "HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN",
            contract["human_home_policy"],
        )
        required = set(contract["human_home_required_sections"])
        for section in (
            "PROJECT_DEFINITION_AND_VALUE",
            "CORE_LOOP_AND_FLOW",
            "CORE_SYSTEMS",
            "UX_UI_VISUAL_DIRECTION",
            "IMPLEMENTATION_STATUS",
            "VALIDATION_EVIDENCE_CEILING",
            "BLOCKERS_AND_NEXT_WORK",
            "IMPORTANT_DECISIONS",
            "RISKS_AND_REVISIT_CONDITIONS",
        ):
            self.assertIn(section, required)

    def test_base_home_contract_is_self_contained_for_learning(self) -> None:
        text = BASE_MODEL.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        for term in (
            "Skill 목적",
            "호출 조건",
            "입력",
            "처리",
            "출력",
            "기대효과",
            "Module",
            "없으면",
            "P01~P09",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
