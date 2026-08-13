# Concurrent Git Sync Preflight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fail-closed concurrent-change preflight to the existing Git synchronization Skill so parallel chats and agents do not overwrite, duplicate, self-conflict, or merge against stale Base work.

**Architecture:** Keep `synchronizing-local-and-github-state` as the sole owner. Add identity-bound and phase-bound SHA evidence to its `inspect` contract, place operational detail in the existing safe-sync reference, wire a dedicated contract test into focused Base v9 CI, connect the established GPT/Codex workflow test and a Skill-local Learning Log, and document the repository-wide adversarial audit. No new ACTIVE Skill, Work Mode, workflow, dependency, schema, generated artifact, lock service, or repository setting is introduced.

**Tech Stack:** Markdown Skill contracts, Python 3.12 `unittest`, GitHub Actions, GitHub branch/PR APIs.

## Global Constraints

- Baseline is `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0` unless freshness checks require reconciliation.
- Do not modify any path changed by open PR #312.
- Do not modify `AGENTS.md`, Skill Registry, generated artifacts, release locks, workflows, schemas, or repository settings.
- Treat missing current identity, work-branch HEAD, PR/path/main, semantic ownership, or policy evidence as `BLOCKED_UNVERIFIED`, never as clear.
- Exclude the current Task/PR itself from same-goal and overlap comparison.
- Before the first write, use the observed isolated-branch HEAD as `write_parent_sha` and `expected_head_sha: PENDING_FIRST_WRITE`.
- After each write, bind the returned commit SHA as exact `expected_head_sha`; reread it before using it as the next `write_parent_sha`.
- A Skill body change must satisfy the repository's existing canonical-reference freshness companions rather than weakening the checker or relying only on a new standalone test.
- Search/code-search output is discovery evidence only. A repository fact must be confirmed by exact-SHA readback of the cited file or commit before it becomes a finding or coordination request.
- Use an isolated branch and squash merge only after exact-head CI, current-main recheck, and zero unresolved review threads.
- Preserve existing DIRTY/REMOTE_AHEAD/LOCAL_AHEAD/DIVERGED behavior.

---

### Task 1: Prove the missing concurrent preflight contract

**Files:**
- Create: `tests/test_concurrent_git_sync_preflight_contract.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: `skills/synchronizing-local-and-github-state/SKILL.md` and `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`.
- Produces: `ConcurrentGitSyncPreflightContractTests`, imported by `tests.test_v9_machine_contracts` so focused Base v9 CI executes it.

- [x] **Step 1: Write the initial failing contract test**

Require the Skill and reference to expose:

```text
CONCURRENT_CHANGE_PREFLIGHT
source_main_sha
current_main_sha
expected_head_sha
intended_paths
semantic_resource_locks
same_goal_open_and_recent_prs
open_pr_changed_paths
CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
first persistent write | PR creation | merge | post-merge main readback
PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
```

- [x] **Step 2: Wire the test into focused Base v9 CI**

```python
from tests.test_concurrent_git_sync_preflight_contract import (
    ConcurrentGitSyncPreflightContractTests
    as _ConcurrentGitSyncPreflightContractTests,
)
```

- [x] **Step 3: Verify initial RED**

Connector-only exact-head evidence:

```text
head: acb59559701f90ceb835a8a271c630058b863696
workflow run: 31653620789
job: 94303084090
focused tests: 327
failures: 2
skipped: 1
```

The only failures were the absent production preflight and absent first-write recheck. Generated/integrity gates and existing unrelated contracts passed.

- [x] **Step 4: Commit the test-only checkpoint**

The draft PR preserved this exact RED checkpoint before production implementation.

### Task 2: Implement the minimal owner and operational protocol

**Files:**
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`
- Create: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
- Modify: `tests/test_gpt_codex_workflow_contract.py`

**Interfaces:**
- Consumes: the dedicated test, the established GPT/Codex workflow integration test, canonical-reference freshness coupling, and existing Loop Engineering `TASK_LEASE` and path/semantic resource concepts.
- Produces: an inspect-time `CONCURRENT_CHANGE_PREFLIGHT`, ordered coordination procedure, reusable learning record, and existing-suite integration evidence.

- [x] **Step 1: Add the base preflight contract**

Define:

```yaml
CONCURRENT_CHANGE_PREFLIGHT:
  source_main_sha:
  current_main_sha:
  expected_head_sha:
  intended_paths: []
  semantic_resource_locks: []
  same_goal_open_and_recent_prs: []
  open_pr_changed_paths: {}
  overlap_classification: NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
  disposition: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
```

Preserve the existing sync state machine and state that this is a cooperative contract, not a GitHub-enforced mutex.

- [x] **Step 2: Add ordered safe-sync checks**

