# Claim and Intent Verification Gate — Design

- Date: 2026-08-13
- Proposal: `BCP-2026-027-claim-and-intent-verification-gate`
- Work Mode: `REVIEW`
- Owner: `reviewing-and-validating-project-changes`
- Integration choice: `ABSORB`

## 1. Problem

Base는 이미 계약 검토, 실제 diff 우선, reference freshness, 정적·런타임·접근성·성능·회귀 검증, exact HEAD와 post-merge readback을 보유한다. 그러나 이 규칙이 분산돼 있어 다음 실패가 하나의 차단 Gate로 닫히지 않았다.

1. 검색 snippet이나 작업자 설명을 저장소 사실로 과승격한다.
2. 테스트 정의를 실행 결과로 오인한다.
3. 일부 구현 경로만 확인하고 모든 Acceptance를 충족했다고 보고한다.
4. stale branch의 PASS를 current candidate에 재사용한다.
5. merged 상태·merge SHA·main readback 없이 병합 완료를 주장한다.
6. 기술 PASS를 UX·재미·시장성 PASS로 승격한다.

PR #316의 교정은 실제 회귀를 제공한다. PR #313 감사 문서의 README drift finding은 exact-SHA readback 없이 검색 관찰을 확정 사실로 승격해 잘못 기록됐다. 이 사례는 별도 신규 Skill보다 기존 통합 검증 owner 내부의 fail-closed claim gate가 필요함을 보여 준다.

## 2. Goals

- material claim을 authority·freshness·counterevidence에 연결한다.
- 승인 Intent·Acceptance와 실제 diff·관찰 결과를 항목별로 연결한다.
- 구현·검증·의도·통합 완료 주장을 서로 다른 Evidence 계약으로 판정한다.
- exact HEAD와 post-merge main readback을 분리해 stale evidence를 막는다.
- 사용자 표현인 완료 주장, 승인 의도, 실제 diff, 할루시네이션 감사를 기존 REVIEW owner로 좁게 라우팅한다.
- 30 ACTIVE Skills와 `PLAN / BUILD / REVIEW`를 유지한다.

## 3. Non-goals

- 모든 문장을 claim ledger에 기록하지 않는다.
- 새 광역 ACTIVE Skill이나 네 번째 Work Mode를 만들지 않는다.
- 외부 Eval SaaS 또는 LLM judge를 필수화하지 않는다.
- 모델의 자기평가를 진실 판정으로 사용하지 않는다.
- 정적 테스트로 실제 UX·재미·시장성·법률 검토를 통과 처리하지 않는다.
- PR #312의 Figma·시각 도구 경로나 PR #316의 교정 경로를 수정하지 않는다.

## 4. Existing Solution First

| 선택 | 장점 | 위험 | 판정 |
|---|---|---|---|
| 신규 ACTIVE Skill | 이름 발견성 | 기존 review owner와 중복, 라우팅·컨텍스트 비용 증가 | 제외 |
| 기존 owner에 Mode·reference·trigger·template·eval 흡수 | 입력·출력·Evidence·회귀 구조 재사용 | 파생본·소비자 갱신 필요 | 채택 |
| 문서만 추가하고 Registry 불변 | 작은 diff | 실제 자동 라우팅 경로가 약함 | 제외 |
| 외부 Eval 플랫폼 의무화 | 대시보드·dataset 관리 | 공급자 종속, 비용·보안·설정 부담 | 제외 |

## 5. Benchmark synthesis

외부 사례의 공통 패턴을 Base 문맥으로 변형한다.

