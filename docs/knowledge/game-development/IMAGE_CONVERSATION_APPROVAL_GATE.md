# Image Conversation Approval Gate

## Purpose

프로젝트용 이미지·목업·UI 시각화·캐릭터·배경·에셋 생성·편집의 **후보 제작 권한**과 **최종 확정 권한**을 분리한다.

사용자가 current turn에서 이미지를 직접 요청한 경우뿐 아니라, 작업 중 구체적인 실제 소비처 또는 Blueprint 검수용 planning-board 필요성이 확인된 경우에도 프로젝트 정본과 기존 시각 방향을 먼저 읽고 후보 1건을 제작할 수 있다. 사용자 승인은 생성 전에 반복해서 받는 것이 아니라 생성 결과 뒤 `LOCK / REVISE / REJECT`로 받는다.

```text
NEED_DRIVEN_GENERATE_THEN_LOCK
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

이 Gate는 Visual Requirement, 프로젝트 Visual Canon, 권리·provenance, asset promotion, repository readback, Blueprint final approval와 runtime evidence를 대체하지 않는다.

## Active machine contract

```text
PROJECT_REVIEW_COMPLETE
VISUAL_NEED_DEFINED
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
NEED_DRIVEN_GENERATE_THEN_LOCK
CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
TEXT_BRIEF_COMPLETE
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

## Superseded compatibility markers

다음 문자열은 기존 consumer와 역사 추적을 위한 compatibility marker이며 **현재 active path가 아니다**.

```text
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE__SUPERSEDED
TEXT_BRIEF_STOP_REQUIRED__SUPERSEDED_FOR_CONCRETE_NEED
NEXT_USER_EXPLICIT_APPROVAL__SUPERSEDED_FOR_CANDIDATE_GENERATION
```

기존 consumer가 exact legacy token을 검색할 수 있으므로 아래 이름도 역사 키워드로만 보존한다.

```text
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
```

이 키워드 존재를 이유로 새 작업에서 생성 전 중복 승인을 요구하지 않는다. final lock과 production/runtime 승격 승인만 유지한다.

## Image production method owner

모든 실제 이미지 생성·편집은 authority 판정 뒤 tool 호출 전에 `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 적용한다.

```text
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

이미지 deliverable은 host image generation/editing model로만 만든다. SVG/vector path, HTML/CSS/Canvas, Python/Pillow/Cairo/matplotlib, Godot draw primitive로 이미지 모델을 대신하지 않는다. 이미지 모델을 사용할 수 없으면 brief·consumer·규격·상태군 정리는 계속할 수 있지만 생성은 `BLOCKED_IMAGE_MODEL_UNAVAILABLE`로 닫는다.

기존 승인 vector asset의 수정 없는 재사용, runtime-native UI·shader·VFX 구현, Mermaid·Flow·표 같은 구조 정보 작성은 좁은 예외다. 새 artwork를 우회 제작하는 권한이 아니다.

## Host / system precedence

`HOST_PLATFORM_PRECEDENCE`

상위 system·developer·host tool 계약이 이 Base workflow보다 우선한다. host가 사용자 이미지 첨부를 요구하거나 생성 시점·응답 형태를 제한하면 해당 규칙을 따른다.

정상 sequence를 그대로 실행할 수 없으면 다음을 기록한다.

- `HOST_POLICY_OVERRIDE`
- `RUNTIME_ENFORCEMENT_NOT_GUARANTEED`
- `BLOCKED_IMAGE_MODEL_UNAVAILABLE` 또는 실제 blocker

상위 정책을 위반해 Base Gate를 강제하거나 실행하지 않은 동작을 PASS로 쓰지 않는다.

## Generation authority routes

### Path A — current-turn explicit request

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact Project / consumer / purpose resolve
→ PROJECT_REVIEW_COMPLETE
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ GENERATE_ONE_CANDIDATE_BEFORE_LOCK
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
→ USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

다음은 명시적 생성·편집 요청이다.

- `이미지 만들어줘`
- `그려줘`
- `이 화면을 제작해줘`
- `이 이미지에서 ○○를 바꿔줘`
- `이 Brief대로 생성해`

사용자의 current request는 기본적으로 시각 deliverable 1건 authority다. current package가 필수 state family를 명시했다면 그 bounded family를 하나의 deliverable package로 다룰 수 있지만 별개 캐릭터·화면·스타일로 확장하지 않는다.

### Path B — 작업 중 구체적 시각 필요 발견

```text
NEED_DRIVEN_GENERATE_THEN_LOCK
→ exact actual consumer or Blueprint planning-board purpose
→ PROJECT_REVIEW_COMPLETE
→ current canon / approved images / previous mockups / visual anchor readback
→ existing approved asset reuse/edit check
→ Visual Need + keep/avoid/do-not-drift + size/state/rights brief
→ TEXT_BRIEF_COMPLETE
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ GENERATE_ONE_CANDIDATE_BEFORE_LOCK
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
→ USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

별도의 `생성해도 될까요?` 질문은 요구하지 않는다. 다음 조건이 모두 있어야 한다.

1. 실제 runtime node/path/slot, planned player-facing screen 또는 현재 Blueprint 검수에 필요한 구체적인 planning-board 목적이 있다.
2. 대상 프로젝트의 latest current canon, approved visual direction, 기존 승인 이미지와 relevant 시안을 실제로 읽었다.
3. 기존 자산 재사용·편집·runtime-native 구현으로 해결 가능한지 확인했다.
4. 유지할 요소, 금지 drift, 규격, 상태군, rights/provenance 경계를 brief로 고정했다.
5. 다른 프로젝트의 이미지를 편의상 섞지 않았다.

다음은 후보 생성 권한이 아니다.

- 막연한 이미지 공백
- consumer 없는 장식 이미지
- 과거 채팅의 일반적 이미지 관심
- Base/프로젝트 문서 수정 승인
- 다른 프로젝트 이미지와 비슷하게 만들고 싶은 편의
- 요구 목록을 모두 이미지 파일로 바꾸는 행위

## Project context and visual continuity

```text
latest user decision
→ exact project AGENTS / current visual owner
→ actual or planned consumer
→ approved asset / visual anchor / relevant mockup
→ related Flow / Screen / System
→ implementation state when runtime consistency matters
→ Visual Need brief
```

`CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED`는 파일명만 찾는 것이 아니다. 가능한 환경에서는 실제 preview/binary를 확인하고, 사용할 수 없는 경우 `APPROVED_ANCHOR_BINARY_UNREADABLE` 또는 `BLOCKED_UNVERIFIED`로 남긴다.

사용 가능한 anchor가 없으면 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`에 따라 concept comparison deliverable 1건을 만들 수 있다. comparison은 `GENERATED_EXPLORATION`이며 production asset이 아니다. 사용자가 방향을 고른 뒤 standalone anchor와 final lock을 별도로 관리한다.

