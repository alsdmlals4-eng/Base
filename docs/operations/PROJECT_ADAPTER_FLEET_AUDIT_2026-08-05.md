# Project Adapter Fleet Audit — 2026-08-05

## Status

```yaml
audit_id: BASE-AUD-2026-08-05-PROJECT-ADAPTER-FLEET
base_pr: 175
scope:
  - alsdmlals4-eng/Ten-Paces-Hidden-Moves
  - alsdmlals4-eng/Blacksmith
  - alsdmlals4-eng/omenward
  - alsdmlals4-eng/urban-legend
  - alsdmlals4-eng/GRIMOIRE-
  - alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
result: BASE_CONTRACT_HARDENED_PROJECT_ROLLOUT_BLOCKED
runtime_validation: NOT_RUN
project_mutations: NOT_STARTED
```

This audit compares each repository's current `main` and canonical
`skills/PROJECT_BASE_ADAPTER.json` against
`schemas/project-base-adapter-v1.schema.json` and the Base project operating
validator. It does not treat the presence of an adapter file as proof that the
adapter is executable.

## Adversarial findings

### P1 — released project pins were not representable by the v1 Schema

The live project adapters use `base_release.finalization_commit`, while the
canonical v1 Schema used `additionalProperties: false` and did not declare the
field. Base PR #175 adds only this explicit release pin. The Schema remains
strict; it is not widened to accept arbitrary project state.

A second RED test proved that structural validation alone was insufficient:
an arbitrary 40-character SHA could pass because the semantic release-lock
validator ignored the new field. The release index now binds v9.4.3 to the
actual immutable finalization commit and rejects forged, absent, or
non-descendant finalization identity.

### P1 — actual project adapters are absent from Base CI

Base's focused tests validate the template and synthetic repositories. They do
not validate the six remote canonical adapters. A green Base CI therefore did
not prove fleet compatibility.

Each project must install and require the canonical project validation
workflow. The workflow must use an immutable full Base validator commit rather
than floating `main`.

### P1 — every inspected protected baseline is stale

All six project `main` branches advanced after their adapter baseline was
recorded. The current validator intentionally requires exact equality between
the adapter baseline and the trusted remote or PR base. Therefore a structurally
valid adapter can still fail until its baseline and policy hash are refreshed.

Do not weaken this check silently. The operating policy must choose between:

1. preserving exact equality and making baseline refresh a required, automated
   part of every accepted project change; or
2. allowing an ancestor baseline only when an independently computed protected
   path diff proves that the policy and protected paths did not change.

The current recommendation is option 1 because it is simpler to audit and fails
closed. Automation should remove the repetitive manual work rather than weaken
the authority boundary.

### P1 — three repositories use the adapter as a project-state database

Blacksmith, GRIMOIRE, and Switchy Express place planning state, evidence state,
entrypoints, decision summaries, or custom validator objects in the canonical
adapter. This conflicts with the thin-adapter ownership rule and with the
strict v1 Schema.

Project operating state belongs in project health, decision, planning, or
evidence artifacts. The canonical adapter should retain only release pins,
routes, registries, project bindings, protected baseline, protected paths,
validators, compatibility views, and narrowly scoped overrides.

## Compatibility matrix

| Project | Audited `main` | Adapter shape | Primary blockers | Verdict |
|---|---|---|---|---|
| Ten Paces: Hidden Moves | `4b5967dee99592de4a09a611068344994e1ee026` | Close to v1 | protected baseline is one commit behind; canonical Base validator workflow is not installed | `P1_MIGRATION_REQUIRED` |
| Blacksmith | `b1dd945875568098b107815a03e88b0272d384e9` | v1 label, non-v1 payload | root project-state objects, invalid route status, invalid baseline authority/source types, null policy or registry evidence, stale baseline | `P1_REBUILD_THIN_ADAPTER` |
| OMENWARD | `da382d52b4490acb8758a1683ea6c9e4f4bf388b` | Close to v1 | protected baseline is one commit behind; canonical Base validator workflow is not installed | `P1_MIGRATION_REQUIRED` |
| urban-legend | `f7edb459938bb5f3e2533ad828c2fe55019cd14b` | Close to v1 | protected baseline is one commit behind; canonical Base validator workflow is not installed | `P1_MIGRATION_REQUIRED` |
| GRIMOIRE | `2d80e4afcfc6b530b76912826f5984cdf1184678` | custom schema v2 | incompatible root shape, mixed project-state authority, missing v1 validator list and baseline contract, stale baseline | `P1_CANONICAL_MIGRATION_REQUIRED` |
| Switchy Express | `0bdcdae2092460431f81d383b34b51f725a4ab08` | v1 label, non-v1 payload | string routes instead of route records, object validators instead of commands, invalid Sheet and baseline enums, stale baseline | `P1_REBUILD_THIN_ADAPTER` |

