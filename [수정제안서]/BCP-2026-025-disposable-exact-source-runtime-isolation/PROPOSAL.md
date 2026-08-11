# BCP - OMENWARD: Disposable Exact-Source Runtime Isolation

## 출처와 상태

- Proposal ID: `BCP-2026-025-disposable-exact-source-runtime-isolation`
- 사용자 표시명: `BCP - OMENWARD: Disposable Exact-Source Runtime Isolation`
- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 기준 커밋: `b51bb29471ab802c6241d72a9af1226209934887`
- 출처 Project PR: `https://github.com/alsdmlals4-eng/omenward/pull/196`
- 관련 runtime PR: `https://github.com/alsdmlals4-eng/omenward/pull/175`
- 관련 Decision: `OMW-DEC-20260809-PLANNING-BARRACKS-ROLE-OUTPUT-RUNTIME-IMPLEMENTATION-PACKAGE-V1`
- 제출일: `2026-08-12`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- Existing Solution Verdict: `ABSORB`
- Project Application: `APPLIED_AND_MERGED_BY_OMENWARD_PR_196`
- Base active implementation authority: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 runtime/project startup crash를 조사할 때 **active checkout의 cache·미커밋 delta·sandbox 제약과 committed source 자체를 분리하고, trusted exact source identity를 disposable clean project로 materialize한 뒤 import/boot/script 등 가장 이른 실제 실패 boundary를 먼저 확정하고 독립 one-variable variant로 root cause를 좁히는 공용 진단 계약**을 제안한다.

이번 단계는 proposal storage만 수행한다. Base 활성 Skill, Registry, Template, Test, Tool, Workflow, Docs 또는 project runtime implementation은 변경하지 않는다.

## 관찰과 증거

OMENWARD Issue #176 runtime 구현은 먼저 genuine semantic GUT RED를 요구했다. 그러나 승인된 single-file GUT entrypoint와 별도 headless runtime script에서 Windows exit `-1073741819` / signal 11이 test discovery보다 먼저 발생했다.

처음에는 GUT 자체, local test delta, active `.godot` cache, Godot-AI runtime helper 등 여러 후보가 섞여 있었다. active project에 fix를 적용하지 않고 source identity와 derived state를 분리한 진단을 수행했다.

### Project application evidence

OMENWARD PR #196은 현재 blocker와 재개 절차를 기존 current-state owner에 반영하고, Handoff를 v4.5 current-consumer fail-closed surface에 포함했다.

- source project new main: `b51bb29471ab802c6241d72a9af1226209934887`
- source project closure PR: `#196`
- source project exact closure head: `7dd5658b535c71746d3ae046ee74b9f40ff1151d`
- exact-head triggered workflows: `12 SUCCESS / 0 FAILURE`
- unresolved review threads: `0`
- product/Godot/GDScript/GUT runtime source changed by PR #196: `0`

### Runtime isolation evidence

The project diagnostic used the exact committed PR #175 source identity and disposable TEMP state.

1. An exact-head archive was materialized outside the active project.
2. The disposable project initially contained no `.git` and no `.godot`.
3. Fresh Godot `--import` completed without signal-11 crash markers and generated fresh derived `.godot` state.
4. A subsequent normal headless project boot crashed with exit `-1073741819` and signal-11 markers.
5. The user's active local `.godot` state was therefore not required for the earliest reproduced crash.
6. The user's uncommitted two-test delta was not present in the exact committed archive, so it was not required for the earliest reproduced crash.
7. Active project tracked source was unchanged by the diagnostic.
8. The next diagnostic was reduced to independent disposable autoload A/B variants rather than an active-project fix.

Current project classification at handoff:

```text
CANONICAL_EXACT_HEAD_PROJECT_BOOT_BOUNDARY
```

The diagnostic did **not** prove which autoload or startup component is the root cause. It proved a narrower, reusable investigation boundary.

### Failed or misleading approaches observed

- Treating a GUT crash as proof that GUT itself is the root cause before testing normal project boot.
- Reusing one active checkout/cache for every probe, which leaves source identity and derived state confounded.
- Attempting `git worktree` inside an execution sandbox whose `.git/worktrees` metadata write is forbidden, then misclassifying that preparation failure as a Godot failure.
- Jumping directly from a plausible autoload suspicion to an active-source fix before a one-variable runtime matrix exists.
- Treating `--import` success as equivalent to normal game boot success.

## 일반화 후보

### Disposable Exact-Source Runtime Isolation Contract

For a runtime/startup failure whose source is not yet isolated:

```text
FRESH_AUTHORITY
→ TRUSTED_EXACT_SOURCE_IDENTITY
→ DISPOSABLE_COMMITTED_TREE_MATERIALIZATION
→ VERIFY_ARCHIVE_OR_MATERIALIZATION_COMPLETENESS
→ FRESH_DERIVED_STATE
→ EARLIEST_RUNTIME_BOUNDARY_MATRIX
→ INDEPENDENT_ONE_VARIABLE_VARIANTS
→ ROOT_CAUSE_CLASSIFICATION
→ ONLY_THEN_ACTIVE_FIX
```

