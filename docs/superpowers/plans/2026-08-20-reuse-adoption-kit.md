# Reuse Adoption Kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the merged P0 reuse modules safely adoptable across all 10 active projects without duplicating authority or overwriting project-owned files.

**Architecture:** Base owns versioned reference modules plus a stdlib-only adoption tool. Each project gets a small manifest that selects only relevant modules and records a Base source commit. The tool copies only selected Base-owned vendor files, records hashes in a lock file, fails closed on local modifications, and supports a read-only `check` mode. Project runtime/state/art remain project-owned.

**Tech Stack:** Python 3 stdlib, JSON, Godot/GDScript reference modules, GitHub PR workflow, existing P04 Python regression suite.

**Spec:** User-approved chat design on 2026-08-20: `Base Adoption Kit + project manifest + selected vendor sync`.

## Global Constraints

- Do not modify any path owned by an open/draft/ready PR.
- Base PR #556 paths are read-only for this work.
- No new paid service, package dependency, autoload, global singleton, or network dependency.
- Never overwrite a project-modified vendored module unless its hash still matches the adoption lock.
- `check` must be read-only.
- Project manifest may mark modules `enabled`, `planned`, `not_applicable`, or `deferred`.
- Applying a module does not transfer project canon, save-state, art, UI, or gameplay authority to Base.
- Tetris/Switchy/Omenward open PRs remain untouched; Ninja Survival/Blacksmith/Ten Paces gates remain fail-closed.

---

### Task 1: Adoption contract tests

**Files:**
- Modify: `tests/test_p04_reverse_engineering_reuse_pipeline.py`

**Interfaces:**
- Consumes: current P0 Base reference files.
- Produces: executable contract for manifest validation, safe install, drift detection, and 10-project status coverage.

- [ ] Add failing tests requiring `tools/reuse_modules/reuse_adoption.py`, manifest schema/template, and active-project adoption matrix.
- [ ] Assert enabled modules install into an isolated temp project and create `.base-reuse/adoption-lock.json`.
- [ ] Assert `check` detects modified vendor files without changing them.
- [ ] Assert unsupported module IDs/statuses fail closed.
- [ ] Assert all 10 active project keys have an explicit adoption state.

### Task 2: Stdlib-only adoption tool

**Files:**
- Create: `tools/reuse_modules/reuse_adoption.py`
- Create: `templates/reuse-modules/PROJECT_REUSE_ADOPTION_MANIFEST.json`

**Interfaces:**
- `load_manifest(path) -> dict`
- `apply_adoption(base_root, project_root, manifest) -> dict`
- `check_adoption(base_root, project_root, manifest) -> dict`
- lock path: `.base-reuse/adoption-lock.json`

- [ ] Validate manifest version, Base commit field, module IDs, states, source/destination paths.
- [ ] Copy only `enabled` module files.
- [ ] Refuse to overwrite an existing destination unless lock hash equals current file hash.
- [ ] Write deterministic lock metadata after successful apply.
- [ ] Implement read-only drift/missing/source checks.
- [ ] Expose CLI `apply` and `check` with JSON report and nonzero exit on failure.

### Task 3: Active-project adoption matrix

**Files:**
- Create: `docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json`
- Create: `docs/knowledge/game-development/reuse/adoption/README.md`

**Interfaces:**
- One entry per active project with repository, global status, selected P0 modules, blocker/revisit condition.

- [ ] Record `URBAN_LEGEND` as adopted for RM-TOOL-001 based on merged project PR #208.
- [ ] Record Switchy/Omenward/Tetris as deferred for open-PR isolation.
- [ ] Record Ninja Survival, Blacksmith, Ten Paces with their explicit project gates.
- [ ] Mark Coc-Fiction, GRIMOIRE, My Little Boat as first safe manifest/adoption candidates.
- [ ] Keep `not_applicable` explicit instead of installing every module everywhere.

### Task 4: Safe project rollout

**Files:** Project-specific, new branches only where no open PR and project rules allow low-risk sidecar adoption.

- [ ] Coc-Fiction: install validator/adoption manifest only; no Godot-only modules.
- [ ] GRIMOIRE: install validator + semantic UI/symbol helpers as sidecar reference; do not modify FIVE_POINT_STAR runtime authority.
- [ ] My Little Boat: install validator + semantic UI/symbol helpers as sidecar reference; do not add combat/failure systems.
- [ ] For deferred projects, do not modify repository files; preserve exact blocker and revisit trigger in Base/Notion matrix.
- [ ] Verify each created project PR with the repository's own CI; do not merge if project-required checks fail.

### Task 5: Notion human-view sync and final verification

**Files:**
- Update Notion page `Base · 재사용 모듈 라이브러리` after repository evidence exists.

- [ ] Add adoption-state table for all 10 active projects.
- [ ] Distinguish `ADOPTED_AND_VERIFIED`, `READY_TO_ADOPT`, `DEFERRED_OPEN_PR`, `DEFERRED_PHASE_GATE`, `NOT_APPLICABLE`.
- [ ] Run Base required CI on exact head.
- [ ] Recheck current main, open PR isolation, changed paths, and unresolved threads before merge.
- [ ] Merge only under normal repository rules and read back new Base main.
