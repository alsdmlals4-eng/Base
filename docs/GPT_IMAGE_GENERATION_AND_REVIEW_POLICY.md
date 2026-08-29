# GPT Image Generation and Review Policy

## Purpose

프로젝트 이미지·편집·시각 후보의 필요성, 실제 consumer, 프로젝트 일관성, 생성 수단, 후보 QA, 사용자 final lock, repository asset promotion과 runtime evidence를 하나의 상태 계보로 관리한다.

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
PRESENT_FOR_USER_FINAL_LOCK
CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY
```

이 정책은 `이미지가 필요해 보인다`는 판단만으로 무제한 생성하지 않는다. current project·approved visual·existing draft·actual 또는 명시적으로 계획된 consumer·bounded brief를 확인한 뒤 후보 한 건을 먼저 제작하고, 사용자가 결과를 보고 최종 확정한다.

## Authority and workspace

```text
REPOSITORY_PRIMARY_CANON
NOTION_LEGACY_MIGRATION_ONLY
GOOGLE_SHEETS_MIGRATION_ONLY
```

프로젝트의 current visual direction, asset catalog/manifest, candidate, provenance, consumer와 implementation evidence는 repository owner가 기본 정본이다. Notion·Google Sheets는 고유 미이관 자료가 실제로 남은 경우에만 read-only migration input으로 사용한다.

## Composed owners

다음 순서를 유지한다.

```text
docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md
→ docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md
→ Visual Requirement Gate
→ Image Conversation Approval Gate
→ docs/knowledge/game-development/IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md
→ docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
```

이 정책은 다음 전문 owner를 대체하지 않는다.

- `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`
- `PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`
- project `AGENTS.md`, current Decisions, Visual owner, asset manifest
- rights/provenance와 runtime implementation owner

권리·플랫폼·유통 evidence가 필요한 제품 또는 출시 이미지는 전문 owner의 판정이 닫히기 전까지 `RELEASE_BLOCKED_UNVERIFIED`를 유지한다.

## Visual Asset Coverage Preflight

먼저 화면과 실제 소비처를 역산한다.

```text
GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md
→ GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md
→ screen / scene / UI / object / action / state consumer inventory
→ reuse and state-family coverage check
```

```text
ACTUAL_CONSUMER_REQUIRED
PLAYER_FACING_EXPLANATORY
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

coverage gap은 requirement이지 생성 권한 자체가 아니다.

- runtime asset: 실제 Scene·UI·object·state가 소비하는 이미지
- `PLAYER_FACING_EXPLANATORY`: 인게임 튜토리얼·도감·관계 UI처럼 플레이어가 소비하는 설명 이미지
- production information: 시스템 설명, 세계관, 관계도, 제작 체크리스트

```text
PRODUCTION_INFORMATION
TEXT_TABLE_FLOW_DB_FIRST
INFORMATION_ARTIFACT_NOT_IMAGE_ASSET
```

구조·규칙·관계·Flow는 수정 가능한 Markdown·표·JSON·Mermaid를 우선한다. 이미지 파일로 소비되지 않으면 `DO_NOT_GENERATE`다.

## 1. Visual Requirement Gate

```yaml
VISUAL_REQUIREMENT:
  project:
  source_sha:
  requirement_id:
  user_or_player_value:
  actual_or_planned_consumer:
  screen_scene_slot_state:
  existing_approved_asset:
  existing_candidate:
  required_state_family:
  dimensions_format_color_alpha:
  current_visual_anchor:
  keep: []
  avoid: []
  do_not_drift: []
  rights_provenance:
  implementation_mode:
  result: GENERATE_CANDIDATE | REUSE | TEXT_NATIVE | ENGINE_NATIVE | DO_NOT_GENERATE | BLOCKED_UNVERIFIED
```

후보 선정은 player/user value, delete test, actual consumer, 우선순위, 기존 자산 재사용 가능성과 검증 비용을 근거로 한다.

`GENERATE_CANDIDATE`는 다음을 모두 만족해야 한다.

```text
VISUAL_NEED_CONFIRMED
CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
BOUNDED_BRIEF_READY
```

기존 승인 asset·candidate·runtime capture가 requirement를 충족하면 새 이미지를 만들지 않는다. consumer나 visual canon이 없으면 `BLOCKED_UNVERIFIED`다.

## 2. Conversation authority

모든 생성·편집은 `IMAGE_CONVERSATION_APPROVAL_GATE.md`를 따른다.

### Current-turn explicit request

```text
PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
```

현재 요청 범위의 bounded deliverable 한 건을 바로 만들 수 있다.

