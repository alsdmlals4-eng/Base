# Work Five-Phase Vertical Slice — Implementation Plan

> **Approval reference:** 2026-08-27 user instruction to verify and correct the Work workflow into five explicit stages, co-design core planning with Grill Me and benchmarking, preserve current Base/project canon, and define exactly where Vertical Slice completion ends.

## Goal

Add a thin project-neutral five-phase interface without duplicating current Base owners or mass-renaming project-native Task/Decision/PLAN/BUILD/REVIEW states.

```text
1. PHASE_1_PLANNING_CO_DESIGN
2. PHASE_2_PREPRODUCTION_REVIEW
3. PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
4. PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
5. PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```

## Current authority

- completed main at implementation start: `ab6375ea5e5c08048a8b4cba57b9f3c51c5b2518`
- approved proposal: BCP-2026-040 / PR #740
- preserved owners:
  - `WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
  - `WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md`
  - `WORK_PROJECT_START_CANON_CHECKLIST.md`
  - `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
  - `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
  - `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
  - `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
  - `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
  - `skills/designing-vertical-slices/SKILL.md`

## Actual audit finding

Current Base capabilities are present but distributed:

- startup canon and core-fun/system/SWOT/work-order correction exists;
- Grill Me owns core product decisions;
- benchmark, reuse and three alternatives exist;
- minimum-transition profile compresses planning, review and asset/input production into Stage A;
- Codex and final Work review exist;
- automated readiness and user-validation pending exist;
- no project-neutral `USER_VALIDATED_VERTICAL_SLICE` terminal state or phase-reopen map exists.

Representative project canons confirm the need for mapping rather than migration:

- projects use `PLAN/BUILD/REVIEW`, Task/Decision gates, package candidates and Human evidence contracts;
- GRIMOIRE explicitly distinguishes automated-ready from user-validation-pending;
- Switchy and Tetris separate package/runtime evidence from physical/Human evidence;
- non-game Coc-Fiction must keep Godot fields `NOT_APPLICABLE`.

## Implementation scope

### Task 1 — RED contract

Add `tests/test_work_five_phase_vertical_slice_contract.py` first.

The test requires:

- exact five phase names and order;
- Phase 1 core co-design with current canon, Grill Me, benchmark and three alternatives;
- routine approval not equal to core-product approval;
- Phase 2 preproduction review before serial element production or Codex;
- Phase 3 Work-owned Visual/Audio/UI/Data/VFX packet and local Visual routing;
- Phase 4 one Codex implementation window, machine QA, Work final implementation review, CI/merge/build;
- Phase 4 automated-ready not equal to final Vertical Slice completion;
- Phase 5 exact user build play and explicit outcome statuses;
- bounded reopen mapping to phases 1–4;
- project-native state mapping without rename/migration;
- non-game domain adaptation;
- current owners preserved and routed from Router/Starter.

Verify expected failure while the new owner/case/routing is absent.

### Task 2 — minimal GREEN owner

Create:

- `templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md`
- `docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md`

Update only:

- `templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md`

Do not edit the existing detailed minimum-transition profile. The new owner maps and composes it.

### Task 3 — project-canon optimization boundary

Add `FIVE_PHASE_PROJECT_MAPPING` and `PROJECT_PHASE_DRIFT_CORRECTION_REQUIRED` to the new contract.

At each project Work start:

```text
project-native states
→ map to phases 1–5
→ detect ambiguity/drift
→ correct current status/next gate in the project’s actual owner when safe
→ preserve historical Task/Decision names
```

Do not mass-migrate Notion IA or rename all project states.

### Task 4 — exact verification

Run/observe:

- Python syntax;
- focused unittest;
- full core regression;
- docs/publication/governance checks;
- exact current required checks;
- changed-file/open-PR concurrency audit;
- unresolved thread/review/conflict check;
- minimum five full-scope adversarial loops.

### Task 5 — closeout

- update implementation PR with RED/GREEN exact heads;
- squash merge with expected head;
- read back new main and all routed files;
- verify post-merge workflows;
- generate one final downloadable Work instruction file from merged current truth;
- recalculate required work.

## Phase semantics

### Phase 1

Core product meaning is co-designed with the user. Existing confirmed decisions are reused. Only unresolved material choices use Grill Me. Routine delegation does not authorize new core meaning.

### Phase 2

Preproduction review only. It validates the Phase 1 contract and implementation/production feasibility. Codex result review belongs to Phase 4.

### Phase 3

Work finishes all implementation inputs that it can own before one Codex window.

### Phase 4

Codex implements; machine QA and Work final implementation evidence review close the automated package. Output is runnable build readiness, not Human/Player completion.

### Phase 5

The user plays the exact build. Feedback routes to the earliest affected phase. Only actual user validation can produce `USER_VALIDATED_VERTICAL_SLICE`.

## Vertical Slice completion

```text
AUTOMATED_VERTICAL_SLICE_READY
!= USER_VALIDATED_VERTICAL_SLICE
!= WHOLE_GAME_COMPLETE
!= RELEASE_READY
```

Phase 4 requires representative build, integrated shipping-intent inputs, machine evidence, exact identity, safe merge/readback and downloadable launch route.

Phase 5 additionally requires actual user play, representative action→choice→result→feedback completion, usability/fun-direction findings and Canonical Reflection After Play.

## Protected scope

- no Skill Registry change;
- no CI workflow/ruleset change;
- no engine/dependency/provider change;
- no Project canon mass migration;
- no Notion IA remigration;
- no project-specific Task/Decision/SHA/path/style in active generic policy;
- no Human/Player evidence promotion;
- no direct main/force/admin bypass;
- no new cost or public release.

## Rollback

Revert the implementation squash commit and remove the new owner links from Router/Starter. Existing startup checklist, Grill Me, minimum-transition, local Visual, evidence identity and project-native states remain intact.
