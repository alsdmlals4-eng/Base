# Universal Loop v1 Closure Learning Reuse Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote five verified Universal Loop v1 closure lessons into existing Base validation/freshness contracts and synchronize the stale current Local Executor evidence ceiling.

**Architecture:** Extend the existing claim/intent validation reference and canonical-freshness Skill rather than adding a new Skill. Prove a focused RED that is explicitly consumed by Base-v9, bind the freshness body change to the existing recognized `tests/test_reference_freshness.py`, record the exact case in the freshness Skill's owner-local `LEARNING_LOG.md`, and update only the active Local Executor current-state section while preserving historical evidence. The owner-local log is an intentional post-RED refinement because the global log already contains earlier false-GREEN/test-consumption lessons and the existing coupled-change contract explicitly permits `skills/**/LEARNING_LOG.md`.

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
- Add/Modify: `tests/test_universal_loop_v1_closure_learning_reuse.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`
- Modify: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`

**Interfaces:**
- Consumes: existing `claim-and-intent-verification` mode and `COMPLETION_CLAIM_GATE`.
- Produces: explicit machine-evidence correction, test-consumption proof, latest-exact-head, and bounded-zero-escape contracts.

- [ ] **Step 1: Write the failing contract assertions and consume them**

Require:

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

Add the test module to Base-v9's explicit unittest command before treating CI as evidence.

- [ ] **Step 2: Verify RED**

Expected proof is not merely a started workflow: the Base-v9 log must show the new module in the actual command and its assertions must fail on the missing rules.

- [ ] **Step 3: Add the minimal reference rules**

Add a compact `Closure evidence hardening` section with:

```text
MACHINE_EVIDENCE_CORRECTION
TEST_CONSUMPTION_PROOF
LATEST_EXACT_HEAD_ONLY
BOUNDED_ZERO_ESCAPE
```

Do not create new modes, registries, schemas, or runtime code.

- [ ] **Step 4: Verify GREEN**

Run the same explicitly consumed regression and require pass.

---

### Task 2: Successor-aware canonical freshness

**Files:**
- Modify: `tests/test_reference_freshness.py`
- Modify: `skills/auditing-canonical-reference-freshness/SKILL.md`
- Add: `skills/auditing-canonical-reference-freshness/LEARNING_LOG.md`

**Interfaces:**
- Consumes: `CURRENT_MUTABLE`, `HISTORICAL_DISCOVERY`, `MISSING_PROPAGATION`, `CONFLICTING_SOURCE`.
- Produces: a successor-state propagation rule for mutable checkpoints and predecessor tests.

- [ ] **Step 1: Require the successor-state contract**

Require:

```python
for marker in (
    "VERIFIED_SUCCESSOR_STATE",
    "PREDECESSOR_CEILING_FREEZE",
    "CURRENT_MUTABLE",
    "HISTORICAL_DISCOVERY",
):
    self.assertIn(marker, skill)
```

The existing recognized freshness regression also carries a repository-level assertion so `.github/reference-freshness.json`'s coupled-change rule is genuinely satisfied.

- [ ] **Step 2: Verify RED**

Expected failure: the new successor-state contract is absent while existing freshness behavior remains green.

- [ ] **Step 3: Add minimal Skill guidance and local learning evidence**

Add:

```text
VERIFIED_SUCCESSOR_STATE
- historical evidence remains immutable
- CURRENT_MUTABLE consumers and predecessor regression assertions are re-inspected
- former NOT_RUN/0 ceilings cannot be permanently frozen as current truth
- unexplained frozen ceilings are PREDECESSOR_CEILING_FREEZE and become a propagation/content-drift finding
```

Record the #489–#494 case in the owner-local Learning Log rather than duplicating global historical lessons.

- [ ] **Step 4: Verify GREEN**

Run focused freshness regressions and canonical-reference freshness.

---

### Task 3: Synchronize the active Local Executor status

**Files:**
- Modify: `docs/LOOP_A2_LOCAL_EXECUTOR.md`
- Covered by: `tests/test_universal_loop_v1_closure_learning_reuse.py`

**Interfaces:**
- Consumes: #489 non-counting receipt, #490/#491/#492 counted receipts, #494 closure checkpoint.
- Produces: a current operational document consistent with the machine checkpoint.

- [ ] **Step 1: Require current live evidence**

Require:

```text
live_v4_user_pc_preflight: PASS
real_local_chatgpt_codex_call: PASS
blacksmith_real_burnin_runs: 3
```

and reject the old current-state values before `## Queue job`.

- [ ] **Step 2: Verify RED**

Expected failure: the active Local Executor document still says NOT_RUN/NOT_COMPLETED/0.

- [ ] **Step 3: Synchronize only the active current-state section**

Preserve queue, Docker, security and non-goal contracts and record exact provenance:

```text
Base runtime used by successful runs: f4deebfc06de828cc956e47220e829cd98b1eb09
Blacksmith authority: 6b241f28969410de78156c90cc10f33a067426a2
Diagnostic: #489 / BS_A2_DIAG_20260817_005 / non-counting
Counted: #490/#491/#492 / BS_A2_BURNIN_001_R1/R2/R3
Closure main: 2b8856054573f1a06297ac8e65f5ca009fa2daef
```

Do not rewrite historical evidence files or pretend the later closure SHA was the runtime used by the earlier burn-ins.

- [ ] **Step 4: Verify GREEN**

Run focused contract tests plus canonical reference freshness.

---

### Task 4: Exact-head review, merge, and remaining-work disposition

**Files:**
- No new runtime/product files unless exact-head validation exposes a propagation defect.
- Update PR/Issue metadata only after evidence exists.

**Interfaces:**
- Consumes: final feature head, current completed main, open PR/Issue inventory.
- Produces: merged reusable contract and evidence-backed remaining-work classification.

- [ ] **Step 1: Run exact-head repository gates**

Require:

```text
Base-v9 focused contracts: PASS
adversarial-gate: PASS
Game Project Operating System selected jobs + final ci-gate: PASS
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

```text
#368 / PR #369: IN_PROGRESS_OWNER — do not touch.
#393/#375: REMAINING_REAL_VISUAL_INTEGRATION — live Figma/Desktop/Tool Hub/Godot evidence still required; do not close from CI alone.
#395: CLOSED_NOT_PLANNED_SUPERSEDED — replaced by standalone Local Executor #397/#398; do not claim completed as-written.
A3/Scheduler: INTENTIONALLY_DEFERRED — do not open automatically.
```

No item is closed merely because adjacent functionality exists.
