---
name: synchronizing-local-and-github-state
description: Use when local and GitHub state must be compared, reconciled, refreshed, published, or verified without overwriting work or divergent history, including when GitHub CLI or local push authentication is unavailable and connector fallback must be selected.
---

# Synchronizing Local and GitHub State

## Core principle

동기화 목표는 최신처럼 보이는 상태가 아니라 **같은 Commit 계보와 같은 승인 Decision을 안전하게 공유하는 상태**다.

```text
remote baseline
→ local snapshot
→ concurrent-change preflight
→ compare
→ reconcile
→ refresh
→ publish
→ exact-SHA verify
→ derived-surface refresh
```

다른 채팅 또는 독립 workstream의 Branch·path·PR은 같은 Goal처럼 보여도 기본적으로 별개다.

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

`same goal`은 `same workstream`의 증거가 아니다. `different workstream`이면 사용자의 현재 명시 승인 없이 checkout/write/rebase/close/merge/selective-copy를 수행하지 않는다.

## Skill Modes

- `preflight`: remote/local/branch/worktree/PR/ownership 상태를 읽고 첫 write 전에 충돌을 판정한다.
- `reconcile`: divergence, stale base, same-goal overlap, workstream ownership을 분류하고 안전 경로를 선택한다.
- `refresh`: remote 최신 상태와 승인 Decision을 현재 작업면에 반영한다.
- `publish`: 검증된 변경만 push/PR로 게시한다.
- `verify`: 정확한 SHA·PR·Required Check·merge·main readback을 검증한다.
- `recover`: auth/tool/network/409/cancelled-run 같은 실패를 원인별로 분리하고 안전한 대체 경로로 재개한다.
- `copy-integrate`: **same workstream** 또는 사용자가 현재 작업에서 명시적으로 흡수 승인한 `different workstream`의 owner delta를 latest completed `main` 위 별도 `PROVISIONAL_INTEGRATION` Branch에서 선택적으로 재현·흡수한다.

## Required inputs

```yaml
repository:
current_task_or_pr_identity:
current_workstream_identity:
owner_workstream_identity:
cross_workstream_absorption_authorized: false | true
source_main_sha:
current_main_sha:
write_parent_sha:
expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
current_branch:
current_worktree:
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
open_pr_changed_paths: []
protected_paths: []
user_approved_scope:
```

첫 persistent write 전 `write_parent_sha`가 아직 없으면 `PENDING_FIRST_WRITE`로 둔다. `expected_head_sha`도 첫 persistent write 전에는 `PENDING_FIRST_WRITE`, 그 뒤에는 실제 `<exact-sha>`로 갱신한다. 값을 추측하지 않는다.

## CONCURRENT_CHANGE_PREFLIGHT

모든 L1 이상 GitHub write/PR/merge 작업은 첫 persistent write 전에 다음 표를 닫는다.

```text
CONCURRENT_CHANGE_PREFLIGHT
current_task_or_pr_identity
current_workstream_identity
owner_workstream_identity
cross_workstream_absorption_authorized
source_main_sha
current_main_sha
write_parent_sha
expected_head_sha
intended_paths
semantic_resource_locks
same_goal_open_and_recent_prs
open_pr_changed_paths
```

### Workstream identity gate

1. 현재 채팅/작업 계약/PR을 `current_workstream_identity`로 식별한다.
2. 겹치는 owner Branch/PR의 소유 작업을 `owner_workstream_identity`로 식별한다.
3. 둘이 명확히 같은 작업 흐름이면 `same workstream`으로 판정할 수 있다.
4. 다른 채팅·독립 작업으로 확인되면 `different workstream`이다.
5. owner identity를 확인할 수 없으면 `UNKNOWN_WORKSTREAM`이며, cross-workstream 흡수는 `BLOCKED_UNVERIFIED`다.
6. `different workstream`에서 `cross_workstream_absorption_authorized=false`이면 read-only 충돌 탐지만 허용하고 실제 Branch/path/PR 변경·흡수는 `WAITING_RESOURCE`로 둔다.
7. 사용자가 현재 작업에서 다른 workstream을 **명시적으로 흡수·통합 승인**한 경우에만 `cross_workstream_absorption_authorized=true`로 기록하고 예외적인 copy integration을 허용한다.

### Preflight outcomes

