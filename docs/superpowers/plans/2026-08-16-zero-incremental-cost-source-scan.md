# Zero Incremental Cost Source Scan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make zero incremental monetary cost a Base-wide work invariant and convert Periodic Source Scan from API-backed automated analysis into deterministic Queue preparation followed by user-directed ChatGPT research/review.

**Architecture:** Keep the existing Source Watchlist, ledger, Queue generator, Evidence Method, and copy-integration policy. Remove the active scheduler's model credentials, AI analysis invocation, repository mutation, PR creation, validator dispatch, and auto-merge; replace them with a bounded `AWAITING_CHATGPT_REVIEW` receipt. Bind the cost rule and zero-cost scheduler shape with regression tests.

**Tech Stack:** Markdown policy contracts, Bash orchestration, Python unittest contract tests, GitHub Actions.

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED` is the standing Base budget policy.
- No pay-as-you-go API, paid credit, new paid subscription, marketplace purchase, paid hosted compute, or separately metered service may be introduced by this change.
- Existing user subscriptions may be used only through included functionality that does not trigger separate metered billing.
- Cost uncertainty fails closed as `COST_GATE_BLOCKED`; do not make the live call.
- Periodic Source Queue preparation must not call OpenAI or any other paid/metered model API.
- Queue preparation is not a Source scan and must not update scan/contribution ledger state.
- Existing open PR branches remain read-only; current open PRs have no direct overlap with the planned paths.
- No direct main push, force push, `--admin`, ruleset bypass, or Evidence inflation.
- Required exact-head checks, unresolved review thread 0, current-main reconciliation, and post-merge readback remain mandatory.

---

### Task 1: Lock zero-cost policy and scheduler behavior with RED tests

**Files:**
- Create: `tests/test_zero_incremental_cost_policy.py`
- Modify: `tests/test_periodic_source_analysis_runner.py`
- Modify: `tests/test_periodic_source_scan_queue.py`

**Interfaces:**
- Consumes: current `AGENTS.md`, Periodic Source Queue workflow/runner/doc.
- Produces: static regression requirements for Base-wide cost policy and active zero-cost scheduler shape.

- [ ] **Step 1: Add Base-wide cost-policy assertions.**

Create `tests/test_zero_incremental_cost_policy.py` with assertions that `AGENTS.md` contains:

```text
ZERO_INCREMENTAL_COST_REQUIRED
COST_GATE_BLOCKED
pay-as-you-go
separately metered
```

and that the active Source workflow/runner do not contain:

```text
OPENAI_API_KEY
SOURCE_ANALYSIS_MODEL
python -m tools.periodic_source_analysis
gh pr create
gh workflow run validate-evidence-knowledge.yml
gh pr merge
```

- [ ] **Step 2: Rewrite scheduled-runner contract expectations.**

In `tests/test_periodic_source_analysis_runner.py`, require:

```text
ZERO_INCREMENTAL_COST_QUEUE_PREP
AWAITING_CHATGPT_REVIEW
ai_api_call
NONE
USER_DIRECTED_CHATGPT_REVIEW
```

Keep due-source rotation tests. Remove active-scheduler requirements for analysis PR creation, downstream validator dispatch, overlap checks, and merge.

- [ ] **Step 3: Rewrite Queue workflow expectations.**

In `tests/test_periodic_source_scan_queue.py`, require only the permissions and commands needed for deterministic Queue preparation, and explicitly reject model secrets/API invocation and repository/PR write authority.

- [ ] **Step 4: Commit RED tests.**

Expected exact behavior before implementation: the new cost-policy test and zero-cost scheduler assertions fail because current `AGENTS.md`, workflow, and runner still require API-backed analysis.

---

### Task 2: Add the Base-wide zero incremental cost gate

**Files:**
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: user standing constraint from the current task.
- Produces: `ZERO_INCREMENTAL_COST_REQUIRED` / `COST_GATE_BLOCKED` invariant used by all Base work.

- [ ] **Step 1: Add the invariant under work-entry gates.**

Add a concise rule that:

```text
ZERO_INCREMENTAL_COST_REQUIRED
```

forbids incremental paid execution by default, distinguishes already-included subscription use from separately metered API/credits, and fails closed as `COST_GATE_BLOCKED` when cost status is uncertain.

- [ ] **Step 2: Preserve existing protected boundaries.**

Do not alter security, branch-protection, approval, Evidence, or copy-integration authority.

- [ ] **Step 3: Run the focused cost-policy test.**

Expected: Base-wide policy assertions pass; scheduler assertions may remain RED until Task 3.

---

### Task 3: Convert Periodic Source Scan to zero-cost Queue preparation

**Files:**
- Modify: `.github/workflows/periodic-source-scan-queue.yml`
- Modify: `tools/run_periodic_source_scan_queue.sh`
- Modify: `docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md`

**Interfaces:**
- Consumes: `tools/periodic_source_scan_queue.py`, operations ledger read-only, GitHub Issue API.
- Produces: deterministic Queue Issue with state `AWAITING_CHATGPT_REVIEW` and no metered AI/API or repository mutation.

- [ ] **Step 1: Reduce workflow permissions and inputs.**

Keep:

```yaml
permissions:
  contents: read
