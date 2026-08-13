# Claim and Intent Verification Gate — Design

- Date: 2026-08-13
- Proposal: `BCP-2026-027-claim-and-intent-verification-gate`
- Work Mode: `REVIEW`
- Owner: `reviewing-and-validating-project-changes`
- Integration: `ABSORB_BY_PROGRESSIVE_DISCLOSURE`

## 1. Problem

Base는 이미 계약 검토, 실제 diff 우선, 정적·런타임·회귀 검증, BCP-008 traceability, exact HEAD와 post-merge readback을 보유한다. 그러나 다음 실패를 하나의 완료 주장 Gate로 판정하는 재사용 계약이 없었다.

1. 검색 snippet이나 작업자 설명을 저장소 사실로 과승격한다.
2. 테스트 정의를 실행 결과로 오인한다.
3. 일부 구현 경로만 확인하고 모든 Acceptance를 충족했다고 보고한다.
4. stale branch의 PASS를 current candidate에 재사용한다.
5. merged 상태·merge SHA·main readback 없이 병합 완료를 주장한다.
6. 기술 PASS를 UX·재미·시장성 PASS로 승격한다.

PR #316의 교정은 실제 회귀다. PR #313 감사 문서의 README drift finding은 exact-SHA readback 없이 검색 관찰을 확정 사실로 승격했다. 별도 신규 Skill보다 기존 통합 검증 owner 안의 fail-closed 계약이 필요하다.

## 2. Goals

- material claim을 authority·freshness·counterevidence에 연결한다.
- 승인 Intent·Acceptance와 실제 diff·관찰 결과를 항목별로 연결한다.
- 구현·검증·의도·통합 완료 주장을 서로 다른 Evidence 계약으로 판정한다.
- exact HEAD와 post-merge main readback을 분리한다.
- 30 ACTIVE Skills와 `PLAN / BUILD / REVIEW`를 유지한다.
- 기존 owner와 기존 Registry trigger를 재사용한다.

## 3. Non-goals

- 모든 문장을 claim ledger에 기록하지 않는다.
- 새 ACTIVE Skill이나 네 번째 Work Mode를 만들지 않는다.
- 외부 Eval SaaS 또는 LLM judge를 필수화하지 않는다.
- 모델 자기평가를 진실 판정으로 사용하지 않는다.
- 정적 테스트로 UX·재미·시장성·법률 검토를 통과 처리하지 않는다.
- PR #312·#316 소유 경로를 수정하지 않는다.

## 4. Existing-solution-first decision

| 선택 | 장점 | 위험 | 판정 |
|---|---|---|---|
| 신규 ACTIVE Skill | 이름 발견성 | 기존 owner 중복, 컨텍스트·오라우팅 증가 | 제외 |
| Registry에 유사 trigger 추가 | 사용자 문구 노출 | 기존 `external-ai-result`, `contract-check`, `evidence-report`와 중복 | 보류 |
| 기존 owner 본문에 전체 절차 삽입 | 한 파일에서 보임 | 25KB 본문 팽창, 상세 계약 중복 | 제외 |
| 기존 validation Template에서 전용 reference로 progressive disclosure | 기존 route·산출물 재사용, 본문 크기 보존 | Template 소비 경로 검증 필요 | 채택 |

기존 Registry의 `external-ai-result`, `contract-check`, `evidence-report`는 이 요청을 기존 REVIEW owner로 보낼 수 있다. 실제 model-run 오라우팅이 반복 증거로 확인되기 전에는 유사 trigger를 추가하지 않는다.

## 5. Benchmark synthesis

외부 사례의 공통 구조를 Base에 맞게 변형한다.

- NIST GenAI Profile: confabulation·prompt 불일치·내부 모순을 위험으로 보고 사실·인용 확인, 적대 테스트, 지속 모니터링을 결합한다.
- NASA Requirements Verification Matrix: 요구사항 ID, 출처, 검증 방법, 결과를 연결한다.
- OpenAI SimpleQA: 긴 응답의 다수 주장을 한 번에 신뢰성 있게 채점하기 어려워 짧은 사실 질문과 `correct / incorrect / not attempted` 구분을 사용한다.
- Phoenix·LangSmith·Braintrust·Promptfoo: 고정 dataset·snapshot, deterministic evaluator, 보조 rubric/judge, CI 회귀와 production feedback 분리를 사용한다.
- Agent Skills·Superpowers: 좁은 trigger, progressive disclosure, 반례 기반 behavior eval, RED→GREEN→회귀를 강조한다.

Base 채택 결과:

```text
material claim 원자화
+ exact repository authority
+ deterministic-first evidence
+ requirement/intent traceability
+ explicit UNVERIFIED state
+ exact-head / post-merge split
```

