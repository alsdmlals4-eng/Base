# 사람용 Blueprint 프로젝트 작업현황 장 템플릿

```text
HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION
PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON
PROJECT_WORK_KANBAN_DIRECT_SOURCE_NO_STATUS_COPY
NO_SEPARATE_PM_PDF
NO_HTML_DASHBOARD
```

이 템플릿은 별도 문서가 아니라 기존 `HUMAN_MASTER_GDD_PDF` 안에 들어가는 장의 source 형식이다. 실제 값은 repository owner, AI production spec, 기존 `project_work_kanban`, evidence에서 같은 revision으로 읽는다. Goal/System checklist와 관계 mapping은 transient projection이고, 작업 상태는 board에서 직접 읽는다.

## 프로젝트 작업 현황

| Metadata | Value |
|---|---|
| project | `${project}` |
| current_goal_or_slice | `${project_work_kanban.goal_or_slice_issue_ref}` |
| source_commit | `${source_commit}` |
| generated_at | `${generated_at}` |
| included_scope | `${included_scope}` |
| approval_status | `${approval_status}` |
| evidence_ceiling | `${evidence_ceiling}` |
| work_status_snapshot_source | `${work_status_snapshot_source}` |
| work_status_snapshot_generated_at | `${work_status_snapshot_generated_at}` |
| work_status_snapshot_staleness | `${CURRENT_AT_SOURCE_SHA / STALE_SNAPSHOT / UNVERIFIED}` |
| progress_calculation_basis | `INDEPENDENT_GOAL_SYSTEM_CASE_WORK_COUNTS` |

| 현황 축 | 완료 / 적용 |
|---|---:|
| 프로젝트 목표 | `${completed_goals} / ${applicable_goals}` |
| 시스템 | `${completed_systems} / ${applicable_systems}` |
| 플레이 케이스 | `${completed_cases} / ${applicable_cases}` |
| 필수 작업 | `${completed_work_items} / ${applicable_work_items}` |
| 차단 | `${blocked_count}` |
| 사용자 결정 필요 | `${user_decision_count}` |

> 한 개의 전체 퍼센트로 합치지 않는다. `NOT_APPLICABLE`은 reason을 기록하고 분모에서 제외하며, 적용 항목이 0이면 `NO_APPLICABLE_CHECKLIST`를 표시한다.

## 현재 작업과 다음 행동

| 항목 | 값 source |
|---|---|
| active `WORK_ITEM_ID` | `${project_work_kanban.active_work_item_ref}` |
| 상태·작업명 | `${project_work_kanban.work_items[WORK_ITEM_ID]}` |
| blocker | `${project_work_kanban.work_items[WORK_ITEM_ID].blocker_or_none}` |
| resume condition | `${project_work_kanban.work_items[WORK_ITEM_ID].resume_condition_or_none}` |
| 다음 안전 작업 | `${project_work_kanban.next_action}` |

별도 root work-status 필드를 복사하지 않는다.

## 프로젝트 목표 지도

| GOAL_ID | 목표 | SYSTEM_ID | CASE_ID | WORK_ITEM_ID |
|---|---|---|---|---|
| `${GOAL_ID}` | `${goal_title}` | `${system_refs}` | `${case_refs}` | `${work_item_refs}` |

## 목표별 체크리스트

### `${GOAL_ID}` `${goal_title}`

| 항목 | 값 |
|---|---|
| 플레이어 가치 | `${player_value}` |
| 현재 / 목표 성숙도 | `${maturity_status} → ${target_status}` |
| 연결 시스템 | `${system_refs}` |
| 연결 케이스 | `${case_refs}` |
| 연결 작업 상태 | `${project_work_kanban status by work_item_refs}` |
| 연결 blocker | `${derived from linked project_work_kanban work items}` |
| 다음 행동 | `${next_action}` |

| 체크 ID | 목표 완료 조건 | 상태 | evidence / reason |
|---|---|---|---|
| `${GOAL-CHECK-ID}` | `${human-readable criterion}` | `${PASS / NOT_RUN / PARTIAL / BLOCKED_UNVERIFIED / USER_DECISION_REQUIRED / NOT_APPLICABLE}` | `${evidence locators or N/A reason}` |

