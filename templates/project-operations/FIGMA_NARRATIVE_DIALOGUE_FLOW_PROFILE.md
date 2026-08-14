# Figma Narrative Dialogue Flow Profile

이 프로필은 `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`, `FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`, `FIGMA_VISUAL_BIBLE_PROFILE.md`를 확장하는 프로젝트용 **대화 흐름 시각화·편집 규칙**이다.

목표는 게임의 분기형 대화를 Figma에서 한눈에 읽고, **씬·분기 구간·개별 대화·선택지를 각각 따로 선택하고 수정 후보로 다룰 수 있게 하는 것**이다. Figma는 계속 `VISUAL_WORKSPACE`이며 프로젝트의 확정 대화 데이터, Decision, Godot 구현을 대체하는 canonical source가 아니다.

---

## 1. 적용 위치

프로젝트의 기본 권장 위치:

```text
20_<PROJECT>_UI_UX
└─ 60_GAMEPLAY_FLOWS
   └─ NARRATIVE_DIALOGUE
      ├─ 00_FLOW_INDEX
      ├─ SCENE_<scene_id>
      ├─ SCENE_<scene_id>
      └─ ...
```

Starter 3-page fallback을 쓰는 프로젝트는 `02_WORKSPACE` 안에 동등한 Section을 만든다. 페이지 수보다 Stable ID와 권한 경계가 우선한다.

---

## 2. 최소 계층

```text
SCENE_GROUP
└─ DIALOGUE_BEAT
   ├─ DIALOGUE_LINE
   └─ CHOICE
      └─ STAY_IN_SCENE | MOVE_SCENE | END
```

### `SCENE_GROUP`

`SCENE_GROUP`은 **배경·장소·연출의 시각적 연속성이 유지되는 범위**다. 모든 분기 지점을 별도 Scene으로 만들지 않는다.

최소 필드:

```yaml
scene_id:
location_id:
background_ref:
title:
entry_beat_id:
```

같은 `scene_id` 안에서 진행되는 선택 결과는 기본적으로 현재 `background_ref`를 유지한다. 배경 변화가 없는 대화 분기를 새 Scene으로 복제하지 않는다.

프로젝트에서 `Scene`이 Godot `.tscn`, 컷신, 스테이지 등 다른 뜻의 canonical 용어라면 Figma 표기에는 `SCENE_GROUP`을 사용하거나 프로젝트 번역 규칙을 둔다.

### `DIALOGUE_BEAT`

`DIALOGUE_BEAT`은 한 Scene 안의 **읽기 좋은 분기 단위**다. 보통 짧은 대화 목록과 그 뒤의 선택지 또는 종료를 묶는다.

```yaml
beat_id:
scene_id:
title:
dialogue_ids: []
choice_ids: []
```

한 대화 줄마다 그래프 박스를 만들지 않는다. 그래프는 Beat 단위로 유지해 가독성을 확보하되, 내부 대화 줄은 Stable ID로 각각 선택 가능하게 한다.

### `DIALOGUE_LINE`

각 대화 줄은 독립적인 편집·검토 대상을 가진다.

```yaml
dialogue_id:
beat_id:
speaker_id:
text:
```

**Do not use array index as durable identity.** 대화가 삽입·삭제·재정렬돼도 `dialogue_id`가 동일한 줄의 리뷰·Figma annotation·현지화·구현 인계를 계속 가리킬 수 있어야 한다.

### `CHOICE`

```yaml
choice_id:
source_beat_id:
text:
target_beat_id:
transition_kind: STAY_IN_SCENE | MOVE_SCENE | END
```

- `STAY_IN_SCENE`: source와 target Beat가 같은 `scene_id`다. Scene/background continuity를 유지한다.
- `MOVE_SCENE`: target Beat가 다른 `scene_id`에 속한다. 장소·배경 전환을 명시한다.
- `END`: 플레이 가능한 다음 Beat 없이 해당 흐름을 종료한다.

조건식, 변수, 비용, 스킬 체크, 플래그 부여, 보상 등은 실제 프로젝트가 요구할 때 프로젝트 데이터 계약으로 확장한다. Base 공용 Figma 프로필은 미리 강제하지 않는다.

---

## 3. 캔버스 배치 규칙

각 `SCENE_GROUP`은 Figma **Section 또는 명확한 containing frame**으로 표현한다.

```text
SCENE_SCHOOL_HALLWAY
├─ scene header
├─ background preview
├─ location / background metadata
├─ BEAT_INTRO
│  ├─ DIALOGUE_D001
│  ├─ DIALOGUE_D002
│  ├─ DIALOGUE_D003
│  ├─ CHOICE_C001 -> BEAT_TALK     [STAY_IN_SCENE]
│  └─ CHOICE_C002 -> SCENE_CLASS   [MOVE_SCENE]
└─ BEAT_TALK
   └─ ...
```

### 연결선 의미

