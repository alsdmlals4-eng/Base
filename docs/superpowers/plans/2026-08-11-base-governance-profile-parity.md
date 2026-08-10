# Base Governance Profile Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Base's mutable GitHub governance profile record the governance surfaces already required by the project template and verified by current GitHub repository/ruleset evidence, with a regression that prevents silent schema drift.

**Architecture:** Keep `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md` as the reusable project template and `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md` as Base's mutable instance. Extend the existing repository-governance regression to require the Base instance to cover the template's major governance surfaces without making CI depend on live GitHub API availability.

**Tech Stack:** Markdown/YAML-like profile blocks, Python `unittest`, GitHub Actions `ci-gate`.

## Global Constraints

- Base baseline: `main@ba4ad067684952d987790f0ebda1a96d9554bc09`.
- Work only on an isolated branch; never write directly to `main`.
- Do not modify frozen `base*.lock.json` release evidence.
- Do not create a new Skill or duplicate the governance owner.
- Static CI must not require a live GitHub API call.
- Live evidence may populate the mutable Base profile only when it was directly observed in this work.
- Preserve unverified fields as `unverified` / `UNVERIFIED_REPOSITORY_SETTING`; do not infer them.
- Keep Patch A limited to profile parity and its regression. Repository merge-method setting changes and stale Dependabot PR disposition are separate patches.

---

### Task 1: Add a failing Base-profile parity regression

**Files:**
- Modify: `tests/test_repository_governance_baseline.py`
- Test: `tests/test_repository_governance_baseline.py`

**Interfaces:**
- Consumes: existing `read()` helper and Base/profile template Markdown files.
- Produces: `test_base_profile_records_current_repository_governance_surfaces`, which fails whenever the mutable Base profile omits required governance surfaces or verified current values.

- [ ] **Step 1: Write the failing test**

Add this test to `RepositoryGovernanceBaselineTests`:

```python
def test_base_profile_records_current_repository_governance_surfaces(self) -> None:
    profile = read("docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md")
    template = read("templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md")

    for heading in (
        "## Pull Request Policy",
        "## Required Checks",
        "## Ruleset",
        "## Auto-merge Gate",
        "## Actions Budget",
        "## Rollback",
        "## Evidence",
    ):
        with self.subTest(heading=heading):
            self.assertIn(heading, template)
            self.assertIn(heading, profile)

    for token in (
        "auto_merge: enabled",
        "primary: ci-gate",
        "strict_up_to_date: true",
        "name: solo-main-safety",
        "enforcement: active",
        "behavior_verified: true",
        "default_branch_targeted: true",
        "pull_request_required: true",
        "linear_history: true",
        "force_push_blocked: true",
        "deletion_blocked: true",
        "required_check_context: ci-gate",
        "Repository settings snapshot:",
        "Ruleset URL or ID:",
        "Required Check run:",
        "Remaining unverified settings:",
    ):
        with self.subTest(token=token):
            self.assertIn(token, profile)
```

- [ ] **Step 2: Run the exact test on the test-only branch state and verify RED**

Run through the repository PR CI after pushing only the test change. Expected: `tests/test_repository_governance_baseline.py` fails because the current Base profile lacks the required sections/tokens.

- [ ] **Step 3: Confirm the failure is about profile drift**

Expected failure must mention one of the absent headings/tokens above, not syntax/import/test-discovery errors. If it fails for another reason, repair only the test and repeat RED.

---

### Task 2: Bring the mutable Base profile to template parity

**Files:**
- Modify: `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`
- Test: `tests/test_repository_governance_baseline.py`

**Interfaces:**
- Consumes: current repository metadata, current `solo-main-safety` Ruleset response, exact-head `ci-gate` evidence from PR #274, and the reusable profile template.
- Produces: a Base profile with Repository, Pull Request Policy, Required Checks, Ruleset, Auto-merge Gate, Actions Budget, Rollback, and Evidence sections.

- [ ] **Step 1: Update only directly verified current values**

Record:

```yaml
pull_requests:
  required: true
  allowed_merge_methods:
    - squash
  auto_merge: enabled
  merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS
  agent_merge_execution: required
  required_approving_review_count: 0
  required_review_thread_resolution: true
  require_code_owner_review: false
  require_last_push_approval: false

required_checks:
  primary: ci-gate
  additional: []
  strict_up_to_date: true
  last_observed_success_sha: d5527fa4b4be390a1d7aae6caf1792c3587e6e04
  status: verified

ruleset:
  name: solo-main-safety
  source_template: templates/project-operations/github/rulesets/solo-main-safety.json
  enforcement: active
  behavior_verified: true
  default_branch_targeted: true
  pull_request_required: true
  linear_history: true
  force_push_blocked: true
  deletion_blocked: true
  required_check_context: ci-gate
```

Keep account-plan, private vulnerability reporting, code-owner review execution, billing/budget values, and any unobserved per-PR auto-merge gate fields explicitly unverified/not-run.

- [ ] **Step 2: Preserve the distinction between repository settings and Ruleset policy**

Do not claim that repository-level merge/rebase methods are disabled in Patch A. Note that live repository metadata currently allows squash/merge/rebase while the active Ruleset permits squash for the protected default branch; leave setting alignment to Patch B.

- [ ] **Step 3: Record evidence references and update timestamp**

Set `last_verified_at: 2026-08-11` and list the repository metadata observation, Ruleset ID `19688076`, and PR #274 exact-head required-check evidence. Do not rewrite historical release locks.

- [ ] **Step 4: Run the focused regression and verify GREEN**

Expected: `tests/test_repository_governance_baseline.py` passes on the updated exact head.

---

### Task 3: Review, full validation, and merge gate

**Files:**
- Review: the two Patch A files plus this plan.

**Interfaces:**
- Consumes: exact branch diff and GitHub Actions results.
- Produces: evidence-backed PR disposition for squash merge.

- [ ] **Step 1: Run adversarial review on the exact diff**

Attack for accidental live-API dependency, false verified claims, duplicate authority, frozen release mutation, or Patch B/C scope leakage.

- [ ] **Step 2: Run repository-required CI on the exact PR head**

Require the canonical `Validate Game Project Operating System` workflow and final `ci-gate` to succeed. Treat skipped applicable jobs or missing required evidence as blocking.

- [ ] **Step 3: Re-read unresolved review threads and exact head SHA**

Require zero unresolved review threads and no head movement after review.

- [ ] **Step 4: Squash merge only after exact-head evidence passes**

Use the repository-required squash method. After merge, re-read `main`, the mutable profile, and Ruleset state; report any residual drift as Patch B/C follow-up rather than silently expanding this patch.
