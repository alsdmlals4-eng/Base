# GitHub Usage Budget

## Scope

```yaml
account:
plan: Pro
billing_cycle:
repositories:
  public: []
  private: []
```

## Included Usage

Record the current GitHub billing page values instead of copying assumptions from Base.

For public repositories, standard GitHub-hosted runners are the normal `REMOTE_CI` path and are not treated as paid-minute budget consumption. Larger/GPU runners and future private repositories remain billing-sensitive and must be verified against the current GitHub billing contract before use.

```yaml
included:
  actions_minutes:
  actions_storage_gb:
  packages_storage_gb:
  packages_transfer_gb:
  codespaces_core_hours:
  codespaces_storage_gb:
verified_at:
source: GitHub Billing and licensing page
```

## Limits

```yaml
limits:
  monthly_soft_limit_percent: 70
  monthly_warning_percent: 85
  stop_usage_at_budget_limit: true
  artifact_default_retention_days: 1
  artifact_release_retention_days:
```

## Repository Allocation

| Repository | Visibility | CI tier | Monthly target | High-cost jobs | Notes |
|---|---|---|---:|---|---|
| Base | public | cost-aware | 0 billed standard minutes expected | publication, Windows smoke | standard GitHub-hosted `REMOTE_CI`; optimize for speed and reliability |
| omenward | public | cost-aware | 0 billed standard minutes expected | Godot, Windows, publication | standard GitHub-hosted `REMOTE_CI`; larger/GPU runners require separate billing review |
| other active projects | public | cost-aware | 0 billed standard minutes expected | project-specific | verify visibility before applying this assumption |

## Two-mode response

- `REMOTE_CI` is the default whenever GitHub Actions can create the repository's Required Check.
- A zero paid budget does not select `LOCAL_FALLBACK` for a public repository using standard GitHub-hosted runners.
- `LOCAL_FALLBACK` is infrastructure-only: it may be attempted only when Actions cannot create any `ci-gate` Check Run for the current validation target and every exact-SHA safeguard in `docs/CI_EXECUTION_COST_POLICY.md` passes.
- If a `ci-gate` Check Run exists but is failed, cancelled, queued, or in progress, stay in `REMOTE_CI`; do not replace that result with a local status.
- If fallback preconditions or required local evidence cannot be satisfied, record `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`; do not auto-merge.

## Alert Response

- 70%: identify top workflows and repeated matrix axes for billing-sensitive usage.
- 85%: move non-blocking full matrix to nightly/manual and shorten artifact retention where evidence is preserved.
- 100% or budget stop on billing-sensitive usage: determine whether standard public `REMOTE_CI` remains available. If the Required Check cannot be created, apply the infrastructure-only fallback contract; otherwise continue `REMOTE_CI`.

## Monthly Evidence

```yaml
month:
used_actions_minutes:
used_actions_storage_gb:
used_packages_storage_gb:
used_codespaces_core_hours:
top_workflows: []
actions_taken: []
remaining_risks: []
```
