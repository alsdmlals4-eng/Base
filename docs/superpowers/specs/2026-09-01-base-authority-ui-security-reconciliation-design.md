# Base Authority, UI Workflow, and Security Reconciliation Design

## Decision

Base uses the V4 repository-first workspace contract as the sole active default. The V3 Notion domain-split contract remains a compatibility and history source only; it cannot be an active route for new project work.

The approved successor work also restores two independently useful, stale PR proposals on fresh `main`: project-specific UI production planning from PRs #803 and #804, and backend authorization denial-path guidance from PR #809. The source PRs remain read-only; their material is re-evaluated and selectively reimplemented on current-main successor branches.

## Problem and observed evidence

- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` is `ACTIVE_DEFAULT`, declares `REPOSITORY_PRIMARY_CANON`, and retires new Notion writes by default.
- Current active entrypoints and templates still direct new work to the V3 contract and `NOTION_DEFAULT_PROJECT_WORKSPACE`. This creates two incompatible active answers to the same authority question.
- PRs #803, #804, and #809 are open but behind current `main`; their historical CI and review state cannot prove a merge-safe current result. PR #803/#804 overlap on UI production material. PR #809 contains unresolved review findings about authorization evidence granularity.

## Approved requirements

1. Preserve V3 documents and keys needed for compatibility, migration, and history, but mark their contract as `V3_COMPATIBILITY_AND_HISTORY_ONLY` and disable it for new-work routing.
2. Update every active V4 entrypoint, Skill, and project bootstrap template in the actual impact map so it explicitly routes to the V4 policy and machine contract.
3. Add machine regression coverage that fails if an active entrypoint restores the V3 contract as the default while allowing explicitly marked legacy history to remain.
4. For UI planning, require a project-specific screen/action/flow discovery pass from that project's fresh-read implementation, product context, and relevant benchmark evidence. Do not impose a universal menu or button inventory. A screen, control, flow map, or wireframe exists only when it has a project need and an identified consumer or planned consumer.
5. Treat wireframes and flow maps as decision and implementation-planning evidence. They are not claims that Godot buttons, input paths, captures, or user validation already exist.
6. Preserve the separate evidence ceilings for static contracts, automated tests, Godot runtime capture, human review, and final player approval.
7. Rebuild UI and security work only from current `main`, with focused RED→GREEN regression coverage, normal PR CI, squash merge, and post-merge main readback. Do not update, rebase, force-push, or merge the stale source PR branches.
8. Make `MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT` a fixed precondition for every Base or project L1+ task. The preflight compares actual current consumers and task-relevant references, records an evidence-bound disposition, and discovers a project-specific direction; it never injects a universal game menu, flow, genre, or visual style.
9. Make `LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED` a fixed, scope-bounded precondition. Classify legacy context/configuration by owner and lifecycle, correct misleading active routes first, and remove material only after reference/consumer proof, Git-recoverable removal, and readback. Age or filename alone is not deletion evidence.
10. Prefer soft-coded project variation: values that may differ by project, benchmark, platform, presentation, or flow have one data/configuration/Resource/contract owner. Security, protocol, save compatibility, and other true invariants remain explicitly fixed with their migration path; do not build a generic configuration framework for one-off constants.

## Alternatives considered

| Option | Decision | Reason |
| --- | --- | --- |
| Keep V3 and V4 as parallel defaults | REJECT | A new worker can select conflicting canon and completion rules. |
| Delete the V3 contract and all Notion-era material | REJECT | Compatibility, migration provenance, and historical regression evidence would be destroyed. |
| V4 as the one active default; V3 preserved only as explicitly inactive compatibility/history | ADOPT | Removes active ambiguity while preserving recovery and migration evidence. |
| Require fixed buttons such as New Game, Continue, Settings, or Exit in every project | REJECT | Genre, platform, and actual player path determine whether any control is needed. |
| Let every project invent UI without an evidence-based discovery pass | REJECT | It leaves screen/action gaps invisible until late implementation. |
| Derive project-specific flows and wireframes from fresh-read consumers plus relevant benchmarks | ADOPT | It guides necessary implementation without turning references or a generic menu into product canon. |
| Treat an old file name or a broad repository scan as enough reason to delete or compress material | REJECT | It loses compatibility and unique evidence while creating new reference and token-recovery failures. |

## Architecture and boundaries

```text
V4 policy + V4 JSON machine contract
  → active Base entrypoints / Skills / project templates
  → benchmark·reverse-engineering preflight + scoped context/configuration hygiene
  → project repository fresh-read
  → project-specific screen · action · flow inventory
  → benchmark-informed wireframe or flow proposal where useful
  → approved project canon and implementation handoff
  → code · scene · input · save/load · runtime capture evidence

V3 contract / historical Notion material
  → explicit compatibility or read-only migration only
```

The V4 policy owns the authority decision. Active routers only link to it and must not recreate a second authority model. The UI production owner will own benchmark and flow discovery; a project owns its actual genre, world, screens, buttons, Godot scenes, images, and runtime evidence. The backend guide owns security requirements; a project contract records applicable evidence without promoting a template field to runtime security proof.

## Scope-bounded hygiene audit for this correction

| Candidate | Classification | Evidence and action |
| --- | --- | --- |
| `PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` and active routers/templates | `ACTIVE_OWNER` | The only active default; corrected stale entrypoints to route here. |
| `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` V3 and V3 literals | `COMPATIBILITY` | Required for migration/history and explicit regression coverage; retained with `V3_COMPATIBILITY_AND_HISTORY_ONLY` and `active_route_for_new_work: false`. |
| Legacy Notion flow/visual policy routes | `COMPATIBILITY` | Retained only as migration/reference material and linked in the documentation map with an explicit V4 non-default boundary. |
| Unread or untraced historical material outside the authority impact map | `UNKNOWN_UNVERIFIED` | Not deleted or bulk rewritten. It is outside this correction's scope until a consumer/provenance audit selects it. |

No `OBSOLETE_CANDIDATE` in this authority-impact set reached the removal gate: V3 content has documented compatibility/test consumers. The actual cleanup was therefore route correction and explicit classification, not destructive pruning.

## Failure handling and rollback

- A failed authority regression is corrected in the active entrypoint that restores the obsolete route; V3 historical content is not deleted to make the test pass.
- If a project has a genuine exception requiring Notion as an active surface, it must use the V4 explicit project-specific exception gate with owner, scope, measurable value, and revisit condition.
- If a UI source-PR proposal lacks a current project consumer or benchmark evidence, it remains a proposed item rather than a required button or a completed implementation claim.
- If a security surface is not exposed, it is recorded as justified `NOT_APPLICABLE`; if it is exposed but lacks an executed denial readback, it remains `NOT_RUN` or `BLOCKED_UNVERIFIED`.
- Each successor is a squash-mergeable, reversible PR. No protected-branch bypass, force update, or bulk history rewrite is permitted.

## Verification design

- V4 authority: focused contract tests, active-source reference scan, full local validation, remote required checks, post-merge readback.
- UI successor: RED tests for project-specific flow discovery and no-fixed-controls policy, targeted parser/contract checks, reference freshness, remote CI, and no runtime overclaim.
- Security successor: RED tests for each validated PR #809 review finding, contract test suite, focused guide/template propagation checks, reference freshness, remote CI, and no deployment/runtime-security overclaim.
- Every retained branch: five complete adversarial loops, then further loops until no valid finding remains; run again on the merged `main` state.
