# BCP-2026-013 — Post-Merge Continuation-State Reconciliation

## 출처와 상태

- Proposal ID: `BCP-2026-013-post-merge-continuation-state-reconciliation`
- 출처 프로젝트: `alsdmlals4-eng/ninja-survival-godot`
- 출처 프로젝트 기준 main: `9b85cf65a3ca4278f7d8ec1a7e527ecc857cbad1`
- 관련 프로젝트 PR: `#5`
- 관련 프로젝트 파일:
  - `docs/ACTIVE_CONTEXT.md`
  - `docs/CURRENT_CONFIRMED_DECISIONS.md`
  - `docs/handoffs/2026-08-10-mvp4-backpack-design-handoff.md`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- Knowledge Level: `Pattern`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow를 수정하지 않는다. 승인 전에는 proposal/evidence/registry만 등록한다.

## 관찰과 증거

### Problem

프로젝트 인수인계 문서와 Active Context를 **병합 직전 상태에서 정확하게 작성**하더라도, 그 문서가 들어 있는 PR을 실제로 병합하면 다음 사실들이 즉시 바뀐다.

- `main` SHA
- PR 상태 (`OPEN`/`DRAFT` → `MERGED`/`CLOSED`)
- merge commit SHA
- post-merge `push` CI 상태
- 다음 작업자가 읽어야 할 active source (`PR branch` → `main`)

따라서 merge 전에는 정확했던 Continuation State가 merge 직후에는 스스로 stale해질 수 있다.

닌자 서바이벌 프로젝트에서 실제로 다음 일이 발생했다.

1. MVP-4 설계 인수인계용 문서들을 별도 branch와 Draft PR #5에 저장했다.
2. `docs/ACTIVE_CONTEXT.md`는 당시 실제 상태를 정확히 기록했다.
   - `main_sha: 7ef8ee...`
   - `handoff_pr_state: OPEN_DRAFT`
   - `handoff_pr_merged: NOT_RUN_USER_APPROVAL_REQUIRED`
3. 사용자가 인수인계 PR 병합을 승인했다.
4. PR #5는 squash merge되어 `main@9b85cf65...`가 되었다.
5. post-merge main CI도 별도 `push` run으로 시작됐다.
6. 그러나 방금 병합된 `docs/ACTIVE_CONTEXT.md` 안에는 여전히 병합 전 SHA와 `OPEN_DRAFT / NOT_MERGED` 상태가 남았다.

즉:

```text
HANDOFF_STATE_VALID_AT_PR_HEAD
+ MERGE
= HANDOFF_STATE_STALE_ON_NEW_MAIN
```

이 문제는 제품 내용의 오류가 아니라 **상태 스냅샷이 자기 자신을 운반하는 PR의 병합 이벤트를 미래 상태로 기록할 수 없다는 구조적 문제**다.

### Root Cause

현재 Base `maintaining-project-context-and-handoff`는 runtime truth 확인, 상태 분리, 책임 원본 갱신, `context-refresh`, `session-handoff`, `resume`를 이미 소유한다.

부족한 것은 새 책임 영역이 아니라 **integration이 실제로 완료된 뒤 continuation-state owner를 한 번 더 runtime truth에 맞춰 reconcile해야 한다는 명시적 lifecycle 단계**다.

```text
PRE_MERGE_HANDOFF_SNAPSHOT
→ INTEGRATION
→ POST_MERGE_RUNTIME_TRUTH
→ CONTINUATION_STATE_RECONCILIATION
```

merge 이전의 exact-head 검증은 merge 이후의 repository-state metadata까지 미래 예측할 수 없다.

### Existing Base Coverage

현행 `maintaining-project-context-and-handoff`는 이미 다음을 제공한다.

- 실제 저장소·프로젝트 상태를 먼저 확인하는 `Runtime truth`
- 확정/구현/검증/진행 중/미확정을 분리하는 상태 모델
- Active Context를 전문 복제물이 아니라 압축 라우터로 유지하는 `context-refresh`
- 세션/브랜치/마일스톤 경계의 `session-handoff`
- 최신 Branch·Commit·실제 파일을 다시 확인하는 `resume`

따라서 새 ACTIVE Skill은 필요하지 않다.

### Existing Solution Verdict

`ABSORB`

- owner: `maintaining-project-context-and-handoff`
- supporting owner: 기존 integration / verification 규칙
- 새 ACTIVE Skill: `0`
- 새 광역 Template: 원칙적으로 `0`

## 일반화 후보

### Proposed General Rule

Continuation State 또는 Handoff 문서가 포함된 PR/branch를 병합하거나 통합한 경우, integration 성공 자체로 작업을 종료하지 말고 **post-merge runtime truth를 다시 관측한 뒤 상태 라우터를 reconcile**한다.

권장 lifecycle:

```text
1. PRE_MERGE_STATE_CAPTURE
2. EXACT_HEAD_OR_MERGE_REF_VERIFICATION
3. USER_INTEGRATION_APPROVAL
4. MERGE / INTEGRATION
5. OBSERVE_POST_MERGE_TRUTH
   - actual main/default-branch SHA
   - PR merged/closed state
   - merge commit SHA
   - post-merge CI/check state
   - active source-of-truth branch/path
6. RECONCILE_CONTINUATION_STATE
7. VERIFY_RECONCILIATION
8. ONLY_THEN_CLOSE_HANDOFF
```

