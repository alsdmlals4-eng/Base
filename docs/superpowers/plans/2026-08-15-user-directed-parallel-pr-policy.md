# User-Directed Parallel PR Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Base distinguish explicit user-directed work from scheduled automation when same-goal PRs are already in progress.

**Architecture:** Extend the existing Continuous Work contract rather than creating a new Skill or workflow. User-directed execution may create a separate PR from current completed `main` while leaving all other in-progress PR branches untouched; scheduled/periodic automation keeps its independent active-PR fail-closed boundary.

**Tech Stack:** Markdown operating contracts, Python unittest repository contract tests, existing GitHub Actions required checks.

## Global Constraints

- Do not modify open PR #422 or any other active PR branch.
- Do not weaken scheduled/periodic active-PR guards.
- Do not create a new Skill, Work Mode, or Registry entry.
- User-directed new work starts from current completed `main`.
- Never push/rebase/update/close/merge another in-progress PR unless explicitly assigned.
- Reconcile duplicate work against current `main` immediately before merge.

---

### Task 1: Contract regression

**Files:**
- Modify: `tests/test_continuous_work_execution_contract.py`

**Interfaces:**
- Requires literals `USER_DIRECTED_PARALLEL_PR`, `current completed main`, `separate branch/PR`, and `scheduled/periodic` in the owner surfaces.

- [ ] Add a failing test that requires the interactive/scheduled split in `continuous-work-execution.md` and `SKILL.md`.
- [ ] Run exact-head PR CI and record RED because production docs do not yet contain the contract.

### Task 2: Existing-owner absorption

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`

- [ ] Add `USER_DIRECTED_PARALLEL_PR` under the existing continuous-work execution owner.
- [ ] State that a same-goal in-progress PR is read-only evidence unless explicitly assigned.
- [ ] Require a new branch/PR from current completed `main` when the user explicitly says to continue independently.
- [ ] Preserve scheduled/periodic automation active-PR guards as a separate stricter boundary.
- [ ] Require pre-merge current-main/same-goal reconciliation; close as superseded if no material delta remains.
- [ ] Re-run CI and require the focused contract plus Base required workflows green.

### Task 3: Merge gate

- [ ] Compare the feature head against current `main` and verify no overlap with PR #422 changed files.
- [ ] Require unresolved review threads = 0 and exact-head required checks green.
- [ ] If `main` moved, synchronize only this new branch and rerun the exact-head gate; do not touch active PR branches.
- [ ] Squash merge under repository rules and read back `main`.
