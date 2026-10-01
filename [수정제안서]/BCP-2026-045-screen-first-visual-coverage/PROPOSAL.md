# BCP-2026-045 · 화면 인벤토리 선행형 게임 시각 자산 Coverage

## 출처와 상태

- 출처: 사용자 제공 다중 프로젝트 화면 구성 예시와 기존 Base `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md` 재검토
- 기준 Base: `f5b181b68af4e496dc0873a3070d0b25d12c9f88`
- 제출일: `2026-08-27`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `재현된 운영 누락`
- 승인 근거: 사용자 메시지 `좋아 만들어주고 교정작업까지 진행해줘` — 화면 단위 필수 이미지 추적 템플릿 작성과 Base 교정을 함께 승인

## 관찰과 증거

현행 Base는 캐릭터, 적, 환경, UI, 메인 메뉴, 결과, 마케팅 등 자산 종류와 상태군을 폭넓게 열거하고 `ACTUAL_CONSUMER_REQUIRED`, `STATE_FAMILY_COMPLETENESS`, `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`를 이미 보유한다.

그러나 감사의 기본 시작점이 **자산 카테고리**라서 다음과 같은 누락이 여전히 가능하다.

1. 메인 화면, 시작 선택, 허브, 전투 준비, 전투, 특수 연출, 결과·보상, 성장, 기록·도감, 설정·일시정지, 게임오버·엔딩처럼 플레이어가 실제로 통과하는 **화면군 전체**를 먼저 나열하지 않고 일부 자산 종류만 채운다.
2. 화면 전체의 구도·배경·정보 위계·첫인상을 검증하는 `SCREEN_DESIGN_REFERENCE` 또는 실제 화면 목업이 빠져도 캐릭터·아이콘 몇 종이 있다는 이유로 준비 완료처럼 보인다.
3. 반대로 하나의 합성 화면 목업을 실제 런타임에서 분리 소비해야 하는 배경, UI component, icon, sprite, VFX, text layer와 동일시한다.
4. `필수 시각 표현`과 `필수 이미지 파일`을 구분하지 않아 Godot Theme, StyleBox, shader, text, primitive drawing으로 구현할 요소까지 신규 bitmap 생성 backlog로 바꿀 수 있다.

따라서 기존 자산 카탈로그를 폐기하거나 두 번째 asset canon을 만들지 않고, 그 앞에 **화면 인벤토리 선행 계약**이 필요하다.

## 일반화 후보

### 1. `SCREEN_SURFACE_INVENTORY_FIRST`

프로젝트 전체 또는 Vertical Slice의 시각 자산 범위를 감사할 때는 자산 종류보다 먼저 플레이어 흐름에 존재하는 모든 target screen/surface를 나열한다.

```text
TARGET_PLAYER_FLOW
→ SCREEN_SURFACE_INVENTORY
→ SCREEN_TO_ASSET_COVERAGE_MATRIX
→ STATE_AND_VARIANT_FAMILY
→ IMPLEMENTATION_MODE
→ REQUIREMENT / REUSE / DEFER
```

최소 후보군은 다음을 검토하되, 장르·단계상 불필요하면 이유 있는 `NOT_APPLICABLE`로 남긴다.

- boot / splash / title / main menu
- new game / continue / load / profile
- character·class·weapon·deck·build select
- hub / home / world map / route / stage select
- exploration / field / puzzle / management / core gameplay
- dialogue / event / cutscene / player-facing tutorial
- battle preparation / battle / tactical overlay / special cut-in
- pause / settings / accessibility / language
- inventory / equipment / skill / upgrade / shop / crafting
- codex / archive / journal / quest / manual
- result / reward / defeat / retry / game over / ending
- loading / transition / reconnect / error / empty state
- store / platform / distribution surface when in current target scope

### 2. `SCREEN_LEVEL_VISUAL_IS_A_DELIVERABLE`

실제 `GAME_RUNTIME` 또는 `PLANNED_GAME_SURFACE` 소비처가 있는 화면은, 화면 전체의 구도·배경·정보 위계·상호작용·첫인상을 검증하는 screen-level deliverable을 가진다.

이 deliverable은 다음 중 하나일 수 있다.

- 구현된 실제 runtime screen
- Figma/Notion/UI layout 등 editable screen specification
- 실제 화면을 검증하는 approved mockup/reference
- 기존 승인 screen의 재사용·adapt evidence

모든 화면에 별도 고해상도 생성 이미지를 강제하지 않는다.

### 3. `COMPOSITE_REFERENCE_RUNTIME_COMPONENT_SEPARATION`

화면 합성 목업과 실제 런타임 자산을 구분한다.

```yaml
screen_design_reference:
  purpose: composition / hierarchy / visual target
runtime_consumables:
  - background_or_world_layer
  - character_or_object_assets
  - ui_components_and_icons
  - state_and_variant_assets
  - vfx_and_telegraph
  - text_or_localization_layer
  - technical_mask_shader_texture
```

합성 화면 한 장이 존재해도 하위 runtime consumer가 준비된 것은 아니다. 반대로 하위 자산이 있어도 전체 화면의 정보 위계와 첫인상이 검증된 것은 아니다.

