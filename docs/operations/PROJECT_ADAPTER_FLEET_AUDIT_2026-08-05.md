# Project Adapter Fleet Audit — 2026-08-05 / 2026-08-06 Rollout Addendum

## Status

```yaml
audit_id: BASE-AUD-2026-08-05-PROJECT-ADAPTER-FLEET
parent_decision: DEC-BASE-20260805-001
base_contract_pr: 185
trusted_base_validator: bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
validator_pin_pr: 187
scope:
  - alsdmlals4-eng/Ten-Paces-Hidden-Moves
  - alsdmlals4-eng/Blacksmith
  - alsdmlals4-eng/omenward
  - alsdmlals4-eng/urban-legend
  - alsdmlals4-eng/GRIMOIRE-
  - alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
result: FOUR_PROJECTS_MERGED_ONE_BLOCKED_ONE_SEPARATELY_MANAGED
project_rollout: PARTIAL_COMPLETE
completed_projects: 4
blocked_projects: 1
separately_managed_projects: 1
google_sheets_sync: NOT_APPLICABLE_BASE_CONTRACT
runtime_validation: NOT_RUN
physical_device_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
```

The original audit identified fleet drift before Base contract hardening. This
addendum records the later project-by-project outcome. It does not reinterpret
repository-contract validation as gameplay, Runtime, device, human, Sheet, or
release evidence.

## Original adversarial findings and disposition

### P1 — released finalization pins were not representable or semantically bound

The strict v1 Schema did not model the already-used
`base_release.finalization_commit`, and semantic validation did not reject an
arbitrary 40-character value.

Disposition:

- resolved in Base PR #185;
- strict `additionalProperties: false` retained;
- supplied finalization identity is bound to Base's release index and ancestry;
- project validator is pinned to immutable trusted merge
  `bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1` by merged PR #187.

### P1 — project validation floated or was absent

The initial project repositories did not all run the canonical validator, and a
floating Base reference could change results over time.

Disposition:

- resolved for the four merged project migrations through project-local caller
  workflows pinned to the trusted Base merge;
- unresolved for OMENWARD because its Actions job cannot obtain a runner and a
  Base-owned external run cannot read the private repository;
- OMENWARD remains `BLOCKED_ENVIRONMENT_RUNNER_AND_AUTHORIZATION`.

### P1 — stale exact baselines

All audited projects had advanced beyond their recorded protected baseline.
Option A exact trusted-base equality was approved.

Disposition:

- the four completed PRs refreshed baseline and dependent hashes against their
  exact PR base;
- OMENWARD PR #148 proposes the narrow repair but has not produced trusted
  generator and validator evidence;
- no ancestor-baseline exception was introduced.

### P1 — adapters used as project-state databases

Blacksmith, Switchy Express, and GRIMOIRE mixed project operating state with the
Base connection contract.

Disposition:

- Blacksmith PR #112 preserved the broad previous adapter and health authority,
  then restored a strict thin adapter;
- Switchy Express PR #87 preserved the incompatible adapter and legacy authority,
  separated project-only Registry ownership, then restored a strict thin adapter;
- GRIMOIRE is `SEPARATELY_MANAGED` outside this rollout thread and is not claimed
  complete here.

## Current compatibility and rollout matrix

| Project | Exact migration base | Implementation evidence | Current disposition |
|---|---|---|---|
| Ten-Paces-Hidden-Moves | `4b5967dee99592de4a09a611068344994e1ee026` | PR #95, merge `7083829d8eb627e46227c0ac98845adfc2c61bb4` | `MERGED_VALIDATED` |
| urban-legend | `f7edb459938bb5f3e2533ad828c2fe55019cd14b` | PR #153, merge `1cda33f9eb238c9a32d0a8f4a3edfa5e203b0634` | `MERGED_VALIDATED` |
| Blacksmith | `b1dd945875568098b107815a03e88b0272d384e9` | PR #112, merge `4dc4f3f8a6fc4d379c5eddce8b59fc8733e6a4ed` | `MERGED_VALIDATED_THIN_ADAPTER` |
| Switchy-Express-Cargo-Puzzle | `8c6dd60c634019e64178e72aa4959a2a970708e1` | PR #87, merge `dc2a6696beced12c8e352fa154648cdb4e80796b` | `MERGED_VALIDATED_THIN_ADAPTER` |
| OMENWARD | `f5e4bcee7f8459fcfeb492f1ebc19ff932a352f0` | Draft PR #148; trusted execution unavailable | `BLOCKED_ENVIRONMENT_RUNNER_AND_AUTHORIZATION` |
| GRIMOIRE | project-owned | issue #66 and separate project workflow | `SEPARATELY_MANAGED` |

