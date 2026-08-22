# Current Workstream Continuation Through Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make an approved current-workstream continuation directive authorize the normal lifecycle through merge and postmerge readback without weakening protection for other PRs.

**Architecture:** Keep `OPEN_PR_READ_ONLY_BY_DEFAULT` and named authorization for foreign/unknown workstreams, then add a narrow `CURRENT_WORKSTREAM_CONTINUE_INCLUDES_MERGE` exception. The exception is gated by current-workstream identity, explicit stop precedence, exact-head Required Checks, bounded conflict reconciliation, repository governance, and postmerge readback.

**Tech Stack:** Markdown policy/Skill contracts, Python unittest contract tests, GitHub Required Checks.

**Spec:** `docs/superpowers/specs/2026-08-22-current-workstream-continue-includes-merge-design.md`

## Global Constraints

- No force-push or repository governance bypass.
- No foreign/unknown workstream PR mutation without explicit PR/action authorization.
- Failed or pending Required Checks block merge.
- Explicit `do not merge`/`PR only`/draft-stop instruction overrides continuation.
- Semantic conflicts that change approved scope, cost, security, permissions, or product direction require user decision.

---

### Task 1: Add regression contract first

**Files:**
- Create: `tests/test_current_workstream_continue_merge_contract.py`

**Interfaces:**
- Consumes: existing AGENTS/long-horizon/sync owner text.
- Produces: required machine tokens and safety-boundary assertions.

- [x] **Step 1: Add failing contract test requiring the new continuation token and boundaries.**
- [ ] **Step 2: Run/observe the test fail because current owners do not yet contain `CURRENT_WORKSTREAM_CONTINUE_INCLUDES_MERGE`.**

### Task 2: Update canonical authority and lifecycle owner

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`

**Interfaces:**
- Consumes: `SINGLE_INITIAL_APPROVAL_THEN_CONTINUE`, existing open-PR protection.
- Produces: current-workstream continuation exception and lifecycle semantics.

- [ ] **Step 1: Preserve the default read-only rule for foreign/unknown open PRs.**
- [ ] **Step 2: Define continuation phrases as approval to continue the current workstream through exact-head PR Gate, merge, and postmerge readback.**
- [ ] **Step 3: Define explicit stop, failed/pending checks, governance bypass, and semantic-conflict blockers.**

### Task 3: Update Git synchronization execution owner

**Files:**
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`

**Interfaces:**
- Consumes: current/owner workstream identity, exact head/base/check evidence.
- Produces: bounded current-PR reconciliation and automatic merge/readback routing after continuation authorization.

- [ ] **Step 1: Route current-workstream PR separately from foreign/unknown PRs.**
- [ ] **Step 2: Permit only bounded conflict reconciliation that preserves latest completed `main` and approved workstream semantics.**
- [ ] **Step 3: Re-run exact-head checks after reconciliation and require post-merge main readback.**

### Task 4: Validate propagation and integrate

**Files:**
- Test: `tests/test_current_workstream_continue_merge_contract.py`
- Inspect: all occurrences of `OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION` and `PR 번호와 허용 동작`.

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: exact-head CI evidence and merge-ready PR.

- [ ] **Step 1: Run focused test and relevant repository CI.**
- [ ] **Step 2: Search for unqualified stale contradictions and reconcile them only where they are active owner text.**
- [ ] **Step 3: Verify exact-head Required Checks.**
- [ ] **Step 4: Under this user's explicit request, merge the policy PR and read back latest main.**
