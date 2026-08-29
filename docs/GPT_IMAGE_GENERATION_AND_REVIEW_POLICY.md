# GPT 이미지 생성·검수 정책

이 문서는 Base를 적용한 프로젝트에서 이미지·목업·UI 시각화·캐릭터·배경·에셋의 필요성 판정, 후보 생성, 검수, 사용자 확정, repository 등록, 실제 구현과 runtime 검증 경계를 정의한다.

```text
REPOSITORY_FIRST_CURRENT_CANON
NEED_DRIVEN_GENERATE_THEN_LOCK
ACTUAL_CONSUMER_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
EXISTING_APPROVED_ASSET_REUSE_FIRST
STYLE_CONTINUITY_REVIEW_REQUIRED
RIGHTS_AND_REFERENCE_REVIEW_REQUIRED
```

## 1. Authority와 workspace

기본 current owner는 프로젝트 GitHub repository다.

```text
REPOSITORY_HUMAN_FACING_CANON
→ GDD / Flow / Storyboard / Visual / approval decision / asset catalog

REPOSITORY_STRUCTURED_CANON
→ Markdown / JSON / game data / ASSET_MANIFEST / Scene / Resource / Test

REPOSITORY_RUNTIME_TRUTH
→ actual import / Scene connection / build / runtime / device evidence
```

Notion과 Google Sheets는 프로젝트 current authority가 명시한 고유 migration input이 있을 때만 참고한다. 신규 이미지 기획·승인·저장·동기화·완료 readback의 기본 destination이 아니다. 프로젝트의 최신 `AGENTS.md`와 current Decision이 좁은 예외를 명시하면 그 범위만 따른다.

## 2. 관련 owner

이미지 작업은 다음 owner를 중복 생성하지 않고 조합한다.

1. `docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`
2. `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`
3. `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
4. `docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`
5. `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
6. `docs/knowledge/game-development/IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`
7. `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
8. `docs/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
9. project Visual Canon / approved decisions / asset manifest / actual consumer

`GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`는 실제 화면·상태·consumer를 먼저 역산하고, `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`가 에셋 패밀리 전체 coverage를 책임진다. 생성 후보의 local-only 보관, tombstone, sync와 tracked production path로의 명시적 promotion은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`가 책임진다.

## 3. Machine contract

```text
PROJECT_REVIEW_COMPLETE
Visual Asset Coverage Preflight
Visual Requirement Gate
ACTUAL_CONSUMER_REQUIRED
PRODUCTION_INFORMATION
TEXT_TABLE_FLOW_DB_FIRST
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
NEED_DRIVEN_GENERATE_THEN_LOCK
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
EXISTING_APPROVED_ASSET_REUSE_FIRST
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
PROJECT_LOCAL_ASSET_VAULT_POLICY.md
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
STYLE_CONTINUITY_REVIEW_REQUIRED
FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
RIGHTS_AND_REFERENCE_REVIEW_REQUIRED
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

기존 `ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE`는 superseded history다. active marker는 다음과 같다.

```text
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE__SUPERSEDED
```

## 4. Visual Asset Coverage Preflight

에셋 coverage 표는 누락을 찾는 검수 owner이며 자체 생성 queue가 아니다.

```text
COVERAGE_CHECK_ONLY
NOT_A_SECOND_ASSET_CANON
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

coverage gap을 발견했다는 사실만으로 후보를 만들지 않는다. gap이 actual consumer, planned player-facing surface, product distribution 또는 현재 Blueprint 결정용 planning-board에 연결되고, current canon·승인 anchor·기존 asset 재사용 검토까지 끝난 경우에만 `NEED_DRIVEN_GENERATE_THEN_LOCK`으로 진입한다.

### 4.1 Visual Requirement Gate

이미지 생성 전에 단순 목록이 아니라 실제 필요성을 검증한다.

```yaml
requirement_id:
project:
consumer_class: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_scene_or_surface:
consumer_node_slot_or_planning_board:
primary_use:
player_or_user_decision_supported:
approved_visual_direction:
existing_asset_candidates: []
required_state_family: []
target_size_aspect_alpha_crop:
implementation_owner_or_path:
rights_and_reference_boundary:
fallback_if_unconsumed:
```

### 4.2 허용되는 consumer class

- `GAME_RUNTIME`: 실제 Scene·Node·material·UI slot·sprite·texture·cut-in 등 exact runtime consumer.
- `PLANNED_GAME_SURFACE`: 승인 Blueprint에서 구현할 실제 화면·씬·상태의 visual candidate.
- `PLAYER_FACING_EXPLANATORY`: 게임 안에서 플레이어가 규칙·선택·결과를 이해하기 위해 소비하는 manual/card/tutorial visual.
- `PRODUCT_DISTRIBUTION`: store capsule, logo, key art, trailer frame 등 실제 출시 consumer.

Blueprint 검수용 planning-board는 production asset이 아니지만, 구체적인 제품·화면·Flow 결정을 비교하는 목적이 있을 때 `GENERATED_EXPLORATION` 후보를 만들 수 있다.

### 4.3 생성하지 않는 정보 산출물

다음 제작 정보는 `PRODUCTION_INFORMATION`이며 이미지 파일보다 수정 가능한 정본이 우선이다.

```text
TEXT_TABLE_FLOW_DB_FIRST
```

- 시스템 설명
- 세계관 구조
- 관계도
- 제작 체크리스트
- 상태 전이
- 데이터 표
- asset coverage inventory
- test matrix

이 항목은 Markdown, 표, Mermaid, JSON, schema, database와 Flow로 작성한다. 이미지 파일이 실제 player-facing 또는 distribution consumer가 없다면 `DO_NOT_GENERATE`다. 구조 정보가 필요하다는 이유로 설명용 raster sheet를 남발하지 않는다.

## 5. Existing solution first

```text
EXISTING_APPROVED_ASSET_REUSE_FIRST
```

새 이미지를 만들기 전에 다음 순서로 확인한다.

1. 현재 project의 실제 구현·tracked asset
2. 사용자 승인 이미지와 visual anchor
3. 기존 시안 중 current canon과 일치하는 것
4. 수정 가능한 기존 source asset
5. Base 재사용 pattern
6. 직접 관련된 프로젝트 evidence
7. 마지막으로 신규 생성

기존 asset이 consumer를 충족하면 재사용한다. 필요한 차이가 배경 제거·crop·상태 보정처럼 identity-preserving edit이면 image editing model로 bounded edit를 검토한다. 기존 asset을 찾지 않고 비슷한 새 이미지를 만드는 것은 default가 아니다.

## 6. Generation authority

이미지 후보는 두 경로에서 만들 수 있다.

### 6.1 사용자의 current-turn explicit request

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ GENERATE_ONE_CANDIDATE_BEFORE_LOCK
```

