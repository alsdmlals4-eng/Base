# Copy Integration Default Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Base's wait-on-open-PR behavior with a latest-main copy-integration workflow that preserves active PR branches read-only, reconciles conflicts on a separate branch, and removes unrelated open PRs as a global automation blocker.

**Architecture:** Reuse the existing `PROVISIONAL_INTEGRATION`, `USER_DIRECTED_PARALLEL_PR`, concurrent preflight, exact-head validation, and periodic Source Scan owners. Change the authorization default rather than adding a new Skill: the user's 2026-08-16 standing approval becomes the concurrency policy for Base. Periodic automation moves from all-open-PR blocking to overlap-aware gating.

**Tech Stack:** Markdown policy contracts, Bash orchestration, Python unittest contract tests, GitHub Actions.

## Global Constraints

- Active owner PR branches remain read-only unless the user explicitly assigns that PR itself.
- Every integration branch starts from exact latest completed `main`.
- Copy/reconcile only required material deltas; never overwrite newer main state with a stale whole-file copy.
- `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` is standing replacement authority for same-goal/path/semantic overlap coordination only.
- No direct main push, force push, `--admin`, ruleset bypass, deferred auto-merge, product scope expansion, payment, or privilege expansion.
- Required exact-head checks, unresolved review thread 0, P0/P1 0, and post-merge main readback remain mandatory.
- Scheduled automation may continue with unrelated open PRs; actual overlap must still be detected.

---

### Task 1: Lock the new concurrency behavior with RED contract tests

**Files:**
- Modify: `tests/test_concurrent_git_sync_preflight_contract.py`
- Modify: `tests/test_continuous_work_execution_contract.py`
- Modify: `tests/test_periodic_source_analysis_runner.py`
- Modify: `tests/test_periodic_source_scan_queue.py`

**Interfaces:**
- Consumes: existing `PROVISIONAL_INTEGRATION`, `USER_DIRECTED_PARALLEL_PR`, periodic runner text contracts.
- Produces: contract assertions for standing copy-integration authorization and overlap-aware scheduled automation.

- [ ] **Step 1: Update concurrent sync expectations.**

Require:

```text
BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
copy integration
owner PR branches
semantic reconciliation
absorbed_owner_deltas
residual_owner_deltas
```

Reject the old invariant that a fresh `explicit user authorization` is required for every overlap merge.

- [ ] **Step 2: Update continuous-work expectations.**

Require that same-goal/path/semantic overlap routes to latest-main separate integration branch, and that an open owner PR is not itself a merge blocker once all material delta is absorbed and exact-head gates pass.

- [ ] **Step 3: Update scheduled Source Scan expectations.**

Replace the test that requires `any foreign PR => defer` with assertions that:

```text
open PR presence alone does not block analysis
actual path overlap is checked
BLOCKED_ACTIVE_PR_GUARD is absent
BLOCKED_OPEN_PR_CONFLICT remains or is replaced by an equally narrow overlap blocker
```

- [ ] **Step 4: Commit RED tests.**

Expected CI result: focused contract tests fail only because current policy/runner still contains the old all-open-PR and per-case authorization rules.

---

### Task 2: Promote copy integration to the Base standing coordination rule

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`
- Modify: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`

**Interfaces:**
- Consumes: the existing concurrency preflight and provisional integration data fields.
- Produces: standing policy `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` and updated merge/supersede behavior.

- [ ] **Step 1: Replace per-case authorization wording.**

Set `provisional_integration_authorized` to derive from the standing Base policy for ordinary same-goal/path/semantic reconciliation. Keep explicit user confirmation only for new scope/high-risk actions.

- [ ] **Step 2: Change WAITING/DUPLICATE recovery.**

For approved work, `WAITING_RESOURCE` and `DUPLICATE_WORK` first attempt:

```text
latest main
→ separate integration branch
→ owner head/path/resource snapshot
→ selective material copy
→ semantic reconciliation
→ exact-head validation
```

Only genuinely unresolvable evidence/authority gaps remain deferred.

- [ ] **Step 3: Change merge gate.**

Do not require owner PR closure before integration merge when the integration PR proves complete material absorption. Record `absorbed_owner_deltas` and `residual_owner_deltas`. After merge, fully absorbed PRs are superseded; residual unique work remains open.

- [ ] **Step 4: Update both Learning Logs.**

Record the user-observed failure mode: strict serialization created avoidable waiting; selective copy integration preserves branch safety without idle time.

---

### Task 3: Remove the global active-PR stop from Periodic Source Scan

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md`
- Modify: `tools/run_periodic_source_scan_queue.sh`
- Modify: `.github/workflows/periodic-source-scan-queue.yml`

**Interfaces:**
- Consumes: open PR list and changed-path inspection.
- Produces: unrelated-open-PR tolerant scheduled execution with overlap-only blocking/reconciliation.

- [ ] **Step 1: Replace `SCHEDULED_AUTOMATION_ACTIVE_PR_GUARD`.**

Document an overlap-aware contract:

```text
open PR query
→ analysis allowed
→ changed files known
→ compare foreign PR paths
→ no overlap: continue
→ overlap: copy-integration reconciliation when bounded/deterministic
→ unsafe reconciliation: defer only conflicted write
```

- [ ] **Step 2: Remove runner entry/merge checks that call `assert_no_foreign_open_prs`.**

Keep an open-PR query helper that can fail closed when the PR set itself cannot be read, but do not block solely on a non-empty set.

- [ ] **Step 3: Keep actual path-overlap detection.**

Before branch publication and again before merge, compare `changed-files.txt` with foreign PR changed files. Unrelated PRs must not block.

- [ ] **Step 4: Update workflow contract comments.**

Remove obsolete `BLOCKED_ACTIVE_PR_GUARD*` tokens and expose the overlap-aware copy-integration contract to workflow-only readers.

---

### Task 4: GREEN validation, adversarial review, merge, and post-merge reconciliation

**Files:**
- No new production paths unless validation finds an in-scope contract mismatch.

- [ ] **Step 1: Run/observe exact-head required checks.**

At minimum:

```text
Validate Base v9 Operating Contracts
Validate Game Project Operating System
Validate Loop A2 Durable Resume or current consumer of continuous-work tests
Validate Evidence-Based Game Development Knowledge / Periodic Source Scan contract path when triggered
```

- [ ] **Step 2: Adversarially attack the policy.**

Check:

```text
stale whole-file copy overwrites newer main
owner branch is modified
unique owner delta is lost when superseding
unrelated PR still blocks periodic automation
actual overlap is ignored
main moves after validation
standing authorization leaks into scope expansion/high-risk action
```

- [ ] **Step 3: Reconcile current main.**

If `main` moved, merge/reapply the policy branch onto latest main without touching active owner branches, rerun exact-head validation.

- [ ] **Step 4: Merge with expected head.**

Require unresolved review threads 0 and exact reviewed head. Use repository-allowed squash merge.

- [ ] **Step 5: Post-merge readback.**

Verify new `main` contains the standing policy, periodic runner no longer contains global active-PR blocking, and open PRs remain untouched.

## Rollback

Revert the merged policy PR. This restores strict active-PR serialization and per-case provisional replacement authorization. No data migration is involved.
