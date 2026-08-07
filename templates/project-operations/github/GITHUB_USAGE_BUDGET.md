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

- `REMOTE_CI` is the default for public repositories using standard GitHub-hosted runners. A zero paid budget does not select `LOCAL_FALLBACK`.
- A canonical `REMOTE_CI workflow run` on the current PR head owns validation even if the final `ci-gate` Check Run has not been created yet.
- Existing `ci-gate` Check Runs or commit statuses also block fallback ownership.
- `LOCAL_FALLBACK` is infrastructure-only and may be attempted only when the canonical remote run and existing gate evidence are absent, the change is locally reproducible, and every exact-SHA safeguard in `docs/CI_EXECUTION_COST_POLICY.md` passes.
- The Base default fallback boundary is conservative: documentation and limited canonical contract files may qualify; `CODE_OR_ENGINE` and `CI_TOOLCHAIN_HIGH_RISK` do not qualify without a repository-specific equivalent local validation contract.
- If a remote run/check exists but is failed, cancelled, queued, or in progress, stay in `REMOTE_CI`; do not replace that result with a local status.
- If fallback preconditions or required local evidence cannot be satisfied, record `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`; do not auto-merge.

## Alert Response

- 70%: identify top workflows and repeated matrix axes for billing-sensitive usage.
- 85%: move non-blocking full matrix to nightly/manual and shorten artifact retention where evidence is preserved.
- 100% or budget stop on billing-sensitive usage: determine whether standard public `REMOTE_CI` remains available. If remote ownership evidence is absent and the change is locally reproducible, apply the infrastructure-only fallback contract; otherwise continue `REMOTE_CI` or remain `UNVERIFIED`.

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
