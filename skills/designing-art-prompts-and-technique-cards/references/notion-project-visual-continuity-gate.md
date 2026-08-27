# Notion Project Visual Continuity Gate

Use this reference only for project-scoped visual generation, editing or visual-flow review after the Visual Requirement Gate has selected a real need.

## Authority

```text
latest user decision
→ Project relation + current project canon / Decision
→ APPROVED_VISUAL_REFERENCE records in ASSET_KNOWLEDGE_MASTER
→ current Screen / flow records
→ candidate / draft material
→ external references
```

`PROJECT_RELATION_REQUIRED` is mandatory. If Project identity is missing or ambiguous, return `BLOCKED_UNVERIFIED` rather than borrowing a neighboring project's visual record.

Notion is the project operating workspace; repository code/data/scenes/resources/tests remain runtime truth.

## Required project context

Resolve when relevant:

```yaml
project_relation:
requirement_id:
responsible_document_id:
related_decision_ids: []
approved_visual_reference_ids: []
screen_id:
flow_id:
visual_map_status:
```

If a required approved direction does not exist, use `MISSING_CANON`. Do not infer canon from a draft Gallery card, archived candidate, rejected image, old chat, or another project.

## Visual direction exploration route

새 프로젝트의 첫 material Visual Direction, 새 핵심 visual family, approved direction 부재·충돌, 그림체·분위기·카메라·렌더 문법의 material 재설계에서는 다음 composed contract를 조건부로 읽는다.

```text
VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE
→ docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md
→ controlled concept options
→ user selection
→ APPROVED_VISUAL_DIRECTION_PACKET
→ bounded production continuity review
```

이 route는 `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 Concept Exploration, current image policy, candidate review와 conversation approval을 대체하지 않고 연결한다.

현재 Project에 유효한 `APPROVED_VISUAL_DIRECTION_PACKET` 또는 동등 Art Bible/Decision이 있고 actual consumer·Flow/Screen·protected identity 전제가 유지되면 이를 재사용한다. 같은 lock 안의 bounded asset마다 concept exploration을 반복하지 않는다.

다음이면 새 contract를 다시 적용하거나 affected scope를 reopen한다.

- current direction이 없음, conflict 또는 superseded
- user Decision이 mood/style/camera/proportion을 material하게 변경
- confirmed Flow/Screen이 바뀌어 기존 anchor가 stale
- runtime evidence가 current lock의 readability/continuity 실패를 증명

방향 탐색 결과와 후속 production asset은 별도 상태다. comparison board나 candidate 승인만으로 `PROJECT_ASSET_APPROVED` 또는 runtime evidence를 주장하지 않는다.

## APPROVED_VISUAL_REFERENCE continuity

For each applicable `APPROVED_VISUAL_REFERENCE`, extract a bounded continuity card:

```text
Keep
→ identity, proportion, silhouette, palette, material/line language, camera/framing, lighting grammar, UI family

Avoid
→ known rejected drift, unreadable detail, pseudo-text, inconsistent icon/material language, accidental style-family changes

Do Not Drift
→ project-specific traits that must remain stable across new images/screens
```

`Keep / Avoid / Do Not Drift` is a constraint summary, not a second canon. If it disagrees with a newer project Decision, record `VISUAL_CANONICAL_CONFLICT` and stop promotion until reconciled.

## Image conversation approval boundary

프로젝트 이미지 **생성·편집**을 실제로 실행할 때는 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`를 함께 적용한다. 이 reference는 아트 Skill의 project-scoped visual 경로에서 항상 적용되므로 Home/Notion 배치 경로를 거치지 않는 직접 이미지 작업도 conversation Gate를 우회하지 않는다.

```text
PROJECT_REVIEW_COMPLETE
→ current Project/Visual canon + Keep/Avoid/Do Not Drift
→ text brief
→ TEXT_BRIEF_STOP_REQUIRED

next user message
→ NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

- text brief를 처음 제시한 같은 assistant turn에서 곧바로 생성/편집으로 넘어가지 않는다.
- 한 번의 승인 뒤 기본 생성은 이미지/편집 결과 1건이다.
- 생성 직후 다음 pose/character/UI/component/decomposition asset을 자동 연쇄 생성하지 않는다.
- 이미 존재하는 승인 Visual의 **배치·링크·readback만** 수행하는 경우에는 새 이미지를 생성하지 않으므로 이 generation checkpoint를 만들지 않는다.
- 생성 성공은 `PROJECT_ASSET_APPROVED`나 runtime integration을 뜻하지 않는다.

## Conditional modules

Load only what the current task needs:

- unresolved/material visual direction exploration and lock → `docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md`
- character face/expression/gaze/head controls → `character-identity-expression-controls.md`
- pose/action/sprite sequence controls → `sprite-pose-sequence-controls.md`
- effect/VFX stage/compositing controls → `effect-stage-compositing-controls.md`
- candidate comparison/reuse harvest → `candidate-review-and-reusable-harvest.md`

Do not load every module by default.

## Screen / flow interpretation

For a visualized screen or flow, preserve machine-readable identifiers behind the human map:

```yaml
screen_id:
flow_id:
artifact_type:
  - SCREEN
  - INTERPRETATION_RECORD
  - VISUAL_MAP
interpretation_status:
  - CONFIRMED
  - DISCOVERED_IDEA
  - AI_ASSUMPTION
runtime_compare_required: true | false
runtime_capture_path:
runtime_compare_status:
```

`DISCOVERED_IDEA` and `AI_ASSUMPTION` must never be silently rewritten as project requirements.

If a prototype or draft shows behavior that is not established in project records, label it as a discovered idea or AI assumption. If actual runtime comparison is required, the evidence type is `RUNTIME_CAPTURE`; a Notion preview does not satisfy it.

## Candidate lifecycle

```text
Visual Requirement Gate
→ conversation Gate when generation/editing is required
→ generate / edit candidate
→ DRAFT_VISUAL or GENERATED_EXPLORATION
→ attach to correct Project record
→ readback
→ Screen Interpretation Review
→ APPROVED_CANDIDATE or REVISION_REQUIRED / REJECTED
→ explicit user/project Decision
→ PROJECT_ASSET_APPROVED
→ repository implementation when required
→ APPLIED_AND_RUNTIME_VERIFIED only with runtime evidence
```

Generation or upload alone never promotes a candidate.

## Readback requirement

After upload, attachment, image replacement, status promotion or visual-map update:

1. fetch the intended Project target again;
2. verify Project relation;
3. verify expected file/preview/version/status;
4. verify an old replaced candidate is not still being presented as current;
5. record readback status.

Failure is `BLOCKED_UNVERIFIED` or an unverified delivery state, not success.

## Reuse harvest

Candidate reuse classification may use:

```text
REUSE_AS_IS
VARIANT_SEED
STRUCTURE_PATTERN
STYLE_DNA
REBUILD_FOR_REUSE
ONE_OFF_KEEP
REJECT_REUSE
```

A reuse classification does not change approval, Project authority, rights or runtime status.

## External-reference boundary

External visual sources are `REFERENCE` or `BENCHMARK` records. Record source provenance and rights/license boundary where material. Extract functional principles and use a `reference_brief`; do not copy identifiable expression or imply that visual similarity grants rights.

## Fail-closed outcomes

Return one or more of these rather than guessing:

```text
MISSING_CANON
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
REVISION_REQUIRED
REJECTED
```

Never promote a cross-project, inaccessible, unverified, rejected or superseded visual as `PROJECT_ASSET_APPROVED`.