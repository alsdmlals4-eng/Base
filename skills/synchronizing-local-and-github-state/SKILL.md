---
name: synchronizing-local-and-github-state
description: Use when local and GitHub state must be compared, reconciled, refreshed, published, or verified without overwriting work or divergent history, including when GitHub CLI or local push authentication is unavailable and connector fallback must be selected.
---

# Synchronizing Local and GitHub State

## Core principle

동기화는 무조건 pull·commit·push하는 자동화가 아니다. 먼저 양쪽 상태와 권한을 판정하고, **clean + fast-forward + 승인된 변경**일 때만 자동 진행한다.

여러 채팅·Agent·PR이 같은 저장소를 다룰 때 Git의 ahead/behind만으로는 안전을 증명할 수 없다. 첫 persistent write, PR 생성, merge 전에는 열린·최근 PR과 의도한 경로·의미 자원·기준 SHA를 비교한 `CONCURRENT_CHANGE_PREFLIGHT`를 닫는다. 이 기록은 협업자가 따르는 **cooperative coordination contract**이며 GitHub가 강제하는 mutex·lock service라고 주장하지 않는다.

이 Skill은 Git 상태의 동등성, 동시작업 소유권 사전판정과 안전한 전달만 책임진다. 변경 내용의 품질·완료 여부는 `reviewing-and-validating-project-changes`, PR 제안·승인 정책은 `managing-base-change-proposals`, 장기 실행 checkpoint는 `maintaining-long-running-task-continuity`가 책임진다. Loop Engineering Run이 있으면 그 `TASK_LEASE`·path/semantic `RESOURCE_LOCK`을 재사용하고 별도 권한 체계를 만들지 않는다.

## Modes and states

`inspect` → `reconcile` → `refresh-local | publish-remote` → `verify-sync`

Git 상태:

`SYNCED / DIRTY / LOCAL_AHEAD / REMOTE_AHEAD / DIVERGED / BLOCKED`

동시작업 disposition:

`CLEAR / STALE_BASE_SHA / WAITING_RESOURCE / DUPLICATE_WORK / BLOCKED_UNVERIFIED`

GitHub 실행 capability:

`github_connector / local_git / gh_cli / MISSING_OPTIONAL_CLI`

## Required inputs

항상 필요한 입력:

```yaml
repository_and_remote:
local_branch_head_and_status:
remote_branch_head:
uncommitted_and_untracked_files:
upstream_and_branch_policy:
credentials_permissions_and_required_checks:
allowed_generated_files_and_secrets_policy:
available_github_capabilities:
```

첫 persistent write, PR 생성 또는 merge를 수행할 때 추가로 필요한 입력:

```yaml
current_task_or_pr_identity:
source_main_sha:
current_main_sha:
write_parent_sha:
expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
open_pr_changed_paths: {}
protected_concurrent_paths: []
```

- `current_task_or_pr_identity`는 현재 작업을 다른 Task·Branch·PR과 구별하는 안정적 식별자다. same-goal·path 비교에서는 이 작업 자신을 제외한다.
- `source_main_sha`는 조사·분기 기준, `current_main_sha`는 판정 시점의 실제 기본 Branch다.
- `write_parent_sha`는 **다음 persistent write가 적용될 것으로 기대하는 현재 작업 Branch의 exact HEAD**다. 실제 Branch HEAD와 다르면 write를 중단하고 다시 읽는다.
- 첫 write 전 최종 변경 HEAD는 아직 존재하지 않으므로 `expected_head_sha: PENDING_FIRST_WRITE`다. 첫 write가 반환한 commit SHA부터 exact `expected_head_sha`로 갱신하고, 다음 write 전에는 그 값을 새 `write_parent_sha`로 승격한다.
- PR 검토·CI·merge 단계의 `expected_head_sha`는 검토·검사·병합하려는 정확한 변경 HEAD다.

열린 PR 목록, changed paths, 현재 main, 현재 작업 identity, Branch HEAD 또는 권한 정책을 읽지 못하면 충돌 없음으로 추정하지 않는다.

