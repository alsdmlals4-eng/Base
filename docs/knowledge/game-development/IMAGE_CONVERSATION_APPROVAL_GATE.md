# Image Conversation Approval Gate

## Purpose

프로젝트용 이미지·목업·UI 시각화·캐릭터·배경·에셋 생성·편집의 실행 시점과 승인 상태를 소유한다.

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
VISUAL_NEED_CONFIRMED
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ BOUNDED_BRIEF_READY
→ CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
```

사용자가 현재 turn에서 직접 생성·편집을 요청한 경우와, fresh-read 중 실제 Visual Need가 확인된 경우를 모두 처리한다. exact project, current approved visual, 기존 시안, 실제 또는 명시적으로 계획된 consumer와 bounded scope가 확인되면 같은 내용을 다시 사전 승인받기 위해 멈추지 않고 후보 한 건을 만들 수 있다.

```text
CANDIDATE_PRODUCTION_MAY_PRECEDE_BLUEPRINT_FINAL_REVIEW
CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY
NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL
```

후보를 본 뒤 사용자가 final lock·수정·폐기·참고 보존을 결정한다. repository asset promotion과 runtime 구현·검증은 별도 current owner를 따른다.

## Related owners

```text
PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md
GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md
```

이 Gate는 Visual Need, Art Direction, asset manifest, Blueprint, rights/provenance owner를 대체하지 않는다.

## Image production method owner

모든 실제 이미지 생성·편집은 tool 호출 전에 `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 적용한다.

```text
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

SVG/vector path, HTML/CSS/Canvas, Python drawing, Godot primitive drawing으로 이미지 모델을 대신하지 않는다. 이미지 모델을 사용할 수 없으면 requirement·brief·consumer·규격·재사용 조사는 계속할 수 있지만 제작은 `BLOCKED_IMAGE_MODEL_UNAVAILABLE`로 닫는다.

기존 승인 vector asset의 수정 없는 재사용, runtime-native UI·shader·VFX 구현, Mermaid·Flow·표 같은 구조 정보는 좁은 예외다. 새 artwork를 직접 그리거나 이미지 모델을 우회하는 권한은 아니다.

## Host / system precedence and evidence ceiling

```text
HOST_PLATFORM_PRECEDENCE
HOST_POLICY_OVERRIDE
RUNTIME_ENFORCEMENT_NOT_GUARANTEED
```

상위 **시스템**·developer·host platform·tool contract가 이미지 생성 시점이나 응답 형태를 더 엄격하게 제한하면 그 상위 정책을 따른다. Base 문서만으로 host runtime을 강제했다고 주장하지 않는다.

## Preconditions

```yaml
VISUAL_CANDIDATE_PREFLIGHT:
  exact_project:
  current_project_source_sha:
  requirement_id:
  visual_need:
  consumer:
  consumer_state_or_slot:
  current_approved_visual_anchor:
  existing_approved_asset_reuse_result:
  existing_candidate_reuse_result:
  required_dimensions_and_format:
  keep: []
  avoid: []
  do_not_drift: []
  rights_and_provenance_constraints:
  bounded_deliverable:
  result: READY | BLOCKED_UNVERIFIED | DO_NOT_GENERATE
```

```text
PROJECT_REVIEW_COMPLETE
VISUAL_NEED_DEFINED
VISUAL_NEED_CONFIRMED
CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
TEXT_BRIEF_COMPLETE
BOUNDED_BRIEF_READY
CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
```

다음이면 임의 생성하지 않는다.

- exact project identity가 없다.
- current visual owner·approved anchor·기존 시안을 읽지 못했다.
- 서로 다른 current anchor가 충돌한다.
- 실제 또는 명시적으로 계획된 consumer가 없다.
- 기존 승인 asset 또는 candidate 재사용을 확인하지 않았다.
- rights·format·scope가 제품 결과를 바꿀 정도로 불명확하다.
- 상위 host policy가 명시 요청 없이 tool 호출을 금지한다.

이 경우 `BLOCKED_UNVERIFIED`, `MISSING_CANON`, `VISUAL_CANONICAL_CONFLICT`, `DO_NOT_GENERATE` 중 정확한 상태로 닫는다.

## Path A — current-turn explicit request

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact project / actual consumer / current requirement resolve
→ PROJECT_REVIEW_COMPLETE
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
→ STOP_REQUIRED_AFTER_GENERATION
```

```text
GENERATE_EXACTLY_ONE
NO_AUTOMATIC_IMAGE_CHAIN
NO_AUTOMATIC_SCOPE_EXPANSION
```

