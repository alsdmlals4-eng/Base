# Base Authority, UI Workflow, and Security Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the active V3/V4 workspace-authority conflict, then safely restore the approved UI workflow and backend authorization guidance as separately verified current-main successor PRs.

**Architecture:** V4 is the only active workspace authority and V3 remains an explicit compatibility/history input. UI planning discovers project-specific screen/action/flow needs from fresh evidence rather than a global menu list. Security guidance records applicable, reproducible authorization evidence without asserting deployment or runtime PASS from a template.

**Tech Stack:** Markdown and JSON contracts, Python `unittest`, existing Base validators, GitHub pull requests and required Actions checks.

**Spec:** `docs/superpowers/specs/2026-09-01-base-authority-ui-security-reconciliation-design.md`

## Global Constraints

- Start every successor from the current completed `origin/main`; source PRs #803, #804, and #809 are read-only evidence sources under the user's explicit absorption approval.
- Do not direct-push, force-push, change Rulesets, or merge a stale PR branch.
- Keep V3 history and compatibility intact while removing its active-default route.
- Every Base/project L1+ task begins with `BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED` and scope-bounded `LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED`; this discovers project-specific direction and safely reduces misleading/stale routing without blanket deletion.
- Use soft-coded variation owners for project/benchmark/platform/presentation/flow values, while recording true fixed security and compatibility boundaries with their owner and migration path.
- Do not introduce fixed project buttons, product data, runtime images, Godot scenes, or unearned runtime/human evidence.
- Every behavior change starts with a focused test that fails for the missing behavior, then receives the smallest passing correction.

---

### Task 1: Reconcile active V4 authority routing

**Files:**
- Modify: `tests/test_repository_first_workspace_contract.py`
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- Modify: active V4 entrypoints identified by the impact map, including `docs/DOCUMENTATION_MAP.md`, `docs/OPERATING_MODEL.md`, project intake/operating-system/design-document Skills, and project bootstrap templates
- Create: `docs/superpowers/specs/2026-09-01-base-authority-ui-security-reconciliation-design.md`
- Create: `docs/superpowers/plans/2026-09-01-base-authority-ui-security-reconciliation.md`

**Interfaces:**
- Consumes: `PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` (`ACTIVE_DEFAULT`, `REPOSITORY_PRIMARY_CANON`, `NO_NEW_NOTION_WRITE_BY_DEFAULT`)
- Produces: one active route to V4 and an explicitly inactive V3 compatibility contract

- [ ] **Step 1: Write the failing authority test**

Add `test_active_entrypoints_do_not_restore_v3_as_the_default_workspace` to assert that V3 has a compatibility-only state and active entrypoints name V4, `REPOSITORY_PRIMARY_CANON`, and no V3-current-default sentence.

- [ ] **Step 2: Run the test to verify RED**

Run: `python -m unittest tests.test_repository_first_workspace_contract.RepositoryFirstWorkspaceContractTests.test_active_entrypoints_do_not_restore_v3_as_the_default_workspace -v`

Expected: failure because the V3 JSON lacks its retired state and one or more active entrypoints still route new work to the V3 contract.

- [ ] **Step 3: Apply the minimum canonical correction**

Add `status: V3_COMPATIBILITY_AND_HISTORY_ONLY` and `active_route_for_new_work: false` to the V3 JSON. Replace only active-default V3 passages with V4 routing and retain any historical/migration wording as explicitly inactive compatibility. Update project templates so a fresh project reads V4 first and Notion only under V4's exception or read-only migration gate.

- [ ] **Step 4: Run focused authority regression tests**

Run: `python -m unittest tests.test_repository_first_workspace_contract tests.test_notion_project_workspace_contract tests.test_gpt_codex_workflow_contract tests.test_project_master_gdd_two_artifact_contract -v`

Expected: all tests pass after V3 compatibility tests are updated to distinguish history from active default.

- [ ] **Step 5: Commit the authority correction**

Run: `git add docs tests skills templates && git commit -m "fix: reconcile repository-first workspace authority"`

### Task 1.5: Fix mandatory benchmark and safe context/configuration hygiene into the work contract

