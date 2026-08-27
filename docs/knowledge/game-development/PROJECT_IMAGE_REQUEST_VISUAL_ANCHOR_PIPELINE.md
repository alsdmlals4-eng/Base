# Project Image Request Visual Anchor Pipeline

> 사용자가 프로젝트 채팅에서 `이미지 만들어줘`, `그려줘`, `이 화면을 제작해줘`, `이 이미지를 편집해줘`처럼 현재 이미지 출력을 명시적으로 요청했을 때 적용하는 공용 routing owner다. 사용자는 별도 장문 이미지 작업지시문을 반복해서 붙이지 않는다.

```text
EXPLICIT_PROJECT_IMAGE_REQUEST_AUTO_PIPELINE
NO_SEPARATE_LONG_IMAGE_INSTRUCTION_REQUIRED
APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED
EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED
THIN_PIPELINE_NOT_SECOND_VISUAL_CANON
CURRENT_PROJECT_CANON_WINS_ON_DRIFT
HOST_PLATFORM_PRECEDENCE
```

이 문서는 프로젝트의 Art Direction·승인 이미지·Flow·Asset Manifest를 새로 소유하지 않는다. 다음 current owner를 조합한다.

- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`
- `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- exact Project GitHub·Notion·actual implementation

상세 owner와 이 문서가 충돌하면 current Project decision과 상세 owner가 우선한다.

---

## 1. Trigger와 범위

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact Project identity resolve
→ current Project GitHub·Notion·actual implementation fresh-read
→ exact requirement / actual consumer resolve
→ approved visual direction resolve
→ current request에 맞는 한 output route 선택
```

현재 사용자의 명시적 이미지 요청은 **현재 요청 범위의 시각 결과 1건**을 만들기 위한 authority다. 별도 장문 문구를 다시 요구하지 않는다.

이 authority가 허용하는 결과는 둘 중 하나다.

1. 사용 가능한 승인 시각 앵커가 있으면 그 앵커를 적용한 요청 자산/목업 후보 1건
2. 사용 가능한 승인 시각 앵커가 없으면 1안을 선택하기 위한 concept comparison deliverable 1건

다음 권한은 생기지 않는다.

- 다음 캐릭터·다음 화면·다음 variant 자동 생성
- current Slice나 asset count 확대
- 생성 결과 자동 승인
- Notion/Manifest/runtime 자동 승격 주장
- 새 core identity·Art Direction 자동 확정
- 권리 불명확 source 사용

프로젝트가 불명확하거나 actual consumer가 없으면 추측하지 않는다.

```text
EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED
→ unresolved: BLOCKED_UNVERIFIED | DO_NOT_GENERATE
```

---

## 2. 승인 시각 방향 탐색

### 2.1 Authority order

```text
latest explicit user visual decision
→ current Project confirmed Decision / Active Context
→ Notion Project Home / Visual Bible / approved Asset·Reference
→ repository ASSET_MANIFEST / structured visual canon
→ actual runtime visual truth when already implemented
→ approved external reference with provenance
→ draft / candidate / historical material
```

Draft, rejected, archived, replaced, superseded, 다른 프로젝트의 이미지는 current 1안이 아니다.

### 2.2 Anchor resolution receipt

```yaml
VISUAL_ANCHOR_RESOLUTION_RECEIPT:
  project:
  image_request:
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
  readback_status:
  conflict:
  result: APPROVED_VISUAL_ANCHOR_FOUND | NO_USABLE_APPROVED_VISUAL_ANCHOR | MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT | APPROVED_ANCHOR_BINARY_UNREADABLE | BLOCKED_UNVERIFIED
```

### 2.3 Usable anchor 조건

```text
APPROVED_VISUAL_ANCHOR_FOUND
```

은 다음을 모두 요구한다.

- current Project에 관계됨
- 사용자/프로젝트 authority가 승인함
- superseded/replaced가 아님
- 현재 요청의 global style 또는 해당 surface/layer 역할에 적용 가능함
- 실제 preview 또는 source binary/원본에 접근 가능함
- approval·version·preview/binary destination readback이 일치함

```text
ANCHOR_PREVIEW_OR_BINARY_READBACK_REQUIRED
```

텍스트 설명만 있거나 thumbnail 이름만 있고 실제 시각물을 읽지 못하면 같은 그림체를 봤다고 주장하지 않는다.

```text
APPROVED_ANCHOR_BINARY_UNREADABLE
→ BLOCKED_UNVERIFIED
```

이 경우 승인 방향을 자동 교체하거나 기억으로 재현하지 않는다. 원본 recovery, 사용자 재제공 또는 explicit re-exploration이 필요하다.

### 2.4 Global과 layer anchor

한 프로젝트가 반드시 모든 layer를 같은 렌더링 밀도로 만들 필요는 없다.

```text
global visual grammar
→ palette family / shape language / material language / camera tendency / lighting grammar / identity hierarchy

