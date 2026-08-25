# Reuse-First Preflight Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make reuse/reference/benchmark lookup an enforced project-work entry gate and close the project-to-Base reuse learning loop.

**Architecture:** Reuse the existing `managing-project-intake-and-work-contract` as the universal router and `PROJECT_WORK_REUSE_HANDOFF.json` as the structured reuse owner. Add only root invariants, intake sequencing, structured handoff fields, visible START_HERE routing, focused regression tests, and minimal Notion human-view synchronization; do not create a new Skill or scan every project by default.

**Tech Stack:** Markdown contracts, JSON handoff contract, Python `unittest`, GitHub Actions, Notion human-facing pages.

**Spec:** `docs/superpowers/specs/2026-08-25-reuse-first-preflight-enforcement-design.md`

## Global Constraints

- Start from completed `main@0c5137d96b6a613687d9e8610ad4f26d4a38b75a`.
- Open/draft/ready PRs remain read-only; PR #660/#658/#650 are not modified or absorbed.
- No new Skill, paid dependency, runtime framework, or bulk cross-project scan.
- Project canon/identity overrides Base references; candidate discovery is not project adoption or runtime proof.
- Applicable `REUSE_FIRST_PREFLIGHT_REQUIRED=NOT_RUN` blocks new design/creation/`BUILD_NEW` readiness.
- Mechanical no-design changes may record reasoned `NOT_APPLICABLE`; unchanged approved continuation may use `REUSED_EVIDENCE`.
- Existing Base knowledge/case/reference is checked before fresh external research when it is relevant to the decision.
- Completion must evaluate the existing reuse handoff fields without manufacturing Base churn when no new reusable lesson exists.

---

### Task 1: Add a failing focused contract test

**Files:**
- Create: `tests/test_reuse_first_preflight_enforcement.py`
- Modify: `.github/workflows/validate-v47-workflow-alignment.yml`

**Interfaces:**
- Consumes: current `AGENTS.md`, intake Skill, `START_HERE.md`, `PROJECT_WORK_REUSE_HANDOFF.json`.
- Produces: explicit assertions for entry gate, source order, fail-closed behavior, accumulated Base knowledge, targeted cross-project boundary, and exit learning handoff.

- [ ] **Step 1: Create the focused test**

The test must assert that:

```python
self.assertIn("REUSE_FIRST_PREFLIGHT_REQUIRED", agents)
self.assertIn("REUSE_LEARNING_HANDOFF_REQUIRED", agents)
self.assertIn("PROJECT_WORK_REUSE_HANDOFF.json", intake)
self.assertIn("Asset/Reference/Benchmark", intake)
self.assertIn("Base accumulated knowledge/case/reference", intake)
self.assertIn("targeted", intake.lower())
self.assertIn("NOT_RUN", intake)
self.assertIn("REUSED_EVIDENCE", intake)
self.assertIn("NOT_APPLICABLE", intake)
self.assertIn("BASE_ACCUMULATED_KNOWLEDGE_CASE_REFERENCE", handoff["preflight_gate"]["required_source_order"])
self.assertIn("REUSE_FIRST_PREFLIGHT_REQUIRED", handoff["preflight_gate"]["id"])
self.assertTrue(handoff["preflight_gate"]["not_run_blocks_build_new"])
self.assertTrue(handoff["preflight_gate"]["targeted_cross_project_only"])
self.assertIn("REUSE_LEARNING_HANDOFF_REQUIRED", handoff["exit_learning_gate"]["id"])
self.assertIn("NO_NEW_REUSE_LEARNING", handoff["exit_learning_gate"]["no_change_result"])
```

- [ ] **Step 2: Wire the test into `validate-v47-workflow-alignment.yml`**

Add the new test path to `pull_request.paths` and `tests.test_reuse_first_preflight_enforcement` to the unittest command.

- [ ] **Step 3: Open a draft PR and verify RED**

Expected: the new focused test fails because current contracts do not yet contain the required markers/JSON objects.

---

### Task 2: Enforce the universal entry gate

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `START_HERE.md`

**Interfaces:**
- Consumes: existing current-state audit, Base reuse handoff/registry/profile, accumulated Base knowledge/case/reference, Notion workspace authority.
- Produces: universal fail-closed reuse-first routing without a new Skill.

- [ ] **Step 1: Add root invariants**

Add concise root rules for `REUSE_FIRST_PREFLIGHT_REQUIRED` and `REUSE_LEARNING_HANDOFF_REQUIRED`, referencing the intake/handoff owner rather than duplicating its detailed playbook.

- [ ] **Step 2: Insert reuse-first source order into intake current-state audit**

Required sequence:

```text
current project authority/implementation
→ approved Project Asset/Reference/Benchmark surfaces
→ Base PROJECT_WORK_REUSE_HANDOFF + adoption profile/matrix + REUSABLE_MODULE_REGISTRY
→ relevant Base accumulated knowledge/case/reference
→ targeted cross-project evidence only when directly relevant
→ decision-relevant external benchmark/professional practice/success-failure evidence
→ owner-specific reuse/adapt/reference/no-reuse disposition
→ alternatives + IRG
```

