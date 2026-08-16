# Loop A2 Windows Codex Shim Execution Design

## Goal

Make the REAL Loop A2 subscription provider use the same Windows Codex npm-shim execution semantics that already succeed in the v4 installer, without enabling `shell=True`, paid OpenAI API fallback, broader process authority, or any Blacksmith product change.

## Live evidence

- User-PC v4 on `Base@e0a1b1bb577bafe30a27708e8934e9ae89f28e71` reports `Codex: READY (ChatGPT)` and reaches `LOCAL_EXECUTOR_READY`.
- REAL job #464 on `Blacksmith@6b241f28969410de78156c90cc10f33a067426a2` is consumed but returns `SUBSCRIPTION_CODEX_GATE_CLOSED`.
- The installer validates auth through resolved Codex + `ComSpec /d /s /c`.
- `subscription_codex_cli_gate()` and `CodexCliProcess.invoke()` currently execute hard-coded `codex` directly with `shell=False`.

## Design decision

Create one Loop-A2-owned command resolver used by both login-status and actual Codex execution.

On non-Windows, keep the existing direct command shape: `codex ...`.

On Windows:

1. Resolve the usable Codex launcher from the inherited sanitized environment, preferring the standard `%APPDATA%/npm/codex.cmd` npm shim and native `codex.exe`/`codex.com` candidates before PATH fallback.
2. If the resolved launcher is native, execute it directly.
3. If it is `.cmd` or `.bat`, execute it through exact `COMSPEC` using `[/d, /s, /c, call, <exact wrapper>, ...]` while Python still uses `shell=False`.
4. Reject missing launchers, missing command processor, unsafe wrapper paths, or cmd metacharacters in wrapper arguments before process creation.
5. Preserve UTF-8 capture, sanitized environment, timeouts, structured-output limits, ephemeral/read-only Codex flags, disabled web/shell features, and no API-key fallback.

## Approaches considered

### Selected: Loop-A2-owned shared resolver

Pros: fixes both login and exec with one contract; matches the existing Base Windows wrapper pattern; no dependency on publication modules; testable in the Local Executor Windows matrix.

Cons: adds one small runtime module.

### Rejected: fix only `subscription_codex_cli_gate()`

This would make login pass but leave `CodexCliProcess.invoke()` vulnerable to the same Windows npm-shim failure on the next step.

### Rejected: import `publication_v3.safe_executable_command()`

That module has unrelated publication dependencies and would couple the minimal A2 runtime to publication/PDF/image tooling.

## Testing

- Windows-only functional login test creates a temporary `codex.cmd` that emits `Logged in using ChatGPT`; current code must fail before implementation and pass after.
- Windows-only functional exec test creates a temporary `codex.cmd` that writes the requested `--output-last-message` JSON; current code must fail before implementation and pass after.
- Ubuntu retains existing direct `codex` unit behavior.
- Existing provider-gate, Codex transport, Local Executor, Runtime Foundation, Base-v9/adversarial, Dependency Review, and GPO gates must remain green.

## Safety invariants

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI
blacksmith_authority: UNCHANGED
blacksmith_product_scope: UNCHANGED
reviewed_docker_image: UNCHANGED
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
real_a2_burnin_runs: 0
```
