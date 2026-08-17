# Universal Loop v1 Closure Learning Reuse Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote five verified Universal Loop v1 closure lessons into existing Base validation/freshness contracts and synchronize the stale current Local Executor evidence ceiling.

**Architecture:** Extend the existing claim/intent validation reference and canonical-freshness Skill rather than adding a new Skill. Bind both behavior changes to existing consumed regression modules, record the reusable learning in the global learning log, and update only the active Local Executor current-state section while preserving historical evidence.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions Base-v9/GPO validation, GitHub exact-SHA evidence.

## Global Constraints

- Baseline completed main: `2b8856054573f1a06297ac8e65f5ca009fa2daef`.
- Do not modify unrelated open/draft/ready PR branches.
- No runtime/provider/Tool Hub implementation or Blacksmith product change.
- `paid_openai_api=FORBIDDEN` and `api_key_fallback=FORBIDDEN` remain unchanged.
- `a3_auto_merge=DISABLED` and `scheduler=NOT_CONFIGURED` remain unchanged.
- Historical PR/SHA/run/evidence records keep their historical values.
- Current mutable status may advance only from exact machine evidence already recorded in merged main.

---

### Task 1: Claim-verification closure lessons

**Files:**
- Modify: `tests/test_claim_and_intent_verification_contract.py`
- Modify: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`

**Interfaces:**
- Consumes: existing `claim-and-intent-verification` mode and `COMPLETION_CLAIM_GATE`.
- Produces: explicit machine-evidence correction, test-consumption proof, latest-exact-head, and bounded-zero-escape contracts.

- [ ] **Step 1: Write the failing contract assertions**

Extend `test_reference_is_fail_closed_and_evidence_bounded` or add a focused test requiring all of these literal contract markers and meanings:

```python
for marker in (
    "MACHINE_EVIDENCE_CORRECTION",
    "TEST_CONSUMPTION_PROOF",
    "LATEST_EXACT_HEAD_ONLY",
    "BOUNDED_ZERO_ESCAPE",
    "workflow trigger",
    "receipt digest",
    "stale-head",
):
    self.assertIn(marker, reference)
```

Also require text stating that a trigger/path match is not execution evidence and that summary prose is corrected when exact terminal evidence contradicts it.

- [ ] **Step 2: Verify RED**

Run the existing consumed regression through the repository CI path. Expected failure: only the new markers/semantics are absent from `claim-and-intent-verification.md`; existing contract assertions remain green.

- [ ] **Step 3: Add the minimal reference rules**

Add a compact `Closure evidence hardening` section with exactly these rules:

```text
MACHINE_EVIDENCE_CORRECTION
TEST_CONSUMPTION_PROOF
LATEST_EXACT_HEAD_ONLY
BOUNDED_ZERO_ESCAPE
```

Do not create new modes, registries, schemas, or runtime code.

- [ ] **Step 4: Verify GREEN**

Run the same regression and require all assertions to pass.

- [ ] **Step 5: Commit**

Commit the test/reference pair together.

---

### Task 2: Successor-aware canonical freshness

**Files:**
- Modify: `tests/test_reference_freshness.py`
- Modify: `skills/auditing-canonical-reference-freshness/SKILL.md`

**Interfaces:**
- Consumes: `CURRENT_MUTABLE`, `HISTORICAL_DISCOVERY`, `MISSING_PROPAGATION`, `CONFLICTING_SOURCE`.
- Produces: a successor-state propagation rule for mutable checkpoints and predecessor tests.

- [ ] **Step 1: Write the failing contract assertion**

Add a repository-level contract test that reads the canonical Skill and requires:

```python
for marker in (
    "VERIFIED_SUCCESSOR_STATE",
    "PREDECESSOR_CEILING_FREEZE",
    "CURRENT_MUTABLE",
    "HISTORICAL_DISCOVERY",
):
    self.assertIn(marker, skill)
