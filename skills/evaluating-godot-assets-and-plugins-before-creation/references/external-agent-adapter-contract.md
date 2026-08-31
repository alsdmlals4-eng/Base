# External Agent Adapter Contract

- `STATUS: ACTIVE_REFERENCE`
- `AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- `REPOSITORY_PRIMARY_CANON`
- `EXTERNAL_OUTPUT_ADVISORY_ONLY`
- `INSPECT_MUTATE_VERIFY_SEPARATION`
- `ARGV_ARRAY_EXECUTION`
- `SHELL_FALSE`
- `RAW_OUTPUT_FALLBACK_REQUIRED`
- `SOURCE_MODEL_VERSION_RECEIPT`
- `A_B_EVIDENCE_REQUIRED`
- `NO_HIDDEN_BILLING`
- `NO_PLAINTEXT_SECRET_OR_PROMPT_LOGGING`
- `BOUNDED_RETRY`
- `KILL_SWITCH_REQUIRED`
- `PROVIDER_NEUTRAL_CORE`
- `MACRO_OPTIONAL_ADAPTER`

## 1. Purpose

This contract governs optional external code reviewers, command-output proxies, model CLIs, agent workspaces, and future running-mate adapters.

It does not approve a tool by name. A project may activate an adapter only after the current repository authority, the candidate's current behavior, and a bounded A/B gate have been read and recorded.

## 2. Authority and data ownership

The repository remains the primary writable canon for project facts, approved decisions, code, data, assets, tests, and implementation evidence.

External workspaces, shared-memory products, model outputs, compressed command output, and LLM review comments are derived or advisory. They may point to evidence but cannot silently promote a decision, mark a gate complete, overwrite approved meaning, or replace repository readback.

Each adapter must define:

- canonical input owner;
- outputs and their consumers;
- whether the operation is inspect-only, mutating, or verifying;
- data classes transmitted or retained;
- exact rollback path;
- what remains usable when the provider is unavailable.

## 3. Stage separation

Use three explicit stages:

1. **Inspect:** read current authority and collect evidence without changing repository or external state.
2. **Mutate:** apply only the approved bounded change and emit an exact change receipt.
3. **Verify:** read back the resulting state and run Base/project-owned checks independently of the mutating model or service.

An adapter must not combine inspection, mutation, and self-attested verification into one opaque success claim. A generated explanation or review is not verification evidence by itself.

## 4. Process execution safety

Local wrappers and CLIs must use argument arrays rather than interpolated shell commands.

- Set `shell=False` or the platform-equivalent no-shell mode.
- Allowlist executables and supported subcommands.
- Resolve the executable path explicitly when practical.
- Set working directory, environment allowlist, timeout, output byte cap, and process-tree termination behavior.
- Treat filenames, prompts, issue text, model output, and repository content as untrusted data, never executable fragments.
- Separate read-only commands from write-capable commands.
- Require an explicit adapter capability for network, filesystem mutation, credential use, or remote write.

Retries must be finite and cause-aware. Authentication, permission, billing, schema, and deterministic validation failures do not receive blind retries. The receipt records every retry and the final failure class.

## 5. Evidence and raw fallback

Every transformed or generated result must retain a route to the underlying evidence.

For command-output compression:

- store or make reproducible the exact raw command, arguments, working directory, exit code, tool version, and relevant environment identifiers;
- preserve raw stderr and any omitted/aggregated sections needed to diagnose failure;
- bypass compression for exact source reads, exact diffs, test failures, security findings, migration output, release evidence, and any task whose correctness depends on line-level fidelity;
- automatically fall back to raw output when the proxy returns an error, an unknown schema, truncation, contradictory counts, or a verification discrepancy.

For LLM review or model delegation:

- retain the bounded input revision/diff and model response receipt;
- map each finding to exact repository evidence;
- verify proposed fixes using project-owned tests and readback;
- record dismissed findings when they reveal a repeatable false-positive pattern.

## 6. Source, model, and version receipt

Each invocation that can affect a decision or change must record, when observable:

- adapter and upstream tool name/version/commit;
- source or provider;
- model identifier and reasoning/profile setting;
- endpoint type and account/tier used;
- configuration hash or stable configuration summary;
- repository and project revision;
- permission policy and telemetry state;
- start/end timestamps, exit status, retries, and output locator;
- deterministic verification command and result.

Unknown source/model/version is acceptable only for disposable exploration. It blocks promotion, mutation, approval, and completion claims.

## 7. Cost and billing boundary

No adapter may silently enable paid credits, upgrade a plan, purchase usage, select a more expensive route, or continue after a quota/billing response changes the expected cost boundary.

Before a cost-bearing invocation, record:

- free/current-plan route and its limits;
- expected marginal cost or explicit inability to estimate it;
- the approved budget owner and ceiling when non-zero cost is allowed;
- stop behavior at quota, rate, or billing boundaries.

Cost evaluation uses total task cost, not a vendor's per-command token-reduction claim. Include retries, raw rereads, validation, latency, setup, maintenance, and failure recovery.

## 8. Privacy, secrets, and telemetry

- Pass credentials through the platform's secret facility or short-lived environment injection; never commit them.
- Redact secrets before prompts, logs, traces, issue comments, or shared memory.
- Do not record plaintext prompts or repository contents merely to improve recall or debugging.
- Minimize transmitted context to the bounded task.
- Record telemetry, retention, training-use, region, and deletion settings when available.
- Disable optional content telemetry by default for private or unreleased project work.
- A local wrapper does not make a remote endpoint local; document the complete data path.

Ambiguous retention, auth, or telemetry blocks mutation and canon-impacting use.

## 9. A/B promotion gate

Optional use starts disabled. Compare the raw Base-owned path against the adapter on representative bounded tasks.

Record:

- equivalent input and exact revision;
- task success and deterministic verification;
- total input/output tokens where measurable;
- elapsed time and operator interventions;
- retries, crashes, and fallback frequency;
- false positives, false negatives, omissions, and altered evidence;
- marginal cost and exposed data classes.

Promote only when repeated results show meaningful net benefit without authority drift or information loss. Keep the baseline path operational after promotion.

## 10. Kill switch and rollback

Every adapter requires one command/configuration switch that disables interception and restores the raw path.

Trigger the kill switch when:

- deterministic checks disagree with adapter output;
- raw and transformed evidence cannot be reconciled;
- model/tool/version cannot be identified;
- billing, auth, telemetry, or retention changes unexpectedly;
- retries exceed the bounded policy;
- output causes scope, canon, or approved-meaning drift;
- the provider is unavailable and blocks ordinary repository work.

Rollback must not require the failed provider. Re-run the task from repository evidence through the raw path, then archive the failure receipt for revalidation.

## 11. Adapter profiles

### 11.1 Open Code Review profile

- Advisory line-level review only.
- Use bounded diffs and machine-readable output when available.
- Existing project tests and Base review contracts remain the completion gate.
- Do not transmit secrets or unrelated repository history.
- Endpoint and telemetry configuration must be explicit.

### 11.2 RTK profile

- Eligible only for noisy, reconstructable command output.
- Raw command escape must remain obvious and immediate.
- Exact failures, diffs, source, security output, migration output, and release evidence bypass the proxy.
- Auto-disable on count mismatch, truncation, schema drift, negative task-cost result, or repeated raw rereads.

### 11.3 Antigravity CLI profile

- Route only a named task class with a measurable hypothesis; do not route by unsupported claims that one model is generally better.
- Use the narrowest workspace-scoped permission policy and explicit deny/ask/allow rules.
- Record account/tier, model, quota route, telemetry setting, plugin/hook set, and headless output mode.
- Stop before any paid-credit or tier change not already approved.
- Treat generated files and recommendations as untrusted until repository review and tests pass.

### 11.4 Macro profile

- Macro may provide an optional interaction, inbox, task, or observation surface.
- Repository state remains usable and authoritative without Macro.
- Shared memory is derived and must cite/reconcile repository evidence.
- Auth, MCP, storage, search, messaging, and agent paths are evaluated separately; a successful UI setup is not end-to-end runtime evidence.
- Self-hosting requires project-specific architecture, operational, security, backup, update, and AGPL review.

## 12. Future game-development running mate

Build the running mate as a provider-neutral core with explicit ports for:

- repository authority and revision reads;
- task/decision/status receipts;
- asset and runtime evidence locators;
- model/executor routing;
- review and deterministic verification;
- notifications and human decision gates.

A Macro adapter may be the first UI integration, but the core must run headlessly and export all durable state without Macro. Keep connectors replaceable and capability-scoped. Do not merge project canon, agent memory, chat history, and operational telemetry into one undifferentiated store.

## 13. Activation checklist

An adapter is implementation-ready only when all are true:

- current owner and repository authority confirmed;
- version/license/data path read from current primary sources;
- overlap and alternatives reviewed;
- inspect/mutate/verify capabilities separated;
- argument-array/no-shell, timeout, output cap, retry, and termination behavior tested where applicable;
- source/model/version and cost receipts implemented;
- raw fallback and kill switch tested;
- secret and telemetry policy verified;
- representative A/B evidence passes;
- rollback succeeds without the provider;
- project-specific human approval obtained for any cost, auth, external write, or canon-impacting behavior.
