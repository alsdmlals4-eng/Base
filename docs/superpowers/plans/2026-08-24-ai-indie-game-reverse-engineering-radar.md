# AI Indie Game Reverse-Engineering Radar Implementation Plan

> **For agentic workers:** use the existing planning/TDD/review lifecycle. This plan records the actual bounded implementation path and does not authorize project gameplay mutation.

**Goal:** Add a weekly AI-assisted solo/indie game reverse-engineering capture path that feeds existing Base source-discovery and reuse owners without creating a new Skill, scheduler, or runtime AI framework.

**Architecture:** One specialty Radar remains subordinate to the existing periodic Watchlist. One dated Pattern Pack remains subordinate to the existing reverse-engineering reuse pipeline. One focused regression protects owner boundaries and required capture fields. Because the permanent Base validator enumerates unittest modules explicitly, the regression is routed through the existing validator with one added test-module entry rather than a new workflow.

**Spec:** `docs/superpowers/specs/2026-08-24-ai-indie-game-reverse-engineering-radar-design.md`

## Global constraints

- `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` remains source-policy owner.
- scheduling remains `EXTERNAL_TO_BASE`.
- `REVERSE_ENGINEERING_REUSE_PIPELINE.md` remains reuse-discovery owner.
- `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md` remains AI-production authority.
- `REUSABLE_MODULE_REGISTRY.md` remains promotion registry.
- no new Skill/Agent, paid dependency, runtime-AI dependency, project gameplay implementation, or Notion mutation.
- separate `PRODUCTION_ASSISTED` from `RUNTIME_GENERATIVE`.
- popularity is discovery evidence, never causal proof by itself.
- Red → partial Green → full Green must be visible in CI.

## Task 1 — TDD ownership/capture regression

**Files**
- Create: `tests/test_ai_indie_game_reverse_engineering_radar.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`

- [x] Add a focused test that fails while Radar and Pattern Pack are absent.
- [x] Discover that the existing Base validator enumerates unittest modules instead of auto-discovering new files.
- [x] Route the new test through the existing validator with one module entry; do not create a second CI workflow.
- [x] Verify actual RED in GitHub Actions: both expected missing-artifact assertions fail while existing neighboring contracts remain green.

## Task 2 — Specialty weekly Radar

**Files**
- Create: `docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md`

- [x] Preserve existing Watchlist/reuse/AI-guide ownership.
- [x] Define weekly cadence, previous-scan comparison, AI-use lanes, source/evidence classes, release-state separation, success/failure sampling, and candidate packet.
- [x] Define Existing Solution First and project no-auto-adoption boundary.
- [x] Verify partial Green in CI: Radar contract test passes while Pattern Pack test remains intentionally red.

## Task 3 — First evidence-derived Pattern Pack

**Files**
- Create: `docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md`

Cases:
- Slotbound
- Ashen Crown
- Express 404
- Infinite Arcana
- Vapor World: Over the Mind
- Grimoire of Hecate: Tower of Starlight
- FARLUME: Into the Silent Dark

Reusable production candidates:
- `HUMAN_DIRECTED_AI_BUILD_LOOP`
- `SILENT_OMISSION_GATE`
- `CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET`
- `BREADTH_AFTER_CORE_IDENTITY_LOCK`
- `PLAYER_FEEDBACK_REBUILD_LOOP`
- `AI_VISIBLE_OUTPUT_QUALITY_GATE`

Reusable gameplay candidate:
- `RNG_AGENCY_AND_RECOVERY`

- [x] Record official product facts separately from developer self-report/player report/secondary reporting/inference.
- [x] Record popularity signal dates and explicit causal ceilings.
- [x] Include strong, weak, upcoming, and failure/mixed evidence rather than only favorable cases.
- [x] Route reusable candidates to existing Base owners before proposing anything new.
- [x] Add 10-project fit hypotheses with `PROJECT_ADOPTION_NOT_RUN`.
- [x] Add Implementation Reality Gate and 5-pass adversarial review.
- [ ] Verify full Green on the Pattern Pack commit and resolve any current-head failures.

## Task 4 — Current-head PR closure

**PR:** `#631`

- [ ] Compare branch against current `main` and active independent PR files.
- [ ] Confirm only spec, plan, test, Radar, Pattern Pack, and one existing-CI test routing line changed.
- [ ] Recheck evidence claims: upcoming games are not called successes; self-reported metrics are labeled; popularity is not treated as causality.
- [ ] Run/observe permanent Base contract, evidence-knowledge, project-operating, and dependency checks on current head.
- [ ] Perform final adversarial review against the current diff.
- [ ] Update PR body from RED-phase description to final verified scope.
- [ ] Merge only under current Base merge policy after current-head verification is green and no active-PR conflict exists.

## Task 5 — External weekly scheduler handoff

- [ ] After the Radar exists on merged `main`, update the already-approved weekly automation prompt to explicitly consume `AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md`.
- [ ] Require every run to compare against the prior scan and route candidate promotion through existing Base owners.
- [ ] Keep scheduler authority external; Base must not claim task execution.

## Completion claims allowed

After all tasks close, it is valid to claim the weekly research/capture path and its Base contracts are installed and verified. It is **not** valid to claim any project adopted a gameplay candidate, any runtime AI system exists, or any benchmark pattern improves sales/retention until project-level evidence proves it.