### 1. Fresh authority

Before diagnosis, identify the exact repository/project, current source commit, executable/tool version, and current execution target. Historical PID/session/process identifiers remain evidence only.

### 2. Trusted exact source identity

The diagnostic clean project must derive from an explicit commit/tree identity rather than from a possibly dirty active checkout.

The materialization method is implementation-specific. `git archive` is one suitable method when a clean committed tree is needed but Git metadata is not; clone/worktree/fixture packaging may be preferable when their metadata is required.

### 3. Materialization completeness gate

Before treating the disposable tree as equivalent source input, verify source-selection rules that can omit or rewrite files.

For Git archive, this includes at minimum `.gitattributes` `export-ignore` / `export-subst` behavior and required project-file presence.

```text
CLEAN_MATERIALIZATION
!= ASSUME_ARCHIVE_CONTAINS_EVERY_TRACKED_FILE
```

### 4. Fresh derived/cache state

Do not copy active generated/cache state into the clean variant unless that variable is intentionally under test. Let the tool regenerate derived state from the committed source identity.

### 5. Earliest runtime boundary matrix

Separate lifecycle gates instead of collapsing them into one Green/Red label. Examples include:

```text
materialization
→ import/dependency generation
→ normal project boot
→ script/test runner startup
→ test discovery
→ semantic test behavior
→ live QA
```

The earliest failing layer becomes the next investigation owner. A downstream failure must not be diagnosed until its prerequisites are Green.

### 6. Independent one-variable variants

When multiple startup components remain plausible, each A/B variant starts from an independent clean materialization of the same exact source identity and changes exactly one intended variable.

```text
SAME_BASE_SOURCE
+ FRESH_DERIVED_STATE
+ ONE_CHANGED_VARIABLE
= INTERPRETABLE_VARIANT
```

Do not sequentially mutate one disposable tree for A/B if the first run can leave cache/generated/runtime state that contaminates the second result.

### 7. Preparation/tooling failure remains separate

A sandbox permission failure, archive failure, extraction failure, connector cancellation, or process-wrapper failure before the intended runtime probe actually runs is classified as an execution/evidence blocker, not as product/runtime failure.

### 8. Active fix gate

No active-source fix is justified solely by suspicion. The disposable evidence must first identify a component, interaction, or lower project-startup boundary with sufficient confidence for a minimal active fix/test.

## 프로젝트 전용으로 남길 내용

Base 공용 원칙으로 승격하지 않는다.

- OMENWARD PR #175/#196 and Issue #176 numbers
- OMENWARD Decision ID
- Godot 4.7.1-specific binary path
- HTTP 8002 / WS 9502
- `HeraGameInspector` and `_mcp_game_helper` names
- Windows exit `-1073741819` as an OMENWARD incident detail
- barracks role-output seven runtime gaps
- local GUT/FV fixture names and metrics
- current OMENWARD product parameters

These remain source evidence. The Base candidate is the source/cache/runtime-boundary isolation method, not the project-specific startup components.

## 적용 조건과 비사용 조건

### 적용 조건

- A runtime/test crash occurs before the expected semantic test or live-QA evidence can be collected.
- The active checkout may contain local changes, generated/cache state, or environment-specific artifacts.
- An exact committed source identity is available.
- The runtime can be launched against a disposable project copy without mutating the active source.
- Multiple plausible startup components can be disabled/substituted independently in disposable state.
- Sandbox or shared-editor constraints make active-repository experiments unnecessarily risky.

### 비사용 조건

- The failure is already deterministically reproduced by a focused test with a proven root cause.
- The bug specifically depends on uncommitted active working-tree state; in that case the clean committed-tree control is useful as a comparison, not a replacement for the active-state reproduction.
- The required runtime depends on Git metadata/submodules/LFS/filter outputs or secret/private assets that the chosen materialization method does not reproduce; use a suitable clean clone/worktree/fixture instead.
- The chosen archive has `export-ignore` or other transformation behavior that excludes a required runtime file and completeness cannot be proven.
- A disposable copy would violate licensing, secret-handling, large-asset, or environment constraints.
- Human QA requires the real integrated environment and the source/cache boundary is already proven healthy.

## 반례와 위험

### MUST_FIX — clean archive falsely treated as exact runtime source

`git archive` can exclude `export-ignore` paths and apply export substitutions. A clean archive is valid evidence only after archive-relevant attributes and required project files are checked.

### MUST_FIX — disposable PASS falsely clears active-environment bugs

A clean disposable project PASS only proves the committed-source/fresh-derived path. It does not prove that the active cache, local delta, machine configuration, external service, or live editor is healthy.

