# Tool Hub Runtime Dirty Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Windows Tool Hub launcher distinguish a real tracked runtime diff from a Git check failure and preserve a bounded path-only diagnostic for the user-PC blocker.

**Architecture:** Keep the existing fail-closed `HEAD == origin/main` and runtime-cleanliness gates. Replace the information-losing `git diff --quiet` probe with one read-only, runtime-path-scoped `git diff --name-only -z --exit-code`: return code `0` means clean, `1` means a real diff whose NUL-delimited relative names can be validated and recorded, and any other return code is a Git check failure. Do not mutate the Base checkout.

**Tech Stack:** Python 3.12, Git for Windows, pytest, GitHub Actions Ubuntu/Windows.

## Global Constraints

- Base authority starts at `74dadc082001124d9f79262198bad3e9bd7f6977`.
- No reset/checkout/clean/stage/write of the user's Base checkout.
- No file contents, diff bodies, local credentials, tokens, prompts, or provider data in diagnostics.
- No paid OpenAI API/API-key fallback, A3, Scheduler, Figma mutation, or project mutation.
- Existing reviewed `_RUNTIME_PATHS` remain the only scope.

---

### Task 1: RED — precise Git result and bounded dirty-path evidence

**Files:**
- Create: `tools/tool-hub/tests/test_windows_launcher_runtime_dirty_diagnostics.py`
- Modify: `.github/workflows/validate-tool-hub-subscription-contracts.yml`

**Interfaces:**
- Consumes: `windows_launcher_repair._assert_reviewed_runtime(root, git)`.
- Produces: failing contracts for `LAUNCHER_GIT_CHECK_FAILED` and `%LOCALAPPDATA%/BaseToolHub/logs/launcher-runtime-dirty.log` that are explicitly consumed by the required Tool Hub workflow.

- [x] Add a test where HEAD/origin match and the runtime diff query returns `2`; assert the result is `LAUNCHER_GIT_CHECK_FAILED`, not `LAUNCHER_RUNTIME_DIRTY`.
- [x] Add a test where the runtime diff query returns `1` plus NUL-delimited reviewed relative names; assert `LAUNCHER_RUNTIME_DIRTY` and an exact path-only diagnostic file under a temporary `LOCALAPPDATA`.
- [x] Add a test that rejects an out-of-scope path instead of recording it.
- [x] Explicitly add the regression file to `Validate Tool Hub Subscription Contracts` triggers and pytest command.
- [x] Observe intended RED before production changes: run `32043464612`, Ubuntu/Windows focused jobs failed with exactly the three new contracts while the prior suite stayed green (`3 failed, 71 passed` on Ubuntu).

### Task 2: GREEN — read-only runtime-dirty diagnosis

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/windows_launcher_repair.py`
- Test: `tools/tool-hub/tests/test_windows_launcher_runtime_dirty_diagnostics.py`

**Interfaces:**
- Consumes: existing `_git`, `_RUNTIME_PATHS`, `LauncherError`, `_atomic_write`.
- Produces: precise Git failure code plus bounded dirty-path log.

- [x] Run one `git diff --name-only -z --no-ext-diff --no-renames --exit-code HEAD -- <existing runtime paths>`.
- [x] Treat return `0` as clean, `1` as real tracked runtime dirtiness, and every other code as `LAUNCHER_GIT_CHECK_FAILED`.
- [x] Strictly validate the NUL-delimited UTF-8 names; reject oversized, undecodable, absolute, parent-traversing, control-character, or out-of-scope output as `LAUNCHER_GIT_CHECK_FAILED`.
- [x] Write only `LAUNCHER_RUNTIME_DIRTY` plus validated repository-relative path names to `%LOCALAPPDATA%/BaseToolHub/logs/launcher-runtime-dirty.log`, with bounded count/size.
- [x] Keep the existing `LAUNCHER_RUNTIME_DIRTY` native failure and diagnostic-folder pointer.
- [x] Keep unexpected untracked reviewed-runtime files fail-closed; report Git command/decode failure as `LAUNCHER_GIT_CHECK_FAILED`.
- [x] Observe GREEN on exact implementation head `3230d4619607f14a0ef648144b72da9112603992`: Tool Hub Subscription Contracts run `32043591490` PASS on Ubuntu and Windows, including production-boundary contracts.

### Task 3: Exact-head integration and merge

**Files:**
- No additional production surface unless a required current-main regression identifies a real incompatibility.

- [x] Tool Hub Subscription Contracts Ubuntu + Windows PASS on `3230d461...`.
- [x] Base v9/adversarial PASS on `3230d461...`, run `32043591419`.
- [x] Dependency Review PASS on `3230d461...`, run `32043591594`.
- [ ] Game Project Operating System including Windows Tool Hub smoke and final `ci-gate` PASS.
- [ ] Confirm current main ancestry, zero unresolved review threads, and no unrelated PR branch edits.
- [ ] Merge the exact verified head.
- [ ] Re-read new main and postmerge checks.

### Task 4: User-PC IRG continuation

- [ ] Pull the merged Base main using the existing normal update path.
- [ ] Launch the desktop Tool Hub once.
- [ ] If still `LAUNCHER_RUNTIME_DIRTY`, read `%LOCALAPPDATA%\BaseToolHub\logs\launcher-runtime-dirty.log`; the named reviewed-runtime files become the exact next root-cause evidence.
- [ ] Preserve local changes until their ownership is known; do not auto-discard.
- [ ] After launcher recovery, verify final-tab auto-shutdown, Character Studio child launch, Figma Bridge pairing, and real Figma receipt/readback in that order.
