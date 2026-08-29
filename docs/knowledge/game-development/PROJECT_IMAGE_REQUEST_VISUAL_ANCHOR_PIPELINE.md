# Project Image Request Visual Anchor Pipeline

이 문서는 프로젝트 이미지 candidate를 만들 때 현재 프로젝트의 승인 방향과 실제 소비처를 자동 복원하는 얇은 routing owner다. 사용자는 이미지마다 별도 장문 작업지시문을 반복하지 않는다.

```text
EXPLICIT_PROJECT_IMAGE_REQUEST_AUTO_PIPELINE
APPROVED_WORK_VISUAL_NEED_AUTO_PIPELINE
NO_SEPARATE_LONG_IMAGE_INSTRUCTION_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED
REPOSITORY_FIRST_VISUAL_AUTHORITY
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
POST_GENERATION_USER_LOCK_REQUIRED
THIN_PIPELINE_NOT_SECOND_VISUAL_CANON
CURRENT_PROJECT_CANON_WINS_ON_DRIFT
HOST_PLATFORM_PRECEDENCE
```

이 문서는 새 Art Bible이나 asset canon을 만들지 않는다. 다음 current owner를 조합한다.

- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`
- `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`

마지막 세 Notion 이름의 owner는 legacy migration이나 이미 채택한 프로젝트 예외에서만 읽는다. 기본 current authority는 repository의 AGENTS, Decision, Visual owner, ASSET_MANIFEST, 실제 binary·consumer·runtime evidence다.

## 1. Trigger

### 1.1 현재 사용자가 이미지 출력을 명시한 경우

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact project and consumer resolve
→ current repository visual authority readback
→ current approved visual anchor resolve
→ one bounded candidate deliverable
→ objective QA
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
```

현재 요청은 `EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY`다. 별도 장문 승인문이나 다음 turn의 중복 사전 승인을 요구하지 않는다.

### 1.2 승인된 작업 중 이미지 필요성이 확인된 경우

```text
VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK
→ actual/planned consumer confirmed
→ project canon and existing visual readback complete
→ candidate scope and no-drift constraints complete
→ NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
→ one bounded candidate deliverable
→ objective QA
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
```

이 경로도 candidate 생성 권한만 만든다. final Art Direction, canon registration, product implementation과 runtime promotion은 자동 승인하지 않는다.

## 2. Authority order

```text
latest explicit user decision
→ project AGENTS / current Decision / Active Context
→ repository human Visual owner / approved reference record
→ repository ASSET_MANIFEST / provenance / actual binary
→ actual current implementation and consumer
→ project-adopted Base owner
→ legacy Notion / Sheets / historical candidate
```

Draft, rejected, archived, replaced, superseded, 다른 프로젝트의 이미지 또는 metadata-only record는 current anchor가 아니다.

## 3. Anchor resolution receipt

```yaml
VISUAL_ANCHOR_RESOLUTION_RECEIPT:
  project:
  image_request_or_need:
  requirement_id:
  consumer_kind:
  consumer_surface:
  primary_use:
  global_style_anchor:
  surface_layer_anchor:
  flow_screen_context:
  approved_visual_reference_ids: []
  preview_or_binary_locators: []
  approval_refs: []
  superseded_reference_ids: []
  keep: []
  avoid: []
  do_not_drift: []
  readback_status:
  conflict:
  result: APPROVED_VISUAL_ANCHOR_FOUND | NO_USABLE_APPROVED_VISUAL_ANCHOR | MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT | APPROVED_ANCHOR_BINARY_UNREADABLE | VISUAL_CANONICAL_CONFLICT | BLOCKED_UNVERIFIED
```

`APPROVED_VISUAL_ANCHOR_FOUND`는 다음을 모두 요구한다.

- current project와 consumer에 관련됨
- current authority가 승인함
- superseded가 아님
- global style 또는 해당 surface layer에 적용 가능함
- actual preview/source binary를 직접 읽을 수 있음
- approval, version, binary locator와 destination readback이 일치함

```text
ANCHOR_PREVIEW_OR_BINARY_READBACK_REQUIRED
```

텍스트 설명이나 파일명만 있고 pixels/source를 읽지 못하면 같은 시각 방향을 확인했다고 주장하지 않는다.

```text
APPROVED_ANCHOR_BINARY_UNREADABLE
→ BLOCKED_UNVERIFIED
```

여러 current anchor가 충돌하면 `MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT` 또는 `VISUAL_CANONICAL_CONFLICT`로 fail closed한다.

## 4. 승인 anchor가 있는 경로

```text
APPROVED_VISUAL_ANCHOR_FOUND
→ SURFACE_APPROVED_ANCHOR_TO_USER
→ continuity constraints extract
→ relevant Flow / Screen / System context apply
→ USE_CURRENT_APPROVED_ANCHOR
→ one bounded candidate output
→ STYLE_CONTINUITY_REVIEW_REQUIRED
→ FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
→ STOP_REQUIRED_AFTER_GENERATION
→ user decision
```

`SURFACE_APPROVED_ANCHOR_TO_USER`:

- host가 actual preview를 표시할 수 있으면 current anchor를 보여 준다.
- 표시할 수 없으면 reference ID, version, locator와 Keep/Avoid/Do Not Drift를 제시한다.
- actual readback 없이 보여 줬다고 주장하지 않는다.

새 스타일 탐색이나 master Art Direction 교체가 명시된 경우 current anchor를 바로 덮어쓰지 않는다.

