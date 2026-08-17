# Protected Baseline Ancestry Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permit a stable historical protected baseline for a canonical project adapter using `REMOTE_TRACKING_REF` when that baseline remains an ancestor of the current external authority, without weakening protected-path change detection or the stricter first-migration boundary.

**Architecture:** The large legacy `project_operating_contract.py` remains byte-stable. The already-reviewed `base_release_index.py` compatibility installer wraps only `REMOTE_TRACKING_REF` baselines whose `policy_source_type` is `CANONICAL_ADAPTER_SOURCE`. `FIRST_MIGRATION_LEGACY_SOURCE`, explicit `--protected-base`, and `GITHUB_PR_BASE` delegate unchanged to the legacy implementation. Official `check_project_operating_contract.py` installs this compatibility layer before validation, and both Linux and Windows Tool Hub identity validators package `base_release_index.py` into their reviewed validator runtime. On successful canonical ancestry authentication the wrapper returns the historical adapter baseline, not the current authority commit, so `_protected_policy_errors()` still diffs the complete historical-baseline→working-tree interval.

**Tech Stack:** Python 3.12, `unittest`, temporary Git repositories through argv-only `subprocess`, existing Base compatibility installer and project operating-contract helpers, GitHub Actions.

## Global Constraints

- `CANONICAL_ADAPTER_SOURCE + REMOTE_TRACKING_REF` baseline must be equal to or an ancestor of the resolved authority commit.
- `FIRST_MIGRATION_LEGACY_SOURCE + REMOTE_TRACKING_REF` retains the existing exact-authority rule.
- A missing or non-ancestor canonical adapter baseline fails closed.
- Successful canonical ancestry authentication returns the adapter-recorded historical baseline; returning the resolved authority commit is forbidden.
- Protected-path changes since the historical baseline remain fail-closed through `_protected_policy_errors()`.
- `GITHUB_PR_BASE` semantics and explicit trusted `--protected-base` semantics remain unchanged.
- The compatibility layer uses existing `_resolve_commit()`, `_commit_exists()`, and `_is_ancestor()` helpers; no shell-string Git execution.
- Linux and Windows Tool Hub validator bundles must continue to include and authenticate `base_release_index.py`.
- Do not modify unrelated open/draft/ready PRs.
- Do not add paid services, subscriptions, or new network dependencies.
- This Base PR completes before the `urban-legend` adapter-v2 migration begins.

---

### Task 1: Lock the ancestry and historical-diff contract with failing tests

**Files:**
- Create: `tests/test_project_protected_baseline_authority.py`
- Modify: `tests/test_local_validation.py`

- [x] **Step 1: Reproduce the original defect before production modification**

PR #495 test-only head `a68c53c05c4e8f5748e498a67cad2f149e32ce93` reproduced the exact-equality defect in the dependency-complete Ubuntu contract gate.

- [x] **Step 2: Reject invalid RED evidence from the lightweight docs environment**

The initial placement also caused `ModuleNotFoundError: jsonschema` in `docs-validation`; that environment failure was explicitly rejected as RED evidence.

- [x] **Step 3: Move focused coverage to the Ubuntu-only local-validation aggregate**

The focused TestCase is imported from `tests/test_local_validation.py`, already executed by `ubuntu-contract` but not by the lightweight docs gate.

- [x] **Step 4: Rebase the test-only state onto completed Base main and verify clean RED**

Test-only head `6ea6839fbb8168e58f347ed1a3c9cfefe1f5fbf7` was based on Base main `2b8856054573f1a06297ac8e65f5ca009fa2daef`. `docs-validation` passed; `ubuntu-contract` failed only on the five intended new ancestry/historical-diff cases while equal authority, explicit override, and `GITHUB_PR_BASE` remained green.

### Task 2: Install the minimum fail-closed canonical ancestry rule

**Files:**
- Modify: `tools/base_release_index.py`
- Test: `tests/test_project_protected_baseline_authority.py`
- Existing compatibility coverage: `tests/test_v9_1_project_operating_contract.py`

- [x] **Step 1: Add one idempotent compatibility installer**

The first implementation applied ancestry to every remote baseline. Base v9.1 regression exposed that this would also relax `FIRST_MIGRATION_LEGACY_SOURCE`. The implementation was narrowed so only canonical adapter baselines receive ancestry authentication; legacy first-migration baselines retain exact equality. For the canonical branch:

```python
resolved = contract_module._resolve_commit(project_root, authority_ref)
if resolved is None:
    return None, [f"Protected authority ref cannot be resolved to a commit: {authority_ref}"]
if not contract_module._commit_exists(project_root, adapter_commit):
    return None, [f"Protected baseline commit is absent: {adapter_commit}"]
if not contract_module._is_ancestor(project_root, adapter_commit, resolved):
    return None, [
        "External protected authority requires adapter baseline ancestry: "
        f"{adapter_commit} is not an ancestor of {authority_ref} ({resolved})"
    ]
return adapter_commit, []
```

Implementation commits: `66c49c66b274989920f765c2a68cff359287be2e` (initial) and `0736111ec92107b1ba4ad5ecf316240274b96fe0` (canonical-source narrowing).

- [ ] **Step 2: Re-run exact-head focused and aggregate contract coverage**

Expected: canonical historical baseline tests pass, existing first-migration exact-authority tests pass, and historical protected-path changes are still detected.

- [ ] **Step 3: Verify the full PR gate**

Require `Validate Game Project Operating System` `ci-gate`, `Validate Base v9 Operating Contracts`, and every selected required job for the exact PR head to complete successfully.

- [ ] **Step 4: Adversarially inspect the final diff**

Confirm the only production semantic change is the idempotent canonical `REMOTE_TRACKING_REF` compatibility wrapper. Confirm no protected-path matching, policy hashing, first-migration exact-authority behavior, explicit override behavior, `GITHUB_PR_BASE`, release pins, Tool Hub identity trust, generated-artifact logic, or paid-provider policy was weakened.

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
