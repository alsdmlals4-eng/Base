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

프로젝트가 **어떻게 보여야 하는가**를 빠르게 복원하는 페이지.

권장 Section:

```text
00.1_ART_DIRECTION_SUMMARY
00.2_MOOD_EMOTION
00.3_PALETTE
00.4_SHAPE_LANGUAGE
00.5_CAMERA_COMPOSITION
00.6_UI_DIRECTION
00.7_DO_NOT_DRIFT
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
```

`02_WIP`의 항목은 다음 작업의 승인 레퍼런스로 자동 사용하지 않는다.

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
- [ ] 설정/GDD 충돌을 `VISUAL_CANONICAL_CONFLICT`로 분리했다.
- [ ] 사용자 승인 없이 `01_APPROVED_REFERENCE`나 `04_FINAL`로 옮기지 않았다.
- [ ] 승인 시 Visual Artifact Registry와 Decision 연결을 갱신했다.
- [ ] 실제 제품 asset이라면 별도 `PROJECT_ASSET_APPROVED → promote`를 수행했다.

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
│  └─ 00.7_DO_NOT_DRIFT
│     └─ PROTECTED_VISUAL_RULES
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
│  └─ 02.3_COMPARISON
│     └─ UI_MAINHUD_002_AB_COMPARE
│
├─ 03_REJECTED
│  ├─ CHAR_HERO_002_REJECTED_A
│  └─ UI_MAINHUD_002_REJECTED_B
│
└─ 04_FINAL
   ├─ UI_MAINHUD_FINAL
   └─ MKT_STEAM_CAPSULE_FINAL
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
- [ ] `01_APPROVED_REFERENCE`에 승인 reference만 있다.
- [ ] WIP/Rejected가 승인 reference와 분리되어 있다.
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
4. 이미 그 reference를 사용한 후속 WIP를 찾아 회귀 검수한다.
5. Figma version history/checkpoint가 있으면 필요 시 이전 상태를 복원한다.
6. 실제 tracked asset이나 Godot 구현은 별도 승인·rollback 절차로 처리한다.
