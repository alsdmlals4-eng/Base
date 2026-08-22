# Visual & Asset-Material Reusable Modules

이 문서는 이미지를 “한 장 완성품”으로만 소비하지 않고, 프로젝트별 시각 정체성을 해치지 않는 범위에서 **구조·레이어·상태·semantic 역할을 재사용하는 자산 계약**으로 분해한다.

핵심 경계:

```text
reference/discovery
→ rights + provenance
→ project visual fit
→ primary-use quality
→ reusable-harvest review
→ project promotion
```

`DIRECT_LICENSED_REUSE` 또는 이 문서의 module 정의만으로 `PROJECT_ASSET_APPROVED`가 되지 않는다.

---

## RM-VIS-001 · SEMANTIC_UI_SKIN_KIT

**문제:** 프로젝트마다 버튼·패널·선택/잠금/비활성/경고 상태를 새로 그리면 구현·아트·가독성 QA가 반복된다.

```yaml
semantic_tokens:
  surfaces: []
  text_roles: []
  state_roles:
    - default
    - hover_or_focus
    - pressed
    - selected
    - disabled
    - locked
    - warning
    - success
components:
  - panel
  - button
  - tab
  - tooltip
  - badge
  - progress
  - modal
  - list_item
sizing:
  density_profiles: []
  minimum_hit_targets:
accessibility:
  focus_visibility:
  redundant_state_channels:
project_skin:
  typography:
  materials:
  ornaments:
  animation:
```

### 공유할 것

- semantic component 이름.
- padding/state/interaction contract.
- 9-slice 또는 scalable frame 구조.
- focus/selected/disabled의 구별 규칙.

### 공유하지 않을 것

- 프로젝트 고유 장식.
- 세계관별 재질·문양.
- 특정 경쟁작의 화면 배치/색/아이콘을 그대로 복제한 skin.

### 적용

모든 Godot 프로젝트의 prototype/Vertical Slice UI에서 후보. 특히 TETRIS의 active/inactive/lock, SWITCHY의 build/run/control state, NINJA의 REST/workbench, OMENWARD의 roulette/deployment와 잘 맞는다.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE`.

---

## RM-VIS-002 · GAMEPLAY_SYMBOL_ATLAS

**문제:** 공격/방어/치유/상태/자원/경로/화물 같은 gameplay semantic을 프로젝트마다 무작위 아이콘으로 만들면 학습비와 제작비가 반복된다.

```yaml
symbol_id:
semantic_role:
shape_family:
filled_outline_variant:
size_profiles:
state_variants:
  normal:
  selected:
  disabled:
  warning:
redundant_channels:
  color:
  shape:
  text_or_label:
project_skin_rules:
source_provenance:
```

### 원칙

- `semantic_role`은 공용화 가능.
- 최종 icon art는 project visual language에 맞춰 교체 가능.
- 색만으로 의미를 전달하지 않는다.
- 16/24/32/48px 등 실제 사용 크기에서 legibility를 검증한다.

SWITCHY가 이미 색+형상+텍스트 중복 채널을 사용한다는 점은 이 module의 강한 내부 사례다.

---

## RM-VIS-003 · MODULAR_BACKGROUND_LAYER_KIT

**목적:** 장소마다 전체 배경을 처음부터 다시 만드는 대신 같은 장소/세계관에서 변형 가능한 구조를 먼저 분리한다.

1차 적용: URBAN_LEGEND, GRIMOIRE, MY_LITTLE_BOAT, COC_FICTION의 visual storyboard/reference.

```yaml
background_scene_id:
layers:
  base_environment:
  depth_midground:
  foreground_props:
  lighting:
  time_weather:
  event_overlay:
  atmosphere_fx:
variant_axes:
  time_of_day: []
  weather: []
  story_state: []
  damage_or_change: []
reusable_parts: []
one_off_parts: []
```

### 제작 순서

```text
approved scene purpose
→ primary image/background production
→ primary-use review
→ harvest review
→ layer/part classification
→ selective rebuild/decomposition
→ later variant reuse
```

완성 이미지의 분리 가능성을 위해 1차 품질을 희생하지 않는다.

### 이미지 분해 provenance

- `SOURCE_LAYER`
- `MASK_CUTOUT`
- `MANUAL_OR_SEMANTIC_REBUILD`
- `DERIVED_GENERATIVE_RECOVERY`

가려진 부분을 생성해 복원했다면 관찰된 원본 layer로 기록하지 않는다.

---

## RM-VIS-004 · COMBAT_TELEGRAPH_VFX_KIT

**문제:** 공격 경고·target·impact·status·cooldown·위험 범위를 매 기능마다 독립 제작하면 읽기 규칙이 흔들린다.

적용: NINJA_SURVIVAL, OMENWARD, GRIMOIRE, TEN_PACES의 시각 해결/replay.

```yaml
telegraph_id:
semantic_role:
phases:
  anticipate:
  commit:
  impact:
  recover:
