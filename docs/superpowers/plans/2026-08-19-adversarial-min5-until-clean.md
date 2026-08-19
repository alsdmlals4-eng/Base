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

Run: `python -m unittest tests.test_base_long_horizon_work_contract -v`

Expected: FAIL because current production Skill has clean-exit semantics but no minimum-five markers.

### Task 2: Update active policy owners

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`

**Interfaces:**
- Consumes: the RED regression from Task 1.
- Produces: one consistent active contract: five mandatory full loops, then continue until clean.

- [ ] **Step 1: Add the minimum floor to `AGENTS.md`**

Keep `ADVERSARIAL_REVIEW_UNTIL_CLEAN`, add explicit minimum-five markers, forbid clean exit before loop 5, and require continuation after loop 5 while valid findings remain.

- [ ] **Step 2: Update Long-Horizon machine and narrative contracts**

Add both minimum markers to the machine block and make the lifecycle say `AT LEAST 5 FULL ADVERSARIAL LOOPS, THEN UNTIL CLEAN`.

- [ ] **Step 3: Update the Skill owner**

Add the minimum markers, mandatory loop-1-through-5 rule, post-five continuation, and the rule that clean mandatory loops do not require manufactured findings or changes.

### Task 3: Synchronize historical learning and companion regression

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/LEARNING_LOG.md`
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: updated active Skill contract.
- Produces: historical explanation and a second regression that prevents either pure fixed-five termination or floorless clean exit from returning.

- [ ] **Step 1: Add a new Learning Log entry**

Record that the 2026-08-19 floorless clean-exit decision is superseded by the later user decision: minimum five complete loops plus unbounded continuation to clean.

- [ ] **Step 2: Update the neutral lifecycle regression**

Assert both minimum markers and clean exit; keep assertions rejecting the obsolete five-lens abstraction.

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

Execute at least five full-scope review cycles over the approved change. If cycle 5 or later finds any valid blocker, fix, verify, and continue full cycles until a post-minimum cycle is clean.

- [ ] **Step 4: Exact-head merge**

Merge only if required checks are green, unresolved review threads are zero, and the head SHA is unchanged.

- [ ] **Step 5: Post-merge readback**

Read new `main` versions of `AGENTS.md`, Long-Horizon policy, and Skill owner and verify PR status and same-goal open PR isolation.
