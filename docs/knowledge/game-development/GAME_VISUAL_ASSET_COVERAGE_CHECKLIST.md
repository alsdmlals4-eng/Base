# 게임 Visual Asset Coverage 체크리스트

## 0. 목적과 권위 경계

이 문서는 게임 프로젝트에서 **필요한 이미지·시각 자산의 종류와 상태군을 빠뜨리지 않았는지** 확인하는 공용 coverage 기준이다.

```text
COVERAGE_CHECK_ONLY
NOT_A_SECOND_ASSET_CANON
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
PRODUCTION_INFORMATION
INFORMATION_ARTIFACT_NOT_IMAGE_ASSET
TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
```

이 체크리스트는 실제 자산 원장이나 승인 상태 머신이 아니다.

- 무엇을 만들 가치가 있는지는 `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`가 소유한다.
- 생성·편집·검수·명시적 승인 경계는 `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`와 `designing-art-prompts-and-technique-cards`가 소유한다.
- 실제 승인 파일·경로·권리·promotion은 프로젝트 Asset/Manifest/Vault owner가 소유한다.
- 실제 적용과 플레이 화면 사실은 repository/runtime evidence가 소유한다.
- 사람용 Visual Bible·Asset Gallery는 프로젝트 Notion의 `NOTION_HUMAN_FACING_CANON`을 따른다.

따라서 coverage row에는 **기존 requirement/asset/evidence를 링크**하고, 동일 정보를 별도 정본으로 복제하지 않는다.

### 0.1 정보 산출물과 이미지 자산 분리

`PRODUCTION_INFORMATION`은 제작자와 AI가 프로젝트를 이해·비교·구현하기 위해 알아야 하는 정보다. 시스템 설명, 세계관, 인물·세력 관계, 관계도, 제작 체크리스트, 밸런스 구조, Flow, 구현 계약 같은 정보는 필요하면 **계속 생성·갱신한다**.

다만 이런 정보의 존재만으로 이미지 생성 backlog를 만들지 않는다.

```text
INFORMATION_ARTIFACT_NOT_IMAGE_ASSET
→ TEXT_TABLE_FLOW_DB_FIRST
→ Markdown / Notion text / table / database / Mermaid / Flow / JSON 등으로 먼저 표현
→ 실제 게임·제품 소비처가 이미지 자체를 요구할 때만 Visual Requirement Gate로 전달
```

- 제작자·AI 이해가 목적이면 텍스트·표·DB·Mermaid·Flow처럼 수정·검색·비교 가능한 형식을 우선한다.
- 문서를 보기 좋게 꾸미기 위한 설명용 시트, 캐릭터 설명판, 세계관 설명 포스터, 관계 설명 이미지 자체는 기본 image-generation requirement가 아니다.
- 관계도·시스템도·세계관 구조도는 필요하면 만든다. 다만 기본 형식은 구조화 데이터와 텍스트 기반 diagram이며, 그 자체를 고해상도 생성 이미지로 만들 이유가 되지 않는다.
- 게임 내 튜토리얼·도감·세력 관계 UI처럼 플레이어가 실제로 소비하는 설명 visual은 `PLAYER_FACING_EXPLANATORY`로 image asset 후보가 될 수 있다.
- store capsule·key art·trailer thumbnail처럼 게임 runtime 밖이라도 실제 배포·판매 경로가 소비하는 시각물은 `PRODUCT_DISTRIBUTION` consumer로 인정한다.

`ACTUAL_CONSUMER_REQUIRED`: 이미지 생성 후보에는 최소한 다음이 특정되어야 한다.

```yaml
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_surface:
primary_use:
validation:
```

`consumer_surface`가 단순 `문서 설명용`, `AI 이해용`, `체크리스트 장식용`뿐이면 이미지 생성 대상으로 올리지 않는다. 아직 구현 전이어도 실제 게임에 들어갈 구체적인 screen/scene/asset slot을 설계·검증하는 목업이면 `PLANNED_GAME_SURFACE`로 기록할 수 있다.

## 1. Visual Asset Coverage Preflight

프로젝트 전체, 화면군, 캐릭터군, 적군, UI군, 아이템군, 환경군, 마케팅 asset set을 계획하거나 이미지 생성을 시작할 때 다음 순서로 확인한다.

