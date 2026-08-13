# BCP-2026-027 — Claim and Intent Verification Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 관찰 기준 Base 커밋: `453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- 제출일: `2026-08-13`
- Registry 상태: `IMPLEMENTED`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/317`
- 지식 상태: `PATTERN_CANDIDATE`
- 사용자 구현 승인 증거: 2026-08-13 ChatGPT 세션에서 할루시네이션 방지, 승인 의도대로 구현됐는지 확인하는 공용 절차, 작업 구조 반영과 검증 후 병합을 명시적으로 요청했다.

## 관찰과 증거

Base에는 이미 다음 책임이 있었다.

- `reviewing-and-validating-project-changes`: 실제 파일·diff·실행 결과 우선, 외부 AI 산출물 독립 검수, 정적·런타임·회귀·Evidence 보고
- `FEATURE_SPEC_TRACEABILITY_PACKET`: Requirement→Acceptance→Task→implementation path→verification evidence 연결
- `running-adversarial-review-and-refinement`: 공격→비판 검증→승인된 최소 개선→회귀 재검사
- Evidence ceiling, exact HEAD, untouched consumer, post-merge main readback

그러나 다음 질문을 한 번에 닫는 재사용 Gate가 없었다.

1. AI·Agent·작업자의 사실·완료 주장에 직접 Evidence가 있는가?
2. 승인한 WHAT/WHY·Acceptance가 실제 diff·관찰 동작에 연결되는가?
3. 테스트 정의가 아니라 해당 exact HEAD에서 검증이 실행됐는가?
4. 병합 주장이 merge SHA와 새 main readback까지 확인됐는가?

### 실제 회귀

PR #313 감사 문서는 `README.md`가 활성 Skill 수를 하드코딩한다는 검색 관찰을 exact-SHA file readback 없이 verified finding으로 과승격했다. PR #316은 baseline·merged main·관련 PR의 exact-SHA readback으로 이 finding을 `INVALIDATED_FINDING`으로 교정했다.

따라서 다음 반례를 공용 회귀로 채택했다.

```text
검색 결과·snippet·작업자 설명
+ exact-ref file readback 없음
→ CLAIM_UNVERIFIED
→ 정본·감사 finding·완료 보고로 승격 금지
```

### 외부 1차 출처·현업 비교

- NIST AI 600-1: confabulation, prompt 불일치, 응답 내부 모순, 사실·인용 확인, 적대 테스트와 지속 모니터링
- NASA Requirements Verification Matrix: 요구사항 ID·출처·검증 방법·결과 연결
- OpenAI SimpleQA: 긴 completion의 다수 주장 대신 짧은 사실 질문과 `correct / incorrect / not attempted` 구분
- Phoenix·LangSmith·Braintrust·Promptfoo: 고정 dataset·snapshot, deterministic evaluator, 보조 rubric/judge, CI 회귀와 production feedback 분리
- Agent Skills·Superpowers: 좁은 trigger, progressive disclosure, 반례 기반 behavior eval, RED→GREEN→회귀

참조 URL은 구현 Design에 보존한다.

### Existing Solution First — 최종 disposition

초기안은 기존 owner에 Mode·reference·Registry metadata·Template·중앙 eval을 모두 삽입하는 방식이었다. 구현 전 적대적 재검토에서 다음 중복이 확인됐다.

- Registry는 이미 `external-ai-result`, `contract-check`, `evidence-report`로 같은 owner를 route한다.
- review Skill 본문은 이미 실제 diff 우선, 외부 독립 검수, BCP-008 traceability, fail-closed Evidence를 소유한다.
- 전체 절차를 25KB Skill 본문에 다시 넣으면 progressive disclosure 원칙을 위반하고 컨텍스트 비용을 늘린다.

최종 판정은 `ABSORB_BY_PROGRESSIVE_DISCLOSURE`다.

```text
existing Registry triggers
→ REVIEW
→ reviewing-and-validating-project-changes
→ PROJECT_CHANGE_VALIDATION.md
→ references/claim-and-intent-verification.md
```

| 선택 | 최종 판정 |
|---|---|
| 31번째 ACTIVE Skill | 제외 — owner 중복 |
| 네 번째 Work Mode | 제외 |
| 유사 Registry trigger 추가 | 보류 — 실제 model-run 오라우팅 반복 증거가 생길 때 재검토 |
| 25KB SKILL.md 전체 절차 삽입 | 제외 — 본문 팽창·중복 |
| 기존 Template→전용 reference | 채택 |
| 외부 Eval SaaS 필수화 | 제외 — 선택적 보조 도구로만 허용 |

## 일반화 후보

### `MATERIAL_CLAIM_LEDGER`

```yaml
claim_id:
claim_type: REPOSITORY_FACT | EXTERNAL_FACT | INFERENCE | IMPLEMENTATION | VERIFICATION | INTEGRATION
claim_text:
authority_source:
evidence_locator:
freshness:
  observed_at:
  branch_or_version:
  commit_sha:
