# BCP-2026-024-execution-sandbox-authority-split-recovery — Execution Sandbox Remote-Authority Split Recovery

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/GRIMOIRE-`
- 기준 커밋: `d277a2f5cd4a57947d176e3c49ae7f8f6db97230`
- 관련 프로젝트 PR: `https://github.com/alsdmlals4-eng/GRIMOIRE-/pull/134`
- 관련 Decision: `GM-SPELL-WORKFLOW-UI-V2-01`, `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`
- Learning ID: `LRN-GR-20260812-01`
- 제출일: `2026-08-12`
- 상태: `SUBMITTED`
- 지식 상태: `PATTERN`
- Project Application: `APPLIED` — `GR-SYNC-20260812-21-TASK8-HANDOFF-BCP`와 기존 continuation owner에 `REMOTE_AUTHORITY_RECEIPT + LOCAL_EXECUTION_RECEIPT` 분리를 반영하고 focused current-state regression을 연결했다.
- Project Verification: 프로젝트 PR #134 exact reviewed head `71d0a814043275b9453c9bdb218eac1be9ae31fa`의 적용 가능한 CI가 통과했고, PR은 `d277a2f5cd4a57947d176e3c49ae7f8f6db97230`으로 병합·new-main readback되었다.
- Existing Solution Verdict: `ABSORB`
- Base 구현 권한: `NOT_GRANTED_IN_THIS_STAGE`

동시성 기록: 최초 GRIMOIRE proposal #293은 slot 022, replacement #295는 slot 023을 사용했지만 각각 mandatory final race check에서 다른 프로젝트의 동시 할당을 확인했다. 두 PR 모두 미병합 종료했고 다른 프로젝트를 수정하지 않은 채 이 제안만 current Base main에서 현재 비어 있는 024로 재할당했다.

## 관찰과 증거

GRIMOIRE Task8 PR-prep에서 하나의 executor가 모든 필요한 authority channel을 동일하게 사용할 수 없다는 failure mode가 재현되었다.

1. dedicated Codex sandbox는 exact linked worktree/branch/HEAD와 cached diff를 읽을 수 있었다.
2. 같은 sandbox에서 `git fetch origin main`은 `.git/worktrees/task8-spell-use-screen-v2/FETCH_HEAD` 쓰기에서 `Permission denied`로 실패했다.
3. read-only 대안 `git ls-remote origin refs/heads/main`도 `github.com:443` 연결 실패로 종료되었다.
4. 반면 별도 GitHub connector는 같은 work unit에서 GRIMOIRE/Base의 exact `main`과 open PR을 fresh-read할 수 있었다.
5. 실패한 Codex 시도들은 source edit/stage/commit/push/reset/restore/clean/rebase/amend를 하지 않았다.
6. 프로젝트 PR #134는 이 차이를 remote authority와 local execution receipt로 분리하고 executor capability failure를 product failure와 분리하는 continuation contract를 적용·검증·병합했다.

### Root Cause

remote repository freshness와 local executor readiness를 한 executor의 동일 Git/network capability 성공 여부에 묶은 것이 원인이다. 실행 채널은 working-tree read, linked-worktree administrative metadata write, outbound network, credentials, control-plane connector 권한을 서로 다르게 가질 수 있다.

공식 Git `git-worktree` 문서는 linked worktree가 repository `$GIT_DIR/worktrees/<id>` 아래 private administrative directory를 사용하고 `$GIT_COMMON_DIR`로 common repository state를 참조한다고 설명한다. 따라서 working tree read capability가 administrative metadata write capability까지 자동으로 증명하지 않는다.

공식 GitHub required-status-check 문서는 현재 validation commit identity가 중요하며 head와 test-merge/merge-queue identity를 구분해야 한다고 설명한다. 이 제안의 receipt split 명칭은 Git/GitHub 규정이 아니라 exact identity/freshness를 유지하면서 다른 trusted capability channel을 결합해야 했던 프로젝트 증거에서 도출한 inference다.

공식 benchmark:

- https://git-scm.com/docs/git-worktree
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

### Existing Base Coverage

현재 Base에는 주변 책임이 이미 존재한다.

