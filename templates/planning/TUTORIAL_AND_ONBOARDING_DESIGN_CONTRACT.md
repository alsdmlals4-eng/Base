# 튜토리얼·온보딩 설계 Contract

```yaml
project:
  work_mode: PLAN
  owner_skill: analyzing-and-refining-game-concepts
  owner_mode: tutorial-and-onboarding-design
  status: DRAFT | REVIEW | APPROVED | BLOCKED_UNVERIFIED
  base_commit:
  project_commit:
  project_workspace: DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
  repository_human_projection:
  v4_notion_exception_scope: NONE | EXPLICITLY_APPROVED
  repository_structured_canon:
  legacy_sheet_migration_evidence: NONE | READ_ONLY_REFERENCE
```

## 1. 프로젝트·첫 세션 현황 감사

```yaml
latest_user_instruction:
current_confirmed_decisions:
project_agents_and_start_here:
current_gdd_owner:
repository_human_projection_and_v4_notion_exception_state:
actual_code_data_scene_resource_ui_paths:
open_and_recent_merged_prs:
legacy_sheet_migration_evidence:
existing_tutorial_help_and_first_session:
blocked_or_unverified:
```

- [ ] 프로젝트 repository 정본·exact-SHA human projection·실제 코드·데이터·Scene·Resource·UI·입력·테스트를 확인했다. 명시된 V4 Notion exception 또는 legacy migration source만 추가로 대조했다.
- [ ] 폐기된 Google Sheets는 프로젝트가 명시적으로 보존한 migration/read-only evidence가 있을 때만 비교했고 신규 입력·활성 정본으로 사용하지 않았다.
- [ ] 확인하지 못한 사실을 `BLOCKED_UNVERIFIED`로 분리했다.

## 2. 대상 플레이어·학습 목표

| ID | 학습 목표 | 플레이어 행동 | 필요한 정보 | 시스템 반응 | 본편 정본·구현 경로 | 성공 증거 | 실패·복구 |
|---|---|---|---|---|---|---|---|
| LEARN-001 |  |  |  |  |  |  |  |

## 3. RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER

| 단계 | 상황·문제 | 플레이어 행동·선택 | 안내 수준 | 시스템 반응·피드백 | 통과 조건 | 실패·복구 | 근거 상태 |
|---|---|---|---|---|---|---|---|
| RULE |  |  |  |  |  |  | CURRENT / PROPOSED / BLOCKED_UNVERIFIED |
| NEED |  |  |  |  |  |  |  |
| DISCOVER |  |  |  |  |  |  |  |
| FEEL |  |  |  |  |  |  |  |
| PROVE | 안내 없는 독립 수행 |  |  |  |  |  |  |
| TRANSFER | 다른 상황에서 재사용 |  |  |  |  |  |  |

### FIRST_10_MINUTES_CONTRACT

첫 10분은 장르·세션 길이에 맞춰 조정 가능한 기본값이며, 전체 시스템 설명 목표가 아니다. 대표 경험이 한 번 완결되는지 기록한다.

| 흐름 | 첫 세션에서 확인할 내용 | 관찰 방법 | 근거 상태 |
|---|---|---|---|
| 대표 문제 | 지금 해결할 문제를 설명할 수 있는가 |  | NOT_RUN / PARTIAL / PASSED / FAILED |
| 대표 행동 | 핵심 행동을 안내 없이 찾는가 |  |  |
| 첫 선택 | 선택 이유와 포기하는 것을 말할 수 있는가 |  |  |
| 첫 결과 | 결과의 원인을 설명할 수 있는가 |  |  |
| 다음 질문 | 다음 시도에서 바꿀 행동을 말하는가 |  |  |

의도적 미스터리·느린 도입은 시간값을 `PROJECT_ADAPTED`로 바꿀 수 있지만, 행동 목적까지 불명확하게 만드는 근거가 되지 않는다.

## 4. 성장 체감·접근성·근거

```yaml
before_time_cost_risk:
change_applied:
after_time_cost_risk:
new_choice_or_capability:
skip_available:
help_reopen_path:
returning_player_recap:
accessibility_alternative_channels:
benchmark_question:
benchmark_decision: ADOPT | ADAPT | AVOID | TEST | IGNORE
```

## 5. 플레이테스트·텔레메트리·적대적 검토

```yaml
target_group_and_prior_exposure:
evidence_layers:
  TECH_EVIDENCE: NOT_RUN
  UI_EVIDENCE: NOT_RUN
  HUMAN_USABILITY_EVIDENCE: NOT_RUN
  PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
player_task:
primary_metric:
guardrails:
success_criteria:
stop_criteria:
telemetry_events:
  - first_meaningful_action
  - hint_requested
  - help_reopened
  - tutorial_skipped
  - independent_task_succeeded
  - transfer_task_succeeded
```

| Finding | 근거 | 판정 | 수정·보류 | 회귀 확인 |
|---|---|---|---|---|
| 강제 패배·가짜 성장·정적 조작표·전이 누락 여부 |  | MUST_FIX / SHOULD_FIX / DEFER / BLOCKED_UNVERIFIED |  |  |

## 6. 결정·미검증·다음 Gate

| 대상 | 판정 | 근거 | 정본 반영 위치 | 검증 | 다음 Gate |
|---|---|---|---|---|---|
|  | KEEP / CHANGE / REMOVE / TEST / HOLD |  |  |  |  |

```yaml
not_run:
remaining_risks:
rollback:
next_validation:
next_owner:
```