사용자가 현재 turn에서 생성·편집을 명시하면 별도의 긴 pipeline 지시문이나 중복 사전 승인을 요구하지 않는다.

### 6.2 작업 중 확인된 구체적 필요

```text
NEED_DRIVEN_GENERATE_THEN_LOCK
→ CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
→ PROJECT_REVIEW_COMPLETE
→ APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
→ EXISTING_APPROVED_ASSET_REUSE_FIRST
→ brief
→ image model candidate
→ USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

다음 조건을 모두 만족하면 `생성해도 될까요?`를 묻지 않고 후보 1건을 제작할 수 있다.

- actual consumer 또는 현재 Blueprint 결정용 planning-board 목적이 구체적이다.
- project latest canon, approved images, relevant mockups와 actual implementation을 읽었다.
- current visual anchor를 실제로 확인했거나 `NO_USABLE_APPROVED_VISUAL_ANCHOR`를 기록했다.
- 기존 asset 재사용·편집 가능성을 확인했다.
- keep/avoid/do-not-drift, 규격, 상태군과 rights 경계를 brief로 고정했다.
- host image model을 사용할 수 있다.

막연한 공백, consumer 없는 장식, 다른 프로젝트 스타일 복제, 요구 목록의 무차별 이미지화는 `DO_NOT_GENERATE`다.

## 7. Visual anchor와 일관성

```text
CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
STYLE_CONTINUITY_REVIEW_REQUIRED
NO_UNAPPROVED_STYLE_DRIFT
```

`PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`를 따라 다음을 확인한다.

- current approved visual anchor 존재 여부
- preview/binary readback 가능 여부
- global style, surface layer, character identity, palette, material, shape, typography
- relevant Flow/Screen/System 의미
- superseded reference와 금지 표현

usable anchor가 없으면 concept comparison deliverable 1건을 만들 수 있다.

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ COMPARISON_SHEET_NOT_PRODUCTION_ASSET
→ USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

comparison panel은 production asset이 아니다. selected direction은 standalone anchor와 final lock을 거쳐야 한다.

## 8. Image production method

모든 실제 생성·편집은 `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 따른다.

```text
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

SVG/XML path, HTML/CSS/Canvas, Python/Pillow/Cairo/matplotlib, Godot primitive로 이미지 모델을 대신하지 않는다. image model을 사용할 수 없으면 brief와 requirement는 준비할 수 있지만 결과는 `BLOCKED_IMAGE_MODEL_UNAVAILABLE`다.

Mermaid·표·Flow·JSON은 artwork 대체가 아니라 구조 정보 owner다. runtime-native UI·shader·VFX는 image deliverable 제작이 아니라 implementation mode다.

## 9. Candidate unit와 자동 chain 제한

```text
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
```

기본 단위는 시각 deliverable 1건이다. concept comparison board 하나도 1건이다. current package가 실제 consumer의 필수 상태군을 명시하면 하나의 bounded state-family package로 준비할 수 있다.

후보 뒤 다음 캐릭터·화면·독립 variant·분해 asset·production batch로 자동 확장하지 않는다. 객관적 결함은 QA에서 `REVISION_REQUIRED`로 표시하고, 원 brief를 바꾸지 않는 bounded correction만 허용한다.

## 10. Post-generation decision과 상태

후보 제시 뒤 사용자는 다음 중 하나를 결정한다.

```text
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