- `CLEAR`: 현재 작업과 경쟁하는 write owner가 없고 base/head 증거가 최신이다.
- `STALE_BASE_SHA`: 작업의 기준 SHA가 현재 authority와 다르다. 최신 main에서 재기준화한다.
- `WAITING_RESOURCE`: path/semantic resource가 다른 task/PR 또는 다른 workstream owner에게 있고 현재 작업에 변경 권한이 없다.
- `DUPLICATE_WORK`: 같은 Goal의 material delta가 이미 다른 owner에 의해 구현·검증되고 있다.
- `BLOCKED_UNVERIFIED`: workstream identity·branch ownership·current SHA·open PR·권한을 검증할 수 없다.
- `PROVISIONAL_INTEGRATION`: same-workstream overlap 또는 현재 사용자에게 cross-workstream 흡수 승인을 받은 owner delta를 latest-main 통합 Branch에서 재현 중이다.

`PATH_OVERLAP`이 없어도 같은 schema, registry entry, policy decision, route identity처럼 `SEMANTIC_OVERLAP`이면 충돌로 본다.

## BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16

이 standing authorization은 동시 작업을 막지 않고 latest completed `main`에서 통합하는 기본 기술 경로를 제공하지만, **workstream 경계를 자동으로 넘는 사용자 권한은 아니다.**

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

### Authorization boundary

- `same workstream`: 기존 승인 Goal 안의 same-goal/path/semantic overlap이면 standing authorization으로 `PROVISIONAL_INTEGRATION`을 시작할 수 있다.
- `different workstream`: standing authorization만으로는 흡수 권한이 생기지 않는다. 현재 사용자가 명시적으로 흡수·통합 승인해 `cross_workstream_absorption_authorized=true`가 된 경우에만 예외적으로 같은 절차를 사용한다. This is **explicit user authorization** for the current integration scope; it is not standing cross-workstream permission.
- `UNKNOWN_WORKSTREAM`: 사용자의 명시 승인과 owner identity evidence가 없으면 `BLOCKED_UNVERIFIED` 또는 `WAITING_RESOURCE`다.
- 다른 채팅 owner PR을 “같은 Goal”이라는 이유만으로 자동 close/merge/rebase/copy하지 않는다.

### Integration sequence

```text
exact latest completed main
→ record owner PR head SHAs read-only
→ record current_workstream_identity / owner_workstream_identity
→ confirm same workstream OR explicit cross-workstream absorption authorization
→ record overlapping paths / semantic resources
→ create separate PROVISIONAL_INTEGRATION branch
→ selective copy / reproduce only material delta
→ semantic reconciliation against latest main
→ run relevant tests + exact-head checks
→ absorbed_owner_deltas / residual_owner_deltas
→ merge integration PR if normal repository gates pass
→ postmerge main readback
→ supersede only authorized owner PRs with zero residual material delta
```

owner PR branches를 직접 수정하지 않는다. current integration Branch에서만 변경한다. 전체 stale branch를 merge해서 오래된 base를 되살리지 않는다.

### Required copy-integration evidence

```yaml
owner_pr_head_shas: []
current_workstream_identity:
owner_workstream_identity:
cross_workstream_absorption_authorized:
provisional_overlap_paths: []
provisional_semantic_resources: []
absorbed_owner_deltas: []
residual_owner_deltas: []
rejected_duplicate_authority: []
```

`residual_owner_deltas`가 있으면 owner PR을 보존한다. zero residual이어도 다른 workstream owner PR은 사용자의 명시 승인 범위 밖에서 close/supersede하지 않는다.

## Safe sync protocol

세부 명령·상태 표·충돌 판정은 `references/safe-sync-protocol.md`를 따른다.

핵심 단계:

1. exact remote authority를 읽는다.
2. current workstream/owner workstream identity를 판정한다.
3. local/worktree/branch 상태를 읽는다.
4. first persistent write 전에 path + semantic overlap + open/recent PR를 비교한다.
5. same workstream이면 cooperative ownership 규칙을 적용한다.
6. different workstream이면 explicit user absorption authorization 없이는 read-only 탐지까지만 하고 owner surface를 건드리지 않는다.
7. `CLEAR` 또는 승인된 `PROVISIONAL_INTEGRATION`에서만 write한다.
8. PR creation 전 같은 preflight를 반복한다.
9. merge 직전 exact head/base/checks/threads를 다시 확인한다.
10. merge 후 새 main SHA와 파생 소비자를 readback한다.

## Failure and recovery

### Stale write / HTTP 409

GitHub contents API 등에서 stale blob/head로 409가 나면 blind retry하지 않는다.

```text
409 / non-fast-forward
→ exact current blob/head re-read
→ compare intended delta with current content
→ preserve newer content
→ apply only missing delta
→ re-run regression
```

stale bytes로 전체 파일을 다시 밀어넣지 않는다.

### Missing local CLI or auth — `GITHUB_CAPABILITY_FALLBACK`

