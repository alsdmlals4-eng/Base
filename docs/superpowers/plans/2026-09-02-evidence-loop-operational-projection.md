# Evidence-Based Work-Loop Operational Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing project work card expose the user-approved `READ → PICK → BUILD → CHECK → COMMIT` loop without creating a second canonical state system.

**Architecture:** `PROJECT_WORK_ITEM_CHECKLIST.md` remains the single reusable handoff and work-card owner. `GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` points to that owner rather than duplicating the loop. An existing contract test proves the lifecycle pointer and the card’s no-second-canon, evidence, human-gate, bounded-correction, and commit boundaries.

**Tech Stack:** Markdown policy/template contracts and Python `unittest`; no new package, runtime schema, service, workflow, or automation.

**Spec:** `docs/superpowers/specs/2026-09-02-evidence-loop-operational-projection-design.md`

**Direct approval and current locator:** The user directly approved promotion, absorption,
and protected merge in this chat on 2026-09-02. This plan and its paired design record
that bounded Base change until the normal protected PR is created. The closed Base Issue
`#825` is historical evidence for the prior PM execution-gate work only; it is not an
authority or active work record for this change or for a future project application.

## Global Constraints

- Reuse the existing Goal/Issue, `project_work_kanban`, Active Context, continuous-work queue, and evidence matrix; create no default `PROMPT.md`, `DESIGN.md`, `INBOX.md`, or `STATUS.md` files.
- Preserve progressive loading: registered design/guide owners are selected only when the current work requires them.
- Preserve one WIP item, normal protected PR merge, exact-head verification, merged-main readback, and no direct `main` push/force/bypass.
- Preserve the distinction between machine/runtime/visual evidence and user-declared `E6_HUMAN_PLAYTEST`.
- Keep all existing open PRs read-only; do not copy or modify their material.
- Base branch: `9a620220cae371a41af92adbc2cfa9935860c000`. Before publishing or
  merging, fresh-read `origin/main`; if it moved, rebase and rerun the exact-base
  checks with that new SHA rather than treating this recorded base as perpetual.

---

### Task 1: Add a failing shared-loop contract regression

**Files:**

- Modify: `tests/test_project_work_kanban_checklist_contract.py`

**Interfaces:**

- Consumes: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` and `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`.
- Produces: `ProjectWorkKanbanChecklistContractTests.test_evidence_loop_projection_reuses_existing_owners_and_gates`, discovered by `python -m unittest`.

- [x] **Step 1: Add the failing test method**

```python
    def test_evidence_loop_projection_reuses_existing_owners_and_gates(self) -> None:
        policy = self._read(POLICY)
        card = self._read(CARD)
        for token in (
            "EVIDENCE_WORK_LOOP_PROJECTION",
            "PROJECT_WORK_ITEM_CHECKLIST.md §11",
        ):
            self.assertIn(token, policy)
        for token in (
            "READ → PICK → BUILD → CHECK → COMMIT",
            "PROMPT / DESIGN / INBOX / STATUS",
            "INBOX_IS_NOT_EXECUTION_AUTHORITY",
            "GUIDES_PROGRESSIVELY_LOADED_BY_SELECTED_WORK",
            "CHECKPOINT_IS_NOT_COMPLETION",
            "HUMAN_PLAYTEST_EXPLICIT_USER_GATE",
            "QUALITY_NOT_ASSUMED_TO_INCREASE_PER_LOOP",
            "NO_UNBOUNDED_REPEAT_WITHOUT_NEW_EVIDENCE",
        ):
            self.assertIn(token, card)
```

- [x] **Step 2: Run the focused test and observe its expected failure**

Run: `python -m unittest tests.test_project_work_kanban_checklist_contract.ProjectWorkKanbanChecklistContractTests.test_evidence_loop_projection_reuses_existing_owners_and_gates -v`

Expected: FAIL because the baseline card and lifecycle policy do not yet contain the projection markers.

### Task 2: Implement the thin operational projection

**Files:**

- Modify: `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`
- Modify: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`

**Interfaces:**

- Consumes: existing section 11 fresh-session handoff, section 14 lifecycle/WIP model, evidence levels `E0`–`E6`, and protected PR completion gates.
- Produces: an explicit loop and reference-label mapping with no new canonical file, receipt field, renderer state, or PM product.

- [x] **Step 1: Extend the card’s section 11 with the role map and loop**

Add the exact marker block and prose that map the five reference labels to existing owners, require inbox triage before selected work, use `READ → PICK → BUILD → CHECK → COMMIT`, preserve staged evidence, and bound no-evidence repetitions to diagnose/correct/defer/decision.

- [x] **Step 2: Add the lifecycle-policy pointer**

In section 14, identify the card’s section 11 as the owner of `EVIDENCE_WORK_LOOP_PROJECTION`; point to it without reproducing the full procedure or adding a second status/document authority.

- [x] **Step 3: Run the focused regression and the existing PM integration checks**

Run:

```powershell
python -m unittest `
  tests.test_project_work_kanban_checklist_contract `
  tests.test_project_work_tracking_integration `
  tests.test_pm_review_regressions -v
```

Expected: PASS. The run proves the new shared contract text and existing receipt/renderer safety boundaries; it does not prove project runtime or Human review.

**Windows execution note:** on this host's default `cp949` console, eight existing
`test_pm_review_regressions` assertions fail because the existing receipt renderer
prints `—`, which `cp949` cannot encode. The identical `a5a1e7e` baseline fails the
same 8/33 tests; the changed branch passes all 34 focused tests under
`PYTHONUTF8=1`. The production Python/renderer source is outside this change and
was not modified. This keeps the pre-existing host encoding boundary separate from
the new card contract's result.

### Task 3: Verify complete Base integration and prepare the protected PR

**Files:**

- Verify: all changed files from Tasks 1–2 and their active consumers.

**Interfaces:**

- Consumes: the exact branch head, trusted base SHA, local validation runner, reference freshness checker, and normal GitHub PR checks.
- Produces: a reviewed, exact-head, protected-merge candidate.

- [x] **Step 1: Run complete local validation**

Run: `python tools/run_local_validation.py --trusted-history-commit 9a620220cae371a41af92adbc2cfa9935860c000`

Expected: exit `0`; inspect the reported test count and any skipped checks. A skipped platform/runtime job remains `NOT_RUN`, not PASS.

Result at `c93b5b8d7a3823056a94a8867b95d1db851fb54f`: exit `0`; 2,584 tests
passed and 59 platform-scoped tests were skipped. The local fallback gate, Base v9
integrity, generated-artifact check, skill-system coverage, and `git diff --check`
passed. This is Base contract evidence, not project runtime or Human review.

- [x] **Step 2: Run reference-freshness against the exact branch head**

Run: `python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base 9a620220cae371a41af92adbc2cfa9935860c000 --head HEAD`

Expected: exit `0`, with no active stale owner or consumer path.

Result at `c93b5b8d7a3823056a94a8867b95d1db851fb54f`: `PASS` with 1,417
scanned files, 11 legacy aliases, and 5 changed files.

- [x] **Step 3: Complete five full-scope adversarial loops**

For each loop, compare the spec, actual diff, active card/policy consumers, open PR boundaries, tests, evidence ceiling, protected merge path, and long-term duplication risk. Apply only a validated in-scope correction; rerun the affected tests after any correction. Record `NO_MATERIAL_FOLLOWUP` rather than inventing a change when no finding exists.

- [ ] **Step 4: Commit, publish, request independent review, and merge normally**

Create one focused commit, push the branch, create a PR against the then-current `main`, and wait for exact-head required checks, independent review, no unresolved threads, and ruleset eligibility. Re-read current `main` before merge; if it moved, reconcile and revalidate. Squash merge only through the normal protected route; no direct push, force push, or bypass. Read back the merged `main` and re-run the applicable post-merge review.

## Adversarial review record

Each loop re-read the user-approved scope, spec, active policy/card owners, actual
diff and test consumer, open-PR boundary, evidence ceiling, protected-merge path,
and long-term duplication/maintenance risk. `NO_MATERIAL_FOLLOWUP` means no new
in-scope defect was found; it does not claim runtime or Human validation.

1. **Loop 1 — second-canon attack:** The card mapped the four reference labels but
   the new regression did not yet assert the literal no-default-file marker. Added
   `PROMPT_DESIGN_INBOX_STATUS_ARE_ROLE_MAPS_NOT_DEFAULT_FILES` to the contract
   regression. No new file, schema, renderer, dashboard, or Skill was introduced.
2. **Loop 2 — false-completion attack:** Rechecked checkpoint, automatic test,
   runtime/capture, Human gate, PR and merged-main clauses against the existing
   E0–E6 and lifecycle boundaries. `NO_MATERIAL_FOLLOWUP`; the exact markers keep
   checkpoint and capture from becoming completion or Human approval.
3. **Loop 3 — scope/soft-coding attack:** Rechecked that the loop does not prescribe
   a fixed menu, button, genre, world, wireframe, benchmark conclusion, or project
   numeric value. `NO_MATERIAL_FOLLOWUP`; selected design/guide owners are
   progressive-load and project-local variables stay in their current owners.
4. **Loop 4 — concurrency/authority attack:** Rechecked the candidate paths against
   the current open PR snapshot and existing optional `DESIGN.md` support. This found
   a stale-current-context risk: section 11 called closed Base Issue `#825` the current
   application record. Corrected it to historical evidence only, required each current
   application to use a fresh Goal/Issue/card locator, and bound both meanings to the
   regression. The change neither consumes another PR nor turns an optional project
   design file into a Base-wide default.
5. **Loop 5 — operational-safety attack:** Rechecked fresh-read, inbox triage, WIP,
   blocking, no-evidence repetition, protected merge, exact-head and post-merge
   readback behavior. `NO_MATERIAL_FOLLOWUP`; the loop remains a small derived view,
   not an execution authority, quality guarantee, or unbounded autonomous loop.

**Independent-review correction — rebase-base freshness attack:** The independent
review found that the plan still supplied the pre-rebase `a5a1e7e` SHA to the global
base and exact-base validation commands. Updated all three execution boundaries to
the rebased `9a620220` base, made the reference-freshness head resolve from `HEAD`,
and added a regression that rejects the retired SHA in those executable positions.
