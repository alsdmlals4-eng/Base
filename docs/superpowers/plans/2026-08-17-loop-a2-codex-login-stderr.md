# Loop A2 Codex Login Stderr Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the REAL A2 subscription gate accept the official stderr-only ChatGPT login status while remaining fail-closed for all ambiguous output.

**Architecture:** Keep the existing process invocation and Windows resolver unchanged. Change only login-status interpretation: treat stdout/stderr as two separate bounded channels and accept the exact ChatGPT marker on one channel only.

**Tech Stack:** Python 3.12, subprocess, unittest, GitHub Actions Windows 2025/Ubuntu 24.04.

## Global Constraints

- `paid_openai_api: FORBIDDEN`
- `api_key_fallback: FORBIDDEN`
- `primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI`
- Never use `shell=True`.
- Blacksmith authority/product scope unchanged.
- `a3_auto_merge: DISABLED`
- `scheduler: NOT_CONFIGURED`
- Successful REAL burn-in count remains 0 until a live `WAITING_INTEGRATION` receipt exists.

---

### Task 1: Reproduce official stderr behavior

**Files:**
- Modify: `tests/test_loop_a2_subscription_gate.py`
- Modify: `tools/loop-a2-local-executor/tests/test_windows_codex_npm_shim.py`

- [ ] Extend the injected runner to expose stderr.
- [ ] Add a test where stdout is empty and stderr is exactly `Logged in using ChatGPT\n`; expected current result is not READY.
- [ ] Make the Windows temporary `codex.cmd login status` echo the marker to stderr; expected current Windows functional test fails.
- [ ] Add fail-closed tests for both streams populated and extra diagnostics.
- [ ] Run exact test-only head and record RED.

### Task 2: Minimal login-status interpretation fix

**Files:**
- Modify: `tools/loop_a2_runtime/provider_gate.py`

- [ ] Strip stdout/stderr independently.
- [ ] READY only when `(stdout == marker and stderr == '')` or `(stderr == marker and stdout == '')`.
- [ ] Preserve all process invocation, UTF-8, timeout, resolver, `shell=False`, and existing public error codes.
- [ ] Run focused tests and full Local Executor Windows/Ubuntu; require GREEN.

### Task 3: Exact-head and postmerge verification

- [ ] Require Runtime Foundation, OpenAI transport, Base-v9/adversarial, and GPO `ci-gate` success on exact head.
- [ ] Re-read current completed main and open-PR overlap; if main moved, copy final material delta to a clean integration branch.
- [ ] Merge only validated head with expected-head protection and zero review blockers.
- [ ] Require the same postmerge gates on the merged SHA and close #469 completed.
- [ ] Refresh user-PC v4, then retry one exact Blacksmith `BS_A2_BURNIN_001`; increment burn-in count only on `PASS/A2_WAITING_INTEGRATION`.
