# Dual CI Validation Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the existing GitHub Actions `ci-gate` as the normal Required Check and add a fail-closed local fallback that can publish the same `ci-gate` commit status only when Actions failed to create any `ci-gate` Check Run for the current PR SHA.

**Architecture:** Reuse `tools/run_local_validation.py` for the actual local test contract and add one bounded orchestration tool that verifies PR/base/SHA/worktree state, detects `ci-gate` Check Run collisions before and after validation, and publishes a commit status through `gh api`. Synchronize the existing CI-cost policy and validation Skill; keep the current Ruleset and Required Check name unchanged.

**Tech Stack:** Python 3.12 standard library, `unittest`, local `git`, GitHub CLI `gh`, GitHub REST API, existing GitHub Actions YAML and Base governance documents.

## Global Constraints

- Baseline is `main@4f98f968a377f7b6a11aafa4fc94d11bddbebedc`.
- Work on `agent/dual-validation-gate`; never implement directly on `main`.
- Runtime modes are exactly `REMOTE_CI` and `LOCAL_FALLBACK`; an automatic selector is routing logic, not a third mode.
- `REMOTE_CI` remains the default for public repositories; zero paid budget is not a fallback trigger for standard GitHub-hosted runners.
- Preserve the existing Required Check context `ci-gate` and the active `solo-main-safety` Ruleset; do not add bypass actors or disable strict required-status policy.
- `LOCAL_FALLBACK` is allowed only when the current PR head and current test merge commit have no `ci-gate` Check Run.
- A failed/cancelled/queued/in-progress `ci-gate` Check Run is not fallback-eligible. Fix or resume remote CI instead.
- `LOCAL_FALLBACK` must fail closed on dirty worktree, stale base, SHA mismatch/drift, failed local validation, unavailable GitHub API, or a `ci-gate` Check Run appearing during validation.
- Reuse `tools/run_local_validation.py`; do not duplicate its command matrix or temporary-directory implementation.
- No new broad Skill, Mode, Schema, Ruleset, or Required Check identity.
- Use TDD: new executable behavior must be observed failing before production code is added.
- Do not modify released compatibility lock files, Godot runtime code, project repositories, Google Sheets, assets, or PR #200.

---

### Task 1: Specify fallback behavior with failing tests

**Files:**
- Create: `tests/test_local_ci_fallback.py`

**Interfaces:**
- Consumes: future `tools.run_local_ci_fallback` module.
- Produces: executable acceptance tests for exact SHA, clean/up-to-date git state, check-run collision refusal, local-validation propagation, and `ci-gate` status publication.

- [ ] **Step 1: Add integration-style tests using temporary git repositories and a fake `gh` executable**

The test module must create a temporary repository with `main`, a feature branch, and an `origin` remote that points to a local bare repository. The fake `gh` executable must read request/response fixtures from environment variables and append every invocation to a JSON-lines log so assertions cover real command boundaries rather than Python mocks.

Required tests:

```python
def test_refuses_when_worktree_is_dirty(): ...
def test_refuses_when_local_head_differs_from_pr_head(): ...
def test_refuses_when_base_is_not_ancestor_of_head(): ...
def test_refuses_when_ci_gate_check_exists_on_head(): ...
def test_refuses_when_ci_gate_check_exists_on_test_merge_commit(): ...
def test_validation_failure_never_publishes_success_status(): ...
def test_ci_gate_appearing_after_validation_prevents_status_publish(): ...
def test_success_publishes_ci_gate_for_exact_head_sha(): ...
```

For the success case, the fake GitHub API responses must describe:

```json
{"state":"open","head":{"sha":"<local-head>"},"base":{"ref":"main"},"merge_commit_sha":"<merge-sha>"}
```

and both pre/post check-run queries must return:

```json
{"check_runs":[]}
```

The fake local validator command must exit `0`. Assert that the final `gh api --method POST repos/alsdmlals4-eng/Base/statuses/<head-sha>` invocation contains `state=success` and `context=ci-gate`.

- [ ] **Step 2: Commit the tests before adding production code**

Commit only `tests/test_local_ci_fallback.py` with:

```text
test: specify local CI fallback gate
```

- [ ] **Step 3: Run the focused test in GitHub Actions and verify RED**

Open/update the draft PR and let the current public-repository Actions workflow run against the test-only commit.

Expected: the focused/local test fails because `tools/run_local_ci_fallback.py` does not exist. Record the failed run/check as RED evidence before implementing the tool.

### Task 2: Implement the bounded local fallback tool

**Files:**
- Create: `tools/run_local_ci_fallback.py`
- Test: `tests/test_local_ci_fallback.py`

**Interfaces:**
- CLI:

```text
python tools/run_local_ci_fallback.py \
  --repo OWNER/REPO \
  --pr NUMBER \
  --trusted-history-commit SHA \
  [--base main] \
  [--python PATH]
```

- Module functions:

```python
@dataclass(frozen=True)
class PullRequestState:
    head_sha: str
    base_ref: str
    merge_commit_sha: str | None


def read_pull_request(repo: str, pr: int, *, env: Mapping[str, str] | None = None) -> PullRequestState: ...
def ci_gate_check_exists(repo: str, sha: str, *, env: Mapping[str, str] | None = None) -> bool: ...
def assert_clean_exact_head(root: Path, expected_head: str) -> None: ...
def assert_base_is_ancestor(root: Path, base: str) -> None: ...
def publish_success_status(repo: str, sha: str, *, env: Mapping[str, str] | None = None) -> None: ...
def run_local_fallback(root: Path, repo: str, pr: int, base: str, trusted_history_commit: str, python: str, *, env: Mapping[str, str] | None = None) -> int: ...
```

- [ ] **Step 1: Implement command helpers and fail-closed parsing**

Use `subprocess.run(..., capture_output=True, text=True, check=False)` and raise a descriptive `RuntimeError` for non-zero `git`/`gh` preflight calls. Parse `gh api` JSON with the standard-library `json` module only.

- [ ] **Step 2: Implement preflight in this exact order**

```text
gh auth status
gh api repos/<repo>/pulls/<pr>
validate PR open + base ref
git rev-parse HEAD
require local HEAD == PR head SHA
git status --porcelain
require clean
git fetch origin <base>
git merge-base --is-ancestor origin/<base> HEAD
query head check-runs
query merge_commit_sha check-runs when present
require no ci-gate Check Run
```

Any existing `ci-gate` Check Run, regardless of conclusion/status, must reject fallback.

- [ ] **Step 3: Reuse the existing local validator**

Execute exactly:

```text
<python> tools/run_local_validation.py --trusted-history-commit <trusted-history-commit>
```

Propagate a non-zero exit without publishing any commit status.

- [ ] **Step 4: Recheck race-sensitive state after validation**

Repeat:

```text
git rev-parse HEAD == original head
git status --porcelain is empty
PR head SHA still equals original head
head has no ci-gate Check Run
current merge_commit_sha (if present) has no ci-gate Check Run
```

If any value changed, return non-zero and do not publish.

- [ ] **Step 5: Publish only the final success status**

Use:

```text
gh api --method POST repos/<repo>/statuses/<head-sha> \
  -f state=success \
  -f context=ci-gate \
  -f description=LOCAL_FALLBACK validated exact head SHA
```

Print:

```text
LOCAL FALLBACK CI GATE: PASS
mode: LOCAL_FALLBACK
head_sha: <sha>
required_context: ci-gate
```

- [ ] **Step 6: Run the focused tests and verify GREEN**

Run:

```text
python -m unittest tests.test_local_ci_fallback -v
```

Expected: all fallback tests PASS.

- [ ] **Step 7: Commit Task 2**

Commit `tools/run_local_ci_fallback.py` with:

```text
feat: add fail-closed local CI fallback
```

### Task 3: Wire fallback code into existing validation and operating policy

**Files:**
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `tests/test_ci_workflow_cost_policy.py`
- Modify: `docs/CI_EXECUTION_COST_POLICY.md`
- Modify: `docs/GITHUB_PRO_OPERATING_POLICY.md`
- Modify: `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`

**Interfaces:**
- Consumes: `tools/run_local_ci_fallback.py`, existing `ci-gate`, existing `run_local_validation.py`.
- Produces: two-mode operating contract and CI self-validation coverage for the fallback tool.

- [ ] **Step 1: Add failing policy/workflow assertions**

Extend `tests/test_ci_workflow_cost_policy.py` so the repository must contain all of these literals or equivalent exact assertions:

```text
REMOTE_CI
LOCAL_FALLBACK
tools/run_local_ci_fallback.py
tests/test_local_ci_fallback.py
ci-gate Check Run
public
standard GitHub-hosted
```

Also assert the policy rejects fallback for test/workflow failure and says an existing `ci-gate` Check Run blocks fallback.

Run:

```text
python -m unittest tests.test_ci_workflow_cost_policy -v
```

Expected: FAIL before the policy/workflow changes.

- [ ] **Step 2: Update canonical CI self-validation**

In `.github/workflows/validate-game-project-operating-system.yml`:

- classify `tools/run_local_ci_fallback.py` and `tests/test_local_ci_fallback.py` as code/tooling changes at the same risk tier as `run_local_validation.py`.
- add both files to the existing Python syntax compilation list.
- include `tests.test_local_ci_fallback` wherever the local-validation regression suite is explicitly enumerated.
- do not change the `ci-gate` job name, needs graph, evaluator behavior, event triggers, matrix policy, or Ruleset contract.

- [ ] **Step 3: Replace the Actions-unavailable policy with the two-mode contract**

`docs/CI_EXECUTION_COST_POLICY.md` must state:

```text
REMOTE_CI = default
LOCAL_FALLBACK = infrastructure-only fallback
```

It must distinguish:

```text
Actions can create ci-gate -> REMOTE_CI only
ci-gate exists but failed/cancelled/pending -> REMOTE_CI failure/block; no fallback
no ci-gate Check Run can be created -> LOCAL_FALLBACK may run if all exact-SHA safeguards pass
local fallback cannot reproduce required evidence -> BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED
```

- [ ] **Step 4: Synchronize GitHub operating/budget documentation**

`docs/GITHUB_PRO_OPERATING_POLICY.md` and `templates/project-operations/github/GITHUB_USAGE_BUDGET.md` must say that current public repositories use standard GitHub-hosted runners without treating paid-minute budget as the fallback selector. Remove stale examples that label current game repositories as private. Retain warnings that larger/GPU runners and future private repositories can have billing implications.

- [ ] **Step 5: Absorb routing into the existing validation Skill**

In `skills/reviewing-and-validating-project-changes/SKILL.md`, update `ci-cost-optimization` so agents:

```text
1. default to REMOTE_CI;
2. inspect actual Actions/check state;
3. never use fallback to replace a failed test/workflow;
4. when no ci-gate Check Run exists because Actions infrastructure is unavailable, run tools/run_local_ci_fallback.py;
5. preserve BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED when fallback preconditions cannot be satisfied.
```

Do not add another Skill or Mode entry.

- [ ] **Step 6: Run focused policy tests and verify GREEN**

Run:

```text
python -m unittest tests.test_local_ci_fallback tests.test_ci_workflow_cost_policy tests.test_local_validation tests.test_ci_required_gate_topology -v
```

Expected: PASS.

- [ ] **Step 7: Commit Task 3**

Commit the synchronized workflow/policy/Skill changes with:

```text
refactor: route CI through remote and local fallback modes
```

### Task 4: Repository-wide adversarial verification and PR handoff

**Files:**
- Modify only if evidence finds a live stale consumer: active docs/templates/tests referencing the old unconditional Actions-unavailable contract.

**Interfaces:**
- Consumes: complete Task 1-3 diff.
- Produces: final evidence, exact-head PR, and no stale active references.

- [ ] **Step 1: Search the tracked repository for affected references**

Search active files for:

```text
BLOCKED_BY_GITHUB_ACTIONS
UNVERIFIED
ci-gate
GITHUB_USAGE_BUDGET
private repository
Actions unavailable
```

Classify hits as active consumer, historical plan/changelog/case, or generated/legacy evidence. Update active consumers only.

- [ ] **Step 2: Run repository-owned validation**

Run:

```text
python -m unittest discover -s tests -v
python tools/check_ci_required_gate_topology.py
python tools/build_base_v9_artifacts.py --check
python tools/check_base_v9_integrity.py --trusted-history-commit 4f98f968a377f7b6a11aafa4fc94d11bddbebedc
python tools/check_skill_system_coverage.py
git diff --check
git fsck --strict
```

If the local environment cannot execute these, use the public-repository GitHub Actions run for the exact PR head as the authoritative execution evidence and report local commands as `NOT_RUN`, never as passed.

- [ ] **Step 3: Run adversarial review**

Explicitly attack these failure modes:

```text
fallback used after a genuine test failure
same-name Check/status collision
stale local branch satisfying strict required checks
status posted to a different SHA than validated
Actions recovering during local validation
Ruleset/Required Check drift
public/private billing assumption drift
new broad Skill or duplicate validator accidentally introduced
```

Any unresolved P0/P1 finding blocks completion.

- [ ] **Step 4: Verify the exact PR head in GitHub**

Confirm:

```text
PR head SHA == final branch SHA
ci-gate == success on that exact PR validation target
no unresolved review thread
no unexpected changed file
```

- [ ] **Step 5: Leave the PR as Draft unless explicitly asked to merge**

PR body must include:

```text
what changed
why public-repository Actions remain default
LOCAL_FALLBACK eligibility and fail-closed conditions
TDD RED evidence
GREEN/full validation evidence
Ruleset remains ci-gate
PR #200 compatibility
rollback: remove fallback tool + restore prior policy/Skill references
```

Do not merge automatically unless the user separately authorizes merge.
