# 게임 벤치마크·플레이어 근거·개선안

> 비교 게임의 표면 기능을 복제하지 않고, 현재 결정 질문과 Evidence ID·원출처·플레이어 행동·자기보고·실패 사례·Case Card를 연결한다. 더 넓은 분야 횡단 조사는 `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`를 사용한다.

## 메타데이터

```yaml
research_id:
project:
baseline_commit:
created_at:
updated_at:
owner:
related_evidence_pack:
status: DRAFT | IN_RESEARCH | READY_FOR_DECISION | DECIDED | VALIDATED | SUPERSEDED
```

## 결정 질문

- 현재 결정:
- 현재 가설:
- 결정을 바꿀 근거:
- 보호할 프로젝트 코어:
- 대상 플레이어·플랫폼·지역·언어:
- 조사 기간·버전:
- 비교 차원:
- 조사 제외:
- 성공·실패·중단 조건:

## CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY

중요한 L1+ 결정은 하나의 해법을 먼저 정한 뒤 벤치마크를 근거로 붙이지 않는다. 현재 상태와 기존 해법을 먼저 확인한 뒤 **`MINIMUM_VIABLE_ALTERNATIVES: 3`**의 materially distinct 실질 대안을 만든다. 숫자를 채우기 위한 허수 대안은 금지한다.

| 대안 | 접근 방식 | 플레이어 가치 | 정확성·근거 | 제작·유지 비용 | AI Context 비용 | 충돌·위험 | Rollback | 검증 가능성 | 장기 확장성 | 관련 Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 현행 유지·현행 해법 재사용 | | | | | | | | | |
| B | 최소 수정·흡수 | | | | | | | | | |
| C | 책임 경계 재구성·다른 실행 경로 | | | | | | | | | |
| D+ | 조사에서 발견한 더 나은 대안 | | | | | | | | | |

- 유효 대안 수:
- 3개 미만이면 추가 조사·추상화가 필요한 이유:
- 임시 권장안:
- 탈락안과 탈락 이유:
- 핵심 trade-off:

### BETTER_ALTERNATIVE_SEARCH

임시 권장안을 선택한 뒤에도 새 Evidence·실패·플레이테스트·적대적 검토 finding이 나오면 더 나은 대안이 생겼는지 다시 탐색한다.

```yaml
better_alternative_search:
  new_candidates_considered: []
  stronger_option_found: false
  selected_option_after_recheck:
  replacement_reason:
```

### LONG_TERM_PLAN_FIT_REQUIRED

단기 구현량만이 아니라 플레이어 가치, 정확성·기획 충실도, 위험, 수명주기 비용, 유지보수성, rollback, 재사용·모듈성, 증거 강도와 현재 비용 경계를 비교한다.

```yaml
long_term_fit:
  player_value:
  design_fidelity:
  maintenance_and_lifecycle_cost:
  rollback_difficulty:
  reuse_and_modularity:
  evidence_strength:
  current_cost_boundary:
revisit_condition:
```

## 비교 대상

| 대상 | 유형 | 비교 차원 | 버전·기간 | 선정 이유 | Case Card |
|---|---|---|---|---|---|
|  | 직접 경쟁/인접 장르/실패 사례/혼합 사례/비게임 참고 |  |  |  | `templates/research/GAME_DEVELOPMENT_CASE_CARD.md` |

성공 사례만 선택하지 않고 최소한 실패 사례 또는 혼합 반응 사례를 함께 검토한다.

## Evidence 체계

근거 층:

- `T1_PRIMARY_OFFICIAL`
- `T2_PROFESSIONAL_PRACTICE`
- `T3_PLAYER_BEHAVIOR`
- `T4_PLAYER_SELF_REPORT`
- `T5_SYNTHESIS`
- `T6_AI_INFERENCE`

근거 상태:

- `VERIFIED_SOURCE`
- `PARTIALLY_VERIFIED`
- `CONTEXT_LIMITED`
- `STALE_RECHECK_REQUIRED`
- `CONFLICTING_EVIDENCE`
- `UNVERIFIED`

| Evidence ID | 대상 | 원출처 | 게시일·버전 | 확인일 | 근거 층 | 근거 상태 | 확인된 사실 | 사용 한계 |
|---|---|---|---|---|---|---|---|---|
| EVD-001 |  |  |  |  |  |  |  |  |

`T6_AI_INFERENCE`는 원출처와 실제 프로젝트 증거 없이 공식 사실로 승격하지 않는다.

## 제품 사실

| 대상 | 실제 규칙·흐름 | Evidence ID | 공식 근거 | 우리와 같은 점 | 다른 점 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

