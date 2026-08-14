# Figma → Godot Narrative Dialogue Runtime Design

Date: 2026-08-14
Status: approved implementation follow-up to PR #382/#383

## Goal

Figma에서 Scene/Beat/Dialogue/Choice를 시각적으로 검토·수정 후보로 다루면서, 같은 Stable-ID 관계 데이터를 Godot이 직접 소비해 분기 대화를 실행할 수 있게 한다.

## Compared approaches

1. 현재 Make의 Scene-per-branch + 별도 MNODES/MEDGES 유지: 빠르지만 같은 배경 Scene 복제와 이중 edge drift 때문에 제외.
2. Dialogic 2 전면 도입: 기능은 풍부하지만 이번 최소 Stable-ID JSON bridge보다 범위/의존성이 크고 프로젝트 공통 Base에 강제하기 부적합해 제외.
3. Yarn Spinner Godot 통합: 강한 narrative authoring 도구지만 현재 Figma JSON 계약과 source model이 다르고 Base 전체 기본값으로 강제하지 않음.
4. **최소 JSON contract + dependency-free GDScript model/session + Make reference editor**: 채택.

## Chosen architecture

```text
project narrative canon
        ↓ proposal/sync
DialogueFlow JSON
  scene_id
    beat_id
      dialogue_id
      choice_id -> target_beat_id + transition_kind
       ↓                         ↓
Figma Make reference         Godot model/session
Preview + Edit               runtime execution
```

분기 맵은 choice 관계에서 derived한다. 별도 manual edge canon은 금지한다.

## Runtime boundary

Base 공용 구현은 JSON validation과 deterministic flow traversal까지만 소유한다. 조건식, 변수, 저장, 현지화, 보이스, 컷신은 프로젝트 요구가 생길 때 별도 계약으로 확장한다.

## Authority boundary

Figma/Make 편집은 `DRAFT_VISUAL`/proposal이다. 프로젝트 narrative canon 자동 변경이 아니다. Base Godot sample은 isolated reference fixture이며 실제 프로젝트의 HiGodot authoring authority를 대체하지 않는다.

## Completion gates

- expected RED on missing production runtime
- Godot 4.7.1 actual test PASS
- sample main scene headless startup PASS
- invalid transition fail-closed PASS
- Make reference build PASS
- Base contract/required CI PASS
- adversarial recheck with no unresolved P0/P1
- merge and post-merge recheck
