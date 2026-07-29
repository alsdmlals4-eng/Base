# Synthetic Tester Simulation Packet

> 이 Template은 실제 사람 플레이를 대체하지 않는다. 모든 결과는 `T6_AI_INFERENCE`이며 실제 사람 검증은 `NOT_RUN`으로 유지한다.

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

### 구조 분석 메모

- 현재 책임 원본:
- 기존 Skill과 Base Skill의 책임 경계:
- 합성 시뮬레이션을 기록할 문서 위치:
- 현재 상태 문서에 연결할 방식:
- 실제 사람 검증 상태를 보존하는 방식:

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

| persona_id | 분석 렌즈 | 공격할 실패 가설 | 실제 사용자 대표 주장 여부 |
|---|---|---|---|
| `NOVICE` | 장르 초보 | 용어·목표·인과 오해 | 아니오 |
| `EXPERT` | 장르 숙련 | 깊이 부족·장르 관습 충돌 | 아니오 |
| `IMPATIENT` | 설명 건너뜀 | 정보 위계·발견 실패 | 아니오 |
| `OPTIMIZER` | 기대값·지배 전략 | 서사·선택 축소 | 아니오 |
| `ADVERSARIAL` | 악용·메타 공략 | 찍기·우회·후견 편향 | 아니오 |
| `RISK_AVERSE` | 손실 회피 | 위험 과장·결정 회피 | 아니오 |
| `COLLECTOR` | 소유·서사 | 수치 외 가치 부재 | 아니오 |
| `LOW_WORKING_MEMORY` | 정보량·접근성 위험 | 과밀·가림·기억 부담 | 아니오 |

프로젝트에 맞지 않는 페르소나는 제거하고 필요한 렌즈를 추가한다.

## 6. 페르소나별 시나리오 기록

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

각 가정은 실제 클릭·발언·시간 기록처럼 표현하지 않는다.

## 7. 교차 공격

### 지배 전략

- 단서·서사·정보를 무시해도 항상 우세한 행동이 있는가?
- 실패 비용을 없애는 반복·취소·저장 악용이 가능한가?
- 한 선택이 표현상 또는 기대값상 사실상 정답인가?

### 정답 누출

- 문구·아이콘·상태가 정확 행동을 직접 알려주는가?
- 진행자 또는 결과 카드가 원하는 사고법을 먼저 가르치는가?
- 피드백 이후 결과를 최초 이해처럼 오인할 수 있는가?

### 책임 혼합

- 입력 실패와 설계 실패가 한 시나리오에 섞였는가?
- 규칙 문제와 UI 문제를 구분할 수 있는가?
- 실제 결과와 scripted/fixed 결과가 혼합되는가?

### 정보 위계

- 중요한 정보가 텍스트 양·장식·확률·보상에 묻히는가?
- 초보와 숙련자 모두 같은 잘못된 단축 해석에 도달하는가?
- `미해결`, 불확실성, 잔여 RNG가 실패로 읽히는가?

### 복구와 복기

- 무엇을 되돌리고 무엇을 유지하는지 알 수 있는가?
- 실패 이유와 다음 수정안을 구체적으로 연결할 수 있는가?
- 전체 재시작만 유일한 복구인가?

## 8. Finding 원장

| finding_id | 상태 | 근거 | 영향 | 반례 | 최소 조치 | 실제 검증 필요 |
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

- [ ] 프로젝트 현재 `main`과 기준 commit을 기록했다.
- [ ] `current_skill_registry`와 선택 Skill·mode를 기록했다.
- [ ] `canonical_sources`, `protected_paths`, `validation_routes`를 기록했다.
- [ ] 기존 사람 세션 패킷의 claim ceiling을 보존했다.
- [ ] 모든 페르소나 결과에 `assumption_not_observation: true`가 있다.
- [ ] 실제 성공률·선호율·시간 평균을 만들지 않았다.
- [ ] 반대 근거와 `counterexample`이 있다.
- [ ] `PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP` 중 하나로 판정했다.
- [ ] `human_validation: NOT_RUN`을 유지했다.
- [ ] 제품 변경 권한을 생성하지 않았다.