Cover first persistent write, PR creation, merge, and post-merge readback. Include disjoint-path reduction, owner-PR coordination, explicit handoff/resource release, stale-base reconciliation, exact-head verification, and fail-closed evidence handling.

- [x] **Step 3: Attack the first implementation**

Adversarial review found two concrete ambiguities:

1. The current PR could be classified as its own `SAME_GOAL` duplicate.
2. Before the first write, a final `expected_head_sha` does not exist, so write-parent and reviewed-head meanings could be conflated.

- [x] **Step 4: Strengthen the test before the fix**

Require:

```text
current_task_or_pr_identity
write_parent_sha
PENDING_FIRST_WRITE
exclude the current task or PR itself
```

Connector-only adversarial RED evidence:

```text
head: dc120e173922d97b610c115f82ba683d9c32157d
workflow run: 31654086012
job: 94304547739
focused tests: 327
failures: 2
skipped: 1
```

The only failures were the two newly required identity/phase tokens. Existing contracts again remained green.

- [x] **Step 5: Implement identity-bound and phase-bound SHA semantics**

Final production contract:

```yaml
current_task_or_pr_identity:
source_main_sha:
current_main_sha:
write_parent_sha:
expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
```

Rules:

1. Exclude the current Task/PR itself from same-goal and overlap comparisons.
2. Missing or ambiguous current identity fails closed.
3. `write_parent_sha` is the optimistic concurrency precondition for the next persistent write.
4. First write uses `PENDING_FIRST_WRITE`; its returned commit becomes exact `expected_head_sha`.
5. Before a later write, reread the Branch and promote the verified previous head to the new `write_parent_sha`.
6. A moved Branch HEAD blocks overwrite.
7. PR review, CI, and merge bind to the exact reviewed `expected_head_sha`.

- [x] **Step 6: Treat canonical-reference freshness failure as a third RED**

The first integration candidate proved the core contract but exposed a real repository consumer omission:

```text
head: 617778650deb644e0b549fc675ed942c786a6389
workflow: Validate Base v9 Operating Contracts
result: PASS, 327 tests, 1 configured Godot skip
workflow: Validate Game Project Operating System
run: 31654405601
job: 94305570328
result: FAIL at Check canonical reference freshness
```

Exact failure classes:

1. `local-skill-contract-learning-test-sync`: the new standalone test was not sufficient; an established integrated test companion had to change.
2. `local-skill-contract-learning-sync`: the Skill body change required a central or Skill-local Learning Log update.

Do not weaken `.github/reference-freshness.json` or touch an unrelated test merely to satisfy the gate.

- [x] **Step 7: Repair the missing consumers**

- Create `skills/synchronizing-local-and-github-state/LEARNING_LOG.md` with finding, decision, RED evidence, boundary, and next trigger.
- Modify `tests/test_gpt_codex_workflow_contract.py`, which already owns GPT/Codex handoff, Git authority, exact-head, and merge contracts.
- Assert the Skill, safe-sync protocol, and Learning Log together.
- Keep the dedicated focused test as the precise owner regression; use the established workflow test as integration evidence.

- [x] **Step 8: Verify final GREEN on the exact reviewed head**

Exact head `2780ee076c03f1257f0d28be1b541bb6877b6ad0` passed both repository workflows.

```text
Validate Base v9 Operating Contracts: SUCCESS
focused suite: 327 passed
configured Godot runtime skip: 1
adversarial gate: SUCCESS

Validate Game Project Operating System: SUCCESS
canonical-reference freshness: SUCCESS
docs/publication/concluding gates: SUCCESS
```

- [x] **Step 9: Truthfully substitute connector evidence for unavailable local validation**

Preferred local command when a checkout is available:

```bash
python tools/run_local_validation.py \
  --trusted-history-commit 453f790821a108a1d4f6e1f4e45f6931c2396ee0
```

This connector-only session had no local checkout. Exact-head GitHub Actions and post-merge push workflows were used, while local `tools/run_local_validation.py`, full tracked-byte inventory, `git fsck`, Godot runtime, and render checks remained explicitly unverified.

### Task 3: Record adversarial audit, review, and integrate

**Files:**
- Create: `docs/audits/2026-08-13-base-work-structure-adversarial-audit.md`
- Review: every PR diff path and concurrent PR #312 changed paths

**Interfaces:**
- Consumes: Base canon/Registry/generated map, open/recent PR inventory, external primary-source benchmarks, all RED checkpoints, final GREEN evidence, and exact-head CI.
- Produces: classified findings, before/after behavior, deferred risks, rollback, and post-merge readback.

- [x] **Step 1: Write the repository audit**

Record:

- current authority map, three Work Modes, and 30 Registry-derived ACTIVE Skills;
- verified omission: general sync Skill lacked concurrent PR/path/semantic preflight;
- verified adversarial ambiguity: current-PR self-conflict and first-write SHA phase confusion;
- verified integration omission: Skill body changed without an established test companion and Learning Log;
- concurrent PR #312 path ownership and zero changed-path intersection;
- `INVALIDATED_FINDING`: a search-only README drift hypothesis was disproved by exact-SHA readback and must not be presented as repository fact;
- rejected critique: a new broad Skill or lock service would duplicate the recent Loop Control Plane;
- `BLOCKED_UNVERIFIED`: connector-only session cannot claim a local byte-for-byte full tracked-file audit;
- benchmark decisions, source dates, exact changed/protected paths, validation, rollback, and expected effects.

- [x] **Step 2: Run adversarial regression review**

Attack:

1. Did the change create a fourth Work Mode or new ACTIVE Skill?
2. Did it weaken existing DIRTY/DIVERGED safeguards?
3. Does path overlap incorrectly imply a definite textual merge conflict?
4. Can missing evidence be reported as clear?
5. Can the current PR conflict with itself?
6. Are first-write parent and final reviewed head distinct?
7. Can a moved work Branch be overwritten?
8. Did any path overlap PR #312?
9. Is the dedicated test actually consumed by focused CI?
10. Does an established integration test and Learning Log consume the Skill change?
11. Was every repository factual claim confirmed on an exact ref rather than inferred from a search result?
12. Did main or the open PR set change after preflight?

Fix only verified in-scope findings and rerun exact-head checks.

- [x] **Step 3: Verify exact PR head and review state**

- reviewed HEAD: `2780ee076c03f1257f0d28be1b541bb6877b6ad0`
- applicable workflows: success
- unresolved inline review threads: 0
- mergeability: verified before merge

- [x] **Step 4: Recheck current main and concurrent work**

Immediately before merge:

```text
current main: 453f790821a108a1d4f6e1f4e45f6931c2396ee0
PR #312 changed-path intersection: 0
PR #315 changed-path intersection: 0
same-goal competing PR: none
```

- [x] **Step 5: Squash merge the reviewed exact head**

PR #313 was squash merged with the exact-head precondition. Resulting main commit:

```text
190511e3b7dcc368f45eb61348b23d2b5a93f3c2
```

- [x] **Step 6: Read back new main**

Verified on `main@190511e3b7dcc368f45eb61348b23d2b5a93f3c2`:

1. nine intended changed paths are present;
2. Skill/reference/dedicated-test/integration-test/Learning-Log tokens are present;
3. Work Modes remain three and Registry-derived ACTIVE Skills remain 30;
4. no new workflow, schema, dependency, Registry, or generated-artifact change was introduced;
5. open PRs #312 and #315 are not same-goal duplicates;
6. post-merge Base v9 push workflow succeeded and the Game Project Operating System push workflow entered its full validation topology.

- [ ] **Step 7: Rollback if a post-merge regression is verified**

Revert the single squash merge. No data/schema migration, generated-artifact restoration, dependency rollback, or project-specific synchronization is required.

### Task 4: Correct the search-only repository finding

**Files:**
- Modify: `docs/audits/2026-08-13-base-work-structure-adversarial-audit.md`
- Modify: `docs/superpowers/specs/2026-08-13-concurrent-sync-preflight-design.md`
- Modify: `docs/superpowers/plans/2026-08-13-concurrent-sync-preflight.md`
- Modify: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
- Modify: `tests/test_concurrent_git_sync_preflight_contract.py`

- [x] **Step 1: Reproduce the documentation error with a regression test**

Exact RED head:

```text
cb0ce1e6b9a0bf5936a8a024d23e8ab9b4b1d4cc
```

Focused suite result:

```text
328 tests run
1 expected failure: missing INVALIDATED_FINDING correction
327 existing contracts passed
1 configured Godot runtime skip
```

- [x] **Step 2: Establish exact repository truth**

Exact-SHA readback of the baseline, merged main, and PR #312 HEAD confirmed that README delegates the ACTIVE Skill view to `docs/generated/BASE_ACTIVE_SKILLS.md` and does not maintain a second Skill count/list.

- [x] **Step 3: Correct the durable record**

- Mark the hypothesis `INVALIDATED_FINDING` in audit, design, plan, and Learning Log.
- Preserve the real concurrency finding: PR #312 owned protected paths and PR #313 used a zero-intersection path set.
- Withdraw the incorrect coordination burden from PR #312.
- Keep the core sync-preflight implementation unchanged.

- [ ] **Step 4: Final correction gate**

The correction PR must pass both workflows on one exact head, recheck current main/open PR overlap, squash merge, and read back the corrected records on new main. Dynamic SHA and workflow evidence belong in the PR/Actions record rather than a self-referential final edit to this plan.

## Completion criterion

The work is complete only when the core preflight remains green, the search-only hypothesis is explicitly invalidated on main, the correction test passes, concurrent PR paths remain non-overlapping, and no unverified local/runtime claim is presented as executed.