- `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`: exact local project/worktree/environment identity와 fail-closed startup.
- `BCP-2026-015-external-runtime-session-same-snapshot-recovery`: process/transport/session/registry stale locator recovery.
- continuation/handoff 및 validation owners: stale state와 old-head evidence의 current 승격 금지.
- current PR validation identity: required check의 current validation target freshness 구분.

그러나 current Base에서 local executor가 remote network/shared Git metadata capability를 잃었을 때 별도 trusted connector가 remote repository freshness를 공급하고, local exact state/test receipt는 독립적으로 유지하는 fallback contract는 확인되지 않았다.

### Existing Solution Verdict

`ABSORB`

BCP-015의 runtime-session 책임을 넓혀 repository authority split까지 합치거나 새 broad Skill을 만드는 것보다 기존 intake/continuation/local-execution/verification owner의 recovery reference와 tests에 최소 흡수하는 후보가 적절하다.

## 일반화 후보

remote repository truth와 local executor truth가 모두 필요한 작업에서 receipt producer가 반드시 같을 필요는 없지만 identity·freshness·capability 경계는 각각 증명해야 한다.

```text
REMOTE_AUTHORITY_RECEIPT
  trusted source/tool
  repository + ref
  exact remote SHA
  same-goal/open-PR snapshot when relevant
  observation/freshness boundary

+

LOCAL_EXECUTION_RECEIPT
  exact local repository/worktree
  branch + HEAD
  cached/staged state
  required local tool/session readiness
  current tests/QA where required

+

EXECUTOR_CAPABILITY_BLOCKER
  blocked operation
  denied capability
  original sanitized failure payload
  retry/disposition

→ CURRENT_TASK_RESUME_DECISION
```

공용 후보 규칙:

1. local executor의 remote-query 실패만으로 remote repository/product failure를 선언하지 않는다.
2. alternate remote receipt는 approved trusted channel이며 repository/ref/exact SHA/freshness가 식별 가능해야 한다.
3. remote receipt는 local worktree/HEAD/staged/test/tool readiness를 대체하지 않는다.
4. remote read capability는 local stage/commit/push/shared-metadata write 권한으로 확대되지 않는다.
5. 동일 capability failure를 의례적으로 반복해 independent local verification을 계속 막지 않는다.
6. remote write/PR/merge/shared Registry 변경 직전에는 write-capable trusted channel에서 latest main/open PR/race state를 다시 읽는다.
7. main/ref/PR/head 이동 또는 work-unit 전환 시 이전 receipt의 current freshness를 폐기한다.
8. alternate trusted channel이 없으면 `BLOCKED_UNVERIFIED`를 유지한다.

## 프로젝트 전용으로 남길 내용

- GRIMOIRE Task8 local worktree 경로, branch/head, 9-path allowlist.
- HiGodot/Hera/GUT/Godot exact versions, ports, project-scoped `CODEX_HOME`/Hera profile.
- `GM-SPELL-WORKFLOW-UI-V2-01` gameplay/Stage3 authority.
- Task8 GUT/Hera acceptance counts와 evidence ceilings.
- 사용자의 `CURRENT_DEDICATED_CODEX_REUSE_ALLOWED_FOR_CODEX_ONLY_CONTINUATION` workflow preference.

모든 프로젝트가 connector와 local executor를 동시에 갖는다고 가정하지 않는다.

## 적용 조건과 비사용 조건

### Use When

- current task가 remote authority freshness와 local execution evidence를 모두 요구한다.
- local executor가 local worktree/tests를 다룰 수 있지만 remote network/shared Git metadata 등 일부 capability가 막힌다.
- blocked operation과 sanitized original failure가 보존되어 있다.
- 다른 approved trusted channel이 exact remote repository/ref/SHA를 fresh-read할 수 있다.
- local mutation/validation은 별도 local receipt로 계속 검증한다.
- remote write 직전 final freshness/race recheck가 가능하다.

### Do Not Use When

- local branch/HEAD/worktree 자체가 기대 identity와 다르다.
- compile/test/parser/product failure가 실제 발생했다.
- trusted remote sources끼리 repository state가 불일치한다.
- alternate source가 오래된 handoff/log/search snippet/추론뿐이다.
- required remote write와 final race check를 수행할 approved capable channel이 없다.
- security/credential incident를 단순 capability blocker로 숨기려 한다.

## 반례와 위험

### Counterexamples

