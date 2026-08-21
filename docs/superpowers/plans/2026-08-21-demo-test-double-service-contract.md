# Demo/Test-Double Service Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Absorb the reusable demo/test-double patterns from the WE-AR ERP study into Base without adding an ERP, new active Skill, duplicate capability registry, or mandatory project economics system.

**Architecture:** Extend the existing `GAME_BACKEND_CLOUD_RUN` guide and project-owned backend service contract. Consumer code keeps one service interface, while real and fake adapters implement the same operation contract; fake data is deterministic, resettable, synthetic, fail-closed for unknown operations, and capped at simulated evidence until real-provider parity/runtime checks run.

**Tech Stack:** Markdown contracts, Python `unittest` regression tests, existing Base documentation governance.

**Spec:** Approved recommendation from the 2026-08-21 WE-AR ERP reuse spike; existing owners are `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`, `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`, and `tests/test_cloud_run_game_backend_capability.py`.

## Global Constraints

- Do not add a new active Skill or shared project route.
- Do not add an ERP, HTML/local dashboard, CRM/HR/finance subsystem, or mandatory P&L workflow.
- Do not add a second capability/module registry; reuse existing Base routing and adapter authorities.
- Unknown fake operations must fail closed, not silently return success.
- Fake/demo execution may validate flow and consumer behavior but may not satisfy real provider runtime, load, failure, cost, security, or production-readiness evidence.
- Public/demo fixtures must use synthetic data and exclude real secrets and private records.
- Preserve current Cloud Run conditional-fit decisions and project-owned service contract lifecycle.

---

### Task 1: Add regression expectations for the approved contract

**Files:**
- Modify: `tests/test_cloud_run_game_backend_capability.py`

**Interfaces:**
- Consumes: existing Cloud Run guide and project backend contract.
- Produces: regression expectations for `ONE_CONSUMER_INTERFACE`, `REAL_ADAPTER`, `FAKE_ADAPTER`, `FAIL_CLOSED_UNKNOWN_OPERATION`, `CONTRACT_PARITY_REQUIRED`, `DETERMINISTIC_FIXTURE`, `RESETTABLE_STATE`, `SYNTHETIC_DATA_ONLY`, `PUBLIC_DEMO_SANITIZATION`, and `SIMULATED_ONLY`.

- [ ] **Step 1: Write tests that require interface parity and fail-closed fake behavior.**
- [ ] **Step 2: Write tests that require deterministic/resettable synthetic fixtures and public-demo sanitization.**
- [ ] **Step 3: Confirm the existing no-new-Skill/no-shared-route test remains applicable.**
- [ ] **Step 4: Run the targeted test and confirm the new assertions fail before contract implementation.**

### Task 2: Extend the existing backend guide and project contract

**Files:**
- Modify: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
- Modify: `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`

**Interfaces:**
- Consumes: the existing API operation contract, provider/runtime evidence lifecycle, and project-owned backend contract.
- Produces: one-interface real/fake adapter contract, contract parity requirements, deterministic synthetic fixtures, reset contract, public-demo sanitization, and simulated-evidence ceiling.

- [ ] **Step 1: Add a guide section defining one consumer interface with `REAL_ADAPTER` and `FAKE_ADAPTER`.**
- [ ] **Step 2: Require exact operation/request/response/error semantics parity and `FAIL_CLOSED_UNKNOWN_OPERATION`.**
- [ ] **Step 3: Add deterministic/resettable synthetic fixture and public-demo sanitization rules.**
- [ ] **Step 4: State that fake execution remains `SIMULATED_ONLY` until real-provider contract/runtime evidence exists.**
- [ ] **Step 5: Add corresponding project-owned fields to `GAME_BACKEND_SERVICE_CONTRACT.md`.**

### Task 3: Verify, review, and integrate

**Files:**
- Verify: `tests/test_cloud_run_game_backend_capability.py`
- Review: changed files only, then same-goal open/recent PRs read-only.

**Interfaces:**
- Consumes: Tasks 1-2 changes.
- Produces: validated PR and post-merge main readback.

- [ ] **Step 1: Run targeted Cloud Run capability regression.**
- [ ] **Step 2: Run repository CI available on the PR and inspect failures rather than assuming pass.**
- [ ] **Step 3: Perform adversarial review for duplicate responsibility, fail-open behavior, evidence laundering, secret/private-data leakage, and unnecessary project-wide obligations.**
- [ ] **Step 4: Merge only after required checks pass and the approved scope remains minimal.**
- [ ] **Step 5: Fetch the new exact `main` SHA and re-read the changed contracts plus same-goal PR state.**
