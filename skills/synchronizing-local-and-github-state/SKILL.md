---
name: synchronizing-local-and-github-state
description: Use when a local checkout and its GitHub branch must be compared, safely reconciled, refreshed, published, or verified as equivalent without overwriting uncommitted work, secrets, divergent history, or unreviewed changes.
---

# Synchronizing Local and GitHub State

## Core principle

동기화는 무조건 pull·commit·push하는 자동화가 아니다. 먼저 양쪽 상태와 권한을 판정하고, **clean + fast-forward + 승인된 변경**일 때만 자동 진행한다.

이 Skill은 Git 상태의 동등성과 안전한 전달만 책임진다. 변경 내용의 품질·완료 여부는 `reviewing-and-validating-project-changes`, PR 제안·승인 정책은 `managing-base-change-proposals`, 장기 실행 checkpoint는 `maintaining-long-running-task-continuity`가 책임진다.

## Modes and states

`inspect` → `reconcile` → `refresh-local | publish-remote` → `verify-sync`

`SYNCED / DIRTY / LOCAL_AHEAD / REMOTE_AHEAD / DIVERGED / BLOCKED`

## Required inputs

```yaml
repository_and_remote:
local_branch_head_and_status:
remote_branch_head:
uncommitted_and_untracked_files:
upstream_and_branch_policy:
credentials_permissions_and_required_checks:
allowed_generated_files_and_secrets_policy:
```

안전한 명령·충돌 절차는 `references/safe-sync-protocol.md`를 필요할 때만 읽는다.

## Rules

- `DIRTY`: 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
- `REMOTE_AHEAD`: fast-forward 가능할 때만 자동 갱신한다.
- `LOCAL_AHEAD`: diff·검증·커밋 범위를 확인한 뒤 push·PR한다.
- `DIVERGED`: 자동 force push·hard reset을 금지하고 병합·rebase·새 branch 중 하나를 명시적으로 선택한다.
- 비밀·대용량 생성물·승인되지 않은 파일은 자동 커밋하지 않는다.

## Output contract

```md
## 로컬·원격 HEAD와 상태
## 차이 파일·커밋·미추적 항목
## 선택한 reconcile 방식과 이유
## 수행한 fetch/pull/commit/push/PR
## 검증·Required Checks·최종 동등성
## 충돌·권한·미검증·사용자 조치
```

## Quality gate

로컬 작업 유실, 무검토 자동 커밋, force push, 인증 실패 은폐, pull 성공을 기능 검증으로 오인하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
