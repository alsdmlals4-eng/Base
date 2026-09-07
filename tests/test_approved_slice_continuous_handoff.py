"""Documentation regressions, not proof of agent execution or Godot runtime."""
from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md"
START = "## 8A. 승인 Slice 연속 실행 인계"
END = "## 9. 선택적 Codex Godot technical preflight"


class ApprovedSliceContinuousHandoffTests(unittest.TestCase):
    def section(self) -> str:
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertEqual(text.count(START), 1, "continuous slice instruction must have one active owner section")
        self.assertEqual(text.count(END), 1)
        start, end = text.index(START), text.index(END)
        self.assertLess(start, end)
        return text[start:end]

    def assert_terms(self, *terms: str) -> None:
        section = self.section()
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, section)

    def test_approval_is_slice_bound_not_permission_to_expand(self) -> None:
        self.assert_terms(
            "PLAY_MEANINGFUL_WORK_SLICE", "approval reference",
            "BLUEPRINT_PASS_2_FINAL", "explicit_non_scope",
            "같은 승인 범위의 기술적 교정에는 routine 재승인을 요구하지 않는다.",
            "새 Goal·범위·비용·권한을 자동 승인하지 않는다.",
        )

    def test_existing_template_and_fields_are_the_consumer(self) -> None:
        self.assert_terms(
            "templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md",
            "acceptance_criteria", "review_evidence_expected", "required_runtime_or_play_checks",
            "repository_sources", "asset_audio_dependencies", "codex_result",
            "새 필수 Schema나 별도 진행표를 만들지 않는다.",
        )

    def test_run_and_reproduction_routes_come_from_actual_project(self) -> None:
        self.assert_terms(
            "working directory", "project.godot", "engine/version",
            "실제 명령 또는 기존 script 경로", "scenario/seed",
            "입력 → 상태 변화 → 화면·소리 → 결과", "exact revision",
            "없는 명령·도구·실행 결과를 만들어 적지 않는다.",
        )

    def test_journey_coverage_does_not_invent_game_features(self) -> None:
        self.assert_terms(
            "시작 → 선택·행동 → 결과 → 다음 행동",
            "실패·재시작·저장/불러오기는 해당 Slice에 적용되는 경우만",
            "새 화면·기능을 검증 명목으로 추가하지 않는다.",
        )

    def test_loop_rechecks_behavior_and_preserves_acceptance(self) -> None:
        self.assert_terms(
            "baseline smoke", "최소 end-to-end 구현", "실제 입력·상태·캡처 확인",
            "실패 재현 → 범위 안 교정 → 영향받는 회귀검사", "READY_FOR_GPT_REVIEW",
            "완료를 위해 acceptance나 테스트의 기대 결과를 낮추지 않는다.",
        )

    def test_existing_recovery_owner_bounds_execution(self) -> None:
        self.assert_terms(
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md",
            "recover → local defer → independent ready work",
            "현재 계약의 실행 상한·quota·중단 조건", "반복 실패·개선 정체",
            "상한 미확인은 무제한 실행 허가가 아니다.",
        )

    def test_stronger_global_stop_is_not_overridden_by_local_defer(self) -> None:
        self.assert_terms("최신 사용자 지시·AGENTS가 명시한 전역 중단 조건은 우선한다.")

    def test_checkpoint_prevents_blind_replay_of_side_effects(self) -> None:
        self.assert_terms(
            "checkpoint", "commit·PR·외부 쓰기를 무조건 재시도하지 않는다.",
            "current SHA·dirty state·PR ownership readback", "미완료 단계만 재개",
            "다른 open/draft/ready PR은 read-only",
        )

    def test_visual_and_final_review_authorities_are_preserved(self) -> None:
        self.assert_terms(
            "GPT_VISUAL_REQUEST", "CHANGE_PROPOSAL", "GPT 최종 검수",
            "승인 자산을 임의 교체하지 않는다.", "사용자 승인이나 출시 PASS가 아니다.",
        )

    def test_not_run_and_not_measured_are_not_success(self) -> None:
        self.assert_terms(
            "NOT_RUN", "NOT_MEASURED", "BLOCKED_UNVERIFIED",
            "headless 통과를 화면·조작 검증 PASS로 바꾸지 않는다.",
            "문서 회귀검사는 agent 실행 강제·프로젝트 채택·Godot runtime의 증거가 아니다.",
        )

    def test_pilot_uses_comparable_observations_not_promised_speed(self) -> None:
        self.assert_terms(
            "첫 플레이 가능 결과까지의 시간", "사용자 재전달·재지시 횟수",
            "정당한 핵심 결정 요청", "검수 결함·회귀·재작업",
            "같은 범위·엔진·자산·완료 기준", "측정 전 생산성 향상을 단정하지 않는다.",
        )

    def test_no_new_or_retired_orchestrator_is_implied(self) -> None:
        self.assert_terms(
            "GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED", "새 daemon·scheduler·유료 API",
            "재활성화하거나 도입하지 않는다.", "백그라운드 실행을 보장하지 않는다.",
            "openai.com/index/introducing-the-codex-app/",
            "anthropic.com/engineering/effective-harnesses-for-long-running-agents",
            "docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html",
        )


if __name__ == "__main__":
    unittest.main()
