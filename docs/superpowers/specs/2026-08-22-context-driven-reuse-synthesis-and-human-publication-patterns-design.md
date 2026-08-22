# Context-Driven Reuse Synthesis + Human-Facing Artifact Patterns Design

- date: 2026-08-22
- status: APPROVED_FOR_IMPLEMENTATION
- user direction: 실제 반복 기록이 없어도 프로젝트 컨텍스트를 읽고 새 구조·모듈을 능동적으로 설계할 수 있어야 한다. TodayFreeAI의 presentation-AI 사례도 참고하되 실제 흡수 가치는 원출처로 검증한다.

## 1. Problem

현재 Reuse Pipeline은 `PROJECT_CANON_FIRST`와 `PROJECT_SPECIFIC_SYNTHESIS`를 이미 갖고 있지만 실제 candidate origin은 반복 병목·외부 사례·기존 구현에서 **발견**하는 경로에 더 강하게 기울어 있다. 이 구조만 따르면 다음 기회를 놓칠 수 있다.

- 아직 한 번밖에 구현되지 않았지만 roadmap상 여러 consumer가 예정된 공통 primitive
- 반복 오류 기록은 없지만 현재 책임 결합만으로 미래 수정비 증가가 예측되는 구조
- 여러 프로젝트 계획을 함께 보면 아직 구현 전인데도 공용 계약이 자연스럽게 드러나는 경우
- 한 번 입력한 구조화 데이터를 여러 문서·화면·검증기가 소비하게 만들어 중복입력을 제거할 수 있는 경우
- 기존 모듈 둘 이상을 더 작은 neutral primitive로 재조합할 수 있는 경우

반대 위험도 있다. 컨텍스트만으로 만든 아이디어를 곧바로 `검증됨`, `공용화 완료`, `재미 PASS`로 올리면 과설계와 잘못된 일반화가 발생한다.

## 2. Decision

Reuse candidate는 두 개의 동등한 origin path를 허용한다.

```text
A. EVIDENCE_DERIVED
실제 코드 / 반복 병목 / 벤치마크 / 실패 / 프로젝트 사례
→ 반복 불변원리 추출

B. CONTEXT_SYNTHESIZED
프로젝트 목표 / 구조 / 제약 / roadmap / 예상 반복비용 / planned consumers
→ 아직 존재하지 않는 더 나은 계약을 설계

A + B가 함께 쓰이면 HYBRID
```

둘은 이후 같은 Gate로 합류한다.

```text
PROJECT_CANON_FIRST
→ ORIGIN_PATH
→ EXISTING_SOLUTION_FIRST
→ REUSABLE_CONTRACT
→ PROJECT_FIT_AND_NOVELTY_DELTA
→ OWNER_ROUTING
→ PILOT / VALIDATION
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE | BASE_ACTIVE_METHOD
```

## 3. Three-axis state model

후보의 출처, 성숙도, 검증을 하나의 문자열로 섞지 않는다.

```yaml
origin:
  EVIDENCE_DERIVED | CONTEXT_SYNTHESIZED | HYBRID
maturity:
  HYPOTHESIS | MODULE_CONTRACT_DEFINED | REFERENCE_IMPLEMENTATION_EXISTS | PROJECT_ADAPTER_VERIFIED | PROJECT_MERGED
validation:
  NOT_RUN | FOCUSED_VERIFIED | MULTI_CONTEXT_VERIFIED | PLAYER_OR_USER_VERIFIED
```

### 핵심 ceiling

```text
SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS
CONTEXT_SYNTHESIS_CAN_DEFINE_CONTRACT
CONTEXT_SYNTHESIS_IS_NOT_VALIDATION
REFERENCE_IMPLEMENTATION_IS_NOT_PROJECT_ADOPTION
PROJECT_ADAPTER_VERIFIED_IS_NOT_PLAYER_VALUE_PASS
EVIDENCE_REQUIRED_FOR_PROMOTION
```

Context-Synthesized 후보는 외부 사례가 없어도 `HYPOTHESIS` 또는 `MODULE_CONTRACT_DEFINED`까지 갈 수 있다. 그러나 실제 구현·프로젝트 적용·Base active method·player value를 주장하려면 해당 수준의 실행 증거가 필요하다.

## 4. Context synthesis triggers

다음 신호 중 하나 이상이 구체적일 때 candidate synthesis를 허용한다.

1. `PLANNED_MULTI_CONSUMER`: roadmap에 둘 이상의 실제 consumer가 예정됨.
2. `PREDICTED_REPEAT_COST`: 현재 설계대로 확장하면 같은 수작업/코드를 반복할 가능성이 높음.
3. `ONE_INPUT_MULTI_OUTPUT`: 같은 정보를 여러 surface에 반복 입력하고 있어 single structured flow로 줄일 수 있음.
4. `RESPONSIBILITY_TANGLE`: 한 owner가 독립적으로 변해야 할 책임을 함께 소유함.
5. `COMPOSITION_OPPORTUNITY`: 여러 기존 시스템을 작은 neutral primitive + thin adapter로 줄일 수 있음.
6. `CROSS_PROJECT_PLAN_PATTERN`: 구현은 없어도 여러 프로젝트의 승인 계획에서 같은 shape가 반복됨.
7. `USER_REUSE_INTENT`: 사용자가 장기 재사용/모듈화를 명시적으로 요구함.

단순히 “나중에 쓸 수도 있음”은 trigger가 아니다.

## 5. Context synthesis packet

```yaml
candidate_id:
origin: CONTEXT_SYNTHESIZED | HYBRID
context_basis:
planned_consumers: []
predicted_repeat_or_tangle:
why_now:
existing_solution_search:
proposed_contract:
expected_value:
likely_failure_modes: []
falsification_test:
smallest_pilot:
rollback_or_discard_condition:
maturity: HYPOTHESIS | MODULE_CONTRACT_DEFINED
validation: NOT_RUN
```

`falsification_test`와 `rollback_or_discard_condition`이 없으면 단순 아이디어 메모이며 reusable module candidate로 승격하지 않는다.

## 6. Existing Solution First remains mandatory

Context-driven 설계는 직접 구현 허가증이 아니다.

```text
context hypothesis
→ 프로젝트 내부 existing owner
→ Base/다른 프로젝트 existing module
→ 공식/오픈소스/허용 자산
→ adapter/composition 가능성
→ 그래도 gap이 남을 때 새 contract
```

새 contract가 기존 owner의 설정·adapter로 해결 가능하면 새 module/Skill/Tool을 만들지 않는다.

## 7. First HYBRID example: human-facing artifact synthesis

사용자가 제시한 `todayfreeai.com` presentation-AI 페이지는 현재 실행 환경에서 직접 본문 fetch가 되지 않았으므로 **그 페이지의 정확한 제품 목록을 읽었다고 주장하지 않는다**. 페이지는 discovery prompt로만 사용하고, presentation-AI의 반복 구조는 각 서비스의 공식 원출처에서 검증한다.

검증한 대표 원출처:

- Gamma Help Center / official product: Generate · Paste · Import, source material, outline-first creation, editable slides, export.
- Canva Help Center / official product: Magic Design, source/Brand input, on-brand generated drafts, editable design.
- Beautiful.ai official: outline/story shaping before design, Smart Slides auto-layout, brand controls, layout alternatives preserving content.
- Pitch official/help: prompt/files/template input, on-brand generation, AI chat refinement, deck interrogation for weak proof points and gaps, editable workspace.
- SlidesAI official/help: prompt/text/notes/document input, outline review before generation, editable Google Slides/PowerPoint/web outputs, staged generation and retry.

### Extracted provider-neutral contract

```text
INPUT_MODE_GENERATE
INPUT_MODE_STRUCTURE_EXISTING
INPUT_MODE_IMPORT
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

Evidence boundaries:

```text
IMPORTED_CONTENT_IS_NOT_IMPORTED_VISUAL_CANON
AI_DRAFT_IS_NOT_APPROVED_NARRATIVE
AUTO_LAYOUT_IS_NOT_DESIGN_QUALITY_PASS
BRAND_TEMPLATE_IS_NOT_PROJECT_CANON_BY_ITSELF
EXPORT_IS_DERIVATIVE_NOT_CANON
PROVIDER_USE_IS_OPTIONAL_NOT_BASE_DEPENDENCY
```

이 패턴은 `RM-WORK-003 HUMAN_FACING_ARTIFACT_SYNTHESIS` 후보로 기록한다. 새 presentation SaaS를 Base 기본 의존성으로 채택하지 않는다. 기존 `managing-design-documents`와 Notion/repository domain split을 침범하지 않으며, 실제 deck 생성 기능이 필요해질 때만 해당 owner가 consumer가 된다.

## 8. Registry integration

Registry는 origin/maturity/validation의 의미를 정의하고, 각 row의 기존 legacy status를 한 번에 전면 마이그레이션하지 않는다. 새/갱신 candidate가 세 축을 명시할 수 있게 하고, completed-main 직접 증거가 있는 P0 reference implementation은 stale `IMPLEMENTATION_NOT_BUILT`를 유지하지 않는다.

이번 정합화 대상:

- RM-TOOL-001
- RM-SYS-001
- RM-SYS-003
- RM-VIS-001
- RM-VIS-002
- RM-TOOL-003 (PR #580 merged main evidence 이후)

프로젝트별 adoption 상태는 별도 evidence owner가 책임하며 Registry가 추정하지 않는다.

## 9. Alternatives considered

### A. Evidence-only + exceptions
변경량은 작지만 사고가 계속 “사례를 먼저 찾는 것”에 종속된다. Reject.

### B. Dual-origin model (selected)
창의적 구조설계와 검증된 역공학을 모두 허용하고, 검증 ceiling을 분리할 수 있다. Adopt.

### C. Free-form architecture invention
창의성은 크지만 중복 module, YAGNI, false promotion 비용이 높다. Reject as default.

## 10. Validation

- focused contract tests must RED before production changes and GREEN after.
- whole core regression must pass.
- Evidence/appropriate workflow checks must pass if triggered.
- exact-head main freshness and open-PR path overlap must be rechecked before merge.
- five full adversarial improvement loops cover over-generalization, module explosion, evidence overclaim, source/provider lock-in, and concurrency/freshness.

## 11. Rollback

Documentation/contract changes are squash-revertable. No external SaaS installation, API key, paid plan, runtime dependency, project canon migration, or automatic project adoption is introduced.
