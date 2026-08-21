---
name: synchronizing-local-and-github-state
description: Use when local and GitHub state must be compared, reconciled, refreshed, published, or verified without overwriting work or divergent history, including when GitHub CLI or local push authentication is unavailable and connector fallback must be selected.
---

# Synchronizing Local and GitHub State

## Core principle

동기화 목표는 최신처럼 보이는 상태가 아니라 **같은 Commit 계보와 같은 승인 Decision을 안전하게 공유하는 상태**다.

```text
remote baseline
→ execution-surface-aware snapshot
→ concurrent-change preflight
→ compare
→ reconcile
→ refresh
→ publish
→ exact-SHA verify
→ derived-surface refresh
```

PR·Branch·path의 존재와 현재 활성 write owner는 별개지만, 열린 PR의 기본 보호는 owner 추정에 의존하지 않는다.

```text
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
FOLLOW_UP_TARGET_IS_MERGED_MAIN
```

`same goal`, owner evidence 부재, 현재 coordinator만 활성이라는 사실은 열린 PR mutation 권한이 아니다. open/draft/ready PR은 현황 확인에만 사용하고, 일반 후속 수정은 latest completed `main`에서 새 Branch로 시작한다.

## Skill Modes

- `preflight`: 현재 `execution_surface`에서 검증 가능한 remote/local/branch/worktree/PR/ownership 상태를 읽고 첫 write 전에 충돌을 판정한다.
- `reconcile`: divergence, stale base, same-goal overlap, workstream ownership과 **owner activity**를 분류하고 안전 경로를 선택한다.
- `refresh`: remote 최신 상태와 승인 Decision을 현재 작업면에 반영한다.
- `publish`: 검증된 변경만 push/PR로 게시한다.
- `verify`: 정확한 SHA·PR·Required Check·merge·main readback을 검증한다.
- `recover`: auth/tool/network/409/cancelled-run 같은 실패를 원인별로 분리하고 안전한 대체 경로로 재개한다.
- `copy-integrate`: latest completed `main`에 이미 병합된 material delta를 새 `PROVISIONAL_INTEGRATION` Branch에서 재현·흡수한다. 열린 PR delta는 사용자가 PR 번호와 허용 동작을 명시한 경우에만 예외적으로 사용한다.

## Required inputs

```yaml
repository:
execution_surface: LOCAL_WORKTREE | GITHUB_CONNECTOR_ONLY | HYBRID
current_task_or_pr_identity:
current_workstream_identity:
owner_workstream_identity:
owner_activity_classification: CURRENT_COORDINATOR | ACTIVE_OTHER_WORKER | NO_ACTIVE_OWNER_EVIDENCE | UNKNOWN_OWNER_ACTIVITY
current_owner_evidence: []
cross_workstream_absorption_authorized: false | true
source_main_sha:
current_main_sha:
write_parent_sha:
expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
current_branch:
current_worktree: <actual path> | NOT_APPLICABLE_CONNECTOR_ONLY
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
open_pr_changed_paths: []
protected_paths: []
user_approved_scope:
```

### Execution surface contract

- `LOCAL_WORKTREE`: 실제 local branch/worktree/dirty state를 읽고 그 관찰값을 기록한다.
- `GITHUB_CONNECTOR_ONLY`: authenticated connector의 remote branch/head/diff/PR/check 증거만 기록한다. 로컬 worktree가 존재한다고 가정하지 않고 `current_worktree: NOT_APPLICABLE_CONNECTOR_ONLY`로 둔다. 실행하지 않은 local test·dirty-state·filesystem 검사를 PASS로 만들지 않는다.
- `HYBRID`: local evidence와 connector evidence를 각각 어느 surface에서 읽었는지 구분한다. 한쪽 관찰을 다른 쪽 상태로 추정하지 않는다.

첫 persistent write 전 `write_parent_sha`가 아직 없으면 `PENDING_FIRST_WRITE`로 둔다. `expected_head_sha`도 첫 persistent write 전에는 `PENDING_FIRST_WRITE`, 그 뒤에는 실제 `<exact-sha>`로 갱신한다. 값을 추측하지 않는다.

## CONCURRENT_CHANGE_PREFLIGHT

모든 L1 이상 GitHub write/PR/merge 작업은 첫 persistent write 전에 다음 표를 닫는다.

