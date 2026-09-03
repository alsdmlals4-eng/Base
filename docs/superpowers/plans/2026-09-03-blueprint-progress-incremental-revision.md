# Federated GitHub + Approved PDF Dual Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct Base so repository execution/data and a user-approved, manifest-registered human Blueprint PDF are both canonical in separate domains, with one editable owner per atomic fact and fail-closed drift handling.

**Architecture:** Extend the existing V4 repository-first workspace into a federated dual-canon model. Repository owners remain authoritative for editable structured and runtime facts; the immutable approved PDF is authoritative for the human visual/review baseline. Shared IDs, exact SHA/hash metadata, a registration manifest contract, status-specific projection rules, predecessor comparison, and conflict states connect the two without duplicate editing.

**Tech Stack:** Markdown policy and templates, JSON machine contract, Python `unittest`, GitHub Actions/Base CI.

**Spec:** `docs/superpowers/specs/2026-09-04-federated-github-pdf-dual-canon-design.md`

## Global Constraints

- Continue Issue #846 / PR #847; do not create a third same-goal PR.
- Preserve PR #845 read-only and block its merge until it is reconciled with this authority model.
- No direct `main` push, force push, ruleset bypass, project-fleet rollout, paid dependency, or runtime mutation.
- Preserve exactly two user-facing planning deliverables: human PDF and repository AI Markdown.
- Preserve `PROJECT_WORK_KANBAN_IS_PROGRESS_SOURCE`; do not create a second editable status ledger.
- Preserve historical BCPs, old plans, review evidence, and V3 compatibility records.
- Candidate PDF is not canon; only user-approved and manifest-registered PDF is human visual canon.
- One atomic fact has one editable owner.
- `CANON_CONFLICT` blocks completion and release.
- Document/static/test/runtime/UX/user approval/release evidence remain distinct.

---

### Task 1: Lock the dual-canon regression contract

**Files:**
- Create: `tests/test_federated_dual_canon_contract.py`
- Modify later during GREEN: `tests/test_repository_first_workspace_contract.py`
- Modify later during GREEN: `tests/test_notion_project_workspace_contract.py`
- Modify later during GREEN: `tests/test_blueprint_progress_incremental_revision_contract.py`

**Interfaces:**
- Consumes: current V4 contract and active routing files.
- Produces: executable expectations for authority fields, active-surface propagation, PDF activation, ownership, conflict, immutable supersession, and repository-owned PM projection.

- [ ] **Step 1: Add a failing contract test**

```python
def test_machine_contract_declares_federated_dual_canon(self):
    contract = json.loads(V4.read_text(encoding="utf-8"))
    self.assertEqual(
        "FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER",
        contract["authority_model"],
    )
    self.assertEqual(
        "REPOSITORY_EXECUTION_DATA_CANON",
        contract["repository_canon"],
    )
    self.assertEqual(
        "APPROVED_HUMAN_BLUEPRINT_PDF_CANON",
        contract["human_pdf_canon"],
    )
```

- [ ] **Step 2: Run the focused test and preserve RED**

Run:

```bash
python -m unittest tests.test_federated_dual_canon_contract -v
```

Expected: FAIL because current V4 still declares `REPOSITORY_PRIMARY_CANON_WITH_DERIVED_HUMAN_PDF` and lacks the PDF canon registration object.

- [ ] **Step 3: Commit only the approved design, plan, and failing test**

```bash
git add docs/superpowers/specs/2026-09-04-federated-github-pdf-dual-canon-design.md \
  docs/superpowers/plans/2026-09-03-blueprint-progress-incremental-revision.md \
  tests/test_federated_dual_canon_contract.py
git commit -m "test: define GitHub and approved PDF dual canon"
```

### Task 2: Correct the core workspace authority

**Files:**
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`
- Modify: `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`
- Modify: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`

**Interfaces:**
- Consumes: approved design tokens and existing Blueprint incremental revision fields.
- Produces: `human_pdf_canon_contract`, required registration metadata, alignment states, conflict gate, and immutable supersession policy.

- [ ] **Step 1: Update V4 fields**

Set:

```json
{
  "authority_model": "FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER",
  "repository_canon": "REPOSITORY_EXECUTION_DATA_CANON",
  "human_pdf_canon": "APPROVED_HUMAN_BLUEPRINT_PDF_CANON",
  "single_fact_owner": "ONE_EDITABLE_OWNER_PER_ATOMIC_FACT",
  "pdf_policy": "APPROVED_PDF_IS_HUMAN_VISUAL_CANON",
  "candidate_pdf_policy": "CANDIDATE_PDF_NOT_CANON"
}
```

Add `human_pdf_canon_contract` with activation, owned domains, repository projection, annotation, required registration fields, alignment states, conflict gate, and supersession policy exactly as defined by the spec.

- [ ] **Step 2: Correct policy prose without weakening repository truth**

Replace blanket “PDF is not canon” statements with:

```text
Repository owners are editable canon for structured/executable facts.
A user-approved and manifest-registered PDF is immutable human visual/review canon.
Structured values and work status displayed in the PDF remain repository projections.
```

- [ ] **Step 3: Preserve the status-specific projection boundary**

Use:

```text
PROJECT_WORK_KANBAN_IS_PROGRESS_SOURCE
PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION
NO_PARALLEL_BLUEPRINT_STATUS_CANON
```

Do not use a blanket token that says the entire approved PDF is non-canonical.

- [ ] **Step 4: Run focused tests**

```bash
python -m unittest \
  tests.test_federated_dual_canon_contract \
  tests.test_blueprint_progress_incremental_revision_contract -v
```