```text
MATERIAL_VISUAL_DIRECTION_CHANGE_REQUEST
→ preserve current anchor
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ user decision
```

## 5. 승인 anchor가 없는 경로

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ COMPARISON_BOARD_ONE_DELIVERABLE
→ THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS
→ CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION
→ user compares
→ USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

비교 deliverable은 같은 actual/planned consumer와 subject를 유지한 실질적으로 다른 옵션을 기본 3개 제시한다. 비교할 축은 mood, palette, material, line, camera, detail density, readability 중 이번 결정에 필요한 것만 사용한다.

```text
CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION
COMPARISON_SHEET_NOT_PRODUCTION_ASSET
```

- comparison board와 panel은 runtime asset이 아니다.
- 생성 성공으로 어느 옵션도 자동 승인되지 않는다.
- 긴 pseudo-text를 이미지 내부에 넣지 않고 option 설명은 text-native card로 분리한다.

```text
USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR
```

선택된 panel crop을 final master로 사용하지 않는다. standalone anchor candidate를 다시 만들고 사용자가 lock한 뒤 current approved reference로 등록한다.

## 6. Visual Direction Lock Packet

사용자 `LOCK` 뒤 current repository owner에 다음 receipt를 기록한다.

```yaml
VISUAL_DIRECTION_LOCK_PACKET:
  project:
  decision_id:
  requirement_or_scope:
  global_style_anchor:
  surface_layer_anchor:
  approved_visual_reference_ids: []
  flow_screen_context:
  mood_and_emotion:
  palette_value_lighting:
  shape_line_material_language:
  camera_framing_composition:
  detail_density_and_readability:
  ui_icon_vfx_family:
  keep: []
  avoid: []
  do_not_drift: []
  permitted_layer_variation: []
  superseded_reference_ids: []
  provenance_and_rights:
  repository_or_manifest_destination:
  destination_readback:
  evidence_ceiling:
  result: APPROVED_VISUAL_REFERENCE | REVISION_REQUIRED | BLOCKED_UNVERIFIED
```

`VISUAL_DIRECTION_LOCK_PACKET`은 current Decision·Visual owner·approved asset record를 연결하는 receipt이지 두 번째 Art Bible이 아니다.

## 7. Candidate continuity review

```text
STYLE_CONTINUITY_REVIEW_REQUIRED
NO_UNAPPROVED_STYLE_DRIFT
FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE
```

검수 축:

1. current Canon/anchor와 identity
2. actual consumer와 행동·정보 의미
3. palette·camera·lighting·material·UI family continuity
4. anatomy·edge·crop·alpha·pseudo-text·resolution/import 결함
5. exploration·approval·asset·runtime evidence 경계

current Flow/Screen/System에 없는 버튼·상태·규칙을 이미지가 새 요구사항처럼 발명하지 않는다. Flow context가 없으면 `MISSING_FLOW_CONTEXT`다.

같은 bounded deliverable의 객관적 결함은 재장문 요청 없이 correction할 수 있다. 새 스타일, 새 pose set, 별도 asset 또는 scope expansion은 새 need/consumer 판정을 거친다.

## 8. Candidate lifecycle

```text
GENERATED_EXPLORATION
→ GENERATED_CANDIDATE
→ REVIEWED
→ USER_APPROVED
→ PROJECT_ASSET_APPROVED
→ CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_PROMOTED
→ RUNTIME_VERIFIED
```

```text
GENERATED_EXPLORATION != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED
GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED
```

사용자 lock 전에 repository product asset, runtime-ready 또는 구현 완료로 승격하지 않는다. lock 뒤에도 rights, provenance, SHA-256, state mapping, Primary Use Gate와 runtime evidence는 별도다.

## 9. Bounded output와 자동 연쇄 금지

```text
GENERATE_EXACTLY_ONE
BOUNDED_STATE_FAMILY_ALLOWED_WHEN_CONSUMER_REQUIRES
NO_AUTOMATIC_IMAGE_CHAIN
```

한 deliverable은 다음 중 하나다.

- candidate image/edit 1건
- concept comparison board 1건
- 한 실제 consumer가 동시에 요구하는 bounded state family 1세트

한 candidate의 성공을 근거로 다음 캐릭터, 화면, pose, variant 또는 production batch를 자동 확장하지 않는다.

## 10. Blueprint 관계

Blueprint 검수에 필요한 image candidate는 최종 Blueprint 승인 전에 만들 수 있다.

```text
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ GENERATED_CANDIDATE review
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

candidate 준비는 신규 runtime 구현 승인과 다르다.

## 11. Specialist-owner composition

```text
THIN_PIPELINE_NOT_SECOND_VISUAL_CANON
```

- requirement selection: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- generation/review lifecycle: `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- conversation timing and final lock: `IMAGE_CONVERSATION_APPROVAL_GATE.md`
- continuity helper: `notion-project-visual-continuity-gate.md`
- candidate QA/reuse: `candidate-review-and-reusable-harvest.md`
- legacy Notion migration placement only: `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`

Repository-first project에서 Notion specialist는 current canon이나 필수 destination이 아니다.

## 12. Evidence ceiling

```text
candidate preview != source binary readback
source binary readback != user lock
user lock != repository registration
repository registration != implementation
implementation != runtime verification
```

host/system 정책이 더 엄격하면 `HOST_PLATFORM_PRECEDENCE`를 따른다. 실행하지 않은 image generation, readback, runtime 또는 Human verification은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.