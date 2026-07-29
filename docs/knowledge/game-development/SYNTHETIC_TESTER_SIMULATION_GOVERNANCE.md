# Synthetic Tester Simulation Governance

## 1. 목적

이 문서는 실제 참가자를 모집할 수 없을 때 AI가 여러 플레이어 관점을 가정하여 설계 결함·모순·악용 가능성·정보 누락을 공격하는 `SYNTHETIC_TESTER_SIMULATION`의 공용 계약이다.

합성 테스터는 사람의 행동을 관찰한 것이 아니다. 결과는 항상 `T6_AI_INFERENCE`이며 구현 전 적대적 설계 검토와 후속 테스트 설계에만 사용한다.

```yaml
validation_method: SYNTHETIC_TESTER_SIMULATION
evidence_tier: T6_AI_INFERENCE
human_validation: NOT_RUN
ai_simulation: COMPLETED
implementation_authority: NONE
assumption_not_observation: true
```

## 2. 핵심 경계

합성 시뮬레이션으로 주장할 수 있는 것은 다음뿐이다.

- 문서·규칙·정보 위계에서 예상 가능한 오해.
- 하나의 선택이 사실상 지배 전략이 될 가능성.
- 실패 원인·책임 계층·복구 경로의 모순.
- 악용·메타 공략·찍기·최적화 축소 가능성.
- 상충하는 가정과 심각도 높은 반례.
- 실제 Prototype·사람 검증에서 확인할 우선 질문.

다음은 주장할 수 없다.

```yaml
claims_not_allowed:
  - actual_player_behavior
  - actual_fun
  - actual_preference
  - actual_usability
  - actual_performance
  - actual_accessibility
  - actual_retention
  - actual_conversion
  - actual_touch_accuracy
  - actual_rng_feel
  - actual_algorithm_accuracy
```

다음 상태를 합성 결과에 사용하지 않는다.

- `ADOPT`
- `VALIDATED`
- `HUMAN_TEST_PASSED`
- `PLAYTEST_PASSED`
- `CORE_LOOP_PROVEN`
- `PRODUCTION_APPROVED`

## 3. 적용 전 프로젝트 구조 분석

합성 페르소나를 만들기 전에 대상 프로젝트의 현행 운영 구조를 복원한다. 모든 실행 패킷은 다음을 기록한다.

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
  protected_paths: []
  validation_routes: []
  document_router:
  existing_human_session_packet:
  prohibited_authority_changes: []
