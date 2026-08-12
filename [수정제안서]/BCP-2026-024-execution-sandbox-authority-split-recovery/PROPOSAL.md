# BCP-2026-024-execution-sandbox-authority-split-recovery — Execution Sandbox Remote-Authority Split Recovery

## 출처와 상태

```yaml
proposal_id: BCP-2026-024-execution-sandbox-authority-split-recovery
status: SUBMITTED
knowledge_state: PATTERN
source_project: alsdmlals4-eng/GRIMOIRE-
source_commit: d277a2f5cd4a57947d176e3c49ae7f8f6db97230
source_project_pr: https://github.com/alsdmlals4-eng/GRIMOIRE-/pull/134
learning_id: LRN-GR-20260812-01
submitted_at: 2026-08-12
existing_solution_verdict: ABSORB
proposal_storage_merge_authority: GRANTED_BY_CURRENT_HANDOFF_INSTRUCTION
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
approval_ref: null
implementation_pr: null
```

Project Application은 완료되었다. GRIMOIRE PR #134에서 `GR-SYNC-20260812-21-TASK8-HANDOFF-BCP`, 기존 continuation owner, focused current-state regression에 remote/local receipt 분리를 반영했고 exact reviewed head `71d0a814043275b9453c9bdb218eac1be9ae31fa`의 적용 가능한 CI를 통과했다. 일시적 external HTTP 525였던 Star Runtime POC도 동일 exact head 재실행에서 성공한 뒤 `d277a2f5cd4a57947d176e3c49ae7f8f6db97230`으로 병합·new-main readback했다.

동시성 provenance도 보존한다. GRIMOIRE proposal PR #293/#295/#296은 각각 final race에서 ID 충돌 또는 Base advancement를 발견해 미병합 종료했다. 다른 프로젝트 branch/PR/Registry entry를 수정하지 않고, 최신 Base main `be2435bc5ebb9f55c49c0b37284a122a3689e583`의 BCP-021/022를 그대로 보존한 뒤 이 제안만 BCP-024로 재구성했다.

### 충돌 복원 감사

- PR #293의 초기 BCP-022에는 `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`과 일시적 external HTTP 525 뒤 동일 exact-head Star Runtime POC 재성공 기록이 모두 있었다.
- PR #295의 BCP-023과 PR #296의 BCP-024에는 Decision ID가 남았지만 HTTP 525/Star Runtime 기록은 이미 빠져 있었다.
- PR #297의 최종 BCP-024에서는 Decision ID도 빠졌다.
- 현재 수정은 이 서로 다른 두 손실 시점을 명시하고 provenance만 복원한다. BCP-024의 active Base 구현 승인이나 구현 상태를 변경하지 않는다.

## 관찰과 증거

GRIMOIRE Task8 PR-prep에서 실행 채널별 capability가 달랐다.

1. dedicated Codex sandbox는 exact linked worktree/branch/HEAD와 cached diff를 읽을 수 있었다.
2. 같은 sandbox의 `git fetch origin main`은 `.git/worktrees/task8-spell-use-screen-v2/FETCH_HEAD` 쓰기에서 `Permission denied`로 실패했다.
3. `git ls-remote origin refs/heads/main`도 `github.com:443` 연결 실패로 종료되었다.
4. 별도 GitHub connector는 같은 work unit에서 GRIMOIRE/Base의 exact `main`과 open PR을 fresh-read할 수 있었다.
5. 실패한 Codex 시도는 source edit, stage, commit, push, reset, restore, clean, rebase, amend를 하지 않았다.
6. 프로젝트는 이 차이를 `REMOTE_AUTHORITY_RECEIPT + LOCAL_EXECUTION_RECEIPT`로 분리하고 executor capability failure를 product failure와 구분하는 continuation contract를 실제 적용·검증·병합했다.

### Root Cause

remote repository freshness와 local executor readiness를 **한 executor의 동일 Git/network capability 성공**으로 묶은 것이 원인이다. 실행 채널은 working-tree read, linked-worktree administrative metadata write, outbound network, credentials, control-plane connector capability를 서로 다르게 가질 수 있다.

