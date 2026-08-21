# Semantic Completion + Destination Freshness Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fail-closed completion phase that proves requirement closure, required validation execution, and destination freshness without changing current readiness behavior.

**Architecture:** Keep `validate_bundle()` as the pre-execution/readiness validator. Add a standalone verification receipt plus `validate_completion()` and a CLI phase selector. Pilot factual destination freshness on COC-Fiction, then audit other active projects and change only verified stale states.

**Tech Stack:** Python 3.12, jsonschema Draft 2020-12, GitHub Actions, Notion connector/readback.

**Spec:** `docs/superpowers/specs/2026-08-21-semantic-completion-destination-freshness-design.md`

## Global Constraints

- Open/draft/ready PRs are read-only unless the user explicitly names the PR and permitted mutation.
- Existing readiness semantics must remain backward compatible.
- No new active Skill, Slack bot, or vendor-specific hook becomes Base authority.
- Required `NOT_RUN`, `SKIPPED`, or `FAIL` blocks completion.
- `SYNCED` requires destination readback equality.
- Zero incremental paid services.

---

### Task 1: Define failing completion contract tests

**Files:**
- Modify: `tests/test_loop_execution_capsule_contracts.py`

**Interfaces:**
- Consumes: existing Base Loop template bundle.
- Produces: expected API `validate_completion(capsule_path: Path) -> list[Finding]` and completion failure codes.

- [ ] **Step 1: Write failing tests**

Add tests that require:

```python
from tools.loop_contracts.bundle_validation import validate_bundle, validate_completion
```

and assert:

```python
assert validate_bundle(capsule_path) == []
assert "COMPLETION_REQUIREMENT_OPEN" in {
    item.code for item in validate_completion(capsule_path)
}
```

for a `MAPPED` requirement, plus cases for required `NOT_RUN`, stale destination refs, and a fully verified receipt.

- [ ] **Step 2: Run focused CI and verify RED**

Run via PR GitHub Actions. Expected: failure because `validate_completion` and/or the verification receipt contract do not exist yet.

### Task 2: Add verification receipt schema/template

**Files:**
- Create: `schemas/loop-verification-receipt-v1.schema.json`
- Create: `templates/project-operations/loop/VERIFICATION_RECEIPT.json`
- Modify: `schemas/loop-project-execution-capsule-v1.schema.json`
- Modify: `templates/project-operations/loop/PROJECT_EXECUTION_CAPSULE.json`
- Modify: `tests/test_loop_execution_capsule_contracts.py`

**Interfaces:**
- Produces optional capsule field `verification_receipt_path` and schema role `LOOP_VERIFICATION_RECEIPT`.

- [ ] **Step 1: Define schema**

The receipt contains identity, `exact_head_sha`, overall status, `checks[]`, and `destinations[]` with fail-closed enums.

- [ ] **Step 2: Add Base template receipt and optional path**

Existing project capsules remain schema-valid without the optional path; Base's current template opts in.

- [ ] **Step 3: Run schema/template tests**

Expected: template bundle and explicit receipt schema tests pass.

### Task 3: Implement completion validator and CLI phase

**Files:**
- Modify: `tools/loop_contracts/bundle_validation.py`
- Modify: `tools/check_loop_execution_capsule.py`
- Modify: `tests/test_loop_execution_capsule_contracts.py`

**Interfaces:**
- Produces: `validate_completion(capsule_path: Path) -> list[Finding]`.
- CLI: `--phase readiness|completion`, default `readiness`.

- [ ] **Step 1: Implement minimal validator**

Completion calls readiness validation first, then loads the optional receipt path fail-closed. It verifies identity, coverage closure, required checks, reasons for omissions, and required destination freshness.

- [ ] **Step 2: Make CLI select the validator**

```python
parser.add_argument("--phase", choices=("readiness", "completion"), default="readiness")
findings = validate_bundle(args.capsule) if args.phase == "readiness" else validate_completion(args.capsule)
```

- [ ] **Step 3: Run focused tests**

Expected: RED cases now pass and readiness backward-compatibility remains Green.

### Task 4: Document the operational rule without duplicating global policy

**Files:**
- Create: `docs/COMPLETION_AND_DESTINATION_FRESHNESS_GATE.md`

**Interfaces:**
- Consumes: existing post-merge and Loop Engineering policies.
- Produces: one narrow owner for completion-vs-readiness semantics and destination readback receipts.

- [ ] **Step 1: Document the state machine**

Include readiness/completion separation, required-check behavior, `SYNCED` readback rule, external connector boundary, rollback, and downstream adoption guidance.

- [ ] **Step 2: Run Base documentation/core regression CI**

Expected: all required Base checks Green.

### Task 5: COC-Fiction factual freshness correction and pilot

**Files/Surfaces:**
- Notion Project Registry row for `COC_FICTION`.
- Notion `08 · Continuity · Publication Handoff` current-state block.
- Project repository only if a non-overlapping project-local receipt adapter is justified after Base merge.

**Interfaces:**
- Consumes: fresh COC-Fiction `main`, `fiction/ACTIVE_CONTEXT.md`, `fiction/FICTION_MASTER.md`.
- Produces: truthful Notion current state and readback evidence.

- [ ] **Step 1: Re-read fresh GitHub main and open PRs**
- [ ] **Step 2: Update only stale current-state fields/content**
- [ ] **Step 3: Re-read Notion and verify SHA/frontier equality**
- [ ] **Step 4: Keep fiction/canon/manuscript unchanged**

### Task 6: Audit other active projects and apply only verified gaps

**Files/Surfaces:**
- Base active-project registry/adoption data for project list.
- Each project's GitHub main/open PR state.
- Corresponding Notion Project Registry/Home current-state fields.

- [ ] **Step 1: Build an evidence table**

For each active project record actual GitHub main, Notion recorded SHA/sync state, and whether a current completion contract is in use.

- [ ] **Step 2: Classify**

`NO_CHANGE / NOTION_STALE / REPOSITORY_ADOPTION_CANDIDATE / DEFER_OPEN_PR / BLOCKED_UNVERIFIED`.

- [ ] **Step 3: Apply bounded corrections**

Only factual Notion freshness corrections and non-overlapping approved Base completion-adoption work are allowed.

- [ ] **Step 4: Destination readback and rollback check**

Every changed project must be re-read after mutation.

### Task 7: Five adversarial loops and merge/readback

**Files:**
- No new files unless a verified finding requires a bounded fix.

- [ ] **Step 1: Attack full approved scope**
- [ ] **Step 2: Validate findings against source authority**
- [ ] **Step 3: Apply only verified minimal corrections**
- [ ] **Step 4: Run regression/exact-head checks**
- [ ] **Step 5: Repeat full loop at least five times and until clean**
- [ ] **Step 6: Merge only after zero unresolved threads, current-main freshness, and exact-head evidence**
- [ ] **Step 7: Post-merge GitHub/Notion readback and remaining-work recalculation**
