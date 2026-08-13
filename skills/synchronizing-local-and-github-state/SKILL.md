---
name: synchronizing-local-and-github-state
description: Use when local and GitHub state must be compared, reconciled, refreshed, published, or verified without overwriting work or divergent history.
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
```

첫 persistent write, PR 생성 또는 merge를 수행할 때 추가로 필요한 입력:

```yaml
source_main_sha:
current_main_sha:
expected_head_sha:
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
open_pr_changed_paths: {}
protected_concurrent_paths: []
```

`source_main_sha`는 조사·분기 기준, `current_main_sha`는 판정 시점의 실제 기본 Branch, `expected_head_sha`는 검토·검사·병합하려는 정확한 변경 HEAD다. 열린 PR 목록, changed paths, 현재 main 또는 권한 정책을 읽지 못하면 충돌 없음으로 추정하지 않는다.

안전한 명령·충돌·조정 절차는 `references/safe-sync-protocol.md`를 필요할 때만 읽는다.

## `CONCURRENT_CHANGE_PREFLIGHT`

```yaml
CONCURRENT_CHANGE_PREFLIGHT:
  source_main_sha:
  current_main_sha:
  expected_head_sha:
  intended_paths: []
  semantic_resource_locks: []
  same_goal_open_and_recent_prs: []
  open_pr_changed_paths: {}
  overlap_classification: NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
  disposition: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
  coordination_action:
```

- `CLEAR`: 필요한 증거를 실제로 읽었고 `source_main_sha == current_main_sha`이며, 동일 Goal의 활성·대체 작업과 path/semantic writer 충돌이 없다.
- `STALE_BASE_SHA`: 기준을 고정한 뒤 main이 이동했다. 최신 main에 reconcile하고 영향 검증과 preflight를 다시 수행한다.
- `WAITING_RESOURCE`: 다른 활성 PR·Task가 겹치는 경로 또는 의미 자원을 소유한다. 비중첩 경로로 축소하거나 소유 PR에서 조정·인계하고, 해제 전에는 경쟁 write를 만들지 않는다.
- `DUPLICATE_WORK`: 같은 Goal과 기대 결과를 다른 열린·최근 대체 PR이 이미 소유한다. 새 구현을 만들지 않고 기존 작업을 검토·보완한다.
- `BLOCKED_UNVERIFIED`: main, PR, changed-path, semantic ownership, policy 또는 exact-head 증거를 읽지 못했다. 이 상태를 `CLEAR`로 낮추지 않는다.

`PATH_OVERLAP`은 텍스트 merge conflict가 확정됐다는 뜻이 아니다. 반대로 파일이 달라도 같은 정본·Schema·생성물·save/runtime·Scene·자산 계열을 바꾸면 `SEMANTIC_OVERLAP`일 수 있다. overlap 분류 뒤 실제 소유권·source/derivative 관계·의도한 변경 범위를 검증해 disposition을 정한다.

preflight는 첫 persistent write 전, 최종 `intended_paths`가 확정된 PR 생성 전, exact reviewed HEAD 병합 전, main·열린 PR·resource owner가 바뀐 뒤에 다시 실행한다. merge 뒤에는 새 main을 read back하고 같은 Goal의 PR·정본·소비자 상태를 재검사한다.

## Rules

- `DIRTY`: 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
- `REMOTE_AHEAD`: fast-forward 가능할 때만 자동 갱신한다.
- `LOCAL_AHEAD`: diff·검증·커밋 범위를 확인한 뒤 push·PR한다.
- `DIVERGED`: 자동 force push·hard reset을 금지하고 병합·rebase·새 branch 중 하나를 명시적으로 선택한다.
- `STALE_BASE_SHA`, `WAITING_RESOURCE`, `DUPLICATE_WORK`, `BLOCKED_UNVERIFIED`에서는 persistent write·새 경쟁 PR·merge를 자동 진행하지 않는다.
- path가 비중첩이어도 semantic resource가 같으면 동시 writer를 허용하지 않는다.
- 비밀·대용량 생성물·승인되지 않은 파일은 자동 커밋하지 않는다.
- 기존 PR에 조정 comment를 남기거나 명시적 handoff를 받았다는 사실과 실제 resource 해제는 구분한다.
- Required Checks 통과는 정확한 `expected_head_sha`와 현재 main에 대한 freshness를 함께 확인할 때만 병합 증거로 사용한다.

## Output contract

```md
## 로컬·원격 HEAD와 상태
## CONCURRENT_CHANGE_PREFLIGHT 증거·분류·disposition
## 동일 Goal PR·경로 중첩·semantic resource와 조정 결과
## 차이 파일·커밋·미추적 항목
## 선택한 reconcile 방식과 이유
## 수행한 fetch/pull/commit/push/PR
## exact HEAD·Required Checks·최종 동등성
## post-merge main readback·같은 Goal 재검사
## 충돌·권한·미검증·사용자 조치
```

## Quality gate

로컬 작업 유실, 무검토 자동 커밋, force push, 인증 실패 은폐, pull 성공을 기능 검증으로 오인, 열린 PR·changed paths를 보지 않고 `CLEAR` 판정, path만 보고 semantic 충돌을 무시, stale base 또는 다른 HEAD의 CI를 병합 증거로 사용하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
