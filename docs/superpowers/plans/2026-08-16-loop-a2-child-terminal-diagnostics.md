# Loop A2 Child Terminal Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve a bounded stable pre-runtime REAL A2 child blocker code through Local Executor without exposing raw child output.

**Architecture:** `tools/loop_a2.py` emits a role-tagged `LOOP_A2_CHILD_TERMINAL` envelope for pre-runtime failures. `LocalA2Runtime` recognizes only that explicit schema/role/status/code shape on nonzero exit, carries `a2_child_code` as a public detail, and existing service/control-plane allowlists publish only that scalar. Full `LOOP_A2_RUN_RECEIPT` diagnostics remain unchanged.

**Tech Stack:** Python 3.12, unittest, existing Local Executor subprocess boundary, GitHub Actions Windows/Ubuntu validation.

## Global Constraints

- Base start SHA: `7958ebfcbd4a23bd04fe360b123c005d8bb66339`.
- Source PR #445 stays read-only; its material is already fully absorbed by #446.
- `paid_openai_api: FORBIDDEN`.
- `api_key_fallback: FORBIDDEN`.
- `a3_auto_merge: DISABLED`.
- `scheduler: NOT_CONFIGURED`.
- Blacksmith product scope remains unchanged.
- Raw stdout/stderr, messages, local paths, credentials, prompts, provider payloads, and reasoning must never enter public receipts.

---

### Task 1: Lock the child-terminal contract with RED tests

**Files:**
- Modify: `tools/loop-a2-local-executor/tests/test_windows_utf8_blocked_receipt_diagnostics.py`
- Create: `tests/test_loop_a2_child_terminal_contract.py`

**Interfaces:**
- Consumes: current `LocalA2Runtime.execute()` nonzero handling and `tools/loop_a2.py::_blocked`.
- Produces: exact tests requiring `LOOP_A2_CHILD_TERMINAL` and `a2_child_code`.

- [ ] Add a runtime test where child stdout is `{"schema_version":1,"contract_role":"LOOP_A2_CHILD_TERMINAL","status":"BLOCKED_UNVERIFIED","code":"SUBSCRIPTION_CODEX_AUTH_REQUIRED","message":"private"}` and assert current main fails to preserve `a2_child_code`.
- [ ] Add negative cases for invalid role, lowercase/oversized code, and invalid status; assert generic `A2_EXECUTION_BLOCKED`.
- [ ] Add CLI contract test that `_blocked()` output contains schema/role/status/code while message remains present only inside child stdout.
- [ ] Run focused tests and record expected RED.

### Task 2: Implement the bounded terminal envelope

**Files:**
- Modify: `tools/loop_a2.py`
- Modify: `tools/loop-a2-local-executor/src/loop_a2_local_executor/runtime.py`
- Modify: `tools/loop-a2-local-executor/src/loop_a2_local_executor/service.py`
- Modify: `tools/loop-a2-local-executor/src/loop_a2_local_executor/control_plane.py`

**Interfaces:**
- Consumes: `LOOP_A2_CHILD_TERMINAL` stdout JSON.
- Produces: `LocalRuntimeError.public_details["a2_child_code"]` and sanitized GitHub receipt field.

- [ ] Change `_blocked()` to emit `schema_version=1` and `contract_role="LOOP_A2_CHILD_TERMINAL"` with the existing bounded `status`, stable `code`, and private `message`.
- [ ] Route the initial contract-construction exception through `_blocked(status="CONTRACT_INVALID", code="A2_CONTRACT_INVALID", ...)` so all pre-runtime failures use the same role-tagged envelope.
- [ ] Add a runtime helper that accepts only schema 1, role `LOOP_A2_CHILD_TERMINAL`, status `CONTRACT_INVALID|BLOCKED_UNVERIFIED`, and code regex `^[A-Z][A-Z0-9_]{0,127}$`; return only `{"a2_child_code": code}`.
- [ ] Keep full `LOOP_A2_RUN_RECEIPT` parsing first-class and unchanged; on nonzero exit combine either full receipt diagnostics or child-terminal code, never raw output.
- [ ] Add `a2_child_code` to service and control-plane public allowlists with the same stable-code regex.
- [ ] Run focused tests and require GREEN.

### Task 3: Regression and exact-head validation

**Files:**
- No new production files.

**Interfaces:**
- Consumes: final branch head.
- Produces: merge evidence and a safe next live retry gate.

- [ ] Run full Local Executor suite on Ubuntu and Windows.
- [ ] Run Loop A2 Runtime Foundation and subscription/Codex transport validation.
- [ ] Run Base-v9 contract + adversarial gate.
- [ ] Run Game Project Operating System required gate.
- [ ] Re-read current `main`; if it moved, copy/reconcile onto latest completed main without modifying source/open owner PRs, then rerun exact-head validation.
- [ ] Merge only the clean integration result with expected-head protection.
- [ ] Run postmerge push validation and read back the merged terminal contract.
- [ ] Refresh user-PC v4, stage and activate a new `BS_A2_BURNIN_001` job, then read `a2_child_code` or successful `WAITING_INTEGRATION` receipt. Do not increment `real_a2_burnin_runs` unless the receipt is PASS.
