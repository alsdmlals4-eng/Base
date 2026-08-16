# Loop A2 Codex Login Stderr Gate Design

## Goal

Accept the official Codex CLI ChatGPT login-status output when it is emitted on stderr, without broadening the subscription provider gate or exposing raw process output.

## Evidence

- User-PC v4 reports `Codex: READY (ChatGPT)` because the installer captures `codex login status` with stdout and stderr combined.
- REAL A2 job #467 on merged `Base@faff4bfdf6d5cd07d79e8352d1a3f6cd8d957906` returns `SUBSCRIPTION_CODEX_GATE_CLOSED`.
- OpenAI Codex CLI `run_login_status` uses `eprintln!("Logged in using ChatGPT")`, so the canonical status is stderr output.

## Decision

`subscription_codex_cli_gate()` keeps capturing stdout and stderr separately. It returns READY only when the process exits 0 and exactly one stream, after stripping whitespace, equals `Logged in using ChatGPT` while the other stream is empty. This preserves stdout-only compatibility but matches the official stderr behavior.

All other shapes remain fail-closed: API-key status, nonzero exit, additional diagnostics, both streams populated, missing executable, timeout, or execution error. Raw stdout/stderr are never returned or published.

## Invariants

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI
shell_true: FORBIDDEN
blacksmith_authority: UNCHANGED
blacksmith_product_scope: UNCHANGED
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
real_a2_burnin_runs: 0
```

## Verification

- Unit RED/GREEN for official stderr-only status.
- Unit fail-closed tests for dual-stream and extra diagnostics.
- Windows functional `codex.cmd` shim emits login status to stderr.
- Local Executor Windows/Ubuntu, Runtime Foundation, OpenAI transport, Base-v9/adversarial, and GPO final `ci-gate` must pass exact head and postmerge.
