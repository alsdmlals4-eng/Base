# Project Figma Visual Bible Profile

이 파일은 각 프로젝트에 복제해 사용하는 **프로젝트 로컬 Figma Visual Bible 운영 Profile**이다. Base의 `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`를 구체화하지만 GitHub/GDD/Decision, 실제 자산 파일, Godot 구현 권위를 대체하지 않는다.

## 0. Project identity

```yaml
project_name:
repository:
figma_status: CONFIGURED | NOT_CONFIGURED | AUTH_REQUIRED | ACCESS_DENIED | READ_ONLY | LINK_UNVERIFIED
figma_file_url:
figma_file_key:
owner:
usage_context: GDD | EXTERNAL_COLLABORATION | BOTH
responsible_document_id:
related_decision_ids: []
visual_artifact_registry_path: templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json
last_verified_at:
```

프로젝트에 Figma가 없거나 접근할 수 없으면 URL·frame 내용을 추정하지 않는다. `figma_status`를 정확히 기록하고 Markdown, text wireframe, local approved asset 등 접근 가능한 근거를 사용한다.

---

## 1. Authority boundary

```text
사용자 최신 지시
→ 프로젝트 AGENTS.md / Active Context / Confirmed Decisions
→ 등록된 아트·UI·세계관·캐릭터·시스템 정본
→ Figma APPROVED_VISUAL_REFERENCE
→ WIP·과거 Figma 시안·외부 레퍼런스
```

Figma는 다음을 소유한다.

- 승인된 시각 방향과 비교 기준
- 화면/컴포넌트/상태/프로토타입
- art direction, mood, palette, shape language
- camera/composition, UI visual language
- 승인된 시각 레퍼런스와 WIP 비교면
- 화면 간 `FLOW_MAP`, GPT 해석 기록, 구현 비교를 보여주는 시각 작업면

Figma는 다음을 소유하지 않는다.

- 게임 규칙·수치·확정 Decision의 유일 정본
- 실제 이미지 bytes의 로컬 후보 권위
- tracked 제품 자산 승인
- Godot 구현 완료·런타임 검증

정본과 Figma가 충돌하면 `VISUAL_CANONICAL_CONFLICT`로 기록하고 시각 자료를 자동 덮어쓰지 않는다.

---

## 2. Minimum page structure

프로젝트 시작 시 아래 5개를 최소 구조로 사용한다.

```text
00_DIRECTION
01_APPROVED_REFERENCE
02_WIP
03_REJECTED
04_FINAL
```

필요할 때만 추가한다.

```text
05_DEPRECATED
06_MARKETING
07_ARCHIVE
```

### `00_DIRECTION`

프로젝트가 **어떻게 보여야 하는가**와 주요 화면이 **어떻게 연결되는가**를 빠르게 복원하는 페이지.

권장 Section:

```text
00.1_ART_DIRECTION_SUMMARY
00.2_MOOD_EMOTION
00.3_PALETTE
00.4_SHAPE_LANGUAGE
00.5_CAMERA_COMPOSITION
00.6_UI_DIRECTION
00.7_DO_NOT_DRIFT
00.8_VISUAL_FLOW_HUB
```

최소 기록:

```yaml
visual_statement:
first_impression:
player_emotion:
key_palette:
shape_language:
camera_rules:
ui_density:
do_not_drift: []
```

`00.8_VISUAL_FLOW_HUB`에는 대표 화면 썸네일·Frame과 화살표를 배치해 전체 이동 구조를 한눈에 확인한다. 화면은 `screen_id`, 흐름은 `flow_id`를 사용하며 실제 Prototype 연결이 있는 경우 그 시작점과 범위를 함께 표시한다. 이 지도는 게임 규칙 정본이 아니라 탐색·검토용 `FLOW_MAP`이다.

### `01_APPROVED_REFERENCE`