```text
current Project canon / stage / target flow
→ production information인지 먼저 판정
→ PRODUCTION_INFORMATION이면 TEXT_TABLE_FLOW_DB_FIRST로 route-out
→ image asset 후보이면 actual consumer / consumer surface 확인
→ existing approved asset / current implementation / reusable source 조사
→ 이 문서에서 해당되는 coverage item만 선택
→ 적용 여부 + 누락 + STATE_FAMILY_COMPLETENESS 판정
→ 필요한 gap만 Visual Requirement Gate로 전달
→ requirement_id / reuse decision 연결
→ Image Conversation Approval Gate
→ generate / edit / source / reuse
→ candidate QA + explicit approval
→ promotion / implementation
→ runtime validation
→ coverage readback
```

`NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`:

- `GAP_BLOCKING` 또는 `GAP_NONBLOCKING` 발견만으로 이미지를 자동 생성하지 않는다.
- gap 발견은 사용자 승인 없는 batch 확대, 다음 포즈 자동 생성, 전체 캐릭터군 자동 생산 권한이 아니다.
- 한 장의 명시적 사용자 요청을 전체 프로젝트 asset inventory 제작으로 확대하지 않는다.
- 재사용·기존 자산·표준 UI로 해결되는 항목을 신규 생성으로 바꾸지 않는다.
- `PRODUCTION_INFORMATION` 누락을 image coverage gap으로 바꾸지 않는다. 필요한 정보 자체는 적합한 텍스트·표·Flow·DB 형식으로 보완한다.

## 2. Coverage 상태

`coverage_status`는 다음 값만 사용한다.

| 상태 | 의미 |
|---|---|
| `NOT_REVIEWED` | 아직 적용 여부를 검사하지 않음 |
| `NOT_APPLICABLE` | 현재 프로젝트·단계·소비처에는 불필요하며 이유가 있음 |
| `COVERED_EXISTING` | 기존 승인 자산·시스템·구현으로 이미 충족 |
| `REQUIREMENT_LINKED` | 필요한 항목이며 기존/신규 `requirement_id`에 연결됨 |
| `GAP_BLOCKING` | 현재 목표 화면·흐름·검증을 막는 누락 |
| `GAP_NONBLOCKING` | 필요하지만 현재 목표 완료를 막지는 않는 누락 |
| `DEFERRED_BY_DECISION` | 가치가 있으나 현재 단계에서 의도적으로 보류 |

`coverage_status`는 `PLANNED / GENERATED_EXPLORATION / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED` 같은 asset lifecycle을 대체하지 않는다.

### 최소 기록

```yaml
coverage_item_id:
category:
surface_or_flow:
project_stage:
player_question:
required_role:
applicable: YES | NO | UNVERIFIED
coverage_status:
state_family:
state_family_status: NOT_REVIEWED | COMPLETE | PARTIAL | NOT_APPLICABLE
source_or_requirement_id:
consumer_kind:
consumer:
primary_use:
validation:
note:
```

## 3. 단계별 적용 범위

### Concept

방향을 가르는 최소 세트만 본다.

- 대표 gameplay 화면 또는 구조 목업 — 실제 planned game surface를 검증할 때
- 핵심 캐릭터/대상/환경의 identity anchor — 실제 제품 visual identity와 연결될 때
- 핵심 정보 위계와 UI 방향
- visual style / palette / value / material / lighting 기준
- 필요하면 store first-impression 가설

세계관·관계·시스템 이해 자체가 목적이면 먼저 `PRODUCTION_INFORMATION`으로 문서화한다. 전체 production asset library를 완성 조건으로 만들지 않는다.

### PoC / Technical Spike

- 기능 검증용 placeholder 허용
- 핵심 상호작용의 최소 readable state
- 위험/선택/성공/실패를 판독할 수 있는 최소 feedback
- 성능·import·sprite slicing 등 기술 가설 검증에 필요한 최소 자산

PoC placeholder를 최종 player-experience PASS로 해석하지 않는다.

### Vertical Slice

`shipping-intent` player-facing 경로에서는 P0/P1과 필요한 P2를 목표 품질에 가깝게 만든다.

- 핵심 캐릭터·적·환경
- 실제 UI/HUD
- 핵심 skill/combat VFX
- enemy telegraph
- interaction/feedback/reward
- 필요한 audio/VFX 연계 상태
- 실제 target resolution에서 가독성