- `STAY_IN_SCENE` 연결은 같은 Scene section 안에서 끝난다.
- `MOVE_SCENE` 연결은 **Scene section boundary**를 넘어가며 connector label 또는 annotation에 `MOVE_SCENE`을 표시한다.
- `END`는 명시적인 End card/terminal에 끝난다.
- 선택지 텍스트만 보고 장소 이동 여부를 추정하게 만들지 않는다.

### 그래프 단일 관계 모델

대화 데이터와 분기 맵이 서로 다른 edge 목록을 각자 canonical하게 관리하면 안 된다.

**Use a single relationship model.** 생성 도구나 동기화 도구가 존재할 경우 `choice_id / source_beat_id / target_beat_id / transition_kind`에서 분기 맵을 **derived**해야 한다.

**Do not maintain** 실제 선택 관계와 무관한 두 번째 수동 edge canon을 추가한다. 수동 Figma 연결만 가능한 단계라면 각 connector에 같은 Stable ID를 기록하고 다음 데이터 변경 때 reconciliation 대상으로 둔다.

---

## 4. Edit Mode selection contract

씬과 대화를 각각 따로 확인·수정하려면 다음 네 대상이 **individually selectable**이어야 한다.

### Scene selection

선택 시 보여줄 항목:

```yaml
scene_id: read-only identity
location_id:
background_ref:
title:
entry_beat_id:
contained_beat_ids: derived/read-only list
```

- WIP에서 제목·장소/배경 reference를 수정할 수 있다.
- 승인된 `APPROVED_REFERENCE`/FINAL을 직접 덮어쓰지 않고 복제 → WIP → review 흐름을 따른다.
- 다른 Beat로 이동해도 `STAY_IN_SCENE`이면 Scene selection의 배경 연속성이 유지돼야 한다.

### Beat selection

```yaml
beat_id: read-only identity
scene_id: owning scene
title:
dialogue_ids:
choice_ids:
```

- Beat 단위로 대화 목록과 outgoing choices를 한 번에 확인한다.
- Beat 순서를 바꿔도 내부 `dialogue_id`를 새로 만들지 않는다.

### Dialogue Line selection

```yaml
dialogue_id: read-only identity
beat_id: owning beat
speaker_id:
text:
```

- 한 줄만 선택해 speaker/text를 확인·수정 후보로 만들 수 있다.
- 인접 대화 줄을 편집해야만 해당 줄을 수정할 수 있는 구조를 금지한다.
- 줄 삽입/삭제/정렬은 array index가 아니라 `dialogue_id` 기준으로 추적한다.

### Choice selection

```yaml
choice_id: read-only identity
source_beat_id: read-only source
text:
target_beat_id:
transition_kind: STAY_IN_SCENE | MOVE_SCENE | END
```

- target과 `transition_kind`를 한 화면에서 같이 확인한다.
- target 변경으로 source/target의 `scene_id` 관계가 달라지면 transition kind도 검증한다.
- 같은 Scene인데 `MOVE_SCENE`, 다른 Scene인데 `STAY_IN_SCENE`인 상태는 review 오류로 표시한다.

---

## 5. 권장 화면 모드

최소 두 모드만 필요하다.

### Preview Mode

- 실제 플레이 순서로 한 줄씩 진행.
- 선택지를 눌러 분기를 따라간다.
- 현재 Scene/background와 현재 Beat/Line을 보여준다.
- 방문 경로를 시각화할 수 있다.

### Edit Mode

- 왼쪽/중앙: Scene section + Beat branch map.
- 선택 Beat: ordered dialogue list + choices.
- 선택 Dialogue Line/Choice: 좁은 Inspector에서 해당 항목만 수정.
- Scene 선택 시 background/location metadata를 별도 Inspector로 수정.

Preview Mode와 Edit Mode는 같은 Stable ID와 관계 데이터를 읽어야 한다. Preview용 story model과 Edit용 branch map model을 수동으로 따로 유지하지 않는다.

---

## 6. Figma naming

권장 이름:

```text
SCENE_<scene_id> / <location>
BEAT_<beat_id> / <short title>
DIALOGUE_<dialogue_id> / <speaker>
CHOICE_<choice_id> / <short text>
END_<ending_id>
```

예:

```text
SCENE_S01 / 학교 복도
BEAT_B01 / 방과 후 시작
DIALOGUE_D003 / 유이
CHOICE_C001 / 말을 걸다
CHOICE_C002 / 그냥 지나치다
```

사람이 읽는 이름은 바뀔 수 있지만 Stable ID는 변경 이유 없이 재발급하지 않는다.

---

## 7. 프로젝트 데이터와 Figma 사이의 권한

```text
confirmed planning / project narrative data
→ canonical story rule
→ Figma narrative dialogue workspace
→ visual review / proposal / prototype
→ implementation handoff
→ Godot runtime + tests
```

Figma에서 수정한 텍스트·target·transition은 **자동 canonical 결정이 아니다**. 프로젝트가 Figma→데이터 round-trip을 별도로 승인·구현하지 않은 상태라면 Figma 수정은 `DRAFT_VISUAL` 또는 제안이며 책임 narrative/data 문서에 반영된 뒤에만 확정된다.

