# RM-WORK-003 · Human-Facing Artifact Synthesis

- candidate_origin: `HYBRID`
- maturity: `MODULE_CONTRACT_DEFINED`
- validation_state: `VALIDATION_NOT_RUN`
- default_provider: `NONE`
- authority: provider-neutral workflow candidate; existing document/Notion/repository owners remain authoritative
- cost boundary: no new paid SaaS/API/subscription is required by this contract

## Purpose

`HUMAN_FACING_ARTIFACT_SYNTHESIS`는 발표자료·사람용 설명문서·시각 요약처럼 **구조와 시각 배치가 함께 필요한 human-facing artifact**를 만들 때, 내용 정본을 바로 자동-layout에 던지지 않고 구조·근거·시각 제약·사람 검수 단계를 분리하는 workflow candidate다.

새 presentation 앱이나 새로운 문서 authority가 아니다. 현재 Base의 `managing-design-documents`, Notion human surface, repository structured/runtime truth를 소비하며 그 authority를 대체하지 않는다.

```text
PROVIDER_USE_IS_OPTIONAL_NOT_BASE_DEPENDENCY
DEFAULT_PROVIDER: NONE
```

## Discovery and evidence boundary

사용자가 제시한 `https://todayfreeai.com/recommendations/make-presentation/`는 2026-08-22 현재 실행 환경에서 직접 본문 fetch가 `Cache miss`로 실패했다. 따라서 TodayFreeAI 페이지의 정확한 제품 목록·평가·추천문을 확인했다고 주장하지 않는다. 이 URL은 `DISCOVERY_ONLY`다.

반복 패턴은 2026-08-22 각 제품의 공식 자료를 별도로 확인해 추출했다.

| Provider | 공식 원출처에서 확인한 현재 기능 범위 | 여기서 추출한 원리 | Claim ceiling |
|---|---|---|---|
| Gamma | Generate / Paste / Import, source 기반 생성, editable slides, theme/layout, export. Import는 text 중심이며 원래 styling/layout을 그대로 가져오지 않음 | 입력 모드 분리, editable artifact, import-content와 visual canon 분리 | Gamma 채택/품질 PASS 아님 |
| Canva | Magic Design 기반 presentation draft, drag/drop 편집, branding 적용 | 생성 전/후 brand constraint와 human editability | Canva 채택/품질 PASS 아님 |
| Beautiful.ai | prompt → text-only outline → outline edit/reorder → visual preferences → designed slides | `OUTLINE_BEFORE_LAYOUT`, 구조 검토와 시각 생성 분리 | Beautiful.ai 채택/품질 PASS 아님 |
| Pitch | prompt/files/template 기반 생성, chat refine, deck 질문/weak proof point·gap 확인, template 기반 brand, editable workspace | post-generation claim-gap review, brand/template constraint, editable output | Pitch 채택/품질 PASS 아님 |
| SlidesAI | topic + audience/type/tone → outline review/edit → theme → presentation 생성 | audience packet, outline gate, staged generation | SlidesAI 채택/품질 PASS 아님 |

Provider의 마케팅 문구·사용자 수·품질 주장은 Base의 효과 evidence로 사용하지 않는다.

## Input modes

### `INPUT_MODE_GENERATE`

주제와 목표에서 새 artifact 초안을 만든다.

### `INPUT_MODE_STRUCTURE_EXISTING`

이미 확정된 text/canon/analysis를 새 사실을 발명하지 않고 human-facing 구조로 정리한다.

### `INPUT_MODE_IMPORT`

기존 문서·deck·structured source를 가져와 새 artifact 구조에 매핑한다.

```text
IMPORTED_CONTENT_IS_NOT_IMPORTED_VISUAL_CANON
```

기존 내용을 import했다는 사실은 기존 layout/theme/visual language가 그대로 보존됐다는 뜻이 아니다. 원본 visual canon을 보존해야 하면 별도 constraint와 comparison evidence가 필요하다.

## Canonical workflow candidate

```text
INPUT_MODE_GENERATE | INPUT_MODE_STRUCTURE_EXISTING | INPUT_MODE_IMPORT
→ SOURCE_AND_AUDIENCE_PACKET
→ OUTLINE_BEFORE_LAYOUT
→ CLAIM_AND_EVIDENCE_CHECK
→ BRAND_VISUAL_CONSTRAINTS_BEFORE_GENERATION
→ EDITABLE_BLOCK_ARTIFACT
→ LAYOUT_VARIANTS_WITH_CONTENT_PRESERVATION
→ CLAIM_GAP_REVIEW_AFTER_GENERATION
→ HUMAN_VISUAL_REVIEW
→ EXPORT_DERIVATIVE
```

### `SOURCE_AND_AUDIENCE_PACKET`

```yaml
artifact_goal:
audience:
source_of_truth:
required_claims: []
claims_needing_evidence: []
content_that_must_not_change: []
visual_constraints:
brand_or_project_visual_language:
output_format:
```

사람용 artifact가 source of truth를 새로 만들지 않는다. 기존 project/repository/Notion authority에서 파생한다.

### `OUTLINE_BEFORE_LAYOUT`

시각 디자인 전에 section/slide 순서와 목적을 text-level로 먼저 검토한다.

최소 질문:

- 각 section/slide가 하나의 분명한 목적을 갖는가.
- 순서가 독자의 판단 흐름과 맞는가.
- 중복 또는 빠진 전제가 있는가.
- 결론이 근거보다 먼저 과장되어 있지 않은가.
- 삭제해도 의미가 유지되는 장식적 section은 없는가.