플레이어가 실제로 보는 Slice 경로에 임시 player-facing placeholder를 남기지 않는다.

### Production

- 반복 asset set과 variation
- `STATE_FAMILY_COMPLETENESS`
- localization 가능한 graphics/text 분리
- 접근성 대체 cue
- import/performance/naming/atlas 정책
- provenance/rights
- implementation path와 runtime 검증

### Release

`PLATFORM_SPEC_RECHECK_REQUIRED`를 적용한다.

- Steam/Google Play/기타 target platform의 **현재 공식 규격·수량·콘텐츠 규칙을 출시 시점에 다시 조회**한다.
- Base에 과거 pixel size나 수량을 영구 정답처럼 복제하지 않는다.
- store screenshot은 해당 플랫폼 정책이 요구하는 실제 gameplay 표현인지 다시 확인한다.

## 4. 공용 Coverage Catalog

아래는 **후보군**이다. 각 프로젝트에 전부 적용하지 않는다. `Delete Test`, current stage, genre, camera, input, target platform과 **actual consumer**로 applicability를 먼저 판정한다. Foundation/reference 항목이 필요하다는 사실만으로 생성 이미지를 만들지 않는다.

### A. Visual Direction / Foundation

- [ ] Art/Visual Bible 또는 승인된 visual north star
- [ ] 대표 gameplay screen / composition anchor
- [ ] palette와 value/contrast 기준
- [ ] silhouette/shape language
- [ ] line/texture/material grammar
- [ ] lighting/shadow grammar
- [ ] typography 원칙과 실제 text-layer 분리 기준
- [ ] iconography grammar
- [ ] UI family / panel / border / focus treatment
- [ ] VFX grammar
- [ ] camera/view/framing 기준
- [ ] base design resolution / target aspect / scaling 원칙
- [ ] pixel-art이면 pixel density/grid/integer scaling 원칙
- [ ] approved reference + Keep / Avoid / Do Not Drift

### B. Player / Character / NPC

- [ ] gameplay representation: sprite/model/portrait 중 실제 소비되는 것
- [ ] silhouette와 gameplay-size readability
- [ ] direction variants: 카메라/이동 구조에서 실제 필요한 방향만
- [ ] idle
- [ ] movement: walk/run/fly/swim 등 실제 행동만
- [ ] attack / cast / skill
- [ ] hit / hurt
- [ ] death / disable
- [ ] interact / use
- [ ] dodge / jump / land / block / parry 등 mechanic이 있을 때만
- [ ] equipment/weapon visible variant가 gameplay에 필요할 때
- [ ] portrait / bust-up / expression set가 대화·서사에 필요할 때
- [ ] status/buff/debuff visibility가 캐릭터 위에 필요할 때

### C. Enemy / Boss

- [ ] base gameplay representation
- [ ] normal / elite / boss의 구분 cue
- [ ] movement/idle
- [ ] attack wind-up
- [ ] attack active
- [ ] attack recovery
- [ ] hit/death
- [ ] AoE/range/trajectory telegraph
- [ ] boss phase / enraged / vulnerable 등 실제 mechanic state
- [ ] target/aggro/selected cue가 필요한 경우

### D. Environment / Tile / Prop / Interactable

- [ ] background / biome / room visual
- [ ] floor / wall / boundary / road / terrain
- [ ] tile 기반이면 edge/corner/transition/end/intersection 중 실제 autotile set
- [ ] foreground/background depth cue
- [ ] door/gate/chest/lever/button/harvestable/trap 등 interactable
- [ ] normal / highlighted-targeted / usable / unavailable
- [ ] open / closed
- [ ] active / inactive
- [ ] intact / damaged / destroyed
- [ ] movable/pushable/blocked state가 mechanic에 있을 때
- [ ] environmental hazard telegraph

### E. Building / Facility / Construction

- [ ] icon / world representation
- [ ] placement preview
- [ ] valid / invalid placement
- [ ] constructing
- [ ] completed
- [ ] upgrading
- [ ] level/tier visual difference가 판단에 필요할 때
- [ ] inactive/resource-shortage/production state
- [ ] damaged/destroyed

### F. Item / Equipment / Resource / Currency