**Files:**
- Modify: `AGENTS.md`, `skills/managing-project-intake-and-work-contract/SKILL.md`, `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`, `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- Modify: `tests/test_work_project_start_canon_checklist_contract.py`

- [x] **Step 1: Write failing receipt tests**

Added tests for a mandatory, evidence-bound benchmark/reverse-engineering receipt and a non-destructive legacy context/configuration hygiene receipt.

- [x] **Step 2: Confirm RED**

The two new tests failed because no owner supplied the mandatory state, classification, or removal-safety fields.

- [x] **Step 3: Implement the smallest shared contract extension**

Added fixed L1+ preflight rules, existing owner routes, template fields, a no-fixed-controls boundary, and safe cleanup requirements without adding a new Skill, runtime schema, or universal configuration framework.

- [x] **Step 4: Verify focused contracts and generated artifacts**

Run: `python -m unittest tests.test_work_project_start_canon_checklist_contract tests.test_feature_code_contract_modularity tests.test_repository_first_workspace_contract tests.test_resilient_execution_narrative_reference_contract tests.test_visual_collaboration_capability_contract -v`, `python tools/build_base_v9_artifacts.py --check`, and `python tools/check_ci_required_gate_topology.py`.

Expected: all focused tests and both structural checks pass; no runtime or human evidence is implied.

### Task 2: Publish and integrate the V4 correction

**Files:**
- Modify only Task 1 files if CI or review finds a valid scope-bound correction

**Interfaces:**
- Consumes: latest `origin/main`, Task 1 exact commit, Ruleset-required `ci-gate`
- Produces: squash-merged V4 authority correction and exact `main` readback

- [ ] **Step 1: Re-fetch and preflight before publishing**

Run: `git fetch origin --prune` followed by a base/head/dirty-state comparison and a read-only comparison against PRs #803, #804, and #809.

- [ ] **Step 2: Run full exact-head validation**

Run: `python tools/run_local_validation.py --trusted-history-commit <current-origin-main-parent-sha>`

Expected: full Base validator passes; configured Godot/environment checks may remain explicitly skipped.

- [ ] **Step 3: Publish a new V4 correction PR**

Push the current branch, create a PR against `main`, record its exact head SHA and scope, and leave the source PR branches untouched.

- [ ] **Step 4: Verify remote gates and merge**

Confirm the current PR exact head has all required checks, strict `ci-gate`, zero unresolved threads, and a mergeable squash path; squash merge only after those readbacks.

- [ ] **Step 5: Read back merged main**

Fetch `origin/main`, verify the merge SHA and relevant active files, rerun focused authority checks, and retain V3 as compatibility-only.

### Task 3: Rebuild the UI workflow successor for PRs #803 and #804

**Files:**
- Modify/Create from the current UI owner only: `skills/auditing-and-refining-ui-art/`, its project adapter reference, UI production guide/packet, focused contract tests, and any validator already owned by that route

**Interfaces:**
- Consumes: fresh project repository authority, actual consumers, relevant benchmark evidence, V4 workspace authority, and read-only source PR deltas
- Produces: project-specific screen/action/flow discovery requirements and an evidence ceiling that cannot claim runtime implementation

- [ ] **Step 1: Start a new worktree from the merged V4 `main`**

Create a separate `codex/` branch; record PR #803 and #804 head SHAs, path overlap, and absorbed versus residual material.

- [ ] **Step 2: Write RED tests for the clarified UI contract**

Add focused tests that fail when the guide requires a fixed global button list, accepts a benchmark without project-specific consumer/discovery evidence, or promotes a wireframe/flow proposal to runtime proof.

- [ ] **Step 3: Reimplement only validated UI proposal material**

Integrate current-main-compatible content from #803/#804 into the existing UI owner. Require project-specific `existing / needed / not-applicable` screen and action status, relevant benchmark disposition, consumer/planned-consumer trace, and wireframe/flow use only where it reduces a concrete decision ambiguity.

- [ ] **Step 4: Run focused and reference-freshness tests**

Run the UI contract tests, validator regression tests, `git diff --check`, and `python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base <base-sha> --head HEAD`.

- [ ] **Step 5: Publish, CI-verify, squash merge, and read back**

Create a successor PR, wait for its exact-head required checks and zero unresolved threads, squash merge, then verify the merged UI owner does not require universal buttons and does not assert Godot runtime evidence.

### Task 4: Rebuild the backend authorization successor for PR #809

**Files:**
- Modify/Create from existing owners only: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`, `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`, `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`, focused backend tests, and their documented learning links when required by coupled-change checks

**Interfaces:**
- Consumes: current backend guide, project contract template, evidence pack, and the fifteen read-only PR #809 review findings
- Produces: applicability-aware denial, session, identity, protocol, and reproducibility evidence fields without a runtime-security PASS claim

- [ ] **Step 1: Start a new worktree from the merged UI `main`**

Record PR #809's exact source head and all unresolved review threads as a read-only finding list.

- [ ] **Step 2: Write RED tests for each validated security gap**

Cover per-case denial readbacks; all required session invalidation triggers; reproducibility context; managed identity applicability; separate read/update/delete and identity-state cases; filtered bulk-read outcomes; self-managed password parameters; protocol/client applicability; WebSocket reconnect authorization; trusted server-side privilege derivation; strict section extraction; and independent evidence-state preservation.

- [ ] **Step 3: Apply narrow guide/template/test corrections**

Make each requirement either required when applicable or justified `NOT_APPLICABLE`. Keep deployment, load, failure, cost, runtime, human, and release evidence independent; retain `STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE`.

- [ ] **Step 4: Run targeted security regression and full validation**

Run backend focused suites first, then the full local validator with the fresh trusted base SHA, freshness audit, and `git diff --check`.

- [ ] **Step 5: Publish, CI-verify, squash merge, and read back**

Create a successor PR, confirm every resolved finding is covered by the current exact head and remote required checks, squash merge, and verify the merged main contains no false runtime/deployment completion claim.

### Task 5: Final adversarial closure

**Files:**
- Inspect: all merged successor paths, `docs/DOCUMENTATION_MAP.md`, `START_HERE.md`, `skills/SKILL_REGISTRY.json`, related tests, PRs #803/#804/#809, and new merge commits

**Interfaces:**
- Consumes: final `origin/main`, merge commit evidence, remote checks, and fresh reference scan
- Produces: five full-scope adversarial-loop records and a truthful clean-exit report

- [ ] **Step 1: Run five full-scope attack/validate/regression loops**

For each loop, inspect authority, source PR overlap, consumer propagation, fixed-control regression, security evidence ceiling, CI, branch protection, rollback, and long-term maintenance; make a minimal fix only for a validated finding.

- [ ] **Step 2: Recalculate remaining work**

Verify all three correction goals have a merged successor or a precise blocker; do not treat a source PR, test definition, or historical CI as completion evidence.

- [ ] **Step 3: Final readback and report**

Fetch main, inspect all merge commits and current required-check results, rerun applicable focused checks, report no unperformed runtime/human tests as PASS, and identify only actual remaining blockers or deferred project-specific implementation.