## Completed project evidence

### Ten Paces — PR #95

- baseline and policy/Registry identity refreshed from the exact PR base;
- immutable Base validator workflow installed;
- official Snapshot, Dashboard, router, and compatibility views regenerated;
- seven-file adapter/generated scope;
- all eight observed exact-head workflows passed;
- product, gameplay canon, Runtime files, and Google Sheets unchanged.

### urban-legend — PR #153

- baseline and hashes refreshed from the exact PR base;
- immutable Base validator workflow installed;
- official generated views refreshed;
- seven-file adapter/generated scope;
- all seven exact-head workflows passed;
- canon, episode data, product files, Runtime files, and Google Sheets unchanged.

### Blacksmith — PR #112

- previous broad adapter and rich health authority preserved before normalization;
- project state moved out of the Base connection adapter;
- strict Base v1 thin adapter and valid machine health installed;
- official generated views refreshed;
- all seven exact-head workflows passed;
- no product, gameplay canon, Runtime, or Google Sheet mutation.

A separately developed duplicate was closed as
`SUPERSEDED_DUPLICATE_PR_113`; it must not be reopened or used as implementation
authority.

### Switchy Express — PR #87

- incompatible adapter and legacy authority preserved;
- Base routes normalized to typed records;
- project Registry narrowed to project-owned authority while retaining compatible
  identity fields;
- Sheet meaning preserved without a Sheet write;
- official generated views and legacy consumers updated;
- all seven exact-head workflows passed;
- no product, Godot, Android/APK evidence, or Google Sheet mutation.

A separately developed duplicate was closed as
`SUPERSEDED_DUPLICATE_PR_90`; it must not be reopened or used as implementation
authority.

## OMENWARD fail-closed record

Draft PR #148 remains the only active OMENWARD migration proposal.

```yaml
pull_request: 148
project_head: cd8266f51f206bcd600f2e8e98604d1ee9d6ec2d
exact_pr_base: f5e4bcee7f8459fcfeb492f1ebc19ff932a352f0
repository_actions: BLOCKED_BEFORE_STEP_EXECUTION_RUNNER_ID_0
external_base_run: 31052501249
external_base_job: 92462657680
external_checkout: BLOCKED_PRIVATE_REPOSITORY_AUTHORIZATION
base_generator: NOT_RUN
base_validator: NOT_RUN
merge_status: BLOCKED_ENVIRONMENT_RUNNER_AND_AUTHORIZATION
```

A trusted completion path must restore repository Actions or explicitly provide
a read-capable GitHub App/PAT for isolated validation. Static diff review alone
is insufficient.

## GRIMOIRE separation boundary

GRIMOIRE remains `SEPARATELY_MANAGED`. Its issue #66, project decisions,
project-specific PRs, planning authority, and Google Sheet synchronization are
outside this Base rollout status PR. This audit neither modifies nor attests to
that project state.

## Benchmark and collaboration decisions retained

Applied:

- full commit SHA pinning for Actions and Base validation;
- strict closed-object JSON Schema;
- required checks and code-owner review;
- isolated Base and project PRs;
- exact trusted-base equality with automated refresh rather than a weaker
  ancestor exception;
- state preservation before rebuilding non-thin adapters.

Deferred:

- a cross-repository reusable validator workflow requiring private-repository
  permission, visibility, failure-reporting, and rollback design;
- this deferral is validated by the OMENWARD private-checkout failure.

## Project PR review rules

A project adapter PR is not ready unless all are true:

- the adapter validates against the exact pinned Base validator commit;
- adapter baseline equals the trusted PR base;
- release, finalization, policy, and Registry identities resolve to canonical
  immutable content;
- Base routes use typed records and validator entries are executable commands;
- project state is not embedded in the adapter root;
- generated outputs are produced by the official Base generator;
- protected product/canon paths remain unchanged unless separately approved;
- exact-head CI is green and unresolved review threads are zero;
- unexecuted Runtime, device, accessibility, and human checks remain `NOT_RUN`.

## Evidence limits

```yaml
google_sheets_sync: NOT_APPLICABLE_BASE_CONTRACT
runtime_validation: NOT_RUN
physical_device_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
project_gameplay_correctness: NOT_PROVEN
release_readiness: NOT_CLAIMED
```

The four merged project PRs prove repository adapter migration within their
recorded scopes. OMENWARD remains blocked, and GRIMOIRE remains separately
managed. This document does not promote any absent product or human evidence.
