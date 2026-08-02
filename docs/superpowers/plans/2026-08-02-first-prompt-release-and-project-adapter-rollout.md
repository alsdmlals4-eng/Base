# First-Prompt Release and Project Adapter Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge the approved first-prompt intake contract, release it as Base v9.4.3 with trusted evidence, and update six project adapters to the exact released payload/evidence pair without copying Base Skill bodies.

**Architecture:** Base remains the single owner of `managing-project-intake-and-work-contract`. The release follows the existing two-stage compatibility process: merge the implementation payload, create trusted release evidence with a pending lock, then finalize the lock as `BASE_RELEASED`. Each project receives an isolated adapter-only PR that changes its existing Base release pin and first-prompt override/validation surfaces while preserving project canon, product files, and Google Sheets state.

**Tech Stack:** GitHub pull requests and Actions, JSON release locks and schemas, Python `unittest` contract tests, project `skills/PROJECT_BASE_ADAPTER.json` files, existing project validators.

## Global Constraints

- Release line: `v9.4.3`.
- Predecessor: released `v9.4.2` from `base-v9.4.2.lock.json`.
- Source implementation PR: Base PR `#143`.
- Base Registry raw bytes and SHA-256 remain unchanged unless the implementation diff proves otherwise; expected existing SHA-256 is `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- Do not copy `skills/managing-project-intake-and-work-contract/SKILL.md` into projects.
- Do not change project game code, scenes, resources, data, assets, canon, or Google Sheets in the adapter rollout.
- Every merge uses the exact reviewed HEAD and requires zero unresolved review threads, zero P0/P1 findings, successful required checks, and a mergeable latest-main result.
- Runtime, model-behavior, human-comprehension, and real project execution claims remain `NOT_RUN` unless separately executed.

---

### Task 1: Finalize and merge Base PR #143

**Files:**
- Modify: `docs/superpowers/plans/2026-08-02-first-prompt-release-and-project-adapter-rollout.md`
- Existing implementation scope: the files already listed in Base PR #143

**Interfaces:**
- Consumes: Base `main`, PR #143 exact HEAD, required workflow results, review threads.
- Produces: `MERGED_PAYLOAD_SHA`, the Base main commit containing the first-prompt contract.

- [ ] **Step 1: Re-read PR #143 metadata, changed files, diff, review threads, and exact-head workflow runs.**
- [ ] **Step 2: Verify the GitHub test merge result contains both released v9.4.2 planning-first governance and the PR #143 `route → first-prompt → contract → clarify` contract.**
- [ ] **Step 3: Confirm protected paths are absent: `skills/SKILL_REGISTRY.json`, `base-v9.4.2.lock.json`, released evidence, project repositories, and product/runtime files.**
- [ ] **Step 4: Mark PR #143 ready for review when required checks succeed.**
- [ ] **Step 5: Merge PR #143 with squash merge and `expected_head_sha` fixed to the reviewed HEAD. Record the returned merge SHA as `MERGED_PAYLOAD_SHA`.**
- [ ] **Step 6: Re-read Base main and confirm `MERGED_PAYLOAD_SHA` is reachable and the first-prompt reference, intake mode, aliases, tests, and Learning Log are present.**

### Task 2: Prepare Base v9.4.3 trusted evidence

**Files:**
- Create: `base-v9.4.3.lock.json`
- Create: `schemas/base-v9.4.3-lock.schema.json`
- Create: `schemas/base-v9.4.3-evidence.schema.json`
- Create: `docs/operations/BASE_V9_4_3_RELEASE_CONTRACT.md`
- Create: `docs/releases/base-v9.4.3-evidence.json`
- Create or modify: the v9.4.3 release checker following `tools/check_base_v9_4_2_release.py`
- Modify: the canonical compatible-release index used by Base project tooling
- Create: focused v9.4.3 release regression following the v9.4.2 regression
- Modify: existing required workflow so the focused regression and checker execute

**Interfaces:**
- Consumes: `MERGED_PAYLOAD_SHA`, v9.4.2 lock/evidence, unchanged Registry hash, first-prompt implementation paths.
- Produces: a pending v9.4.3 lock and a merged trusted evidence commit `TRUSTED_EVIDENCE_SHA`.

- [ ] **Step 1: Create a release issue declaring source PR #143, predecessor v9.4.2, payload `MERGED_PAYLOAD_SHA`, Registry hash, protected scope, and explicit evidence limits.**
- [ ] **Step 2: Create a release-evidence branch from exact Base main at `MERGED_PAYLOAD_SHA`.**
- [ ] **Step 3: Add a failing focused regression that requires a v9.4.3 pending lock, source PR #143, predecessor v9.4.2, exact payload SHA, unchanged Registry hash, required first-prompt validator paths, and a null evidence pin.**
- [ ] **Step 4: Run the regression through the required Base workflow and confirm RED is caused only by missing v9.4.3 release artifacts.**
- [ ] **Step 5: Implement the pending lock, schemas, evidence record, release contract, fail-closed checker, compatible-release index entry, and workflow integration by adapting the v9.4.2 pattern without modifying v9.4.2 history.**
- [ ] **Step 6: Verify payload ancestry, Registry bytes, predecessor identity, source PR, required paths, evidence limits, and project-adoption prohibition while state is `TRUSTED_EVIDENCE_PENDING`.**
- [ ] **Step 7: Open a release-evidence PR, run all required checks, verify zero unresolved threads and exact-head mergeability, then squash merge with the reviewed head. Record the merge result as `TRUSTED_EVIDENCE_SHA`.**

### Task 3: Finalize Base v9.4.3 release

**Files:**
- Modify: `base-v9.4.3.lock.json`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: the focused v9.4.3 regression from pending to released state
- Modify only if required by existing release tooling: the v9.4.3 evidence record or compatible-release index

**Interfaces:**
- Consumes: `MERGED_PAYLOAD_SHA`, `TRUSTED_EVIDENCE_SHA`, pending v9.4.3 release artifacts.
- Produces: released Base v9.4.3 identity available to project adapters.

- [ ] **Step 1: Create a finalization branch from exact main at `TRUSTED_EVIDENCE_SHA`.**
- [ ] **Step 2: Write a failing final-state regression requiring `BASE_RELEASED`, evidence pin `TRUSTED_EVIDENCE_SHA`, latest compatible line `v9.4.3`, and immutable v9.4.2 history.**
- [ ] **Step 3: Update the v9.4.3 lock to `BASE_RELEASED`, pin `candidate_release_evidence_commit` to `TRUSTED_EVIDENCE_SHA`, and add the v9.4.3 released section to `docs/BASE_RULES_VERSION.md`.**
- [ ] **Step 4: Run focused release, full Base contract/governance, canonical freshness, publication/generation, and required `ci-gate` validation.**
- [ ] **Step 5: Open and merge the finalization PR with exact reviewed HEAD. Record the resulting Base main SHA and re-read the lock and version document.**

### Task 4: Inspect six project adapter contracts

**Files:**
- Read in each project: `skills/PROJECT_BASE_ADAPTER.json`
- Read each project’s Base adoption regression, project operating validator, release compatibility views, and current open PR inventory

**Interfaces:**
- Consumes: released Base v9.4.3 payload/evidence pair.
- Produces: six repository-specific adapter change maps with exact files and validators.

- [ ] **Step 1: Inspect `Ten-Paces-Hidden-Moves`, `Blacksmith`, `omenward`, `urban-legend`, `GRIMOIRE-`, and `Switchy-Express-Cargo-Puzzle` from current main.**
- [ ] **Step 2: Record each adapter’s JSON shape, Base route representation, generated compatibility consumers, validator command form, protected paths, current open PR overlap, and latest main SHA.**
- [ ] **Step 3: Confirm every project already routes `managing-project-intake-and-work-contract` as `BASE_SHARED` and contains no copied Base Skill body.**
- [ ] **Step 4: Define the minimum per-project override for first-prompt adoption: Base contract source, `route → first-prompt → contract → clarify`, direction-anchor reference, `AWAITING_USER_CONFIRMATION` gate, approval reuse, L0 exceptions, and `actual_project_execution: NOT_RUN`.**

### Task 5: Update each project through an isolated Draft PR

**Files for each project:**
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify: existing generated compatibility views only through the project’s established generator or exact canonical-consumer procedure
- Create or modify: one focused adapter regression integrated into an existing required workflow
- Modify only when existing project contracts require it: Base adoption audit or project operating health evidence

**Interfaces:**
- Consumes: released Base v9.4.3 identity and the repository-specific change map.
- Produces: one exact-head validated adapter PR per project.

- [ ] **Step 1: Create a dedicated branch from each project’s latest main; do not build on active planning or product branches.**
- [ ] **Step 2: Add the focused failing regression first. It must require v9.4.3 payload/evidence, unchanged Base Registry hash, active intake route, first-prompt override, no copied Base Skill body, project protected paths, and `actual_project_execution: NOT_RUN`.**
- [ ] **Step 3: Confirm RED is caused by the existing v9.4.2 pin and missing first-prompt adapter metadata.**
- [ ] **Step 4: Update the canonical adapter and established consumers to v9.4.3, preserving each project’s JSON representation and project-specific boundaries.**
- [ ] **Step 5: Run each project’s existing adapter, operating-system, documentation, and applicable Godot/static validators. Runtime and human tests remain `NOT_RUN` unless already mandatory and executable.**
- [ ] **Step 6: Open one Draft PR per project with exact payload/evidence pins, changed-file inventory, protected scope, RED→GREEN evidence, open-PR overlap analysis, and rollback instructions.**
- [ ] **Step 7: Verify exact-head checks, mergeability, zero unresolved threads, and no product/canon/Sheet changes. Mark ready and merge only when each repository’s automatic merge policy authorizes it.**

### Task 6: Cross-repository release readback

**Files:**
- No new product files.
- Read: Base v9.4.3 lock/version and all six merged project adapters.

**Interfaces:**
- Consumes: Base and project merged-main SHAs.
- Produces: a final cross-repository evidence report.

- [ ] **Step 1: Re-read Base main and verify v9.4.3 is the latest released compatible line with exact payload/evidence pair.**
- [ ] **Step 2: Re-read all six project main branches and verify the same Base v9.4.3 payload, evidence, Registry hash, first-prompt override, and adapter-only policy.**
- [ ] **Step 3: Confirm no project contains `skills/managing-project-intake-and-work-contract/SKILL.md` and no project product/canon/Sheet path changed in the adapter PR.**
- [ ] **Step 4: Report Base merge/release PRs, six project PRs, exact commits, validation results, unresolved-thread counts, evidence limits, and any project left unmerged or blocked.**
