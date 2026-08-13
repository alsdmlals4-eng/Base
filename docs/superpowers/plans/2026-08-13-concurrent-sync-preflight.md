# Concurrent Git Sync Preflight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fail-closed concurrent-change preflight to the existing Git synchronization Skill so parallel chats and agents do not overwrite, duplicate, or merge against stale Base work.

**Architecture:** Keep `synchronizing-local-and-github-state` as the sole owner. Add evidence and dispositions to its `inspect` contract, place operational detail in the existing safe-sync reference, wire a dedicated contract test into focused Base v9 CI, and document the repository-wide adversarial audit. No new ACTIVE Skill, Work Mode, workflow, dependency, schema, or lock service is introduced.

**Tech Stack:** Markdown Skill contracts, Python 3.12 `unittest`, GitHub Actions, GitHub branch/PR APIs.

## Global Constraints

- Baseline is `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0` unless freshness checks require reconciliation.
- Do not modify any path changed by open PR #312.
- Do not modify `AGENTS.md`, Skill Registry, generated artifacts, release locks, workflows, schemas, or repository settings.
- Treat missing PR/path/main evidence as `BLOCKED_UNVERIFIED`, never as clear.
- Use an isolated branch and squash merge only after exact-head CI and current-main recheck.
- Preserve existing DIRTY/REMOTE_AHEAD/LOCAL_AHEAD/DIVERGED behavior.

---

### Task 1: Prove the missing concurrent preflight contract

**Files:**
- Create: `tests/test_concurrent_git_sync_preflight_contract.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: existing Skill path `skills/synchronizing-local-and-github-state/SKILL.md` and reference path `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`.
- Produces: `ConcurrentGitSyncPreflightContractTests`, imported by `tests.test_v9_machine_contracts` so focused Base v9 CI executes it.

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_concurrent_git_sync_preflight_contract.py` with assertions for:

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ConcurrentGitSyncPreflightContractTests(unittest.TestCase):
    def test_sync_skill_fails_closed_on_concurrent_change_evidence(self) -> None:
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")
        for token in (
            "CONCURRENT_CHANGE_PREFLIGHT",
            "source_main_sha",
            "current_main_sha",
            "expected_head_sha",
            "intended_paths",
            "semantic_resource_locks",
            "same_goal_open_and_recent_prs",
            "open_pr_changed_paths",
            "CLEAR",
            "STALE_BASE_SHA",
            "WAITING_RESOURCE",
            "DUPLICATE_WORK",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, skill)

    def test_safe_sync_protocol_rechecks_before_write_pr_merge_and_after_merge(self) -> None:
        protocol = read(
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        )
        for token in (
            "first persistent write",
            "PR creation",
            "merge",
            "post-merge main readback",
            "PATH_OVERLAP",
            "SEMANTIC_OVERLAP",
            "SAME_GOAL",
            "UNKNOWN",
            "cooperative",
        ):
            self.assertIn(token, protocol)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Wire the test into focused Base v9 CI**

Add this import to `tests/test_v9_machine_contracts.py`:

```python
from tests.test_concurrent_git_sync_preflight_contract import (
    ConcurrentGitSyncPreflightContractTests
    as _ConcurrentGitSyncPreflightContractTests,
)
```

- [ ] **Step 3: Verify RED**

Run locally when a checkout is available:

```bash
python -m unittest tests.test_v9_machine_contracts -v
```

Expected: FAIL because `CONCURRENT_CHANGE_PREFLIGHT` and its dispositions are absent from the production Skill/reference.

In a connector-only session, open a draft PR at the test-only head and require the focused `base-v9-contract` job to fail for the same missing tokens. Record the exact RED head and failing assertion.

- [ ] **Step 4: Commit**

```bash
git add tests/test_concurrent_git_sync_preflight_contract.py tests/test_v9_machine_contracts.py
git commit -m "test: require concurrent sync preflight"
```

### Task 2: Implement the minimal owner and operational protocol

