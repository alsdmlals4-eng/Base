# Visual Concept Exploration and Continuity Lock

> 새롭거나 material하게 변경되는 Visual Direction을 **비교 → 사용자 선택 → 방향 잠금 → 일관된 production/runtime 검수**로 연결하는 얇은 전이 계약이다. Project Art Bible과 기존 이미지·후보·전달 정책을 복제하지 않는다.

```text
VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE
THIN_CONTRACT_NOT_SECOND_ART_BIBLE
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
ACTUAL_CONSUMER_REQUIRED
CURRENT_SPECIALIST_OWNER_WINS_ON_DETAIL_DRIFT
NO_AUTOMATIC_IMAGE_GENERATION_AUTHORITY
```

## 0. Current owner composition

작업 시점의 Base latest completed main과 exact Project canon에서 다음 상세 owner를 읽는다.

- 필요성·actual consumer·candidate lifecycle·검수: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Concept Exploration·Art Bible·Asset Specification: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- 생성 대화 승인: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- 후보 비교·선정: `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- Project relation·Flow/Screen·Keep/Avoid/Do Not Drift: `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`
- 프로젝트 로컬 후보·승격·Codex 전달: `templates/project-operations/WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`

Project-specific 분위기·팔레트·비례·Flow·asset ID는 Project GitHub/Notion 정본이 소유한다.

---

## 1. Trigger / reuse Gate

다음이면 이 계약을 적용한다.

- 새 프로젝트의 첫 material Visual Direction
- 새 핵심 Slice의 대표 screen/environment/character/UI visual family
- current approved direction이 없거나 충돌함
- 그림체·분위기·렌더·카메라·밀도 문법의 material 변경
- confirmed Flow/Screen 변경으로 기존 visual anchor가 stale

```text
CURRENT_APPROVED_VISUAL_DIRECTION_REUSE
NO_REEXPLORATION_FOR_EVERY_BOUNDED_ASSET
```

현재 approved Art Bible/Visual Direction이 있고 actual consumer·Flow/Screen·protected identity 전제가 유지되면 기존 lock을 재사용한다. bounded pose·icon·prop마다 후보 탐색을 반복하지 않는다.

Project identity, actual consumer, current direction 또는 Flow/Screen을 읽지 못하면 다른 프로젝트·과거 채팅·draft 이미지로 추측하지 않는다.

```text
MISSING_VISUAL_DIRECTION_CANON
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

---

## 2. Required transition

```text
CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK
→ USER_SELECTED_VISUAL_DIRECTION_REQUIRED
→ APPROVED_VISUAL_DIRECTION_PACKET
→ CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK
```

```text
Project canon / implementation / approved references fresh-read
→ actual consumer와 시각 결정 질문
→ Reuse First + reference/benchmark axes
→ controlled concept options
→ 사용자 선택
→ adopted/rejected 요소와 allowed variation
→ confirmed Flow/Screen anchor
→ Visual Direction readback
→ production/Codex packet
→ target-size/runtime consistency validation
```

후보 존재만으로 production scale을 시작하지 않는다.

---

## 3. Controlled concept options

```text
MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3
NO_FAKE_CONCEPT_OPTION
SAME_CONSUMER_CONTROLLED_COMPARISON
CONTROLLED_VARIABLE_COMPARISON_REQUIRED
```

중요한 방향 선택은 가능한 경우 최소 3개의 materially distinct 후보를 비교한다. 팔레트나 이름만 바꾼 허수 후보를 만들지 않는다. 실질 후보가 3개 미만이면 이유와 실제 후보 수를 기록한다.

가능한 범위에서 actual consumer, 기본 내용, camera/framing, scale/viewing distance를 고정하고 선언한 축만 바꾼다.

```yaml
CONTROLLED_CONCEPT_COMPARISON:
  decision_question:
  actual_consumer:
  invariant_content:
  invariant_camera_and_framing:
  invariant_scale_and_viewing_distance:
  declared_variable_axes: []
  candidate_ids: []
  evaluation_dimensions: []
  constraints_that_cannot_be_equalized: []
```

후보는 기존 candidate review owner가 canon fit, identity, composition, actual-use readability, implementation fitness, production 반복성, rights/reference risk로 비교한다.