이후 이미지·UI·시각 자료 작업에서 **실제로 비교 기준으로 사용할 승인 레퍼런스만** 둔다.

권장 Section:

```text
01.1_CHARACTERS
01.2_UNITS_ENEMIES
01.3_BUILDINGS
01.4_ENVIRONMENT
01.5_BATTLEFIELD_MAP
01.6_UI_HUD
01.7_ICONS
01.8_VFX
01.9_MARKETING
```

이 페이지에 들어가는 기준 Artifact는 Visual Artifact Registry에서 최소 `APPROVED_VISUAL_REFERENCE` 상태여야 한다.

### `02_WIP`

탐색·수정·비교 중 후보를 둔다.

권장 Section:

```text
02.1_CURRENT_ITERATION
02.2_ALTERNATIVES
02.3_COMPARISON
02.4_PENDING_REVIEW
02.5_FLOW_PROTOTYPE
02.6_GPT_INTERPRETATION
```

`02_WIP`의 항목은 다음 작업의 승인 레퍼런스로 자동 사용하지 않는다. `02.5_FLOW_PROTOTYPE`은 전환·취소·복귀·상태 변화를 검토하는 Prototype 작업면이며 Godot runtime proof가 아니다. `02.6_GPT_INTERPRETATION`은 화면 옆에 붙이는 `INTERPRETATION_RECORD`를 모으거나 연결하는 영역으로 사용할 수 있다.

### `03_REJECTED`

불채택 시안과 **왜 제외했는지**를 남긴다.

최소 기록:

```yaml
rejected_reason: []
reusable_parts: []
reentry_requires_review: true
```

예시 제외 사유:

- 캐릭터 비율이 승인 기준과 다름
- 색상 채도가 세계관 톤과 충돌
- UI 계층이 한눈에 읽히지 않음
- 카메라 거리가 승인 전장 기준과 다름
- 기존 승인 icon/shape language와 불일치

### `04_FINAL`

시각적으로 사용 확정된 표현을 모은다.

권장 Section:

```text
04.1_APPROVED_SCREENS
04.2_IMPLEMENTATION_COMPARE
```

`04.2_IMPLEMENTATION_COMPARE`는 `IMPLEMENTATION_PINNED` 이후 승인 시안과 실제 `RUNTIME_CAPTURE`를 나란히 놓고 차이를 검토할 때만 사용한다.

주의:

`04_FINAL`은 Figma 내부 조직명이다. 아래 상태를 자동 의미하지 않는다.

- `PROJECT_ASSET_APPROVED`
- tracked asset 존재
- 라이선스/권리 승인
- Godot 적용 완료
- runtime/human validation 완료

제품 자산 승격은 별도 asset lifecycle을 따른다.

---

## 3. Frame and artifact naming

### Prefix

```text
CHAR_   character
UNIT_   unit
ENEMY_  enemy
BOSS_   boss
BLDG_   building
ENV_    environment
BATTLE_ battlefield/map
UI_     UI/HUD/screen
FLOW_   visual flow/prototype
INT_    GPT/person interpretation record
CMP_    approved-vs-runtime compare
ICON_   icon
VFX_    visual effect
MKT_    marketing
```

### Stable ID examples

```text
CHAR_HERO_001
CHAR_NPC_ARCHIVIST_001
UNIT_RANGED_002
ENV_CITY_NIGHT_001
BATTLE_MAIN_001
UI_MAINHUD_001
UI_INVENTORY_002
FLOW_OUTGAME_001
INT_UI_MAINHUD_001
CMP_UI_MAINHUD_001
ICON_STATUS_FEAR_003
VFX_HIT_OCCULT_001
MKT_STEAM_CAPSULE_001
```

### Iteration examples

```text
CHAR_HERO_001_A
CHAR_HERO_001_B
UI_MAINHUD_001_v01
UI_MAINHUD_001_v02
```