## Applied Base corrections

Base PR #175 currently provides the following backward-compatible corrections:

1. model `base_release.finalization_commit` as an optional full SHA in the v1
   Schema so older v9.1 adapters remain valid;
2. include the field in the canonical adapter template;
3. index the canonical v9.4.3 finalization commit outside the immutable released
   lock and fail closed when a project supplies a forged or inconsistent pin;
4. pin the copied project validation workflow to the immutable validator commit
   that contains structural and semantic finalization validation;
5. wire the focused fleet-hardening test into required Base contract CI.

The project repositories are intentionally not mutated before this Base
contract is reviewed. A project PR must not depend on an unreviewed floating
Base branch. After merge, the workflow pin should be advanced once to the
merged trusted validator commit before the six-project rollout.

## Benchmark and collaboration decisions

The audit used official platform guidance as an external check on the local
contract rather than copying a framework wholesale.

### Applied now

- GitHub recommends full commit SHAs as the safest immutable reference for
  third-party Actions and reusable automation. The project validator template
  therefore pins both Actions and the Base validator repository by full SHA.
- JSON Schema's closed-object pattern rejects undeclared properties. The Base v1
  Schema retains `additionalProperties: false`; only the explicitly governed
  `finalization_commit` field was added.
- Workflow and contract changes must be protected by required checks and code
  ownership. Base already owns `.github/` through CODEOWNERS; project rollout
  PRs must make adapter validation required before merge.
- Project changes are split into independent PRs so Base contract review,
  project migration, product changes, and Google Sheets changes cannot silently
  attest to each other.

### Evaluated but deferred

GitHub reusable workflows can reduce duplicated CI across repositories. A
cross-repository reusable validator is a reasonable later optimization, but it
is deferred until repository visibility, caller permissions, failure reporting,
and rollback are piloted. The first rollout keeps a small checked-in caller
workflow pinned to one immutable Base validator commit. This is more repetitive
but easier to audit and roll back while the contract is still stabilizing.

### Primary references

- https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://json-schema.org/understanding-json-schema/reference/object#additional-properties

## Rollout plan

### Wave A — narrow repair

- Ten-Paces-Hidden-Moves
- omenward
- urban-legend

For each repository:

1. refresh the adapter baseline against the exact PR base;
2. recompute the baseline policy and project registry hashes;
3. install the exact-SHA Base validator workflow;
4. run the full project operating validator;
5. verify that no project state was added to the adapter;
6. open one isolated Draft PR.

### Wave B — thin-adapter rebuild

- Blacksmith
- Switchy-Express-Cargo-Puzzle

First preserve project-only state in canonical project health, decision, and
evidence files. Then rebuild the adapter from the v1 contract without deleting
or weakening project canon.

### Wave C — schema-authority reconciliation

- GRIMOIRE-

The custom schema-v2 file must not silently redefine Base's canonical adapter.
Recommended disposition:

- restore `skills/PROJECT_BASE_ADAPTER.json` as the Base v1 thin adapter;
- move the current schema-v2 project-state payload to a clearly named project
  operating-state artifact;
- retain a migration record and compatibility view if an active consumer still
  requires the old shape.

This is a canonical authority change and requires an explicit project decision
before migration.

## PR review rules

A project adapter PR is not ready unless all of the following are true:

- adapter validates against the exact pinned Base validator commit;
- adapter baseline equals the trusted PR base;
- release, finalization, and registry pins resolve to immutable canonical content;
- Base routes are records, not untyped strings;
- validator entries are executable command strings;
- project state is not embedded in the adapter root;
- existing project canon and protected paths are unchanged unless separately
  approved;
- exact-head CI is green;
- unresolved review threads are zero;
- unexecuted runtime or human checks remain explicitly `NOT_RUN`.

## Evidence limits

This audit is repository-contract evidence. It does not prove Godot runtime,
Google Sheets readback, human usability, project gameplay correctness, or
release readiness. Those checks remain project-specific and must not be
promoted by adapter validation alone.
