# Continuous Work Blocker Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `[연속작업] 진행해` recover from transient verification failures, local tool blockers, and inherited approvals instead of stopping at the first blocker, while preserving genuine user-decision, authority, and high-risk gates.

**Architecture:** Keep `CONTINUOUS_WORK_ACTIVE` as an intake orchestration flag. Add a blocker taxonomy, recovery ladder, and global progress queue to the existing continuous-work reference; wire the same semantics into routing, GPT→Codex handoff, long-running continuity, and top-level operating docs. Preserve all existing authority boundaries and prove the four reported failure patterns with contract tests.

**Tech Stack:** Markdown operating contracts, Python `unittest` contract tests, GitHub Actions, canonical reference freshness checker.

## Global Constraints

- `[연속작업] 진행해` remains explicit opt-in.
- Do not bypass `USER_DECISION_REQUIRED` when the approved outcome itself changes.
- Do not bypass payment/account/security/permission or other true high-risk confirmation gates.
- Do not bypass HiGodot or project-specific persistent-authoring authority.
- Do not claim unavailable Codex/HiGodot/executor calls happened.
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY` remains authoritative for already-approved scope.
- No infinite retry; exhaust a finite set of evidence/executor recovery paths, then defer or terminally block.

---

### Task 1: Add RED contract tests for the four reported stop failures

**Files:**
- Modify: `tests/test_continuous_work_execution_contract.py`
- Modify: `tests/test_gpt_codex_workflow_contract.py`

**Interfaces:**
- Consumes: current continuous-work reference and GPT→Codex policy.
- Produces: failing semantic assertions for blocker recovery, executor fallback, approval inheritance, and global progress continuation.

- [ ] **Step 1: Add failing tests**

Add assertions requiring these terms/behaviors:

```python
"RECOVERABLE_VERIFICATION_BLOCKER"
"EVIDENCE_TRANSPORT_INCOMPLETE"
"RECOVERABLE_EXECUTION_ROUTE_BLOCKER"
"LOCAL_TASK_BLOCKER"
"GLOBAL_TERMINAL_BLOCKER"
"ready_tasks"
"deferred_tasks"
"APPROVED_ITEM_INHERITS_MERGE_AUTHORITY"
"dedicated execution package"
"현재 세션"
"alternate executor"
```

Require the contract to state that a 10k verification package inside an approved outcome is execution method, not a new user decision; output truncation triggers requery/rerun rather than stop; current-session tool absence triggers authorized executor discovery/defer-and-continue; approved PRs do not ask for separate merge approval.

- [ ] **Step 2: Run the focused tests and verify RED**

Run through the repository CI or available Python environment:

```bash
python -m unittest tests.test_continuous_work_execution_contract tests.test_gpt_codex_workflow_contract -v
```

Expected: new assertions fail because the recovery taxonomy and handoff override are absent.

- [ ] **Step 3: Record the exact RED evidence**

Record failing test names and exact head SHA in the PR body or implementation learning log.

---

### Task 2: Implement the blocker recovery ladder in the canonical continuous-work reference

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

**Interfaces:**
- Consumes: approved work contract, task dependency graph, existing adversarial review states.
- Produces: blocker classification, recovery ladder, global progress queue, terminal-stop definition.

- [ ] **Step 1: Replace immediate-stop semantics**

Change the loop from:

```text
USER_DECISION_REQUIRED/BLOCKED_UNVERIFIED → stop
```

to:

```text
finding/blocker
→ classify
→ retry/requery
→ alternate authoritative evidence
→ authorized alternate executor/tool
→ defer blocked task
→ continue independent ready task
→ terminal stop only when no actionable work remains
```

- [ ] **Step 2: Add blocker taxonomy**

Define exactly:

```text
RECOVERABLE_VERIFICATION_BLOCKER
RECOVERABLE_EXECUTION_ROUTE_BLOCKER
LOCAL_TASK_BLOCKER
USER_DECISION_REQUIRED
HIGH_RISK_CONFIRMATION_REQUIRED
GLOBAL_TERMINAL_BLOCKER
```

- [ ] **Step 3: Add global progress queue**

Define:

```yaml
ready_tasks: []
deferred_tasks: []
completed_tasks: []
```

and require re-evaluation of deferred tasks after state changes.

- [ ] **Step 4: Encode the four examples as normative examples**

Cover 10k package, GitHub output truncation, HiGodot current-session absence, and inherited merge authority.

---

### Task 3: Wire recovery semantics into intake and top-level routing

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: continuous-work reference.
- Produces: one-hop discoverability and consistent state transition semantics.

- [ ] **Step 1: Update intake state transitions**

Require `CONTINUOUS_WORK_ACTIVE` to remain active through recoverable/local blockers and terminate only at `GLOBAL_TERMINAL_BLOCKER`, true user decision, true high-risk confirmation, user stop, or completion.

- [ ] **Step 2: Update routing contract**

State that `BLOCKED_UNVERIFIED` is a task/evidence state, not automatically a global continuous-work terminal state.

- [ ] **Step 3: Update operating model and AGENTS invariant**

Add compact invariant: recover first, defer locally second, continue independent work third, stop globally last.

---

### Task 4: Make continuous work an implicit executor-handoff request when execution is required

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Modify: `skills/maintaining-long-running-task-continuity/SKILL.md`

**Interfaces:**
- Consumes: approved scope, available executor/tool inventory, project authority rules.
- Produces: `CONTINUOUS_WORK_EXECUTOR_HANDOFF` semantics and defer-with-checkpoint behavior when no executor is callable.

- [ ] **Step 1: Add executor routing rule**

When `[연속작업]` is active and the current worker lacks an authorized execution tool, treat the active continuous-work request as sufficient approval to hand off the same approved scope to a callable authorized executor. Do not ask `Codex로 넘길까요?` again.

- [ ] **Step 2: Preserve capability honesty**

If no executor is actually callable, create an executor-ready handoff/checkpoint, mark only that task `DEFERRED_EXTERNAL_EXECUTOR`, and continue other ready work. Never claim a handoff was executed when it was only prepared.

- [ ] **Step 3: Preserve HiGodot authority**

Explicitly forbid direct text/GitHub editing as a workaround when the project declares HiGodot the sole persistent Godot authoring authority.

- [ ] **Step 4: Update long-running continuity behavior**

Before `partial-delivery`, require recovery ladder exhaustion and independent-task scan.

---

### Task 5: GREEN verification and regression hardening

**Files:**
- Modify: `tests/test_continuous_work_execution_contract.py`
- Modify: `tests/test_gpt_codex_workflow_contract.py`
- Modify one reference-freshness-recognized focused test if needed, preferably `tests/test_neutral_adversarial_feature_lifecycle.py`.

**Interfaces:**
- Consumes: Tasks 2–4 implementation.
- Produces: focused GREEN and CI-consumed regression evidence.

- [ ] **Step 1: Run focused tests**

```bash
python -m unittest tests.test_continuous_work_execution_contract tests.test_gpt_codex_workflow_contract tests.test_neutral_adversarial_feature_lifecycle -v
```

Expected: PASS.

- [ ] **Step 2: Check canonical reference freshness**

Run the repository canonical checker against the exact trusted main/base SHA and current head.

- [ ] **Step 3: Run required Base validation**

Use the repository's required GitHub Actions / `ci-gate`; do not infer success from file contents.

---

### Task 6: Record learning, publish PR, adversarial review, and merge

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md` if required by reference-freshness coupling.
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: verified implementation and actual CI evidence.
- Produces: durable learning and merged Base contract.

- [ ] **Step 1: Record root cause and correction**

Document that BCP-2026-010 initially conflated local/recoverable blockers with global terminal blockers and that user field examples drove the correction.

- [ ] **Step 2: Open a ready-for-review PR**

PR body must include the four examples, RED evidence, GREEN evidence, exact head, safety boundaries, and benchmark references.

- [ ] **Step 3: Run adversarial review**

Check especially for:

```text
infinite retry
hidden cost escalation
unauthorized HiGodot bypass
false Codex execution claims
silent scope expansion
merge without required checks
```

- [ ] **Step 4: Merge using inherited approval authority**

When exact HEAD required checks pass, unresolved threads are zero, and no P0/P1/USER_REVIEW_REQUIRED/CHANGE_PROPOSAL remains, merge without asking the user for another approval.