### Actual need found during work

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
```

current project·approved visual direction·existing drafts·actual/planned consumer와 bounded brief가 확인되면 후보 제작 전 같은 내용을 다시 승인받기 위해 멈추지 않는다.

```text
IMAGE_MODEL_GENERATES_ONE_CANDIDATE
GENERATE_EXACTLY_ONE
NO_AUTOMATIC_IMAGE_CHAIN
NO_AUTOMATIC_SCOPE_EXPANSION
PRESENT_FOR_USER_FINAL_LOCK
STOP_REQUIRED_AFTER_GENERATION
```

후보 한 건과 객관 결함의 bounded correction 뒤 사용자가 승인·수정·폐기·참고 보존을 결정한다.

## 3. Image creation method

```text
IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

실제 이미지 산출물은 host image generation/editing model로 만든다. SVG/vector path, HTML/CSS/Canvas, Python/Pillow/Cairo/matplotlib, Godot draw_* / Line2D / Polygon2D / primitive drawing은 이미지 모델 대체 수단이 아니다.

```text
EXISTING_APPROVED_VECTOR_ASSET_REUSE_ONLY
ENGINE_NATIVE_UI_AND_EFFECT_IMPLEMENTATION_IS_NOT_IMAGE_DELIVERABLE_CREATION
STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE
HOST_PLATFORM_PRECEDENCE
```

예외는 새 artwork를 직접 authoring할 권한이 아니다. 상위 host가 현재 메시지의 명시 요청을 요구하거나 tool call을 제한하면 상위 정책을 따른다.

## 4. Project and visual continuity readback

후보 제작 전 다음을 fresh-read한다.

1. exact project and current repository SHA
2. project `AGENTS.md`, Active Context, approved Decisions
3. current Art Direction/Visual owner, approved anchors and candidate history
4. actual/planned screen·Scene·UI·object·state consumer
5. existing approved asset·candidate·runtime capture reuse
6. Keep / Avoid / Do Not Drift
7. required dimensions·format·alpha·platform
8. rights·provenance·storage path

다른 프로젝트의 스타일이나 기억을 빈칸 채우기에 사용하지 않는다.

## 5. Candidate production

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
→ VISUAL_NEED_CONFIRMED
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ BOUNDED_BRIEF_READY
→ CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
```

usable approved anchor가 없으면 final production을 추측하지 않는다.

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ COMPARISON_BOARD_ONE_DELIVERABLE
→ USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

comparison deliverable은 generated exploration이며 runtime asset이 아니다.

## 6. Objective QA

후보를 사용자에게 제시하기 전에 확인한다.

- brief·consumer·규격·state family
- current anchor·색·실루엣·재질·시대·세계관
- UI 가독성·화면 의미·선택 상태 구분
- crop·seam·artifact·투명도·text corruption·anatomy
- rights·provenance·forbidden motifs
- 기존 asset과의 continuity

명백한 결함만 같은 deliverable 안에서 교정한다.

```text
OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE
```

새 Art Direction·캐릭터·화면·asset family는 별도 scope다.

## 7. Primary Use Gate and Reusable Visual Harvest Gate

후보의 첫 목적은 현재 title의 실제 consumer에서 요구한 품질을 충족하는 것이다. 공용화 가능성 때문에 primary quality나 `title-specific identity`를 낮추지 않는다.

```text
Primary Use Gate
GENERATED_CANDIDATE
→ USER_FINAL_LOCKED
→ PROJECT_ASSET_APPROVED
→ IMPLEMENTED
→ primary-use success
```

`primary-use success`는 current consumer에서 의미·가독성·style·규격·runtime 요구를 충족했다는 evidence가 있을 때만 선언한다. 그 전에는 reuse harvest를 시작하지 않는다.

```text
Reusable Visual Harvest Gate
primary-use success
→ reuse candidate review
→ reuse classification
→ decomposition method
→ second-use validation
→ explicit reuse promotion
```

재사용 분류:

```text
REUSE_AS_IS
VARIANT_SEED
STRUCTURE_PATTERN
STYLE_DNA
REBUILD_FOR_REUSE
ONE_OFF_KEEP
REJECT_REUSE
```

분해 방식:

```text
SOURCE_LAYER
MASK_CUTOUT
MANUAL_OR_SEMANTIC_REBUILD
DERIVED_GENERATIVE_RECOVERY
```

`reuse promotion`은 별도 승인·rights·provenance·second-use validation을 요구하며 `PROJECT_ASSET_APPROVED`를 자동으로 공용 자산 승인으로 확대하지 않는다. 공용화가 current title의 품질·identity·rights를 훼손하면 `ONE_OFF_KEEP` 또는 `REJECT_REUSE`다.

## 8. Final lock, promotion and evidence ceiling

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
GENERATED_EXPLORATION != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED
image generation success != user approval != PROJECT_ASSET_APPROVED != runtime integration
CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY
CANDIDATE_PRODUCTION_MAY_PRECEDE_BLUEPRINT_FINAL_REVIEW
NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL
```