- [ ] inventory/list icon
- [ ] world pickup/drop representation가 있을 때
- [ ] held/equipped visual가 있을 때
- [ ] selected
- [ ] equipped
- [ ] locked/unavailable
- [ ] new/unread
- [ ] rarity/tier cue가 판단에 필요할 때
- [ ] stack/resource/currency family
- [ ] craft/material/quest/key item family가 실제 시스템에 있을 때

### G. Skill / Combat / VFX / Feedback

- [ ] skill/passive/ultimate icon 중 실제 UI에 필요한 종류
- [ ] ready / selected / disabled / cooldown
- [ ] cast/start effect
- [ ] projectile / trail
- [ ] impact/hit
- [ ] damage / critical
- [ ] miss / block / parry
- [ ] heal / shield
- [ ] buff/debuff/status
- [ ] death/defeat effect
- [ ] AoE/danger/safe-area cue
- [ ] projectile path / line of fire cue가 판단에 필요할 때
- [ ] effect가 subject identity와 important UI를 가리지 않는지

### H. UI / HUD / System Components

- [ ] panel/window/container
- [ ] button / icon button
- [ ] tabs
- [ ] checkbox/radio/toggle
- [ ] slider/progress
- [ ] scroll
- [ ] tooltip
- [ ] popup/dialog
- [ ] cursor/focus/navigation indicator
- [ ] HP/MP/energy/resource
- [ ] EXP/level/progression
- [ ] score/timer/wave/stage/objective
- [ ] currency/inventory/slot
- [ ] minimap/map marker가 실제로 필요할 때
- [ ] notification/new/warning/error/success
- [ ] loading/progress/transition
- [ ] empty/error/disabled state

### I. Common UI Icons

- [ ] confirm/cancel/close/back/home
- [ ] settings/save/load/delete/edit
- [ ] info/help/warning/error
- [ ] search/filter/sort
- [ ] lock/unlock/favorite
- [ ] play/pause/skip/speed
- [ ] directional/navigation arrows

공용 icon set이 이미 역할을 충족하면 `REUSE_SYSTEM` 또는 `REUSE_PROJECT`를 우선한다.

### J. Input Prompt

지원 입력장치에 대해서만 만든다.

- [ ] keyboard keycap prompt
- [ ] mouse button/wheel prompt
- [ ] gamepad face button / d-pad / stick / shoulder / trigger
- [ ] touch tap/hold/swipe/drag/pinch
- [ ] 현재 입력장치 변화 시 prompt 교체가 필요한지
- [ ] remapping을 지원할 때 hard-coded glyph가 깨지지 않는지

### K. Map / Node / Progression

- [ ] map/world overview
- [ ] current position/node
- [ ] reachable/available
- [ ] selected
- [ ] locked
- [ ] completed/cleared
- [ ] event/shop/reward/boss node가 실제로 있을 때
- [ ] path/connection/branch
- [ ] available/unavailable route 차이

### L. Narrative / Story / Character Presentation

- [ ] portrait 또는 bust-up
- [ ] expression set
- [ ] pose/cut-in
- [ ] event CG / chapter image
- [ ] cutscene background
- [ ] intro/ending visual
- [ ] faction/relationship/location visual — 게임 내 도감·관계 UI·지도 등 실제 player-facing consumer가 있을 때

제작자·AI가 세력·관계·위치를 이해해야 한다는 이유만이면 `PRODUCTION_INFORMATION`으로 관계도/표/DB/Mermaid를 만들고 이미지 생성 requirement로 올리지 않는다. 서사 visual이 없는 장르에 억지로 추가하지 않는다.

### M. Tutorial / Guidance / Accessibility

- [ ] tutorial arrow/pointer
- [ ] highlight/focus frame
- [ ] target/interaction hint
- [ ] input demonstration
- [ ] success/failure/recovery guidance
- [ ] subtitle/caption background와 speaker identifier가 필요한 경우
- [ ] 중요한 상태가 **색 하나에만 의존하지 않는** shape/icon/pattern/text cue
- [ ] scalable UI/text와 고대비 상황에서 식별 가능한 자산
- [ ] 적/아군/위험/안전이 color-vision 차이에서도 구별되는 semantic cue

튜토리얼·도감·도움말처럼 게임에서 직접 소비되는 설명 visual은 `PLAYER_FACING_EXPLANATORY`로 분류한다.

### N. Reward / Progress / Outcome

- [ ] item/currency pickup
- [ ] EXP gain
- [ ] level-up
- [ ] unlock
- [ ] rare reward
- [ ] achievement
- [ ] stage clear/victory
- [ ] defeat/game over
- [ ] retry/continue/next-step affordance

