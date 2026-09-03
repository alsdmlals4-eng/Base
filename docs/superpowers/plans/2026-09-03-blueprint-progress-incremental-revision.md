# Blueprint Progress Projection and Incremental Revision Implementation Plan

> Issue: #846  
> Pull request: #847  
> Base revision: `850204b3e5de81a4045111b4a050c46c5a292b59`  
> Working branch: `work/846-blueprint-progress-incremental-revision`

## Goal

Extend the existing two-artifact Master GDD contract so the human Blueprint PDF shows project goals, system-planning checklists, case-level implementation and verification status, blockers, user decisions, and the next safe action. Preserve the repository and AI production specification as canon; the PDF remains a read-only derived view.

When a valid predecessor Blueprint exists, revise it incrementally instead of rebuilding from a blank document. Preserve stable IDs, approved decisions, explanatory content, diagrams, approved visuals, consumer references, and evidence unless an explicit semantic delta records the reason, replacement, and verification impact.

## Non-goals

- No separate PM PDF, HTML dashboard, third Blueprint artifact, or parallel status canon.
- No mass backfill of untouched projects or systems.
- No automatic demotion of existing implementation, runtime, UX, or approval evidence.
- No project runtime implementation in this Base change.

## Task 1 — Lock the regression contract

**Files**
- `tests/test_blueprint_progress_incremental_revision_contract.py`

**Steps**
1. Add focused assertions for goal/system/case progress views, evidence separation, PM-source routing, predecessor inventory, semantic delta, and loss-regression protection.
2. Run the repository test workflow and confirm the new tests fail before policy changes.
3. Preserve the failed run as RED evidence.

**Evidence**
- Initial head: `7dce2db87a3f54ca5bcd2a8543b7feee66fa8838`
- Workflow run: `33729770907`
- Expected failures: missing progress-projection tokens and missing V4 machine-contract fields.

## Task 2 — Extend the existing Master GDD owners additively

**Files**
- `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
- `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md`

**Steps**
1. Append a bounded progress-projection section without replacing existing Blueprint layers or publication gates.
2. Define the required human-PDF views:
   - project goal status summary;
   - goal-level checklist;
   - system-level checklist;
   - case-level status matrix;
   - blockers, decisions, and next safe action.
3. Separate `DOCUMENTED`, `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, and `USER_APPROVED`.
4. Require predecessor discovery, source inventory, stable-ID carry-forward, semantic-delta reporting, and predecessor/successor loss comparison.
5. Fail closed as `BLOCKED_UNVERIFIED` when the predecessor cannot be read reliably; never reconstruct missing facts from memory.

## Task 3 — Route PM data into the Blueprint without a new canon

**Files**
- `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`
- `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`

**Steps**
1. Define `project_work_kanban`, Goal/Issue records, Active Context, AI production specification, and repository evidence as the progress source.
2. Add optional `blueprint_refs` for goal, system, and case IDs.
3. Require Goal → System → Case → Work item → Evidence traceability.
4. Count completion only from evidence-backed PASS/DONE states; do not average unlike evidence layers into one opaque percentage.
5. Keep existing Markdown/Issue/receipt workflow intact and prohibit a parallel Blueprint status ledger.

## Task 4 — Add the machine-readable contract

**File**
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`

**Steps**
1. Add `blueprint_revision_contract` with incremental mode, forbidden blank rebuild, and required preservation receipts.
2. Add `human_blueprint_progress_projection` with canonical source, required views, and evidence dimensions.
3. Add predecessor and snapshot metadata to `human_pdf_required_metadata`.
4. Add invariants that preserve the two-artifact boundary and block unexplained loss or status demotion.

## Task 5 — Verify, review, and integrate

**Steps**
1. Run focused and full repository tests on the exact PR head.
2. Inspect the full PR diff and verify existing owner content was not silently deleted.
3. Check open review threads, required checks, mergeability, and current Base drift.
4. Mark the PR ready only after exact-head checks pass.
5. Squash merge under repository policy.
6. Fresh-read merged `main`, rerun/read back required checks, and confirm issue closure.

## Acceptance criteria

- Human Blueprint progress is derived from existing repository owners and evidence.
- Goal, system, and case status can be traced to work items and evidence.
- Evidence levels are not collapsed or overclaimed.
- A valid predecessor prevents blank rebuild.
- Existing IDs, content, diagrams, approved assets, consumers, and evidence are carried forward by default.
- Every removal, replacement, rename, or status downgrade has an explicit reason and impact record.
- Missing or unreadable predecessors fail closed instead of being recreated from recollection.
- Existing two-artifact, image, runtime-truth, and no-mass-backfill boundaries still pass regression tests.
- Exact-head CI and merged-main readback pass.