Expected: PASS for core fields and Blueprint status ownership.

### Task 3: Propagate the active routing vocabulary

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Modify: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`
- Modify: `skills/managing-design-documents/SKILL.md`
- Modify: `templates/AGENTS.project.md`
- Modify: `templates/copilot-instructions.md`
- Modify: `templates/custom-instructions.codex.md`
- Modify: `templates/custom-instructions.gpt.md`
- Modify: `templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `templates/project-operations/README.md`
- Modify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`
- Modify: `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md`

**Interfaces:**
- Consumes: V4 authority tokens.
- Produces: consistent cold-start and handoff routing with no active blanket “PDF is non-canon” instruction.

- [ ] **Step 1: Replace active retired vocabulary**

Replace only active-route occurrences:

```text
REPOSITORY_PRIMARY_CANON_WITH_DERIVED_HUMAN_PDF
→ FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER

HUMAN_GDD_PDF_DERIVED_VIEW
→ APPROVED_HUMAN_BLUEPRINT_PDF_CANON

PDF_IS_DERIVED_SNAPSHOT_NOT_CANON
→ APPROVED_PDF_IS_HUMAN_VISUAL_CANON
```

Do not rewrite historical BCPs, old plans, reviews, or V3 compatibility records.

- [ ] **Step 2: Add the single-owner and candidate boundary where a route could otherwise imply equal editability**

```text
ONE_EDITABLE_OWNER_PER_ATOMIC_FACT
CANDIDATE_PDF_NOT_CANON
PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION
```

- [ ] **Step 3: Update compatibility tests before production verification**

Change active V4 assertions in the three existing test modules to the new authority tokens. Keep V3/Notion history assertions unchanged.

- [ ] **Step 4: Run routing and workspace tests**

```bash
python -m unittest \
  tests.test_federated_dual_canon_contract \
  tests.test_repository_first_workspace_contract \
  tests.test_notion_project_workspace_contract \
  tests.test_blueprint_progress_incremental_revision_contract -v
```

Expected: PASS.

### Task 4: Reconcile same-goal PR boundaries

**Files:**
- Modify: PR #847 body.
- Comment only: PR #845.

**Interfaces:**
- Consumes: exact #847 head and #845’s current contract.
- Produces: one current implementation owner and an explicit non-merge condition for the stale complementary draft.

- [ ] **Step 1: Update PR #847 scope and approval**

Record:

```text
approval_ref: current-user-message:2026-09-04:앞으로-둘-다-정본
selected_model: FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER
```

Remove “PDF 자체를 canon으로 승격” from non-scope.

- [ ] **Step 2: Place a blocking reconciliation comment on PR #845**

The comment must state that #845 remains read-only and must not merge until its blanket non-canon wording, V4 fields, tests, and renderer inputs are reconciled with #847 or #847’s merged successor.

- [ ] **Step 3: Do not close or absorb #845 automatically**

Preserve its implementation and test history for later reconciliation.

### Task 5: Verify and integrate

**Files:**
- Create or update: `docs/reviews/2026-09-04-federated-dual-canon-adversarial-review.yml`
- Modify: `docs/superpowers/plans/2026-09-03-blueprint-progress-incremental-revision.md` only for exact evidence readback.

**Interfaces:**
- Consumes: final PR diff, exact-head CI, review threads, current `main`, and active ruleset.
- Produces: five-loop review evidence, exact-head verification, and merge/readback decision.

- [ ] **Step 1: Run five full-scope adversarial loops**

Cover:

1. authority ambiguity and double-entry;
2. candidate/approval/hash/supersession lifecycle;
3. structured-data and visual-baseline conflict resolution;
4. active-route propagation, legacy/history preservation, and PR concurrency;
5. evidence ceilings, rollback, and project-adoption limits.

- [ ] **Step 2: Run focused and full CI**

Focused:

```bash
python -m unittest \
  tests.test_federated_dual_canon_contract \
  tests.test_repository_first_workspace_contract \
  tests.test_notion_project_workspace_contract \
  tests.test_blueprint_progress_incremental_revision_contract -v
```

Then run the repository-required workflows on the exact PR head.

- [ ] **Step 3: Inspect exact diff and references**

Confirm:

- no historical BCP/old plan/V3 rewrite;
- no blanket non-canon token remains in active routes;
- no duplicate editable PM status;
- #845 remains unmodified except for a reconciliation comment;
- no project/runtime/asset binary changed.

- [ ] **Step 4: Check merge gates**

Read back:

- latest `main`;
- exact PR head;
- required checks;
- unresolved review threads;
- mergeability;
- active ruleset;
- independent review state.

- [ ] **Step 5: Integrate only when all required gates pass**

Use expected-head squash merge. Then fresh-read merged `main`, V4 contract, policy, tests, PR state, and post-merge workflow results.

## Acceptance Criteria

- Both repository and approved PDF are explicitly canonical in their assigned domains.
- Every atomic fact has one editable owner.
- Candidate PDFs and PDF annotations cannot silently mutate canon.
- Approved PDF identity is exact-SHA, SHA-256, approval-ref, timestamp, status, manifest, and supersession traceable.
- Work status remains repository-owned even when displayed in the canonical PDF.
- Structured mismatches and approved visual-baseline mismatches have deterministic resolution rules.
- `CANON_CONFLICT` blocks completion/release.
- Active Base cold-start and handoff surfaces use the new model.
- Historical evidence and V3 compatibility remain unchanged.
- #845 cannot merge with stale blanket non-canon semantics.
- Focused tests, required exact-head CI, review gates, and merged-main readback distinguish what actually passed.
