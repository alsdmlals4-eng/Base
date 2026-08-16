# Zero Incremental Cost Source Scan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make zero incremental monetary cost a Base-wide work invariant and convert Periodic Source Scan from metered automated analysis into deterministic Queue preparation followed by user-directed ChatGPT research/review.

**Architecture:** Keep the existing Source Watchlist, ledger, Queue generator, Evidence Method, cost-policy owner, and copy-integration policy. `AGENTS.md` binds the always-on cost invariant; `docs/CI_EXECUTION_COST_POLICY.md` remains the detailed CI/runner cost authority. Remove the active Source scheduler's model credentials, AI analysis invocation, repository mutation, PR creation, validator dispatch, and auto-merge; replace them with a bounded `AWAITING_CHATGPT_REVIEW` receipt. Bind the cost rule and zero-cost scheduler shape through existing Source contract suites so no duplicate test workflow is created.

**Tech Stack:** Markdown policy contracts, Bash orchestration, Python unittest contract tests, GitHub Actions.

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED` is the standing Base budget policy.
- `docs/CI_EXECUTION_COST_POLICY.md` remains the specialized CI cost owner; do not create a duplicate policy owner.
- No pay-as-you-go API, paid credit, new paid subscription, marketplace purchase, paid hosted compute, or separately metered service may be introduced by this change.
- Existing user subscriptions may be used only through included functionality that does not trigger separate metered billing.
- Cost uncertainty fails closed as `COST_GATE_BLOCKED`; do not make the live call.
- Periodic Source Queue preparation must not call any paid/metered model API.
- Queue preparation is not a Source scan and must not update scan/contribution ledger state.
- Existing open PR branches remain read-only; current open PRs have no direct overlap with the planned paths.
- No direct main push, force push, `--admin`, ruleset bypass, or Evidence inflation.
- Required exact-head checks, unresolved review thread 0, current-main reconciliation, and post-merge readback remain mandatory.

---

### Task 1: Lock zero-cost policy and scheduler behavior with RED tests

**Files:**
- Modify: `tests/test_periodic_source_analysis_runner.py`
- Modify: `tests/test_periodic_source_scan_queue.py`

**Interfaces:**
- Consumes: current `AGENTS.md`, existing `docs/CI_EXECUTION_COST_POLICY.md`, Periodic Source Queue workflow/runner/doc.
- Produces: executed regression requirements for Base-wide cost policy and active zero-cost scheduler shape without adding a new test workflow.

- [x] **Step 1: Add Base-wide cost-policy assertions to an existing executed Source test owner.**

Require `AGENTS.md` to contain:

```text
ZERO_INCREMENTAL_COST_REQUIRED
COST_GATE_BLOCKED
pay-as-you-go
separately metered
docs/CI_EXECUTION_COST_POLICY.md
```

and verify the existing CI cost owner remains present.

- [x] **Step 2: Rewrite scheduled-runner contract expectations.**

In `tests/test_periodic_source_analysis_runner.py`, require:

```text
ZERO_INCREMENTAL_COST_QUEUE_PREP
AWAITING_CHATGPT_REVIEW
ai_api_call
NONE
USER_DIRECTED_CHATGPT_REVIEW
```

Keep due-source rotation tests. Remove active-scheduler requirements for analysis PR creation, downstream validator dispatch, overlap checks, and merge.

- [x] **Step 3: Rewrite Queue workflow expectations.**

In `tests/test_periodic_source_scan_queue.py`, require only the permissions and commands needed for deterministic Queue preparation, and reject model/API execution and repository/PR write authority.

- [x] **Step 4: Observe RED before implementation.**

Observed on exact branch head `88e9a189d3e3c20a8b02c27a08999620965fae79`: Evidence Knowledge run `31950032241` executed 107 tests and failed only the four new zero-cost/Queue expectations because the active workflow, runner, Queue doc, and top-level policy still represented the prior metered path.

---

### Task 2: Add the Base-wide zero incremental cost gate

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/CI_EXECUTION_COST_POLICY.md`

**Interfaces:**
- Consumes: user standing constraint from the current task and the existing CI cost owner.
- Produces: `ZERO_INCREMENTAL_COST_REQUIRED` / `COST_GATE_BLOCKED` invariant used by all Base work while preserving the detailed CI owner.

- [x] **Step 1: Add the invariant under work-entry gates.**

`AGENTS.md` forbids incremental paid execution by default, distinguishes already-included subscription use from separately metered API/credits/services, and fails closed as `COST_GATE_BLOCKED` when cost status is uncertain.

