"""Guard documentation, not live permissions or Godot runtime behavior."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md"


class SharedDirectCallContractTests(unittest.TestCase):
    def setUp(self) -> None:
        source = OWNER.read_text(encoding="utf-8")
        self.section = source.partition("### UI·직접 호출의 동일 규칙 경계")[2].partition("\n### Godot 연결")[0]

    def require(self, *clauses: str) -> None:
        for clause in clauses:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.section)

    def test_shared_entrypoint_does_not_create_a_parallel_agent_rule_engine(self) -> None:
        self.require(
            "UI·CLI·API·MCP·자동 테스트는 같은 기능의 공개 진입점과 규칙을 재사용한다.",
            "AI 전용 상태·규칙 복제본을 만들지 않는다.",
            "필요 기능 탐색 → 선택한 계약 확인 → 허용된 실행 → 결과 readback",
        )

    def test_executor_guards_are_not_ui_or_annotation_security(self) -> None:
        self.require(
            "입력 ID·타입·현재 상태·대상 소유권과 적용되는 권한·승인 범위는 실제 실행 경계에서 검사한다.",
            "비활성 버튼·프롬프트·MCP readOnlyHint는 실행 권한 검사나 격리를 대신하지 않는다.",
            "로컬 상태기계의 유효성 검사는 원격 인증·인가가 구현됐다는 증거가 아니다.",
        )

    def test_rejection_readback_and_retry_contracts_preserve_owned_state(self) -> None:
        self.require(
            "거절된 호출은 소유한 도메인 상태를 변경하지 않는다.",
            "오류·감사 기록처럼 허용된 진단 부작용은 별도로 명시한다.",
            "읽기 결과를 수정해 원본 상태를 우회 변경할 수 없게 한다.",
            "중복·재시도·취소는 기능별 기존 계약을 따르며 모든 명령을 무조건 멱등으로 바꾸지 않는다.",
        )

    def test_existing_reference_and_evidence_ceiling_stay_connected(self) -> None:
        self.require(
            "examples/godot-narrative-dialogue-flow/tests/test_dialogue_flow_runtime.gd",
            "정상 경로와 미시작·잘못된 ID·타 구간 ID·조기 호출·종료 후 재호출",
            "헤드리스 규칙 PASS는 렌더링·입력 장치·UX·사용자 승인 PASS가 아니다.",
            "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
            "새 MCP·범용 dispatcher·Registry를 기본 산출물로 추가하지 않는다.",
        )


if __name__ == "__main__":
    unittest.main()