### State classes

병합 전과 병합 후를 한 문서에서 섞지 않도록 다음 개념을 구분한다.

#### `PRE_MERGE_SNAPSHOT`

당시 실제 상태를 보존하는 history snapshot. 이후 stale해져도 틀린 기록이 아니라 과거 기록이다.

예:

- dated handoff
- review report
- pre-merge verification report

이런 문서는 과거 시점을 명시한다면 병합 뒤 굳이 rewrite하지 않아도 된다.

#### `LIVE_CONTINUATION_STATE`

다음 세션이 현재 상태로 읽는 mutable router.

예:

- `ACTIVE_CONTEXT.md`
- `CURRENT_STATUS.md`
- resume manifest

이 파일은 merge 이후 stale metadata를 그대로 남기면 안 된다.

### Required post-merge observations

최소 관측값:

```yaml
integration:
  merged: true | false
  merged_pr:
  merge_commit_sha:
repository:
  default_branch:
  default_branch_sha:
verification:
  post_merge_ci: PASS | FAIL | IN_PROGRESS | NOT_RUN
continuation:
  active_source: main | branch | pr
  next_work:
  blockers:
```

프로젝트가 이 모든 필드를 실제 파일에 사용해야 한다는 뜻은 아니다. **동등한 의미의 runtime truth**를 확보하면 된다.

### Reconciliation invariant

```text
LIVE_CONTINUATION_STATE
must not claim a branch/PR/integration state
that contradicts currently observed repository truth.
```

구체적으로:

- PR이 merged인데 `OPEN_DRAFT`를 current state로 유지: `STALE`
- main SHA가 바뀌었는데 이전 SHA를 current baseline으로 유지: `STALE`
- post-merge CI가 아직 돌고 있는데 `PASS`로 기록: `UNVERIFIED / INVALID`
- historical handoff가 “당시 PR은 draft였다”고 기록: `VALID_HISTORY`

### Safe update pattern

병합 직후 state 파일을 고치는 방법은 프로젝트 상황에 따라 다를 수 있다.

권장 우선순위:

1. merge 전에 live state가 미래 merge 결과를 추측해서 쓰지 않는다.
2. merge 후 실제 값을 읽는다.
3. live continuation file만 최소 수정한다.
4. dated historical snapshot은 시점이 명확하면 보존한다.
5. 상태 수정 자체도 branch/PR 정책을 따라 검증한다.

자동화를 도입하더라도 CI가 merge commit SHA를 추측하거나 미완료 check를 PASS로 기록하지 않게 한다.

## 프로젝트 전용으로 남길 내용

Base에 올리지 않을 값:

- Ninja Survival의 MVP-4 백팩 규칙
- `6x6`, `4x3`, 3분 엘리트, 5분 보스 등 제품 결정
- 프로젝트 PR #5 자체의 번호
- 특정 `ACTIVE_CONTEXT.md` schema
- 프로젝트별 Godot/GUT workflow 이름
- 특정 branch naming convention

Base는 **integration 이후 live continuation state를 runtime truth와 재조정한다는 lifecycle 원리**만 소유한다.

## 적용 조건과 비사용 조건

### Use When

- 인수인계/Active Context/Resume 문서가 변경 branch 또는 PR 안에 함께 포함되어 있다.
- merge로 baseline SHA, PR 상태, active branch, CI 상태가 변한다.
- 다음 세션이 live status 문서를 현재 truth로 사용할 예정이다.
- integration 자체가 milestone/session boundary다.

### Do Not Use When

- 문서가 명시적인 과거 snapshot이며 current-state router 역할을 하지 않는다.
- merge가 repository-state metadata에 아무 영향도 주지 않고 live continuation file도 없다.
- 단순 코드 PR이며 handoff/current-status 문서를 전혀 다루지 않는다.
- 외부 시스템이 이미 authoritative live state를 자동 생성하고 stale 여부를 검증한다.

### Counterexample

`docs/reviews/2026-08-10-pre-merge-review.md`가 “검수 시점 head SHA는 abc123이었다”고 기록하고 이후 PR이 merge되어 main SHA가 달라졌다면, 그 리뷰 문서는 과거 증거이므로 수정할 필요가 없다.

반면 `docs/ACTIVE_CONTEXT.md`가 “current main = abc123, current PR = open”이라고 주장한다면 merge 후에는 reconcile 대상이다.

## 산업 관행과 정합성

상세 근거는 `evidence/INDUSTRY_AND_PROJECT_EVIDENCE.md`가 책임진다.

핵심은 GitHub 자체도 PR merge branch, PR head, default-branch push를 서로 다른 ref/event 상태로 구분한다는 점이다.

