# Loop A2 Subscription-Native Codex CLI Transport Design

## Decision

Universal Loop A2 must not use separately billed OpenAI API calls. The approved provider path is the user's existing ChatGPT-authenticated Codex CLI entitlement. Direct `OPENAI_API_KEY` transport remains fail-closed and is not an automatic fallback.

## Goal

Replace the paid-provider decision gate with a bounded, automatable Codex CLI transport that can run Builder and Critic turns through an existing ChatGPT plan while preserving the current Loop A2 deterministic authority, isolated worktree ownership, scope checks, denied-network project tests, and post-change evidence model.

## Existing Solution First

### Option A — ChatGPT-authenticated Codex CLI (selected)

- Reuses the official Codex client already intended for local coding work.
- Supports non-interactive `codex exec` runs.
- ChatGPT login and API-key billing are distinct authentication paths; the transport must accept only the ChatGPT-authenticated path.
- Preserves automation without adding a separately billed API dependency.
- Builder and Critic can be independent ephemeral CLI sessions while deterministic Base code remains authoritative.

Decision: **REUSE + ABSORB**.

### Option B — local OSS provider through Codex (`--oss`, Ollama/LM Studio)

- Avoids external paid API billing.
- Requires local model/runtime installation and sufficient hardware.
- Quality, model availability, and tool behavior vary more than the ChatGPT-plan path.

Decision: **DEFER AS OPTIONAL FALLBACK**, not required for v1.

### Option C — manual ChatGPT handoff

- Requires no new provider implementation.
- Breaks the automation objective and introduces manual copy/paste state transfer.

Decision: **REJECT FOR PRIMARY PATH**.

## Architecture

### 1. Policy gate

`provider_gate.py` owns two explicit facts:

- separately billed OpenAI API provider use is forbidden by the approved project policy;
- subscription-native Codex CLI is ready only when the executable exists and `codex login status` reports ChatGPT authentication.

The gate must never treat an API key as a valid fallback. `OPENAI_API_KEY` presence must not upgrade the state.

### 2. CLI transport

Add a focused `codex_cli_transport.py` module. It reuses the existing structured Builder/Critic contract style instead of granting Codex direct authority over the project worktree.

For each model turn:

1. Host code collects the already-approved bounded context/diff.
2. Host code starts a separate temporary directory.
3. Host code runs Codex non-interactively with strict explicit tool restrictions:
   - global `--strict-config`;
   - `features.shell_tool=false`;
   - `features.web_search_request=false`;
   - `features.web_search_cached=false`;
   - `features.standalone_web_search=false`;
   - `exec --ephemeral`;
   - `--ignore-user-config` so project/user config cannot silently add tools or MCP authority;
   - `--ignore-rules` so local exec rules cannot add authority;
   - `--skip-git-repo-check` because the model runs in an empty isolated directory;
   - `--sandbox read-only`;
   - an output schema and final-message file.
4. The child environment strips `OPENAI_API_KEY` and other provider/GitHub secret environment variables. ChatGPT-managed Codex auth remains available through Codex's normal auth store.
5. The final structured JSON is parsed and bounded.
6. Builder write plans are validated by existing deterministic path/authority checks before host-side application.
7. Critic receives only approved requirements plus actual diff evidence and cannot mutate the worktree.

This preserves the existing security property: the model proposes; deterministic host code decides what can be written. Shell and web-search capabilities are intentionally disabled so the model turn cannot use local shell reads or live/cached/extension web search to expand its information boundary.

### 3. Builder/Critic independence

Independence is defined by process and context isolation, not by requiring two separately billed model IDs:

- Builder and Critic are separate `codex exec --ephemeral` processes.
- Critic receives no Builder transcript or hidden session state.
- Critic receives only the locked contract identifiers, actual changed paths, deterministic test/diff evidence, and Builder summary.
- Model selection defaults to Codex CLI's ChatGPT-plan default. Optional explicit model overrides may be supported without becoming a user-approval gate.

### 4. CLI entry point

`tools/loop_a2.py --provider real` becomes the subscription-native real provider path. It must:

- fail closed if ChatGPT Codex authentication is unavailable;
- fail closed if only API-key authentication is active;
- construct the existing `GitWorktreeBuilderAdapter` and read-only Critic using the CLI transport;
- retain the existing `provider_mode=REAL` protocol to avoid a broad schema migration;
- never activate A3 auto-merge or Scheduler.

### 5. Paid API transport status

The existing direct Responses API implementation is retained as historical/rollback code but its gate is permanently closed by policy. No `OPENAI_API_KEY` request is made by the active A2 path.

## Error handling

The subscription transport fails closed on:

- Codex executable missing;
- `codex login status` non-zero;
- authentication state other than exactly ChatGPT-managed login;
- timeout;
- non-zero `codex exec` exit;
- missing/oversized/non-JSON structured final output;
- output schema mismatch;
- unsafe Builder write path, authority-file mutation, changed-path mismatch, or Critic scope expansion.

Failure does not silently retry with API billing or another provider.

## Testing

### Deterministic unit tests

Use a fake Codex executable/process runner so CI needs no ChatGPT credentials. Tests must prove:

- ChatGPT login passes the subscription gate.
- API-key login is rejected even when an API key exists.
- no API-key/GitHub secret environment value reaches the child process.
- CLI invocation is ephemeral, read-only, config/rules-isolated, shell-free, and explicit web-search features are disabled.
- Builder structured writes still pass through existing deterministic validation.
- Critic runs in a separate invocation and receives only bounded review material.
- malformed/oversized/non-zero/timeout outputs fail closed.

### Regression tests

- Existing OpenAI Responses transport tests remain deterministic and cannot make a real paid call.
- Existing A2 runtime, worktree, denied-network, Base-v9, adversarial, and Game Project Operating System gates remain green.

### Real smoke ceiling

A real subscription smoke cannot be claimed unless run on a machine with an actual ChatGPT-authenticated Codex CLI. GitHub Actions without that credential can validate transport construction only. Absence of a local authenticated environment is `BLOCKED_UNVERIFIED`, not failure of the deterministic implementation.

## Machine-readable checkpoint

After merge and postmerge validation, update `UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json` so it no longer says paid smoke is awaiting approval. The new remaining gate is a local subscription-native smoke/burn-in, not a user credential/cost decision.

Expected policy state:

```yaml
paid_openai_api: FORBIDDEN
paid_provider_smoke: NOT_PLANNED
subscription_codex_cli_transport: MERGED_MAIN_VALIDATED
real_openai_api: NOT_APPLICABLE_POLICY_FORBIDDEN
real_a2_burnin_runs: 0
```

A3 auto-merge stays `DISABLED`, Scheduler stays `NOT_CONFIGURED`, and automatic product-scope selection stays `FORBIDDEN`.

## Rollback

Rollback consists of reverting the subscription transport PR and restoring the previous checkpoint. Reverting must not automatically reopen or authorize paid API usage; that would require a new explicit user policy change.