### MUST_FIX — active fix before isolation

Disabling or editing a suspected plugin/autoload in the active project before the disposable matrix can destroy the original evidence and confound multiple variables.

### MUST_FIX — one TEMP reused across A/B

Generated/import/runtime state from variant A may survive into B. Independent fresh extractions are required when derived state can persist.

### SHOULD_FIX — over-generalizing Git archive

The contract is about **trusted disposable exact-source materialization**, not mandating `git archive`. Repositories using submodules, Git LFS, filters, generated source, or runtime Git metadata may need a clean clone/worktree or project-specific fixture.

### SHOULD_FIX — diagnostic matrix grows without bound

Once the earliest failing boundary is known, vary one high-information factor at a time. Do not generate combinatorial permutations that do not change the next decision.

### SECURITY — disposable data leakage

TEMP/log paths must follow existing secret/redaction/cleanup policy. Do not copy credentials or private machine state just to make the clean reproduction resemble the active environment.

## 영향 범위와 검증

### Existing Base coverage

`BCP-2026-015-external-runtime-session-same-snapshot-recovery` owns fresh process/transport/server-registry identity and safe external-session recovery. It does not define clean committed-tree versus generated/cache versus runtime-startup isolation.

`BCP-2026-018-godot-pilot-failure-diagnostic-preservation` owns preserving failure payload before terminal verification. It does not define disposable source materialization or independent one-variable startup variants.

The Base already has general debugging, validation, handoff, and Godot/live-editor owners. Therefore the Existing Solution Verdict is `ABSORB`: if separately approved later, add the smallest compatible mode/reference/test to existing diagnostic owners rather than create another broad Skill.

### External benchmark

Official Git documents `git archive` as creating an archive from a named tree/tree-ish and documents that `export-ignore` paths are omitted. This supports using an exact commit/tree as a disposable source identity while requiring an explicit archive-completeness gate.

Reference:
`https://git-scm.com/docs/git-archive`

Official Godot command-line documentation treats `--import` as an editor/import lifecycle that waits for imports and quits, while normal game execution and `--headless` runtime are separate command modes. This supports treating import and normal runtime boot as separate verification gates rather than one result.

Reference:
`https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html`

### Project application verification

OMENWARD applied the learning before Base proposal submission:

- current-state/Handoff consumers persist the exact committed-source crash boundary and next one-variable step;
- fail-closed v4.5 scope requires the Handoff/current-state surface together;
- exact project closure head `7dd5658b535c71746d3ae046ee74b9f40ff1151d` passed all 12 triggered workflows;
- project PR #196 merged to main `b51bb29471ab802c6241d72a9af1226209934887`;
- the project runtime implementation remains paused, so this handoff did not launder an unresolved product bug into a completion claim.

### Proposal-stage validation

Before proposal merge require:

1. changed files are exactly this `PROPOSAL.md` plus `[수정제안서]/PROPOSAL_REGISTRY.json`;
2. current Base proposal validator passes;
3. Proposal ID/folder/Registry path/source/status match;
4. no orphan proposal or ghost Registry entry;
5. latest Base main + open proposal PRs are re-read immediately before merge;
6. all other project proposal entries are preserved exactly;
7. exact proposal head CI is terminal Green and unresolved review threads are zero.

### Future implementation validation — separate stage only

If the proposal is later approved for implementation, a focused regression should cover at least:

- exact-source materialization with required-file completeness check;
- an `export-ignore` counterexample;
- fresh derived/cache generation separate from normal runtime boot;
- a preparation failure classified separately from runtime failure;
- two independent one-variable variants that start from the same source identity;
- active tracked source unchanged by diagnostic-only execution;
- historical PID/session/source identifiers rejected as current execution authority where relevant.

No Base active implementation is performed by this proposal PR.

## 필요한 도구·파일·권한

Proposal storage stage:

- Base GitHub branch/PR write access
- `[수정제안서]/**` write access
- Proposal Registry semantic-union update
- current proposal validation and CI

No new runtime software, shared server restart, credential, or Base active-file mutation is required for proposal storage.

Future implementation, only after a separate approval, may use the existing debugging/Godot/runtime validation owner and synthetic disposable fixtures. That is outside this stage.

## 승인과 구현

- proposal storage/merge authority: `GRANTED_BY_CURRENT_HANDOFF_INSTRUCTION`
- proposal status: `SUBMITTED`
- 사용자 승인 근거: `미승인 — proposal storage/merge only; implementation approval not granted`
- approval_ref: `null`
- implementation_pr: `null`
- Base active implementation authority: `NOT_GRANTED_IN_THIS_STAGE`
- implementation status: `NOT_STARTED_IN_THIS_STAGE`
- implementation boundary: `SEPARATE_FOLLOWUP_STAGE`
- rollback: proposal-only PR can be reverted without changing active Base behavior; any future implementation must have a separate rollback and approval boundary.