제품 사실, 개발자 의도, 플레이어 반응과 분석자의 해석을 같은 칸에 합치지 않는다.

## 현업·개발자 사례

| 대상 | 해결하려던 문제 | 접근 방식 | 관찰된 결과 | 적용 조건 | 실패·비복제 요소 | Evidence ID |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 플레이어 반응 클러스터

| 클러스터 | 상황·트리거 | 긍정·부정·혼합 | 플레이어 맥락 | 빈도 신호 | 영향 | Evidence ID | 신뢰도 |
|---|---|---|---|---|---|---|---|
|  |  |  | 플랫폼·언어·플레이타임·패치 |  |  |  | HIGH/MEDIUM/LOW |

플레이어 자기보고는 실제 행동과 분리한다.

## 기대와 실제 경험

| 약속·기대 | 실제 플레이어 행동 | 플레이어 자기보고 | 일치 여부 | 원인 가설 | Evidence ID | 추가 검증 |
|---|---|---|---|---|---|---|
|  |  |  | MATCH/GAP/UNKNOWN |  |  |  |

## 행동·퍼널 근거

| 이벤트·단계 | 대상 집단 | 통과·이탈·시간 | 빌드·버전 | Evidence ID | 해석 한계 | 개선 후보 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

퍼널은 무엇이 일어났는지를 보여 주지만 감정과 원인을 자동으로 증명하지 않는다.

## 실패 사례·혼합 사례

### 실패 사례

| 대상·Case Card | 실패한 약속·흐름 | 관찰 결과 | 원인 가설 | 우리 프로젝트가 피할 요소 | 추가 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 혼합 사례

| 대상·Case Card | 잘된 부분 | 나빠진 부분 | 조건별 차이 | ADAPT 후보 | 추가 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 상충 근거

| 충돌 ID | Evidence A | Evidence B | 충돌 내용 | 조건 차이 | 현재 해석 | 추가 검증 |
|---|---|---|---|---|---|---|
| CONFLICT-001 |  |  |  |  |  |  |

신뢰 가능한 근거가 충돌하면 하나를 숨기지 않고 `CONFLICTING_EVIDENCE`로 유지한다.

## 플레이테스트·실험 계약

```yaml
hypothesis:
decision_if_supported:
decision_if_refuted:
build_and_version:
tester_segment:
prior_exposure:
recruitment_and_access:
tasks_or_play_window:
observation_points:
feedback_questions:
feedback_channel:
telemetry_events:
funnel_steps:
control_and_variants:
primary_metric:
guardrail_metrics:
accessibility_checks:
performance_budget:
success_failure_stop:
bias_and_validity_risks:
```

## 개선 판정

판정:

- `ADOPT`
- `ADAPT`
- `TEST`
- `AVOID`
- `IGNORE`
- `REFERENCE_ONLY`

| 발견 | 핵심 컨셉 정렬 | 플레이어 가치 | 제작 비용·위험 | 접근성·성능 | Evidence ID | 판정 | 변경 후보 | 검증 |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | ADOPT/ADAPT/TEST/AVOID/IGNORE/REFERENCE_ONLY |  |  |

`REFERENCE_ONLY`는 현재 적용하지 않지만 실패·반례·역사·향후 비교를 위해 보존할 때 사용한다.

## 편향·한계

- 표본 편향:
- 리뷰 폭탄·오프토픽:
- 버전·패치 차이:
- 플랫폼·지역·언어 차이:
- 플레이타임·숙련도 차이:
- 행동과 자기보고 불일치:
- 개발자·마케팅 이해관계:
- 성공 사례 선택 편향:
- 확인하지 못한 원출처:
- AI 추론·환각 위험:
- 현재 프로젝트와 다른 제작 규모:

## Case Card 연결

| Case Card | 분류 | 공용 원리 | 적용 조건 | 그대로 복제하지 않을 요소 | 프로젝트 판정 |
|---|---|---|---|---|---|
|  | SUCCESS/FAILURE/MIXED |  |  |  |  |

Case Card Template: `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`

## 최종 반영

- 유지:
- 강화:
- 수정:
- 제거:
- `ADOPT`:
- `ADAPT`:
- `TEST`:
- `AVOID`:
- `IGNORE`:
- `REFERENCE_ONLY`:
- 별도 PoC·Vertical Slice·A/B·Concept Test:
- 기획서·Issue·Plan·Project Sheet 갱신:
- 실제 코드·데이터·자산 영향:
- 미검증·재검증 조건:
- Base 승격 후보:
- 프로젝트 전용 유지:
