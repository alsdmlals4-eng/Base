from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FULL = ROOT / "tests/test_full_adversarial_loop_semantics.py"
FULL.write_text(
    r'''from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
AGENTS = ROOT / "AGENTS.md"


class FullAdversarialLoopSemanticsTests(unittest.TestCase):
    def authoritative_text(self) -> str:
        return POLICY.read_text(encoding="utf-8") + "\n" + OPERATING_MODEL.read_text(encoding="utf-8")

    def test_base_still_requires_minimum_five_full_loops(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", agents)
        self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", agents)

    def test_full_loop_is_not_a_review_lens(self) -> None:
        text = self.authoritative_text()
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("관점 하나", text)
        self.assertIn("최소 5", text)

    def test_each_counted_loop_repeats_the_complete_lifecycle(self) -> None:
        text = self.authoritative_text()
        for term in (
            "CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK",
            "MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK",
            "FULL-SCOPE ATTACK",
            "VALIDATE CRITIQUE",
            "FIX / REFINE VERIFIED FINDINGS",
            "EXECUTION / REGRESSION / REFERENCE VERIFICATION",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "RE-ATTACK THE WHOLE RESULTING STATE",
        ):
            self.assertIn(term, text)

    def test_lens_split_examples_are_explicitly_rejected(self) -> None:
        text = self.authoritative_text()
        self.assertIn("Loop 1=scope", text)
        self.assertIn("Loop 2=UX", text)
        self.assertIn("Loop 3=CI", text)
        self.assertIn("계수하지 않는다", text)


if __name__ == "__main__":
    unittest.main()
''',
    encoding="utf-8",
    newline="\n",
)

HOME = ROOT / "tests/test_human_home_self_contained_contract.py"
HOME.write_text(
    r'''from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "HUMAN_HOME_SELF_CONTAINED_POLICY.md"
NOTION_CONTRACT = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
BASE_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"


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


if __name__ == "__main__":
    unittest.main()
''',
    encoding="utf-8",
    newline="\n",
)

print("PR530_ISOLATION_TEST_STRINGS_FIXED")