- `LOCK`: 결과와 명시 범위를 final direction 또는 asset-promotion candidate로 고정
- `REVISE`: 유지·수정 조건을 좁혀 동일 후보를 보정
- `REJECT`: 폐기하고 current canon으로 사용하지 않음

상태는 반드시 분리한다.

```text
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

`image generation success != user approval != PROJECT_ASSET_APPROVED != runtime integration`.

### 10.1 Local candidate vault와 명시적 promotion

생성 후보는 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`에 따라 local-only vault에서 보관·sync할 수 있다.

```text
LOCAL_CANDIDATE
!= TRACKED_PRODUCTION_ASSET
!= PROJECT_ASSET_APPROVED
```

local vault 존재, 다운로드 감지, sync 또는 recovery harvest는 tracked production path로 승격하지 않는다. 사용자 `LOCK`, current rights/provenance/consumer readback, 명시적 `promote` 동작과 repository manifest 갱신이 있어야만 production candidate로 이동한다. 삭제 tombstone과 workspace cleanup 규칙도 local vault owner를 따른다.

### 10.2 Repository registration

`LOCK` 뒤에도 product asset이 자동 승인되는 것은 아니다. 필요한 경우 current owner에 다음을 기록한다.

```yaml
asset_id:
source_path:
canonical_path:
consumer:
state_family:
pixel_size_and_format:
SHA-256:
provenance:
model_and_generation_receipt:
rights:
approval_decision:
implementation_status:
runtime_evidence:
```

`PROJECT_ASSET_APPROVED`는 repository manifest·decision·rights·consumer가 같은 결과를 가리킬 때만 사용한다. `IMPLEMENTED`는 actual consumer가 asset을 연결한 상태, `RUNTIME_VERIFIED`는 실제 render/input/readability/performance evidence가 있는 상태다.

## 11. Reference와 rights

```text
RIGHTS_AND_REFERENCE_REVIEW_REQUIRED
PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md
```

reference 기반 제작은 다음 구조를 기록한다.

```yaml
reference_brief:
  transferable_principles: []
  project_specific_adaptation: []
  forbidden_expression: []
reference_similarity_status:
rights_and_license_status:
release_status: RELEASE_BLOCKED_UNVERIFIED | REVIEWED | CLEARED
```

특정 작가·상표·trade dress·저작물의 표면 표현을 복제하지 않는다. 독립적인 프로젝트 언어로 재구성하고 visual similarity와 commercial use 경계를 검수한다. rights나 reference 독립성이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다.

## 12. 검수

후보마다 최소 다음을 검수한다.

### Canon / visual

- project identity와 승인 style 일치
- 캐릭터 얼굴·의상·비율·상징 유지
- palette·material·lighting·camera 일관성
- `STYLE_CONTINUITY_REVIEW_REQUIRED`

### Flow / product meaning

- actual consumer와 primary use 일치
- 화면 상태·정보 위계·조작 결과를 왜곡하지 않음
- `FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED`
- fake screenshot을 runtime evidence로 사용하지 않음

### Technical

- size/aspect/alpha/crop/anchor
- state family 누락
- import/filter/compression/atlas requirement
- memory/performance/platform risk

### Image defects

- 손·얼굴·해부·원근·광원
- 글자·간판·UI 텍스트 오류
- edge halo·background contamination
- unintended logo·watermark·artifact

### Rights / evidence

- source, model, prompt/brief, provenance
- reference similarity
- approval scope와 evidence ceiling
- release rights

검수 결과:

```text
GENERATED_EXPLORATION
IN_REVIEW
REVISION_REQUIRED
REJECTED
USER_LOCKED
PROJECT_ASSET_APPROVED
IMPLEMENTED
RUNTIME_VERIFIED
```

## 13. Blueprint와 implementation Gate

필요한 이미지·자료 후보는 Blueprint 검수 전에 준비한다.

```text
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

후보 생성, user visual lock 또는 asset approval은 신규 implementation package 전체의 final Blueprint approval을 대신하지 않는다.

## 14. Evidence ceiling

- 정적 candidate는 runtime PASS가 아니다.
- 문서·manifest 존재는 import/Scene 연결 증거가 아니다.
- automated screenshot은 Human UX PASS가 아니다.
- user visual lock은 rights/release PASS가 아니다.
- desktop render는 Android/device PASS가 아니다.
- 한 state의 성공은 state family 전체 PASS가 아니다.

실행하지 않은 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.

## 15. 완료 보고

```text
need and consumer
→ reused or newly generated
→ approved visual anchor
→ candidate result and QA
→ user LOCK / REVISE / REJECT
→ local vault or repository path / SHA-256 / provenance / rights
→ explicit promotion receipt
→ implementation consumer
→ runtime evidence
→ NOT_RUN / remaining risk
```

생성·승인·정본 등록·구현·runtime 검증을 한 단어 `완료`로 합치지 않는다.
