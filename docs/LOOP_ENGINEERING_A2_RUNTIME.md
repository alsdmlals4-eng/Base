# Loop Engineering A2 Runtime Foundation

## Status

```text
SUPERSEDED_STATUS_SNAPSHOT
CURRENT_OPERATIONAL_STATUS_AUTHORITY:
  docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json
```

이 문서는 **A2 foundation의 설계 경계와 초기 실패-폐쇄 불변식**을 보존하는 역사/설계 문서다. 2026-08-14 당시의 FAKE-only 단계, 미구현 transport, deferred integration 목록을 현재 구현 상태로 사용하지 않는다.

현재 project test executor, PR handoff/postmerge closure, durable worktree resume, provider transport, Local Executor, Windows Docker boundary, REAL A2 burn-in 같은 이동 가능한 운영 상태는 `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`을 단일 machine-readable checkpoint로 조회한다. 이 문서에 해당 상태를 다시 수동 복제해 두 번째 권위를 만들지 않는다.

## Foundation authority

A run request는 유효한 Project Execution Capsule과 승인된 Implementation Package에서 파생되어야 한다. caller는 다음을 임의로 넓히거나 바꿀 수 없다.

- `allowed_paths`
- `forbidden_paths`
- Resource Locks
- project identity
- Requirement IDs
- authority/base SHA

기본 권위 흐름:

```text
Planning Lock + Visual Lock + Package + Coverage
→ M2 bundle validation
→ A2 Run Request
→ bounded Builder execution
→ actual Git Diff attestation
→ identity / budget / deadline / scope gate
→ read-only Critic result
→ Critic authority and coverage gate
→ WAITING_INTEGRATION or fail-closed terminal state
```

현재 실행 mode/transport의 실제 지원 범위는 machine checkpoint와 현재 runtime code/test를 다시 확인한다.

## Repository-control protection

A2 계열 실행은 malformed Package가 허용하려 해도 repository-control surface를 독립 보호해야 한다.

```text
.git/**
.github/**
AGENTS.md
SECURITY.md
```

Critic은 승인된 Package 밖의 Requirement ID나 path를 새 권위로 만들 수 없다. Critic `PASS`는 deterministic failure를 무시하지 못한다.

## Terminal-state meaning

역사적으로 A2 foundation은 다음과 같은 fail-closed 상태를 사용해 왔다.

```text
STALE_BASE_SHA
PROVIDER_FAILURE
PROVIDER_TIMEOUT
BUDGET_EXCEEDED
QUARANTINED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
NO_PROGRESS
REPAIR_LIMIT
WAITING_INTEGRATION
```

현재 schema의 정확한 상태 집합은 runtime code/schema를 확인한다.

`WAITING_INTEGRATION`은 **merge evidence가 아니다.** provider/Builder/Critic 실행이 성공했더라도 PR exact-head Required Checks, review threads, merge SHA, postmerge main readback, 제품 runtime evidence는 별도 책임이다.

## Worktree and Diff invariants

초기 `GitWorktreeBuilderAdapter`에서 정립된 다음 불변식은 후속 REAL/Local Executor 구현에서도 약화해서는 안 된다.

- 제품 source repository와 실행 worktree의 소유권을 분리한다.
- 기대하는 `expected_main_sha`/authority SHA를 명시적으로 검증한다.
- runtime root가 project repository와 충돌하지 않게 한다.
- changed-path evidence는 Worker 자기주장이 아니라 Git/authoritative filesystem evidence로 확인한다.
- declared-vs-actual changed-path mismatch는 fail closed다.
- out-of-scope mutation은 Critic 이전/이후 deterministic gate에서 차단된다.
- shell expansion에 의존하지 않고 bounded argv/process contract를 사용한다.
- secret-bearing environment를 일반 상속하지 않는다.
- timeout, ownership, cleanup은 현재 실행자가 소유한 범위만 다룬다.
- process/worktree resume는 durable ownership/lease identity를 확인하고 임의 workspace adopt를 금지한다.

과거 FAKE adapter가 지원하지 않았던 기능이 후속 slice에서 구현되었더라도 이 역사적 제약을 “현재 미구현”으로 읽지 않는다.

## Provider and evidence boundary

- `FAKE` 증거와 `REAL` 증거를 구분한다.
- provider transport 성공과 제품 변경 권위를 구분한다.
- repository CI와 사용자 PC/live runtime evidence를 구분한다.
- API key, authorization header, access/refresh token, client secret, hidden reasoning, 전체 environment를 public receipt에 기록하지 않는다.
- Builder/Critic의 project/run/package/SHA identity는 Run Request와 결합되어야 한다.
- provider/worker timeout·budget·repair limit는 누적 실행을 fail closed로 제한해야 한다.
- `COMPLETED`/`FAILED`/`BLOCKED` 의미는 bounded machine evidence와 일치해야 한다.

## Current operational checkpoint

현재 상태를 확인할 때는 먼저 다음을 읽는다.

```text
docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json
```

2026-08-18 현재 해당 checkpoint는 후속 작업을 통해 다음 범주의 구현/검증 상태가 foundation snapshot보다 진전되었음을 기록한다.

- project test executor
- PR handoff / postmerge closure
- durable worktree resume
- denied-network boundary
- ChatGPT-authenticated subscription Codex CLI transport
- unattended Local Executor / Windows host path
- REAL A2 burn-in evidence

정확한 SHA, PR, run count, current status는 이 문서의 문장보다 checkpoint를 사용한다. checkpoint와 실제 code/test가 충돌하면 freshness finding으로 처리하고 둘 중 하나를 추정으로 덮어쓰지 않는다.

## Preserved decisions

후속 구현이 진행되어도 다음 제품/자동화 권위는 별도 승인 없이 넓히지 않는다.

```yaml
A3_AUTO_MERGE: DISABLED
SCHEDULER: NOT_CONFIGURED
AUTOMATIC_PACKAGE_SELECTION: FORBIDDEN
AUTOMATIC_PRODUCT_SCOPE_SELECTION: FORBIDDEN
PLANNING_APPROVAL: HUMAN_ONLY
VISUAL_APPROVAL: HUMAN_ONLY
PROJECT_PRODUCT_MUTATION_IN_BASE_TESTS: NONE
```

- `AUTOMATIC_PACKAGE_SELECTION`은 승인된 Implementation Package를 runtime이 임의로 고르는 권한을 금지한다.
- `AUTOMATIC_PRODUCT_SCOPE_SELECTION`은 다음 프로젝트/제품 범위를 runtime이 임의로 고르는 권한을 금지한다.
- 둘은 서로 다른 권한 경계이며 하나가 다른 하나를 대체하지 않는다.

provider 비용 정책은 `AGENTS.md`의 `ZERO_INCREMENTAL_COST_REQUIRED`와 current operational checkpoint를 따른다. 과거의 paid-provider 전제를 현재 정책으로 재사용하지 않는다.

## Freshness rule

이 문서와 machine checkpoint가 서로 다른 역할을 가진다.

```text
foundation / historical invariants
  → docs/LOOP_ENGINEERING_A2_RUNTIME.md

current mutable operational status / evidence ceiling
  → docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json
```

새 Loop slice가 병합될 때 current status를 이 문서와 checkpoint 양쪽에 수동 복제하지 않는다. foundation invariant가 실제로 바뀐 경우에만 이 문서를 수정하고, 운영 상태 변화는 machine checkpoint와 그 소비 테스트를 갱신한다.