구조 승인 전 고비용 시각 polish를 반복하지 않는다.

### `CLAIM_AND_EVIDENCE_CHECK`

artifact에 들어갈 외부 사실·수치·상태 claim을 원 source와 대조한다. AI가 빈칸을 자연스럽게 채웠다는 이유로 새로운 사실을 정본화하지 않는다.

```text
AI_DRAFT_IS_NOT_APPROVED_NARRATIVE
```

### `BRAND_VISUAL_CONSTRAINTS_BEFORE_GENERATION`

가능하면 layout 생성 전에 색·폰트·spacing·image style·tone·visual reference의 허용 범위를 정한다. provider의 default theme가 project visual canon을 대체하지 않는다.

```text
BRAND_TEMPLATE_IS_NOT_PROJECT_CANON_BY_ITSELF
```

### `EDITABLE_BLOCK_ARTIFACT`

초기 결과는 가능한 경우 사람이 section/slide/block 단위로 수정 가능한 구조를 유지한다. 이미지로 flatten된 결과만 만들고 다시 처음부터 생성하는 workflow를 기본값으로 삼지 않는다.

### `LAYOUT_VARIANTS_WITH_CONTENT_PRESERVATION`

layout 대안을 만들 때 이미 승인된 핵심 내용과 claim identity를 보존한다. 구조적 내용 변경과 시각 layout 변경을 같은 diff로 숨기지 않는다.

### `CLAIM_GAP_REVIEW_AFTER_GENERATION`

생성 후 artifact 자체를 다시 공격한다.

- 가장 중요한 claim은 무엇이며 evidence가 충분한가.
- 반론/질문에 답하지 못하는 부분은 어디인가.
- 너무 많은 일을 하는 slide/section은 어디인가.
- 약한 proof point, 설명되지 않은 숫자, 누락된 맥락이 있는가.
- source에는 있으나 artifact에서 사라진 중요한 제한조건이 있는가.

Pitch의 current official pattern처럼 deck 자체에 질문하는 방식은 참고할 수 있지만, 특정 provider가 없어도 같은 review를 GPT/사람/기존 review owner로 수행할 수 있어야 한다.

### `HUMAN_VISUAL_REVIEW`

```text
AUTO_LAYOUT_IS_NOT_DESIGN_QUALITY_PASS
```

실제 사람이 가독성·정보 위계·밀도·시각 일관성·이미지 적합성·핵심 메시지 전달을 검수한다. 자동 layout 성공 또는 export 성공은 human visual PASS가 아니다.

### `EXPORT_DERIVATIVE`

PPTX/PDF/PNG/공유 링크 등 export는 원본 구조/정본의 파생 산출물이다.

```text
EXPORT_IS_DERIVATIVE_NOT_CANON
```

export 파일에서 역으로 project canon을 덮어쓰지 않는다. 수정이 필요하면 source/authoritative artifact를 고친 뒤 다시 export한다.

## Existing Solution First

이 candidate는 다음 순서를 따른다.

1. 현재 Base 문서 생성/Notion human surface로 충분한가.
2. 기존 Markdown/Docs/Slides/PPTX workflow에서 outline·evidence·visual review만 추가하면 되는가.
3. 사용자가 이미 쓰는 도구 또는 무료 경로로 해결 가능한가.
4. 특정 presentation provider의 기능이 현재 workload를 실제로 줄이는가.
5. provider adoption이 필요한 경우에만 비용·권한·import/export fidelity·데이터 처리·lock-in을 별도 평가한다.

특정 provider 기능이 편리하다는 이유만으로 Base 기본 dependency로 채택하지 않는다.

## Context-synthesis packet

```yaml
candidate_id: RM-WORK-003
candidate_origin: HYBRID
context_basis:
  - 사람용 결과와 AI/System 정본의 분리가 현재 Base에서 중요함
  - 자료/기획을 한 번 구조화한 뒤 여러 human-facing output으로 파생할 반복 가능성이 있음
planned_consumers:
  - managing-design-documents
  - project human-facing Notion/publication flows
falsification_test:
  - outline/evidence/review 단계가 total human edit + QA cost를 줄이지 못하면 공용 workflow로 승격하지 않음
smallest_pilot:
  - 기존 승인 자료 하나를 source로 동일 내용의 human-facing artifact 1개를 생성하고 기존 방식과 HUMAN_EDIT_DELTA 비교
rollback_or_discard_condition:
  - 단계가 문서 생산을 복잡하게 만들거나 provider-specific 예외가 neutral contract보다 커지면 reference-only로 낮춤
maturity: MODULE_CONTRACT_DEFINED
validation_state: VALIDATION_NOT_RUN
```

## Validation before promotion

`RM-WORK-003`은 현재 `BASE_ACTIVE_METHOD`가 아니다.

승격 전 최소 증거:

- 실제 Base/project human-facing artifact consumer 1개 이상의 Pilot.
- source claim 누락/변형 여부 비교.
- outline-first가 재작업을 줄였는지 `HUMAN_EDIT_DELTA` 또는 동등한 total-effort 기록.
- provider를 썼다면 provider 없이도 contract가 유지되는지 확인.
- human visual review 결과.
- export/readback이 원 source/canon과 일치하는지 확인.

현재 상태는 `MODULE_CONTRACT_DEFINED · VALIDATION_NOT_RUN`을 넘지 않는다.