공식 Git `git-worktree` 문서는 linked worktree가 `$GIT_DIR/worktrees/<id>` 아래 private administrative directory와 `$GIT_COMMON_DIR`의 common repository state를 사용한다고 설명한다. 따라서 working-tree read가 administrative metadata write까지 자동으로 증명하지 않는다.

공식 GitHub required-status-check 문서는 현재 validation commit identity와 freshness를 중요하게 다룬다. 본 제안의 receipt split 명칭은 Git/GitHub가 규정한 API가 아니라, exact identity/freshness를 유지하면서 서로 다른 trusted capability channel을 결합해야 했던 프로젝트 증거에서 도출한 inference다.

Benchmark:
- https://git-scm.com/docs/git-worktree
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

### Existing Base Coverage

현재 Base는 이미 다음 주변 책임을 가진다.

- `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`: exact local identity와 fail-closed startup.
- `BCP-2026-015-external-runtime-session-same-snapshot-recovery`: stale process/transport/session/registry locator recovery.
- continuation/handoff 및 validation owners: stale state/old-head evidence의 current 승격 금지.
- PR validation identity: current required check target freshness 구분.

그러나 local executor가 remote network/shared Git metadata capability를 잃었을 때 별도 trusted connector가 remote repository freshness를 공급하고 local exact state/test receipt를 독립적으로 유지하는 공용 fallback contract는 current Base에서 확인되지 않았다.

## 일반화 후보

### Proposed General Principle

remote repository truth와 local executor truth가 모두 필요한 작업에서 receipt producer가 반드시 같을 필요는 없지만 authority, exact identity, freshness, capability boundary는 각각 증명해야 한다.

```text
REMOTE_AUTHORITY_RECEIPT
  trusted source/tool
  repository + ref + exact remote SHA
  same-goal/open-PR snapshot when relevant
  observed-at/freshness boundary

+

LOCAL_EXECUTION_RECEIPT
  exact repository/worktree + branch + HEAD
  cached/staged state
  required local tool/session readiness
  current local tests/QA when required

+

EXECUTOR_CAPABILITY_BLOCKER
  blocked operation
  denied capability
  sanitized original failure payload
  retry/disposition

→ CURRENT_TASK_RESUME_DECISION
```

Rules:
1. local executor의 remote-query 실패만으로 project/remote failure를 선언하지 않는다.
2. alternate remote receipt는 approved trusted channel이며 repository/ref/exact SHA/freshness를 식별해야 한다.
3. remote receipt는 local worktree/HEAD/staged/test/tool receipt를 대체하지 않는다.
4. remote read capability를 local stage/commit/push/shared-metadata write 권한으로 확대하지 않는다.
5. 이미 같은 work unit에서 정확히 분류된 capability failure를 의례적으로 반복해 independent local verification을 계속 막지 않는다.
6. remote write/PR/merge/shared Registry 변경 직전 latest main/open PR/race state를 write-capable trusted channel에서 다시 읽는다.
7. main/ref/PR/head 이동 또는 work-unit 전환 시 이전 receipt의 current freshness를 폐기한다.
8. alternate trusted channel이 없으면 `BLOCKED_UNVERIFIED`를 유지한다.

### Existing Solution Verdict

`ABSORB`.

새 broad Skill을 만들거나 BCP-015의 runtime-session 책임을 과도하게 넓히기보다 기존 intake/continuation/local-execution/verification owner의 recovery reference와 tests에 최소 흡수하는 후보가 적절하다. 이번 단계에서는 active Base 구현을 하지 않는다.

## 프로젝트 전용으로 남길 내용

Base에 올리지 않는 GRIMOIRE 전용 값:
- Task8 worktree/branch/head와 exact 9-path product allowlist.
- Godot 4.7.1, HiGodot 3.1.4, Hera 1.0.0, GUT 9.7.1, project-scoped ports/CODEX_HOME/Hera profile.
- Task8 GUT/Hera counts, acceptance evidence ceilings, Stage3/gameplay authority.
- `GM-SPELL-WORKFLOW-UI-V2-01`, `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`.
- 사용자 workflow preference `CURRENT_DEDICATED_CODEX_REUSE_ALLOWED_FOR_CODEX_ONLY_CONTINUATION`.

모든 프로젝트가 connector와 local executor를 동시에 갖는다고 가정하지 않는다.

## 적용 조건과 비사용 조건

