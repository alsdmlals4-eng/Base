# Base v9.1 Operating Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:writing-skills while implementing this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release a v9.0-compatible Base v9.1 project operating contract with deterministic project adapters, generated views, fail-closed validation, and hardened CI/publication tooling.

**Architecture:** Keep the released v9.0 artifacts immutable and add a v9.1 contract layer. A canonical per-project `skills/PROJECT_BASE_ADAPTER.json` drives a generated Skill snapshot, compatibility views, operating-health state, and an HTML dashboard; one Python core provides deterministic generation and cross-repository validation, with small CLI wrappers for migration, generation, and checking.

**Tech Stack:** Python 3.12 standard library, JSON Schema 2020-12, unittest, Git, deterministic JSON/HTML, GitHub Actions, Markdown Skill packages.

## Global Constraints

- Implement GitHub Issue #71 only; do not change product code, scenes, data, assets, balance, or player-facing rules.
- Preserve v9.0 release history; v9.1 uses separate `release_commit` and `release_evidence_commit` pins.
- Shared Skill bodies remain in Base. Projects store routes, adapters, overrides, and genuinely project-specific Skills only.
- Generated files are byte-deterministic, marked generated, and support `--check` without mutation.
- Operating maturity (`OM-L0`..`OM-L5`) and product evidence (`PE-0`..`PE-5`) remain separate and are never averaged; critical gates remain explicit.
- Runtime, device, accessibility, and human validation must remain `NOT_RUN` unless evidence exists.
- Binary attestation remains `DEFERRED_UNTIL_RELEASE_ARTIFACT`.

---

### Task 1: Freeze the v9.1 machine contracts

**Files:**
- Create: `tests/test_v9_1_project_operating_contract.py`
- Create: `schemas/project-base-adapter-v1.schema.json`
- Create: `schemas/project-skill-snapshot-v1.schema.json`
- Create: `schemas/project-operating-health-v1.schema.json`
- Create: `templates/project-operations/PROJECT_BASE_ADAPTER.json`

- [ ] Write schema/template tests for every required top-level contract and rejection case.
- [ ] Run the focused suite and confirm RED because the v9.1 files do not exist.
- [ ] Add the minimal schemas and canonical template.
- [ ] Run the focused suite and confirm GREEN.

### Task 2: Build deterministic migration, generation, and validation

**Files:**
- Create: `tools/project_operating_contract.py`
- Create: `tools/migrate_project_operating_contract.py`
- Create: `tools/build_project_operating_artifacts.py`
- Create: `tools/check_project_operating_contract.py`
- Modify: `tests/test_v9_1_project_operating_contract.py`

- [ ] Add failing fixture tests for route precedence, aliases/cycles, registry hashes, pin ancestry, path existence, duplicate IDs, protected paths, copied shared bodies, stale pins, mismatched pins, and generated-file drift.
- [ ] Implement canonical loading, migration, deterministic generation, and fail-closed validation.
- [ ] Add `--check` paths and prove a second generation is byte-identical.

### Task 3: Add project views, health, dashboard, and compatibility outputs

**Files:**
- Create: `templates/project-operations/PROJECT_OPERATING_HEALTH.json`
- Create: `templates/project-operations/.agents/skills/base-project-router/SKILL.md`
- Create: `docs/operations/BASE_V9_1_DASHBOARD_CONTRACT.md`
- Modify: `tools/project_operating_contract.py`
- Modify: `tests/test_v9_1_project_operating_contract.py`

- [ ] Add failing tests for snapshot field normalization, source hashes, compatibility markers, health axes/gates, and deterministic accessible HTML.
- [ ] Generate `PROJECT_SKILL_SNAPSHOT.json`, `PROJECT_OPERATING_DASHBOARD.html`, `BASE_V9_ADAPTER.json`, `PROJECT_BASE_SKILL_ADAPTER.json`, and `PROJECT_PATH_ADAPTER.json` from the canonical adapter.
- [ ] Verify manual edits fail `--check`.

### Task 4: Harden shared Skills and governance through pressure tests

**Files:**
- Create: `tests/test_v9_1_skill_pressure_contracts.py`
- Create: `skills/managing-game-project-operating-system/references/project-adapter-and-routing-contract.md`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`

- [ ] Record RED baseline outcomes for body copying, stale-pin execution, local/shared same-name precedence, and mismatched-pin ignoring.
- [ ] Keep Skill bodies focused; move detailed operating contracts to references.
- [ ] Re-run the same scenarios and verify the required fail-closed decisions.

### Task 5: Fix Windows PDF execution and harden CI supply chain

**Files:**
- Modify: `tests/test_design_document_generation.py`
- Modify: `tools/publication_v3.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`
- Create: `.github/workflows/dependency-review.yml`
- Modify: `tests/test_v9_1_project_operating_contract.py`

- [ ] Add a failing unit test that requires `.exe` direct invocation and `.cmd`/`.bat` invocation through an explicit safe command array without `shell=True`.
- [ ] Implement the safe PDF command builder and use it in all PDF rendering paths.
- [ ] Add least-privilege workflow permissions, pin official actions to full commit SHAs, and add dependency review for dependency-changing pull requests.
- [ ] Keep binary attestation explicitly deferred until a release artifact exists.

### Task 6: Publish v9.1 governance and verify the release candidate

**Files:**
- Create: `docs/operations/BASE_V9_1_SYSTEM_MAP.md`
- Create: `docs/operations/BASE_V9_1_MATURITY_MODEL.md`
- Create: `docs/operations/BASE_V9_1_RELEASE_CONTRACT.md`
- Create: `docs/operations/BASE_V9_1_CODEX_GOAL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `docs/knowledge/OPEN_SOURCE_GODOT_UI_REFERENCE_CATALOG.md`
- Modify: `skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md`

- [ ] Document Godot 4.7 native `Control`/`Container`/`Theme`, focus/accessibility, long Korean text, 1280x720 and 1920x1080 validation contracts.
- [ ] Limit Maaack (MIT) and Kenney (CC0) references to patterns/reference cards, never identity or distinctive expression copying.
- [ ] Run focused RED/GREEN evidence, full unittest discovery, every generator `--check`, `git diff --check`, and `git fsck --strict`.
- [ ] Review the complete diff, commit all intentional Base-only changes locally, and report evidence and remaining NOT_RUN gaps.
