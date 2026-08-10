# BCP-2026-013 — Post-Merge Continuation-State Reconciliation

## 출처와 상태

- Proposal ID: `BCP-2026-013-post-merge-continuation-state-reconciliation`
- 출처 프로젝트: `alsdmlals4-eng/ninja-survival-godot`
- 출처 프로젝트 기준 main: `9b85cf65a3ca4278f7d8ec1a7e527ecc857cbad1`
- 관련 프로젝트 PR: `#5`
- 제출일: `2026-08-10`
- 상태: `IMPLEMENTED`
- Knowledge Level: `Pattern`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow를 수정하지 않는다. 승인 전에는 proposal/evidence/registry만 등록한다.

## 관찰과 증거

프로젝트 인수인계 문서와 Active Context를 병합 직전 상태에서 정확하게 작성해도, 그 문서가 들어 있는 PR을 실제로 병합하면 `main` SHA, PR 상태, merge commit, post-merge CI, active source가 즉시 바뀐다.

닌자 서바이벌 프로젝트에서는 다음 순서가 실제로 발생했다.

1. MVP-4 설계 인수인계 문서를 `docs/mvp4-handoff-20260810`과 Draft PR #5에 저장했다.
2. `docs/ACTIVE_CONTEXT.md`는 당시 실제 상태인 `main@7ef8ee...`, `OPEN_DRAFT`, `NOT_MERGED`를 정확히 기록했다.
3. 사용자가 병합을 승인했다.
4. PR #5가 squash merge되어 `main@9b85cf65...`가 되었다.
5. 별도의 default-branch `push` CI가 시작됐다.
6. 그러나 방금 main에 들어온 live `docs/ACTIVE_CONTEXT.md`에는 여전히 병합 전 상태가 남았다.

즉 다음 구조적 stale edge가 존재한다.

```text
HANDOFF_STATE_VALID_AT_PR_HEAD
+ MERGE
= HANDOFF_STATE_STALE_ON_NEW_MAIN
```

원인은 pre-merge 검증 실패가 아니다. **상태 라우터가 자신을 운반하는 integration 결과를 미래 시점에 정확히 기록할 수 없기 때문**이다.

현재 Base의 `maintaining-project-context-and-handoff`는 runtime truth, 상태 분리, `context-refresh`, `session-handoff`, `resume`를 이미 소유한다. 따라서 새 Skill보다 기존 owner에 integration 이후 reconciliation lifecycle을 흡수하는 것이 적절하다.

상세 프로젝트 및 GitHub 근거는 `evidence/INDUSTRY_AND_PROJECT_EVIDENCE.md`에 보존한다.

## 일반화 후보

### Proposed General Rule

Continuation State 또는 Handoff를 포함한 PR/branch를 실제 통합한 뒤에는 integration 성공 자체로 handoff를 닫지 않고, **post-merge runtime truth를 다시 관측한 뒤 live continuation state를 reconcile**한다.

```text
PRE_MERGE_STATE_CAPTURE
→ EXACT_HEAD_OR_MERGE_REF_VERIFICATION
→ USER_INTEGRATION_APPROVAL
→ MERGE / INTEGRATION
→ OBSERVE_POST_MERGE_TRUTH
→ RECONCILE_LIVE_CONTINUATION_STATE
→ VERIFY_RECONCILIATION
→ CLOSE_HANDOFF
```

최소 관측 대상은 프로젝트가 사용하는 범위 안에서 다음 의미를 포함한다.

```yaml
integration:
  merged:
  merged_pr:
  merge_commit_sha:
repository:
  default_branch:
  default_branch_sha:
verification:
  post_merge_ci: PASS | FAIL | IN_PROGRESS | NOT_RUN
continuation:
  active_source:
  next_work:
  blockers:
```

필드명 자체를 Base가 강제하는 것은 아니다. 동등한 runtime truth를 확인하면 된다.

### Historical snapshot과 live router 분리

`PRE_MERGE_SNAPSHOT`은 과거 시점의 사실을 보존하는 history다. 날짜가 붙은 handoff, review report, pre-merge verification report는 이후 저장소가 변해도 당시 사실을 정확히 기록했다면 rewrite하지 않아도 된다.

반면 `LIVE_CONTINUATION_STATE`는 다음 세션이 현재 truth로 읽는 mutable router다. `ACTIVE_CONTEXT.md`, `CURRENT_STATUS.md`, resume manifest 등이 이에 해당한다.

핵심 invariant:

```text
LIVE_CONTINUATION_STATE
must not contradict currently observed repository truth.
```

예:

- 실제 PR이 merged인데 live state가 `OPEN_DRAFT`: `STALE`
- 실제 main이 B인데 current baseline을 A로 주장: `STALE`
- post-merge CI가 실행 중인데 `PASS` 기록: `INVALID / UNVERIFIED`
- dated handoff가 과거 draft 상태를 기록: `VALID_HISTORY`

### Existing Solution Verdict

`ABSORB`

- owner: `maintaining-project-context-and-handoff`
- supporting owner: 기존 integration / verification 규칙
- 신규 ACTIVE Skill: `0`
- 신규 자동 write workflow: `0`을 기본값으로 시작

### 프로젝트 전용으로 남길 내용

Base에 승격하지 않을 값:

- Ninja Survival의 백팩/조합 제품 규칙
- `6x6`, `4x3`, 3분 엘리트, 5분 보스 등의 숫자
- 프로젝트 PR #5 자체 번호
- 특정 `ACTIVE_CONTEXT.md` schema
- Godot/GUT workflow 이름
- 프로젝트 branch naming convention

Base는 **integration 후 live continuation state를 post-merge runtime truth와 재조정한다는 lifecycle 원리**만 소유한다.

## 적용 조건과 비사용 조건

### Use When

- current-state/handoff/router 문서가 변경 branch 또는 PR 안에 포함된다.
- merge로 baseline SHA, PR 상태, active branch, CI 상태가 변한다.
- 다음 세션이 해당 live 문서를 현재 truth로 읽는다.
- integration 자체가 session/milestone boundary다.

### Do Not Use When

- 문서가 명시적인 historical snapshot이고 current router 역할을 하지 않는다.
- live continuation state 자체가 없다.
- 외부 시스템이 authoritative live state를 자동 생성하고 freshness를 이미 보장한다.
- 단순 PR이고 다음 작업자의 resume 상태가 integration metadata에 의존하지 않는다.

## 반례와 위험

### Counterexample

`docs/reviews/2026-08-10-pre-merge-review.md`가 “검수 시점 head SHA는 abc123”이라고 기록했다면 이후 main이 바뀌어도 역사 문서이므로 수정할 필요가 없다.

반면 `docs/ACTIVE_CONTEXT.md`가 “현재 main=abc123, 현재 PR=open”이라고 주장한다면 merge 후에는 reconcile 대상이다.

### Risks

- 모든 merge마다 state commit을 강제하면 불필요한 commit churn이 생길 수 있다.
- state-only follow-up commit이 다시 main SHA를 바꾸는 자기참조 문제가 생길 수 있다.
- 자동화가 완료 전 CI를 PASS로 기록할 수 있다.
- historical snapshot을 live state처럼 rewrite하면 과거 증거가 훼손된다.

### Controls

- `LIVE_CONTINUATION_STATE`가 있는 경우에만 적용한다.
- historical handoff는 시점이 명확하면 보존한다.
- exact current SHA가 필수 정보가 아니면 stable ref와 `last_observed_sha` 의미를 분리할 수 있다.
- reconciliation commit 자신의 SHA를 다시 문서에 영원히 추적하도록 요구하지 않는다.
- post-merge CI는 실제 완료 전 `IN_PROGRESS` 또는 `UNVERIFIED`로 유지한다.
- 자동 write workflow는 이 proposal의 필수 구현이 아니다.

## 영향 범위와 검증

### 승인 후 영향 후보

- `skills/maintaining-project-context-and-handoff/SKILL.md`
  - integration 후 `post-merge reconcile` 단계 추가
  - live state와 historical snapshot 구분 명시
- `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
  - lifecycle reference 추가
- 관련 contract test
  - merged PR + stale live context fixture
  - historical snapshot은 rewrite 대상이 아님을 검증

초기 구현은 새 template/workflow보다 기존 owner의 reference contract와 test 추가를 우선한다.

### Compatibility

live Active Context가 없는 프로젝트에는 영향이 없다. 기존 dated handoff는 migration 강제 없이 historical evidence로 남길 수 있다.

### Security

향후 자동화가 write token을 사용하게 된다면 별도 보안 검토가 필요하다. 본 proposal은 자동 write 권한을 요구하지 않는다.

### Cost

수동 reconcile에는 merge 후 작은 read/update 비용이 생긴다. 대신 stale handoff를 다음 세션이 신뢰해 잘못된 branch·PR·baseline에서 작업하는 재조사 비용을 줄인다.

### Verification scenarios

#### Scenario 1 — merged handoff PR

Given:
- live state says `main=A`, `PR=OPEN`
- PR merges and actual main becomes `B`

Expected:
- handoff close 전에 live state를 reconcile하거나 명시적으로 stale/unverified 상태로 표시한다.
- final live state가 실제 merged state와 모순되지 않는다.

#### Scenario 2 — post-merge CI running

Given:
- PR merged
- default-branch CI still running

Expected:
- `IN_PROGRESS`는 허용
- `PASS` 선기록은 금지

#### Scenario 3 — historical snapshot

Given:
- dated handoff가 pre-merge state를 정확히 기록

Expected:
- historical file은 rewrite하지 않아도 된다.
- live router만 별도로 reconcile한다.

#### Scenario 4 — no live router

Given:
- ordinary PR
- current-state router 없음

Expected:
- 후속 state commit을 강제하지 않는다.

### Rollback

제안 단계에서는 활성 Base 동작이 바뀌지 않는다. 거절 시 Registry 상태만 Base 정책에 맞게 변경하고 proposal/evidence history는 보존한다.

## 승인과 구현

```yaml
proposal_status: IMPLEMENTED
approval_ref: docs/superpowers/specs/2026-08-10-approved-base-continuity-diagnostics-actions-design.md
implementation_pr: https://github.com/alsdmlals4-eng/Base/pull/260
implementation_merge_sha: d45a80c6b12a2c790bf1f5ba2338a1a53e5c165e
active_base_behavior_changed: true
```

구현 PR #260은 live continuation state 재조정과 historical snapshot 보존을 기존 handoff/freshness owner에 반영했다. 제품·프로젝트 runtime 상태를 자동 PASS로 승격하지 않는다.