```

At job level add only:

```yaml
permissions:
  contents: read
  issues: write
```

Remove `SOURCE_ANALYSIS_MODEL`, `SOURCE_SCAN_BATCH_SIZE` if unused, `OPENAI_API_KEY`, `actions: write`, `contents: write`, and `pull-requests: write` from the active Queue-preparation job.

- [ ] **Step 2: Replace the runner with bounded Queue preparation.**

Runner flow:

```text
validate GH_TOKEN/GH_REPO
→ render Queue from operations ledger
→ create/update [Periodic Source Scan Queue]
→ append zero-cost receipt
→ write source-analysis-status.json with AWAITING_CHATGPT_REVIEW
→ update Issue with final state
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

Do not invoke `tools.periodic_source_analysis`, inspect model auth, mutate ledgers, create repository branches/PRs, dispatch validators, or merge.

- [ ] **Step 3: Rewrite Queue documentation.**

Document the two-stage owner boundary:

```text
free deterministic scheduler = due-source Queue preparation only
user-directed ChatGPT review = actual web research and Evidence decisions
```

State explicitly that `AWAITING_CHATGPT_REVIEW` is neither `NO_CHANGE` nor a completed scan, and that later repository changes still use the ordinary latest-main copy-integration and exact-head gates.

- [ ] **Step 4: Run focused Queue tests.**

Expected: zero-cost policy, runner, and Queue workflow tests pass.

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
Validate Evidence-Based Game Development Knowledge when triggered
Dependency Review
```

and the focused Source Queue tests.

- [ ] **Step 2: Adversarially attack the change.**

Check:

```text
API key or model variable still reachable from active scheduled path
Queue preparation incorrectly marked as scan success or NO_CHANGE
ledger freshness updated without research
repository/PR write permission retained unnecessarily
existing copy-integration safety accidentally removed
paid service silently reintroduced through another command
manual ChatGPT review incorrectly claimed automatic
```

- [ ] **Step 3: Reconcile current main.**

If `main` moved, absorb latest completed `main` on the integration branch without modifying open owner PR branches, then rerun exact-head validation.

- [ ] **Step 4: Merge with expected head and ruleset enforcement.**

Require unresolved review threads = 0, P0/P1 = 0, and repository-required checks including `ci-gate` if applicable.

- [ ] **Step 5: Post-merge readback and operational proof.**

Verify merged `main` contains `ZERO_INCREMENTAL_COST_REQUIRED`, the active Queue workflow/runner contain no `OPENAI_API_KEY` or model analysis invocation, and the next push/manual Queue run reaches `AWAITING_CHATGPT_REVIEW` rather than `BLOCKED_MODEL_AUTH`.

## Rollback

Revert the merged change as one unit. Do not re-enable the prior API-backed scheduled analysis unless the user explicitly changes the zero-incremental-cost policy.