### O. Main Menu / System Screens

- [ ] logo/title
- [ ] title background 또는 gameplay-derived presentation
- [ ] new/start/continue/load
- [ ] settings
- [ ] accessibility/language가 지원될 때
- [ ] save/load/profile
- [ ] credits/quit
- [ ] result screen
- [ ] loading screen

### P. Marketing / Platform / Store

`PLATFORM_SPEC_RECHECK_REQUIRED`.

- [ ] game logo/logotype
- [ ] key art
- [ ] app/game icon
- [ ] store capsule/header/vertical/library assets — target platform이 요구할 때
- [ ] screenshots
- [ ] trailer thumbnail
- [ ] announcement/update/event artwork
- [ ] press kit visuals
- [ ] social thumbnail/banner가 실제 홍보 경로에 있을 때
- [ ] platform rules에 맞는 text/logo/content 제한
- [ ] store screenshot이 실제 gameplay를 정확히 보여주는지

이 범주는 runtime 밖이지만 실제 storefront/홍보/배포 소비처가 명확한 `PRODUCT_DISTRIBUTION` 시각물이다.

### Q. Development / Debug / Placeholder

최종 제품 asset과 명확히 분리한다.

- [ ] player/enemy/item/environment placeholder
- [ ] collision visualization
- [ ] spawn point
- [ ] navigation/path
- [ ] trigger/interaction area
- [ ] camera bounds
- [ ] AI state debug
- [ ] damage/range/telegraph debug
- [ ] performance/overdraw/atlas debug가 필요할 때

Technical Spike에서 유효한 placeholder라도 shipping-intent player-facing evidence로 승격하지 않는다. Debug 표현은 가능한 한 engine primitive·standard icon·text overlay를 사용하고, 개발 편의를 이유로 생성 이미지 제작을 기본값으로 만들지 않는다.

## 5. STATE_FAMILY_COMPLETENESS

대표 이미지 한 장이 있다고 해당 component가 완성된 것은 아니다. 소비처에 필요한 상태군을 먼저 정의하고 `state_family_status`를 기록한다.

### UI Control

```text
Normal
→ Hover (pointer가 있을 때)
→ Pressed
→ Disabled
→ Focus (keyboard/gamepad navigation이 있을 때)
→ Selected / Checked (상태형 control일 때)
```

### Enemy Attack

```text
Idle/Seek
→ Wind-up / Telegraph
→ Active
→ Recovery
→ Hit/Interrupt (지원 시)
→ Death/Disable
```

### Player Character

```text
Idle
→ Move
→ Attack/Use
→ Hit
→ Death/Disable
+ mechanic-specific Skill / Interact / Dodge / Jump / Block
```

### Interactable

```text
Default
→ Targeted/Highlighted
→ Usable | Unavailable
→ Active/Triggered
→ Open/Closed 또는 Intact/Damaged/Destroyed (해당 시)
```

### Item / Equipment

```text
Inventory
→ World pickup (해당 시)
→ Selected
→ Equipped (해당 시)
→ Locked/Unavailable
→ New/Unread 또는 Rarity/Tier cue (해당 시)
```

### Map Node

```text
Current
→ Reachable
→ Selected
→ Locked
→ Completed
+ Event / Shop / Reward / Boss semantic variant
```

### Building

```text
Preview
→ Valid/Invalid placement
→ Constructing
→ Complete
→ Upgrading
→ Damaged/Destroyed (해당 시)
```

### Status Effect

```text
Icon
→ Start cue
→ Active cue
→ End/cleanse cue
+ character overlay가 실제 판독에 필요할 때만
```

`COMPLETE`는 프로젝트가 요구하는 상태가 모두 있다는 뜻이지 위 예시의 모든 상태를 강제한다는 뜻이 아니다.

## 6. Technical Consumption Contract

실제 게임에서 소비되는 asset은 필요한 항목만 requirement/handoff에 기록한다.

```yaml
source_master:
export_format:
resolution_or_design_size:
aspect_ratio:
crop_and_safe_area:
alpha_or_mask:
color_space:
filter_mode:
mipmap:
compression:
atlas_or_sprite_sheet:
slicing:
pivot_or_anchor:
nine_patch_or_scaling_region:
animation_fps_loop:
naming_and_variant:
engine_import_profile:
localization_text_separation:
performance_budget:
rights_or_provenance:
```

