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
  last_verified_at: 2026-08-01
  verified_by: GitHub repository metadata
```

## Current platform evidence

```yaml
platform_status:
  required_check: ci-gate
  required_check_status: VERIFIED_PR_127
  ruleset: unverified
  codeowners_owner: "@alsdmlals4-eng"
  codeowners_review_request: NOT_RUN
  private_vulnerability_reporting: UNVERIFIED_REPOSITORY_SETTING
  dependabot_configuration: PRESENT_NOT_RUN
  dependabot_pnpm_11: DEFERRED_UNTIL_OFFICIAL_SUPPORT
```

`required_check_status` records that the exact-head `ci-gate` completed and satisfied the merge gate on PR #127. It does not prove every Ruleset option. The remaining states stay unverified or not run until GitHub supplies direct evidence.

## Update boundary

Update this profile in the same change as a verified repository rename, transfer, visibility/default-branch change, Required Check change, or newly observed platform behavior. Update `.github/CODEOWNERS`, security routes, workflows, and their regression tests when the changed identity or setting affects them. Do not rewrite frozen release locks to represent current mutable state.