```yaml
CONCEPT_DIRECTION_CANDIDATE:
  candidate_id:
  title:
  actual_consumer:
  player_experience_strengthened:
  information_or_experience_weakened:
  mood_and_style_axes:
  production_cost_and_repeatability:
  technical_or_platform_risk:
  reference_and_rights_boundary:
```

후보 ID·장단점은 생성 이미지의 pseudo-text가 아니라 실제 텍스트 record가 소유한다.

---

## 4. Explicit concept comparison board

```text
EXPLICIT_CONCEPT_COMPARISON_BOARD
ONE_EXPLORATION_BOARD_NOT_N_RUNTIME_DELIVERABLES
CONCEPT_COMPARISON_BOARD_IS_EXPLORATION_NOT_RUNTIME_ASSET
```

사용자가 비교 board 목적·후보 수·고정 조건·변경 축을 text brief로 승인하면, 여러 option panel을 담은 board 하나는 existing Gate의 **one explicit comparison artifact**가 될 수 있다.

```text
TEXT_BRIEF_STOP_REQUIRED
→ NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE explicit comparison artifact
→ STOP_REQUIRED_AFTER_GENERATION
```

```text
comparison board = GENERATED_EXPLORATION
comparison board = not runtime evidence
comparison board != independent runtime asset delivery
```

board는 여러 independent runtime asset, 독립 고해상도 source, `PROJECT_ASSET_APPROVED`, Scene 소비 또는 Human/Player PASS를 뜻하지 않는다. N개 독립 runtime 자산이 필요하면 N개의 production deliverable·format·path·manifest·runtime validation이 별도로 필요하다.

---

## 5. User selection

```text
USER_SELECTED_VISUAL_DIRECTION_REQUIRED
CONCEPT_DIRECTION_SELECTION
```

```yaml
CONCEPT_DIRECTION_SELECTION:
  selected_candidate_id:
  adopted_elements: []
  rejected_elements: []
  selection_reason:
  conditions_or_assumptions:
  allowed_variation: []
  superseded_direction_ids: []
  visual_direction_lock_output:
  approval_ref:
```

사용자는 한 후보 전체를 선택하거나 A의 분위기+B의 UI 절제+C의 camera처럼 요소를 조합할 수 있다. 조합 결과는 새 lock으로 기록한다.

---

## 6. Visual Direction lock

```text
APPROVED_VISUAL_DIRECTION_PACKET
FLOW_AND_SCREEN_ANCHORS_LOCKED_BEFORE_SCALE
```

```yaml
APPROVED_VISUAL_DIRECTION_PACKET:
  project:
  visual_direction_lock_id:
  lock_version:
  source_candidate_ids: []
  selection_and_approval_ref:
  actual_consumer_families: []
  approved_flow_or_screen_anchor_ids: []
  mood_and_emotion:
  style_and_rendering_language:
  shape_silhouette_and_proportion:
  palette_value_material_lighting:
  camera_framing_density:
  ui_iconography_vfx_family:
  keep: []
  avoid: []
  do_not_drift: []
  allowed_variation: []
  production_constraints: []
  rights_and_reference_boundary:
  target_size_and_runtime_checks: []
  supersedes: []
  status: CURRENT | SUPERSEDED | CONFLICT | BLOCKED_UNVERIFIED
```

`approved_flow_or_screen_anchor_ids`에는 Project interpretation state가 `CONFIRMED`인 record만 넣는다. `DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 requirement anchor가 아니다.

- `keep`: 유지할 player experience와 visual grammar
- `avoid`: 배제한 drift·가독성 실패·과밀·pseudo-text
- `do_not_drift`: identity·비례·실루엣·palette role·line/material·camera·UI family
- `allowed_variation`: 지역·진영·시간대·상태별로 의도적으로 바꿀 축과 한계

---

## 7. Production / Codex mapping

```text
CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK
ALLOWED_VARIATION_WITHOUT_UNAUTHORIZED_STYLE_DRIFT
```

후속 brief와 asset은 current `visual_direction_lock_id`와 actual consumer를 사용한다. 기존 local Visual packet schema는 바꾸지 않고 다음처럼 매핑한다.

```yaml
VISUAL_LOCK_TO_LOCAL_PACKET_MAPPING:
  visual_direction_lock_id: APPROVED_VISUAL_DIRECTION_PACKET.visual_direction_lock_id
  approved_flow_or_screen_anchor_ids: APPROVED_VISUAL_DIRECTION_PACKET.approved_flow_or_screen_anchor_ids
  approved_reference_or_style_anchor: visual_direction_lock_id + approved reference locator
  notion_reference_surface: Project Visual Bible / confirmed Flow or Screen locator
  objective_acceptance:
    - keep / avoid / do_not_drift / allowed_variation
    - actual consumer 역할과 target-size readability
  runtime_validation:
    runtime_consistency_validation:
    - exact Scene/Screen에서 mood·style·palette·camera·UI/VFX family 검수
