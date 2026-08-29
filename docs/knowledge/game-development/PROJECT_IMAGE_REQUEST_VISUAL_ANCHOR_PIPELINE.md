# Project Image Request Visual Anchor Pipeline

## Purpose

프로젝트 이미지가 current-turn 명시 요청으로 시작되거나, fresh-read 중 실제 필요성이 확인되었을 때 **어떤 프로젝트·consumer·visual anchor를 사용할지** 결정하는 thin routing owner다.

```text
EXPLICIT_PROJECT_IMAGE_REQUEST_AUTO_PIPELINE
NO_SEPARATE_LONG_IMAGE_INSTRUCTION_REQUIRED
CANDIDATE_FIRST_VISUAL_PRODUCTION
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED
THIN_PIPELINE_NOT_SECOND_VISUAL_CANON
CURRENT_PROJECT_CANON_WINS_ON_DRIFT
HOST_PLATFORM_PRECEDENCE
```

이 문서는 Art Direction, project Decision, asset manifest, Blueprint, rights/provenance와 runtime implementation을 새로 소유하지 않는다.

## Composed specialist owners

- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`
- `notion-project-visual-continuity-gate.md`
- `candidate-review-and-reusable-harvest.md`
- `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`

마지막 세 Notion 관련 이름은 legacy migration·historical compatibility adapter다. active current visual lock, candidate, provenance와 implementation evidence는 project repository owner를 따른다.

## 1. Trigger

### Explicit request

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact project identity resolve
→ current repository and visual owner fresh-read
→ EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED
→ APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ one bounded candidate
```

사용자는 장문 pipeline 문구를 반복할 필요가 없다.

### Need discovered during work

```text
VISUAL_NEED_CONFIRMED
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ BOUNDED_BRIEF_READY
→ CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW
→ one bounded candidate
```

current project, approved direction, existing draft와 consumer가 확인되면 candidate 제작 전에 같은 내용을 다시 승인받기 위해 멈추지 않는다.

## 2. Exact project and consumer receipt

```yaml
PROJECT_VISUAL_ROUTE:
  project:
  repository:
  source_sha:
  current_visual_owner:
  requirement_or_decision:
  actual_or_planned_consumer:
  screen_scene_ui_object_state:
  output_role: RUNTIME_ASSET | PLAYER_FACING_EXPLANATORY | PLANNING_REVIEW_CANDIDATE
  dimensions_format_alpha:
  existing_approved_asset:
  existing_candidate:
  result: READY | REUSE | TEXT_NATIVE | BLOCKED_UNVERIFIED
```

다른 프로젝트의 style·asset·memory로 빈칸을 채우지 않는다. consumer가 없으면 production asset을 만들지 않는다.

## 3. Approved anchor resolution

다음 순서로 current anchor를 찾는다.

1. project Decision과 current Visual owner
2. repository asset manifest와 approved runtime binary
3. approved source image·standalone anchor·actual runtime capture
4. current candidate history와 superseded marker
5. unique legacy visual source가 남은 경우에만 migration read

### Anchor found

```text
APPROVED_VISUAL_ANCHOR_FOUND
ANCHOR_PREVIEW_OR_BINARY_READBACK_REQUIRED
SURFACE_APPROVED_ANCHOR_TO_USER
USE_CURRENT_APPROVED_ANCHOR
APPROVED_VISUAL_REFERENCE
```

파일명·요약만 보고 anchor를 읽었다고 주장하지 않는다. 가능한 경우 binary preview 또는 exact repository readback을 확인한다.

### Conflicting or unreadable anchor

