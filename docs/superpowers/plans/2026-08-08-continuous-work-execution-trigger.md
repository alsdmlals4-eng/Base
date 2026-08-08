# Continuous Work Execution Trigger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `[연속작업] 진행해` as an explicit opt-in trigger for bounded continuous execution inside an approved work contract.

**Architecture:** Keep existing Work Mode and Skill ownership intact. Add one intake reference that defines `CONTINUOUS_WORK_ACTIVE`, link it from the canonical operating/routing surfaces, and pin the behavior with static contract tests. No new Skill, scheduler, webhook, or background service is introduced.

**Tech Stack:** Markdown operating contracts, Python `unittest`, GitHub Actions governance CI.

## Global Constraints

- Activation phrase is exactly `[연속작업] 진행해`.
- Triggerless requests remain on existing approval and Grill Me behavior.
- Auto-approval applies only to technical single-safe recommendations inside the current approved work contract.
- `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, scope expansion, high-risk external actions, and user stop/scope change terminate or pause the loop.
- `CONTINUOUS_WORK_ACTIVE` is in-run orchestration, not asynchronous/background execution.
- Existing `PLAN / BUILD / REVIEW` and `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY` contracts remain authoritative.

---

### Task 1: Lock the continuous-work behavior contract

**Files:**
- Create: `tests/test_continuous_work_execution_contract.py`
- Create later in Task 2: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

**Interfaces:**
- Consumes: approved BCP-2026-010 design.
- Produces: static contract expectations for trigger, states, loop, exceptions, and non-background boundary.

- [ ] **Step 1: Write the failing test**

Create a `unittest` file that requires the new reference to exist and contain: `[연속작업] 진행해`, `CONTINUOUS_WORK_ACTIVE`, `CONTINUOUS_WORK_INACTIVE`, `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, `attack → validate-critique`, `regression-recheck`, `승인된 작업 계약`, `백그라운드`, and a termination rule.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_continuous_work_execution_contract -v`

Expected: FAIL because `continuous-work-execution.md` and canonical links do not exist yet.

- [ ] **Step 3: Commit the red contract**

Commit only the failing test so CI evidence shows the feature is not already present.

### Task 2: Implement the intake-owned execution protocol

**Files:**
- Create: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`

**Interfaces:**
- Consumes: exact activation phrase and approved work contract.
- Produces: `CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE` execution state and bounded next-task loop.

- [ ] **Step 1: Add the reference**

Document activation, scope, loop, technical auto-approval criteria, stop conditions, progress updates, and non-background semantics.

- [ ] **Step 2: Link intake routing**

Add the reference to terminology/read-first/workflow so `route` detects the phrase and `contract` carries the state without creating a new Work Mode.

- [ ] **Step 3: Verify GREEN for the protocol test**

Run: `python -m unittest tests.test_continuous_work_execution_contract -v`

Expected: PASS for reference and intake assertions that are already implemented.

### Task 3: Wire canonical operating surfaces

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

**Interfaces:**
- Consumes: intake execution state.
- Produces: one-hop discoverability and canonical Work Mode transition rules.

- [ ] **Step 1: Add AGENTS invariant**

State that `[연속작업] 진행해` activates bounded continuous execution only for the current approved contract and never suppresses user-only decisions or high-risk confirmations.

- [ ] **Step 2: Add operating lifecycle**

Document the loop as `next incomplete task → BUILD → REVIEW → technical recommendation auto-approval → regression → next task → final report`.

- [ ] **Step 3: Add routing-state details**

Document `CONTINUOUS_WORK_ACTIVE` as an execution flag layered over, not replacing, `PLAN / BUILD / REVIEW`.

- [ ] **Step 4: Run focused tests**

Run: `python -m unittest tests.test_continuous_work_execution_contract tests.test_deep_interview_contract -v`

Expected: PASS.

### Task 4: Record implementation and run governance regression

**Files:**
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `[수정제안서]/BCP-2026-010-continuous-work-execution-trigger/PROPOSAL.md`
- Modify: `[수정제안서]/PROPOSAL_REGISTRY.json`

**Interfaces:**
- Consumes: implementation PR number and validation evidence.
- Produces: BCP `IMPLEMENTED` linkage and learning record.

- [ ] **Step 1: Record changelog and learning**

Explain that continuous work is opt-in and bounded, and that no new Skill was required because the behavior was absorbed into intake/routing.

- [ ] **Step 2: Update BCP lifecycle**

Set status to `IMPLEMENTED` and record the implementation PR URL.

- [ ] **Step 3: Run regression**

Run focused contract tests plus Base proposal and governance checks, then require GitHub Actions `ci-gate` success.

- [ ] **Step 4: Adversarial recheck**

Confirm no triggerless auto-approval, no bypass of `USER_DECISION_REQUIRED`, no scope-expanding next-task selection, and no asynchronous/background claim.

- [ ] **Step 5: Merge**

After required checks, unresolved thread 0, and no P0/P1 findings, merge under `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY` without another user approval request.