```

### 필수 분석 순서

1. 최신 사용자 지시와 저장소 `main`을 확인한다.
2. `AGENTS.md`, `START_HERE`, Active/Current Status를 읽는다.
3. Documentation Map과 Design Document Registry에서 질문별 책임 원본을 찾는다.
4. `current_skill_registry`에서 trigger·mode·owner를 확인한다.
5. 실제 사용할 `selected_project_skills`와 `selected_base_skills`를 최소 집합으로 고른다.
6. 제품 정본·실제 코드·데이터·Scene·테스트를 `canonical_sources`와 구분한다.
7. 변경 금지 경로를 `protected_paths`로 기록한다.
8. 자동·수동·사람·플랫폼 검증을 `validation_routes`로 분리한다.
9. 기존 사람 세션 패킷이 있으면 그 claim ceiling과 시나리오를 읽는다.
10. 구조 분석이 완료되기 전에는 `simulation_report`를 작성하지 않는다.

저장소마다 Skill 구조가 다르면 Base 문서를 복사해 동일 라우터를 강제하지 않는다. 프로젝트 Registry와 현재 책임 원본이 실행 책임을 결정한다.

## 4. Skill 라우팅 원칙

새 합성 테스터 전용 광역 Skill을 만들지 않는다. 기존 책임을 조합한다.

- 연구 가설·페르소나·편향: 프로젝트 분석·유저리서치 Skill 또는 `governing-game-user-research-coverage`.
- 게임 규칙·플레이어 선택: 프로젝트 게임 디자인 Skill.
- UI 정보 위계: 프로젝트 UX·접근성 Skill.
- 사건·서사 공정성: 프로젝트 내러티브 또는 사건 작성 Skill.
- 적대적 공격: `running-adversarial-review-and-refinement`.
- 변경·증거·미검증 판정: 프로젝트 QA와 `reviewing-and-validating-project-changes`.
- 정본·상태 라우팅: `managing-design-documents`, `auditing-canonical-reference-freshness`, 프로젝트 Documentation Map.

실제 사람 관찰만을 권한으로 가진 Skill의 `PASS`, `PROVEN`, `LOOP_PROVEN` 상태를 합성 결과로 채우지 않는다. 그 Skill의 세션 계약은 공격 대상·후속 테스트 질문을 만드는 입력으로만 사용한다.

## 5. 페르소나 구성

모든 프로젝트에 같은 이름만 복사하지 않는다. 코어 결정과 실패 표면에 맞춰 5~8개 페르소나를 고른다.

공통 후보:

- 장르 초보자: 용어·목표·인과를 처음 본다.
- 장르 숙련자: 전략 깊이와 기존 장르 관습을 적용한다.
- 성급한 플레이어: 설명을 건너뛰고 가장 눈에 띄는 행동을 선택한다.
- 최적화 플레이어: 기대값·지배 전략·반복 효율로 시스템을 축소한다.
- 적대적 플레이어: 찍기·세이브 반복·메타 정보·진행자 문구를 악용한다.
- 실패 회피형: 손실·후회·불확실성을 과도하게 회피한다.
- 수집·서사형: 이름·관계·기록·소유 의미를 우선한다.
- 낮은 작업기억/접근성 위험 관점: 정보량·색상 의존·가림·입력 부담을 공격한다.

각 페르소나는 실제 인구 통계 대표가 아니라 특정 실패 가설을 공격하기 위한 분석 렌즈다.

## 6. 페르소나 기록 계약

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

- `assumed_first_attempt`는 실제 행동 로그처럼 서술하지 않는다.
- `reasoning_basis`는 정본 문구·상태·규칙·UI 계약에서 추적 가능해야 한다.
- `confidence`는 사람 반응 확률이 아니라 추론 근거의 직접성이다.
- 반드시 자기 결론을 깨는 `counterexample`을 하나 이상 기록한다.
- 동일 페르소나의 모든 답을 일관된 서사로 억지 정렬하지 않는다.

## 7. 시뮬레이션 실행 순서

```text
프로젝트 구조 분석
→ 결정 질문·claim ceiling 고정
→ 시나리오와 보호 경계 복원
→ 페르소나별 first attempt 가정
→ 지배 전략·정답 누출·복구 실패 공격
→ 반대 페르소나·반례 생성
→ 기존 사람 세션 패킷의 측정 가능성 공격
→ Finding 중복 제거
→ 적대적 검토
→ 프로젝트별 최소 수정 또는 TEST 게이트
```

실제 결과 카드·알고리즘·RNG·터치·시간을 실행하지 않았다면 임의의 성공률·평균 시간·선호 비율을 만들지 않는다.

## 8. Finding 분류

| 상태 | 의미 |
|---|---|
| `MUST_FIX_BEFORE_TEST` | 사람/Prototype 테스트 전에도 문서·자극물·책임 분리 결함이 명확함 |
| `SHOULD_ADAPT` | 방향은 유지하되 오해·편향·정보 위계를 교정해야 함 |
| `COUNTEREXAMPLE` | 현재 권장안을 깨는 가능한 행동·해석 |
| `TEST_REQUIRED` | 실제 Build·사람·기기·알고리즘 없이는 판정 불가 |
| `REJECT_ASSUMPTION` | 근거 없는 가정 또는 프로젝트 정본과 충돌 |
| `STOP` | 기준선·정본·시나리오가 불일치하여 분석을 계속할 수 없음 |

## 9. 최종 판정

합성 시뮬레이션의 최종 판정은 다음만 허용한다.

```text
PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP
```

- `PROMISING_DIRECTION`: 문서상 큰 모순은 없고 다음 fidelity 검증 가치가 있음. 실제 선호·재미 성공을 뜻하지 않는다.
- `ADAPT`: 코어 방향은 유지하되 테스트 자극물·정보 위계·복구·설명 책임을 수정한다.
- `REWORK`: 현재 시나리오가 결정 질문을 분리해 측정하지 못한다.
- `REJECT`: 제안 방향이 프로젝트 코어와 명백히 충돌하거나 지배 전략을 강화한다.
- `TEST`: 실제 사람·Build·기기·RNG·알고리즘 없이는 더 나아갈 수 없다.
- `STOP`: 정본 충돌이나 입력 결함으로 분석 무효.

`PROMISING_DIRECTION`도 T6 추론일 뿐이다. 프로젝트 정본이나 제품 승인으로 자동 승격하지 않는다.

## 10. 합성 보고서 계약

`simulation_report`는 다음을 포함한다.

```yaml
simulation_report:
  simulation_id:
  validation_method: SYNTHETIC_TESTER_SIMULATION
  evidence_tier: T6_AI_INFERENCE
  baseline:
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

실제 사람 세션이 불가능한 경우 `human_followup_status: NOT_RUN`을 유지하면서 다음 중 하나로 연결한다.

- 문서·자극물의 명백한 결함 수정.
- 저비용 클릭 Mock 또는 규칙 fixture 제작 제안.
- 자동 계약 테스트로 검증 가능한 규칙 분리.
- 실제 Build 단계에서 확인할 `TEST_REQUIRED` 목록 보존.

## 11. 금지

- 가상의 6명 중 5명이 성공했다고 수치를 만들어 기록.
- AI 페르소나 응답을 인터뷰 인용문처럼 작성.
- 페르소나 수를 표본 수로 취급.
- 실제 사람 검증 문서의 `human_validation`을 변경.
- 실제 재미·선호·가독성·조작감·접근성·성능을 통과 처리.
- simulated recognition을 알고리즘 정확도로 해석.
- fixed RNG 결과를 실제 운 체감이나 밸런스로 해석.
- 프로젝트 Skill·정본·작업 게이트를 읽지 않고 공통 페르소나 문서를 복사.
- 합성 결과만으로 제품 코드·데이터·Scene·밸런스 변경을 승인.

## 12. 완료 조건

- 프로젝트별 구조 분석이 먼저 존재한다.
- Skill·mode·정본·보호 경로·검증 경로가 프로젝트 현재 상태와 일치한다.
- 모든 가상 행동은 `assumption_not_observation`으로 표시된다.
- 주장 불가 항목과 실제 사람 미검증 상태가 남아 있다.
- 적대적 반례가 포함된다.
- 결과가 다음 문서 수정 또는 `TEST_REQUIRED` 항목으로 연결된다.
- 합성 결과와 실제 사람·자동·런타임 증거가 서로 다른 상태로 보존된다.