승인 후에도 stable ID를 보존하고, 교체 관계는 Visual Artifact Registry의 `supersedes`와 Decision 기록으로 연결한다.

---

## 4. Reference card template

중요 frame 옆에 아래 메모 카드를 둔다.

### Approved reference card

```yaml
id:
status: APPROVED_VISUAL_REFERENCE
role:
responsible_document_id:
related_decision_ids: []
summary:
keep:
  -
  -
avoid:
  -
  -
do_not_drift:
  -
notes:
last_verified_at:
```

### WIP card

```yaml
id:
status: DRAFT_VISUAL | REVIEW_CANDIDATE
goal:
testing:
  -
open_questions:
  -
comparison_reference_ids: []
```

### GPT interpretation card

GPT가 Figma 쓰기 권한을 가진 경우 이미지·화면 옆에 **편집 가능한 텍스트 패널·annotation 또는 동등한 객체**로 남긴다.

```yaml
id: INT_<screen_id>
artifact_type: INTERPRETATION_RECORD
screen_id:
flow_id:
visual_artifact_id:
related_decision_ids: []
source_commit:
reviewed_at:
purpose:
first_attention:
primary_action:
confirmed:
  -
discovered_idea:
  -
ai_assumption:
  -
missing_canon:
  -
visual_canonical_conflict:
  -
rejected_expression:
  -
next_gate:
```

분류 의미:

- `CONFIRMED`: 현재 정본과 일치.
- `DISCOVERED_IDEA`: 검토 가치가 있는 새 표현이지만 미승인.
- `AI_ASSUMPTION`: 정본 근거 없이 AI가 추가한 요소.

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 전에는 승인 reference나 구현 요구가 아니다.

### Flow map card

```yaml
id: FLOW_<scope>
artifact_type: FLOW_MAP | PROTOTYPE_FLOW
flow_id:
entry_screen_id:
screen_ids: []
primary_path:
return_path:
failure_recovery:
prototype_status: NOT_RUN | DRAFT | REVIEWED
```

### Runtime compare card

```yaml
id: CMP_<screen_id>
artifact_type: COMPARE_BOARD
screen_id:
approved_visual_artifact_id:
runtime_capture_artifact_id:
source_commit:
target_platform:
target_resolution:
input_method:
drift_status: MATCHED | INTENDED_DIFFERENCE | IMPLEMENTATION_GAP | PLANNING_CHANGE_REQUIRED | AI_MOCKUP_ERROR | VISUAL_CANONICAL_CONFLICT | BLOCKED_UNVERIFIED
finding:
next_gate:
```

실제 `RUNTIME_CAPTURE`가 없으면 `MATCHED`를 사용할 수 없다.

### Rejected card

```yaml
id:
status: REJECTED
reason:
  -
reusable_parts:
  -
```

### Final visual card

```yaml
id:
figma_location: 04_FINAL
visual_status: APPROVED_VISUAL_REFERENCE | IMPLEMENTATION_PINNED | VALIDATED
usage:
  -
related_decision_ids: []
product_asset_status: NOT_APPLICABLE | APPROVED_CANDIDATE | PROJECT_ASSET_APPROVED | APPLIED_AND_RUNTIME_VERIFIED
```

`product_asset_status`와 `visual_status`를 합치지 않는다.

---

## 5. Standard visual work flow

### Before generation/editing

- [ ] 최신 프로젝트 정본과 Decision을 확인했다.
- [ ] Visual Artifact Registry에서 관련 Figma Artifact를 찾았다.
- [ ] `01_APPROVED_REFERENCE`의 관련 frame/node를 실제로 확인했다.
- [ ] 접근 불가라면 `LINK_UNVERIFIED / AUTH_REQUIRED / ACCESS_DENIED`를 기록했다.
- [ ] `Keep / Avoid / Do Not Drift`를 작업 계약에 옮겼다.
- [ ] WIP나 Rejected를 승인 기준으로 잘못 사용하지 않았다.

