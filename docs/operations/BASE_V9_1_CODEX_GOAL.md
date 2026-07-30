/goal Implement GitHub Issue #71 exactly as specified.

Read first: `AGENTS.md`, `START_HERE.md`, `docs/OPERATING_MODEL.md`, `docs/operations/BASE_V9_RELEASE_CONTRACT.md`, `docs/operations/BASE_V9_SYSTEM_MAP.md`, `skills/SKILL_REGISTRY.json`, `docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md`, and the v9.1 implementation plan.

Environment: Godot project-governance Base repository; Python 3.12; Windows and Linux CI consumers; no project product code is in scope. The released v9.0 artifacts and their history remain unchanged.

Goal: add the compatible Base v9.1 operating-system contract defined by GitHub Issue #71. The canonical per-project authority is `skills/PROJECT_BASE_ADAPTER.json`; every snapshot, health/dashboard view, router, and one-cycle legacy adapter is derived or bounded by it.

User-visible behavior: project maintainers and AI agents can identify the exact Base release/evidence pins, resolve shared versus local Skill routes deterministically, see separate operating/product-evidence maturity, and receive fail-closed errors for stale, mismatched, copied, manually edited, or protected-path-violating state.

In scope: schemas, templates, migration/generation/cross-repository validators, generated-view contracts, focused shared-Skill guidance, Base system/maturity/dashboard documentation, Godot UX/UI and GitHub/AI governance, Windows PDF command safety, CI supply-chain hardening, tests, maps, changelog, and learning records.

Out of scope: project game code, scenes, resources, assets, balance, player-facing rules, automatic project migration, release binary production, automatic merge, runtime/device/human/accessibility PASS claims, and rewriting v9.0 history.

Interfaces: canonical adapter sections are `base_release`, `project`, `routing`, `skill_registry`, `shared_overrides`, `gdd_sheet`, `protected_paths`, `validators`, and `compatibility`. The generated Skill snapshot exposes `base_routes`, `project_routes`, `inactive_routes`, `aliases`, plus source Registry path/hash. When explicitly requested and backed by preserved legacy inputs, compatibility views may include `BASE_V9_ADAPTER.json`, `PROJECT_BASE_SKILL_ADAPTER.json`, and `PROJECT_PATH_ADAPTER.json`, marked `GENERATED_COMPATIBILITY_VIEW` for one cycle; missing legacy inputs are omitted rather than synthesized.

Constraints: use RED/GREEN TDD for code and Skill changes; shared Skill bodies stay in Base; project-local routes win over same-name shared routes; pin/hash mismatches are ignored only by refusing execution; generated outputs are deterministic and support `--check`; OM and PE axes are never averaged; critical gates remain separate; official Actions use full commit SHAs and least permissions; binary attestation remains `DEFERRED_UNTIL_RELEASE_ARTIFACT`.

Acceptance: validate pin ancestry, hashes, paths, duplicate IDs, alias cycles, shared-body duplication, protected-path changes, generated-view manual edits, stale/mismatched pins, route precedence, and compatibility outputs. Run focused tests, full `python -m unittest discover -s tests -v`, all generator checks, `git diff --check`, and `git fsck --strict`.

Manual Godot validation: report `NOT_RUN`; provide only the contract/checklist for Godot 4.7, native `Control`/`Container`/`Theme`, focus/accessibility, long Korean text, and 1280x720/1920x1080. Do not claim runtime, device, accessibility, or human evidence.

Documentation: update the v9.1 release/system/maturity/dashboard contracts, Documentation Map, changelog, UI reference policy, relevant Skill references, Registry hashes/snapshots, and Skill learning records.

Completion report: changed files; intent mapping; acceptance status; exact test commands/results; generator/idempotence evidence; protected-path result; P0/P1 findings; runtime/device/human/accessibility NOT_RUN gaps; local commit SHA; and confirmation that nothing was pushed or merged.
