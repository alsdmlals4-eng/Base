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
- A completion receipt contains at least one check and one destination readback; empty arrays cannot be used as verified evidence.
- `SYNCED` requires destination readback equality.
- Zero incremental paid services.

---

### Task 1: Define failing completion contract tests

**Files:**
- Create: `tests/test_loop_completion_gate.py`

**Interfaces:**
- Consumes: existing Base Loop template bundle.
- Produces: expected API `validate_completion(capsule_path: Path) -> list[Finding]` and completion failure codes.

- [x] **Step 1: Write failing tests**

Tests require:

```python
from tools.loop_contracts.bundle_validation import validate_bundle, validate_completion
```

and prove readiness may accept a `MAPPED` requirement while completion rejects it, plus cases for required `NOT_RUN`, stale destination refs, a fully verified receipt, and empty check/destination bypass attempts.

- [x] **Step 2: Run focused CI and verify RED**

Initial RED: completion API/CLI absent. Adversarial RED: empty `checks=[]` or `destinations=[]` was accepted before schema hardening.

### Task 2: Add verification receipt schema/template

**Files:**
- Create: `schemas/loop-verification-receipt-v1.schema.json`
- Create: `templates/project-operations/loop/VERIFICATION_RECEIPT.json`
- Modify: `schemas/loop-project-execution-capsule-v1.schema.json`
- Modify: `templates/project-operations/loop/PROJECT_EXECUTION_CAPSULE.json`
- Modify: `tests/test_loop_execution_capsule_contracts.py`

**Interfaces:**
- Produces optional capsule field `verification_receipt_path` and schema role `LOOP_VERIFICATION_RECEIPT`.

- [x] **Step 1: Define schema**

The receipt contains identity, `exact_head_sha`, overall status, non-empty `checks[]`, and non-empty `destinations[]` with fail-closed enums.

- [x] **Step 2: Add Base template receipt and optional path**

Existing project capsules remain schema-valid without the optional path; Base's current template opts in.

- [x] **Step 3: Add schema/template inventory coverage**

The verification receipt schema and template are part of the explicit Loop contract inventory tests.

### Task 3: Implement completion validator and CLI phase

**Files:**
- Modify: `tools/loop_contracts/bundle_validation.py`
- Modify: `tools/check_loop_execution_capsule.py`
- Test: `tests/test_loop_completion_gate.py`

**Interfaces:**
- Produces: `validate_completion(capsule_path: Path) -> list[Finding]`.
- CLI: `--phase readiness|completion`, default `readiness`.

- [x] **Step 1: Implement minimal validator**

Completion calls readiness validation first, then loads the optional receipt path fail-closed. It verifies identity, coverage closure, required checks, reasons for omissions, and required destination freshness.

- [x] **Step 2: Make CLI select the validator**

```python
parser.add_argument("--phase", choices=("readiness", "completion"), default="readiness")
findings = validate_bundle(args.capsule) if args.phase == "readiness" else validate_completion(args.capsule)
```

- [x] **Step 3: Run RED→GREEN CI**

Readiness backward compatibility and completion behavior are verified through PR GitHub Actions; final exact-head Green is required again after all review fixes.

### Task 4: Document the operational rule without duplicating global policy

**Files:**
- Create: `docs/COMPLETION_AND_DESTINATION_FRESHNESS_GATE.md`

**Interfaces:**
- Consumes: existing post-merge and Loop Engineering policies.
- Produces: one narrow owner for completion-vs-readiness semantics and destination readback receipts.

- [x] **Step 1: Document the state machine**

Includes readiness/completion separation, required-check behavior, non-empty receipt evidence, `SYNCED` readback rule, external connector boundary, rollback, and downstream adoption guidance.

- [ ] **Step 2: Run final Base documentation/core regression CI**

Expected: all required Base checks Green on final exact head.

### Task 5: COC-Fiction factual freshness correction and pilot

**Files/Surfaces:**
- Notion Project Registry row for `COC_FICTION`.
- Notion `08 · Continuity · Publication Handoff` current-state block.
- Project repository only if a non-overlapping project-local receipt adapter is justified after Base merge.

**Interfaces:**
- Consumes: fresh COC-Fiction `main`, `fiction/ACTIVE_CONTEXT.md`, `fiction/FICTION_MASTER.md`.
- Produces: truthful Notion current state and readback evidence.

- [x] **Step 1: Re-read fresh GitHub main and open PRs**
- [x] **Step 2: Update only stale current-state fields/content**
- [x] **Step 3: Re-read Notion and verify SHA/frontier equality**
- [x] **Step 4: Keep fiction/canon/manuscript unchanged**

### Task 6: Audit other active projects and apply only verified gaps

**Files/Surfaces:**
- Notion Project Registry active projects.
- Each project's GitHub main.
- Current project Loop capsule state where present.

- [x] **Step 1: Build an evidence table**

Compared every active Project Registry SHA/sync state against its actual GitHub main.

- [x] **Step 2: Classify**

`NO_CHANGE / NOTION_STALE / REPO_UPDATE_REQUIRED / DORMANT_LOOP_NO_RETROFIT`.

- [x] **Step 3: Apply bounded corrections**

My Little Boat's false `SYNCED` stale SHA was corrected and read back. Other matching projects were not edited. Tetris keeps its intentional `REPO_UPDATE_REQUIRED` state. Dormant historical Loop capsules are not retrofitted.

- [x] **Step 4: Destination readback and rollback check**

Changed Notion destinations were re-read after mutation.

### Task 7: Five adversarial loops and merge/readback

**Files:**
- No new files unless a verified finding requires a bounded fix.

- [ ] **Step 1: Complete at least five full-scope adversarial loops**
- [ ] **Step 2: Validate findings against source authority and apply only verified minimal corrections**
- [ ] **Step 3: Run final regression/exact-head checks**
- [ ] **Step 4: Merge only after zero unresolved threads, current-main freshness, and exact-head evidence**
- [ ] **Step 5: Post-merge GitHub/Notion readback and remaining-work recalculation**