사용자 final lock 뒤 프로젝트 asset owner가 repository path, SHA-256, provenance, license/rights, consumer, state family와 superseded asset을 등록한다. 실제 implementation과 runtime evidence는 별도다.

권리·플랫폼·유통 판정이 필요한 경우 `PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` receipt가 없으면 `RELEASE_BLOCKED_UNVERIFIED`를 유지한다.

정적 이미지 inspection은 runtime PASS가 아니다. 실제 Scene·UI·state·input·platform에서 소비된 증거가 없으면 `IMPLEMENTED` 또는 `RUNTIME_VERIFIED`라고 쓰지 않는다.

## 9. Implementation feasibility for image systems

material asset pipeline·format·import·animation·UI state·storage 선택은 일반론만으로 확정하지 않는다.

```text
IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT
CURRENT_OFFICIAL_PRIMARY_RESEARCH_REQUIRED
DIRECTLY_RELEVANT_FIELD_EVIDENCE_REQUIRED
ACTUAL_PROJECT_STRUCTURE_FEASIBILITY_REQUIRED
```

확인 항목:

- current engine/importer/platform official docs
- directly relevant successful, failed or mixed field cases
- actual Godot Scene·Resource·script·UI consumer and import settings
- memory·VRAM·batching·texture size·compression·atlas·animation constraints
- source/derived asset ownership and migration/rollback
- automated checks and runtime evidence

결론은 `FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED` 중 하나다. 외부 사실이 결과를 바꿀 수 없는 순수 rename·formatting 같은 작업만 `MECHANICAL_NO_EXTERNAL_DEPENDENCY` 사유를 기록할 수 있다.

## 10. Long-term quality and automation

```text
LONG_TERM_QUALITY_OVER_LOCAL_SPEED
ROOT_CAUSE_AND_REUSE_BEFORE_REPEATED_MANUAL_PATCH
MINIMUM_SUFFICIENT_COMPLEXITY
SPECULATIVE_OVERENGINEERING_REJECTED
PLAYABLE_OR_OPERATIONAL_VALUE_OVER_DOCUMENT_VOLUME
MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL
INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP
```

반복 승인은 줄이되 user final lock, product meaning, rights, cost, release, irreversible change는 자동 승인하지 않는다.

```text
problem → reproducible evidence → root cause → correction → regression prevention → project readback → Base BCP
```

## 11. Actual post-change review

material policy·template·asset workflow 변경 후 Base current review owner를 실제 실행한다.

```text
ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
FULL_LOOP_COUNT_MINIMUM: 5
EXECUTION_EVIDENCE_REQUIRED
CORRECT_VALIDATED_FINDINGS
CLEAN_REVIEW_EXIT
NO_REVIEW_COMPLETION_CLAIM_WITHOUT_EVIDENCE
```

검토했다고 쓰는 것만으로 완료되지 않는다. 같은 final-state lineage에서 발견·검증·교정·회귀검사·재공격 증거가 있어야 한다.

## Retired compatibility aliases

다음은 historical test·proposal·adapter 검색용이며 active generation sequence가 아니다.

```text
RETIRED_COMPATIBILITY_ALIAS
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
NO_AUTOMATIC_IMAGE_GENERATION
```

현재 active replacement는 `CANDIDATE_FIRST_VISUAL_PRODUCTION`이다. `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`는 coverage gap만으로 생성 범위를 자동 확대하지 말라는 현재 규칙으로 계속 유효하다.

## Verification checklist

- repository current visual owner와 exact SHA를 읽었는가
- screen/surface inventory가 asset category보다 먼저인가
- actual/planned consumer와 state family가 있는가
- approved asset·candidate 재사용을 확인했는가
- image model only 정책을 지켰는가
- 한 bounded candidate 뒤 scope가 자동 확장되지 않았는가
- objective defect와 취향·direction change를 구분했는가
- user final lock 전 canon/runtime을 주장하지 않았는가
- primary-use success 전 reuse harvest를 시작하지 않았는가
- reuse promotion이 title-specific identity와 primary quality를 보존하는가
- provenance·SHA-256·consumer readback이 있는가
- platform/release rights owner가 필요한 경우 `RELEASE_BLOCKED_UNVERIFIED`를 지켰는가
- implementation·runtime evidence가 별도인가
- material pipeline 선택을 current official docs와 actual project structure에서 검증했는가
- 작업 후 실제 adversarial correction evidence가 있는가
