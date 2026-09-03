# 사람용 Blueprint 프로젝트 작업현황 장 템플릿

```text
HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION
PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON
NO_SEPARATE_PM_PDF
NO_HTML_DASHBOARD
```

이 템플릿은 별도 문서가 아니라 기존 `HUMAN_MASTER_GDD_PDF` 안에 들어가는 장의 source 형식이다. 실제 값은 repository owner, AI production spec, `project_work_kanban`, evidence에서 같은 revision으로 읽는다.

## 프로젝트 작업 현황

| Metadata | Value |
|---|---|
| project | `${project}` |
| current_goal_or_slice | `${current_goal_or_slice}` |
| source_commit | `${source_commit}` |
| generated_at | `${generated_at}` |
| included_scope | `${included_scope}` |
| approval_status | `${approval_status}` |
| evidence_ceiling | `${evidence_ceiling}` |

| 현황 축 | 완료 / 적용 |
|---|---:|
| 프로젝트 목표 | `${completed_goals} / ${applicable_goals}` |
| 시스템 | `${completed_systems} / ${applicable_systems}` |
| 플레이 케이스 | `${completed_cases} / ${applicable_cases}` |
| 필수 작업 | `${completed_work_items} / ${applicable_work_items}` |
| 차단 | `${blocked_count}` |
| 사용자 결정 필요 | `${user_decision_count}` |

> 한 개의 전체 퍼센트로 합치지 않는다. `NOT_APPLICABLE`은 reason을 기록하고 분모에서 제외한다.

## 현재 작업과 다음 행동

| 항목 | 값 |
|---|---|
| active `WORK_ITEM_ID` | `${active_work_item_ref}` |
| 상태 | `${work_status}` |
| 작업 목적 | `${work_title}` |
| blocker | `${blocker_or_none}` |
| resume condition | `${resume_condition_or_none}` |
| 다음 안전 작업 | `${next_action}` |

## 프로젝트 목표 지도

```text
PROJECT_GOAL_MAP
GOAL_ID → SYSTEM_ID → CASE_ID → WORK_ITEM_ID → EVIDENCE
```

현재 승인 Goal/Playable Slice와 필수 하위 목표의 시작·종료·플레이어 가치를 설명한다.

## 목표별 체크리스트

### `${GOAL_ID}` `${goal_title}`

| 항목 | 값 |
|---|---|
| 플레이어 가치 | `${player_value}` |
| 현재 성숙도 | `${maturity_status}` |
| 목표 성숙도 | `${target_status}` |
| 연결 시스템 | `${system_refs}` |
| 연결 케이스 | `${case_refs}` |
| 연결 작업 | `${work_item_refs}` |
| 완료 조건 | `${goal_completion_condition}` |
| blocker | `${blocker_or_none}` |
| 다음 행동 | `${next_action}` |

- [ ] 목표 성숙도 충족
- [ ] 연결 필수 시스템 완료
- [ ] 적용 가능한 필수 케이스 완료
- [ ] 연결 필수 작업 `DONE`

체크는 실제 계산과 evidence를 근거로 채운다. 문서 작성만으로 완료 체크하지 않는다.

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
| 연결 작업 | `${work_item_refs}` |
| 다음 행동 | `${next_action}` |

- [ ] 시스템 목적·경계·입력·출력 정의
- [ ] 상태·데이터·이벤트·저장 영향 정의
- [ ] UI·입력·피드백·실패·복구 흐름 정의
- [ ] 필요한 이미지·사운드·텍스트·애니메이션 상태군 준비
- [ ] 실제 consumer 구현
- [ ] 정적 검사·자동 테스트
- [ ] runtime·visual·play 검증
- [ ] 필요한 human/user approval

적용하지 않는 항목은 `[x]`가 아니라 `NOT_APPLICABLE — reason`으로 남긴다.

## 케이스별 검증 현황

| CASE_ID | 유형 | SYSTEM_ID | 관련 GOAL_ID | 적용 | 기획/구현 성숙도 | 필수 evidence | 실제 결과 | WORK_ITEM_ID | 다음 행동 |
|---|---|---|---|---|---|---|---|---|---|
| `${CASE_ID}` | `${case_type}` | `${system_ref}` | `${goal_refs}` | `APPLICABLE / NOT_APPLICABLE` | `${maturity_status} → ${target_status}` | `${required_evidence}` | `${PASS / FAIL / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED / NOT_APPLICABLE}` | `${work_item_refs}` | `${next_action}` |

케이스 유형은 실제 소비처와 위험에 필요한 것만 선택한다.

```text
NORMAL | BOUNDARY | FAILURE | CONFLICT | INTERRUPTION
RECOVERY | SAVE_LOAD | UI_STATE | ACCESSIBILITY | PERFORMANCE
```

## 목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적

| WORK_ITEM_ID | 작업 상태 | GOAL_ID | SYSTEM_ID | CASE_ID | canon/evidence source | blocker / next action |
|---|---|---|---|---|---|---|
| `${WORK_ITEM_ID}` | `${status}` | `${goal_refs}` | `${system_refs}` | `${case_refs}` | `${source_ref}` | `${blocker_or_next_action}` |

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

자동 테스트 PASS는 runtime·화면·UX·사용자 승인·출시 PASS가 아니다.
