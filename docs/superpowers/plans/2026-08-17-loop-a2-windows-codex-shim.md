# Loop A2 Windows Codex Shim Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make ChatGPT-authenticated REAL A2 login and Codex exec use one safe Windows npm-shim command contract.

**Architecture:** Add a focused Loop A2 command-resolution module. Both `provider_gate.py` and `codex_cli_transport.py` consume it so login and model turns cannot drift. Windows `.cmd/.bat` wrappers use exact `COMSPEC` with `shell=False`; non-Windows/native executables remain direct.

**Tech Stack:** Python 3.12, `subprocess`, `pathlib`, `shutil`, unittest, GitHub Actions Windows 2025/Ubuntu 24.04.

## Global Constraints

- `paid_openai_api: FORBIDDEN`
- `api_key_fallback: FORBIDDEN`
- `primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI`
- Blacksmith authority/product scope unchanged.
- `a3_auto_merge: DISABLED`
- `scheduler: NOT_CONFIGURED`
- Successful REAL burn-in count remains 0 until a live `WAITING_INTEGRATION` receipt exists.
- Never use `shell=True`.

---

### Task 1: Reproduce Windows npm-shim failure

**Files:**
- Create: `tools/loop-a2-local-executor/tests/test_windows_codex_npm_shim.py`

**Interfaces:**
- Consumes: `subscription_codex_cli_gate()` and `CodexCliProcess.invoke()`.
- Produces: Windows functional regression evidence for login and actual exec.

- [ ] **Step 1: Write the failing login test**

Create a temporary `%APPDATA%/npm/codex.cmd` that prints exactly `Logged in using ChatGPT` for `login status`, temporarily prepend its directory to `PATH`, and call the real `subscription_codex_cli_gate()` without a fake runner. Skip only when `os.name != "nt"`.

- [ ] **Step 2: Write the failing exec test**

Use a temporary `codex.cmd` that scans argv for `--output-last-message`, writes `{"ok":true}` to that exact path, and exits 0. Call `CodexCliProcess.invoke()` with a minimal strict object schema and assert it returns the JSON text.

- [ ] **Step 3: Verify RED**

Run the Local Executor PR workflow on the test-only head. Expected Windows result: the new npm-shim tests fail because current provider code directly invokes hard-coded `codex`; existing Local Executor tests remain green. Ubuntu skips the two Windows functional tests and remains green.

- [ ] **Step 4: Commit RED evidence**

Commit only the new test file.

---

### Task 2: Add one shared safe Codex command resolver

**Files:**
- Create: `tools/loop_a2_runtime/codex_cli_command.py`
- Modify: `tools/loop_a2_runtime/provider_gate.py`
- Modify: `tools/loop_a2_runtime/codex_cli_transport.py`
- Test: `tests/test_loop_a2_subscription_gate.py`
- Test: `tests/test_loop_a2_codex_cli_transport.py`
- Test: `tools/loop-a2-local-executor/tests/test_windows_codex_npm_shim.py`

**Interfaces:**
- Produces: `build_codex_command(arguments: tuple[str, ...], *, environment: Mapping[str, str] | None = None) -> list[str]`.
- Consumers: subscription login gate and `CodexCliProcess.invoke()`.

- [ ] **Step 1: Implement resolver minimally**

The resolver must preserve direct `['codex', ...]` on non-Windows. On Windows it must resolve the standard `%APPDATA%/npm/codex.cmd`, then native `codex.exe`/`codex.com`, then PATH `codex.cmd`/`codex.bat`. Native launchers return `[resolved, *arguments]`; wrappers return `[COMSPEC, '/d', '/s', '/c', 'call', resolved, *arguments]`. Reject missing launcher/COMSPEC and cmd metacharacters `&|<>^()%!` in wrapper path or arguments.

- [ ] **Step 2: Use resolver in login gate**

Replace hard-coded `["codex", "login", "status"]` with `build_codex_command(("login", "status"))`. Preserve UTF-8 decoding, timeout, `check=False`, `shell=False`, and existing public gate result codes.

- [ ] **Step 3: Use resolver in actual Codex exec**

Build the existing strict Codex argument list without the leading hard-coded `codex`, then pass it through the same resolver. Preserve the temporary cwd, stdin prompt, sanitized environment, `shell=False`, output schema/file contract, output budget, and secret-echo guard.

- [ ] **Step 4: Verify GREEN**

Run Local Executor Windows/Ubuntu and Runtime Foundation. Expected: Windows npm-shim login and exec tests pass; Ubuntu direct-command unit contracts remain green.

---

### Task 3: Exact-head verification and integration

**Files:**
- No new production files unless a verification-only contract gap is discovered through RED first.

**Interfaces:**
- Consumes: final feature head.
- Produces: merge/postmerge evidence and live-ready main SHA.

- [ ] **Step 1: Run exact-head gates**

Require success for Local Executor Windows/Ubuntu, Runtime Foundation, Base-v9/adversarial, Dependency Review, and GPO final `ci-gate`.

- [ ] **Step 2: Reconcile current main and open PRs**

Re-read current completed `main`, verify same-goal open PR overlap, and keep unrelated open/draft PRs read-only. If `main` moved, copy the final material delta onto a clean integration branch based on the new completed main.

- [ ] **Step 3: Merge only the validated integration PR**

Use expected-head squash merge after review threads/submitted review blockers are zero.

- [ ] **Step 4: Postmerge verification**

On the merged SHA, require Local Executor Windows/Ubuntu, Runtime Foundation, Base-v9/adversarial, and GPO final `ci-gate` success. Confirm Issue #465 closes completed.

- [ ] **Step 5: Live retry gate**

Refresh the existing user-PC v4 from merged main, require `LOCAL_EXECUTOR_READY`, freshly re-read Base/Blacksmith SHA and empty queue, then retry exactly one `BS_A2_BURNIN_001`. Count Burn-in #1 only if the REAL receipt state is `WAITING_INTEGRATION` with A3 disabled and Scheduler not configured.
