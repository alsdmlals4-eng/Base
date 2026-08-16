from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
TASK_RECOVERY = ROOT / "skills/managing-project-intake-and-work-contract/references/task-recovery-protocol.md"
SKILL = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
SYNC_PROTOCOL = ROOT / "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"


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

    def test_recoverable_blockers_do_not_immediately_stop_global_loop(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "RECOVERABLE_VERIFICATION_BLOCKER",
            "RECOVERABLE_EXECUTION_ROUTE_BLOCKER",
            "LOCAL_TASK_BLOCKER",
            "GLOBAL_TERMINAL_BLOCKER",
            "ready_tasks",
            "deferred_tasks",
            "completed_tasks",
            "recovery ladder",
        ):
            self.assertIn(term, text)
        self.assertIn("실행 가능한 독립 task", text)
        self.assertIn("전체 루프를 즉시 종료하지 않는다", text)

    def test_evidence_transport_failure_requeries_exact_head_before_blocking(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "EVIDENCE_TRANSPORT_INCOMPLETE",
            "tool-output truncation",
            "exact HEAD",
            "재조회",
            "동일 SHA",
            "workflow",
            "job",
        ):
            self.assertIn(term, text)
        self.assertIn("FAIL이 아니다", text)

    def test_approved_execution_method_does_not_create_new_user_decision(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "dedicated execution package",
            "10,000-seed",
            "실행 방법",
            "같은 승인 목표",
            "별도 사용자 승인",
        ):
            self.assertIn(term, text)
        self.assertIn("USER_DECISION_REQUIRED가 아니다", text)

    def test_current_session_tool_absence_uses_authorized_alternate_executor_or_defers_locally(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "현재 세션",
            "alternate executor",
            "DEFERRED_EXTERNAL_EXECUTOR",
            "HiGodot",
            "권위",
            "독립 작업",
        ):
            self.assertIn(term, text)
        self.assertIn("전체 실행 경로 부재", text)
        self.assertIn("우회", text)

    def test_continuous_work_consumes_inherited_merge_authority(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for term in (
            "APPROVED_ITEM_INHERITS_MERGE_AUTHORITY",
            "exact HEAD",
            "required checks",
            "unresolved thread 0",
            "별도 병합 승인",
        ):
            self.assertIn(term, text)
        self.assertIn("즉시 병합", text)

    def test_user_directed_work_uses_latest_main_copy_integration_without_touching_in_progress_prs(self) -> None:
        reference = REFERENCE.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        for text in (reference, skill):
            for term in (
                "USER_DIRECTED_PARALLEL_PR",
                "current completed main",
                "separate branch/PR",
                "same-goal",
                "in-progress PR",
                "BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16",
            ):
                self.assertIn(term, text)
        self.assertIn("do not modify/rebase/update", reference)
        self.assertIn("selective copy", reference)
        self.assertIn("superseded", reference)

    def test_overlap_uses_standing_copy_integration_and_material_absorption_merge_gate(self) -> None:
        reference = REFERENCE.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        sync = SYNC_PROTOCOL.read_text(encoding="utf-8")
        for text in (reference, skill):
            self.assertIn("PROVISIONAL_INTEGRATION", text)
            self.assertIn("synchronizing-local-and-github-state", text)
            self.assertIn("BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16", text)
        for term in (
            "owner PR branches",
            "semantic reconciliation",
            "selective copy",
            "absorbed_owner_deltas",
            "residual_owner_deltas",
        ):
            self.assertIn(term, sync)
        self.assertIn("material delta", reference)
        self.assertIn("owner PR이 열려 있다는 사실만으로", reference)
        self.assertNotIn("owner가 해결되기 전에는 merge하지 않는다", reference)
        self.assertNotIn("scheduled/periodic` repository-writing automation의 active-PR guard를 완화하지 않는다", reference)

    def test_unexpected_interruption_routes_to_task_recovery_protocol(self) -> None:
        self.assertTrue(TASK_RECOVERY.is_file(), "task recovery protocol must exist")
        continuous = REFERENCE.read_text(encoding="utf-8")
        recovery = TASK_RECOVERY.read_text(encoding="utf-8")
        for term in (
            "task-recovery-protocol.md",
            "TASK_RECOVERY_PROTOCOL",
            "새로운 Skill이나 Work Mode가 아니다",
        ):
            self.assertIn(term, continuous)
        for term in (
            "RETRY",
            "RESUME",
            "CHECKPOINT",
            "현재 상태 재확인",
            "이미 완료된 단계는 다시 실행하지 않는다",
            "자동 재전송 금지",
        ):
            self.assertIn(term, recovery)


if __name__ == "__main__":
    unittest.main()
