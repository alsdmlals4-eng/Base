from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "skills/managing-project-intake-and-work-contract/references/task-recovery-protocol.md"
CONTINUOUS = ROOT / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"


class TaskRecoveryProtocolTests(unittest.TestCase):
    def test_protocol_exists_and_separates_retry_from_resume(self) -> None:
        self.assertTrue(PROTOCOL.is_file(), "task recovery protocol must exist")
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "TASK_RECOVERY_PROTOCOL",
            "RETRY",
            "RESUME",
            "CHECKPOINT",
            "현재 상태 재확인",
            "완료된 작업",
            "중복 실행",
        ):
            self.assertIn(term, text)

    def test_transient_retry_is_bounded_and_stall_does_not_blindly_replay(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "3초",
            "10초",
            "30초",
            "최대 3회",
            "timeout",
            "network",
            "stalled",
            "자동 재전송 금지",
        ):
            self.assertIn(term, text)

    def test_side_effecting_work_requires_readback_before_resume(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "파일 수정",
            "commit",
            "PR",
            "merge",
            "메일",
            "외부 전송",
            "readback",
            "idempotency",
        ):
            self.assertIn(term, text)
        self.assertIn("이미 완료된 단계는 다시 실행하지 않는다", text)

    def test_recovery_preserves_existing_authority_and_human_gates(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "승인된 작업 계약",
            "USER_DECISION_REQUIRED",
            "HIGH_RISK_CONFIRMATION_REQUIRED",
            "권위",
            "범위 확대",
            "자동 승인하지 않는다",
        ):
            self.assertIn(term, text)

    def test_external_watchdog_is_signal_only_not_new_execution_authority(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for term in (
            "WATCHDOG_SIGNAL",
            "RETRYING",
            "RECOVERY_REQUIRED",
            "RECOVERED",
            "FAILED_TERMINAL",
            "실행 권한을 새로 부여하지 않는다",
        ):
            self.assertIn(term, text)

    def test_continuous_work_links_task_recovery_protocol_without_new_mode(self) -> None:
        text = CONTINUOUS.read_text(encoding="utf-8")
        self.assertIn("task-recovery-protocol.md", text)
        self.assertIn("TASK_RECOVERY_PROTOCOL", text)
        self.assertIn("새로운 Skill이나 Work Mode가 아니다", text)


if __name__ == "__main__":
    unittest.main()
