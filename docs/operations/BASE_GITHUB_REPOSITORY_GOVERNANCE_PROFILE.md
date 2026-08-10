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
  last_verified_at: 2026-08-11
  verified_by: "GitHub repository metadata + Ruleset API + PR #274 exact-head CI"
```

## Pull Request Policy

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
```

`allowed_merge_methods` records the protected default-branch policy enforced by the active Ruleset. The repository-level settings currently also allow merge commits and rebase merges; that defense-in-depth mismatch is intentionally not changed by this profile-parity patch and remains a separate repository-setting follow-up.

## Required Checks

```yaml
required_checks:
  primary: ci-gate
  additional: []
  strict_up_to_date: true
  last_observed_success_sha: d5527fa4b4be390a1d7aae6caf1792c3587e6e04
  status: verified
```

`last_observed_success_sha` is PR #274's exact reviewed head. The `Validate Game Project Operating System` run for that SHA completed its final `ci-gate` successfully before merge to `main` as `ba4ad067684952d987790f0ebda1a96d9554bc09`.

## Ruleset

```yaml
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

Ruleset ID `19688076` was read directly from GitHub on 2026-08-11. It targets `~DEFAULT_BRANCH`, requires pull requests, review-thread resolution, linear history, strict `ci-gate`, and squash as the allowed protected-branch merge method, and blocks deletion and non-fast-forward updates.

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
  recovery_owner: alsdmlals4-eng
  resume_condition: repository settings and exact-head required-check evidence are reverified
```

Rollback changes repository enforcement only when the relevant failure is verified. Do not bypass a broken Ruleset by pushing directly to `main`, and do not rewrite frozen release locks to represent a mutable setting rollback.

## Current platform evidence

```yaml
platform_status:
  required_check: ci-gate
  required_check_status: VERIFIED_PR_274_HEAD_d5527fa4b4be390a1d7aae6caf1792c3587e6e04
  ruleset: VERIFIED_ACTIVE_ID_19688076
  codeowners_owner: "@alsdmlals4-eng"
  codeowners_review_request: NOT_RUN
  private_vulnerability_reporting: UNVERIFIED_REPOSITORY_SETTING
  dependabot_configuration: PRESENT
  dependabot_pnpm_11: DEFERRED_UNTIL_OFFICIAL_SUPPORT
```

`required_check_status` proves an exact-head `ci-gate` success for PR #274; it does not prove every future PR or repository setting. The Ruleset state above is direct GitHub API evidence. Remaining states stay unverified or not run until direct evidence exists.

## Evidence

- Repository settings snapshot: 2026-08-11 GitHub repository metadata — public, default branch `main`, `allow_auto_merge=true`, `allow_squash_merge=true`, `allow_merge_commit=true`, `allow_rebase_merge=true`.
- Ruleset URL or ID: `solo-main-safety`, ID `19688076`, enforcement `active`.
- Required Check run: PR #274 head `d5527fa4b4be390a1d7aae6caf1792c3587e6e04`, `Validate Game Project Operating System` run `31403471324`, final `ci-gate=success`.
- Auto-merge PR: `NOT_RUN` for this profile refresh; repository capability only was verified.
- Auto-merge enabled at: repository setting observed enabled on 2026-08-11; original enable timestamp not available from the observed metadata.
- Observed merge method: protected default-branch Ruleset allows `squash`; repository-level merge/rebase settings remain enabled and are a separate follow-up.
- Observed merge commit: PR #274 merged to `main` as `ba4ad067684952d987790f0ebda1a96d9554bc09`.
- Remaining unverified settings: account plan, private vulnerability reporting, CODEOWNERS review-request behavior, repository Actions budget/retention configuration, and a current per-PR auto-merge execution.

## Update boundary

Update this profile in the same change as a verified repository rename, transfer, visibility/default-branch change, Required Check change, Ruleset behavior change, auto-merge capability change, or newly observed platform behavior. Update `.github/CODEOWNERS`, security routes, workflows, templates, and their regression tests when the changed identity or setting affects them. Do not rewrite frozen release locks to represent current mutable state.