## 6. Architecture

```text
reviewing-and-validating-project-changes
├─ existing Registry route: external-ai-result / contract-check / evidence-report
├─ existing SKILL.md: actual diff + external review + BCP-008 traceability
├─ templates/quality/PROJECT_CHANGE_VALIDATION.md
│  └─ references/claim-and-intent-verification.md
├─ evals/claim-and-intent-verification.json (SBE-038)
├─ LEARNING_LOG.md
└─ tests/test_claim_and_intent_verification_contract.py
```

The Gate owns three contracts.

### 6.1 `MATERIAL_CLAIM_LEDGER`

- Required: claim type, authority source, evidence locator, freshness, counterevidence, status.
- Status: `CLAIM_VERIFIED / CLAIM_CONTRADICTED / CLAIM_UNVERIFIED / NOT_APPLICABLE`.

### 6.2 `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`

- Required: approved intent, protected scope, implementation paths, observed behavior, verification evidence, evidence ceiling.
- Status: `INTENT_CONFORMANT / MINOR_TECHNICAL_DRIFT / PLANNING_CONFLICT / IMPLEMENTATION_UNVERIFIED`.

### 6.3 `COMPLETION_CLAIM_GATE`

Separate gates:

1. implementation complete
2. verification complete
3. intent-conformant behavior
4. integration/merge complete

A PASS in one gate cannot satisfy another.

## 7. Evidence hierarchy

```text
latest user approval
→ exact-SHA canonical repository content
→ exact-SHA static/test/runtime evidence
→ dated/versioned official external primary source
→ explicit inference
→ producer/model narrative
```

`producer/model narrative`는 검증 lead이며 단독 PASS 증거가 아니다.

## 8. Routing contract

Positive prompts:

- “외부 AI가 완료했다고 했는데 실제 diff와 exact HEAD 실행 증거가 맞는지 확인해.”
- “승인한 의도와 구현 결과가 항목별로 일치하는지 검증해.”
- “테스트·병합 완료 주장이 사실인지 main readback까지 확인해.”

Expected route:

```text
Work Mode: REVIEW
Primary Skill: reviewing-and-validating-project-changes
Existing triggers: external-ai-result + contract-check + evidence-report
Progressive disclosure: PROJECT_CHANGE_VALIDATION.md → claim-and-intent-verification.md
```

Do not use the full Gate for pure creative prose, L0 typo fixes, PLAN-only ideation, or isolated engine-crash root-cause diagnosis.

## 9. Failure behavior

- missing authority/freshness → `CLAIM_UNVERIFIED`
- direct contradiction → `CLAIM_CONTRADICTED`
- unmapped Acceptance or missing required evidence layer → `IMPLEMENTATION_UNVERIFIED`
- product/player meaning drift → `PLANNING_CONFLICT`
- missing merge SHA/readback → integration `BLOCKED_UNVERIFIED`

Fail-closed states are released only by the missing evidence.

## 10. TDD and evaluation

### RED

A dedicated test was written first. The first run exposed a separate test-discovery gap: the new test file was not in the explicit workflow list. The test was connected to the existing docs·contract aggregator before production changes.

- initial test commit: `9a4a6e688e993114466e3f25831555b23fcf5912`
- canonical RED head: `8a161eca8d129584aecb3898e8d5622dcfc89efb`
- run: `31656590653`
- job: `94312314139`
- result: 113 tests; the six new Gate contracts failed while existing listed contracts passed before them

### Behavior fixture

`SBE-038` requires exact-ref readback, actual diff, exact-head execution evidence, explicit unverified states, and post-merge main readback. It rejects search snippet or producer narrative as sole evidence.

## 11. Compatibility and rollback

Compatibility:

- no Skill ID, Work Mode, existing Registry entry, or existing SKILL.md mode is renamed.
- the existing validation Template remains at the same path and gains optional sections.
- external tools remain optional.

Rollback:

1. revert PR #317 squash commit.
2. remove reference, eval, design, plan, and regression.
3. restore the validation Template.
4. restore the owner Learning Log entry.
5. restore the proposal lifecycle state if closeout was included.

## 12. Acceptance criteria

- [ ] existing owner routes through existing Registry triggers.
- [ ] validation Template links the dedicated reference.
- [ ] reference defines the three fail-closed contracts.
- [ ] active Skill count remains 30 and Work Modes remain three.
- [ ] `SBE-038` and executable regression run in canonical CI.
- [ ] exact-head repository workflows pass.
- [ ] independent adversarial review has no blocker.
- [ ] expected-head merge and post-merge main readback are verified.
