# Loop A2 Subscription-Native Codex CLI Transport Evidence

Date: 2026-08-14

## Decision authority

The user explicitly approved the following Universal Loop policy:

```yaml
paid_openai_api: FORBIDDEN
paid_provider_smoke: NOT_PLANNED
primary_real_provider: CHATGPT_AUTHENTICATED_CODEX_CLI
api_key_fallback: FORBIDDEN
```

The former paid-provider decision issue #352 was closed as `not_planned`. No separately billed OpenAI API request was executed and no separately billed API cost was incurred.

Implementation issue: #379  
Implementation PR: #380

## Existing-solution review

The selected path reuses the official Codex CLI rather than creating another model client.

- Codex CLI distinguishes ChatGPT-managed login from API-key login.
- `codex exec` supports non-interactive ephemeral execution, ignored user config/rules, read-only sandboxing, output JSON schema, and final-message capture.
- Codex exposes `shell_tool` as a feature. Current official Codex source maps disabled `ShellTool` to `ConfigShellToolType::Disabled`.
- Official Codex CLI tests demonstrate a strict config override can set `features.shell_tool=false`.

Alternatives considered:

1. Direct OpenAI Responses API: rejected by approved no-separate-billing policy.
2. Local OSS provider through Codex/Ollama/LM Studio: valid optional fallback, but requires a local model/runtime and compatible hardware; deferred from the primary v1 path.
3. Manual ChatGPT copy/paste handoff: rejected as the primary path because it breaks the automation objective.

## Implemented boundary

The active `--provider real` path now requires `codex login status` to report ChatGPT authentication. API-key authentication is rejected and legacy `OPENAI_API_KEY` / approval environment values cannot reopen the paid provider gate.

Each Builder/Critic model turn uses an independent `CodexCliProcess` and invokes Codex using this bounded shape:

```text
codex
  --strict-config
  -c features.shell_tool=false
  exec
  --ephemeral
  --ignore-user-config
  --ignore-rules
  --skip-git-repo-check
  --sandbox read-only
  --output-schema <temporary-schema>
  --output-last-message <temporary-output>
  -
```

The model process runs in an empty temporary directory, not the project worktree. It receives no project directory through `--cd` or `--add-dir`. Shell execution is disabled. The dangerous sandbox-bypass option is not used.

The child environment is allowlisted and excludes provider/GitHub secret variables including `OPENAI_API_KEY`, `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`, `OPENAI_BASE_URL`, `GITHUB_TOKEN`, and `GH_TOKEN`. `CODEX_HOME` may be retained only so the official Codex client can use its own ChatGPT-managed authentication store; the model has no shell tool with which to inspect that store.

The Codex process returns only strict schema-bound JSON. Existing deterministic Base host code remains authoritative for:

- Builder allowed-path and authority-file validation;
- host-side write application;
- actual Git diff attestation;
- isolated worktree ownership/resume;
- deterministic project tests and denied-network test execution;
- Critic requirement/path expansion rejection;
- integration/postmerge gates.

Builder and Critic are separate ephemeral process instances. The Critic receives bounded review material derived from the actual owned Git diff and does not receive the Builder transcript/session state. The existing repair mailbox shares only bounded review feedback required by the current A2 repair protocol.

## TDD evidence

### Provider gate RED

Initial subscription-gate tests were added before production implementation. A2 Runtime Foundation detected the new tests and failed only because `subscription_codex_cli_gate` did not exist. The production gate was then added and the focused regression returned GREEN.

### CLI transport RED

Transport contract tests were added before `codex_cli_transport.py`. A2 Runtime Foundation failed only on the missing new transport module; the subsequent implementation returned the suite to GREEN.

### REAL entrypoint RED

The subscription-native CLI entrypoint tests were added before the `--provider real` wiring. The failures were limited to the missing subscription gate/factory/runtime-root path. Production CLI wiring then returned the suite to GREEN.

### Adversarial shell-isolation RED

After the initial implementation passed, adversarial review identified that `--sandbox read-only` alone still allowed a model-visible shell tool to exist. A test requiring strict `features.shell_tool=false` was added first.

RED evidence:

- test-only head: `be3f0eaeba51956ff2c9dabfc3dbd8e0680f0bf2`
- A2 Runtime Foundation run: `31807908045`
- result: 207 tests, exactly one failure: missing `--strict-config` before `exec`

The production invocation was then changed to the official strict-config form.

GREEN implementation evidence:

- implementation head: `6b6f987c4b38c7de62da4a78fc7e0101150c9033`
- A2 Runtime Foundation: `31808000578` — PASS
- OpenAI Transport regression: `31808000655` — PASS
- Base-v9 Operating Contracts: `31808000703` — PASS
- Game Project Operating System: `31808000612` — required jobs PASS, including Ubuntu contract, docs validation, publication validation, and final CI gate

The Windows platform smoke was skipped by the repository's risk classifier for this change shape; no Windows production-boundary claim is made from that skip.

## Adversarial attack matrix

| Attack | Result |
|---|---|
| Legacy API approval/key silently reopens paid provider | blocked by `PAID_OPENAI_API_FORBIDDEN` |
| API-key-authenticated Codex accepted as subscription path | blocked by exact ChatGPT login gate |
| Parent API/GitHub secret inherited by child | blocked by environment allowlist |
| Project/user Codex config injects authority | blocked by `--ignore-user-config` |
| User/project exec rules inject authority | blocked by `--ignore-rules` |
| Model shell reads local auth/workspace files | blocked by `features.shell_tool=false` |
| Model directly mutates project worktree | no worktree cwd/add-dir; read-only temp process; host applies validated writes |
| Shell argument injection | subprocess argv list with `shell=False` |
| Dangerous sandbox bypass | option is not passed and regression asserts absence |
| Malformed/non-JSON/oversized final output | fail-closed transport error |
| Configured secret echoed in structured output | fail-closed secret-echo check |
| Critic shares Builder hidden session state | separate `--ephemeral` process instance and bounded review payload |
| Critic expands requirements/paths | existing deterministic A2 authority checks remain active |
| False real-provider completion claim | explicitly prohibited by the claim ceiling below |
| A3/Scheduler activation | untouched; remain disabled/not configured |

## Implementation Reality Gate / claim ceiling

The following claims are supported:

```yaml
subscription_cli_transport_code: IMPLEMENTED_AND_DETERMINISTICALLY_VALIDATED
paid_openai_api_policy: FORBIDDEN
api_key_fallback: FORBIDDEN
chatgpt_auth_gate: DETERMINISTICALLY_VALIDATED
builder_critic_process_isolation: DETERMINISTICALLY_VALIDATED_BY_STRUCTURE_AND_TESTS
paid_api_request: NOT_RUN
paid_api_cost: NOT_RUN
real_subscription_model_call: NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED
real_a2_burnin_runs: 0
```

The GitHub Actions environment does not contain the user's ChatGPT-authenticated Codex session. Therefore this PR does **not** claim a real subscription model call, real Builder output, real Critic output, or Blacksmith burn-in completion.

## Remaining external validation

After merge/postmerge validation, the next executable gate is a local smoke on a machine where `codex login status` reports ChatGPT authentication. That smoke requires no separately billed API key or API-cost approval. After it succeeds, Blacksmith real A2 Run #1, #2, and #3 can establish the requested burn-in evidence.

A3 auto-merge remains disabled. Scheduler remains not configured. Automatic product-scope selection remains forbidden.

## Rollback

Revert PR #380 to remove the subscription-native transport implementation. Reverting this implementation does not authorize the separately billed OpenAI API path; reopening that policy would require a new explicit user decision.
