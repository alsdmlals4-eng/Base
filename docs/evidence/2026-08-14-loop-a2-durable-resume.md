# Loop A2 Durable Resume Evidence

## Identity

- Tracking issue: `#359`
- PR: `#360`
- Original source main: `141fcab50d55e050637f736840d257bef9f6413c`
- Latest-main refresh source: `4608d6bb8b8ef3b4eb51d02946b107a71f54ac3c`
- Pre-refresh branch preserved as `backup-loop-a2-durable-resume-pre-refresh-20260814`.
- Prerequisites: A2 Foundation `#343`, actual Git worktree/Diff `#351`, Project Test Executor `#354`, PR integration `#358`.

## Initial TDD RED

- Test-only head: `47d4588cbe23fd1e3e10a9abfca5d239133108fe`
- A2 run: `31784036272`
- Existing A2 tests passed.
- New resume tests failed because `tools.loop_a2_runtime.workspace_registry` did not exist.

## Minimum implementation and fixture correction

The first implementation added a durable ownership registry outside the source project repository and explicit `resume(request)` behavior to the existing Git worktree adapter.

The ownership receipt binds:

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

## Path-isolation remediation

Production was hardened so workspace and ownership paths are verified **before** any Git worktree mutation:

- `validate_workspace_path()` requires the closed `<runtime>/<project>/<run>` namespace, physical confinement and no symlink component;
- `preflight_claim()` validates ownership paths and rejects a stale receipt before worktree creation;
- only after both preflights pass may `git worktree add` run;
- receipt publication failure removes only the just-created worktree and fails closed;
- cleanup requires re-verifying the durable receipt before deleting either worktree or receipt.

Remediation head before latest-main refresh: `12e98d9872cbb62db070cbd4ac565bfde21c2c10`.

Validation on that head:

- A2 Runtime Foundation `31784716864` — PASS;
- Base-v9 `31784716869` — PASS;
- Game Project OS `31784716966` — PASS.

## Latest-main and Windows alias regression

The six owned files were reapplied on `main@4608d6bb8b8ef3b4eb51d02946b107a71f54ac3c`. Candidate head `5349c9a441b91be3e5dad380b8a832b0ea9b790d` passed Ubuntu durable-resume, A2 Foundation, Base-v9 and Dependency Review, while dedicated Windows exposed one platform-only regression.

Windows temporary paths can refer to the same directory through an 8.3 short-name alias such as `RUNNER~1` and its canonical long-name form. A lexical `Path.relative_to()` check rejected that physically identical workspace even though it did not escape the Runtime Root. The fix keeps the symlink defense by validating the **closed expected namespace first**, then canonicalizes the supplied path and compares physical paths. It does not accept a symlinked project namespace because that namespace fails the pre-canonicalization safe-tree check.

- Windows failing run: `31785100287`
- failure boundary: `test_stale_ownership_receipt_blocks_before_recreating_missing_worktree`
- root cause: equivalent Windows short/long path spellings failed lexical ancestry comparison
- corrected head before this evidence-only commit: `ee174f5b6e9d1679d90e3896cca735f7d3d084e7`
- dedicated durable-resume run `31785272779`: Ubuntu PASS / Windows PASS
- A2 Foundation `31785272879`: PASS
- Base-v9 `31785272877`: PASS
- Dependency Review `31785272778`: PASS
- Game Project OS `31785272940`: exact-head finalization run

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

1. dedicated Ubuntu/Windows durable-resume PASS on the final exact head;
2. A2 Foundation PASS;
3. Base-v9 PASS;
4. Game Project OS PASS;
5. Dependency Review PASS;
6. unresolved review threads `0`;
7. current-main/path-overlap check;
8. expected-head squash merge;
9. postmerge readback and push validation.

## Rollback

Revert the eventual PR #360 squash merge. Runtime worktrees and ownership receipts are operational state only; no project or product data migration is included.
