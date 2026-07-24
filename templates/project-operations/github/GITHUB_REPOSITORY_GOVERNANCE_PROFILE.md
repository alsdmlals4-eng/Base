# GitHub Repository Governance Profile

## Repository

```yaml
repository:
  name:
  visibility: public | private
  account_plan: Free | Pro | Team | Enterprise
  primary_branch: main
  rollout_stage: BASE | PILOT | ACTIVE | DEFERRED
  last_verified_at:
  verified_by:
```

## Pull Request Policy

```yaml
pull_requests:
  required: true
  allowed_merge_methods:
    - squash
  auto_merge: enabled | disabled | unverified
  merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS | MANUAL_USER_APPROVAL
  required_approving_review_count: 0
  required_review_thread_resolution: true
  require_code_owner_review: false
  require_last_push_approval: false
```

## Required Checks

```yaml
required_checks:
  primary: ci-gate
  additional: []
  strict_up_to_date: true
  last_observed_success_sha:
  status: verified | unverified | blocked
```

## Ruleset

```yaml
ruleset:
  name: solo-main-safety
  source_template: templates/project-operations/github/rulesets/solo-main-safety.json
  enforcement: active | disabled | unverified
  default_branch_targeted: true | false | unverified
  pull_request_required: true | false | unverified
  linear_history: true | false | unverified
  force_push_blocked: true | false | unverified
  deletion_blocked: true | false | unverified
  required_check_context: ci-gate
```

## Auto-merge Gate

```yaml
auto_merge_gate:
  package_status:
  reviewed_head_sha:
  current_head_sha:
  required_checks_passed: true | false | unverified
  unresolved_review_threads: 0
  user_review_required: false
  change_proposal: false
  repository_setting_verified: true | false
  result: AUTO_MERGE_ELIGIBLE | AUTO_MERGE_ENABLED | AUTO_MERGE_BLOCKED | UNVERIFIED_REPOSITORY_SETTING
```

## Actions Budget

```yaml
actions:
  public_repository_standard_minutes: free | not_applicable | unverified
  private_repository_included_minutes:
  monthly_soft_limit:
  stop_usage_at_budget_limit: true | false | unverified
  artifact_retention_days:
  high_cost_jobs:
    - job:
      condition:
      expected_minutes:
```

## Rollback

```yaml
rollback:
  disable_ruleset:
  disable_auto_merge:
  convert_pr_to_draft:
  restore_required_check:
  recovery_owner:
  resume_condition:
```

## Evidence

- Repository settings snapshot:
- Ruleset URL or ID:
- Required Check run:
- Auto-merge PR:
- Remaining unverified settings:
