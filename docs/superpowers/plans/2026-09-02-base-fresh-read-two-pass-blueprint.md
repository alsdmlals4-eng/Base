# Base Fresh-Read and Two-Pass Blueprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every fresh Base read discover a bounded revision lifecycle and a two-pass Blueprint workflow: structural Blueprint draft → required image/material preparation → final Blueprint → exact-revision Godot implementation.

**Architecture:** Extend the existing V4 workspace machine authority rather than creating a new router or Skill. Keep the Blueprint as two revisions inside the existing PDF + AI Markdown artifacts, propagate the sequence through the current two-artifact, image, and Codex handoff consumers, and enforce it with focused regression tests.

**Tech Stack:** Markdown contracts, JSON machine authority, Python `unittest`, GitHub branch/PR/Actions.

**Spec:** `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`

## Global Constraints

- Baseline is exact completed Base `main` SHA `a5a1e7eecc4c58a13c11b98b6c225cb1879e7167`; re-read current `main` at every integration boundary.
- Do not modify, absorb, rebase, close, or merge pre-existing PRs. In particular, paths owned by open PRs #837, #802, and #803 remain read-only.
- Do not edit `AGENTS.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, the intake Skill, or UI adapter/readiness files in this workstream.
- Latest Base discovery must not silently replace a project's adopted Base contract or project canon.
- The selected Base execution SHA stays fixed during one bounded task/Slice; later Base changes require impact classification before adoption.
- Blueprint pass 1 and pass 2 are revisions inside the existing two-artifact profile, not additional deliverables or parallel canon.
- Required image/material preparation is consumer-bounded and does not mean producing every future project asset.
- Static tests prove contract propagation only; they do not prove Godot runtime, visual quality, player UX, device, or release readiness.
- Repository integration uses normal expected-head squash merge only; no direct `main` push, force push, or ruleset bypass.

---

### Task 1: Add the regression contract first

**Files:**
- Create: `tests/test_base_fresh_read_two_pass_blueprint_contract.py`
- Modify later: `tests/test_project_master_gdd_two_artifact_contract.py`

**Interfaces:**
- Consumes: V4 machine contract, two-artifact policy/instruction, image workflow owners, and Codex implementation handoff.
- Produces: executable assertions for revision fields, forbidden pin modes, two-pass sequence, bounded asset/VFX preparation, and final-Blueprint handoff metadata.

- [ ] **Step 1: Create the focused failing test**

Assert that the V4 contract exposes `base_observed_head_sha`, `base_adopted_contract_sha`, and `base_execution_sha`; that all Blueprint consumers contain the same pass-1 → materials → pass-2 sequence; and that Codex receives the final approved Blueprint revision.

- [ ] **Step 2: Run the focused test against the unchanged baseline**

Run:

```bash
python -m unittest tests.test_base_fresh_read_two_pass_blueprint_contract -v
```

Expected: FAIL because the three-revision lifecycle and `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT` do not yet exist.

- [ ] **Step 3: Preserve the RED evidence**

Record the exact failing branch HEAD and workflow run. Do not call the baseline green.

### Task 2: Extend the V4 machine authority

**Files:**
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`

**Interfaces:**
- Consumes: current repository-first authority and exact-SHA Codex rehydration.
- Produces: `base_revision_lifecycle`, `blueprint_preimplementation_lifecycle`, and stable required field names used by templates and tests.

- [ ] **Step 1: Add the bounded Base revision lifecycle**

Add machine-readable values for:

```text
LATEST_BASE_DISCOVERY_REQUIRED
PIN_IS_EVIDENCE_NOT_FRESHNESS_BYPASS
PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED
BASE_DRIFT_CLASSIFICATION_REQUIRED
BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK
NO_PERMANENT_STALE_PIN
NO_FLOATING_EXECUTION
BOUNDARY_FRESH_READ_REQUIRED
```

- [ ] **Step 2: Add the two-pass Blueprint lifecycle**

Use the ordered lifecycle:

```text
PLAN
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

Declare `BLUEPRINT_REVIEW_PUBLICATION` as `BLUEPRINT_PASS_2_FINAL` without creating another artifact.

- [ ] **Step 3: Preserve project authority invariants**

Add invariants stating that latest Base never silently overrides project canon/adopted contract and that a later Base change is classified before the bounded execution pin changes.

- [ ] **Step 4: Validate JSON**

Run:

```bash
python -m json.tool docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json > /dev/null
```

Expected: exit 0.

### Task 3: Propagate the two-pass Blueprint through planning and image consumers

**Files:**
- Modify: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
- Modify: `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`

**Interfaces:**
- Consumes: V4 lifecycle tokens and existing two-artifact/image approval boundaries.
- Produces: one consistent human-readable process and compatibility meaning for legacy `PLAN` sequence references.

- [ ] **Step 1: Define project-wide breadth and Slice depth**

Add `PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH`: map all material project systems and boundaries, but make only the next play-meaningful Slice implementation-ready in depth.

- [ ] **Step 2: Define Blueprint pass 1**

Add `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT` and `STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT`. Require Flow, screen inventory, representative low-fidelity wireframes, entry/exit/cancel/re-entry, state/data/system flow, and actual/planned consumer records before asset production.

- [ ] **Step 3: Bound image/material preparation**

Add `REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`. Reuse first; prepare only current-Slice P0/P1 and necessary P2 image, UI, animation, audio, VFX source, reference, and data materials.

- [ ] **Step 4: Split VFX preparation from Godot implementation**

Before the final Blueprint, specify VFX purpose, trigger, timing, layer, storyboard, source texture/mask, reduced-motion equivalent, budget, and fallback. Keep particles, shader, `AnimationPlayer`, Tween, Signal wiring, interruption behavior, performance measurement, and runtime tuning under `ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`.

- [ ] **Step 5: Define Blueprint pass 2**

Keep `BLUEPRINT_REVIEW_PUBLICATION` as the compatibility token and identify it as `BLUEPRINT_PASS_2_FINAL`, integrating reviewed/locked candidates and final implementation/acceptance traceability.

- [ ] **Step 6: Preserve evidence ceilings**

Candidate generation remains distinct from user approval, canon registration, implementation, and runtime verification.

### Task 4: Bind Codex handoff to the selected Base and final Blueprint revisions

**Files:**
- Modify: `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

**Interfaces:**
- Consumes: the three Base revision values and the final user-approved Blueprint revision.
- Produces: exact handoff metadata and boundary drift behavior for Godot implementation.

- [ ] **Step 1: Add revision metadata**

Add:

```yaml
base_observed_head_sha:
base_adopted_contract_sha:
base_execution_sha:
base_drift_classification:
blueprint_pass_1_revision:
blueprint_pass_2_final_revision:
user_final_approval_decision_id:
implementation_authority_revision:
```

- [ ] **Step 2: Add start and boundary rules**

Codex observes latest completed Base, preserves the adopted project contract, uses the selected execution SHA during bounded work, and rechecks at implementation handoff, pre-merge, post-merge, and closeout.

- [ ] **Step 3: Fail closed on relevant drift**

Relevant Base or project changes require classification, reconciliation, and affected-test reruns. Unrelated changes are recorded while the existing execution pin continues.

### Task 5: Update existing regressions and verify the exact branch HEAD

**Files:**
- Modify: `tests/test_project_master_gdd_two_artifact_contract.py`
- Test: `tests/test_base_fresh_read_two_pass_blueprint_contract.py`

**Interfaces:**
- Consumes: all changed contract files.
- Produces: exact-head static evidence and mutation resistance for the new lifecycle.

- [ ] **Step 1: Update the prior exact-order assertions**

Replace the old direct `PLAN → REQUIRED_IMAGE...` sequence with the pass-1 sequence while preserving existing approval and evidence-boundary assertions.

- [ ] **Step 2: Run focused tests**

Run:

```bash
python -m unittest \
  tests.test_base_fresh_read_two_pass_blueprint_contract \
  tests.test_project_master_gdd_two_artifact_contract -v
```

Expected: PASS.

- [ ] **Step 3: Run repository validation**

Run on the exact branch HEAD:

```bash
python tools/run_local_validation.py --trusted-history-commit <fresh-read-current-main-sha>
```

When a complete local checkout is unavailable, remote exact-head Actions and canonical `ci-gate` are required; the local gap remains explicit.

- [ ] **Step 4: Perform five full-scope adversarial passes**

Review authority/freshness, two-pass ordering, asset/VFX scope, Codex handoff, and claim/rollback boundaries. Correct every valid finding and rerun affected tests.

- [ ] **Step 5: Open and review the PR**

Confirm exact changed paths, same-goal PR overlap, ruleset, required checks, review threads, and current `main` freshness.

- [ ] **Step 6: Integrate normally**

Use expected-head squash merge only after all required checks pass and unresolved threads are zero. Fetch the new `main`, read back all owner tokens, and verify post-merge status without treating static contract success as Godot/runtime success.
