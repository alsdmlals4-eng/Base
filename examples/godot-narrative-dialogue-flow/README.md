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
  test_dialogue_ui_runtime.gd
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

## 실제 UI consumer 회귀 검증

`test_dialogue_ui_runtime.gd`는 복제 UI나 fake session 대신 실제 `main.tscn`을 인스턴스화한다. `Viewport.push_input()`으로 포인터 클릭과 Enter/Tab/Shift-Tab을 Godot GUI에 전달하고, 같은 입력 의도를 받은 별도 `DialogueFlowSession`의 공개 상태와 비교한다. 테스트가 `pressed.emit()`이나 강제 `grab_focus()`로 잘못된 연결·포커스를 숨기지 않는다.

```bash
godot --rendering-method gl_compatibility --audio-driver Dummy \
  --path examples/godot-narrative-dialogue-flow \
  --script res://tests/test_dialogue_ui_runtime.gd
```

Linux의 화면 없는 runner에서는 위 명령 앞에 `xvfb-run -a`를 붙여 실제 렌더 경로를 실행할 수 있다. 캡처가 필요하면 기존 디렉터리의 절대 경로를 `EVIDENCE_DIR` 환경변수로 전달한다. `--headless`이거나 환경변수가 없으면 캡처는 `UI_CAPTURE_NOT_RUN`이다. 캡처 없음은 렌더 검증 성공이 아니다.

검사 범위는 초기 포커스 → Next → 선택지 교체 → 같은 프레임의 반복 갱신 → STAY → MOVE → 거절 후 복구 → END → Scene 재생성이다. 잘못된 선택 거절은 `_on_choice_pressed()`에 stale ID를 주입하는 **handler-boundary 검사**이며, 실제 사용자 입력으로 불가능한 버튼을 눌렀다는 증거가 아니다. 정상 진행·복구는 GUI 입력으로 수행한다. 테스트 성공은 종료 코드 0과 `NARRATIVE_DIALOGUE_UI_TEST_PASS`를 함께 확인한다. 실패·파싱 오류·timeout 또는 marker 누락은 성공으로 올리지 않는다.

### 재현된 문제와 최소 교정

[UI 구현 계약](../../skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md)의 §9 포커스 복구와 §12 반복 갱신 책임을 구현에 적용한다. 공용 owner에 같은 규칙을 중복 추가하지 않는다.

- 기존 도메인 검사 84개는 통과했지만, 새 UI 검사에서는 초기/교체 포커스 부재와 같은 프레임에 남는 이전 선택지가 재현됐다.
- `_clear_choices()`는 `queue_free()` 전에 현재 Container에서 자식을 분리한다. 수명 종료를 안전하게 지연하되 이전 컨트롤을 live GUI 트리에 남기지 않는다.
- 화면 진입·대사/선택 전환에는 현재 의미 있는 Next 또는 첫 선택지로 포커스를 설정한다. 이 최소 예제는 상태 전환 시 목록을 다시 만드는 구조이며, 별도 실시간 목록 갱신/선택 보존 기능을 제공하지 않는다.
- 도메인 모델·세션·샘플 데이터·분기 의미·엔진 pin은 변경하지 않는다. 새로운 async 계층·원격 backend·웹 UI·상시 전용 CI를 추가하지 않는다.

2026-09-09 RED source `f703103ad170c867a1f204b660e07289066df6f5`, run `34327863780`: 도메인 84 PASS, UI 20 assertions 중 8 failures. 최초 GREEN source `02e3b3d31858c553b5d248f6c89d3ddc38bdc91f`, run `34328253408`: 도메인 84 PASS, 렌더 캡처 검사를 포함한 UI 48 PASS/0 failures. 최신 exact-head 재실행·PR/병합 상태는 [작업 기록 #864](https://github.com/alsdmlals4-eng/Base/issues/864)에서 별도로 확인한다. 최초 GREEN을 이후 변경의 자동 검증으로 간주하지 않는다.

Ubuntu/Xvfb/Mesa 소프트웨어 렌더러의 V-Sync 미지원 경고는 성능 PASS가 아니다. 생성된 1280×720 PNG는 초기 화면·선택지·STAY 결과·거절 안내·종료·재진입의 관찰 자료다. 자동 키/포인터 이벤트는 실제 하드웨어 입력이나 사람의 플레이테스트를 대신하지 않는다. 긴 한국어 스트레스, 모든 분기/해상도/장치, screen reader, 성능, 실제 게임 채택과 출시 검증은 별도다. 이 fixture에는 저장·원격 provider·비동기 요청이 없어 해당 검사는 `NOT_APPLICABLE`이며 구현했다고 주장하지 않는다.
