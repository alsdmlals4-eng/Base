# Human Validation Session Packet

```yaml
session_packet_id:
project:
decision_question:
baseline_repository:
baseline_branch: main
baseline_commit:
created_at:
work_mode: PLAN
artifact_status: READY_FOR_PREPARATION
human_validation: NOT_RUN
implementation_authority: NONE
```

> 이 Template은 사람 세션을 계획·기록하기 위한 공용 형식이다. 실제 세션을 실행하지 않은 상태에서 결과·통과·제품 검증을 작성하지 않는다.

## 1. 책임 원본과 보호 경계

```yaml
project_canonical_sources: []
actual_implementation_sources: []
protected_files_or_systems: []
allowed_research_changes: []
forbidden_product_changes: []
```

## 2. Artifact fidelity와 주장 상한

```yaml
artifact_fidelity: PAPER | CARD | CLICKABLE_MOCK | EXISTING_POC_OVERLAY | PRODUCT_BUILD
simulated_components: []
scripted_components: []
fixed_outcomes: []
claim_ceiling:
  can_claim: []
  cannot_claim: []
```

각 simulated·scripted 요소는 다음 형식으로 기록한다.

```yaml
component_id:
component_status: SIMULATED_COMPONENT | SCRIPTED_OUTCOME | FIXED_STIMULUS
measures: UX_RESPONSIBILITY | COMPREHENSION | ATTRIBUTION | RECOVERY_DISCOVERY
not_measured: []
```

## 3. 가설과 반례

```yaml
hypothesis:
expected_behavior:
competing_explanation:
critical_counterexample:
stop_conditions: []
```

정답률이나 선택률만으로 가설을 정의하지 않는다. 무엇을 보고, 무엇을 말하고, 무엇을 수정하는지 행동으로 작성한다.

## 4. 참가자 구성

```yaml
pilot_purpose: DIRECTIONAL_FINDING | DEFECT_DISCOVERY | COMPREHENSION_CHECK
minimum_participants:
segments: []
recruitment_limits: []
order_or_condition_assignment: []
session_minutes:
```

- 모든 프로젝트에 같은 표본 수를 강제하지 않는다.
- 작은 표본에서는 통계적 유의성이나 모집단 일반화를 주장하지 않는다.
- 분자/분모와 경험군별 실제 개수를 기록한다.

## 5. 자극물 목록

| Artifact ID | 참가자에게 보이는 내용 | 숨겨진 진행자 정보 | fidelity | 최종 제품 정본 여부 |
|---|---|---|---|---|
| | | | | `NO` |

모든 연구 전용 글자·역할·카피·확률·결과에는 `RESEARCH_ONLY`, `SIMULATED`, `SCRIPTED` 중 맞는 상태를 표시한다.

## 6. 시나리오 카드

### Scenario 1

```yaml
scenario_id:
starting_state:
participant_information: []
participant_task:
simulated_or_scripted_result:
alternate_result_if_counterbalanced:
expected_observation:
critical_failure:
```

필요한 만큼 시나리오를 추가한다. 같은 구조에 유리·불리 결과를 교차 배정해야 하는 경우 `alternate_result_if_counterbalanced`를 사용한다.

## 7. 진행자 스크립트

### 시작 안내

> 이 테스트의 목적, 정답이 아니라는 점, 진행자가 추천하지 않는다는 점을 프로젝트 문맥에 맞게 한 문단으로 작성한다.

### 고정 순서

1. 기준 상태를 보여준다.
2. 참가자의 `first_attempt`를 기록한다.
3. 필요한 경우 결과·후보·피드백을 공개한다.
4. 정확한 `facilitator_intervention`을 기록한다.
5. 참가자의 `post_feedback_attempt`를 기록한다.
6. 사후 자기보고를 질문한다.

### 금지

- 정답·추천·가치 판단을 암시하지 않는다.
- 첫 시도를 기록하기 전에 교정하지 않는다.
- 동일 세션 중 자극물 문구를 수정하지 않는다.
- 참가자의 문장을 진행자가 대신 완성하지 않는다.

## 8. 관찰 기록지

한 참가자·시나리오당 한 행을 사용한다.

