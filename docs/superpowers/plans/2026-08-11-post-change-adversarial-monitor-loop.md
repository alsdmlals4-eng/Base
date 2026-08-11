# Post-Change Adversarial Monitor Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make adversarial review, PR rechecks, omission/conflict/complement-gap detection, and post-merge readback an explicit completion invariant for retained changes.

**Architecture:** Extend the existing adversarial-review owner and operating lifecycle rather than introducing a new Skill. Add one focused regression to lock the loop, update the central learning log because an ACTIVE Skill body changes, and use existing CI/PR gates for verification.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions repository contracts.

## Global Constraints

- No new ACTIVE Skill, agent, workflow permission, Ruleset, or Required Check topology.
- Existing Solution First remains authoritative.
- `NO_MATERIAL_FOLLOWUP` is a valid terminal state; do not force churn.
- Unrun verification remains `NOT_RUN` / `BLOCKED_UNVERIFIED`.
- Protected policy/security/product-direction changes continue to use existing user/BCP gates.

---

### Task 1: Lock the post-change monitoring contract with RED

**Files:**
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: existing adversarial Skill and operating model text contracts.
- Produces: a focused test requiring the named post-change monitor loop and its mandatory checks.

- [ ] **Step 1: Write the failing test**

Add `test_post_change_monitor_loop_rechecks_prs_omissions_conflicts_and_complements` and require both the Skill and operating model to contain `POST_CHANGE_MONITOR_LOOP`, same-goal open/recent PR recheck, `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, `DUPLICATE_WORK`, `NO_MATERIAL_FOLLOWUP`, untouched-consumer recheck, exact-head validation, and post-merge main readback.

- [ ] **Step 2: Run test to verify it fails**

Run the focused test through the repository CI path. Expected: FAIL because the named invariant and classification vocabulary are not yet present.

- [ ] **Step 3: Commit**

Commit only the failing regression before production contract edits.

---

### Task 2: Absorb the loop into the existing owner

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: existing `attack`, `validate-critique`, `regression-recheck`, `post-merge-review`, repository-wide audit, exact-head validation, and PR gates.
- Produces: one explicit completion invariant named `POST_CHANGE_MONITOR_LOOP`.

- [ ] **Step 1: Implement the minimal Skill contract**

Add the loop after the existing general and post-merge routes. State that every retained repository/project change must recheck same-goal open/recent PRs, untouched consumers/derivatives, and classify material findings as `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, or `DUPLICATE_WORK`, with `NO_MATERIAL_FOLLOWUP` allowed when no durable follow-up exists.

- [ ] **Step 2: Connect it to the operating lifecycle**

Extend the lifecycle so completion occurs only after the post-change monitor loop, exact-head validation, and—when merged—new-main readback plus PR/canon recheck.

- [ ] **Step 3: Record the learning**

Add a central learning-log entry explaining why post-change monitoring is a completion invariant, its no-churn boundary, and revisit triggers.

- [ ] **Step 4: Run the focused test**

Expected: PASS.

- [ ] **Step 5: Commit**

Commit the owner, lifecycle, and learning-log changes together.

---

### Task 3: Adversarial PR audit and exact-head validation

**Files:**
- Review all PR-changed files; no additional file is mandatory.

**Interfaces:**
- Consumes: PR diff, same-goal open/recent PR search, review threads, workflow checks, latest `main`.
- Produces: merge/no-merge decision with explicit omissions/conflicts/complement gaps.

- [ ] **Step 1: Run repository-wide adversarial checks**

Attack for duplicate policy ownership, untouched consumers, accidental Registry/permission changes, forced churn, and background-execution overclaim.

- [ ] **Step 2: Validate critiques**

Keep only `MUST_FIX` / in-scope `SHOULD_FIX`; reject duplicate or preference-only critiques.

- [ ] **Step 3: Verify exact head**

Require focused tests, Base v9 contracts, Game Project Operating System including final `ci-gate`, zero unresolved review threads, latest-main compatibility, and same-goal PR recheck.

- [ ] **Step 4: Merge only if the current head is unchanged and all gates pass**

Use repository-approved squash merge with expected-head SHA.

- [ ] **Step 5: Post-merge readback**

Read the new `main` Skill and operating lifecycle, recheck recent/open PRs, and report any remaining `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, or `DUPLICATE_WORK`. If none exist, report `NO_MATERIAL_FOLLOWUP`.