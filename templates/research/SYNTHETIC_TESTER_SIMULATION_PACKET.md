# Synthetic Tester Simulation Packet

> 실제 사람 플레이를 대체하지 않는다. 모든 결과는 `T6_AI_INFERENCE`이며 사람 검증은 `NOT_RUN`으로 유지한다.

## 1. 상태

```yaml
simulation_id:
project:
repository:
baseline_branch: main
baseline_commit:
validation_method: SYNTHETIC_TESTER_SIMULATION
evidence_tier: T6_AI_INFERENCE
ai_simulation: COMPLETED
human_validation: NOT_RUN
human_followup_status: NOT_RUN
implementation_authority: NONE
canon_changed: false
assumption_not_observation: true
```

## 2. 프로젝트 구조 분석

```yaml
structure_analysis:
  work_mode:
  execution_profile:
  current_skill_registry:
  selected_project_skills:
    - skill_id:
      mode:
      reason:
  selected_base_skills:
    - skill_id:
      mode:
      reason:
  canonical_sources: []
  current_status_sources: []
  document_router:
  existing_human_session_packet:
  protected_paths: []
  validation_routes:
    static:
    automated:
    runtime:
    human:
    platform:
  prohibited_authority_changes: []
```

- 현재 책임 원본:
- 기존 Skill과 Base Skill의 책임 경계:
- 합성 보고서 저장 위치:
- 현재 상태 문서 연결 방식:
- 실제 사람 검증 상태 보존 방식:

## 3. 결정 질문과 주장 상한

```yaml
decision_question:
claim_ceiling:
  can_claim:
    - 예상 가능한 오해·모순·지배 전략·복구 결함
    - 실제 검증에서 확인할 우선 위험
  cannot_claim:
    - actual_player_behavior
    - actual_fun
    - actual_preference
    - actual_usability
    - actual_performance
    - actual_accessibility
    - actual_retention
    - actual_algorithm_accuracy
claims_not_allowed:
  - ADOPT
  - VALIDATED
  - HUMAN_TEST_PASSED
  - PLAYTEST_PASSED
  - CORE_LOOP_PROVEN
  - PRODUCTION_APPROVED
```

## 4. 분석 대상

```yaml
existing_artifact:
artifact_fidelity:
simulated_components: []
scripted_components: []
fixed_outcomes: []
scenario_ids: []
canonical_rules_used: []
known_unverified_assumptions: []
```

## 5. 합성 페르소나

| persona_id | 분석 렌즈 | 공격할 실패 가설 |
|---|---|---|
| `NOVICE` | 장르 초보 | 용어·목표·인과 오해 |
| `EXPERT` | 장르 숙련 | 깊이 부족·관습 충돌 |
| `IMPATIENT` | 설명 건너뜀 | 정보 위계·발견 실패 |
| `OPTIMIZER` | 기대값·지배 전략 | 선택·서사 축소 |
| `ADVERSARIAL` | 악용·메타 공략 | 찍기·우회·편향 |
| `RISK_AVERSE` | 손실 회피 | 위험 과장·결정 회피 |
| `COLLECTOR` | 소유·서사 | 수치 외 가치 부재 |
| `LOW_WORKING_MEMORY` | 정보량 위험 | 과밀·가림·기억 부담 |

프로젝트에 맞지 않는 렌즈는 제거하고 필요한 렌즈를 추가한다.

## 6. 페르소나별 기록

```yaml
- persona_id:
  scenario_id:
  assumed_first_attempt:
    -
  assumed_reasoning:
  reasoning_basis:
    - canonical_rule_or_copy:
    - genre_convention:
    - information_hierarchy:
  confidence: LOW | MEDIUM | HIGH
  counterexample:
  adversarial_question:
  critical_risk:
  assumption_not_observation: true
```

## 7. 교차 공격

### 지배 전략

- 단서·서사·정보를 무시해도 항상 우세한 행동이 있는가?
- 한 선택이 표현상 또는 기대값상 사실상 정답인가?
- 반복·취소·저장으로 실패 비용을 제거할 수 있는가?

### 정답 누출과 편향

- 문구·아이콘·상태가 정확 행동을 직접 알려주는가?
- 결과 카드·진행자 문구가 원하는 사고법을 먼저 가르치는가?
- 피드백 이후 결과를 최초 이해처럼 기록할 위험이 있는가?

### 책임 혼합

- 입력 실패와 설계 실패가 섞였는가?
- 규칙 문제와 UI 문제를 구분하는가?
- 실제 결과와 scripted/fixed 결과가 혼합되는가?

### 정보·복구

- 핵심 정보가 텍스트·장식·보상에 묻히는가?
- 불확실성·미해결·잔여 RNG를 실패로 읽는가?
- 무엇을 되돌리고 무엇을 유지하는지 알 수 있는가?
- 전체 재시작만 유일한 복구인가?

## 8. Finding 원장

| finding_id | 상태 | 근거 | 영향 | counterexample | 최소 조치 | 실제 검증 필요 |
|---|---|---|---|---|---|---|
|  | `MUST_FIX_BEFORE_TEST` |  |  |  |  |  |
|  | `SHOULD_ADAPT` |  |  |  |  |  |
|  | `COUNTEREXAMPLE` |  |  |  |  |  |
|  | `TEST_REQUIRED` |  |  |  |  |  |
|  | `REJECT_ASSUMPTION` |  |  |  |  |  |

## 9. 적대적 검토

```yaml
adversarial_review:
  strongest_case_for_current_direction:
  strongest_case_against_current_direction:
  hidden_assumption:
  dominant_strategy_risk:
  facilitator_or_copy_bias:
  fidelity_confound:
  canon_conflict_check:
  product_path_intrusion_check:
  adversarial_question:
  verdict:
```

## 10. 판정

```yaml
decision: PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP
reason:
changes_allowed_now:
  - 문서·자극물·질문·시나리오 교정
changes_not_authorized:
  - 제품 코드
  - 게임 데이터
  - Scene·Resource
  - 밸런스 확정
  - 정본 승격
human_validation: NOT_RUN
human_followup_status: NOT_RUN
next_gate:
```

## 11. 실행 보고

```yaml
simulation_report:
  simulation_id:
  validation_method: SYNTHETIC_TESTER_SIMULATION
  evidence_tier: T6_AI_INFERENCE
  structure_analysis:
  personas_used: []
  scenarios_reviewed: []
  findings: []
  decision:
  claims_not_allowed: []
  assumption_not_observation: true
  human_validation: NOT_RUN
  human_followup_status: NOT_RUN
  implementation_authority: NONE
  canon_changed: false
```

## 12. 완료 체크

- [ ] 현재 `main`과 기준 commit을 기록했다.
- [ ] `current_skill_registry`, `selected_project_skills`, `selected_base_skills`를 기록했다.
- [ ] `canonical_sources`, `protected_paths`, `validation_routes`를 기록했다.
- [ ] 기존 사람 세션 claim ceiling을 보존했다.
- [ ] 모든 가상 결과에 `assumption_not_observation: true`가 있다.
- [ ] 성공률·선호율·시간 평균을 만들지 않았다.
- [ ] 반대 근거와 `counterexample`이 있다.
- [ ] `PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP` 중 하나로 판정했다.
- [ ] `human_validation: NOT_RUN`을 유지했다.
- [ ] 제품 변경 권한을 생성하지 않았다.