surface_layer_anchor
→ character / environment / UI / icon / VFX / marketing 등 해당 역할의 구체 표현
```

현재 요청에 유효한 layer anchor가 있으면 global anchor와 함께 사용한다. 서로 충돌하면 더 최신의 explicit Decision으로 reconcile하기 전 production을 중지한다.

---

## 3. 승인 1안이 있는 경로

```text
APPROVED_VISUAL_ANCHOR_FOUND
→ SURFACE_APPROVED_ANCHOR_TO_USER
→ continuity constraints extract
→ current Flow / Screen / System context apply when relevant
→ USE_CURRENT_APPROVED_ANCHOR
→ requested visual output exactly one
→ STOP_REQUIRED_AFTER_GENERATION
```

### 3.1 사용자에게 보여주기

```text
SURFACE_APPROVED_ANCHOR_TO_USER
```

- host가 actual preview를 표시할 수 있으면 현재 승인 이미지 자체를 보여준다.
- preview를 직접 표시할 수 없으면 approved reference ID·version·locator와 `Keep / Avoid / Do Not Drift` 요약을 제시한다.
- 실제 binary/readback 없이 보여줬다고 주장하지 않는다.
- current request가 이미 명시적 생성 요청이면 별도 장문 작업지시문을 다시 받지 않고 해당 앵커로 요청 결과 1건을 진행할 수 있다.

### 3.2 기존 앵커를 바꾸려는 요청

사용자가 새 스타일 탐색·Art Direction 변경을 명시했다면 current anchor가 존재해도 production route를 사용하지 않는다.

```text
MATERIAL_VISUAL_DIRECTION_CHANGE_REQUEST
→ preserve current anchor as current until replacement approved
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ user decision
```

---

## 4. 승인 1안이 없는 경로

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ COMPARISON_BOARD_ONE_DELIVERABLE
→ THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS
→ CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION
→ user compares
→ USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

사용자가 이미 `이미지 만들어줘`라고 명시했으므로, 별도 장문 pipeline 설명을 다시 요구하지 않고 **비교용 concept deliverable 1건**을 만든다.

### 4.1 Comparison deliverable

```text
COMPARISON_BOARD_ONE_DELIVERABLE
THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS
```

기본값은 같은 실제 consumer/scene/subject를 유지한 3개의 실질적으로 다른 후보다. 프로젝트 사정상 2개 또는 4개가 더 적합하면 이유를 기록할 수 있다.

비교축 예:

- mood / fantasy / emotional temperature
- art style / pixel density / line or material language
- palette / value / lighting
- camera / framing / composition
- detail density / readability distance
- UI ornament / hierarchy

기계·게임 규칙·캐릭터 identity까지 옵션마다 임의로 바꾸지 않는다. 한 번에 비교할 핵심 축을 좁혀 무엇을 선택하는지 알 수 있게 한다.

```text
CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION
COMPARISON_SHEET_NOT_PRODUCTION_ASSET
```

- 비교 보드는 `GENERATED_EXPLORATION`이다.
- 한 보드 안의 후보 panel은 runtime sprite·background·UI asset이 아니다.
- 설명용 장식 시트가 아니라 실제 planned consumer의 시각 방향을 결정하기 위한 comparison이다.
- pseudo-text 위험이 있으면 이미지 내부 긴 설명 대신 바깥의 구조화된 option card로 의미를 설명한다.
- 생성 성공으로 어느 옵션도 자동 승인되지 않는다.

### 4.2 사용자 선택

```text
USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION
```

사용자가 A/B/C, 위치, candidate ID 등으로 하나를 선택해야 한다. 선택 메시지는 선택된 방향의 standalone anchor 제작 authority가 될 수 있다.

```text
SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR
```

comparison panel을 그대로 잘라 최종 master나 runtime asset으로 쓰지 않는다. 선택 방향을 clean standalone visual anchor로 다시 제작·검수하고, 사용자가 project direction으로 승인한 뒤 current anchor로 기록한다.

---

## 5. Visual Direction Lock

사용자 선택·승인 뒤 project-specific current owner에 다음 receipt를 기록한다.

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
  notion_destination:
  repository_or_manifest_destination:
  destination_readback:
  evidence_ceiling:
  result: APPROVED_VISUAL_REFERENCE | REVISION_REQUIRED | BLOCKED_UNVERIFIED
```

`VISUAL_DIRECTION_LOCK_PACKET`은 Project Decision·Visual Bible·approved Asset record를 연결하는 receipt이지 두 번째 Art Bible이 아니다.

- Notion은 사람이 보는 current 1안·이유·Keep/Avoid/Do Not Drift를 보여준다.
- repository는 structured identity·manifest·implementation locator를 소유한다.
- 실제 image binary owner는 project policy를 따른다.
- 교체된 1안은 `superseded_reference_ids`에 명시하고 current처럼 노출하지 않는다.

---

## 6. 이후 이미지 제작의 일관성

승인 앵커가 생긴 뒤 사용자가 새 이미지를 요청하면 매번 같은 긴 지시문을 요구하지 않는다.

