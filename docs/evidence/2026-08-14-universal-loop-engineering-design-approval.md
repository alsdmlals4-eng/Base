# Universal Loop Engineering Design Approval Evidence

## Identity

- Tracking issue: `#321`
- Pull request: `#322`
- User approval: `2026-08-14`
- Observed current main before this evidence commit: `3e3f59b1b835f9675f0b8dbc4543a6c69a526c36`
- Previous PR head backup: `backup-pr322-pre-current-main-20260814`

## Approved intent

- One deterministic shared Loop Kernel.
- Project-local declarative Execution Capsules.
- Human-led WHAT/WHY and Agent-led HOW.
- Planning Lock and Visual Lock protect approved design intent.
- Figma is optional only as a Visual Lock provider.
- Requirement Coverage blocks omissions and unauthorized additions.
- Canon, assets, sessions, worktrees, credentials, leases, and Agent context are project-isolated.
- Initial maximum autonomy is A2 isolated execution.
- A3 allowlist is empty.
- Scheduler is `NOT_CONFIGURED`.

## Changed scope

Documentation only:

```text
docs/superpowers/specs/2026-08-13-universal-loop-engineering-project-capsule-design.md
docs/superpowers/specs/2026-08-13-universal-loop-engineering-project-capsule/**
docs/superpowers/plans/2026-08-13-universal-loop-engineering-program.md
docs/evidence/2026-08-14-universal-loop-engineering-design-approval.md
```

No Schema, Runtime, Skill Registry, Workflow, project product, planning canon, Figma file, asset, permission, or repository setting is changed.

## Preflight

- Open PR #330 path overlap: 0.
- Open PR #331 path overlap: 0.
- Base #314 remains the first implementation dependency.

## Completion boundary

This PR approves design and implementation order only. It does not claim that Base #314, Capsule schemas, SHADOW Runtime, A2 provider Runtime, Blacksmith migration, cross-project pilots, A3, or Scheduler are complete.

## Required integration evidence

- Ready-state exact-head workflows PASS.
- Independent review: P0 0 / P1 0.
- Unresolved review threads: 0.
- Merge-time main freshness and path-overlap recheck.
- Squash merge with expected head.
- Postmerge main readback and push workflows.

## Rollback

Revert the documentation merge. No project data, product Runtime, or asset migration is required.