원칙:

- Godot 2D/UI는 base design size와 실제 target aspect/resolution에서 확인한다.
- pixel art는 필터링·integer scaling·pixel density가 스타일을 깨뜨리지 않는지 확인한다.
- 축소되는 큰 이미지/3D texture는 mipmap/compression 필요성을 실제 사용처 기준으로 검토한다.
- atlas/sprite sheet는 draw-call/packing/반복 생산에 이득이 있을 때 사용하며 모든 asset을 강제 atlas화하지 않는다.
- UI skin은 stretch 가능한 영역과 고정 corner가 필요하면 9-patch 또는 의미적으로 재구축 가능한 component를 우선한다.
- 이미지 안에 굳은 텍스트는 localization·수정 비용을 키우므로 가능한 경우 art와 실제 typography layer를 분리한다.
- naming은 같은 asset의 role/variant/state를 구별할 수 있어야 하며 특정 엔진의 prefix 체계를 프로젝트에 무조건 복사하지 않는다.

## 7. 3D 조건부 모듈

3D 프로젝트에서만 적용한다.

### Mesh / Rig / Animation

- [ ] player/character/enemy/NPC mesh
- [ ] weapon/item/prop/environment/building mesh
- [ ] skeleton/rig
- [ ] animation clips
- [ ] facial blend shape / morph가 필요할 때
- [ ] LOD가 성능 목표에 필요할 때
- [ ] collision mesh
- [ ] lightmap UV가 실제 lighting pipeline에 필요할 때

### Material / Texture

실제 shader/material pipeline에 필요한 map만 사용한다.

- [ ] Base Color / Albedo
- [ ] Normal
- [ ] Roughness
- [ ] Metallic
- [ ] AO
- [ ] Emission
- [ ] Opacity/Mask

PBR map을 “3D니까 전부 필요”로 판단하지 않는다.

## 8. Benchmark ADOPT / ADAPT / REJECT

### ADOPT

- Godot: 2D/UI의 base design size, 다양한 해상도·종횡비·scale을 실제 target에서 검증한다.
- Godot: image import/compression/filter/mipmap 선택을 asset usage에 맞춘다.
- Steam: store asset은 역할별로 관리하고 release 시 current official rule/spec을 재확인한다.
- 접근성: 중요한 의미를 color 하나에만 의존하지 않고 semantic redundancy를 제공한다.
- 제작 정보: 구조화 텍스트·표·Flow·DB를 editable source of truth로 유지하고 이미지와 분리한다.

### ADAPT

- sprite atlas/variant 관리: 반복 asset과 성능에 실제 이득이 있는 프로젝트에서만 사용한다.
- naming convention: type/role/state/variant가 명확하도록 적용하되 Unreal 등 다른 엔진 고유 prefix를 그대로 강제하지 않는다.
- marketing asset family: 실제 target storefront만 선택한다.
- planning mockup: 실제 planned game surface를 검증하는 경우에만 이미지 후보로 사용한다.

### REJECT

- 모든 게임에 같은 asset 수량·방향 수·상태 수를 강제한다.
- 현재 platform pixel size를 Base 장기 canon으로 하드코딩한다.
- 보기 좋은 concept art를 gameplay screenshot/runtime proof로 취급한다.
- coverage gap을 사용자 승인 없는 자동 생성 queue로 바꾼다.
- coverage table을 Manifest/Notion Asset/Runtime truth와 경쟁하는 second canon으로 만든다.
- 제작자·AI 설명 정보가 필요하다는 이유만으로 별도 설명용 이미지 시트를 만든다.
- actual consumer가 없는 이미지 후보를 production asset backlog에 넣는다.

## 9. 이미지 생성 직전 체크

프로젝트 이미지 생성·편집을 실제로 호출하기 직전에 다음만 확인한다.

