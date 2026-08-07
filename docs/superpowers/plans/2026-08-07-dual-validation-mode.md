# Dual CI Validation Mode Implementation Plan

> **For agentic workers:** Use the existing validation Skill and repository-owned tests. This plan records the approved design, TDD evidence, implementation state, and final verification gate.

**Goal:** Keep the existing GitHub Actions `ci-gate` as the normal Required Check and add a fail-closed local fallback that may publish the same `ci-gate` commit status only when canonical remote validation has not taken ownership and the required evidence is locally reproducible.

**Original baseline:** `main@4f98f968a377f7b6a11aafa4fc94d11bddbebedc`

**Final verification base:** `main@8a1b868346b5d1cbe50d458e975fca277e42b2a5`

**Branch:** `agent/dual-validation-gate`

**Draft PR:** `#208`

## Global constraints

- Runtime modes are exactly `REMOTE_CI` and `LOCAL_FALLBACK`; routing is not a third mode.
- Public standard GitHub-hosted Actions remain the default path. Zero paid budget is not a fallback trigger.
- Preserve the active `solo-main-safety` Ruleset and Required Check name `ci-gate`.
- Do not add bypass actors, disable strict checks, or change branch protection to make fallback work.
- A canonical `REMOTE_CI workflow run`, `ci-gate` Check Run, or existing `ci-gate` commit status owns/occupies the validation target and blocks local fallback.
- A failed/cancelled/queued/in-progress remote run is not fallback-eligible.
- `LOCAL_FALLBACK` must fail closed on dirty worktree, stale base, SHA mismatch/drift, API/auth failure, local validation failure, remote-ownership race, existing gate evidence, or non-locally-reproducible changes.
- Reuse `tools/run_local_validation.py`; do not duplicate its validation matrix.
- Base default fallback eligibility is documentation and limited canonical contract files. `CODE_OR_ENGINE` and `CI_TOOLCHAIN_HIGH_RISK` require remote CI unless a repository-specific equivalent local contract exists.
- No new broad Skill, Mode, Schema, Ruleset, Required Check identity, or canonical workflow topology.
- PR #200 one-click operator handoff is now merged on latest main and is a current compatible consumer; do not duplicate or regress it.

---

## Task 1 — TDD RED: specify fallback behavior

**Files:** `tests/test_local_ci_fallback.py`

- [x] Add temporary git repository + local bare origin fixture.
- [x] Add cross-platform fake GitHub CLI executed with Python rather than POSIX shebang assumptions.
- [x] Specify dirty worktree refusal.
- [x] Specify local HEAD / PR head mismatch refusal.
- [x] Specify stale base refusal.
- [x] Specify head/test-merge `ci-gate` Check Run refusal.
- [x] Specify existing `ci-gate` commit status refusal.
- [x] Specify canonical `REMOTE_CI workflow run` refusal even before final `ci-gate` Check Run exists.
- [x] Specify trusted-history SHA must equal freshly fetched `origin/<base>`.
- [x] Specify non-locally-reproducible code/CI changes are refused.
- [x] Specify local validation failure never publishes success.
- [x] Specify race where `ci-gate` appears during validation blocks publish.
- [x] Specify success publishes exactly one `ci-gate=success` status to exact PR head.

### RED evidence

- [x] Initial RED observed on public GitHub Actions before production tool existed: run `31179584663`.
- [x] Adversarial RED observed after adding stronger guards but before implementing them: canonical run `31181462560` on head `bafb097fd5ad0a68dfeb6efdda96ed52d8486eac`.
- [x] The second RED specifically caught:
  - missing existing commit-status guard,
  - missing locally reproducible change boundary,
  - missing canonical-policy wording for remote workflow ownership.
- [x] A real pending canonical workflow run with zero jobs was separately observed during development, proving that Check Run absence alone cannot establish Actions unavailability.

## Task 2 — Implement bounded local fallback tool

**Files:** `tools/run_local_ci_fallback.py`

- [x] Implement `gh auth status` and PR metadata preflight.
- [x] Verify exact local/PR head and clean worktree.
- [x] Fetch current base and require `origin/<base>` ancestor of head.
- [x] Require supplied trusted-history SHA to equal freshly fetched exact base SHA.
- [x] Classify changed paths and allow only locally reproducible fallback scope.
- [x] Query canonical remote workflow runs by head SHA.
- [x] Query head/test-merge Check Runs for `ci-gate`.
- [x] Query head/test-merge commit statuses for existing `ci-gate`.
- [x] Refuse fallback whenever any remote ownership/gate evidence exists.
- [x] Execute existing `tools/run_local_validation.py --trusted-history-commit <current-base-sha>`.
- [x] Re-fetch/recheck head, worktree, base SHA, PR state, reproducibility boundary, workflow run, Check Run, and status after validation.
- [x] Publish `context=ci-gate`, `state=success` only to exact validated PR head.
- [x] Return non-zero without status on every blocked/error path.

## Task 3 — Reuse existing CI integration instead of changing workflow topology

**Files:**

