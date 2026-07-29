# Synthetic Tester Simulation Governance

## 1. 목적과 상태

`SYNTHETIC_TESTER_SIMULATION`은 실제 참가자를 모집할 수 없을 때 AI가 여러 플레이어 관점을 가정하여 설계 결함·모순·지배 전략·악용 가능성을 공격하는 사전 검토다.

```yaml
validation_method: SYNTHETIC_TESTER_SIMULATION
evidence_tier: T6_AI_INFERENCE
human_validation: NOT_RUN
ai_simulation: COMPLETED
implementation_authority: NONE
assumption_not_observation: true
```

합성 결과는 실제 사람 관찰이 아니며 프로젝트 정본이나 제품 승인으로 자동 승격하지 않는다.

## 2. 주장 상한

주장 가능:

- 문서·규칙·정보 위계에서 예상 가능한 오해.
- 지배 전략·찍기·반복·메타 공략 가능성.
- 실패 책임·복구 경로·설명 순서의 모순.
- 기존 테스트 자극물이 측정 질문을 분리하지 못하는 문제.
- 실제 Prototype·사람·기기 검증에서 우선 확인할 위험.

```yaml
claims_not_allowed:
  - actual_player_behavior
  - actual_fun
  - actual_preference
  - actual_usability
  - actual_performance
  - actual_accessibility
  - actual_retention
  - actual_algorithm_accuracy
```

합성 결과에는 `ADOPT`, `VALIDATED`, `HUMAN_TEST_PASSED`, `PLAYTEST_PASSED`, `CORE_LOOP_PROVEN`, `PRODUCTION_APPROVED`를 사용하지 않는다.

## 3. 프로젝트 구조 분석 선행

모든 프로젝트에서 `structure_analysis`를 먼저 작성한다.

```yaml
structure_analysis:
  repository:
  baseline_branch:
  baseline_commit:
  work_mode:
  execution_profile:
  current_skill_registry:
  selected_project_skills: []
  selected_base_skills: []
  canonical_sources: []
  current_status_sources: []
  document_router:
  protected_paths: []
  validation_routes: []
  existing_human_session_packet:
  prohibited_authority_changes: []
```

분석 순서:

1. 최신 사용자 지시와 저장소 `main`을 확인한다.
2. `AGENTS.md`, `START_HERE`, Active/Current Status를 읽는다.
3. Documentation Map·Registry에서 책임 원본을 찾는다.
4. `current_skill_registry`의 trigger·mode·owner를 확인한다.
5. 실제 사용할 `selected_project_skills`와 `selected_base_skills`를 최소 집합으로 고른다.
6. `canonical_sources`, `current_status_sources`, `protected_paths`를 분리한다.
7. 자동·런타임·사람·플랫폼 검증을 `validation_routes`로 기록한다.
8. 기존 사람 검증 패킷과 claim ceiling을 읽는다.
9. 구조 분석 전에는 `simulation_report`를 작성하지 않는다.

프로젝트마다 구조가 다르면 Base 문서를 복제하여 동일 라우터를 강제하지 않는다.

## 4. Skill 라우팅

새 합성 테스터 전용 광역 Skill을 만들지 않는다.

- 연구 가설·편향: 프로젝트 분석·유저리서치 Skill 또는 `governing-game-user-research-coverage`.
- 규칙·선택: 프로젝트 게임 디자인 Skill.
- 정보 위계: 프로젝트 UX·접근성 Skill.
- 사건 공정성: 프로젝트 내러티브·사건 작성 Skill.
- 공격·반례: `running-adversarial-review-and-refinement`.
- 증거·미검증 판정: 프로젝트 QA와 `reviewing-and-validating-project-changes`.
- 정본 라우팅: 프로젝트 Documentation Map과 `auditing-canonical-reference-freshness`.

실제 사람 관찰만을 권한으로 가진 Skill의 `PASS`, `PROVEN`, `LOOP_PROVEN` 상태를 합성 결과로 채우지 않는다.