적용 가능한 모든 목표 checklist 항목이 evidence-backed `PASS`이고, 연결 시스템·케이스·작업이 완료돼야 목표 완료다.

## 시스템 기획별 체크리스트

### `${SYSTEM_ID}` `${system_title}`

| 항목 | 값 |
|---|---|
| 플레이어 가치 | `${player_value}` |
| canon owner | `${canon_owner}` |
| actual consumer | `${actual_consumers}` |
| 현재 / 목표 성숙도 | `${maturity_status} → ${target_status}` |
| 연결 목표 | `${goal_refs}` |
| 연결 케이스 | `${case_refs}` |
| 연결 작업 상태 | `${project_work_kanban status by work_item_refs}` |
| 연결 blocker | `${derived from linked project_work_kanban work items}` |
| 다음 행동 | `${next_action}` |

| 체크 ID | 시스템 기획·준비·구현·검증 항목 | 상태 | evidence / reason |
|---|---|---|---|
| `${SYS-CHECK-ID}` | `${purpose/boundary/input/output/state/data/UI/asset/save/failure/rollback/verification criterion}` | `${status}` | `${evidence locators or N/A reason}` |

`NOT_APPLICABLE`은 `[x]`로 표시하지 않고 reason과 함께 분모에서 제외한다.

## 케이스별 검증 현황

| CASE_ID | 유형 | SYSTEM_ID | GOAL_ID | 적용 | 성숙도 | 필수 evidence | evidence별 실제 결과 | WORK_ITEM_ID 상태 | 다음 행동 |
|---|---|---|---|---|---|---|---|---|---|
| `${CASE_ID}` | `${case_type}` | `${system_ref}` | `${goal_refs}` | `${APPLICABLE / NOT_APPLICABLE}` | `${maturity_status} → ${target_status}` | `${required_evidence}` | `${E2_TEST: PASS; E3_RUNTIME: NOT_RUN ...}` | `${direct project_work_kanban status}` | `${next_action}` |

적용 가능한 케이스는 비어 있지 않은 필수 evidence를 선언한다. 유형은 실제 consumer와 위험에 필요한 것만 선택한다.

```text
NORMAL | BOUNDARY | FAILURE | CONFLICT | INTERRUPTION
RECOVERY | SAVE_LOAD | UI_STATE | ACCESSIBILITY | PERFORMANCE
```

## 목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적

| WORK_ITEM_ID | 작업·상태 source | GOAL_ID | SYSTEM_ID | CASE_ID | owner / consumer | blocker · resume · next |
|---|---|---|---|---|---|---|
| `${WORK_ITEM_ID}` | `${project_work_kanban.work_items[WORK_ITEM_ID]}` | `${work_item_links.goal_refs}` | `${work_item_links.system_refs}` | `${work_item_links.case_refs}` | `${canon_owner / actual_consumers}` | `${direct board fields}` |

`work_item_links`는 관계만 저장하며 title/status/blocker/next action을 복사하지 않는다. ID 집합은 board의 필수 작업 ID 집합과 정확히 같아야 한다.

## 검증 수준 범례

| Level | 의미 | 현재 결과 |
|---|---|---|
| `E0_CONTRACT` | 기획·승인 계약 | `${status}` |
| `E1_STATIC` | 포맷·문법·정적 검사 | `${status}` |
| `E2_TEST` | 자동 테스트 | `${status}` |
| `E3_RUNTIME` | 실제 실행 | `${status}` |
| `E4_VISUAL` | 실제 화면·렌더 | `${status}` |
| `E5_PLAY` | 기계·담당자 플레이 경로 | `${status}` |
| `E6_HUMAN_PLAYTEST` | 사용자·플레이어 검수 | `${status}` |

`evidence_ceiling`보다 높은 필수 evidence 또는 PASS는 허용하지 않는다. 자동 테스트 PASS는 runtime·화면·UX·사용자 승인·출시 PASS가 아니다.