```text
CONCURRENT_CHANGE_PREFLIGHT
execution_surface
current_task_or_pr_identity
current_workstream_identity
owner_workstream_identity
owner_activity_classification
current_owner_evidence
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
2. 겹치는 Branch/PR의 목적·계보를 `owner_workstream_identity`로 식별하고 open/draft/ready이면 read-only로 둔다.
3. 사용자 지시, current session/automation owner, Resource Lock, matching running execution처럼 **현재 쓰기 주체를 증명하는 자료**를 `current_owner_evidence`로 기록한다.
4. 현재 coordinator가 소유하면 `CURRENT_COORDINATOR`, 실제 다른 작업자가 활동 중이면 `ACTIVE_OTHER_WORKER`, 현재 owner evidence가 없으면 `NO_ACTIVE_OWNER_EVIDENCE`, 판단 근거 자체가 부족하면 `UNKNOWN_OWNER_ACTIVITY`로 `owner_activity_classification`을 정한다.
5. open/draft/ready PR은 owner activity와 무관하게 mutation-protected다. read-only 충돌 탐지만 허용한다.
6. owner evidence가 없어도 coordinator takeover로 재분류하지 않는다. 후속 작업은 latest completed `main`에서 시작한다.
7. 열린 PR mutation이 필요하면 사용자가 PR 번호와 허용 동작을 명시했는지 확인하고 그 범위만 `cross_workstream_absorption_authorized=true`로 기록한다.
8. owner activity를 판정할 수 없어도 read-only 보호는 유지한다. mutation 필요성과 권한이 불명확하면 `BLOCKED_UNVERIFIED`다.

### Preflight outcomes

- `CLEAR`: 현재 작업과 경쟁하는 write owner가 없고 현재 execution surface에서 base/head 증거가 최신이다.
- `STALE_BASE_SHA`: 작업의 기준 SHA가 current authority와 다르다. 최신 main에서 재기준화한다.
- `WAITING_RESOURCE`: 실제 `ACTIVE_OTHER_WORKER` 또는 현재 Resource Lock이 자원을 소유하고 있고 takeover 권한이 없다.
- `DUPLICATE_WORK`: 같은 Goal의 material delta가 실제 active owner에 의해 구현·검증 중이거나 completed main에서 이미 충족됐다.
- `BLOCKED_UNVERIFIED`: owner activity·workstream identity·branch ownership·current SHA·권한 또는 현재 surface에 필요한 증거를 검증할 수 없다.
- `PROVISIONAL_INTEGRATION`: merged-main material delta 또는 사용자가 PR 번호와 동작을 명시 승인한 예외 delta를 latest-main 통합 Branch에서 재현 중이다.

`PATH_OVERLAP`이 없어도 같은 schema, registry entry, policy decision, route identity처럼 `SEMANTIC_OVERLAP`이면 충돌로 본다.

## BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16

이 standing authorization은 latest completed `main`에서 통합하는 기술 경로다. 열린 PR mutation 권한을 만들지 않는다.

```text
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
FOLLOW_UP_TARGET_IS_MERGED_MAIN
```

### Authorization boundary

- latest completed `main`: 기존 승인 Goal 안의 main-retained delta는 별도 Branch의 `PROVISIONAL_INTEGRATION`으로 처리할 수 있다.
- open/draft/ready PR: read-only다. 같은 workstream, owner evidence 부재, 현재 coordinator 소유라는 이유로 close/merge/rebase/copy하지 않는다.
- explicit named exception: 사용자가 PR 번호와 허용 동작을 지정하면 그 exact head와 범위에 한해 `cross_workstream_absorption_authorized=true`로 기록한다.
- authorization ambiguity: 승인 대상 PR 또는 동작이 불명확하면 `BLOCKED_UNVERIFIED`다.

Explicit authorization must name the PR and allowed action; a general takeover or owner inference is insufficient.

### Integration sequence

```text
exact latest completed main
→ record execution_surface
→ record owner PR head SHAs read-only
→ record current_workstream_identity / owner_workstream_identity
→ record owner_activity_classification / current_owner_evidence
→ confirm merged-main source OR explicit named PR/action authorization
→ record overlapping paths / semantic resources
→ create separate PROVISIONAL_INTEGRATION branch
→ selective copy / reproduce only material delta
→ semantic reconciliation against latest main
→ run relevant tests + exact-head checks
→ absorbed_owner_deltas / residual_owner_deltas
→ merge integration PR if normal repository gates pass
→ postmerge main readback
→ supersede only authorized owner/backlog PRs with zero residual material delta
```

열린 owner PR branches를 직접 수정하지 않는다. 승인된 예외도 current integration Branch에서만 처리하고, 전체 stale branch를 merge해서 오래된 base를 되살리지 않는다.

### Required copy-integration evidence

```yaml
execution_surface:
owner_pr_head_shas: []
current_workstream_identity:
owner_workstream_identity:
owner_activity_classification:
current_owner_evidence: []
cross_workstream_absorption_authorized:
provisional_overlap_paths: []
provisional_semantic_resources: []
absorbed_owner_deltas: []
residual_owner_deltas: []
rejected_duplicate_authority: []
```

`residual_owner_deltas`가 있으면 owner PR을 보존한다. zero residual이어도 사용자가 PR 번호와 종료 동작을 명시하지 않았다면 close/supersede하지 않는다.

## Safe sync protocol

세부 명령·상태 표·충돌 판정은 `references/safe-sync-protocol.md`를 따른다.

핵심 단계:

1. exact remote authority를 읽는다.
2. 현재 `execution_surface`를 확정하고 그 surface에서 실제로 관찰 가능한 상태만 기록한다.
3. current workstream/owner workstream identity와 `owner_activity_classification / current_owner_evidence`를 판정한다.
4. local surface가 있으면 실제 local/worktree/branch 상태를 읽고, connector-only면 local 상태를 `NOT_APPLICABLE_CONNECTOR_ONLY`로 둔다.
5. first persistent write 전에 path + semantic overlap + open/recent PR를 비교한다.
6. open/draft/ready PR이면 owner activity와 무관하게 read-only로 둔다.
7. 명시적인 PR 번호+동작 승인이 있는 예외만 latest-main reconciliation 범위에서 처리한다.
8. `CLEAR` 또는 승인된 `PROVISIONAL_INTEGRATION`에서만 write한다.
9. PR creation 전 같은 preflight를 반복한다.
10. merge 직전 exact head/base/checks/threads를 다시 확인한다.
11. merge 후 새 main SHA와 파생 소비자를 readback한다.

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

`MISSING_OPTIONAL_CLI`는 작업 중단 판정이 아니라 capability routing 입력이다. `gh` 또는 local push auth가 없더라도 연결된 GitHub connector가 같은 동작을 권위 있게 지원하면 connector를 사용한다. `gh` 부재만으로 전체 작업을 중단하지 않는다. missing `gh` alone is not a blocker.

```text
GITHUB_CAPABILITY_FALLBACK
MISSING_OPTIONAL_CLI
→ inspect required GitHub capability
→ github_connector: prefer the authenticated connector when it provides the exact remote capability
→ local_git: retain local worktree, diff, commit, and test evidence when actually available
→ gh_cli: use only for a required capability not covered by the connector or local Git
→ execution_surface: GITHUB_CONNECTOR_ONLY if no usable local worktree is observed
→ current_worktree: NOT_APPLICABLE_CONNECTOR_ONLY
→ preserve exact head/base evidence
→ use update_ref(force=false) only when an explicit ref update is actually required
→ never force-update or weaken repository governance
```

connector의 Git Data 경로가 필요한 write를 지원하면 exact parent에서 `create_blob → create_tree → create_commit → update_ref(force=false)` 순서로 게시하고 각 결과를 readback한다. 이 경로도 PR·Required Check·review·merge·postmerge Gate를 우회하지 않는다.

connector가 필요한 read/write/PR/check capability를 제공하지 못하거나 현재 권한을 검증할 수 없으면 `BLOCKED_UNVERIFIED`다. fallback이 권한 확대·새 credential 저장·사용자 계정 변경을 요구하면 사용자 결정 Gate를 사용한다. Connector coverage를 확인하기 전에 사용자에게 반복 설치·재인증을 요청하지 않는다. A missing optional CLI **must not merge** an unverified change or justify bypassing normal PR/check gates.

### Local network/tool unavailable

local clone/test가 DNS/network/tool 부재로 막혀도 authenticated connector + repository-native CI가 같은 acceptance criterion을 증명할 수 있으면 `execution_surface: GITHUB_CONNECTOR_ONLY`로 전환한다. 실행하지 않은 local validation·dirty-state·worktree 검사를 PASS로 주장하지 않는다.

### Cancelled CI

`cancelled`는 PASS도 코드 FAIL도 아니다.

- 같은 exact head의 더 최신 authoritative run이 있으면 최신 run을 사용한다.
- concurrency가 이전 run을 취소한 경우 superseding run을 끝까지 본다.
- 더 최신 run이 없으면 같은 exact head에서 failed/cancelled jobs를 안전하게 rerun한다.
- 실행 중에는 불필요한 PR/head mutation으로 `cancel-in-progress`를 다시 유발하지 않는다.

## Semantic reconciliation

merged-main 후속 변경 또는 명시 승인된 예외를 통합할 때 파일 bytes만 복사하지 않는다. 다음을 latest main 기준으로 재판정한다.

- 현재 owner/canon은 무엇인가
- current owner evidence가 실제로 있는가
- successor PR이 이미 같은 material delta를 병합했는가
- old source PR의 unique delta가 실제로 남았는가
- 더 강한 현재 구현이 old implementation을 대체했는가
- test/evidence ceiling이 더 최신인가
- whole-branch merge가 stale code/policy를 부활시키는가
- 열린 PR을 사용한다면 현재 사용자가 PR 번호와 허용 동작을 명시했는가

판정:

```text
ABSORB_MATERIAL_DELTA
ALREADY_ABSORBED_BY_SUCCESSOR
REJECT_DUPLICATE_AUTHORITY
PRESERVE_RESIDUAL_OWNER
READ_ONLY_OPEN_PR
EXPLICIT_NAMED_EXCEPTION
SUPERSEDED_BY_MERGED_MAIN
BLOCKED_EXTERNAL
WAITING_RESOURCE
BLOCKED_UNVERIFIED
```

## Publish and merge gate

게시·병합은 최소 다음을 확인한다.

- `execution_surface`와 그 surface에서 실제로 관찰한 증거
- current branch/head exact SHA
- current main/base exact SHA
- current/owner workstream identity, `owner_activity_classification`, `current_owner_evidence`, explicit named authorization 상태
- expected head SHA와 실제 head SHA 일치
- intended diff와 실제 diff 일치
- required checks 실제 PASS
- unresolved review thread 0
- required approvals가 저장소 규칙과 일치
- P0/P1 unresolved 0
- `NOT_RUN`/`BLOCKED_*`/`CANCELLED`를 PASS로 승격하지 않음
- 어떤 open/draft/ready PR도 explicit named authorization 없이 건드리지 않음

병합 뒤 새 `main`을 다시 읽지 않으면 완료가 아니다.

## Output contract

```md
## 동기화 mode / execution_surface
## repository / branch / worktree-or-NOT_APPLICABLE_CONNECTOR_ONLY
## current_task_or_pr_identity
## current_workstream_identity / owner_workstream_identity
## owner_activity_classification / current_owner_evidence
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

- 현재 `execution_surface`에 없는 local/remote 상태를 꾸며내지 않았다.
- `GITHUB_CONNECTOR_ONLY`에서는 `current_worktree: NOT_APPLICABLE_CONNECTOR_ONLY`를 사용하고 local 검사 결과를 추정하지 않았다.
- open/draft/ready PR을 owner activity와 무관하게 read-only로 유지했다.
- 열린 PR mutation이 있었다면 사용자가 PR 번호와 허용 동작을 명시했다.
- 일반 후속 수정은 latest completed main에서 시작했고 main-retained delta만 대상으로 했다.
- first write, PR creation, merge 직전 preflight를 실제로 재실행했다.
- stale SHA·409·non-fast-forward를 blind overwrite로 처리하지 않았다.
- 열린 owner PR branches를 직접 수정하지 않았다.
- latest main에서 selective delta만 통합했다.
- exact-head Required Checks를 확인했다.
- postmerge main SHA/readback을 확인했다.
- 실행하지 않은 로컬/CI/merge evidence를 성공으로 표시하지 않았다.

Learning Log: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
