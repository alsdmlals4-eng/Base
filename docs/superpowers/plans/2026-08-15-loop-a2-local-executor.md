# Loop A2 Unattended Local Executor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone, no-terminal-capable Windows local executor that consumes exact-authority GitHub jobs and runs the merged subscription-native REAL Loop A2 path without API billing or user-worktree mutation.

**Architecture:** A strict issue-job parser and `gh` control-plane adapter feed a managed repository/runtime layer. The executor pins Base runtime and project authority SHAs, verifies the preloaded digest-pinned Docker image, then invokes the exact Base `tools/loop_a2.py` process with host-derived argv only. Receipts are validated/sanitized before publication. Open Tool Hub PRs remain untouched; a later thin UI adapter may consume this package after those PRs finish.

**Tech Stack:** Python 3.12 standard library, Git/GitHub CLI subprocesses, existing Loop A2 CLI, Docker local image inspection, `unittest`, GitHub Actions Windows/Ubuntu.

## Global Constraints

- Separately billed OpenAI API calls are forbidden.
- `OPENAI_API_KEY` fallback is forbidden.
- Do not modify open/draft PRs #369, #373, #376, #384, #386, #394.
- No arbitrary argv, shell, environment, local path, model prompt, merge command, or product scope is accepted from queue jobs.
- Exact queue author, Base runtime SHA, project authority SHA, Capsule path, and run ID are required.
- User project working trees are never reset/restored/cleaned/staged/rewritten.
- A3 remains `DISABLED`; Scheduler remains `NOT_CONFIGURED`; automatic product package selection remains `FORBIDDEN`.
- The reviewed Docker test image is `python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65`; work execution never pulls.
- CI must not claim a real local ChatGPT Codex call.

---

### Task 1: Strict local-job contract

**Files:**
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/job.py`
- Create: `tools/loop-a2-local-executor/tests/test_job.py`
- Create: `tools/loop-a2-local-executor/pyproject.toml`
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/__init__.py`

**Interfaces:**
- Produces: `LocalA2Job.from_issue(issue: Mapping[str, object], *, trusted_author: str, required_label: str) -> LocalA2Job`
- Produces immutable fields: `issue_number`, `target_repository`, `base_runtime_sha`, `authority_sha`, `capsule`, `run_id`, `provider`.

- [ ] Write failing tests requiring exact owner/label, strict fenced JSON, exact key set, REAL-only provider, canonical `owner/name`, normalized relative Capsule JSON path, bounded run id, and rejection of executable/local-path/secret keys.
- [ ] Run `python -m unittest tools/loop-a2-local-executor/tests/test_job.py -v` and observe RED because the package does not exist.
- [ ] Implement the minimal dataclass/parser and stable `JobContractError(code)` errors.
- [ ] Re-run focused tests and require GREEN.
- [ ] Commit.

### Task 2: GitHub queue adapter and receipt sanitization

**Files:**
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/control_plane.py`
- Create: `tools/loop-a2-local-executor/tests/test_control_plane.py`

**Interfaces:**
- Produces: `GhControlPlane.list_open_jobs() -> tuple[dict[str, object], ...]`
- Produces: `GhControlPlane.publish_terminal(issue_number: int, receipt: Mapping[str, object], *, close: bool) -> None`
- Produces: `sanitize_public_receipt(...) -> dict[str, object]`.

- [ ] Write RED tests proving argv-only `gh`, bounded output, exact control repo, no shell, secret-stripped child env, and sanitized receipts without absolute paths/raw stdout/raw stderr/token/key/reasoning fields.
- [ ] Run focused tests and observe RED.
- [ ] Implement minimal `gh auth status`, `gh issue list --json`, `gh issue comment`, and `gh issue close` adapter with injected process runner for tests.
- [ ] Re-run and require GREEN.
- [ ] Commit.

### Task 3: Managed exact-SHA repository layer

**Files:**
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/repositories.py`
- Create: `tools/loop-a2-local-executor/tests/test_repositories.py`

**Interfaces:**
- Produces: `ManagedRepositoryStore.ensure_repo(repository: str) -> Path`
- Produces: `ManagedRepositoryStore.exact_worktree(repository: str, sha: str, role: str)` context manager.

- [ ] Write RED tests with disposable Git repositories proving clone/reuse exact-origin verification, wrong-origin fail-close, exact SHA required, detached worktree creation/removal, path containment, and no mutation of a separate user checkout fixture.
- [ ] Run focused tests and observe RED.
- [ ] Implement argv-only Git operations and executor-owned state-root containment. Do not use reset/restore/clean.
- [ ] Re-run and require GREEN.
- [ ] Commit.

### Task 4: Docker boundary preflight and REAL A2 invocation

