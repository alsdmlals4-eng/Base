# Provisional Integration Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow explicitly authorized provisional integration PRs to continue from the latest `main` despite overlapping owner PRs, while preserving owner branches, requiring semantic reconciliation, and blocking merge until overlap ownership is resolved.

**Architecture:** Extend the existing `CONCURRENT_CHANGE_PREFLIGHT` contract rather than creating a second coordination framework. Add `PROVISIONAL_INTEGRATION` as a narrowly gated disposition in `AGENTS.md`, the synchronization Skill, and its safe-sync protocol; keep `WAITING_RESOURCE` and `DUPLICATE_WORK` as defaults when explicit authorization is absent. A regression test pins the required tokens and merge/reconciliation conditions.

**Tech Stack:** Markdown governance contracts, Python `unittest`, GitHub exact-SHA PR/CI workflow.

## Global Constraints

- Explicit user authorization is required before overlapping provisional integration writes.
- Never push to, rewrite, rebase, or otherwise mutate overlapping owner PR branches.
- Provisional work starts from the exact current `main` SHA and records owner PR/head SHAs plus overlapping paths/semantic resources.
- When an owner PR merges/closes/is superseded or `main` materially advances, reconcile immediately and rerun exact-head validation.
- Reconciliation is semantic/contract based; preserve the current canonical implementation and remove provisional duplicates.
- A provisional integration PR cannot merge while an overlapping owner remains unresolved unless that owner is merged and absorbed, explicitly handed off/superseded, or the user explicitly authorizes replacement.
- Existing `WAITING_RESOURCE` and `DUPLICATE_WORK` remain the default without explicit provisional-integration authorization.
- Do not modify Local Executor behavior introduced by PR #420.

---

### Task 1: Pin the new concurrent-work contract with RED

**Files:**
- Modify: `tests/test_concurrent_git_sync_preflight_contract.py`

**Interfaces:**
- Consumes: repository text contracts from `AGENTS.md`, `skills/synchronizing-local-and-github-state/SKILL.md`, and `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`.
- Produces: regression expectations for `PROVISIONAL_INTEGRATION`, explicit authorization, owner-branch immutability, immediate reconciliation, semantic duplicate removal, and merge blocking.

- [ ] **Step 1: Write the failing test**

Add a test that requires all three governance surfaces to contain `PROVISIONAL_INTEGRATION`, requires the protocol to state `explicit user authorization`, `owner PR branches`, `semantic reconciliation`, `exact-head`, and `must not merge`, and requires `AGENTS.md` to state that unresolved overlapping owner PRs block merge.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_concurrent_git_sync_preflight_contract.ConcurrentGitSyncPreflightContractTests.test_explicitly_authorized_provisional_integration_requires_reconciliation_before_merge`

Expected: FAIL because the current contracts do not contain `PROVISIONAL_INTEGRATION`.

### Task 2: Implement the minimal governance contract

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`

**Interfaces:**
- Consumes: existing `CONCURRENT_CHANGE_PREFLIGHT` states and exact-SHA synchronization rules.
- Produces: `PROVISIONAL_INTEGRATION` disposition and merge/reconciliation obligations.

- [ ] **Step 1: Extend `AGENTS.md`**

Add a Base-wide invariant under GitHub/protection rules: explicitly authorized provisional integration may overlap open owner PRs only on an isolated latest-main branch, must not mutate owner branches, must reconcile whenever owner/main state changes, and cannot merge while overlapping ownership is unresolved.

- [ ] **Step 2: Extend the synchronization Skill**

Add `PROVISIONAL_INTEGRATION` to the disposition enum and define its exact authorization, evidence, branch immutability, reconciliation, and merge-blocking semantics. Keep default `WAITING_RESOURCE` / `DUPLICATE_WORK` behavior unchanged when the authorization flag is absent.

- [ ] **Step 3: Extend the safe-sync protocol**

Add a provisional-overlap path after overlap classification, record owner PR/head SHA/path/semantic locks, require immediate semantic reconciliation after owner/main changes, and add a merge gate that rejects unresolved owner overlap.

- [ ] **Step 4: Run the focused test**

Run the same unittest from Task 1.

Expected: PASS.

### Task 3: Validate the exact PR head

**Files:**
- No production-file changes unless validation exposes a contract defect.

**Interfaces:**
- Consumes: exact branch head produced by Tasks 1-2.
- Produces: merge evidence tied to one exact SHA.

- [ ] **Step 1: Run focused contract suite**

Run: `python -m unittest tests.test_concurrent_git_sync_preflight_contract`

Expected: PASS.

- [ ] **Step 2: Run repository-required CI on the PR exact head**

Expected: Base v9 / Game Project OS / dependency and documentation gates required by the repository complete successfully at the exact reviewed head.

- [ ] **Step 3: Adversarially review the policy**

Verify that the new disposition cannot be used without explicit authorization, cannot justify writes to owner branches, cannot treat textual auto-merge as semantic reconciliation, cannot reuse stale CI, and cannot merge while owner overlap remains unresolved.

### Task 4: Merge and read back the canonical rule

**Files:**
- No new files.

**Interfaces:**
- Consumes: merge-ready exact head.
- Produces: merged Base governance usable by the subsequent Tool Hub integration PR.

- [ ] **Step 1: Confirm current `main`, exact reviewed head, required checks, and unresolved review threads**

Expected: no unexplained drift; otherwise rebase/reconcile and revalidate.

- [ ] **Step 2: Squash merge**

Expected: GitHub reports merged successfully.

- [ ] **Step 3: Post-merge readback**

Read `AGENTS.md`, the synchronization Skill, and safe-sync protocol from new `main` and verify `PROVISIONAL_INTEGRATION` plus merge-blocking reconciliation semantics are present.

- [ ] **Step 4: Close Issue #423**

Expected: issue state `closed/completed` after canonical readback succeeds.