### 4. `VISUAL_REQUIREMENT_NOT_ALWAYS_IMAGE_FILE`

각 row는 구현 방식을 명시한다.

```text
REUSE_EXISTING
IMAGE_ASSET
VECTOR_OR_NINE_PATCH
GODOT_THEME_STYLEBOX
TEXT_OR_FONT
SHADER_OR_PROCEDURAL
ENGINE_PRIMITIVE
COMPOSITE_SCREEN_REFERENCE_ONLY
```

이미지 파일이 불필요한 표현은 `NO_NEW_IMAGE_FILE_REQUIRED`로 닫되, 화면에서 필요한 시각 역할 자체는 누락하지 않는다.

## 프로젝트 전용으로 남길 내용

- 각 프로젝트의 실제 화면명, 플레이 흐름, 화면 수, 해상도, 플랫폼, UI layout, 미술 방향
- 특정 캐릭터·배경·아이콘·VFX의 파일명과 규격
- Notion page/database ID, repository path, Godot scene/resource path
- 프로젝트별 P0/P1/P2 우선순위와 실제 승인 판단

## 적용 조건과 비사용 조건

적용:

- 프로젝트 전체 또는 Vertical Slice의 필수 화면·이미지·UI·VFX를 조사할 때
- Work에서 이미지 제작 backlog와 Codex handoff를 준비할 때
- 메인 화면을 포함한 screen set의 누락과 상태군을 확인할 때
- 기존 화면 목업을 실제 runtime asset으로 분해할 때

비사용 또는 축소:

- 사용자가 명시한 독립 이미지 한 장만 다루며 전체 프로젝트 coverage 확대를 요청하지 않은 경우
- 순수 텍스트·데이터·로직 변경으로 player-facing surface가 변하지 않는 경우
- 이미 같은 목표 범위에 대해 최신 screen inventory와 matrix가 존재하고 현재 변경이 그 일부만 갱신하는 경우

## 반례와 위험

- 모든 후보 화면을 무조건 제작하면 범위가 폭증한다. 각 row는 current target flow와 stage로 `APPLICABLE / NOT_APPLICABLE / DEFERRED`를 판정한다.
- 화면 목업을 매번 생성 이미지로 만들면 수정성·localization·implementation 비용이 증가한다. editable UI specification과 engine-native component를 우선할 수 있다.
- screen inventory가 두 번째 GDD나 asset manifest가 되면 정본 충돌이 생긴다. row는 기존 Notion/GitHub requirement·asset·runtime evidence를 링크하고 상태를 복제 소유하지 않는다.
- gap 탐지는 이미지 생성 권한이 아니다. 기존 Image Conversation Approval Gate와 one-output 경계를 유지한다.
- screen-level target만 강조하면 애니메이션·상태·텔레그래프가 다시 빠질 수 있으므로 기존 `STATE_FAMILY_COMPLETENESS`를 하위 필수 단계로 유지한다.

## 승인된 구현 범위

1. 화면 인벤토리 선행형 공용 owner 문서 추가
2. Work 채팅에 그대로 붙여넣을 수 있는 프로젝트 실행 지시문 추가
3. 화면 목업과 runtime component, 시각 requirement와 image file을 구분하는 공용 case 추가
4. focused regression contract 추가 또는 보강
5. 최소 5회 whole-state 적대적 검토 기록

## 제외·보호 범위

- 기존 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`의 asset catalog와 lifecycle 의미를 대체하지 않는다.
- 이미지 자동 생성, batch 확대, 사용자 승인 우회 권한을 추가하지 않는다.
- 프로젝트 전용 화면·수치·아트 방향을 Base에 복사하지 않는다.
- 기존 open/draft PR과 `[수정제안서]/PROPOSAL_REGISTRY.json`은 read-only다. Registry는 해당 경로의 선행 open PR 해소 후 별도 reconciliation한다.
- 새 Skill, provider, dependency, 유료 서비스, runtime code를 추가하지 않는다.

## 검증

1. Work용 template가 `SCREEN_SURFACE_INVENTORY_FIRST`와 메인 화면 포함 필수 후보군을 명시하는지 검사한다.
2. template가 `SCREEN_DESIGN_REFERENCE`와 `RUNTIME_CONSUMABLE`을 분리하는지 검사한다.
3. template가 `NO_NEW_IMAGE_FILE_REQUIRED`와 engine-native implementation mode를 허용하는지 검사한다.
4. 기존 `ACTUAL_CONSUMER_REQUIRED`, `STATE_FAMILY_COMPLETENESS`, `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`, `NOT_APPLICABLE` 경계가 유지되는지 검사한다.
5. screen inventory가 second canon 또는 자동 batch queue가 되지 않는지 5회 적대적 검토한다.

## 롤백

후속 구현 PR의 신규 screen-first owner, Work template, case, focused regression, review receipt를 한 단위로 revert한다. 기존 visual asset coverage checklist, image policy, approval gate, project asset lifecycle은 변경하지 않는다.
