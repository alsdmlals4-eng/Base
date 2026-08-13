# Universal Loop Engineering Program Implementation Plan

> **Execution:** Use `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Every phase uses an isolated branch/worktree, true TDD, exact-head review, and a revertable PR.

**Goal:** Build one project- and genre-agnostic Loop Engineering platform that implements user-approved planning and art direction without omissions, unauthorized additions, planning drift, visual drift, or cross-project context leakage.

**Architecture:** Base owns a deterministic Kernel, machine contracts, evidence gates, and reusable capabilities. Each project owns a declarative Capsule with Planning Lock, Visual Lock, runtime adapter, implementation packages, coverage ledger, active-run pointer, and immutable run history. A bounded Builder edits one isolated worktree; deterministic validators and a separate read-only Critic review the actual diff and evidence.

## Invariants

- Human-led WHAT/WHY; Agent-led HOW.
- Product work requires `PLANNING_LOCKED`.
- Visual work requires `VISUAL_LOCKED`; Figma is only one optional provider.
- Every approved requirement maps to tasks, outputs, tests, and required evidence.
- Every changed output maps back to an approved requirement.
- Planning, player experience, art direction, assets, major UX, save/data meaning, security, permissions, and governance are protected.
- Project canon, assets, sessions, worktrees, credentials, leases, and Agent context are isolated.
- Initial maximum autonomy is `A2_EXECUTE_ISOLATED`.
- A3 allowlist is empty and Scheduler is `NOT_CONFIGURED`.
- Unrun Runtime, visual, Android, playtest, human, or provider evidence is not PASS.

## Milestones

### M0 — Design Canon

Rebase approved design and plans onto current Base main, run exact-head CI and independent review, merge, read back new main, and preserve the former PR #322 branch as backup.

### M1 — Protected Path Safety

Resolve Base #314 in the existing matcher owner. Test exact directories, one-level/deep descendants, sibling prefixes, Windows separators, Unicode NFC, explicit files, wildcards, and exact reconciliation of multiple approved nested paths. Run a Blacksmith nested-path pilot, merge, postmerge validate, and close the issue.

### M2 — Contract Platform

Add JSON Schema Draft 2020-12 contracts for Capsule, Planning Lock, Visual Lock, Runtime Adapter, Implementation Package, Requirement Coverage, Active Run, and Immutable Run. Add templates, valid/invalid fixtures, bundle validation, project-isolation checks, visual-impact gates, coverage completeness, reverse mapping, migration guidance, and documentation routing. Do not add a new ACTIVE Skill or Work Mode.

### M3 — Deterministic SHADOW Runtime

Add typed models, project-bound atomic IO, Git freshness, entry policy, coverage, drift, leases, state machine, immutable ledger, runner, and `loopctl validate|shadow|status|leases`. SHADOW invokes no model and changes no product path. Inject stale SHA, cross-project references, missing coverage, visual gaps, lease conflicts, path escape, duplicate input, repeated failure, and receipt-overwrite attempts.

### M4 — Repeatable A2 Runtime

Add isolated worktree management, bounded commands, exact-pinned Codex Builder worker, strict Python bridge, deterministic diff/coverage/evidence gate, separate read-only Critic, limited GitHub PR provider, `run-a2`, and postmerge `close`. Builder has no push/merge/settings authority and network is denied by default. Complete three consecutive triggered A2 runs without drift, omission, unauthorized addition, regression escape, or rollback.

### M5 — Cross-Project Generality

Migrate Blacksmith, pilot one narrative/data project, and pilot one visual/UI project. Kernel changes between pilots must be 0; project-specific worker code must be 0 unless promoted to a reusable capability. Planning/visual drift escapes, unmapped requirements, unauthorized additions, and cross-project leaks must all be 0.

## Rollback

Revert milestone PRs independently in reverse order. Preserve immutable run history and planning/visual/evidence sources. A project failure disables only that Capsule unless the shared Kernel is proven defective.

## Completion

Claim `MULTI_PROJECT_LOOP_ENGINEERING_READY` only after M5 has direct evidence. Until then, report the highest completed milestone and keep later stages `NOT_RUN`, `NOT_CONFIGURED`, or `BLOCKED_UNVERIFIED`.