| 필드 | 기록 규칙 |
|---|---|
| `participant_id` | 개인정보 없는 코드 |
| `segment` | 사전 정의 경험군 |
| `condition_or_order` | 배정 조건·순서 |
| `scenario_id` | 고정 ID |
| `first_attempt` | 힌트·피드백 전 행동·선택·설명 |
| `post_feedback_attempt` | 피드백 뒤 수정 행동·설명 |
| `behavior_observation` | 실제 클릭·말·시간·되돌리기 |
| `player_self_report` | 감정·이유·선호·기억 |
| `facilitator_intervention` | 안내·재질문·교정·결과 공개 |
| `system_or_artifact_log` | 실제 로그 또는 scripted 카드 ID |
| `observer_interpretation` | 원자료와 분리한 분석 |
| `critical_incident` | 심각도 높은 단일 반례 |
| `privacy_redaction` | 삭제·일반화한 개인정보 여부 |

프로젝트별 수치 필드는 아래에 추가한다.

| 프로젝트 필드 | 정의 | 단위·범위 |
|---|---|---|
| | | |

## 9. 작은 표본 요약

### 실제 개수

| 관찰 패턴 | 전체 n/N | 세그먼트별 n/N | 대표 원자료 | 반례 |
|---|---:|---:|---|---|
| | | | | |

### 반복 결함

| Finding ID | 결함 | 반복 참가자 수 | 심각도 | Artifact 문제 / 제품 문제 / 미분리 | 다음 조치 |
|---|---|---:|---|---|---|
| | | | | | |

### 진행자 영향

| 개입 | 발생 횟수 | 첫 시도에 미친 영향 | 결과 해석 제한 |
|---|---:|---|---|
| | | | |

## 10. 판정

판정 순서:

1. `STOP` 조건.
2. 핵심 질문 측정 가능 여부.
3. 심각도 높은 반례.
4. 두 명 이상 반복된 결함.
5. 경험군 차이.
6. 행동·자기보고·진행자 개입의 일치·충돌.
7. 수치 요약.
8. claim ceiling.

```yaml
verdict: PROMISING_DIRECTION | ADAPT | REWORK | REJECT | STOP
supporting_patterns: []
blocking_findings: []
counterexamples: []
claim:
claims_not_allowed: []
next_fidelity_gate:
```

`ADOPT`는 이 작은 표본 세션 패킷의 기본 판정이 아니다. 실제 제품 또는 목표 fidelity Build에서 반복 증거와 프로젝트 승인 게이트를 통과한 후 별도 결정 문서에서만 사용한다.

## 11. 미실행 검증

```yaml
not_run:
  product_runtime:
  target_device:
  accessibility:
  performance:
  algorithm_accuracy:
  long_term_balance:
  external_sample:
```

## 12. 증거 저장 계약

```yaml
raw_data_location:
report_path:
repository_commit:
artifact_version:
personal_data_stored: false
recording_consent_required: false
```

- 이름·연락처·계정·음성 파일 경로를 기본 원자료에 저장하지 않는다.
- 보고서는 실제 세션 뒤 별도 PR로 생성한다.
- 제품 코드·정본 변경은 보고서 판정과 사용자 승인 뒤 별도 작업으로 분리한다.

## 13. 실행 체크

### 기준선

- [ ] 실행 commit·Artifact 버전을 기록했다.
- [ ] 연구 카드와 실제 정본·데이터가 일치한다.
- [ ] 불일치 시 `STOP`한다.

### 패킷

- [ ] 모든 simulated·scripted 요소에 상태가 표시됐다.
- [ ] claim ceiling이 작성됐다.
- [ ] 참가자 자극물과 진행자 키가 분리됐다.
- [ ] 첫 시도와 피드백 후 시도 필드가 분리됐다.

### 세션

- [ ] 행동·자기보고·진행자 개입을 별도 기록한다.
- [ ] 유리한 결과 하나만으로 방향을 증명하지 않는다.
- [ ] 세션 중 자극물을 수정하지 않는다.

### 판정

- [ ] 작은 표본 비율만으로 `ADOPT`하지 않는다.
- [ ] 반복 결함·반례·경험군 차이를 함께 기록한다.
- [ ] 저충실도 Artifact 결과를 실제 제품 성능으로 확대하지 않는다.
- [ ] 실행하지 않은 항목은 `NOT_RUN`으로 유지한다.
