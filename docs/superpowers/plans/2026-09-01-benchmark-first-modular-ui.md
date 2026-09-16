# Benchmark-First Modular UI Production Implementation Plan

> Execution: continue the explicitly approved current task with TDD and exact-head review; pre-existing PRs remain read-only.

**Goal:** make external comparison, modular image assembly and complete player-surface planning an executable path reached from Base and project adapters.
**Architecture:** extend the existing UI Skill reference path, not a new Skill or game framework. A read-only standard-library Python checker validates declared projections; current game/data/asset/evidence owners remain authoritative.
**Tech Stack:** repository Markdown, Python 3 standard library, existing GitHub checks.
**Spec:** `docs/knowledge/game-development/BENCHMARK_FIRST_MODULAR_UI_PRODUCTION.md` plus the current user's explicit approval and external-first/modular-parts refinement.

## Constraints

- External game/public implementation comparison precedes project-derived design filtering.
- Preserve project core, adopted contracts, fixed engines and approved assets.
- No product GDScript/Scene mutation, new paid dependency, Registry/released-lock edit or other-workstream takeover.
- Structural tests do not verify real texture pixels, canonical denominator completeness, authenticity of approval, runtime, Human or release.
- Current Base baseline: `32f4dd5ba6042dc34611e2c8912f300b90491e0a`.

## Task 1 — read-only structural checker

Files: `tools/validate_player_surface_plan.py`, `tests/test_player_surface_plan.py`.
Interface: `validate_packet(packet, gate='plan') -> list[str]`; CLI `--packet <file> --gate plan|handoff`.

1. Execute negative fixtures for missing required routes, return traps, malformed values and nine-slice geometry.
2. Add independent-part/composition fixtures: missing module/slot, mismatched style family, baked live text, missing layout approval, unused art and unreviewed part.
3. Run `python -m unittest discover -s tests -p 'test_player_surface_plan.py' -v`; record RED before changing the checker.
4. Implement bounded, no-write validation; repeat the same command until GREEN.
5. Mutation and whole-file review must verify a clean result remains structure-only.

## Task 2 — attach the approved method to active routing

Files: `AGENTS.md`, existing `references/project-adapter-contract.md`, `docs/knowledge/game-development/BENCHMARK_FIRST_MODULAR_UI_PRODUCTION.md`, `tests/test_benchmark_first_modular_production_contract.py`.

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

## Remote integration correction

The exact-head Actions run `33418832589` executed 2,443 core tests and 485 contract tests. Each had the same one failure: newly packaged reference/script artifacts were not directly linked from the protected UI `SKILL.md`. Actual downloaded diagnostic artifacts, not the earlier truncated log interpretation, establish this cause.

Reproduced the package-discovery failure in a focused regression. Retain the existing package rule and protected PR #713 boundary by moving only current-task new artifacts to the normal shared `docs/knowledge/game-development/` and `tools/` owners, updating both root and the already discoverable project-adapter reference. No pre-existing file, test or gate is deleted or weakened. The final-line formatting hypothesis was disproved; no formatting validator change is made.

## 2026-09-01 approved continuation — review correction

The user's latest `맞아 진행해` continues PR #803. Fresh readback still has Base main `32f4dd5ba6042dc34611e2c8912f300b90491e0a` and task HEAD `9f426d129d5a8f2e7080f2d846ac6e163fe1d3bc`. No prior local 84-test payload is present in this executor; that earlier report is not reused as present verification. Restore exact remote source bytes, compare Git blob hashes and execute new evidence instead.

Scope remains the seven-file PR. This continuation changes only the existing checker, its tests, this plan, and §12.1 of the guide; root route, project adapter, registry, Skill body and other workstreams are preserved. PR #804 independently touches the same project-adapter path and similar topic; it is read-only and is not absorbed, closed or merged by this continuation. Do not claim fleet adoption while Base integration is unfinished.

### Verified review findings and minimal corrections

| Inline review ID | Reproduced issue | Correction |
|---|---|---|
| 3896830617 | Required action can lead to an optional return trap | Check required action targets against return/exit reachability |
| 3896830623 | Honest OVERLAY surface is rejected | Accept OVERLAY without forcing a scene or modal |
| 3896830631 | Declared loading/error states have no expression mapping | Resolve surface state_bindings through family target/state/method |
| 3896830636 | Local SOURCE_CODE is counted as external | Explicit origin, HTTP(S) locator and normalized repository identity |
| 3896830639 | FRAME role/kind can bypass frame geometry | Require a contracted FRAME module/family relationship |
| 3896830644 | Documented lifecycle stages are rejected | Full lifecycle plus explicit approval locators; preserve candidate alias |
| 3896830648 | Surrogate in diagnostic crashes stdout | ASCII-escaped structured JSON output |
| 3896977426 | Two incomplete compositions masquerade as one complete assembly | Per-composition membership, never a surface-wide union |

The original flattening exception fixture was incorrectly a FRAME family. It now uses an ILLUSTRATION family, while separate regressions reject disguising an icon or unconstrained frame. Other original test methods are retained, and fixture metadata now explicitly supplies the state/origin/approval contract.

### Execution evidence from this continuation

- Exact original checker blob: `e83f59769eaad6b3be4427856f4225186fc40dc4`; original tests: `eafbbe2ec3d0196c33b80ebdcc9b5583d8385835`.
- Baseline run: 58 checker tests, OK.
- Review RED: 79 tests, 24 failed assertions/subtests, no unhandled test errors; then 79 tests, OK after the eight finding corrections.
- Origin-hardening RED: 81 tests, 4 failed assertions/subtests for nonpublic/control-character URLs and case-insensitive .GIT self-reference; then 81 tests, OK.
- Test command: `python -m unittest discover -s tests -p test_player_surface_plan.py -v` in an isolated exact-blob snapshot. This is not a full repository checkout or a Godot runtime run.
- Python JSON primary reference rechecked: https://docs.python.org/3/library/json.html . `ensure_ascii` and decoder hooks support bounded, structured output; no third-party dependency was added.
- Current-head remote full CI, independent review, unresolved-thread handling, normal expected-head merge and postmerge readback remain distinct gates. Historical CI on 9f426d1 is not evidence for changed bytes.

### Reusable lessons

Check relationships between records, not just valid individual records: action → destination recovery, surface state → family method, frame role → geometry owner, family → one complete composition, lifecycle → approval locator. Keep method documents and executable interchange rules aligned. Preserve exact remote blob identities when normal checkout is blocked, and never confuse a partial local test suite with full repository or runtime verification.