```

Codex handoff는 project-relative path, manifest, exact commit, `visual_direction_lock_id`, anchor IDs와 drift 금지 acceptance를 함께 전달한다.

일관성 검수 축:

```text
mood/emotion
rendering/line/cluster/material language
shape/silhouette/proportion
palette/value/lighting
camera/framing/density
UI/iconography/VFX family
information hierarchy/readability
protected identity
allowed variation
```

일관성은 모든 장소를 같은 색·재질로 만드는 것이 아니다. 지역·진영 차이가 있어도 공통 pixel density, camera grammar, value hierarchy, shape language 또는 UI family가 같은 프로젝트로 판독돼야 한다.

```text
source candidate review
!= imported asset review
!= target-size runtime composite review
!= Human/Player evidence
```

---

## 8. State / evidence ceiling

```text
GENERATED_EXPLORATION
→ IN_REVIEW
→ APPROVED_CANDIDATE
→ USER_SELECTED_VISUAL_DIRECTION_REQUIRED
→ APPROVED_VISUAL_DIRECTION_PACKET
→ independent production candidate
→ PROJECT_ASSET_APPROVED
→ APPLIED_AND_RUNTIME_VERIFIED
```

```text
comparison board exists
!= user selected direction
!= Visual Direction locked
!= product asset approved
!= runtime consistency PASS
```

---

## 9. Drift reopen

```text
VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED
EARLIEST_AFFECTED_VISUAL_SCOPE_REOPENS
NO_FULL_PROJECT_VISUAL_RESTART_FOR_LOCAL_DRIFT
```

Trigger:

- user Decision의 material mood/style/camera/proportion 변경
- confirmed Flow/Screen 또는 actual consumer 변경
- runtime evidence의 readability/continuity 실패
- rights/reference 문제로 anchor 사용 불가
- approved player-facing asset family 교체

```text
change evidence
→ affected lock field / anchor / asset family
→ affected candidate·asset·runtime evidence만 stale
→ 필요한 selection/lock field 재승인
→ affected downstream 재검증
→ destination readback
```

local icon drift 하나로 프로젝트 전체를 재시작하지 않는다. 반대로 master direction 변경 뒤 stale downstream을 current PASS로 유지하지 않는다.

---

## 10. Adversarial review

전체 상태에서 다음을 공격한다.

1. 허수 후보 또는 추천안 들러리인가
2. camera/content/scale가 달라 비교 원인이 섞였는가
3. board를 N runtime deliverable로 오인했는가
4. pseudo-text가 candidate meaning을 소유하는가
5. selected/adopted/rejected/allowed variation이 기록됐는가
6. unconfirmed Flow를 anchor로 잠갔는가
7. 후속 asset이 lock을 실제 소비하는가
8. rigid sameness 또는 무제한 variation인가
9. target-size/runtime 검수 없이 원화만 승인했는가
10. drift 뒤 stale evidence가 current인가
11. candidate/asset/runtime/Human evidence를 혼동했는가
12. rights·cross-project identity 위험이 있는가

유효 finding은 가장 이른 affected Visual scope를 reopen한다.

---

## 11. Exit receipt

```yaml
VISUAL_CONCEPT_LOCK_CLEAN_EXIT:
  exact_project_and_consumer_verified:
  exploration_required_or_reuse_reason:
  real_candidate_count:
  controlled_comparison_evidence:
  user_selection_ref:
  visual_direction_lock_id:
  confirmed_flow_or_screen_anchors: []
  local_packet_mapping_verified:
  runtime_consistency_plan:
  rights_and_reference_status:
  blocking_findings: []
  evidence_ceiling:
  result: READY_FOR_BOUNDED_PRODUCTION | REUSE_CURRENT_LOCK | BLOCKED_UNVERIFIED
```

정적 계약은 실제 이미지 품질·프로젝트 사용자 승인·runtime consistency를 증명하지 않는다.