- NIST GenAI Profile: confabulation·prompt 불일치·내부 모순을 위험으로 보고 사실·인용 확인, 적대 테스트, 지속 모니터링을 결합한다.
- NASA Requirements Verification Matrix: 요구사항 ID, 출처, 검증 방법, 결과를 연결한다.
- OpenAI SimpleQA: 긴 응답의 다수 주장을 한 번에 신뢰성 있게 채점하기 어려워 짧은 사실 질문과 `correct / incorrect / not attempted` 구분을 사용한다.
- Phoenix, LangSmith, Braintrust, Promptfoo: 고정 dataset·snapshot, deterministic evaluator, 보조 rubric/judge, CI 회귀와 production feedback 분리를 사용한다.
- Agent Skills·Superpowers 계열: 좁은 trigger, progressive disclosure, 반례 기반 behavior eval, RED→GREEN→회귀를 강조한다.

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
├─ existing modes
├─ claim-and-intent-verification
│  └─ references/claim-and-intent-verification.md
├─ templates/quality/PROJECT_CHANGE_VALIDATION.md
├─ skills/SKILL_REGISTRY.json routing metadata
├─ skills/SKILL_BEHAVIOR_EVALS.json SBE-038
└─ tests/test_claim_and_intent_verification_contract.py
```

The new Mode owns three contracts.

### 6.1 `MATERIAL_CLAIM_LEDGER`

- Scope: decision-, implementation-, verification-, integration-changing claims only.
- Required: claim type, authority source, evidence locator, freshness, counterevidence, status.
- Status: `CLAIM_VERIFIED / CLAIM_CONTRADICTED / CLAIM_UNVERIFIED / NOT_APPLICABLE`.

### 6.2 `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`

- Scope: each approved Intent or Acceptance.
- Required: protected scope, implementation paths, observed behavior, verification evidence, evidence ceiling.
- Status: `INTENT_CONFORMANT / MINOR_TECHNICAL_DRIFT / PLANNING_CONFLICT / IMPLEMENTATION_UNVERIFIED`.

### 6.3 `COMPLETION_CLAIM_GATE`

Separate gates:

1. implementation complete
2. verification complete
3. intent-conformant behavior
4. integration/merge complete

A PASS in one gate cannot satisfy another.

## 7. Routing

Primary owner remains `reviewing-and-validating-project-changes` in `REVIEW`.

Narrow trigger additions:

- `completion-claim`
- `claim-evidence`
- `intent-conformance`
- `hallucination-audit`

Positive examples:

- “AI가 완료했다고 했는데 실제 diff와 exact HEAD 실행 증거가 맞는지 확인해.”
- “승인한 의도와 구현 결과가 항목별로 일치하는지 검증해.”
- “테스트·병합 완료 주장이 사실인지 main readback까지 확인해.”

Negative examples:

- 순수 창작 문장 개선
- L0 오탈자 수정
- 구현 전 아이디어 발산만 수행하는 PLAN 요청
- 엔진 크래시의 원인 격리만 필요한 런타임 디버깅

## 8. Evidence hierarchy

```text
latest user approval
→ exact-SHA canonical repository content
→ exact-SHA static/test/runtime evidence
→ dated/versioned official external primary source
→ explicit inference
→ producer/model narrative
```

`producer/model narrative`는 검증 lead이며 단독 PASS 증거가 아니다.

## 9. Failure behavior

- missing authority/freshness → `CLAIM_UNVERIFIED`
- direct contradiction → `CLAIM_CONTRADICTED`
- unmapped Acceptance or missing runtime layer → `IMPLEMENTATION_UNVERIFIED`
- product/player meaning drift → `PLANNING_CONFLICT`
- missing merge SHA/readback → integration `BLOCKED_UNVERIFIED`

Fail-closed 상태는 증거가 채워질 때만 해제한다.

## 10. TDD and evaluation

### RED

`tests/test_claim_and_intent_verification_contract.py`를 먼저 추가하고, 기존 CI가 새 파일을 실행하지 않는 문제를 발견했다. 이미 docs·contract suite에서 실행되는 `tests/test_repository_governance_baseline.py`에 전용 test case를 import해 canonical suites에 연결했다.

Exact RED head `8a161eca8d129584aecb3898e8d5622dcfc89efb`의 docs-validation은 기존 계약을 통과한 뒤 새 Gate 계약 6개만 실패했다.

### GREEN target

- reference, design, plan, Skill mode, routing, template, operating docs, behavior eval, learning record가 모두 존재한다.
- 30 ACTIVE Skills 유지.
- SBE ID는 기존 `SBE-015` 충돌을 피한 `SBE-038`.
- full exact-head workflows pass.

### Behavior eval

`SBE-038`은 검색 결과 또는 생산자 설명만 있는 저장소 사실을 PASS로 승격하지 않고, exact-ref readback·실제 diff·실행 증거·미검증 표시·post-merge main readback을 요구해야 한다.

## 11. Compatibility and rollback

Compatibility:

- 기존 Skill ID·Work Mode·Template path 유지.
- 신규 field는 Markdown contract이며 기존 소비자가 무시해도 동작한다.
- 기존 review modes는 삭제·이름 변경하지 않는다.

Rollback:

1. PR #319의 squash commit을 revert한다.
2. 신규 reference·design·plan·test·eval을 제거한다.
3. 기존 owner의 mode/trigger/template/docs additions를 되돌린다.
4. Registry 파생본을 generator로 재생성한다.
5. BCP-2026-027 상태를 `SUBMITTED` 또는 별도 withdrawn 기록으로 복구한다.

## 12. Acceptance criteria

- [ ] 기존 review owner가 `claim-and-intent-verification` Mode를 명시한다.
- [ ] 전용 reference에 세 계약과 fail-closed 상태가 있다.
- [ ] Registry는 30 ACTIVE Skills를 유지하면서 네 trigger와 좁은 use_when을 제공한다.
- [ ] validation template과 REVIEW 운영 문서가 Gate를 노출한다.
- [ ] `SBE-038`과 전용 regression이 canonical CI에서 실행된다.
- [ ] exact HEAD의 두 repository workflows가 성공한다.
- [ ] 독립 적대 검토에서 blocker가 없다.
- [ ] expected-head merge 뒤 merge SHA와 새 main readback을 확인한다.