## 5. 페르소나

프로젝트의 코어와 실패 표면에 맞춰 5~8개 분석 렌즈를 선택한다.

- 장르 초보자: 용어·목표·인과 오해.
- 장르 숙련자: 깊이·장르 관습 충돌.
- 성급한 플레이어: 설명 건너뜀·발견 실패.
- 최적화 플레이어: 기대값·지배 전략으로 축소.
- 적대적 플레이어: 찍기·메타 정보·우회 악용.
- 실패 회피형: 손실·불확실성 과잉 회피.
- 수집·서사형: 이름·관계·기록의 가치 확인.
- 낮은 작업기억 관점: 과밀·가림·기억 부담 공격.

페르소나는 실제 사용자 집단의 통계적 대표가 아니다.

## 6. 기록 계약

```yaml
persona_id:
persona_lens:
scenario_id:
assumed_first_attempt: []
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

`confidence`는 사용자 행동 확률이 아니라 추론 근거의 직접성이다. 모든 결론에는 `counterexample`을 둔다.

## 7. 실행 순서

```text
프로젝트 구조 분석
→ 결정 질문·claim ceiling 고정
→ 기존 시나리오·보호 경계 복원
→ 페르소나별 assumed first attempt
→ 지배 전략·정답 누출·책임 혼합 공격
→ 반대 페르소나·반례 생성
→ 적대적 검토
→ 문서 수정 또는 TEST 게이트
```

실제 결과를 실행하지 않았다면 성공률·평균 시간·선호 비율을 만들지 않는다.

## 8. Finding과 판정

Finding 상태:

- `MUST_FIX_BEFORE_TEST`
- `SHOULD_ADAPT`
- `COUNTEREXAMPLE`
- `TEST_REQUIRED`
- `REJECT_ASSUMPTION`
- `STOP`

최종 판정:

```text
PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP
```

- `PROMISING_DIRECTION`: 다음 fidelity 검증 가치가 있음.
- `ADAPT`: 방향은 유지하되 정보·자극물·복구를 수정.
- `REWORK`: 시나리오가 결정 질문을 분리하지 못함.
- `REJECT`: 코어 충돌 또는 지배 전략 강화.
- `TEST`: 실제 사람·Build·기기·RNG·알고리즘이 필요.
- `STOP`: 정본·입력 불일치로 분석 무효.

## 9. 보고서 계약

```yaml
simulation_report:
  simulation_id:
  validation_method: SYNTHETIC_TESTER_SIMULATION
  evidence_tier: T6_AI_INFERENCE
  structure_analysis:
  decision_question:
  personas: []
  scenarios: []
  findings: []
  adversarial_review:
  decision: PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP
  claims_not_allowed: []
  human_validation: NOT_RUN
  human_followup_status: NOT_RUN
  implementation_authority: NONE
  canon_changed: false
```

## 10. 금지와 완료

금지:

- 가상의 참가자 성공 수치 생성.
- AI 응답을 실제 인터뷰 인용문처럼 작성.
- 페르소나 수를 표본 수로 취급.
- 실제 사람 검증 상태 변경.
- 실제 재미·선호·가독성·조작감·접근성·성능 통과 처리.
- fixed RNG·simulated recognition을 실제 성능으로 해석.
- 프로젝트 Skill·정본을 읽지 않고 공통 보고서 복사.
- 합성 결과만으로 제품 코드·데이터·Scene·밸런스 변경 승인.

완료:

- 프로젝트별 구조 분석이 존재한다.
- Skill·mode·정본·보호·검증 경로가 현재 상태와 일치한다.
- 가상 행동은 `assumption_not_observation`으로 표시된다.
- 반례와 `TEST_REQUIRED`가 보존된다.
- `human_validation: NOT_RUN`과 `implementation_authority: NONE`이 유지된다.