Prototype은 선택 흐름·정보 구조를 검토하는 증거일 뿐 **runtime proof**가 아니다. `IMPLEMENTATION_PINNED` 이후에도 실제 Godot scene/script/data와 실행 검증이 별도로 필요하다.

---

## 8. Handoff 최소 필드

```yaml
flow_id:
scene_id:
beat_id:
dialogue_ids: []
choice_ids: []
figma_file:
figma_page:
figma_section_or_frame_node:
responsible_narrative_source:
related_decision_ids: []
source_commit:
godot_scene:
godot_dialogue_data:
implementation_status: NOT_STARTED | IN_PROGRESS | IMPLEMENTED | VERIFIED
last_verified_at:
```

`IMPLEMENTED`와 `VERIFIED`는 `FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`의 기존 의미를 따른다.

---

## 9. 검증 규칙

### 구조 검사

- 모든 `SCENE_GROUP`에 고유 `scene_id`가 있는가.
- 모든 Beat/Line/Choice가 각각 고유 `beat_id` / `dialogue_id` / `choice_id`를 가지는가.
- 모든 target Beat가 존재하거나 `END`인가.
- `STAY_IN_SCENE`의 source/target `scene_id`가 같은가.
- `MOVE_SCENE`의 source/target `scene_id`가 다른가.
- background continuity가 같은 분기를 Scene 복제로 표현하고 있지 않은가.

### 편집성 검사

- Scene을 독립 선택해 장소/배경을 확인할 수 있는가.
- Beat를 독립 선택해 대화 목록/선택지를 확인할 수 있는가.
- 각 Dialogue Line을 독립 선택해 speaker/text를 확인할 수 있는가.
- 각 Choice를 독립 선택해 text/target/transition을 확인할 수 있는가.

### Authority 검사

- Figma가 canonical story DB라고 쓰여 있지 않은가.
- Prototype을 Godot/runtime proof로 보고하지 않는가.
- APPROVED/FINAL을 AI가 직접 수정하지 않는가.
- 데이터 변경 뒤 visual graph reconciliation이 필요한지 추적하는가.

---

## 10. Implementation Reality Gate claim ceiling

이 프로필을 Base에 추가했다는 사실이 증명할 수 있는 최대 주장은 다음과 같다.

```yaml
figma_narrative_dialogue_rule_contract: DOCUMENTED
per_scene_edit_contract: DOCUMENTED
per_dialogue_line_edit_contract: DOCUMENTED
typed_transition_contract: DOCUMENTED
supplied_figma_make_edit_mode: NOT_IMPLEMENTED
godot_runtime_integration: NOT_IMPLEMENTED
project_data_migration: NOT_RUN
human_validation: NOT_RUN
```

프로젝트가 실제 편집 UI를 구현한 뒤에는 그 프로젝트의 실제 코드·데이터·Figma frame/node·runtime capture/test를 다시 확인해 IRG를 통과해야 한다.

---

## 11. 적대적 검토 체크

다음 중 하나라도 생기면 보완한다.

- 모든 branch stop을 Scene으로 만들어 같은 배경이 반복 복제된다.
- `scene_id`와 Godot Scene 의미가 충돌하지만 번역 규칙이 없다.
- 대화 line identity를 array index로만 관리한다.
- 그래프용 edge와 실행용 choice target을 각각 따로 수정한다.
- 한 대화 줄마다 graph node를 강제해 흐름을 읽기 어려워진다.
- 단순 선택지 프로젝트에 조건/변수/보상 schema를 과도하게 강제한다.
- Figma 텍스트 수정이 사용자 승인 없이 project narrative canon을 덮어쓴다.
- Figma prototype만으로 `VERIFIED` 또는 runtime 완료를 주장한다.

---

## 12. 도입 순서

1. 현재 프로젝트의 narrative/data canonical source를 확인한다.
2. 기존 Scene/Node/Dialogue ID가 있으면 재사용한다.
3. 없으면 프로젝트 데이터 정본에서 Stable ID 규칙을 먼저 정한다.
4. `60_GAMEPLAY_FLOWS/NARRATIVE_DIALOGUE`에 Scene section을 만든다.
5. Scene 안에 Beat를 배치하고 Dialogue Line/Choice를 연결한다.
6. `STAY_IN_SCENE / MOVE_SCENE / END`를 검증한다.
7. Preview와 Edit가 같은 모델을 소비하는지 확인한다.
8. 사용자 리뷰 전까지 WIP로 유지한다.
9. 구현 인계 시 Figma Stable ID ↔ responsible source ↔ Godot path를 연결한다.
10. 실제 runtime 검증 후에만 `VERIFIED`로 올린다.

이 프로필은 공용 출발점이다. 프로젝트 고유 캐릭터, 실제 대사, 장소, 조건식, 변수, 엔딩 규칙은 각 프로젝트의 정본에 둔다.