`MISSING_OPTIONAL_CLI`는 작업 중단 판정이 아니라 capability routing 입력이다. `gh` 또는 local push auth가 없더라도 연결된 GitHub connector가 같은 동작을 권위 있게 지원하면 connector를 사용한다. missing `gh` alone is not a blocker.

```text
GITHUB_CAPABILITY_FALLBACK
MISSING_OPTIONAL_CLI
→ inspect required GitHub capability
→ prefer authenticated connector when it provides the exact capability
→ preserve exact head/base evidence
→ use update_ref(force=false) only when an explicit ref update is actually required
→ never force-update or weaken repository governance
```

connector가 필요한 read/write/PR/check capability를 제공하지 못하거나 현재 권한을 검증할 수 없으면 `BLOCKED_UNVERIFIED`다. fallback이 권한 확대·새 credential 저장·사용자 계정 변경을 요구하면 사용자 결정 Gate를 사용한다. A missing optional CLI **must not merge** an unverified change or justify bypassing normal PR/check gates.

### Local network/tool unavailable

local clone/test가 DNS/network/tool 부재로 막혀도 authenticated connector + repository-native CI가 같은 acceptance criterion을 증명할 수 있으면 그 경로로 전환한다. 실행하지 않은 local validation을 PASS로 주장하지 않는다.

### Cancelled CI

`cancelled`는 PASS도 코드 FAIL도 아니다.

- 같은 exact head의 더 최신 authoritative run이 있으면 최신 run을 사용한다.
- concurrency가 이전 run을 취소한 경우 superseding run을 끝까지 본다.
- 더 최신 run이 없으면 같은 exact head에서 failed/cancelled jobs를 안전하게 rerun한다.
- 실행 중에는 불필요한 PR/head mutation으로 `cancel-in-progress`를 다시 유발하지 않는다.

## Semantic reconciliation

같은 Goal의 변경을 흡수할 때 파일 bytes만 복사하지 않는다. 다음을 latest main 기준으로 재판정한다.

- 현재 owner/canon은 무엇인가
- successor PR이 이미 같은 material delta를 병합했는가
- old source PR의 unique delta가 실제로 남았는가
- 더 강한 현재 구현이 old implementation을 대체했는가
- test/evidence ceiling이 더 최신인가
- whole-branch merge가 stale code/policy를 부활시키는가
- 다른 workstream이면 현재 사용자 absorption authorization이 실제로 있는가

판정:

```text
ABSORB_MATERIAL_DELTA
ALREADY_ABSORBED_BY_SUCCESSOR
REJECT_DUPLICATE_AUTHORITY
PRESERVE_RESIDUAL_OWNER
WAITING_RESOURCE
BLOCKED_UNVERIFIED
```

## Publish and merge gate

게시·병합은 최소 다음을 확인한다.

- current branch/head exact SHA
- current main/base exact SHA
- current/owner workstream identity와 cross-workstream authorization 상태
- expected head SHA와 실제 head SHA 일치
- intended diff와 실제 diff 일치
- required checks 실제 PASS
- unresolved review thread 0
- required approvals가 저장소 규칙과 일치
- P0/P1 unresolved 0
- `NOT_RUN`/`BLOCKED_*`/`CANCELLED`를 PASS로 승격하지 않음
- stale/independent owner PR을 승인 없이 건드리지 않음

병합 뒤 새 `main`을 다시 읽지 않으면 완료가 아니다.

## Output contract

```md
## 동기화 mode
## repository / branch / worktree
## current_task_or_pr_identity
## current_workstream_identity / owner_workstream_identity
## cross_workstream_absorption_authorized
## source_main_sha / current_main_sha / write_parent_sha / expected_head_sha
## intended_paths / semantic_resource_locks
## same-goal open/recent PRs
## concurrent preflight 판정
## owner PR head SHAs / overlap
## absorbed_owner_deltas / residual_owner_deltas
## 실행한 write / publish / merge
## exact-head checks / review threads
## postmerge main readback
## BLOCKED / NOT_RUN / rollback
```

## Quality gate

완료 보고 전에 다음을 모두 만족한다.

- 다른 채팅/독립 workstream을 같은 Goal이라는 이유만으로 수정·흡수하지 않았다.
- cross-workstream absorption은 현재 사용자의 명시 승인이 있을 때만 수행했다.
- first write, PR creation, merge 직전 preflight를 실제로 재실행했다.
- stale SHA·409·non-fast-forward를 blind overwrite로 처리하지 않았다.
- owner PR branches를 직접 수정하지 않았다.
- latest main에서 selective delta만 통합했다.
- exact-head Required Checks를 확인했다.
- postmerge main SHA/readback을 확인했다.
- 실행하지 않은 로컬/CI/merge evidence를 성공으로 표시하지 않았다.

Learning Log: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
