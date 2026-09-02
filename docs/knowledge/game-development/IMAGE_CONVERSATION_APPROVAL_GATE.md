# Image Conversation Approval Gate

## Purpose

이 문서는 프로젝트 이미지·목업·UI 시각화·캐릭터·배경·에셋 생성에서 **candidate 생성 권한**과 **사용자 최종 확정·정본 승격 권한**을 분리한다.

현재 사용자 승인 원칙:

```text
필요성이 확인되고 프로젝트 내용·기존 시안·승인 Visual·소비처를 읽을 수 있음
→ 일관된 bounded candidate를 먼저 제작 가능
→ 결과를 사용자에게 제시
→ LOCK / REVISE / REJECT / REFERENCE_ONLY
→ LOCK 뒤에만 canon/runtime promotion
```

이 파일은 conversation-level current owner다. `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`, `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`, project Visual Canon, rights/provenance, asset manifest와 runtime evidence를 대체하지 않는다.

## Machine contract

```text
PROJECT_CANON_AND_EXISTING_VISUAL_READBACK_REQUIRED
ACTUAL_OR_PLANNED_CONSUMER_REQUIRED
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
GENERATE_EXACTLY_ONE
BOUNDED_STATE_FAMILY_ALLOWED_WHEN_CONSUMER_REQUIRES
STOP_REQUIRED_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
PRIMARY_USE_GATE_REQUIRED_AFTER_USER_LOCK
REUSABLE_VISUAL_HARVEST_ONLY_AFTER_PRIMARY_USE_SUCCESS
BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT
BLUEPRINT_PASS_2_FINAL
REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS
HOST_PLATFORM_PRECEDENCE
HOST_POLICY_OVERRIDE
RUNTIME_ENFORCEMENT_NOT_GUARANTEED
```

## 1. 공통 Preflight

이미지 생성 전에 다음을 확인한다.

```text
latest user instruction
→ exact project relation
→ project AGENTS / current Decision / Active Context
→ actual or planned consumer
→ existing approved image / visual anchor / prior draft
→ relevant Screen / Flow / System / implementation
→ Keep / Avoid / Do Not Drift
→ format / size / state family / target owner
→ image model availability
```

필수 값:

```yaml
requirement_id:
consumer_kind:
consumer_surface:
primary_use:
continuity_sources:
keep:
avoid:
do_not_drift:
candidate_kind:
target_spec:
promotion_gate:
```

다음이면 생성하지 않는다.

- 프로젝트가 불명확함
- 실제·planned consumer가 없음
- current Visual 방향이 충돌함
- 기존 이미지/시안 readback이 불가능해 정체성을 보존할 수 없음
- 이미지 모델을 사용할 수 없음
- 생성이 새 핵심 Art Direction이나 제품 의미를 임의 확정함

상태는 각각 `MISSING_PROJECT`, `MISSING_CONSUMER`, `VISUAL_DIRECTION_CONFLICT`, `BLOCKED_UNVERIFIED`, `BLOCKED_IMAGE_MODEL_UNAVAILABLE`, `USER_DECISION_REQUIRED`로 남긴다.

## 2. Image production method

모든 실제 이미지 생성·편집은 `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 적용한다.

```text
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

SVG/vector path, HTML/CSS/Canvas, Python drawing, Godot primitive로 이미지 모델을 대신하지 않는다.

다음은 이미지 모델 우회가 아니다.

- 기존 승인 vector asset의 수정 없는 재사용
- 실제 runtime-native UI·shader·VFX 구현
- Mermaid·Flow·표·JSON 같은 구조 정보
- 정확한 annotation/crop처럼 별도 도구가 더 적합한 비창작 작업