## Brief minimum

후보 제작 전 내부 또는 repository brief에는 최소 다음이 있어야 한다.

```yaml
project:
requirement_id:
consumer_or_planning_board:
primary_use:
approved_visual_anchor:
existing_assets_checked: []
keep: []
avoid: []
do_not_drift: []
subject_and_state:
target_size_aspect_alpha_crop:
state_family:
rights_and_reference_boundary:
output_status: GENERATED_CANDIDATE
fallback_if_unconsumed:
```

brief는 후보 제작을 정확하게 하기 위한 준비물이다. 구체적 필요가 확인된 뒤 brief를 작성한 같은 작업 흐름에서 후보를 만들 수 있다.

## One candidate and stop boundary

```text
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
```

- concept comparison board 하나는 deliverable 1건이다.
- current package가 명시한 필수 상태군은 bounded batch가 될 수 있다.
- 후보를 만든 뒤 다음 캐릭터·화면·독립 variant·분해 asset을 자동 호출하지 않는다.
- 객관적 결함이 있으면 사용자에게 숨긴 채 무한 재생성하지 않고 QA 결과와 `REVISION_REQUIRED`를 제시한다. host가 내부 bounded correction을 지원하고 original brief를 바꾸지 않는 경우에만 제한적으로 교정한다.

## Post-generation decision

후보를 제시한 뒤 사용자는 다음 중 하나를 결정한다.

- `LOCK`: 해당 결과와 명시 범위를 final visual direction 또는 asset-promotion candidate로 고정
- `REVISE`: 유지/수정 조건을 좁혀 동일 후보를 보정
- `REJECT`: 폐기하고 정본으로 사용하지 않음

```text
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

`좋아`, `괜찮아`처럼 범위가 불명확하면 locked scope를 과장하지 않는다. final direction 또는 production promotion이 필요한 경우 어떤 결과·상태·consumer를 잠그는지 확인 가능한 receipt를 남긴다.

## Approval and asset lifecycle

```text
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

- generation success는 후보 존재만 증명한다.
- `USER_LOCKED`는 사용자가 결과·방향을 확정했음을 뜻한다.
- `PROJECT_ASSET_APPROVED`는 repository asset/provenance/rights/consumer owner에 등록된 상태다.
- `IMPLEMENTED`는 actual Scene/Resource/UI/runtime path가 사용함을 뜻한다.
- `RUNTIME_VERIFIED`는 해당 환경에서 실제 렌더·입력·가독성·성능을 확인한 상태다.

승인 후 repository current owner에 원본, SHA-256, provenance, rights, consumer, state family, approval receipt와 implementation evidence를 기록한다. Notion/Sheet는 current project가 명시한 migration-only 예외가 아니면 destination이나 완료 Gate가 아니다.

## Blueprint boundary

필요한 이미지 후보는 Blueprint 검수 전에 준비할 수 있다. 그러나 생성 또는 final visual lock이 새 구현 package authority를 만들지 않는다.

```text
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

## Exceptions

다음은 이미지 생성이 아니므로 generation checkpoint를 만들지 않는다.

- 기존 이미지 텍스트 분석·비평
- 승인 자산의 수정 없는 재사용·링크
- Mermaid·Flow·표·Markdown·JSON 작성
- requirement inventory와 brief 작성
- runtime-native UI·shader·VFX·procedural effect 구현

새 mockup, icon, texture, sprite, UI art 또는 image file을 만드는 순간 예외가 아니며 image model policy를 적용한다.

## Verification

- actual consumer 또는 planning-board 목적이 구체적인가
- current project canon과 실제 approved visual anchor를 읽었는가
- 기존 asset 재사용을 먼저 확인했는가
- explicit request 또는 `NEED_DRIVEN_GENERATE_THEN_LOCK`로 authority를 분류했는가
- image model policy를 적용했는가
- deliverable 1건 범위를 지켰는가
- 생성 뒤 자동 chain을 멈췄는가
- 사용자에게 `LOCK / REVISE / REJECT`를 받는 상태인가
- candidate/lock/asset/runtime 상태를 분리했는가
- provenance·rights·SHA-256·consumer owner를 과장하지 않았는가
- Blueprint final approval 전 새 implementation을 시작하지 않았는가
- host override와 `NOT_RUN / BLOCKED_UNVERIFIED`를 숨기지 않았는가

조건을 충족하지 않으면 `REVIEW_REQUIRED` 또는 `BLOCKED_UNVERIFIED`다.
