# 튜토리얼·온보딩 설계 Contract

```yaml
project:
work_mode: PLAN
owner_skill: analyzing-and-refining-game-concepts
owner_mode: tutorial-and-onboarding-design
status: DRAFT | REVIEW | APPROVED | BLOCKED_UNVERIFIED
prepared_at:
base_commit:
project_commit:
connected_google_sheet:
```

## 1. 프로젝트·첫 세션 현황 감사

```yaml
latest_user_instruction:
current_confirmed_decisions:
project_agents_and_start_here:
active_context_and_documentation_map:
current_gdd_owner:
actual_code_data_scene_resource_ui_paths:
open_and_recent_merged_prs:
configured_google_sheets_state:
existing_tutorial_help_and_first_session:
current_progress:
next_work:
blocked_or_unverified:
```

판정:

- [ ] 프로젝트 정본을 확인했다.
- [ ] 실제 코드·데이터·Scene·Resource·UI·입력·테스트를 확인했다.
- [ ] 프로젝트 Google Sheets가 구성된 경우 현재 계획·진행도·`PROPOSED_SHEET_CHANGE`를 비교했다.
- [ ] 보류·대체·폐기된 구형 기획을 현재안으로 사용하지 않았다.
- [ ] 확인할 수 없는 사실을 `BLOCKED_UNVERIFIED`로 분리했다.

## 2. 대상 플레이어·플레이 상황·선수 지식

```yaml
target_player:
play_context:
first_session_duration_target:
prior_genre_knowledge_assumed:
input_and_platform_assumptions:
accessibility_barriers_to_check:
returning_player_context:
```

### 첫 세션 플레이어 약속

> `[대상 플레이어]가 [플레이 상황]에서 [핵심 행동·선택]을 직접 수행하고 [감정·판타지·성취]를 이해한 뒤, [다음 행동]을 스스로 선택한다.`

## 3. 핵심 학습 목표와 본편 규칙 연결

| ID | 학습 목표 | 플레이어 행동 | 필요한 정보 | 시스템 반응 | 본편 정본·구현 경로 | 성공 증거 | 실패·복구 |
|---|---|---|---|---|---|---|---|
| LEARN-001 |  |  |  |  |  |  |  |

정적 조작표나 팝업 확인만으로 학습 성공을 기록하지 않는다.

## 4. RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER 단계표

| 단계 | 상황·문제 | 플레이어 행동·선택 | 안내 수준 | 시스템 반응·피드백 | 통과 조건 | 실패·복구 | 근거 상태 |
|---|---|---|---|---|---|---|---|
| `RULE` | 기본 규칙을 실제 플레이로 수행 |  |  |  |  |  | CURRENT / INFERRED / PROPOSED / BLOCKED_UNVERIFIED |
| `NEED` | 필요·결핍과 문제 원인을 인식 |  |  |  |  |  |  |
| `DISCOVER` | 성장 시스템·도구·규칙·정보를 발견·적용 |  |  |  |  |  |  |
| `FEEL` | 성장 전후 차이를 비교·체감 |  |  |  |  |  |  |
| `PROVE` | 안내 없는 독립 수행 |  |  |  |  |  |  |
| `TRANSFER` | 다른 상황에서 재사용 |  |  |  |  |  |  |

## 5. 안내 감소·힌트·실패·복구·재시도

```text
시범·명확한 안내
→ 제한된 선택 안에서 수행
→ 힌트가 있는 유사 문제
→ 안내 없는 독립 수행
→ 다른 상황에서 재사용
```

| 학습 ID | 초기 안내 | 감소 조건 | 단계적 힌트 | 실패 원인 표시 | 복구·재시도 비용 | 독립 수행 검증 | 전이 검증 |
|---|---|---|---|---|---|---|---|
| LEARN-001 |  |  |  |  |  |  |  |

## 6. 필요·결핍과 성장 시스템 인과

```yaml
current_capability:
problem_or_deficit:
player_visible_cause:
warning_and_response_opportunity:
loss_or_cost:
recovery_path:
solution_discovered:
why_this_solution_fits:
alternative_solutions_deferred:
```

안전 확인:

- [ ] 상점·과금을 소개하기 위한 강제 패배가 아니다.
- [ ] 보이지 않는 규칙이나 고정 결과로 만든 가짜 결핍이 아니다.
- [ ] 실패 전에 예고와 대응 기회가 있다.
- [ ] 회복 불가능 손실이나 불필요한 긴 반복을 강제하지 않는다.

## 7. 성장 전후 비교와 성장 체감

```yaml
baseline_task:
before_time:
before_resource_cost:
before_risk_or_loss:
before_available_choices:
change_applied:
after_time:
after_resource_cost:
after_risk_or_loss:
after_available_choices:
new_capability_or_route:
player_explanation_expected:
core_fun_effect:
```

판정:

- `REAL_GROWTH`: 행동·선택·비용·위험·가능성이 의미 있게 변함
- `PRESENTATION_ONLY`: 숫자·이펙트·팝업만 변함
- `NULLIFIED_GROWTH`: 즉시 자동 보정되어 성취가 사라짐
- `BLOCKED_UNVERIFIED`: 비교 가능한 실제 근거가 없음

`PRESENTATION_ONLY` 또는 `NULLIFIED_GROWTH`를 성장 체감 완료로 판정하지 않는다.

## 8. Skip·복습·복귀·접근성 대체 채널

```yaml
skip_available:
skip_consequence:
help_reopen_path:
interactive_practice_replay:
returning_player_recap:
voice_alternative:
color_alternative:
time_limit_adjustment:
input_alternative:
subtitle_and_text_support:
focus_and_objective_clarity:
```

- [ ] Skip 후에도 핵심 도움말·목표·조작에 다시 접근할 수 있다.
- [ ] 복습이 정적 조작표만으로 제한되지 않는다.
- [ ] 복귀 플레이어가 필요한 개념만 재학습할 수 있다.
- [ ] 음성·색·시간 제한·단일 입력에만 필수 정보를 의존하지 않는다.
- [ ] 접근성 옵션 존재가 아니라 실제 장벽과 대체 경로를 검증한다.

## 9. 벤치마크 Evidence

### 현재 결정 질문

```yaml
decision_question:
comparison_dimensions:
```

| Evidence ID | 출처·URL | 층 | 게시·버전·확인일 | 제품 사실 | 행동·자기보고 | 작동 원리 | 실패 조건 | 프로젝트 적합성 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| TUT-EV-001 |  | T1 / T2 / T3 / T4 / T5 / T6 |  |  |  |  |  |  | ADOPT / ADAPT / AVOID / TEST / IGNORE |

외부 벤치마크는 프로젝트 정본이나 실제 구현 사실을 대체하지 않는다.

## 10. 플레이테스트·관찰·인터뷰·텔레메트리

```yaml
build_and_version:
target_group_and_prior_exposure:
player_task:
observation_plan:
interview_questions:
primary_metric:
guardrails:
success_criteria:
stop_criteria:
```

### 이벤트·퍼널

```yaml
telemetry_events:
  - session_started
  - learning_step_entered
  - first_meaningful_action
  - action_failed
  - hint_requested
  - help_reopened
  - step_retried
  - step_completed
  - tutorial_skipped
  - independent_task_succeeded
  - transfer_task_succeeded
  - session_abandoned
funnel_steps:
  - RULE
  - NEED
  - DISCOVER
  - FEEL
  - PROVE
  - TRANSFER
```

| 질문 | 실제 행동 근거 | 플레이어 자기보고 | 결과 | 해석 한계 |
|---|---|---|---|---|
| 규칙을 이해했는가 |  |  |  |  |
| 필요·결핍을 이해했는가 |  |  |  |  |
| 성장 체감을 얻었는가 |  |  |  |  |
| 안내 없이 수행하는가 |  |  |  |  |
| 다른 상황에서 재사용하는가 |  |  |  |  |

튜토리얼 완료율만으로 이해·숙련·쾌감·접근성을 판정하지 않는다.

## 11. 적대적 Finding

| Finding ID | 공격 질문 | 근거 | 심각도 | 비판 검증 | 판정 | 수정·보류 | 회귀 확인 |
|---|---|---|---|---|---|---|---|
| TUT-F-001 |  |  | MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER | VALID / INVALID / PARTIAL | ACCEPT / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED |  |  |

필수 공격 범위:

- 튜토리얼 전용 규칙과 본편 불일치
- 정적 조작표를 학습으로 오인
- 문제 인식 전 해결책 광고
- 강제 패배·가짜 결핍·회복 불가능 손실
- 가짜 성장 또는 성장 무효화
- 핵심 재미보다 상점·과금·알림 우선
- 여러 개념 동시 교육
- 완료율·한 번의 성공만으로 숙련 확정
- 안내 없는 독립 수행 누락
- 다른 상황에서 재사용하는 전이 검사 누락
- Skip·복습·복귀·접근성 대체 채널 누락
- 벤치마크를 프로젝트 정본으로 취급

## 12. 결정

| 대상 | 판정 | 이유·근거 | 정본 반영 위치 | 검증 | 다음 Gate |
|---|---|---|---|---|---|
|  | KEEP / CHANGE / REMOVE / TEST / HOLD |  |  |  |  |

## 13. 미검증·롤백·다음 작업

```yaml
not_run:
blocked_environment:
remaining_risks:
rollback:
next_validation:
next_owner:
```

완료 보고에서 실행하지 않은 사람 플레이테스트·엔진 런타임·접근성·성능·Google Sheets 동기화를 통과로 기록하지 않는다.