### After generation/editing

- [ ] 새 결과는 우선 `02_WIP` 또는 review candidate로 두었다.
- [ ] 승인 reference와 스타일·비율·색·형태·질감·광원·카메라·UI 계층을 비교했다.
- [ ] 화면 시각화라면 `INTERPRETATION_RECORD`에 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION / MISSING_CANON / VISUAL_CANONICAL_CONFLICT`를 분리했다.
- [ ] 여러 화면이 연결되면 `FLOW_MAP`의 `screen_id / flow_id`와 진입·복귀 경로를 갱신했다.
- [ ] 설정/GDD 충돌을 `VISUAL_CANONICAL_CONFLICT`로 분리했다.
- [ ] 사용자 승인 없이 `01_APPROVED_REFERENCE`나 `04_FINAL`로 옮기지 않았다.
- [ ] 승인 시 Visual Artifact Registry와 Decision 연결을 갱신했다.
- [ ] 실제 제품 asset이라면 별도 `PROJECT_ASSET_APPROVED → promote`를 수행했다.

### After implementation

- [ ] 승인 화면이 `IMPLEMENTATION_PINNED` 상태인지 확인했다.
- [ ] 실제 Godot/Web 화면을 `RUNTIME_CAPTURE`로 확보했다.
- [ ] `COMPARE_BOARD`에서 승인 시안과 runtime을 비교했다.
- [ ] `MATCHED / INTENDED_DIFFERENCE / IMPLEMENTATION_GAP / PLANNING_CHANGE_REQUIRED / AI_MOCKUP_ERROR / VISUAL_CANONICAL_CONFLICT / BLOCKED_UNVERIFIED` 중 실제 증거에 맞는 상태를 기록했다.
- [ ] Prototype만 보고 runtime 완료를 주장하지 않았다.

---

## 6. Concrete sample — game project

```text
PROJECTNAME_Visual_Bible
│
├─ 00_DIRECTION
│  ├─ 00.1_ART_DIRECTION_SUMMARY
│  │  └─ VISUAL_STATEMENT_CARD
│  ├─ 00.3_PALETTE
│  │  ├─ PALETTE_PRIMARY
│  │  └─ PALETTE_ACCENT
│  ├─ 00.5_CAMERA_COMPOSITION
│  │  └─ CAMERA_GAMEPLAY_REFERENCE
│  ├─ 00.7_DO_NOT_DRIFT
│  │  └─ PROTECTED_VISUAL_RULES
│  └─ 00.8_VISUAL_FLOW_HUB
│     └─ FLOW_OUTGAME_001
│        ├─ UI_TERRITORY_001
│        ├─ UI_GUILD_001
│        ├─ UI_PARTY_001
│        └─ UI_CHAPEL_001
│
├─ 01_APPROVED_REFERENCE
│  ├─ 01.1_CHARACTERS
│  │  ├─ CHAR_HERO_001
│  │  └─ CHAR_NPC_ARCHIVIST_001
│  ├─ 01.4_ENVIRONMENT
│  │  └─ ENV_CITY_NIGHT_001
│  ├─ 01.5_BATTLEFIELD_MAP
│  │  └─ BATTLE_MAIN_001
│  └─ 01.6_UI_HUD
│     ├─ UI_MAINHUD_001
│     └─ UI_INVENTORY_002
│
├─ 02_WIP
│  ├─ 02.1_CURRENT_ITERATION
│  │  ├─ CHAR_HERO_002_v01
│  │  └─ UI_MAINHUD_002_v01
│  ├─ 02.3_COMPARISON
│  │  └─ UI_MAINHUD_002_AB_COMPARE
│  ├─ 02.5_FLOW_PROTOTYPE
│  │  └─ FLOW_OUTGAME_001_PROTO
│  └─ 02.6_GPT_INTERPRETATION
│     └─ INT_UI_MAINHUD_002
│
├─ 03_REJECTED
│  ├─ CHAR_HERO_002_REJECTED_A
│  └─ UI_MAINHUD_002_REJECTED_B
│
└─ 04_FINAL
   ├─ 04.1_APPROVED_SCREENS
   │  └─ UI_MAINHUD_FINAL
   └─ 04.2_IMPLEMENTATION_COMPARE
      └─ CMP_UI_MAINHUD_001
```

예를 들어 `CHAR_HERO_001` 옆 카드:

```yaml
id: CHAR_HERO_001
status: APPROVED_VISUAL_REFERENCE
role: player-character visual baseline
summary: 작은 화면에서도 읽히는 단순 실루엣과 제한된 강조색
keep:
  - head/body proportion
  - primary equipment silhouette
  - outline weight family
avoid:
  - realistic facial rendering
  - extra ornamental equipment
  - palette saturation increase
do_not_drift:
  - character readability at gameplay scale
```

---

## 7. Figma-native organization guidance

- Pages는 작업 단계·milestone·main component/style 정의를 나누는 데 사용한다.
- Sections는 한 page 안에서 관련 frame을 묶고 협업·탐색·handoff 상태를 명확히 하는 데 사용한다.
- `FLOW_MAP`은 화면 Frame을 한눈에 보는 시각 지도이며, 실제 클릭 검증이 필요하면 별도 `PROTOTYPE_FLOW`로 연결한다.
- GPT 해석 기록은 이미지에 구워 넣지 않고 편집 가능한 text/annotation으로 두어 이후 수정·승인·폐기가 가능하게 한다.
- 반복되는 UI가 안정화되면 Main Components/Styles를 사용한다.
- 유료 Library 발행은 여러 파일에서 실제 재사용할 때만 선택한다.
- 이름 규칙은 프로젝트 초기에 고정하고 frame/component 검색성을 유지한다.
- 큰 변경 전에는 Figma version history 또는 사용 가능한 branch/checkpoint를 활용한다.

---

## 8. Project adoption checklist

- [ ] 프로젝트 전용 Figma file을 정했다.
- [ ] `figma_file_url / file_key / owner / access`를 기록했다.
- [ ] 기본 5개 page를 만들었다.
- [ ] `00_DIRECTION`에 최소 visual statement와 `Do Not Drift`가 있다.
- [ ] 화면 흐름이 중요하면 `00.8_VISUAL_FLOW_HUB`에 `FLOW_MAP`과 `screen_id / flow_id`가 있다.
- [ ] `01_APPROVED_REFERENCE`에 승인 reference만 있다.
- [ ] WIP/Rejected가 승인 reference와 분리되어 있다.
- [ ] 중요 AI 화면에는 필요한 경우 `INTERPRETATION_RECORD`가 연결돼 있다.
- [ ] 중요 frame에 stable ID와 metadata card가 있다.
- [ ] Visual Artifact Registry에 file/page/frame/node와 상태가 연결됐다.
- [ ] 이미지 생성 Skill이 승인 reference를 먼저 확인한다.
- [ ] 제품 asset bytes 권위를 Figma로 옮기지 않았다.

---

## 9. Rollback / supersession

잘못된 reference가 승인 위치에 들어간 경우:

1. 현재 Decision과 responsible document를 재확인한다.
2. 잘못된 frame을 `02_WIP`, `03_REJECTED` 또는 `05_DEPRECATED`로 이동한다.
3. Visual Artifact Registry 상태와 `supersedes` 관계를 갱신한다.
4. 이미 그 reference를 사용한 후속 WIP·`INTERPRETATION_RECORD`·`FLOW_MAP`을 찾아 회귀 검수한다.
5. Figma version history/checkpoint가 있으면 필요 시 이전 상태를 복원한다.
6. 실제 tracked asset이나 Godot 구현은 별도 승인·rollback 절차로 처리한다.
