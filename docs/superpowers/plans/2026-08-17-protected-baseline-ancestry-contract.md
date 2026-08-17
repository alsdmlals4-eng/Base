# Protected Baseline Ancestry Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permit a stable historical protected baseline for `REMOTE_TRACKING_REF` when that baseline remains an ancestor of the current external authority, without weakening protected-path change detection.

**Architecture:** The large legacy `project_operating_contract.py` remains byte-stable. The already-reviewed `base_release_index.py` compatibility installer wraps only the `REMOTE_TRACKING_REF` path of `_trusted_protected_base()`. Official `check_project_operating_contract.py` installs this compatibility layer before validation, and both Linux and Windows Tool Hub identity validators package `base_release_index.py` into their reviewed validator runtime. On successful ancestry authentication the wrapper returns the historical adapter baseline, not the current authority commit, so `_protected_policy_errors()` continues diffing the complete historical-baseline→working-tree interval. Explicit `--protected-base` and `GITHUB_PR_BASE` behavior delegate unchanged to the legacy implementation.

**Tech Stack:** Python 3.12, `unittest`, temporary Git repositories through argv-only `subprocess`, existing Base compatibility installer and project operating-contract helpers, GitHub Actions.

## Global Constraints

- `REMOTE_TRACKING_REF` baseline must be equal to or an ancestor of the resolved authority commit.
- A missing or non-ancestor adapter baseline fails closed.
- Successful remote ancestry authentication must return the adapter-recorded historical baseline; returning the resolved authority commit is forbidden.
- Protected-path changes since the historical baseline remain fail-closed through `_protected_policy_errors()`.
- `GITHUB_PR_BASE` semantics and explicit trusted `--protected-base` semantics remain unchanged.
- The compatibility layer must use existing `_resolve_commit()`, `_commit_exists()`, and `_is_ancestor()` helpers; no shell-string Git execution.
- Linux and Windows Tool Hub validator bundles must continue to include and authenticate `base_release_index.py`.
- Do not modify unrelated open/draft/ready PRs.
- Do not add paid services, subscriptions, or new network dependencies.
- This Base PR completes before the `urban-legend` adapter-v2 migration begins.

---

### Task 1: Lock the ancestry and historical-diff contract with failing tests

**Files:**
- Create: `tests/test_project_protected_baseline_authority.py`
- Modify: `tests/test_local_validation.py`

**Interfaces:**
- Consumes: the exact compatibility installer used by the official project validator and Tool Hub sealed runtimes.
- Produces: regression coverage proving ancestor acceptance returns the historical baseline and protected-path changes are still measured from that baseline.

- [x] **Step 1: Reproduce the original defect before production modification**

PR #495 test-only head `a68c53c05c4e8f5748e498a67cad2f149e32ce93` reproduced the exact-equality defect in the dependency-complete Ubuntu contract gate. Equal authority passed while ancestor/missing/divergent/historical-diff cases failed before reaching the intended ancestry contract.

- [x] **Step 2: Reject invalid RED evidence from the lightweight docs environment**

The first placement also caused `ModuleNotFoundError: jsonschema` in `docs-validation`, which intentionally does not install publication/contract dependencies. That failure is not accepted as contract RED evidence.

- [x] **Step 3: Move focused coverage to the Ubuntu-only local-validation aggregate**

Create a dedicated protected-baseline test module and import its TestCase from `tests/test_local_validation.py`, which is already compiled and executed by `ubuntu-contract` but not by the lightweight docs gate. No workflow edit is required.

- [ ] **Step 4: Rebase the test-only state onto the current Base main and verify clean RED**

The branch must be based on completed Base main `2b8856054573f1a06297ac8e65f5ca009fa2daef` (or a later completed main if it advances again). `docs-validation` must pass. `ubuntu-contract` must fail specifically on ancestor/missing/divergent/historical-diff assertions while equal authority and unchanged explicit-override/GITHUB_PR_BASE assertions pass.

### Task 2: Install the minimum fail-closed remote ancestry compatibility rule

**Files:**
- Modify: `tools/base_release_index.py`
- Test: `tests/test_project_protected_baseline_authority.py`

**Interfaces:**
- Consumes: existing `_resolve_commit()`, `_commit_exists()`, `_is_ancestor()`, and legacy `_trusted_protected_base()`.
- Produces: official validator behavior that accepts a historical remote baseline iff it exists and is an ancestor of the resolved remote authority.

- [ ] **Step 1: Add one idempotent compatibility installer**

For `protected_base_override` or any authority kind other than `REMOTE_TRACKING_REF`, delegate to the legacy function unchanged. For `REMOTE_TRACKING_REF` with no explicit override:

```python
resolved = contract_module._resolve_commit(project_root, authority_ref)
if resolved is None:
    return None, [f"Protected authority ref cannot be resolved to a commit: {authority_ref}"]
if not contract_module._commit_exists(project_root, adapter_commit):
    return None, [f"Protected baseline commit is absent: {adapter_commit}"]
if not contract_module._is_ancestor(project_root, adapter_commit, resolved):
    return None, [
        "External protected baseline must be an ancestor of its authority: "
        f"{adapter_commit} is not an ancestor of {authority_ref} ({resolved})"
    ]
return adapter_commit, []
```

`install_release_lock_paths()` must install this wrapper alongside the existing immutable release-finalization compatibility rule.

- [ ] **Step 2: Re-run exact-head focused and aggregate contract coverage**

Expected: all protected-baseline cases pass, including the historical protected-path change detection case.

- [ ] **Step 3: Verify the full PR gate**

Require `Validate Game Project Operating System` `ci-gate`, `Validate Base v9 Operating Contracts`, and every required job selected for the exact PR head to complete successfully.

- [ ] **Step 4: Adversarially inspect the final diff**

Confirm the only production semantic change is the idempotent `REMOTE_TRACKING_REF` compatibility wrapper. Confirm no protected-path matching, baseline policy hashing, explicit override behavior, `GITHUB_PR_BASE`, release pins, Tool Hub identity trust, generated-artifact logic, or paid-provider policy was weakened.

### Task 3: Merge Base and establish the immutable handoff

- [ ] **Step 1: Verify #495 is current with completed Base main and has no unresolved review blockers**
- [ ] **Step 2: Mark #495 ready and squash-merge only this dedicated PR using the exact green head SHA**
- [ ] **Step 3: Re-read Base main and applicable post-merge push workflows**
- [ ] **Step 4: Hand the exact merged Base SHA to the `urban-legend` migration**

Before touching the urban adapter, compare its adapter-recorded protected baseline through then-current `urban-legend/main` and stop if any protected path changed.

### Task 4: Migrate `urban-legend` to adapter v2 and the merged Base validator

- [ ] **Step 1: Re-read completed `urban-legend/main`, adapter, generated views, and validation workflow**
- [ ] **Step 2: Prove protected paths are unchanged since the adapter-recorded baseline**
- [ ] **Step 3: Create one dedicated urban migration branch/PR; add canonical `project_id: urban-legend`, update exact Base validator pin, and refresh only deterministic generated operating artifacts required by the v2 contract**
- [ ] **Step 4: Run project CI, adversarial diff review, exact-head merge, and post-merge validation**
- [ ] **Step 5: Keep real user-PC Tool Hub/Figma/Godot execution explicitly `NOT_RUN` until observed on the user's machine**
