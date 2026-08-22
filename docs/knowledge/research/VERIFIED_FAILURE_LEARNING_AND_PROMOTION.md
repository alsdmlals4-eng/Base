# Verified Failure Learning & Promotion

## 목적

반복 작업에서 발견한 실패를 단순 회고나 기억으로 남기지 않고, **실제로 재현되고 수정이 검증된 실패만** 다음 작업의 예방 규칙 후보로 축적한다.

이 계약은 새 Debug Skill·자동수정 Agent·전역 Rule Engine을 만들기 위한 것이 아니다. Owner는 기존 `evolving-project-discipline-skills`의 `learn` 단계이며, 실제 수정·검증은 해당 도메인의 기존 owner/test/tool이 수행한다.

```text
VERIFIED_FAILURE_LEARNING
= observed failure
→ evidence-backed diagnosis
→ fix
→ same-scope re-verification
→ recurrence analysis
→ smallest existing-owner prevention candidate
→ negative-case validation
→ explicit promotion decision
```

## 외부 benchmark provenance

- 발견 원출처: `leigest519/OpenGame/agent-test/debug-skill`
- license 확인: repository root `LICENSE` = Apache-2.0.
- 흡수 방식: `PATTERN_NOT_PACKAGE_COPY`.
- 관찰한 유용한 원리: failure signature + root cause + verified fix를 축적하고, 반복 패턴을 proactive validation 후보로 전환한다.
- Base 보정: 같은 error code가 일정 횟수 반복됐다는 이유만으로 자동 일반화하지 않는다. 독립 재현성·scope·negative case·기존 owner·false-positive 비용을 추가 Gate로 요구한다.

외부 코드·고유 구현·prompt·명칭을 복제하지 않는다.

---

## 상태 머신

```text
OBSERVED_FAILURE
→ VERIFIED_FIX
→ RECURRENCE_CANDIDATE
→ PROACTIVE_CHECK_CANDIDATE
→ PROMOTED_RULE
```

### `OBSERVED_FAILURE`

실패 증상이 실제 build/test/runtime/CI/human evidence에서 관찰된 상태다. 검색 snippet, 모델 추측, 오래된 기억만으로 생성하지 않는다.

### `VERIFIED_FIX`

같은 scope에서 실패가 먼저 재현됐고 수정 후 동일 검증이 성공했다. `FIX_VERIFICATION_REQUIRED_BEFORE_LEARNING`.

수정 후 성공하지 않았거나 원인이 불명확하면 `UNVERIFIED_FIX`이며 재사용 지식으로 승격하지 않는다.

### `RECURRENCE_CANDIDATE`

유사한 원인과 예방 가능성이 독립적인 작업에서 다시 관찰된 상태다.

`SAME_RUN_RETRY_DOES_NOT_COUNT_AS_INDEPENDENT_EVIDENCE`.

한 실행에서 같은 실패를 여러 번 재시도한 횟수, 동일 branch에서 같은 증상을 반복 본 것, 동일 로그를 여러 agent가 다시 읽은 것은 독립 occurrence가 아니다.

### `PROACTIVE_CHECK_CANDIDATE`

실패 후 대응보다 실행 전 deterministic validation·bounded checklist·focused test가 더 저렴하고 정확하다고 검증할 가치가 생긴 상태다.

`NEGATIVE_CASE_REQUIRED_BEFORE_PROACTIVE_PROMOTION`.

정상 입력, 허용 예외, 다른 프로젝트 구조를 잘못 차단하지 않는지 negative case를 검증한다.

### `PROMOTED_RULE`

기존 owner에 실제 test/check/reference로 흡수되고 해당 owner의 validation 경로에 연결된 상태다. 문서에 문장을 추가한 것만으로 `PROMOTED_RULE`이라 하지 않는다.

`AUTOMATIC_SEMANTIC_PROMOTION_FORBIDDEN`.

LLM·generalizer·주기 automation은 후보를 만들 수 있지만 Base-wide semantic rule, ACTIVE Skill behavior, 보안/권한/제품 방향을 자동 승격하지 않는다. 기존 approval/BCP/owner gate를 따른다.

---

## Failure Learning Entry

```yaml
failure_learning_entry:
  entry_id:
  state: OBSERVED_FAILURE | VERIFIED_FIX | RECURRENCE_CANDIDATE | PROACTIVE_CHECK_CANDIDATE | PROMOTED_RULE
  owner_domain:
  failure_signature:
    stage: build | test | runtime | ci | integration | human_validation
    stable_error_code_or_category:
    normalized_message_or_symptom:
    affected_contract:
  exact_context:
    repository:
    project:
    commit_or_build:
    platform:
    tool_and_version:
    relevant_path_or_component:
  failing_evidence:
    command_or_reproduction:
    artifact_or_log_ref:
    observed_result:
  root_cause:
    evidence:
    confidence:
  verified_fix:
    smallest_change:
    owner:
    diff_or_commit_ref:
  verification_after_fix:
    same_failure_recheck:
    focused_regression:
    broader_regression_when_needed:
    result:
  independent_occurrences:
    count:
    refs: []
  distinct_projects_or_contexts:
    count:
    refs: []
  false_positive_risk:
  counterexample_or_non_applicability:
  proactive_check_candidate:
    check_kind: deterministic_test | static_validation | preflight | checklist | reference_only
    proposed_owner:
    estimated_cost:
    expected_prevention_value:
  prevented_occurrence_evidence:
    refs: []
  disposition:
    project_only | retain_candidate | promote_existing_owner | reject_overgeneralization
```