- [ ] **Step 3: Add applicability and fail-closed semantics**

Applicable new/revised system/UI/asset/tool/workflow/Skill/QA work must not proceed to new creation/`BUILD_NEW` with `NOT_RUN`. Allow reasoned `NOT_APPLICABLE` for mechanical work and `REUSED_EVIDENCE` for unchanged approved continuation.

- [ ] **Step 4: Add a short START_HERE entry note**

Expose the route but do not duplicate the detailed contract.

---

### Task 3: Strengthen the structured reuse handoff and exit loop

**Files:**
- Modify: `docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json`

**Interfaces:**
- Consumes: existing authority order, state sources, entry/exit fields, promotion rule.
- Produces: machine-readable entry preflight and exit-learning gates.

- [ ] **Step 1: Add `preflight_gate`**

Include `id`, applicability, `required_source_order`, `not_run_blocks_build_new=true`, `targeted_cross_project_only=true`, Base accumulated knowledge/case/reference before fresh external research, reuse evidence states (`REUSED_EVIDENCE`, `NOT_APPLICABLE`), and no-bulk-scan boundary.

- [ ] **Step 2: Add `exit_learning_gate`**

Include `id=REUSE_LEARNING_HANDOFF_REQUIRED`, the existing exit handoff fields, `no_change_result=NO_NEW_REUSE_LEARNING`, and `promotion_is_not_automatic=true`.

- [ ] **Step 3: Preserve existing project profiles and adoption states unchanged**

No project runtime/adoption decision changes in this task.

---

### Task 4: Verify GREEN and audit adjacent non-execution gaps

**Files:**
- Read/review: modified files, relevant reuse owners, active automations, open PR overlap.
- Modify only if a finding shares the same root cause and approved scope.

**Interfaces:**
- Consumes: exact PR head, current main, CI, automations state.
- Produces: evidence-backed list of fixed findings vs normal/deferred states.

- [ ] **Step 1: Confirm the focused test is GREEN in GitHub Actions**

Expected: `tests.test_reuse_first_preflight_enforcement` passes.

- [ ] **Step 2: Confirm existing v4.7 alignment regression remains GREEN**

Expected: `tests.test_v47_workflow_alignment` and `tests.test_v47_superseded_pr_closure` pass.

- [ ] **Step 3: Recheck adjacent workflows**

Verify scheduled Source/reuse benchmarking tasks are enabled and inspect last-run evidence. Do not change a task merely because its first scheduled run is legitimately in the future.

- [ ] **Step 4: Classify additional findings**

At minimum distinguish `FIXED_IN_SCOPE`, `ALREADY_ENFORCED`, `NORMAL_DEFERRED`, `USER_DECISION_REQUIRED`, `OUT_OF_SCOPE`.

---

### Task 5: Sync human-facing Notion documentation

**Files:**
- Update: `Base · 작업 시스템 & Skill 지도`
- Update: `Base · 재사용 모듈 라이브러리`

**Interfaces:**
- Consumes: approved gate semantics after repository implementation.
- Produces: concise human explanation without internal receipt duplication.

- [ ] **Step 1: Update the work-system page**

Add the visible workflow concept: reuse-first lookup happens before new design/creation, and an applicable NOT_RUN blocks new creation.

- [ ] **Step 2: Update the reuse-library page**

Add the ordered lookup sources including accumulated Base knowledge/case/reference and the targeted cross-project rule; state that no new reusable lesson means no forced registry churn.

- [ ] **Step 3: Fetch both pages and verify readback**

Expected: the new rules are present exactly once and AI-only receipt metadata remains out of the human-facing summary.

---

### Task 6: PR review, merge, and post-merge readback

**Files:**
- No new scope.

**Interfaces:**
- Consumes: exact reviewed PR head and current main.
- Produces: merged main evidence and post-merge GitHub/Notion readback.

- [ ] **Step 1: Compare PR to approved scope and open PR #660 paths**

Expected: no mutation/absorption of #660 and no unrelated refactor.

- [ ] **Step 2: Run adversarial review against the complete diff**

Check bypass paths, over-scanning, duplicated authority, project identity flattening, unnecessary external research, stale evidence reuse, and missing exit feedback.

- [ ] **Step 3: Verify exact-head checks and review state**

Required checks applicable to the PR must be successful, unresolved threads 0, current main freshness confirmed.

- [ ] **Step 4: Squash merge using expected head protection**

Do not bypass ruleset/checks and do not force push/direct-push main.

- [ ] **Step 5: Post-merge readback**

Re-read main contracts and both Notion pages; recalculate remaining work. Completion requires `REQUIRED_WORK_REMAINING=0` for this approved scope or an explicit truthful blocker.