1. external connector가 remote main을 정확히 읽어도 local HEAD mismatch는 local failure다.
2. local GUT/compile failure는 remote receipt로 우회할 수 없다.
3. connector read 뒤 main/open PR이 이동하면 이전 receipt로 merge할 수 없다.
4. commit/push/shared Registry mutation이 sandbox에서 불가능하면 read receipt가 write capability를 대신하지 않는다.
5. untrusted web snippet/기억된 SHA는 authoritative receipt가 아니다.
6. shared proposal namespace는 branch creation receipt가 있어도 final race check가 필요하다. 실제로 본 작업은 022와 023 collision을 각각 발견하고 own proposal만 재할당했다.

### Risks

- receipt별 exact identity/freshness를 기록하지 않으면 split-brain이 생길 수 있다.
- capability blocker를 넓게 쓰면 실제 Git/network/config defect를 영구 우회할 수 있다.
- remote connector readback이 local mutation 승인으로 오인될 수 있다.
- 과거 live tool/session evidence가 current readiness로 잘못 승격될 수 있다.
- 기존 owner에 흡수하지 않으면 broad Skill/문서 중복이 생길 수 있다.

Mitigation은 fail-closed alternate-source absence, exact identity, freshness invalidation, explicit capability classification, Existing Solution First `ABSORB`, final remote-write race check다.

## 영향 범위와 검증

### Future implementation candidate consumers

별도 구현 승인이 주어질 경우 다음 기존 owner를 먼저 평가한다.

- project intake / continuous-work recovery reference
- maintaining project context and handoff
- project-dedicated local executor continuation/bootstrap reference
- reviewing/validating project changes
- canonical/reference freshness and exact validation identity tests
- 실제 routing 영향이 있을 때만 Registry/generated consumer 동기화

새 broad Skill 생성은 기본값이 아니다.

### Validation Plan

1. 단일 executor가 모든 capability를 가진 정상 경로 — 기존 route 유지.
2. local remote-read만 막히고 trusted connector가 fresh exact SHA 제공 — independent local checks 계속 가능.
3. shared-Git-metadata write가 막힘 — remote receipt가 stage/commit/push 권한으로 확대되지 않음.
4. alternate source stale/ambiguous — `BLOCKED_UNVERIFIED`.
5. local HEAD mismatch/test failure — remote receipt가 실패를 덮지 않음.
6. remote main/open PR이 write 직전에 변경 — stale receipt 폐기, current race recheck.
7. shared Registry ID collision — 다른 project delta를 수정하지 않고 own proposal만 재할당/rebuild.
8. non-selection — 모든 required capability가 정상인 executor에는 split recovery를 강제하지 않음.

### Regression Plan

- project-dedicated local execution fail-closed semantics 유지.
- BCP-015 runtime-session recovery semantics 유지.
- continuous-work blocker taxonomy와 충돌하지 않음.
- exact CI validation identity freshness 유지.
- proposal-only storage와 implementation approval boundary 유지.

### Rollback

이번 단계는 `[수정제안서]/**` proposal/Registry만 추가한다. 문제 발견 시 proposal-only merge를 revert하거나 lifecycle에서 reject/supersede할 수 있으며 active Base behavior는 바뀌지 않는다.

## 필요한 도구·파일·권한

필요:

- current Base main/Registry/open proposal PR read access
- `[수정제안서]/README.md`, Registry, proposal template, validator
- source project PR #134/new-main readback
- `[수정제안서]/**` proposal-only write/PR/merge 권한

금지/불필요:

- Base active `skills/**`, `docs/**`, `templates/**`, `tools/**`, `tests/**`, workflows, `AGENTS.md`, `START_HERE.md` 수정
- GRIMOIRE product mutation
- 다른 project proposal branch/Registry entry 수정

## 승인과 구현

```yaml
proposal_status: SUBMITTED
proposal_storage_merge_authority: GRANTED_BY_CURRENT_HANDOFF_INSTRUCTION
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
implementation_status: NOT_STARTED_IN_THIS_STAGE
approval_ref: null
implementation_pr: null
implementation_boundary: SEPARATE_FOLLOWUP_STAGE
```

proposal-only 저장·병합은 Base 활성 구현 승인이 아니다. 추후 구현은 별도 사용자 승인·별도 구현 단계에서만 수행한다.
