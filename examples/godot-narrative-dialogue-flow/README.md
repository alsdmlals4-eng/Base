# Godot Narrative Dialogue Flow Reference

이 예제는 `FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md`의 Scene → Beat → Dialogue/Choice 계약을 **Godot 4.7.1에서 실제로 실행하는 격리 reference fixture**다.

## 구성

```text
project.godot
main.tscn
src/
  dialogue_flow_model.gd
  dialogue_flow_session.gd
  main.gd
data/
  sample_dialogue.json
tests/
  test_dialogue_flow_runtime.gd
```

- `sample_dialogue.json`: 샘플 관계 데이터. Scene/Beat/Dialogue/Choice Stable ID와 `STAY_IN_SCENE | MOVE_SCENE | END`를 포함한다.
- `dialogue_flow_model.gd`: JSON 로드, Stable ID 인덱싱, 구조/전이 검증. 잘못된 관계는 fail-closed한다.
- `dialogue_flow_session.gd`: 현재 Beat/Line, 선택 대기, 전이, 종료를 관리하는 최소 런타임 상태기계다.
- `main.gd` + `main.tscn`: 샘플을 사람이 실행해 볼 수 있는 최소 UI다.

## 실제 프로젝트에 적용

1. 프로젝트의 확정 narrative/data source에서 동일한 JSON shape를 만든다.
2. `dialogue_flow_model.gd`와 `dialogue_flow_session.gd`를 프로젝트 책임 경로로 복사/흡수한다.
3. UI에서는 `current_line()`, `get_choices()`, `choose(choice_id)`만 소비하고 별도 분기 edge 목록을 만들지 않는다.
4. 실제 프로젝트 저작/씬 변경은 프로젝트의 HiGodot 권한 규칙을 따른다. 이 Base 예제의 실행 성공은 프로젝트 HiGodot authoring 증거를 대신하지 않는다.

## 로컬 실행

```bash
godot --path examples/godot-narrative-dialogue-flow
```

계약 테스트:

```bash
godot --headless \
  --path examples/godot-narrative-dialogue-flow \
  --script res://tests/test_dialogue_flow_runtime.gd
```

이 구현 검증에서는 고정된 Godot `4.7.1.stable.official.a13da4feb` archive와 SHA-256을 사용한 임시 branch harness로 실제 실행을 완료했다. 실행 ID와 결과는 `docs/knowledge/godot/evidence/2026-08-14-narrative-dialogue-runtime-sample.md`에 남긴다. 최종 Base에는 이 기능만을 위한 별도 상시 CI workflow를 추가하지 않고, 위 명령으로 동일한 runtime fixture를 재실행할 수 있게 유지한다.

## 현재 범위

포함: Stable ID, Scene/Beat 구조, line 진행, choice, same-scene continuity, scene move, end, invalid transition fail-closed.

제외: 조건식/변수, 세이브, 현지화, 보이스, 컷신, 실제 프로젝트 데이터 migration, HiGodot project authoring, 사람의 시각 UX 검증.

## 직접 호출 회귀 검증

공용 책임은 [기능별 코드·계약 모듈화](../../skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md)의 `UI·직접 호출의 동일 규칙 경계`를 따른다. 이 예제는 새 MCP나 AI 전용 규칙 엔진이 아니다. `src/main.gd`의 버튼 handler와 위 테스트는 같은 `session.choose(choice_id)`를 사용한다.

같은 테스트 명령이 기존 정상 전이와 잘못된 데이터 fixture에 더해 다음을 검사한다.

- 미시작·선택 대기 전 호출, 빈 ID·없는 ID·다른 Beat의 ID, 즉시 재호출·다음 Beat에서 이전 ID 사용·종료 후 재호출을 거절한다.
- 거절 결과의 요청 ID·오류·Beat·Scene·종료 상태를 실제 공개 getter의 readback과 비교한다. 도메인 상태는 보존하되 `get_last_error()`의 진단 갱신은 허용한다.
- 조회한 대사·선택 목록과 반환 event를 caller가 바꿔도 원본 상태를 우회 변경하지 못한다. 거절 이후 유효한 선택·장면 이동·END가 정상 진행되며 성공 시 이전 오류가 지워진다.

선택 가능 시점은 기존 규칙인 **마지막 대사가 현재 표시된 상태**를 유지한다. 모든 요청을 멱등으로 만들거나 종료 후 자동 재시작하지 않는다. `NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS`와 종료 코드 0을 함께 확인하며, 파싱 오류·timeout·종료 코드만으로 성공 처리하지 않는다.

`tests/test_shared_direct_call_contract.py`는 공용 문구의 누락을 막는 Python 문서 검사다. 위 Godot 테스트는 실제 참조 상태기계의 동작 검사다. 둘 다 원격 인증·인가, MCP read-only 권한, 실제 UI 버튼 입력·렌더링·시각 UX·프로젝트 채택을 증명하지 않는다. 이전 2026-08-14 실행 기록은 새 테스트 실행 증거가 아니며, 새 exact-source 실행과 한계는 이번 작업 receipt/PR에 따로 남긴다.
