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