현재 요청이 여러 독립 파일을 명시하지 않았다면 다음 캐릭터·화면·variant로 확장하지 않는다.

## Path B — work 중 확인된 actual visual need

```text
VISUAL_NEED_CONFIRMED
→ PROJECT_REVIEW_COMPLETE
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ TEXT_BRIEF_COMPLETE
→ BOUNDED_BRIEF_READY
→ CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
→ STOP_REQUIRED_AFTER_GENERATION
```

후보는 기존 프로젝트 내용·승인 시안·Art Direction·Keep/Avoid/Do Not Drift와 일관되어야 한다. 하나의 consumer에 필수 state family가 있더라도 한 candidate authority로 독립 이미지를 무제한 연쇄 생성하지 않는다.

## Missing anchor route

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ COMPARISON_BOARD_ONE_DELIVERABLE
→ PRESENT_FOR_USER_FINAL_LOCK
```

comparison board는 exploration candidate 한 건이며 production asset이 아니다. 사용자가 한 방향을 선택한 뒤 standalone anchor를 current project owner에 등록·readback한다.

## Objective QA and bounded correction

후보 생성 뒤 다음을 검사한다.

- brief·consumer·규격 준수
- approved anchor·색·실루엣·재질·시대·세계관 일관성
- UI·화면 의미와 state 가독성
- 해부학·텍스트·투명도·seam·crop·artifact 오류
- rights·provenance·금지 요소

```text
OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE
```

객관 결함만 같은 deliverable 안에서 한정 교정한다. 새 Art Direction, 다른 캐릭터·화면·asset family와 취향 선택은 scope expansion이다.

## Final lock and lifecycle

```text
NEEDED
→ BRIEF_READY
→ GENERATED_CANDIDATE
→ OBJECTIVE_QA_PASSED | REVISION_REQUIRED | REJECTED
→ USER_FINAL_LOCKED
→ CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_VERIFIED
```

```text
GENERATED_CANDIDATE != USER_FINAL_LOCKED
USER_FINAL_LOCKED != PROJECT_ASSET_APPROVED
image generation success != user approval != PROJECT_ASSET_APPROVED != runtime integration
```

- `GENERATED_CANDIDATE`: 생성·검수 가능한 후보.
- `USER_FINAL_LOCKED`: 사용자가 결과를 보고 최종 방향을 확정.
- `PROJECT_ASSET_APPROVED`: 프로젝트 asset owner와 manifest가 제품 사용을 승인.
- `CANON_REGISTERED`: repository path·provenance·SHA-256·consumer가 readback됨.
- `IMPLEMENTED`: 실제 consumer가 asset을 사용함.
- `RUNTIME_VERIFIED`: 실제 화면·상태·입력·플랫폼에서 검증됨.

Notion·Sheets는 unique migration 자료가 실제로 남은 경우에만 읽는다. candidate, final lock과 current asset approval의 기본 destination은 repository owner다.

## STOP_REQUIRED_AFTER_GENERATION

후보 한 건과 필요한 bounded correction 뒤 결과를 사용자에게 제시한다. 같은 작업에서 다음 독립 asset family로 자동 확장하지 않는다.

## Retired compatibility aliases

다음 token은 historical test·proposal·adapter 검색용이며 active 실행 순서가 아니다.

```text
RETIRED_COMPATIBILITY_ALIAS
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
```

과거 two-turn gate의 active replacement는 `CANDIDATE_FIRST_VISUAL_PRODUCTION`이다. 상위 host policy가 명시 요청을 요구하면 `HOST_PLATFORM_PRECEDENCE`로 fail closed한다.

## Verification

- current project exact SHA와 visual owner를 읽었는가
- actual/planned consumer·slot·state·format이 있는가
- 기존 승인 asset·candidate 재사용을 확인했는가
- candidate가 current visual anchor와 일치하는가
- 이미지 모델을 사용했고 vector/code fallback이 없는가
- 한 bounded candidate 뒤 자동 scope expansion이 없는가
- 객관 결함과 취향·방향 변경을 구분했는가
- user final lock 전 product approval·canon·runtime을 주장하지 않았는가
- repository provenance·SHA-256·consumer readback이 있는가
- implementation·runtime evidence가 별도인가
- host override가 있으면 숨기지 않았는가

하나라도 불충분하면 해당 state만 `REVIEW_REQUIRED` 또는 `BLOCKED_UNVERIFIED`로 둔다.