## 3. Path A — 현재 사용자가 이미지 출력을 명시한 경우

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ PROJECT_REVIEW_COMPLETE
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ GENERATE_EXACTLY_ONE bounded deliverable
→ candidate QA
→ STOP_REQUIRED_AFTER_GENERATION
→ user decision
```

명시 요청 예:

- `이미지 만들어줘`
- `그려줘`
- `이 Brief대로 생성해`
- `이 이미지를 편집해줘`
- `필요한 이미지 작업을 진행해`

현재 요청은 별도 장문 승인문이나 다음 turn의 중복 승인을 요구하지 않는다.

usable current anchor가 있으면 실제 source/preview readback 뒤 재사용한다. anchor가 없으면 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`에 따라 concept comparison deliverable 1건을 만들 수 있다.

## 4. Path B — 승인된 작업 중 AI가 이미지 필요성을 확인한 경우

사용자가 전체 프로젝트 작업·기획·검수·필요 자료 준비를 승인했고 다음 조건이 충족되면 이미지별 사전 승인 없이 candidate를 먼저 제작할 수 있다.

```text
VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK
→ actual/planned consumer confirmed
→ project canon and existing visual readback complete
→ continuity and no-drift constraints complete
→ Visual Requirement Gate = GENERATE_EXPLORATION or CREATE_CUSTOM
→ image model available
→ NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
→ GENERATE_EXACTLY_ONE bounded deliverable
→ candidate QA
→ STOP_REQUIRED_AFTER_GENERATION
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
```

이 경로는 다음 권한을 만들지 않는다.

- candidate의 자동 정본 승격
- runtime 연결
- production batch 전체 확장
- 새 캐릭터·화면·제품 범위 자동 추가
- 사용자 취향을 대신한 final Art Direction 확정

## 5. Path C — 정보나 방향이 부족한 경우

다음 중 하나면 brief·비교·missing evidence만 정리하고 생성하지 않는다.

```text
NO_ACTUAL_OR_PLANNED_CONSUMER
NO_USABLE_PROJECT_VISUAL_CONTEXT
MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT
APPROVED_ANCHOR_BINARY_UNREADABLE
CORE_ART_DIRECTION_DECISION_REQUIRED
```

사용자에게 질문하기 전에 저장소·Library·현재 첨부·approved asset locator에서 확인 가능한 정보를 먼저 읽는다. 객관적 근거로 해소할 수 없는 핵심 취향 선택만 사용자에게 올린다.

## 6. Bounded deliverable

기본 단위:

```text
GENERATE_EXACTLY_ONE
```

한 deliverable은 다음 중 하나다.

1. image/edit candidate 1건
2. concept comparison board 1건
3. 하나의 실제 consumer가 동시에 요구하는 bounded state family 1세트

`BOUNDED_STATE_FAMILY_ALLOWED_WHEN_CONSUMER_REQUIRES`는 UI 버튼 상태, 캐릭터 방향·피격·사망, animation key family처럼 **한 소비처의 완결성**을 위해 여러 파일이 불가피할 때만 적용한다. 각 파일의 path/state mapping을 먼저 기록한다.

무제한 variant, 독립 캐릭터·화면 연쇄, “있으면 좋을 것” batch는 `NO_AUTOMATIC_IMAGE_CHAIN`으로 금지한다.

## 7. Candidate QA

생성 뒤 사용자에게 보여주기 전에 가능한 범위에서 다음을 검토한다.

- 프로젝트 시각 정본과 style continuity
- 캐릭터·세계관·UI identity 보존
- 실제 consumer의 구도·크기·alpha·crop·anchor 적합성
- state family 누락
- 금지 요소·권리·reference similarity 위험
- 텍스트 오류·의도하지 않은 artifact
- 구현/분해 가능성
- candidate와 runtime asset의 증거 경계

host가 사용자 노출 전 내부 correction을 허용하지 않으면 결함을 숨기지 않고 `REVISION_REQUIRED`로 제시한다.

## 8. Post-generation user decision

`STOP_REQUIRED_AFTER_GENERATION`은 candidate를 보여 주고 다음을 기다린다는 뜻이다.

```text
LOCK
→ USER_APPROVED
→ repository owner / provenance / SHA-256 / consumer / state mapping 등록 가능
→ Primary Use Gate
→ 구현 권한이 별도로 있으면 implementation
→ primary-use success 확인
→ Reusable Visual Harvest Gate
→ runtime evidence

REVISE
→ 같은 bounded deliverable의 명시적 correction

REJECT
→ 정본·runtime 승격 금지

REFERENCE_ONLY
→ 탐색 자료로만 보존
```

