# Loop A2 Durable Resume Evidence

## Identity

- Tracking issue: `#359`
- PR: `#360`
- Original source main: `141fcab50d55e050637f736840d257bef9f6413c`
- Prerequisites: A2 Foundation `#343`, actual Git worktree/Diff `#351`, Project Test Executor `#354`, PR integration `#358` merged independently afterward.

## Initial TDD RED

- Test-only head: `47d4588cbe23fd1e3e10a9abfca5d239133108fe`
- A2 run: `31784036272`
- Existing A2 tests passed.
- New resume tests failed because `tools.loop_a2_runtime.workspace_registry` did not exist.

## Minimum implementation and fixture correction

The first implementation added a durable ownership registry outside the source project repository and explicit `resume(request)` behavior to the existing Git worktree adapter.

It binds:

```text
project_id
run_id
expected_main_sha
source_repo
workspace
receipt_digest
```

The first full A2 run reached all new behavior tests; one cleanup callback was incorrectly scheduled after the inherited temporary repository had already been deleted. The test fixture was corrected without changing production behavior.

- corrected head: `18f1f8bba9ccfc047a27760280366291dba367f5`
- A2 run: `31784444105` — PASS

## Adversarial RED

Adversarial review found a real path-isolation gap: if `runtime_root/PROJECT_ID` was a directory symlink, the original implementation could allow `git worktree add` to materialize outside the runtime root before the ownership receipt check.

- adversarial head: `e579c31c0a8647e31bc4f92f145a788028a8571e`
- A2 run: `31784527268`
- result: all existing resume/A2 tests passed except the intentional project-namespace symlink escape regression, which returned `COMPLETED` instead of `BLOCKED`.

The adversarial suite also verifies:

- symlinked `.loop-ownership` registry fails closed;
- stale ownership receipt blocks recreation of a missing worktree;
- unknown receipt fields are rejected;
- a registered worktree without an ownership receipt is never adopted;
- corrupt receipt, wrong source repo, wrong run identity, or missing Git worktree registration cannot resume;
- failed resume preserves forensic evidence rather than guessing ownership.

## Remediation

Production was hardened so workspace and ownership paths are verified **before** any Git worktree mutation:

- `validate_workspace_path()` requires the closed `<runtime>/<project>/<run>` namespace, lexical confinement, physical confinement and no symlink component;
- `preflight_claim()` validates ownership paths and rejects a stale receipt before worktree creation;
- only after both preflights pass may `git worktree add` run;
- receipt publication failure removes only the just-created worktree and fails closed;
- cleanup still requires re-verifying the durable receipt before deleting the worktree or receipt.

Remediation head before latest-main refresh: `12e98d9872cbb62db070cbd4ac565bfde21c2c10`.

Validation on that head:

- A2 Runtime Foundation `31784716864` — PASS;
- Base-v9 `31784716869` — PASS;
- Game Project OS `31784716966` — PASS.

## Cross-platform validation

A dedicated Ubuntu/Windows workflow exercises durable ownership publication, restart/resume, tamper rejection, unowned-worktree rejection, missing-registration behavior, symlink/path confinement when supported by the runner, and cleanup of only verified owned worktrees.

## Boundaries

This slice does not:

- call Codex, GPT, or another model;
- access the network from the runtime;
- create, update, merge, or approve PRs;
- select new product scope;
- change Planning Lock, Visual Lock, Figma, assets, scenes, save data, or product logic;
- enable A3;
- configure a Scheduler.

## Final integration gate

Before merge:

1. reapply only the durable-resume-owned files on current `main`;
2. dedicated Ubuntu/Windows durable-resume PASS;
3. A2 Foundation PASS;
4. Base-v9 PASS;
5. Game Project OS PASS;
6. Dependency Review PASS;
7. unresolved review threads `0`;
8. current-main/path-overlap check;
9. expected-head squash merge;
10. postmerge readback and push validation.

## Rollback

Revert the eventual PR #360 squash merge. Runtime worktrees and ownership receipts are operational state only; no project or product data migration is included.
