# User-Directed Parallel PR Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Base distinguish explicit user-directed work from scheduled automation when same-goal PRs are already in progress, while preserving the canonical concurrent-ownership merge gate.

**Architecture:** Extend the existing Continuous Work contract rather than creating a new Skill or workflow. User-directed execution may create a separate PR from current completed `main` while leaving all other in-progress PR branches untouched. Actual same-goal/path/semantic overlap delegates to `synchronizing-local-and-github-state` and remains `PROVISIONAL_INTEGRATION` until owner resolution; scheduled/periodic automation keeps its independent active-PR fail-closed boundary.

**Tech Stack:** Markdown operating contracts, Python unittest repository contract tests, existing GitHub Actions required checks.

## Global Constraints

- Do not modify another active PR branch.
- Do not weaken scheduled/periodic active-PR guards.
- Do not create a new Skill, Work Mode, or Registry entry.
- User-directed new work starts from current completed `main`.
- Never push/rebase/update/close/merge another in-progress PR unless explicitly assigned.
- `PROVISIONAL_INTEGRATION` remains owned by `synchronizing-local-and-github-state`.
- Actual overlapping provisional work must not merge until each owner is resolved and semantic reconciliation has been revalidated on the exact head.
- Reconcile duplicate work against current `main` immediately before merge; close as `superseded` when no material delta remains.

---

### Task 1: User-directed separate-PR regression

**Files:**
- Modify: `tests/test_continuous_work_execution_contract.py`

- [x] Add a failing test requiring `USER_DIRECTED_PARALLEL_PR`, `current completed main`, `separate branch/PR`, and `scheduled/periodic` in the owner surfaces.
- [x] Route the focused test through `Validate Loop A2 Durable Resume` so a standalone test cannot create a false green.
- [x] Record RED run `31852863100`: existing contract tests passed and the new policy alone failed before production owner changes.

### Task 2: Existing-owner absorption

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `tests/test_claim_evidence_binding.py`
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`

- [x] Add `USER_DIRECTED_PARALLEL_PR` under the existing continuous-work execution owner.
- [x] State that a same-goal in-progress PR is read-only evidence unless explicitly assigned.
- [x] Require a new branch/PR from current completed `main` when the user explicitly says to continue independently.
- [x] Preserve scheduled/periodic automation active-PR guards as a separate stricter boundary.
- [x] Add an allowlisted companion regression and Skill Learning Log evidence instead of weakening canonical freshness.

### Task 3: Reconcile with canonical provisional integration owner

**Trigger:** PR #425 merged during this work and made `PROVISIONAL_INTEGRATION` the canonical overlap disposition for explicitly authorized concurrent work.

**Files:**
- Modify: `tests/test_continuous_work_execution_contract.py`
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `tests/test_claim_evidence_binding.py`
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`

- [x] Add a second RED contract requiring delegation to `synchronizing-local-and-github-state`, `PROVISIONAL_INTEGRATION`, and the owner-resolution merge block.
- [x] Record RED run `31853777847`, Ubuntu job `94934536818`: all previous tests passed and only the new provisional-integration delegation assertion failed.
- [x] Separate PR-creation authority from overlap-merge authority in Continuous Work.
- [x] Route actual `SAME_GOAL / PATH_OVERLAP / SEMANTIC_OVERLAP` through the canonical safe-sync preflight.
- [x] Preserve owner PR branches as read-only and require semantic reconciliation + exact-head validation when owner/main moves.
- [x] State that actual provisional overlap must not merge until each owner is resolved; inherited merge authority does not bypass this gate.
- [ ] Extend the allowlisted companion test and Learning Log with the same reconciliation rule.
- [ ] Re-run the focused Ubuntu/Windows Durable Resume contract to GREEN.

### Task 4: Latest-main synchronization and full merge gate

- [ ] Read current `main` again and inspect same-goal/open/recent PR state.
- [ ] Synchronize **only this feature branch** to the latest completed main; do not write to another PR branch.
- [ ] Compare the feature head against current main and require only the intended files/material delta.
- [ ] Require exact-head Base v9 + adversarial, Game Project OS including canonical freshness/publication/Windows smoke/final `ci-gate`, Durable Resume Ubuntu+Windows, BCA, One-Shot Bootstrap, and Dependency Review/deferred result.
- [ ] Require unresolved review threads = 0 and no blocking submitted review.
- [ ] If actual owner overlap remains, keep `PROVISIONAL_INTEGRATION` and do not merge until owner resolution. If no actual overlap remains, use the normal merge gate.
- [ ] Squash merge under repository rules only when the current canonical gate allows it, then read back `main`.