안전한 명령·충돌·조정 절차는 `references/safe-sync-protocol.md`를 필요할 때만 읽는다.

## `GITHUB_CAPABILITY_FALLBACK`

GitHub 게시·검토 작업은 특정 실행 파일의 존재가 아니라 **현재 필요한 동작을 안전하게 수행할 capability**로 판정한다.

1. 연결·인증된 `github_connector`가 필요한 repository read/write, Branch, Git object, PR, merge, status 동작을 지원하면 먼저 사용한다.
2. `local_git`은 checkout·status·diff·stage·commit과 인증 가능한 push에 사용한다. push 인증이 없더라도 로컬 검증 결과와 파일을 버리지 않는다.
3. `gh_cli`는 connector와 `local_git`이 제공하지 않는 필수 기능에만 사용한다. 설치·인증돼 있으면 사용할 수 있지만 공용 선행조건이 아니다.
4. `gh: command not found`, `gh auth status` 실패 또는 로컬 push 인증 실패는 `MISSING_OPTIONAL_CLI`다. connector가 현재 작업을 완결할 수 있으면 **`gh` 부재만으로 전체 작업을 중단하지 않는다**.
5. connector coverage가 있는데 사용자에게 `gh` 반복 설치·재인증을 요청하지 않는다. Windows token을 cloud container로 복사하거나 비밀이 아닌 `GH_TOKEN`으로 지속시키지 않는다.
6. 필요한 정확한 동작과 증거를 `github_connector`, `local_git`, `gh_cli` 모두 제공하지 못할 때만 `BLOCKED_UNVERIFIED`로 판정하고, 누락 capability 하나를 구체적으로 보고한다.

인증된 push가 없고 connector Git object write가 있으면 검증된 로컬 파일을 `create_blob` → base tree를 사용한 `create_tree` → exact parent의 `create_commit` → `update_ref(force=false)` 순서로 게시한다. 각 persistent write 전 `CONCURRENT_CHANGE_PREFLIGHT`와 `write_parent_sha`를 다시 확인하고, PR·CI·merge에는 connector가 반환한 exact `expected_head_sha`를 사용한다.

connector가 Branch·PR을 만들었다는 사실은 Required Checks, Branch protection, unresolved thread, mergeability 또는 release 성공의 증거가 아니다. 각 표면은 가능한 connector readback이나 실제 Actions 결과로 별도 검증한다.

## `CONCURRENT_CHANGE_PREFLIGHT`

```yaml
CONCURRENT_CHANGE_PREFLIGHT:
  current_task_or_pr_identity:
  source_main_sha:
  current_main_sha:
  write_parent_sha:
  expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
  intended_paths: []
  semantic_resource_locks: []
  same_goal_open_and_recent_prs: []
  open_pr_changed_paths: {}
  overlap_classification: NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
  disposition: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
  coordination_action:
```

- `CLEAR`: 필요한 증거를 실제로 읽었고 `source_main_sha == current_main_sha`이며, 현재 작업 자신을 제외한 동일 Goal의 활성·대체 작업과 path/semantic writer 충돌이 없고 관찰한 Branch HEAD가 `write_parent_sha`와 일치한다.
- `STALE_BASE_SHA`: 기준을 고정한 뒤 main이 이동했다. 최신 main에 reconcile하고 영향 검증과 preflight를 다시 수행한다.
- `WAITING_RESOURCE`: 다른 활성 PR·Task가 겹치는 경로 또는 의미 자원을 소유한다. 비중첩 경로로 축소하거나 소유 PR에서 조정·인계하고, 해제 전에는 경쟁 write를 만들지 않는다.
- `DUPLICATE_WORK`: 현재 작업 자신이 아닌 다른 열린·최근 대체 PR이 같은 Goal과 기대 결과를 이미 소유한다. 새 구현을 만들지 않고 기존 작업을 검토·보완한다.
- `BLOCKED_UNVERIFIED`: main, Branch head, current identity, PR, changed-path, semantic ownership, policy 또는 exact-head 증거를 읽지 못했다. 이 상태를 `CLEAR`로 낮추지 않는다.