counterevidence:
status: CLAIM_VERIFIED | CLAIM_CONTRADICTED | CLAIM_UNVERIFIED | NOT_APPLICABLE
```

### `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`

```yaml
intent_id:
approved_intent_or_acceptance:
protected_and_excluded_scope:
implementation_paths:
observed_behavior:
verification_evidence:
evidence_ceiling:
drift_status: INTENT_CONFORMANT | MINOR_TECHNICAL_DRIFT | PLANNING_CONFLICT | IMPLEMENTATION_UNVERIFIED
```

### `COMPLETION_CLAIM_GATE`

| 주장 | 최소 Evidence |
|---|---|
| 구현 완료 | 실제 diff + 요구사항별 implementation path + 범위 밖 변경 부재 |
| 테스트·검증 완료 | 실행 명령·환경·exact HEAD·결과·실패·skip 수 |
| 의도대로 동작 | Acceptance별 관찰 결과 + 필요한 Evidence level |
| 병합 완료 | merged PR + merge SHA + post-merge main readback + post-merge 검사 |

필수 Evidence가 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`, `BLOCKED_UNVERIFIED`를 유지한다.

## 적용 조건과 비사용 조건

적용:

- L1 이상 AI·Agent 완료 보고
- 저장소 사실·외부 사실·현재 버전 주장
- 승인 의도와 실제 구현의 일치 판정
- 테스트·검증·병합 완료 주장
- L2 이상 복합 변경의 traceability 검증

비사용·경량화:

- L0 오탈자·동일 입력 재검사
- 사실·정본·완료 상태를 주장하지 않는 순수 창작
- 프로젝트 정본 전체를 ledger에 복제하는 작업
- 외부 SaaS·LLM judge를 필수화하는 설계

프로젝트 전용:

- 플레이어 경험·UX·수치·세계관·Acceptance
- 실제 Godot scene·script·data·asset path
- 프로젝트별 테스트 명령·플랫폼·device 조건
- 선택한 외부 Eval 도구와 dataset

## 반례와 위험

| 공격 | 차단 방식 |
|---|---|
| 모든 문장 원장화 | material claim만 기록, L0 경량화 |
| URL은 있으나 stale·충돌 | 날짜·버전·exact SHA·counterevidence 요구 |
| 테스트 파일을 실행 결과로 오인 | 명령·환경·HEAD·결과 요구 |
| Builder 자기확증 | 생산자 설명은 lead, 독립 Evidence 아님 |
| LLM judge 환각 | deterministic-first, judge는 보조 |
| 테스트 PASS로 UX·재미 과장 | Evidence ceiling 적용 |
| 병합 직전 main 이동 | exact-head/current-main/post-merge readback 분리 |
| 새 Skill·trigger 과증식 | 기존 owner·trigger 재사용 |
| 새 test 파일이 CI에서 미실행 | canonical aggregator 연결과 실행 회귀 |

## 영향 범위와 검증

### 구현 경로

- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `skills/reviewing-and-validating-project-changes/evals/claim-and-intent-verification.json`
- `skills/reviewing-and-validating-project-changes/LEARNING_LOG.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `tests/test_claim_and_intent_verification_contract.py`
- `tests/test_repository_governance_baseline.py`
- `docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md`
- `docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md`
- 이 제안서와 `PROPOSAL_REGISTRY.json`

### 보호 경로

- `skills/SKILL_REGISTRY.json`과 generated active Skill map
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- Work Mode 구조
- PR #312·#316 소유 경로
- CI workflow 구조

### TDD 증거

- initial test commit: `9a4a6e688e993114466e3f25831555b23fcf5912`
- canonical RED head: `8a161eca8d129584aecb3898e8d5622dcfc89efb`
- run: `31656590653`
- docs-validation job: `94312314139`
- 결과: 113 tests에서 기존 목록 계약 통과 후 새 Gate 계약 6개만 예상대로 실패

첫 run이 통과한 이유는 기능이 이미 있어서가 아니라 새 테스트 파일이 explicit workflow 목록에 없었기 때문이다. 기존 docs·contract suite가 실행하는 aggregator에 전용 test case를 연결해 거짓 GREEN을 제거했다.

### 완료 검증 계약

- exact PR head의 두 repository workflow 성공
- dedicated six-test contract 실행 확인
- active Skill count 30, Work Mode 3 유지
- Registry·generated active map·SKILL.md 보호 확인
- 독립 적대 검토 blocker 0
- expected-head merge
- merge SHA와 새 main readback
- post-merge required workflow 성공

## 승인과 구현

- 사용자 승인: 2026-08-13 현재 세션의 구현·검증·병합 요청
- 제안 PR: `https://github.com/alsdmlals4-eng/Base/pull/315`
- 제안 merge SHA: `a96864a84ac2513e488f20cba304c252dea3045d`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/317`
- 구현 상태: `IMPLEMENTED` record를 구현 PR에 포함했다. 최종 완료 주장은 PR #317 exact-head workflow, expected-head merge, merge SHA, post-merge main readback과 post-merge workflow가 모두 확인된 뒤 보고한다.
- 롤백: PR #317 squash commit을 revert하고 validation Template·owner Learning Log를 복구하며 신규 reference·eval·design·plan·test를 제거한다.