```text
MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT
APPROVED_ANCHOR_BINARY_UNREADABLE
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

충돌을 AI 취향으로 병합하지 않는다. current project owner를 교정하거나 사용자에게 실제 방향 결정만 올린다.

## 4. Missing anchor route

usable approved anchor가 없으면 final production을 추측하지 않는다.

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION
→ COMPARISON_BOARD_ONE_DELIVERABLE
→ THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS
→ USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

세 option은 색만 바꾼 변형이 아니라 silhouette, composition, material, tone 또는 information hierarchy가 실질적으로 달라야 한다.

```text
COMPARISON_SHEET_NOT_PRODUCTION_ASSET
SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR
```

comparison board는 방향 선택용 candidate이며, panel을 잘라 runtime asset으로 사용하지 않는다.

## 5. Visual direction lock packet

사용자가 한 방향을 선택하면 다음 bounded packet을 repository current owner에 기록한다.

```yaml
VISUAL_DIRECTION_LOCK_PACKET:
  project:
  source_sha:
  decision_id:
  global_style_anchor:
  surface_layer_anchor:
  flow_screen_context:
  keep: []
  avoid: []
  do_not_drift: []
  selected_reference_ids: []
  superseded_reference_ids: []
  approved_consumer_scope:
  approval_evidence:
```

방향 선택은 모든 캐릭터·화면·state·asset family의 자동 생성 권한이 아니다.

## 6. Candidate generation

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ STYLE_CONTINUITY_REVIEW_REQUIRED
→ FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
→ OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE
→ PRESENT_FOR_USER_FINAL_LOCK
```

```text
NO_UNAPPROVED_STYLE_DRIFT
NO_AUTOMATIC_IMAGE_CHAIN
NO_AUTOMATIC_SCOPE_EXPANSION
```

candidate는 current anchor·Keep/Avoid/Do Not Drift와 실제 consumer 의미를 유지한다. objective correction은 crop·artifact·규격·brief 불일치처럼 객관적으로 판정 가능한 결함만 같은 deliverable 안에서 허용한다.

## 7. State and evidence ceiling

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
CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY
```

candidate 제작과 final lock은 Blueprint implementation approval을 대체하지 않는다. product implementation은 exact approved package와 current project owner를 따른다.

## 8. Repository registration after final lock

사용자 final lock 뒤에만 다음을 등록한다.

```yaml
ASSET_PROMOTION_RECEIPT:
  asset_id:
  source_candidate:
  repository_path:
  sha256:
  provenance:
  rights_license:
  consumer:
  state_family:
  supersedes:
  project_asset_status:
  implementation_status:
  runtime_evidence:
```

Notion attachment나 Sheet row는 current asset approval 증거가 아니다. 고유 legacy 자료 이관이 실제 scope인 경우에만 migration receipt로 사용한다.

## 9. Implementation feasibility

새 format·import·animation·atlas·UI state·storage 구조가 필요한 candidate는 다음을 확인한다.

```text
IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT
CURRENT_OFFICIAL_PRIMARY_RESEARCH_REQUIRED
DIRECTLY_RELEVANT_FIELD_EVIDENCE_REQUIRED
ACTUAL_PROJECT_STRUCTURE_FEASIBILITY_REQUIRED
FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

Godot Scene·Resource·script·import settings·platform memory·texture constraints·test·runtime evidence를 실제 project 구조에서 대조한다.

## 10. Current and retired request semantics

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
STOP_REQUIRED_AFTER_GENERATION
```

현재 명시 요청은 current bounded deliverable 한 건의 직접 route다.

다음 token은 historical adapter 검색용이며 active route가 아니다.

```text
RETIRED_COMPATIBILITY_ALIAS
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
```

active replacement는 project/canon/consumer preflight 뒤의 `CANDIDATE_FIRST_VISUAL_PRODUCTION`이다.

## Verification

- exact project·source SHA·visual owner가 확인됐는가
- approved anchor의 preview/binary를 실제로 읽었는가
- actual/planned consumer와 state·format이 있는가
- existing approved asset·candidate 재사용을 먼저 확인했는가
- anchor 부재 시 comparison candidate만 만들었는가
- candidate가 current style와 Flow/screen semantics를 지켰는가
- objective correction과 새 direction을 구분했는가
- candidate/final lock/project asset/runtime state를 분리했는가
- final lock 뒤 repository provenance·SHA-256·consumer를 readback했는가
- actual implementation feasibility가 필요한 경우 current official evidence와 project 구조를 검증했는가
