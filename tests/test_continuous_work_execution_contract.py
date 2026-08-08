from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"


class ContinuousWorkExecutionContractTests(unittest.TestCase):
    def test_continuous_work_reference_exists_and_defines_bounded_loop(self) -> None:
        self.assertTrue(REFERENCE.is_file(), "continuous work execution reference must exist")
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "[연속작업] 진행해",
            "CONTINUOUS_WORK_ACTIVE",
            "CONTINUOUS_WORK_INACTIVE",
            "승인된 작업 계약",
            "attack → validate-critique",
            "regression-recheck",
            "USER_DECISION_REQUIRED",
            "BLOCKED_UNVERIFIED",
            "백그라운드",
            "종료 조건",
        ):
            self.assertIn(term, text)

    def test_trigger_is_opt_in_and_does_not_replace_work_modes(self) -> None:
        self.assertTrue(REFERENCE.is_file(), "continuous work execution reference must exist")
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "트리거가 없는",
            "CONTINUOUS_WORK_INACTIVE",
            "PLAN / BUILD / REVIEW",
            "Work Mode를 대체하지 않는다",
            "현재 승인된 작업 계약",
        ):
            self.assertIn(term, text)

    def test_auto_approval_stops_at_user_decisions_scope_expansion_and_high_risk_actions(self) -> None:
        self.assertTrue(REFERENCE.is_file(), "continuous work execution reference must exist")
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "USER_DECISION_REQUIRED",
            "BLOCKED_UNVERIFIED",
            "범위 확대",
            "결제",
            "계정 삭제",
            "보안·권한",
            "사용자가 중지",
        ):
            self.assertIn(term, text)

    def test_canonical_surfaces_link_continuous_work_contract(self) -> None:
        surfaces = (
            ROOT / "AGENTS.md",
            ROOT / "docs/OPERATING_MODEL.md",
            ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md",
            ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md",
        )
        for path in surfaces:
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                self.assertIn("[연속작업] 진행해", text)
                self.assertIn("continuous-work-execution.md", text)

    def test_continuous_work_is_in_run_orchestration_not_background_execution(self) -> None:
        self.assertTrue(REFERENCE.is_file(), "continuous work execution reference must exist")
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "현재 응답",
            "실행 세션",
            "scheduler",
            "webhook",
            "백그라운드",
            "자동 메시지 전달",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
