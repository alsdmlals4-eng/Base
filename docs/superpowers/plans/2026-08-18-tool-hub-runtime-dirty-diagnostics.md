# Tool Hub Runtime Dirty Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Windows Tool Hub launcher distinguish a real tracked runtime diff from a Git check failure and preserve a bounded path-only diagnostic for the user-PC blocker.

**Architecture:** Keep the existing fail-closed `HEAD == origin/main` and runtime-cleanliness gates. Interpret Git's `diff --quiet` return code precisely; on a real diff, perform one additional read-only, runtime-path-scoped `diff --name-only -z`, validate each repository-relative path, and write only those names to the existing BaseToolHub local diagnostic directory. Do not mutate the Base checkout.

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
- Modify: `tools/tool-hub/tests/test_windows_launcher_self_repair.py`

**Interfaces:**
- Consumes: `windows_launcher_repair._assert_reviewed_runtime(root, git)`.
- Produces: failing contracts for `LAUNCHER_GIT_CHECK_FAILED` and `%LOCALAPPDATA%/BaseToolHub/logs/launcher-runtime-dirty.log`.

- [ ] Add a test where HEAD/origin match and `git diff --quiet` returns `2`; assert the result is `LAUNCHER_GIT_CHECK_FAILED`, not `LAUNCHER_RUNTIME_DIRTY`.
- [ ] Add a test where `git diff --quiet` returns `1` followed by `git diff --name-only -z` returning one reviewed relative path; assert `LAUNCHER_RUNTIME_DIRTY` and an exact path-only diagnostic file under a temporary `LOCALAPPDATA`.
- [ ] Run the already-required Tool Hub Subscription workflow and observe intended RED before production changes.

### Task 2: GREEN — read-only runtime-dirty diagnosis

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/windows_launcher_repair.py`
- Test: `tools/tool-hub/tests/test_windows_launcher_self_repair.py`

**Interfaces:**
- Consumes: existing `_git`, `_RUNTIME_PATHS`, `LauncherError`, `_atomic_write`.
- Produces: precise Git failure code plus bounded dirty-path log.

- [ ] Treat `diff --quiet` return `0` as clean, `1` as real tracked runtime dirtiness, and every other code as `LAUNCHER_GIT_CHECK_FAILED`.
- [ ] For return `1`, run `git diff --name-only -z --no-ext-diff HEAD -- <existing runtime paths>`.
- [ ] Reject failed, oversized, undecodable, absolute, parent-traversing, control-character, or out-of-scope path output as `LAUNCHER_GIT_CHECK_FAILED`.
- [ ] Write only `LAUNCHER_RUNTIME_DIRTY` plus validated repository-relative path names to `%LOCALAPPDATA%/BaseToolHub/logs/launcher-runtime-dirty.log`; cap count/size.
- [ ] Keep the existing `LAUNCHER_RUNTIME_DIRTY` native failure and diagnostic-folder pointer.
- [ ] Run focused tests on Ubuntu and Windows.

### Task 3: Exact-head integration and merge

**Files:**
- No additional production surface unless a required current-main regression identifies a real incompatibility.

- [ ] Run Tool Hub Subscription Contracts Ubuntu + Windows.
- [ ] Run Base v9/adversarial gate.
- [ ] Run Game Project Operating System including Windows Tool Hub smoke and final `ci-gate`.
- [ ] Confirm current main ancestry, zero unresolved review threads, and no unrelated PR branch edits.
- [ ] Merge the exact verified head.
- [ ] Re-read new main and postmerge checks.

### Task 4: User-PC IRG continuation

- [ ] Pull the merged Base main using the existing normal update path.
- [ ] Launch the desktop Tool Hub once.
- [ ] If still `LAUNCHER_RUNTIME_DIRTY`, read `launcher-runtime-dirty.log`; the named runtime files become the exact next root-cause evidence.
- [ ] Preserve local changes until their ownership is known; do not auto-discard.
- [ ] After launcher recovery, verify final-tab auto-shutdown, Character Studio child launch, Figma Bridge pairing, and real Figma receipt/readback in that order.
