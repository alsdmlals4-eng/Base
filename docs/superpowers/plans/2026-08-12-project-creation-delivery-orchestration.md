# Project Creation & Delivery Orchestration Implementation Plan

**Goal:** Add one thin orchestration Guide that coordinates existing Base owners for planning/review/visual production/localization/responsive UI/local execution/incident learning/narrative event ideation without creating a new broad Skill.

**Architecture:** Keep domain truth in current owners. Add only cross-owner phase/gate semantics to a new game-development knowledge Guide, route it one hop from the game-development README, and wire focused regression into the existing Evidence Knowledge workflow.

**Baseline:** `aa45a7589cede16be027b55f15ea4813681df8e3`

## Task 1 — RED contract first

Files:
- create `tests/test_project_creation_delivery_orchestration.py`
- modify `.github/workflows/validate-evidence-knowledge.yml`

Contract must fail while the Guide and README route do not exist.

Required RED reasons:
- missing `PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md`
- missing one-hop README route

The workflow must compile and run the new test in the existing `evidence-knowledge-contract` job. Do not create a new Required Check.

## Task 2 — Minimal GREEN implementation

Files:
- create `docs/knowledge/game-development/PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md`
- modify `docs/knowledge/game-development/README.md`

The Guide coordinates:
1. `PLANNING_COMPLETE -> FINAL_REVIEW_COMPLETE -> SERIAL_VISUAL_PRODUCTION -> CODEX_BUILD_ALLOWED` when the project adopts final visual production gating.
2. Visual inventory/style lock and one-at-a-time approval loop for user-gated production.
3. Project-declared localization readiness, while keeping exact locale list project-owned.
4. PC standard / wide / mobile landscape semantic layout parity rather than pixel identity.
5. Existing dedicated local environment contract; Hera remains live QA/observability and is not prohibited.
6. Bounded workaround, Base Case/Learning/BCP lookup, verified new-case feedback.
7. `MESSAGE_AND_CHARACTER_BEFORE_EVENT` as a narrative ideation heuristic, not a forced moral.

## Task 3 — Focused verification

At exact PR head:
- Evidence Knowledge workflow must be terminal Green.
- Base v9 contract/integrity workflow must be terminal Green if triggered.
- Dependency review or other triggered checks must be terminal Green or explicitly not applicable.
- No unresolved review threads.

## Task 4 — Adversarial review

Attack:
- authority duplication
- project-specific values promoted to Base defaults
- pixel-identical responsive layout interpretation
- planning visualizations accidentally blocked
- Hera ban or authority inflation
- incident workaround without root-cause/evidence discipline
- one incident auto-promoted to active Base rule
- message-first becoming preachy universal law
- duplicate/new broad Skill
- current-main drift and PR #301 overlap

Validate each critique before changing anything. Fix only confirmed findings, rerun exact-head checks.

## Task 5 — Merge and reconciliation

Before merge:
- refetch current `main`
- refetch all Open/Draft PRs
- compare current main to PR base/head
- require strict up-to-date or rebase/recreate on current main
- require exact reviewed head SHA
- require required checks Green
- require unresolved threads = 0

Then squash merge if repository/ruleset allows. After merge:
- read new main SHA
- verify changed files on new main
- rerun/inspect post-merge workflow evidence where available
- reread remaining Open/Draft PRs for stale/overlap state
- report before/after/expected effects and local instruction artifact SHA.
