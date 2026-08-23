# Base GitHub Repository Governance Profile

This is the mutable current-state identity and platform-evidence record for the Base repository. Released `base*.lock.json` files remain frozen historical identities and must not be used as the authority for current repository ownership after a rename or transfer.

## Repository

```yaml
repository:
  name: alsdmlals4-eng/Base
  owner: alsdmlals4-eng
  visibility: public
  account_plan: unverified
  primary_branch: main
  rollout_stage: BASE
  last_verified_at: 2026-08-23
  verified_by: "GitHub repository metadata + authenticated GitHub CLI Ruleset API + PR #614 exact-head CI"
```

## Pull Request Policy

```yaml
pull_requests:
  required: true
  allowed_merge_methods:
    - squash
  repository_allow_squash_merge: true
  repository_allow_merge_commit: false
  repository_allow_rebase_merge: false
  repository_merge_methods_status: VERIFIED_SQUASH_ONLY
  repository_merge_methods_verified_at: 2026-08-23
  auto_merge: enabled
  merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS
  agent_merge_execution: required
  required_approving_review_count: 0
  required_review_thread_resolution: true
  require_code_owner_review: false
  require_last_push_approval: false
```

The repository-level merge-method settings and the protected default-branch Ruleset are now aligned: squash is enabled and merge commits/rebase merges are disabled at repository level, while `solo-main-safety` also allows only squash on the protected default branch. This closes the previous defense-in-depth drift without changing the Ruleset, Required Check, or auto-merge policy.

## Required Checks

```yaml
required_checks:
  primary: ci-gate
  additional: []
  strict_up_to_date: true
  last_observed_success_sha: debe2aa247a8d631267a8309a70a7e44d3c2ffaf
  status: verified
```

`last_observed_success_sha` is PR #614's exact reviewed head. The `Validate Game Project Operating System` run `32576426840` completed its final `ci-gate` successfully before squash merge to `main` as `8dd79816aa39704a8ede8acc965ea452bb5cebc6`.

## Ruleset

```yaml
ruleset:
  id: 19688076
  name: solo-main-safety
  source_template: templates/project-operations/github/rulesets/solo-main-safety.json
  enforcement: active
  behavior_verified: true
  default_branch_targeted: true
  pull_request_required: true
  allowed_merge_methods:
    - squash
  linear_history: true
  force_push_blocked: true
  deletion_blocked: true
  required_check_context: ci-gate
```

Ruleset ID `19688076` was re-read through authenticated GitHub CLI on 2026-08-23 after the repository merge-method change. It remained `active`, requires pull requests, review-thread resolution, linear history, strict `ci-gate`, and squash as the only allowed protected-branch merge method, and blocks deletion and non-fast-forward updates.

## Auto-merge Gate

```yaml
auto_merge_gate:
  package_status:
  reviewed_head_sha:
  current_head_sha:
  required_checks_passed:
  unresolved_review_threads:
  user_review_required:
  change_proposal:
  repository_setting_verified: true
  result:
```

This mutable repository profile verifies that the repository setting `allow_auto_merge` is enabled. It is **not** a live evaluation of a particular pull request, so the per-PR gate fields and `result` remain blank rather than inventing `AUTO_MERGE_ELIGIBLE`, `AUTO_MERGE_ENABLED`, or `AUTO_MERGE_BLOCKED` evidence.

## Actions Budget

```yaml
actions:
  public_repository_standard_minutes: free
  private_repository_included_minutes: not_applicable
  monthly_soft_limit: unverified
  stop_usage_at_budget_limit: unverified
  artifact_retention_days: unverified
  high_cost_jobs: unverified
```

Base is currently public and uses standard GitHub-hosted runners as the normal `REMOTE_CI` path. Repository-specific budget and retention settings remain unverified until directly observed; public-repository status does not prove those settings.

## Rollback

```yaml
rollback:
  disable_ruleset: set solo-main-safety enforcement to disabled
  disable_auto_merge: disable Allow auto-merge in repository settings
  convert_pr_to_draft: convert the affected pull request to Draft
  restore_required_check: restore ci-gate as the strict required status check
  restore_merge_methods: change repository-level merge methods only after a verified policy decision requires it
  recovery_owner: alsdmlals4-eng
  resume_condition: repository settings and exact-head required-check evidence are reverified
```

Rollback changes repository enforcement only when the relevant failure is verified. Do not bypass a broken Ruleset by pushing directly to `main`, and do not rewrite frozen release locks to represent a mutable setting rollback.

## Current platform evidence

```yaml
platform_status:
  required_check: ci-gate
  required_check_status: VERIFIED_PR_614_HEAD_debe2aa247a8d631267a8309a70a7e44d3c2ffaf
  ruleset: VERIFIED_ACTIVE_ID_19688076
  repository_merge_methods: VERIFIED_SQUASH_ONLY
  codeowners_owner: "@alsdmlals4-eng"
  codeowners_review_request: NOT_RUN
  private_vulnerability_reporting: UNVERIFIED_REPOSITORY_SETTING
  dependabot_configuration: PRESENT
  dependabot_pnpm_11: DEFERRED_UNTIL_OFFICIAL_SUPPORT
```

`required_check_status` proves an exact-head `ci-gate` success for PR #614; it does not prove every future PR or repository setting. The merge-method and Ruleset states above are direct live evidence from the 2026-08-23 verification. Remaining states stay unverified or not run until direct evidence exists.

## Evidence

- Repository settings snapshot: 2026-08-23 GitHub repository metadata — public, default branch `main`, `allow_auto_merge=true`, `allow_squash_merge=true`, `allow_merge_commit=false`, `allow_rebase_merge=false`.
- Repository merge-method change: authenticated GitHub CLI/API run on 2026-08-23 changed only merge-method settings from `true/true/true` to `true/false/false` for squash/merge/rebase.
- Ruleset URL or ID: `solo-main-safety`, ID `19688076`, enforcement `active`; authenticated GitHub CLI readback on 2026-08-23 showed `allowed_merge_methods=[squash]` and required status check `ci-gate`.
- Required Check run: PR #614 head `debe2aa247a8d631267a8309a70a7e44d3c2ffaf`, `Validate Game Project Operating System` run `32576426840`, final `ci-gate=success`.
- Auto-merge PR: `NOT_RUN` for this profile refresh; repository capability only was verified.
- Auto-merge enabled at: repository setting observed enabled on 2026-08-23; original enable timestamp not available from the observed metadata.
- Observed merge method: repository-level settings and protected default-branch Ruleset are both squash-only.
- Observed merge commit: PR #614 squash-merged to `main` as `8dd79816aa39704a8ede8acc965ea452bb5cebc6`.
- Remaining unverified settings: account plan, private vulnerability reporting, CODEOWNERS review-request behavior, repository Actions budget/retention configuration, and a current per-PR auto-merge execution.

## Update boundary

Update this profile in the same change as a verified repository rename, transfer, visibility/default-branch change, repository merge-method setting change, Required Check change, Ruleset behavior change, auto-merge capability change, or newly observed platform behavior. Update `.github/CODEOWNERS`, security routes, workflows, templates, and their regression tests when the changed identity or setting affects them. Do not rewrite frozen release locks to represent current mutable state.
