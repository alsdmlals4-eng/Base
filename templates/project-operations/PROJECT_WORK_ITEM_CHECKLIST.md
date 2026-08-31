# 프로젝트 작업 카드·체크리스트

> 이 템플릿은 Goal·Playable Slice 또는 독립 작업의 진행 상태를 보여 주는 운영용 receipt다. 프로젝트의 기획·결정·데이터·코드·Scene·Resource·승인 asset·test·runtime evidence는 현재 repository owner가 계속 소유한다.

```text
PROJECT_WORK_KANBAN_CHECKLIST
CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON
PASS_ONLY_COUNTS_COMPLETE
NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR
NO_APPLICABLE_CHECKLIST
NO_HTML_DASHBOARD
NO_NEW_PAID_PM_TOOL
NO_FLEET_WIDE_EMPTY_ARTIFACT_ROLLOUT
```

## 1. 카드 메타데이터

```yaml
work_item_id:
parent_issue_ref:
project:
goal_or_slice:
title:
category: PLANNING | SYSTEM_DATA | CODE | UI_UX | VISUAL | AUDIO_VFX | BUG | QA | CANON_DOCS | RELEASE
status: BACKLOG | READY | IN_PROGRESS | VERIFY_REVIEW | BLOCKED_UNVERIFIED | USER_DECISION_REQUIRED | DEFERRED | DONE
priority: P0 | P1 | P2 | P3

player_or_user_value:
why_now:
depends_on: []
blocked_by: []

scope: []
out_of_scope: []
protected_scope: []

canon_owner:
actual_consumers: []
source_main_sha:
task_branch_or_pr:

acceptance_criteria: []
required_evidence: []
evidence_ceiling:

progress:
  completed_items:
  applicable_items:
  display:
blocker:
next_action:
resume_condition:
last_updated:
```

## 2. Context and authority

- 현재 사용자 지시:
- 현재 Goal·Playable Slice:
- project `AGENTS.md`·Active Context:
- 책임 원본 `canon_owner`:
- 실제 구현·소비처:
- 기준 branch·SHA:
- 같은 Goal의 기존 Issue·PR 검색 결과:
- 이 카드는 위 정본의 **derived operational view**이며 새로운 사실 정본이 아니다.

## 3. Scope and protected behavior

### 포함 범위

- `<포함 항목>`

### 제외 범위

- `<제외 항목>`

### 보호할 의미·동작·경로

- `<보호 항목>`

## 4. Dependencies and blocker

| 구분 | 참조 | 상태 | 영향 | 해제·재개 조건 |
|---|---|---|---|---|
| 선행 작업 |  |  |  |  |
| 공유 자원 |  |  |  |  |
| 차단 항목 |  |  |  |  |
| 사용자 결정 |  |  |  |  |

## 5. Acceptance criteria

완료 기준은 `조건 → 행동 → 관찰 가능한 결과 → 증거`로 작성한다.

- [ ] AC-01 — `<조건 → 행동 → 결과 → 증거>`
- [ ] AC-02 — `<조건 → 행동 → 결과 → 증거>`

## 6. Evidence-backed checklist

`[x]`는 요구 조건과 증거가 확인된 `PASS`에만 사용한다. 상태를 수동으로 바꾸는 것만으로 완료되지 않는다.

- [x] PASS — 완료 항목. evidence: `<command, URL, repository path, capture, run ID, SHA>`
- [ ] IN_PROGRESS — 현재 수행 중인 항목. owner: `<owner>`
- [ ] READY — 선행 조건을 충족한 다음 항목.
- [ ] BLOCKED_UNVERIFIED — blocker: `<missing source, executor, permission, or evidence>`
- [ ] USER_DECISION_REQUIRED — decision: `<meaning-, scope-, cost-, permission-, or release-changing choice>`
- [ ] DEFERRED — resume_condition: `<observable condition>`
- [ ] FAIL — evidence: `<reproduced failure and affected acceptance>`
- [ ] NOT_APPLICABLE — reason: `<why this item does not apply>`

### 진행률 계산

```text
applicable_items = all checklist items - NOT_APPLICABLE items
completed_items = PASS items only
progress = completed_items / applicable_items
```

- `READY`, `IN_PROGRESS`, `VERIFY_REVIEW`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`, `FAIL`은 완료 수에 포함하지 않는다.
- 적용 가능한 항목이 0개이면 `0/0`, `100%` 또는 `DONE`이 아니라 `NO_APPLICABLE_CHECKLIST`로 표시한다.
- 진행률은 상태 요약일 뿐 Acceptance Criteria와 증거를 대체하지 않는다.

## 7. Verification matrix

전체 검증 절차는 `templates/project-operations/DEVELOPMENT_GATES.md`를 따른다. 이 표는 현재 카드에 필요한 증거와 실제 결과만 연결한다.

| Evidence | 요구 여부 | 상태 | 방법·명령 | exact 대상 | 증거 | 미검증·실패 영향 |
|---|---:|---|---|---|---|---|
| `E0_CONTRACT` 기획·승인 계약 |  | NOT_RUN |  |  |  |  |
| `E1_STATIC` 포맷·문법·정적 검사 |  | NOT_RUN |  |  |  |  |
| `E2_TEST` 자동 테스트 |  | NOT_RUN |  |  |  |  |
| `E3_RUNTIME` 실제 실행 |  | NOT_RUN |  |  |  |  |
| `E4_VISUAL` 실제 화면·렌더 |  | NOT_RUN |  |  |  |  |
| `E5_PLAY` 기계·담당자 플레이 경로 |  | NOT_RUN |  |  |  |  |
| `E6_HUMAN_PLAYTEST` 사용자·플레이어 검수 |  | NOT_RUN |  |  |  |  |

허용 상태:

```text
PASS | FAIL | PARTIAL | NOT_RUN | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

자동 테스트 PASS는 runtime·화면·UX·Human/Player·사용자 승인·출시 PASS를 의미하지 않는다.

## 8. Repository readback

- 변경된 responsibility owner:
- 실제 diff와 승인 범위 대조:
- data·schema·ID·path consumer 확인:
- test·runtime·capture evidence:
- Decision·Active Context·handoff 갱신:
- asset manifest·provenance·SHA-256 갱신:
- exact HEAD 또는 merged main SHA:
- 남은 stale reference·drift:

## 9. Completion and next action

```yaml
acceptance_status: PASS | PARTIAL | FAIL | NOT_RUN
required_evidence_status: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED_UNVERIFIED
must_fix_remaining:
blocked_unverified_remaining:
user_decision_required_remaining:
repository_readback: PASS | PARTIAL | NOT_RUN
work_item_status:
next_action:
resume_condition:
rollback:
```

`DONE`은 다음을 모두 만족할 때만 사용한다.

- 모든 필수 Acceptance Criteria가 증거와 함께 PASS다.
- 이 카드에 요구된 Evidence level이 PASS다.
- 열린 `MUST_FIX`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`가 없다.
- repository owner·actual consumer·handoff의 필요한 readback이 끝났다.
- 변경이 있으면 exact diff·HEAD 또는 merged main·rollback이 연결됐다.

그 외에는 실제 상태에 따라 `VERIFY_REVIEW`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED` 또는 `DEFERRED`를 유지한다.