```

Require the text to say that historical provenance stays exact while current mutable tests/consumers must be inspected when a verified state advances.

- [ ] **Step 2: Verify RED**

Run the existing reference-freshness regression path. Expected failure: the new successor-state contract is absent; the freshness checker’s existing behavior remains green.

- [ ] **Step 3: Add minimal Skill guidance**

Add one subsection under impact/propagation handling:

```text
VERIFIED_SUCCESSOR_STATE
- historical evidence remains immutable
- CURRENT_MUTABLE consumers and predecessor regression assertions are re-inspected
- former NOT_RUN/0 ceilings cannot be permanently frozen as current truth
- unexplained frozen ceilings are PREDECESSOR_CEILING_FREEZE and become a propagation/content-drift finding
```

- [ ] **Step 4: Verify GREEN**

Run the same reference-freshness regression and require pass.

- [ ] **Step 5: Commit**

Commit the test/Skill pair together.

---

### Task 3: Record learning and synchronize the active Local Executor status

**Files:**
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `docs/LOOP_A2_LOCAL_EXECUTOR.md`

**Interfaces:**
- Consumes: #489 non-counting receipt, #490/#491/#492 counted receipts, #494 closure checkpoint.
- Produces: reusable learning record and a current operational document consistent with the machine checkpoint.

- [ ] **Step 1: Add a regression assertion before current-state edits**

Extend the claim/intent regression to require the learning log to contain a `2026-08-17 — Universal Loop v1 closure evidence hardening` entry and require `docs/LOOP_A2_LOCAL_EXECUTOR.md` to contain:

```text
live_v4_user_pc_preflight: PASS
real_local_chatgpt_codex_call: PASS
blacksmith_real_burnin_runs: 3
```

and no longer contain those three old current-state values in its `Current evidence ceiling` block.

- [ ] **Step 2: Verify RED**

Expected failures: the learning entry is absent and the active Local Executor document still says NOT_RUN/NOT_COMPLETED/0.

- [ ] **Step 3: Write the reusable learning entry**

Record:

```text
status: PATTERN
trigger: #494 REAL A2 closure
lessons: machine evidence correction; test-consumption proof; successor-aware mutable state; latest exact-head; bounded zero-escape
boundary: no new Skill; historical evidence not rewritten; no game-wide quality claim
verification: #494 exact-head + postmerge Base-v9/GPO; #489/#490/#491/#492 exact receipt identities
next trigger: recurrence in another lifecycle or a false-green/frozen-successor regression
```

- [ ] **Step 4: Synchronize only the active current-state section**

Update `docs/LOOP_A2_LOCAL_EXECUTOR.md` current evidence to the verified live state while preserving the document’s architecture, queue, Docker, security, and non-goal contracts. Include the exact closure provenance:

```text
Base runtime used by successful runs: f4deebfc06de828cc956e47220e829cd98b1eb09
Blacksmith authority: 6b241f28969410de78156c90cc10f33a067426a2
Diagnostic: #489 / BS_A2_DIAG_20260817_005 / non-counting
Counted: #490/#491/#492 / BS_A2_BURNIN_001_R1/R2/R3
Closure main: 2b8856054573f1a06297ac8e65f5ca009fa2daef
```

Do not rewrite historical evidence files.

- [ ] **Step 5: Verify GREEN**

Run focused contract tests plus canonical reference freshness.

- [ ] **Step 6: Commit**

Commit learning/current-state synchronization with its regression.

---

### Task 4: Exact-head review, merge, and remaining-work disposition

**Files:**
- No new production files unless exact-head validation exposes a propagation defect.
- Update PR/Issue metadata only after evidence exists.

**Interfaces:**
- Consumes: final feature head, current completed main, open PR/Issue inventory.
- Produces: merged reusable contract and evidence-backed remaining-work classification.

- [ ] **Step 1: Run exact-head repository gates**

Require:

```text
Base-v9 focused contracts: PASS
adversarial-gate: PASS
Game Project Operating System docs/contract/publication/Windows/final ci-gate: PASS as selected by risk classifier
canonical reference freshness: PASS
```

- [ ] **Step 2: Adversarial scope review**

Confirm:

```text
new broad Skill: 0
runtime/provider files changed: 0
Blacksmith product files changed: 0
unrelated in-progress PR branches modified: 0
unresolved review threads: 0
same-goal open PRs besides this PR: 0
```

- [ ] **Step 3: Re-read current main before merge**

If completed main advanced, reconcile only completed-main changes. Never rebase or edit unrelated active PR branches.

- [ ] **Step 4: Merge and postmerge verify**

Mark ready only after exact-head gates pass, squash merge with expected head, then read back new main and require postmerge Base-v9/GPO success.

- [ ] **Step 5: Classify remaining Loop work**

Use these dispositions:

```text
#368 / PR #369: IN_PROGRESS_OWNER — do not touch.
#393/#375: REMAINING_REAL_VISUAL_INTEGRATION — live Figma/Desktop/Tool Hub/Godot evidence still required; do not close from CI alone.
#395: inspect current standalone Local Executor authority; close as NOT_PLANNED_SUPERSEDED only if no active PR owns it and current canonical architecture clearly replaces Tool-Hub-embedded broker semantics.
A3/Scheduler: INTENTIONALLY_DEFERRED — do not open automatically.
```

No item is closed merely because adjacent functionality exists.
