# Base v9 Final Release Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release Base v9.0.0 from Base-only evidence while keeping all five project adoptions as a separate post-release wave.

**Architecture:** The canonical version document defines the release boundary. The artifact generator derives the lock and all machine-readable release state from that source, and focused tests prevent project-adoption status from blocking the Base release. The project adoption work order remains an explicit non-authorizing template.

**Tech Stack:** Markdown, JSON, Python standard library, `unittest`, GitHub Actions YAML.

## Global Constraints

- Do not alter any of the five project repositories or Google Sheets.
- Preserve `USER_FACING_GDD_WORKSPACE`, `BASE_EXCLUDED`, and `PROPOSED_SHEET_CHANGE` boundaries.
- Base v9.0.0 requires Base-only evidence; project adoption is `POST_RELEASE_PROJECT_ADOPTION_WAVE`.
- Generated artifacts remain deterministic and Registry-derived.

---

### Task 1: Prove the revised release boundary is not yet implemented

**Files:**
- Modify: `tests/test_v9_machine_contracts.py`
- Test: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: `docs/BASE_RULES_VERSION.md`, `docs/operations/BASE_V9_RELEASE_CONTRACT.md`, `base.lock.json`
- Produces: a regression assertion for `v9.0.0` and `POST_RELEASE_PROJECT_ADOPTION_WAVE`

- [x] **Step 1: Write the failing test**

Require the canonical version document, release contract, and generated lock to identify `v9.0.0` as the release line and `POST_RELEASE_PROJECT_ADOPTION_WAVE` as the separate project-adoption state.

- [x] **Step 2: Run the focused test to verify RED**

Run: `python -m unittest tests.test_v9_machine_contracts.V9MachineContractTests.test_base_version_and_release_contract_keep_rc_and_final_distinct -v`

Observed: failure because the pre-change contract did not contain the final-release state.

### Task 2: Implement the Base-only final-release contract

**Files:**
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `docs/operations/BASE_V9_RELEASE_CONTRACT.md`
- Modify: `tools/build_base_v9_artifacts.py`
- Modify: `docs/operations/BASE_V9_RELEASE_DESIGN.md`
- Modify: `docs/operations/BASE_V9_IMPLEMENTATION_PLAN.md`
- Modify: `docs/operations/BASE_V9_MIGRATION_MAP.md`
- Modify: `docs/operations/BASE_V9_INTEGRITY_AUDIT.md`
- Modify: `docs/operations/BASE_V9_ADVERSARIAL_REVIEW_REPORT.md`
- Modify: `docs/CHANGELOG.md`
- Generated: `base.lock.json`, `docs/operations/BASE_V9_DECISION_REGISTRY.json`, `docs/operations/GITHUB_OBJECT_LEDGER.json`, `docs/operations/ADVERSARIAL_REVIEW_MANIFEST.json`

**Interfaces:**
- Consumes: the revised release test
- Produces: `release_line: v9.0.0`, a final Base release state, and `POST_RELEASE_PROJECT_ADOPTION_WAVE`

- [x] **Step 1: Set the canonical Base release line**

Replace the RC-only release status with `v9.0.0`, while stating that GitHub Actions evidence is still a merge gate rather than a project-adoption gate.

- [x] **Step 2: Separate post-release adoption**

Replace `WAVE_2_HOLD` as a final-release blocker with `POST_RELEASE_PROJECT_ADOPTION_WAVE`, retaining the five-project prerequisite list and no-write rule.

- [x] **Step 3: Derive artifacts from the new source**

Update the generator constants and regenerate artifacts with `python tools/build_base_v9_artifacts.py --write`.

- [x] **Step 4: Run the focused test to verify GREEN**

Run the Task 1 test and confirm it passes.

### Task 3: Verify the final Base contract and preserve non-project scope

**Files:**
- Modify: `tests/test_v9_registry_generation.py`
- Modify: `tests/test_v9_governance_documents.py`
- Modify: `templates/prompts/BASE_V9_COMMON_PROJECT_ADOPTION_WORK_ORDER.md`
- Test: `tests/test_v9_machine_contracts.py`, `tests/test_v9_registry_generation.py`, `tests/test_v9_governance_documents.py`

**Interfaces:**
- Consumes: canonical release line, generated lock, held project work order
- Produces: regression coverage for final Base release and held project adoption

- [x] **Step 1: Add focused assertions**

Assert that the Base lock is final-release scoped and that the project work order is a post-release, explicit-resumption instruction without repository or Sheet writes.

- [x] **Step 2: Run the focused v9 suite**

Run: `python -m unittest tests.test_v9_machine_contracts tests.test_v9_registry_generation tests.test_v9_governance_documents -v`

Expected: all focused tests pass.

### Task 4: Run full verification and record the handoff boundary

**Files:**
- Modify: generated artifacts only if the generator changes them

- [x] **Step 1: Confirm deterministic generation**

Run the generator twice, then `python tools/build_base_v9_artifacts.py --check`; no artifact drift is allowed.

- [x] **Step 2: Run complete validation**

Run the entire `unittest` suite, the Base v9 integrity checker, the skill coverage checker, plugin manifest validation, and `git diff --check`.

- [ ] **Step 3: Commit the contract correction**

Commit only Base release-contract, generated-artifact, and test changes. Do not include a local virtual environment.