### Use When
- remote authority freshness와 local execution evidence가 모두 필요하다.
- local executor는 local worktree/tests를 다룰 수 있지만 remote network/shared Git metadata 등 일부 capability가 막힌다.
- blocked operation과 sanitized original failure가 보존되어 있다.
- 다른 approved trusted channel이 exact remote repository/ref/SHA를 fresh-read할 수 있다.
- local mutation/validation은 별도 local receipt로 검증한다.
- remote write 직전 final freshness/race recheck가 가능하다.

### Do Not Use When
- local branch/HEAD/worktree 자체가 기대 identity와 다르다.
- compile/test/parser/product failure가 실제 발생했다.
- trusted remote sources끼리 state가 불일치한다.
- alternate source가 오래된 handoff/log/search snippet/추론뿐이다.
- required remote write와 final race check를 수행할 approved capable channel이 없다.
- security/credential incident를 capability blocker로 숨기려 한다.

## 반례와 위험

### Counterexamples
1. remote main이 정확해도 local HEAD mismatch는 local failure다.
2. local GUT/compile failure는 remote receipt로 우회할 수 없다.
3. connector read 뒤 main/open PR이 이동하면 이전 receipt로 merge할 수 없다.
4. sandbox가 commit/push/shared Registry write를 못 하면 read receipt가 write capability를 대신하지 않는다.
5. untrusted web snippet/기억된 SHA는 authoritative remote receipt가 아니다.
6. shared proposal namespace는 branch creation receipt가 있어도 final race check가 필요하다. 본 작업 자체가 여러 race를 발견해 다른 project delta를 보존한 실증 사례다.

### Risks
- receipt identity/freshness 누락 시 split-brain.
- capability blocker 남용 시 실제 Git/network/config defect의 영구 우회.
- remote connector read를 local mutation 승인으로 오인.
- 과거 live tool/session evidence를 current readiness로 승격.
- existing owner 대신 새 broad Skill/문서를 만들 경우 책임 중복.

Mitigation: fail-closed alternate-source absence, exact identity, freshness invalidation, explicit capability classification, Existing Solution First `ABSORB`, remote-write final race check.

## 영향 범위와 검증

### Future implementation candidate consumers
별도 구현 승인 시 먼저 평가할 기존 owner:
- project intake / continuous-work recovery reference
- maintaining project context and handoff
- project-dedicated local executor continuation/bootstrap reference
- reviewing/validating project changes
- canonical/reference freshness and exact validation identity tests
- 실제 routing 영향이 있을 때만 Registry/generated consumer

### Validation Plan
1. 한 executor가 모든 capability를 보유한 정상 경로 — 추가 split ceremony 없음.
2. local remote-read만 막히고 trusted connector가 fresh exact SHA 제공 — independent local checks 지속.
3. shared-Git-metadata write 차단 — remote receipt가 stage/commit/push 권한으로 확대되지 않음.
4. alternate source stale/ambiguous — `BLOCKED_UNVERIFIED`.
5. local HEAD mismatch/test failure — remote receipt가 실패를 덮지 않음.
6. remote main/open PR이 write 직전 변경 — stale receipt 폐기 + race recheck.
7. Registry ID collision — 다른 project delta를 수정하지 않고 own proposal만 reassign/rebuild.
8. non-selection — 모든 capability가 정상인 executor에는 recovery flow를 강제하지 않음.

### Regression Plan
- dedicated-local fail-closed semantics 유지.
- BCP-015 runtime-session recovery 유지.
- continuous-work blocker taxonomy와 충돌하지 않음.
- exact CI validation identity freshness 유지.
- proposal-only storage/implementation approval boundary 유지.

### Rollback
proposal-only 문서/Registry만 추가하므로 문제가 있으면 proposal merge revert 또는 lifecycle reject/supersede가 가능하고 active Base behavior는 즉시 바뀌지 않는다.

## 필요한 도구·파일·권한

필요:
- current Base main/Registry/open proposal PR read access
- proposal README/template/validator
- source project PR/new-main evidence
- `[수정제안서]/**` proposal-only write/PR/merge 권한

금지:
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

proposal-only 저장·병합은 Base 활성 구현 승인이 아니다. 구현은 별도 사용자 승인·별도 후속 단계에서만 수행한다.
