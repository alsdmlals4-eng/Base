# Benchmark-First Modular UI Production Implementation Plan

> Execution: continue the explicitly approved current task with TDD and exact-head review; pre-existing PRs remain read-only.

**Goal:** make external comparison, modular image assembly and complete player-surface planning an executable path reached from Base and project adapters.
**Architecture:** extend the existing UI Skill reference path, not a new Skill or game framework. A read-only standard-library Python checker validates declared projections; current game/data/asset/evidence owners remain authoritative.
**Tech Stack:** repository Markdown, Python 3 standard library, existing GitHub checks.
**Spec:** `skills/auditing-and-refining-ui-art/references/benchmark-first-modular-production.md` plus the current user's explicit approval and external-first/modular-parts refinement.

## Constraints

- External game/public implementation comparison precedes project-derived design filtering.
- Preserve project core, adopted contracts, fixed engines and approved assets.
- No product GDScript/Scene mutation, new paid dependency, Registry/released-lock edit or other-workstream takeover.
- Structural tests do not verify real texture pixels, canonical denominator completeness, authenticity of approval, runtime, Human or release.
- Current Base baseline: `32f4dd5ba6042dc34611e2c8912f300b90491e0a`.

## Task 1 — read-only structural checker

Files: `skills/auditing-and-refining-ui-art/scripts/validate_player_surface_plan.py`, `tests/test_player_surface_plan.py`.
Interface: `validate_packet(packet, gate='plan') -> list[str]`; CLI `--packet <file> --gate plan|handoff`.

1. Execute negative fixtures for missing required routes, return traps, malformed values and nine-slice geometry.
2. Add independent-part/composition fixtures: missing module/slot, mismatched style family, baked live text, missing layout approval, unused art and unreviewed part.
3. Run `python -m unittest discover -s tests -p 'test_player_surface_plan.py' -v`; record RED before changing the checker.
4. Implement bounded, no-write validation; repeat the same command until GREEN.
5. Mutation and whole-file review must verify a clean result remains structure-only.

## Task 2 — attach the approved method to active routing

Files: `AGENTS.md`, existing `references/project-adapter-contract.md`, new `references/benchmark-first-modular-production.md`, `tests/test_benchmark_first_modular_production_contract.py`.

1. Run routing tests against unmodified baseline and record failure.
2. Add the one-line always-on route and adapter section; retain existing Skill body and registry unchanged because another open PR owns them.
3. Keep sources, Godot mapping, module families, capture boundaries and copy-free adoption examples in the one referenced method.
4. Run both test files and inspect all retained files together; preserve direct-game-entry and other project exceptions.

## Task 3 — integration and project adoption

1. Compare latest main, current task head, other open PR filenames and required checks.
2. Post this task on an isolated branch/PR; request independent review and correct verified findings.
3. Merge only with exact-head required checks, resolved threads and normal ruleset-compliant merge; read back merged main.
4. Read each project AGENTS and its declared bootstrap/owners before any write. Use the existing project router if unowned; otherwise defer that path and record the overlap.
5. Adopt only the approved workflow/lookup reference; never replace the project's frozen Base contract or game meaning.
6. Record exact per-project readback and explicit runtime-not-run boundaries.

## Verification and rollback

Focused tests use exact source blobs in an isolated snapshot; full local clone is unavailable because container DNS cannot resolve GitHub. The full repository regression is a separate remote CI gate, not a local PASS. Revert only current-task additions/route deltas as one unit; preserve images, source evidence, other PRs and project data.