spatial_channel:
color_channel:
shape_channel:
motion_channel:
text_or_icon_channel:
reduced_motion_variant:
priority:
```

### 공용화 범위

- 위험/지원/target/impact의 semantic state machine.
- timing/priority/Reduced Motion 대체 규칙.
- reusable VFX graph/prefab 구조 후보.

프로젝트별 particle, shader, 색감, 붓터치/픽셀/잉크 표현은 skin이다.

---

## RM-VIS-005 · PORTRAIT_STATE_VARIANT_KIT

**문제:** 동일 캐릭터의 표정·상태·대사 맥락 이미지를 매번 독립 생성하면 얼굴·복장·색·프레이밍 일관성이 깨진다.

적용: URBAN_LEGEND, GRIMOIRE, COC_FICTION visual reference/production.

```yaml
character_visual_id:
base_identity_lock:
  face_geometry:
  hair:
  costume:
  palette:
  framing:
  light_family:
variant_axes:
  expression: []
  gaze: []
  head_pose: []
  condition_overlay: []
  speaker_or_relationship_state: []
source_image_refs: []
derived_variant_refs: []
```

### 재사용 원칙

- base identity를 하나의 기준으로 유지.
- 표정/상태 variant만 bounded change.
- body/pose가 크게 달라지면 별도 base family 여부를 검토.
- 생성 결과는 human visual review 전 제품 자산으로 승격하지 않는다.

---

## RM-VIS-006 · VISUAL_CREATIVE_PROVIDER_ADAPTER

**문제:** 특정 AI 모델·서비스·프롬프트에 시각 제작 workflow를 직접 결합하면 모델 교체, 비용 변화, 약관 변화, 수작업/외주 전환 때 Base 규칙까지 다시 설계해야 한다. 반대로 provider를 추상화하지 않고 결과물만 비교하면 빠른 생성 시간 뒤에 숨은 재시도·사람 수정·통합·QA 비용을 놓친다.

**판정:** `PATTERN_EXTRACT · PROVIDER_NEUTRAL · PROJECT_OWNER_PRESERVED`.

```yaml
module: VISUAL_CREATIVE_PROVIDER_ADAPTER
brief_id:
project_visual_canon_ref:
provider_route: AI_SERVICE | LOCAL_MODEL | MANUAL | OUTSOURCE
provider_or_tool:
model_or_version:
terms_or_license_checked_at:
protected_constraints: []
changeable_scope: []
reference_inputs: []
requested_variants: []
outputs: []
provenance_record_ref:
rights_status:
HUMAN_EDIT_DELTA:
  baseline_total_minutes:
  candidate_generation_or_creation_minutes:
  attempt_count:
  human_edit_minutes:
  integration_minutes:
  qa_minutes:
  candidate_total_minutes:
  net_minutes_saved:
  quality_delta:
  consistency_delta:
  repeatability:
```

### Provider-neutral rules

1. `project_visual_canon_ref`와 승인된 brief가 authority다. provider/model은 교체 가능한 backend일 뿐 프로젝트 Visual Canon을 바꾸지 않는다.
2. 특정 공급자 persona·magic wording·고유 prompt syntax를 Base canonical contract로 승격하지 않는다. 필요하면 project-local technique/prompt card에 둔다.
3. `AI_SERVICE`는 현재 승인된 사용자 플랜/기능 범위 안에서 별도 종량 API credit 없이 쓸 수 있을 때만 기본 후보가 된다. 새로운 paid API/subscription/credit는 별도 사용자 승인 전 자동 선택하지 않는다.
4. `LOCAL_MODEL`은 free라는 이유만으로 자동 채택하지 않는다. GPU/설치/모델 저장공간/업데이트/실행시간을 `HUMAN_EDIT_DELTA`와 유지비에 포함한다.
5. `MANUAL`은 정상 provider route다. 생성형 AI가 항상 우선이라는 전제를 두지 않는다.
6. `OUTSOURCE`는 기존 승인 계약이나 별도 사용자 승인이 있을 때만 실제 소비한다. 이 module이 새 지출을 승인하지 않는다.
7. 생성/제작 후보는 `ASSET_RIGHTS_AND_PROVENANCE_RECORD`와 human visual review 전 `PROJECT_ASSET_APPROVED`가 아니다.
8. 생성 속도가 빨라도 재시도·사람 수정·통합·QA를 포함한 `candidate_total_minutes`와 품질·일관성이 baseline보다 나쁘면 채택 근거가 아니다.

### 기존 Visual module과의 관계

`RM-VIS-006`은 새로운 art style owner나 runtime rendering module이 아니다. 다음 기존 module을 **어떤 제작 backend로 만들지**만 바꿀 수 있다.

```text
approved project visual need
→ RM-VIS-001/002/003/004/005 또는 project-specific visual target
→ VISUAL_CREATIVE_PROVIDER_ADAPTER
→ candidate output
→ rights/provenance + human visual review
→ primary use
→ reusable harvest
```

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · PROJECT_ADOPTION_NOT_RUN`.

---

# Direct licensed prototype material candidates

## Kenney CC0