- [x] **Step 2: Reconcile the existing CI cost owner.**

`docs/CI_EXECUTION_COST_POLICY.md` now subordinates `REMOTE_CI`/runner selection to the zero-incremental-cost Gate and does not assume a potentially metered runner may execute merely because it is available.

- [x] **Step 3: Preserve existing protected boundaries.**

Security, branch protection, approval, Evidence, `REMOTE_CI`/`LOCAL_FALLBACK`, and copy-integration authority remain in their existing owners.

---

### Task 3: Convert Periodic Source Scan to zero-cost Queue preparation

**Files:**
- Modify: `.github/workflows/periodic-source-scan-queue.yml`
- Modify: `tools/run_periodic_source_scan_queue.sh`
- Modify: `docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md`

**Interfaces:**
- Consumes: `tools/periodic_source_scan_queue.py`, operations ledger read-only, GitHub Issue API.
- Produces: deterministic Queue Issue with state `AWAITING_CHATGPT_REVIEW` and no metered AI/API or repository mutation.

- [x] **Step 1: Reduce workflow permissions and inputs.**

The active job keeps only repository read and Issue write authority. Model variables/credentials, Actions dispatch write, repository contents write, and pull-request write are removed from the scheduled path.

- [x] **Step 2: Replace the runner with bounded Queue preparation.**

Runner flow:

```text
validate GH_TOKEN/GH_REPO
→ render Queue from operations ledger
→ write zero-cost receipt
→ create/update [Periodic Source Scan Queue]
→ state AWAITING_CHATGPT_REVIEW
→ exit 0
```

Required receipt:

```yaml
mode: ZERO_INCREMENTAL_COST_QUEUE_PREP
ai_api_call: NONE
repository_change: NONE
ledger_scan_timestamp_change: NONE
candidate_evidence_claim: NOT_RUN
next_executor: USER_DIRECTED_CHATGPT_REVIEW
```

It does not invoke the manual analysis module, inspect model auth, mutate ledgers, create repository branches/PRs, dispatch validators, or merge.

- [x] **Step 3: Rewrite Queue documentation.**

The current owner explicitly separates:

```text
free deterministic scheduler = due-source Queue preparation only
user-directed ChatGPT review = actual web research and Evidence decisions
```

`AWAITING_CHATGPT_REVIEW` is neither `NO_CHANGE` nor a completed scan, and later repository changes still use ordinary latest-main copy-integration and exact-head gates.

- [ ] **Step 4: Run focused Queue tests and full exact-head regression.**

Expected: zero-cost policy, runner, Queue workflow, Base v9, Evidence Knowledge, and Game Project OS contracts all pass on the final exact head.

---

### Task 4: GREEN validation, adversarial review, merge, and post-merge operational proof

**Files:**
- No new production paths unless an in-scope validation mismatch is found.

**Interfaces:**
- Consumes: Tasks 1-3 exact branch head.
- Produces: merged zero-cost policy and observed post-merge Queue preparation state.

- [ ] **Step 1: Run/observe exact-head required checks.**

At minimum:

```text
Validate Base v9 Operating Contracts
Validate Game Project Operating System
Validate Evidence-Based Game Development Knowledge
Dependency Review when triggered
```

and the focused Source Queue tests.

- [ ] **Step 2: Adversarially attack the change.**

Check:

```text
metered model credential or invocation still reachable from active scheduled path
Queue preparation incorrectly marked as scan success or NO_CHANGE
ledger freshness updated without research
repository/PR write permission retained unnecessarily
existing copy-integration safety accidentally removed
paid service silently reintroduced through another command
manual ChatGPT review incorrectly claimed automatic
duplicate cost-policy owner introduced
```

- [ ] **Step 3: Reconcile current main.**

If `main` moved, absorb latest completed `main` on the integration branch without modifying open owner PR branches, then rerun exact-head validation.

- [ ] **Step 4: Merge with expected head and ruleset enforcement.**

Require unresolved review threads = 0, P0/P1 = 0, and repository-required checks including `ci-gate` if applicable.

- [ ] **Step 5: Post-merge readback and operational proof.**

Verify merged `main` contains `ZERO_INCREMENTAL_COST_REQUIRED`, the active Queue workflow/runner expose only zero-cost Queue preparation, and the next push/manual Queue run reaches `AWAITING_CHATGPT_REVIEW` rather than a model-auth blocked state.

## Rollback

Revert the merged change as one unit. Do not re-enable the prior metered scheduled analysis unless the user explicitly changes the zero-incremental-cost policy.