**Files:**
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/runtime.py`
- Create: `tools/loop-a2-local-executor/tests/test_runtime.py`

**Interfaces:**
- Produces: `LocalA2Runtime.execute(job: LocalA2Job) -> dict[str, object]`.
- Consumes exact Base/project worktrees from Task 3.

- [ ] Write RED tests proving only the reviewed image reference is inspected, no pull occurs during execution, exact `sha256` image ID is required, Capsule `source_main_sha` becomes `--observed-main-sha`, and generated A2 argv has no job-supplied extension.
- [ ] Require child env to omit `OPENAI_API_KEY`, `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`, `OPENAI_BASE_URL`, `GITHUB_TOKEN`, and `GH_TOKEN` while retaining only bounded system/path/temp values needed to find authenticated local CLIs.
- [ ] Require successful output to be bounded JSON with `state=WAITING_INTEGRATION`, `provider_mode=REAL`, `a3_auto_merge=DISABLED`, `scheduler=NOT_CONFIGURED`, matching project/run/package/SHA identity.
- [ ] Run focused tests and observe RED.
- [ ] Implement minimal Docker inspect + exact Base `tools/loop_a2.py run` invocation.
- [ ] Re-run and require GREEN.
- [ ] Commit.

### Task 5: One-job executor, daemon, and no-console Windows entrypoint

**Files:**
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/service.py`
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/cli.py`
- Create: `tools/loop-a2-local-executor/src/loop_a2_local_executor/windows_entry.pyw`
- Create: `tools/loop-a2-local-executor/tests/test_service.py`
- Create: `tools/loop-a2-local-executor/tests/test_entrypoint.py`

**Interfaces:**
- `preflight`: non-secret readiness classification only.
- `once`: process at most one eligible open job.
- `daemon --poll-seconds N`: `N >= 15`, sequential execution only.

- [ ] Write RED tests proving one-at-a-time processing, malformed/untrusted jobs skipped without execution, blocked jobs receive terminal sanitized receipt, successful jobs close only after receipt publication, no concurrent duplicate claim in one process, bounded poll interval, and `.pyw` delegates without PowerShell/shell use.
- [ ] Run focused tests and observe RED.
- [ ] Implement minimal service and CLI.
- [ ] Re-run and require GREEN.
- [ ] Commit.

### Task 6: Permanent CI, docs, and installation boundary

**Files:**
- Create: `.github/workflows/validate-loop-a2-local-executor.yml`
- Create: `docs/LOOP_A2_LOCAL_EXECUTOR.md`
- Create: `docs/evidence/2026-08-15-loop-a2-local-executor.md`
- Modify only if required by existing routing tests: repository documentation/router files that own tool discovery; do not touch open Tool Hub PR paths.

- [ ] Add Ubuntu and Windows Python 3.12 focused tests for the new standalone package.
- [ ] Document queue issue format, `preflight/once/daemon`, managed state boundary, no-paid-API policy, reviewed Docker image preload requirement, and `.pyw` no-console entrypoint.
- [ ] Explicitly state that Windows startup registration and real local Codex execution are `NOT_RUN` until performed on the user's PC.
- [ ] Run focused workflow on exact head and require GREEN.
- [ ] Commit.

### Task 7: Adversarial review, exact-head gates, merge, and postmerge

- [ ] Attack issue-author spoofing, label spoofing, JSON/Markdown injection, repo/path traversal, argv injection, malicious git config/hooks, symlink/reparse escape, wrong-origin reuse, stale SHA, race between fetch/worktree creation, Docker tag drift, secret/env leakage, stdout/receipt injection, duplicate job execution, partial GitHub publication, false-success classification, accidental API fallback, A3/Scheduler activation, and user-worktree mutation.
- [ ] Apply only validated in-scope fixes and re-run regressions.
- [ ] Recheck all same-goal/open PRs; leave #369/#373/#376/#384/#386/#394 untouched.
- [ ] Require focused local-executor CI, Base v9/adversarial, Game Project Operating System, and Dependency Review when emitted on the exact PR head; unresolved review threads must be zero.
- [ ] Squash merge with expected-head protection.
- [ ] Read merged main and postmerge workflow results back before claiming implementation complete.
- [ ] Close issue #397 after durable postmerge evidence.

## Post-merge next slice

After this package is merged and validated, create a Blacksmith operations-only/test-only burn-in Package on current Blacksmith main that does not select a product feature, Planning change, Visual change, Task3, or protected product scope. Then the user's PC can execute local smoke and three consecutive REAL A2 burn-in jobs through this bridge. If actual local installation/auth/Docker state is unavailable, report the specific local preflight blocker rather than fabricating a run.