다음 상태는 분리한다.

```text
GENERATED_CANDIDATE
!= USER_APPROVED
!= PROJECT_ASSET_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

사용자 lock 전에 `PROJECT_ASSET_APPROVED`, `CANON_REGISTERED`, runtime-ready 또는 implementation complete로 보고하지 않는다.

## 9. Primary Use Gate와 Reusable Visual Harvest Gate

사용자 lock은 재사용 자산 승격을 자동 승인하지 않는다. 세부 기준은 기존 책임 원본 `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`가 소유한다.

```text
USER_APPROVED / CANON_REGISTERED
→ Primary Use Gate
→ actual consumer에서 primary-use success
→ Reusable Visual Harvest Gate
→ 재사용 가치가 있는 요소만 분류·분해·재구축
```

`PRIMARY_USE_GATE_REQUIRED_AFTER_USER_LOCK`과 `REUSABLE_VISUAL_HARVEST_ONLY_AFTER_PRIMARY_USE_SUCCESS`를 적용한다.

- `title-specific identity`, 감정, 정보 위계와 구도를 재사용성 때문에 약화시키지 않는다.
- `primary-use success`와 `reuse promotion`은 별도 판정이다.
- `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, `REJECT_REUSE`는 Art Direction 책임 원본에서 판정한다.
- `SOURCE_LAYER`, `MASK_CUTOUT`, `MANUAL_OR_SEMANTIC_REBUILD`, `DERIVED_GENERATIVE_RECOVERY`는 관측 source와 새로 생성한 영역을 분리한다.
- Harvest는 `PROJECT_ASSET_APPROVED`, rights, tracked asset 또는 Godot runtime proof를 자동 생성하지 않는다.

## 10. Blueprint relationship

Blueprint 검수에 필요한 이미지·시각자료 candidate는 1차 구조 Blueprint 뒤, 최종 Blueprint 승인 전에 만들 수 있다.

```text
PLAN
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

- `BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`: 1차 Blueprint가 concrete screen/scene/slot, target ratio·size, state family, input/flow, continuity/no-drift 조건을 먼저 제공해야 한다.
- `REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`: candidate preparation은 현재 implementation package에 필요한 consumer-bounded set이며 모든 미래 asset의 일괄 제작이 아니다.
- `BLUEPRINT_REVIEW_PUBLICATION`은 candidate review 결과를 통합한 `BLUEPRINT_PASS_2_FINAL`이다. 두 pass 모두 기존 PDF+AI Markdown의 revision이며 추가 Blueprint artifact가 아니다.

candidate 선제작은 신규 제품 구현 승인과 다르다. Blueprint 최종 승인을 요구하는 implementation package는 승인 전 runtime 구현으로 넘어가지 않는다.

## 11. Host/system precedence

`HOST_PLATFORM_PRECEDENCE`

상위 시스템(system)·developer·host 정책이 이미지 생성 시점, 도구 호출, 사용자 이미지 요구, 응답 형식을 더 엄격하게 규정하면 상위 정책을 따른다. 상위 정책 때문에 현재 sequence를 그대로 실행할 수 없으면 `HOST_POLICY_OVERRIDE`와 실제 evidence ceiling을 기록한다.

`RUNTIME_ENFORCEMENT_NOT_GUARANTEED`: 이 정적 repository 계약은 host가 제공하지 않는 이미지 호출 권한이나 숨은 runtime 동작을 만들어 내지 않는다. 실제 호출 가능 여부와 결과는 current host evidence로 확인한다.

## 12. Legacy compatibility markers

아래 문자열은 과거 test·문서 검색 호환을 위해 남기는 비활성 marker다. 현재 실행 Gate가 아니다.

```text
LEGACY_SUPERSEDED_ONLY:
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
```

현재 권위는 다음이다.

```text
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
```