```text
explicit current image request
→ exact consumer
→ current approved anchor readback
→ relevant Flow / Screen / System
→ Keep / Avoid / Do Not Drift
→ one requested output
→ adversarial visual review
→ correction / review result
```

### 6.1 Style continuity

```text
STYLE_CONTINUITY_REVIEW_REQUIRED
NO_UNAPPROVED_STYLE_DRIFT
```

검수 축:

- project identity / silhouette / proportion
- palette family / value hierarchy
- line·shape·material language
- camera / framing / perspective
- lighting grammar
- UI / icon / VFX family
- intended gameplay scale와 readability
- current layer가 허용한 variation

모든 이미지를 복사처럼 만들지 않는다. 지역·상태·진영·시간대 차이는 허용하되 project visual grammar와 승인 hierarchy를 유지한다.

### 6.2 Flow와 screen semantics

```text
FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
```

Screen·HUD·flow image이면 current approved Flow/Screen/System을 읽는다.

- entry / primary action / choice / result / feedback 위치가 current flow와 맞는가
- 아직 승인되지 않은 버튼·상태·시스템을 그림이 새 요구사항처럼 추가하는가
- 실제 consumer crop·aspect·viewing distance에서 핵심 정보가 읽히는가
- 기획용 mockup과 runtime asset 역할이 구분되는가

Flow context가 필요하지만 current source가 없으면 이미지를 통해 규칙을 발명하지 않고 `MISSING_FLOW_CONTEXT`로 돌린다.

### 6.3 Adversarial review와 교정

최소 다음 다섯 lens로 결과를 재검토한다.

1. **Canon/anchor** — current 승인 1안과 identity를 지켰는가
2. **Consumer/flow** — 실제 사용처와 행동·정보 의미가 맞는가
3. **Style continuity** — palette·camera·lighting·material·UI family drift가 없는가
4. **Artifact/technical** — anatomy, edge, crop, alpha, pseudo-text, resolution/import 결함이 없는가
5. **Lifecycle/evidence** — exploration·approval·asset·runtime 상태를 혼동하지 않았는가

```text
OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE
```

현재 승인된 output의 객관적 결함은 사용자가 장문 pipeline을 다시 입력하지 않아도 bounded correction할 수 있다.

허용되는 correction:

- artifact / anatomy / edge / crop 오류
- 잘못된 alpha·margin·dimension·format
- 승인 팔레트·silhouette·camera·UI family에서 벗어난 명백한 drift
- current consumer/Flow와 다른 버튼·상태·정보 배치
- 가독성을 파괴하는 디테일·대비 문제

새 creative option, 새 스타일, 새 pose set, 다른 asset, asset count 확대, core identity 변경은 같은 correction이 아니다.

host가 결과를 사용자에게 노출하기 전에 내부 review/retry를 지원하지 않으면 자동 교정했다고 주장하지 않는다. 해당 결과를 `REVISION_REQUIRED`로 표시하고 다음 explicit correction request를 받는다. visible automatic image chain은 만들지 않는다.

---

## 7. Candidate·approval·runtime 상태

```text
GENERATED_EXPLORATION != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED
```

```text
generation output
→ GENERATED_EXPLORATION or DRAFT_VISUAL
→ adversarial review
→ APPROVED_CANDIDATE | REVISION_REQUIRED | REJECTED
→ explicit project/user approval
→ approved visual reference / PROJECT_ASSET_APPROVED when applicable
→ repository implementation
→ runtime evidence
→ RUNTIME_PROMOTED or APPLIED_AND_RUNTIME_VERIFIED
```

- concept comparison은 production asset이 아니다.
- standalone anchor approval도 해당 style direction의 승인이지 모든 파생 image의 자동 승인이 아니다.
- Notion preview PASS는 source master·manifest·runtime PASS가 아니다.
- 생성된 이미지가 actual consumer에 쓰이지 않으면 runtime completion을 주장하지 않는다.

---

## 8. Fail-closed outcomes

```text
BLOCKED_UNVERIFIED
DO_NOT_GENERATE
NO_USABLE_APPROVED_VISUAL_ANCHOR
MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT
APPROVED_ANCHOR_BINARY_UNREADABLE
VISUAL_CANONICAL_CONFLICT
MISSING_FLOW_CONTEXT
REVISION_REQUIRED
REJECTED
```

```text
MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT
→ current approval refs / previews surface
→ VISUAL_CANONICAL_CONFLICT
→ user/project authority reconciliation
→ no production generation until resolved
```

다른 프로젝트의 스타일을 편의상 빌리거나, old chat·memory·rejected candidate를 current 1안으로 추정하지 않는다.

---

## 9. Clean exit checklist

```text
explicit project image request identified
exact Project and actual consumer confirmed
current approved visual direction resolved
usable anchor found and surfaced OR comparison deliverable generated
comparison never promoted as runtime asset
selected direction locked as standalone anchor when required
Flow/Screen context applied when relevant
style continuity + semantic consistency reviewed
objective correction bounded to approved deliverable
no automatic next-image chain
candidate / approval / asset / runtime states separated
required Notion / repository destination readback complete
```