- 열린 PR의 `pull_request` workflow는 `refs/pull/<n>/merge`라는 시뮬레이션 merge branch를 사용할 수 있다.
- 실제 merge 후 default branch에는 별도의 `push` event가 발생하며 그 `GITHUB_SHA`는 실제로 갱신된 ref의 tip이다.
- 따라서 pre-merge PR verification과 post-merge default-branch truth는 같은 상태가 아니다.

이는 Base에서 live continuation metadata 역시 `pre-merge verified`와 `post-merge observed`를 구분해야 한다는 제안과 정합적이다.

## Benefits

- 다음 세션이 이미 병합된 PR을 여전히 `OPEN_DRAFT`로 오독하는 문제를 막는다.
- merge 후 새 main SHA를 즉시 resume baseline으로 사용할 수 있다.
- pre-merge 검증과 post-merge 검증의 증거 경계를 선명하게 한다.
- historical snapshot을 불필요하게 rewrite하지 않고 live router만 정확하게 유지한다.
- handoff/integration이 자주 발생하는 장기 프로젝트에서 상태 drift를 줄인다.

## Risks

- 모든 merge마다 상태 문서를 강제 수정하면 불필요한 commit churn이 생길 수 있다.
- state-only follow-up PR이 또 다른 merge를 만들며 SHA를 다시 바꾸는 자기참조 문제가 생길 수 있다.
- 자동화가 미완료 CI를 PASS로 기록할 수 있다.
- historical snapshot과 live state를 구분하지 않으면 과거 증거를 훼손할 수 있다.

### Risk controls

- `LIVE_CONTINUATION_STATE`가 있는 경우에만 적용한다.
- immutable/historical handoff는 그대로 보존한다.
- live state에 exact current SHA가 꼭 필요하지 않다면 stable ref + `last_observed_sha`처럼 의미를 분리할 수 있다.
- state-only reconcile commit 때문에 SHA가 또 바뀌는 경우, 문서가 자기 commit SHA 자체를 반드시 기록하도록 강제하지 않는다.
- post-merge CI는 실제 완료 전까지 `IN_PROGRESS` 또는 `UNVERIFIED`로 기록한다.

## 영향 경로

승인 후 구현 후보:

- `skills/maintaining-project-context-and-handoff/SKILL.md`
  - integration 후 `post-merge reconcile` step 추가
  - `context-refresh`와 `session-handoff`의 live/historical distinction 명시
- `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
  - lifecycle reference 추가
- 관련 test/contract
  - merged PR + stale Active Context fixture
  - historical snapshot은 rewrite 대상이 아님을 검증

초기 구현에서는 새 template이나 자동 workflow를 만들지 않고 **기존 owner의 reference contract + test**로 충분한지 먼저 검증하는 것을 권장한다.

## 호환성·보안·비용

### Compatibility

기존 프로젝트에 live Active Context가 없으면 영향 없음.

기존 handoff 문서는 과거 snapshot으로 유지할 수 있으므로 migration 강제 없음.

### Security

post-merge reconcile 자동화가 write token을 요구하는 방식으로 발전한다면 별도 보안 검토가 필요하다. 본 proposal은 자동 write workflow를 요구하지 않는다.

### Cost

수동 방식은 merge당 API/read + 작은 state update 비용이 생긴다. 그러나 잘못된 stale handoff를 다음 세션이 믿어 생기는 재조사·잘못된 branch 작업 비용을 줄일 수 있다.

## 검증 시나리오

승인 후 구현에서는 최소 다음 계약을 검증한다.

### Scenario 1 — merged handoff PR

Given:
- Active Context says PR open and main=A
- PR is merged and main becomes=B

Expected:
- handoff cannot be declared closed until live state is reconciled or explicitly marked stale/unverified
- final live state reflects merged PR and observed main

### Scenario 2 — post-merge CI running

Given:
- PR merged
- default-branch CI is still running

Expected:
- live state may record `IN_PROGRESS`
- it must not record `PASS`

### Scenario 3 — historical snapshot

Given:
- dated handoff accurately records pre-merge state
- merge happens later

Expected:
- historical file remains valid without rewrite
- live Active Context is updated separately

### Scenario 4 — no live continuation state

Given:
- ordinary code PR
- no current-state router

Expected:
- no mandatory follow-up document churn

## Rollback

제안 단계 rollback은 단순하다.

- 제안이 거절되면 `REJECTED` 또는 해당 Base 상태 모델에 맞게 Registry 상태만 변경한다.
- 활성 Skill·Method·Test는 아직 바뀌지 않았으므로 runtime rollback은 없다.
- evidence와 proposal history는 삭제하지 않는다.

## 승인과 구현

```yaml
proposal_status: SUBMITTED
approval_ref: null
implementation_pr: null
active_base_behavior_changed: false
```

사용자가 이 proposal의 **구현**까지 별도로 승인하면 기존 Base 절차에 따라 proposal 상태를 `APPROVED_FOR_IMPLEMENTATION`으로 바꾸고, 별도 구현 PR에서 기존 `maintaining-project-context-and-handoff` owner에 흡수한다.

이번 proposal PR을 Base main에 병합하는 것은 proposal history를 등록하는 행위이며 활성 Base 동작 변경 승인을 의미하지 않는다.