필수 원칙:

- `failure_signature`는 error string 전체를 맹목적으로 고정하지 않고 **재발을 식별하는 안정된 최소 특징**만 남긴다.
- `exact_context`를 제거해 모든 프로젝트에 적용되는 보편 문제처럼 만들지 않는다.
- `root_cause`는 증상과 분리한다. 한 증상에 여러 원인이 가능하면 서로 다른 entry로 유지한다.
- `verified_fix`는 “이 방법이 좋아 보인다”가 아니라 실제 failing evidence를 제거한 변경이어야 한다.
- `counterexample_or_non_applicability`가 비어 있으면 Base-wide promotion을 서두르지 않는다.

---

## 반복 증거 Gate

`CROSS_PROJECT_OR_INDEPENDENT_RECURRENCE_REQUIRED`.

공용 예방 규칙 후보는 기본적으로 다음 중 하나를 요구한다.

1. **서로 다른 2개 이상 프로젝트**에서 같은 underlying failure class가 독립적으로 검증됨.
2. 같은 프로젝트라도 서로 다른 subsystem/시점/변경에서 최소 3개의 독립 occurrence가 있고, 공통 root cause와 prevention interface가 동일함.
3. 한 번의 치명적 실패라도 보안·데이터 손실·릴리스 무결성처럼 반복을 기다리는 비용이 과도한 경우, 해당 기존 policy owner의 별도 high-impact Gate가 공용 예방을 승인함.

횟수는 증거 강도의 일부일 뿐 authority가 아니다. `occurrence_count >= N`만으로 승격하지 않는다.

`PROJECT_LOCAL_FIRST_WHEN_SCOPE_IS_NARROW`.

특정 프로젝트 schema·씬 구조·도구 버전에 묶인 실패는 프로젝트 local test/check로 먼저 해결한다. 공통 contract가 실제로 반복될 때만 Base candidate로 올린다.

---

## 예방 규칙 승격 Gate

```text
VERIFIED_FIX
→ independent recurrence
→ common root cause
→ EXISTING_OWNER_FIRST
→ prevention cheaper than repeated diagnosis
→ negative case
→ false-positive / maintenance cost
→ bounded implementation
→ focused regression
→ broader regression when applicable
→ explicit existing-owner promotion
```

`EXISTING_OWNER_FIRST`.

우선순위:

```text
기존 test 추가
→ 기존 validator/preflight 보강
→ 기존 Skill/reference의 narrow rule
→ project adapter/config
→ deterministic shared tool extension
→ 새 Tool/Skill (마지막 수단)
```

다음은 승격 근거가 아니다.

- 유명 프로젝트에서도 비슷한 오류가 있었다.
- 같은 로그가 한 세션에서 여러 번 나왔다.
- LLM이 원인이 같다고 판단했다.
- 수정 후 한 번 성공했다.
- 예방 check를 만들기 쉽다.
- “언젠가 유용할 것 같다.”

---

## Reactive → Proactive 전환

Reactive fix를 바로 전역 validator로 만들지 않는다.

```text
failure observed
→ verified fix
→ repeat evidence
→ deterministic predicate exists?
   YES → PROACTIVE_CHECK_CANDIDATE
   NO  → diagnostic reference / project-local knowledge 유지
```

좋은 proactive check는:

- 입력과 판정이 명확하다.
- false-positive가 낮다.
- 실제 오류보다 검사비용이 낮다.
- 정상 예외를 표현할 configuration이 있다.
- 실패 위치와 remediation hint를 반환한다.
- 자동 수정하지 않아도 예방 가치가 있다.

---

## PREVENTED_OCCURRENCE_EVIDENCE

예방 규칙의 가치는 “검사가 존재한다”가 아니라 이후 실제로 같은 failure class를 더 일찍 잡았는지로 평가한다.

```text
PREVENTED_OCCURRENCE_EVIDENCE
= proactive check가 실제 후속 작업에서 merge/build/runtime 이전에 같은 failure class를 탐지한 직접 evidence
```

`PROMOTED_RULE` 이후에도 다음을 추적할 수 있다.

- prevented occurrence
- false positive
- bypass/exception 증가
- maintenance cost
- stale tool/version assumption
- 더 작은 owner로 이동 가능한지

효과가 없거나 유지비가 더 크면 `REDUCE / PROJECT_ONLY / RETIRE` 후보로 되돌린다.

---

## Base Learning Log와의 관계

- `skills/SKILL_LEARNING_LOG.md`: 사람이 읽는 공용 학습 index와 중요한 판정 기록.
- 개별 Skill `LEARNING_LOG.md`: 해당 owner의 focused evidence/history.
- 이 문서의 failure entry: **승격 전 증거 구조**.
- 실제 test/validator/script: 예방 규칙의 실행 권위.

Learning Log에 적혔다는 사실은 실행 가능한 예방 규칙이 생겼다는 뜻이 아니다. 반대로 이미 deterministic test가 owner를 명확히 소유하면 같은 내용을 장문 Learning Log로 중복 복제하지 않는다.

## Evidence ceiling

```text
VERIFIED_FIX
!= GENERAL_RULE

RECURRENCE
!= SAME_ROOT_CAUSE_PROVEN

PROACTIVE_CHECK_PASS
!= RUNTIME_OR_HUMAN_PASS

PROMOTED_RULE
!= PERMANENT_RULE
```

새 버전·플랫폼·엔진·작업구조에서 전제가 깨지면 freshness audit 대상으로 되돌린다.