**Files:**
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`

**Interfaces:**
- Consumes: the test tokens and the existing Loop Engineering `TASK_LEASE`/semantic resource concepts.
- Produces: an inspect-time `CONCURRENT_CHANGE_PREFLIGHT` record and fail-closed coordination procedure.

- [ ] **Step 1: Extend the Skill input and state contract**

Add required inputs for exact source/current/head SHAs, intended paths, semantic resources, same-goal open/recent PRs, changed paths, and protected concurrent paths. Define:

```yaml
CONCURRENT_CHANGE_PREFLIGHT:
  overlap_classification: NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN
  disposition: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED
```

Preserve the existing sync state machine and explain that the record is a cooperative contract, not a GitHub-enforced mutex.

- [ ] **Step 2: Extend the safe-sync reference**

Add ordered checks before first persistent write, PR creation, merge, and after merge. Include disjoint-path selection, PR coordination comments, resource waiting, stale-base reconciliation, exact-head verification, and fail-closed evidence handling.

- [ ] **Step 3: Verify GREEN on the focused test**

```bash
python -m unittest tests.test_v9_machine_contracts -v
```

Expected: PASS.

- [ ] **Step 4: Run full Base validation**

```bash
python tools/run_local_validation.py \
  --trusted-history-commit 453f790821a108a1d4f6e1f4e45f6931c2396ee0
```

Expected: exit 0. In a connector-only session, use all triggered GitHub Actions checks on the exact PR head and report local execution as unavailable rather than inferred.

- [ ] **Step 5: Commit**

```bash
git add skills/synchronizing-local-and-github-state/SKILL.md \
  skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md
git commit -m "feat: add concurrent sync preflight"
```

### Task 3: Record adversarial audit, review, and integrate

**Files:**
- Create: `docs/audits/2026-08-13-base-work-structure-adversarial-audit.md`
- Review: all PR diff paths

**Interfaces:**
- Consumes: Base canon/Registry/generated map, open/recent PR inventory, external primary-source benchmarks, RED/GREEN evidence, and exact-head CI.
- Produces: classified findings, before/after behavior, deferred risks, rollback, and post-merge readback.

- [ ] **Step 1: Write the audit report**

Record:

- current authority map and 30 active Skills;
- verified conflict: README hardcoded 27 vs Registry-derived 30, coordinated through PR #312 rather than overlapping edit;
- verified omission: general sync Skill lacked concurrent PR/path/semantic preflight;
- rejected critique: creating a new broad Skill or lock service would duplicate the recent Loop Control Plane;
- `BLOCKED_UNVERIFIED`: connector-only session cannot claim a local byte-for-byte full tracked-file audit;
- benchmark decisions and source dates;
- exact changed paths, protected paths, validation, rollback, and expected effects.

- [ ] **Step 2: Run adversarial regression review**

Attack:

1. Did the change accidentally create a fourth Work Mode or new ACTIVE Skill?
2. Did it weaken existing dirty/diverged safeguards?
3. Does a path overlap incorrectly imply a definite textual conflict?
4. Can missing evidence be reported as clear?
5. Did any path overlap PR #312?
6. Is the dedicated test actually consumed by focused CI?
7. Did main or the open PR set change after the preflight?

Fix only verified in-scope findings and rerun tests.

- [ ] **Step 3: Verify exact PR head**

Require all applicable GitHub Actions checks to complete successfully on the exact head. Confirm unresolved review threads are zero and compare the reviewed head SHA to the merge target.

- [ ] **Step 4: Recheck current main and open PRs**

If main changed, reconcile without force push and rerun relevant checks. If new path/semantic overlap appears, classify `WAITING_RESOURCE` or `DUPLICATE_WORK` rather than merging.

- [ ] **Step 5: Squash merge and read back new main**

Merge only the reviewed exact head. Fetch new `main`, verify the changed files and key contract tokens, recheck same-goal open/recent PRs, and report any post-merge omission or conflict.

- [ ] **Step 6: Rollback procedure**

If post-merge regression is verified, revert the single squash merge. No data/schema migration or generated-artifact restoration is required.