`PATH_OVERLAP`은 텍스트 merge conflict가 확정됐다는 뜻이 아니다. 반대로 파일이 달라도 같은 정본·Schema·생성물·save/runtime·Scene·자산 계열을 바꾸면 `SEMANTIC_OVERLAP`일 수 있다. overlap 분류 뒤 실제 소유권·source/derivative 관계·의도한 변경 범위를 검증해 disposition을 정한다.

preflight는 첫 persistent write 전, 각 후속 write의 parent 확인 전, 최종 `intended_paths`가 확정된 PR 생성 전, exact reviewed HEAD 병합 전, main·열린 PR·resource owner가 바뀐 뒤에 다시 실행한다. merge 뒤에는 새 main을 read back하고 같은 Goal의 PR·정본·소비자 상태를 재검사한다.

## Rules

- `DIRTY`: 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
- `REMOTE_AHEAD`: fast-forward 가능할 때만 자동 갱신한다.
- `LOCAL_AHEAD`: diff·검증·커밋 범위를 확인한 뒤 push·PR한다.
- `DIVERGED`: 자동 force push·hard reset을 금지하고 병합·rebase·새 branch 중 하나를 명시적으로 선택한다.
- `STALE_BASE_SHA`, `WAITING_RESOURCE`, `DUPLICATE_WORK`, `BLOCKED_UNVERIFIED`에서는 persistent write·새 경쟁 PR·merge를 자동 진행하지 않는다.
- 실제 작업 Branch HEAD가 `write_parent_sha`와 다르면 concurrent branch update로 보고 write를 중단한다.
- same-goal·path 목록에 현재 Task/PR 자신을 포함해 self-conflict를 만들지 않는다.
- path가 비중첩이어도 semantic resource가 같으면 동시 writer를 허용하지 않는다.
- 비밀·대용량 생성물·승인되지 않은 파일은 자동 커밋하지 않는다.
- 기존 PR에 조정 comment를 남기거나 명시적 handoff를 받았다는 사실과 실제 resource 해제는 구분한다.
- Required Checks 통과는 정확한 `expected_head_sha`와 현재 main에 대한 freshness를 함께 확인할 때만 병합 증거로 사용한다.
- `MISSING_OPTIONAL_CLI`를 전체 권한 부재로 확대하거나 connector coverage 확인 전에 사용자 재인증을 요구하지 않는다.

## Output contract

```md
## 로컬·원격 HEAD와 상태
## CONCURRENT_CHANGE_PREFLIGHT 증거·분류·disposition
## current task/PR identity·write parent·exact expected HEAD
## 동일 Goal PR·경로 중첩·semantic resource와 조정 결과
## 차이 파일·커밋·미추적 항목
## 선택한 reconcile 방식과 이유
## github_connector / local_git / gh_cli capability 판정과 fallback
## 수행한 fetch/pull/commit/push/PR
## exact HEAD·Required Checks·최종 동등성
## post-merge main readback·같은 Goal 재검사
## 충돌·권한·미검증·사용자 조치
```

## Quality gate

로컬 작업 유실, 무검토 자동 커밋, force push, 인증 실패 은폐, optional `gh` 부재를 connector 확인 없이 전역 blocker로 처리, connector coverage가 있는데 반복 인증 요구, pull 성공을 기능 검증으로 오인, 열린 PR·changed paths를 보지 않고 `CLEAR` 판정, 현재 PR을 자기 중복으로 판정, stale `write_parent_sha` 위에 write, path만 보고 semantic 충돌을 무시, stale base 또는 다른 HEAD의 CI를 병합 증거로 사용하면 실패다.

Canonical Learning Log: `skills/SKILL_LEARNING_LOG.md`

Change Learning Record: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
