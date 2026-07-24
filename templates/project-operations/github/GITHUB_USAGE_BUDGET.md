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
| Base | public | cost-aware | 0 billed standard minutes expected | publication, Windows smoke | optimize for speed and reliability |
| omenward | private | cost-aware | | Godot, Windows, publication | Pro pilot |

## Alert Response

- 70%: identify top workflows and repeated matrix axes.
- 85%: move non-blocking full matrix to nightly/manual and shorten artifact retention.
- 100% or budget stop: mark affected validation `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`; do not auto-merge.

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
