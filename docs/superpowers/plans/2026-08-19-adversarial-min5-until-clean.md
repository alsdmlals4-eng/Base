# Adversarial Minimum-Five Until-Clean Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require every L1+ full adversarial-review invocation to complete at least five full-scope improvement loops and, after the fifth, continue without a fixed maximum until the verified clean-exit condition is satisfied.

**Architecture:** Keep the existing `running-adversarial-review-and-refinement` Skill as the single owner. Add a minimum-loop floor to the existing clean-exit invariant rather than reviving the old fixed-five termination rule. Synchronize the global entrypoint, Long-Horizon policy, Skill, Learning Log, and existing focused regressions.

**Tech Stack:** Markdown governance contracts, Python `unittest`, GitHub Actions.

**Spec:** User-approved Base work contract in the current GPT conversation, 2026-08-19.

## Global Constraints

- `FULL_LOOP_COUNT_MINIMUM: 5`.
- `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`.
- A clean result before loop 5 cannot terminate the review.
- Loop 5 is not a maximum; any validated error/conflict/omission/blocker after loop 5 forces another complete loop.
- Do not manufacture findings or changes to fill the minimum; a fully executed clean loop may record zero findings and zero modifications.
- Existing `BETTER_ALTERNATIVE_SEARCH`, `LONG_TERM_PLAN_FIT_RECHECK`, evidence ceiling, and post-merge re-attack remain active.
- PR #530 and all other active workstreams remain read-only.

---

### Task 1: Lock the regression contract

**Files:**
- Modify: `tests/test_base_long_horizon_work_contract.py`

**Interfaces:**
- Consumes: current `ADVERSARIAL_REVIEW_UNTIL_CLEAN` contract.
- Produces: regression assertions for the minimum-five floor plus unbounded clean-exit continuation.

- [x] **Step 1: Write the failing test**

Require `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`, the minimum-five Korean rule, the post-five continuation rule, and `CLEAN_REVIEW_EXIT`.

- [x] **Step 2: Run test to verify it fails**

Observed in GitHub Actions run `32210386245`: expected RED. `test_adversarial_review_requires_minimum_five_then_until_clean` and the GPT-first companion contract failed because production did not yet contain `FULL_LOOP_COUNT_MINIMUM: 5`.

### Task 2: Update active policy owners

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`

**Interfaces:**
- Consumes: the RED regression from Task 1.
- Produces: one consistent active contract: five mandatory full loops, then continue until clean.

- [x] **Step 1: Add the minimum floor to `AGENTS.md`**

Kept `ADVERSARIAL_REVIEW_UNTIL_CLEAN`, added explicit minimum-five markers, blocked clean exit before loop 5, and required continuation after loop 5 while valid findings remain.

- [x] **Step 2: Update Long-Horizon machine and narrative contracts**

Added both minimum markers to the machine block and changed the lifecycle to `AT LEAST 5 FULL ADVERSARIAL LOOPS, THEN UNTIL CLEAN`.

- [x] **Step 3: Update the Skill owner**

Added the minimum markers, mandatory loop-1-through-5 rule, post-five continuation, and the rule that clean mandatory loops do not require manufactured findings or changes.

### Task 3: Synchronize historical learning and companion regression

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/LEARNING_LOG.md`
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`
- Modify: `docs/evidence/2026-08-19-gpt-first-clean-review-workflow.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: updated active Skill contract.
- Produces: historical explanation and consumer regressions that prevent either pure fixed-five termination or floorless clean exit from returning.

- [x] **Step 1: Add a new Learning Log entry**

Recorded that the earlier same-day floorless clean-exit decision is superseded by the later user decision: minimum five complete loops plus unbounded continuation to clean.

- [x] **Step 2: Update the neutral lifecycle regression**

The neutral lifecycle regression now asserts both minimum markers and clean exit while still rejecting the obsolete five-lens abstraction.

- [x] **Step 3: Mark the PR #531 evidence as historical for loop-floor semantics**

A full-scope adversarial pass found that the prior evidence file still described floorless clean exit without a supersession marker. It now preserves the historical evidence while directing readers to the later minimum-five-plus-until-clean active contract.

- [x] **Step 4: Synchronize the Documentation Map consumer**

A later full-scope pass found the Long-Horizon row could still read as fixed-five. It now says minimum five full improvements and additional full loops until valid error/conflict/omission/blocker reaches zero. The focused Long-Horizon regression asserts this consumer wording.

### Task 4: Verify, review, merge, and read back

**Files:**
- Verify all changed policy/test files.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: merged Base main with post-merge readback.

- [ ] **Step 1: Run focused tests**

Run the Long-Horizon and neutral adversarial lifecycle tests. Expected: PASS.

- [ ] **Step 2: Run required Base CI**

Expected: required contract/governance checks PASS; any intentionally unconfigured runtime check remains explicitly skipped, not PASS.

- [ ] **Step 3: Perform adversarial review under the new contract**

Review evidence so far:
1. Full-scope loop 1 — contract semantics, user intent, owner Skill, regression design: no fixed-five maximum; minimum-five floor present.
2. Full-scope loop 2 — history/evidence consumers: found stale floorless PR #531 evidence; fixed with explicit supersession.
3. Full-scope loop 3 — active documentation consumers: found `DOCUMENTATION_MAP.md` fixed-five ambiguity; fixed and regression-pinned.
4. Full-scope loop 4 — independent workstream collision: PR #530 overlaps several files but remains read-only; no modification/rebase/merge/absorption performed.
5. Full-scope loop 5 — pending exact-head CI, reference freshness, PR thread, full diff, cost/evidence ceiling, and Notion readback re-attack. If this or any later loop finds a valid blocker, continue with loop 6..N.

- [ ] **Step 4: Exact-head merge**

Merge only if required checks are green, unresolved review threads are zero, and the head SHA is unchanged.

- [ ] **Step 5: Post-merge readback**

Read new `main` versions of `AGENTS.md`, Long-Horizon policy, Skill owner, and Documentation Map; verify PR status and same-goal open PR isolation. Update the Notion `Base · 작업 시스템 & Skill 지도` only from the merged `main`, not from the pending branch.
