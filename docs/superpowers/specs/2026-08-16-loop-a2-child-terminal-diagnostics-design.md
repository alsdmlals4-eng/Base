# Loop A2 Child Terminal Diagnostics Design

## Goal

Preserve one safe, machine-readable blocker code when `tools/loop_a2.py` exits before producing a full `LOOP_A2_RUN_RECEIPT`, so a real Local Executor failure no longer collapses every pre-runtime terminal state into generic `A2_EXECUTION_BLOCKED`.

## Context

Live Blacksmith job #447 ran on Base `7958ebfcbd4a23bd04fe360b123c005d8bb66339` and returned generic `A2_EXECUTION_BLOCKED` after #446 had already added full blocked-run receipt diagnostics. Static tracing shows the remaining split: pre-runtime CLI failures emit `{status, code, message}`, while Local Executor trusts only `LOOP_A2_RUN_RECEIPT`.

## Options considered

1. **Parse the existing ad-hoc `{status, code, message}` shape.** Smallest patch, but the shape has no explicit role and could accidentally elevate unrelated JSON.
2. **Recommended: introduce `LOOP_A2_CHILD_TERMINAL`.** Add `schema_version`, explicit `contract_role`, bounded `status`, and stable `code`. Local Executor publishes only the validated code as `a2_child_code`. Raw `message` remains private.
3. **Force every pre-runtime failure into `LOOP_A2_RUN_RECEIPT`.** Strong uniformity, but invalid because some failures occur before a valid RunRequest/package identity exists.

Option 2 is selected.

## Contract

A pre-runtime machine terminal envelope is exactly:

```json
{
  "schema_version": 1,
  "contract_role": "LOOP_A2_CHILD_TERMINAL",
  "status": "BLOCKED_UNVERIFIED",
  "code": "SUBSCRIPTION_CODEX_AUTH_REQUIRED",
  "message": "private human diagnostic"
}
```

Only `code` may cross the Local Executor public boundary, after matching `^[A-Z][A-Z0-9_]{0,127}$`. `message`, stdout/stderr, absolute paths, credentials, prompts, provider payloads, and reasoning never cross.

## Data flow

```text
loop_a2.py pre-runtime failure
→ LOOP_A2_CHILD_TERMINAL stdout
→ LocalA2Runtime nonzero branch
→ validate explicit role/schema/status/code
→ LocalRuntimeError(public_details={a2_child_code})
→ LocalExecutorService allowlist
→ sanitize_public_receipt
→ GitHub job receipt
```

Full `LOOP_A2_RUN_RECEIPT` handling remains unchanged and remains bound to project/run/package/SHA.

## Fail-closed behavior

Invalid JSON, unknown contract role, missing/invalid code, unsupported status, or any full-run identity/package mismatch remains generic `A2_EXECUTION_BLOCKED` with no public details.

## Scope

Modify only:
- `tools/loop_a2.py`
- `tools/loop-a2-local-executor/src/loop_a2_local_executor/runtime.py`
- `tools/loop-a2-local-executor/src/loop_a2_local_executor/service.py`
- `tools/loop-a2-local-executor/src/loop_a2_local_executor/control_plane.py`
- focused regression tests

No Docker resolver, command authority, provider selection, Blacksmith authority, product scope, A3, Scheduler, or paid API behavior changes.

## Acceptance

- RED proves current main discards a valid child-terminal stable code.
- GREEN preserves only `a2_child_code` for a valid terminal envelope.
- Invalid/unknown envelopes remain generic.
- Existing full blocked run receipt diagnostics still pass.
- Local Executor Windows+Ubuntu, provider/runtime, Base-v9/adversarial, and GPO gates pass.
- After merged-main refresh, Blacksmith `BS_A2_BURNIN_001` is retried; only that live retry identifies the underlying blocker.