- [ ] 정확한 Project relation과 current canon을 읽었다.
- [ ] 현재 목표 screen/flow/use를 확인했다.
- [ ] 먼저 `PRODUCTION_INFORMATION`인지 판정했고, 정보 산출물이면 `TEXT_TABLE_FLOW_DB_FIRST`로 route-out했다.
- [ ] `ACTUAL_CONSUMER_REQUIRED`: `consumer_kind / consumer_surface / primary_use / validation`이 구체적이다.
- [ ] consumer가 문서 설명·AI 이해·체크리스트 장식뿐이면 이미지 생성을 중단한다.
- [ ] 관련 coverage item의 applicability를 판정했다.
- [ ] 기존 승인 asset/reference/reuse 후보를 먼저 확인했다.
- [ ] `coverage_status`와 필요한 `state_family_status`를 확인했다.
- [ ] 신규 제작이 필요하면 Visual Requirement Gate에서 `requirement_id`가 선정됐다.
- [ ] output ratio/resolution/crop/alpha/text 처리와 engine consumption 조건을 정했다.
- [ ] 접근성 대체 cue가 필요한 상태인지 확인했다.
- [ ] 외부 reference의 provenance/rights/similarity 위험을 확인했다.
- [ ] 현재 사용자 메시지가 실제 이미지 생성/편집을 명시적으로 승인했는지 기존 Conversation Gate로 확인했다.
- [ ] 한 gap을 이유로 승인되지 않은 다음 이미지·variant·batch를 자동 추가하지 않는다.

## 10. 생성 후 Coverage Readback

생성 성공만으로 coverage가 닫히지 않는다.

```text
candidate generated
→ visual QA
→ user/project approval
→ correct Project attach + readback
→ product promotion when appropriate
→ implementation/runtime evidence when required
→ linked coverage row readback
```

- 기존 자산으로 해결됐으면 `COVERED_EXISTING`과 source를 기록한다.
- requirement를 만들었지만 아직 승인/구현되지 않았으면 `REQUIREMENT_LINKED` 그대로 둔다.
- current target을 막는 실제 누락이면 `GAP_BLOCKING`을 숨기지 않는다.
- project Decision으로 미뤘으면 `DEFERRED_BY_DECISION`과 이유를 남긴다.

## 11. 적대적 검토 기준

다음 중 하나라도 발생하면 coverage 설계를 교정한다.

1. checklist 때문에 project scope가 불필요하게 폭증했다.
2. `NOT_APPLICABLE`을 허용하지 않아 장르와 무관한 asset을 강제했다.
3. 대표 image만 있고 required state family가 빠졌다.
4. UI state가 color 하나로만 구별된다.
5. enemy attack은 있으나 wind-up/telegraph/recovery가 없어 판단 불가능하다.
6. final visual candidate인데 target resolution에서 읽히지 않는다.
7. export/import/filter/mipmap/atlas/slicing/pivot 같은 실제 소비 조건이 누락돼 구현 시 재작업이 발생한다.
8. platform/store asset이 오래된 규격을 그대로 따른다.
9. concept/reference가 runtime/gameplay evidence처럼 사용된다.
10. coverage row가 requirement/asset/manifest/runtime status를 중복 소유한다.
11. gap 발견이 자동 image chain 또는 대량 batch 생성으로 이어졌다.
12. project-approved identity보다 재사용 편의를 우선해 visual identity가 약화됐다.
13. 시스템 설명·세계관·관계도·제작 체크리스트 같은 `PRODUCTION_INFORMATION`이 누락되거나, 반대로 그것을 생성 이미지로 대체했다.
14. actual game/product consumer를 특정하지 못한 설명용 이미지 시트가 생성 backlog에 남았다.
15. 실제 게임 내 설명 visual인데 `PLAYER_FACING_EXPLANATORY` 소비처를 기록하지 않아 문서용 이미지와 구분되지 않는다.

## 12. 완료 판정

Coverage 검사의 완료는 “모든 checkbox가 체크됨”이 아니다.

```text
해당 목표 범위의 모든 relevant item
→ production information과 image asset 후보가 분리됨
→ 필요한 production information은 적합한 text/table/flow/db owner에 존재함
→ image 후보는 ACTUAL_CONSUMER_REQUIRED 충족
→ applicability 판정됨
→ blocking gap 0 또는 명시적 Decision으로 처리됨
→ 필요한 state family 정의됨
→ requirement / existing asset / defer decision에 연결됨
→ 실제 생성이 필요하면 기존 approval gate를 통과함
```

`CLEAN_COVERAGE_EXIT`는 해당 목표·단계의 coverage가 정리됐다는 뜻일 뿐, 모든 이미지가 생성·승인·Godot 적용·runtime 검증됐다는 뜻이 아니다.