Kenney의 여러 asset 페이지는 해당 game asset을 `Creative Commons CC0`로 제공한다고 명시한다. 따라서 아래 사용을 `DIRECT_LICENSED_REUSE_CANDIDATE`로 둔다.

- prototype UI frame/button.
- placeholder icon.
- input/readability test용 neutral UI.
- internal tool/sample screen.

예시 후보 family:
- UI Pack / RPG Expansion.
- UI Pack - Adventure.
- Pixel UI Pack / Pixel Adventure.
- UI Audio처럼 UI feedback 재료.

### 사용 전 체크

```yaml
source_page:
license_at_download:
downloaded_version_or_date:
original_archive_hash:
project_fit:
visual_rework_needed:
attribution_requirement:
trademark_logo_excluded:
asset_vault_record:
```

CC0라는 사실이 **우리 프로젝트에 미적으로 적합함**을 의미하지 않는다. 최종 UI가 세계관과 맞지 않으면 prototype/reference 전용으로 남긴다.

---

# Asset material classification

하나의 이미지/화면을 reusable 후보로 볼 때 다음 중 하나로 분류한다.

| Classification | 의미 |
|---|---|
| `REUSE_AS_IS` | 동일 프로젝트/맥락에서 그대로 재사용 가능 |
| `VARIANT_SEED` | base는 유지하고 상태/표정/조명 등 variant 생산 |
| `STRUCTURE_PATTERN` | 픽셀이 아니라 레이아웃/레이어/조립 구조만 재사용 |
| `STYLE_DNA` | 재질·선·명암·밀도 같은 추상 시각 규칙만 참고 |
| `REBUILD_FOR_REUSE` | 원본은 one-off지만 semantic part를 새로 만들어 재사용 |
| `ONE_OFF_KEEP` | 한 장으로 남기는 것이 더 좋음 |
| `REJECT_REUSE` | 품질/권리/일관성/비용 때문에 재사용하지 않음 |

---

# Project-specific visual mapping

| Project | 우선 module | 프로젝트-specific skin |
|---|---|---|
| `COC_FICTION` | RM-VIS-003, RM-VIS-005 | 회차/장면 mood, 인물/세력 visual reference |
| `GRIMOIRE` | RM-VIS-001~005 | 마도학교·글자/회로·주문 시각 언어 |
| `SWITCHY` | RM-VIS-001, RM-VIS-002 | 선로·화물·스위치의 명확한 semantic 표시 |
| `TETRIS` | RM-VIS-001, RM-VIS-002 | 프로젝트 고유 퍼즐/전투 skin; Tetris trade dress 복제 금지 |
| `URBAN_LEGEND` | RM-VIS-001/002/003/005 | 현대 괴이 조사·기관 UI·인물 상태 |
| `NINJA_SURVIVAL` | RM-VIS-001/002/004 | 닌자 skill/백팩/위험 telegraph |
| `MY_LITTLE_BOAT` | RM-VIS-001/002/003 | 잔잔한 항해·날씨·사진/수집 mood |
| `BLACKSMITH` | RM-VIS-001/002 | 단조/강화/위험/품질 semantic |
| `TEN_PACES` | RM-VIS-001/002/004 | 계획 단계·거리·의도/replay readable state |
| `OMENWARD` | RM-VIS-001/002/004 | 룰렛 확률·배치·wave threat·전술 timing |

`RM-VIS-006`은 위 표의 gameplay/visual module을 대체하지 않고, 실제 시각 제작이 필요한 프로젝트에서만 선택적으로 붙는 production adapter다.

---

# Rights & similarity guard

- 경쟁작의 고유 UI layout, 캐릭터, 아이콘, 배경 composition을 raster/template로 복제하지 않는다.
- 동일 장르에서 흔한 semantic 필요를 프로젝트 고유 표현으로 다시 설계한다.
- 외부 asset을 직접 사용할 때는 실제 license/provenance를 Asset Vault에 기록한다.
- 프로젝트가 상표/trade dress 위험이 있는 reference를 사용하면 `RIGHTS_REVIEW_REQUIRED`를 유지한다.
- 생성형 변형은 “원본에 없던 픽셀”을 관찰된 source layer처럼 취급하지 않는다.
- provider/model 교체는 입력 reference에 대한 사용 권리와 최종 결과의 similarity/terms review를 우회하지 않는다.

# Validation

```text
asset/material candidate
→ rights/provenance
→ primary-use visual review
→ actual target resolution
→ input/readability/accessibility state review
→ consistency against project visual canon
→ reuse value review
→ PROJECT_ASSET_APPROVED only through project owner
```

`VISUAL_CREATIVE_PROVIDER_ADAPTER`를 사용한 경우 `HUMAN_EDIT_DELTA`와 provider/model/terms provenance를 함께 남긴다. provider가 빠르다는 사실만으로 quality·consistency·rights 검토를 PASS 처리하지 않는다.

이 문서는 visual module 계약을 정의했지만 실제 project-specific sprite sheet, UI atlas, background kit, portrait variants를 생성하지 않았다. 해당 산출물은 각 프로젝트 Art/Visual 단계에서 별도 제작·검증한다.