- `tests/test_local_validation.py`
- `tests/test_ci_workflow_cost_policy.py`
- existing `.github/workflows/validate-game-project-operating-system.yml` (read/verified only)

- [x] Confirm canonical workflow already classifies generic `tools/*` and `tests/*` changes at code/high-risk tiers.
- [x] Confirm `ubuntu-contract` already runs `tests/test_local_validation.py`.
- [x] Import `LocalCiFallbackTests` into `tests/test_local_validation.py` so the existing canonical path executes the new suite.
- [x] Keep `.github/workflows/validate-game-project-operating-system.yml` unchanged.
- [x] Keep final job name and Required Check topology unchanged: `ci-gate`.
- [x] Re-read latest `main@8a1b868346b5d1cbe50d458e975fca277e42b2a5`; PR #200/#210 added operator-handoff validation to the canonical workflow without changing the final `ci-gate` topology, so the aggregator strategy remains compatible.

This is an Existing Solution First refinement over the initial plan. Editing workflow YAML merely to enumerate the new test would duplicate a capability the existing aggregator already provides.

## Task 4 — Synchronize policy, Skill, budget, and repository assumptions

**Files:**

- `docs/CI_EXECUTION_COST_POLICY.md`
- `docs/GITHUB_PRO_OPERATING_POLICY.md`
- `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/reviewing-and-validating-project-changes/LEARNING_LOG.md`
- `tests/test_gpt_codex_workflow_contract.py`

- [x] Define `REMOTE_CI` as the public standard-runner default.
- [x] Define `LOCAL_FALLBACK` as infrastructure-only.
- [x] State that cost/budget alone does not select fallback for public standard runners.
- [x] State that canonical remote workflow-run existence blocks fallback before final Check Run creation.
- [x] State that existing `ci-gate` Check Run/status blocks fallback.
- [x] State that failed/cancelled/pending remote validation cannot be replaced by local status.
- [x] Define conservative locally reproducible scope.
- [x] Default `CODE_OR_ENGINE` and `CI_TOOLCHAIN_HIGH_RISK` to `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED` when Actions is unavailable and no equivalent project-local validation contract exists.
- [x] Update stale active `omenward private` governance test/template assumptions to current public-repository operation.
- [x] Add Skill learning log entry because reference-freshness treats the Skill body as an active behavior source.

## Task 5 — Adversarial review checklist

- [x] **Failed test bypass:** blocked; fallback cannot replace a remote failure.
- [x] **Check/status collision:** blocked; both Check Runs and existing statuses are queried.
- [x] **Workflow-run race:** blocked; canonical workflow run is queried independently of final `ci-gate` Job creation.
- [x] **Stale local branch:** blocked; freshly fetched `origin/<base>` must be ancestor and exact trusted history.
- [x] **Wrong SHA status:** blocked; exact PR/local head is captured and rechecked.
- [x] **Base drift during validation:** blocked; base is re-fetched and exact SHA compared.
- [x] **Actions recovery during validation:** blocked by post-validation remote ownership recheck.
- [x] **Non-equivalent local evidence:** blocked by locally reproducible file boundary; code/engine/CI defaults fail closed.
- [x] **Ruleset drift:** no Ruleset/Required Check change is part of this PR.
- [x] **Duplicate Skill/validator:** no new broad Skill; existing local validator reused.
- [x] **Public/private billing drift:** active current project policy/template now treats current repositories as public, while historical plans/logs remain historical evidence.
- [x] **Concurrent main drift:** latest main advanced to `8a1b868346b5d1cbe50d458e975fca277e42b2a5` with PR #200/#210; re-read affected workflow/tests and found no content overlap in the 12 files changed by this work.

## Task 6 — Final exact-head verification

- [x] Detect that main advanced during the task and invalidate the older exact-head verification attempt.
- [ ] Integrate `main@8a1b868346b5d1cbe50d458e975fca277e42b2a5` into the work branch while preserving only this work's 12-file diff.
- [ ] Wait for the refreshed PR head's canonical public GitHub Actions run.
- [ ] Verify reference freshness passes.
- [ ] Verify docs-validation passes.
- [ ] Verify ubuntu-contract passes, including all fallback tests.
- [ ] Verify required publication/Windows smoke for this high-risk tool change passes.
- [ ] Verify final `ci-gate` passes on the exact final validation target.
- [ ] Compare latest main to final branch and inspect every changed file for unexpected scope.
- [ ] Re-run repository-wide active-reference searches for `ci-gate`, `BLOCKED_BY_GITHUB_ACTIONS`, Actions unavailable, and stale public/private assumptions.
- [ ] Update Draft PR #208 body with RED/GREEN evidence, residual risks, rollback, latest-main refresh, and merged PR #200 compatibility.
- [ ] Keep PR #208 Draft and do not merge without separate authorization.

## Rollback

Rollback is code-only and does not require Ruleset changes:

1. remove `tools/run_local_ci_fallback.py` and its tests/aggregator import;
2. restore the previous CI policy/Skill/budget language;
3. retain the existing `ci-gate` Required Check and canonical workflow;
4. return Actions-unavailable state to `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`.
