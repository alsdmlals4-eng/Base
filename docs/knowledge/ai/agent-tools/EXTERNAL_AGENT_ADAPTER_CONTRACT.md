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

`DISPOSITION_NOT_INSTALLATION_AUTHORITY`: a research disposition does not authorize installation, new account access, execution hooks, external writes, or a project adoption. A project may activate an adapter only after its current authority, the candidate's current behavior, a safely authorized trial, and the resulting bounded A/B evidence have been read and recorded. This document supplies requirements, not an implemented adapter or a second execution owner.

## 2. Authority and data ownership

The repository remains the primary writable canon for project facts, approved decisions, code, data, assets, tests, and implementation evidence. A project's current `AGENTS.md`, adopted contracts, and explicit current exceptions remain authoritative; this shared reference does not silently migrate them.

`PROJECT_ADOPTED_VERSION_REMAINS_AUTHORITY` / `NO_SILENT_PROJECT_ROLLOUT`: read the current project AGENTS.md and its declared owner/version lock before use. A newer Base reference is drift information, not permission to replace the project's adopted contract or install the candidate in every project.

`REUSE_VALID_SCOPED_APPROVAL`: preserve an already valid user approval for the same task, exact allowed operations, and unchanged risk boundary. Do not ask again merely because another stage or session starts. Recheck current project/branch identity, main/head, approval scope, applicable checks, and unresolved review state before any remote write or merge. Changed product meaning, new cost/auth/permissions, unrelated PRs, or destructive scope are not covered by the prior approval.

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
3. **Verify:** read back the resulting state and run Base/project-owned checks, without treating the mutating agent's self-attestation as verification.

An adapter must not combine inspection, mutation, and self-attested verification into one opaque success claim. A generated explanation or review is not verification evidence by itself.

`INDEPENDENCE_IS_CONTEXT_NOT_MODEL`: preserve the existing owner's independent-review requirements using actual author/reviewer context or run identity, role, reviewed revision, and read-only review evidence. A separate reviewer execution may use the same model and provider; a different paid model is not required. Conversely, relabeling a same-context self-review or switching model names does not establish independence. Assigned labels without evidence of separate execution are not sufficient. Deterministic checks, repeated self-review, and an independent review remain distinct evidence types.

## 4. Process execution safety

Local wrappers and CLIs must use argument arrays rather than interpolated shell commands.

- Set `shell=False` or the platform-equivalent no-shell mode.
- Allowlist executables and supported subcommands.
- Resolve the executable path explicitly when practical.
- Set working directory, environment allowlist, timeout, output byte cap, and process-tree termination behavior.
- Treat filenames, prompts, issue text, model output, and repository content as untrusted data, never executable fragments.
- Separate read-only commands from write-capable commands.
- Require an explicit adapter capability for network, filesystem mutation, credential use, or remote write.
- Reuse the current approved executor and its platform-specific safety contract rather than building another wrapper merely to satisfy this reference.

Retries must be finite and cause-aware. Authentication, permission, billing, schema, and deterministic validation failures do not receive blind retries. The receipt records every retry and the final failure class. Termination applies only to the task-owned process tree, not unrelated user processes.

## 5. Evidence and raw fallback

Every transformed or generated result must retain a route to the underlying evidence.

For command-output compression:

- `RAW_CAPTURE_BEFORE_TRANSFORM`: the approved execution path must retain the original invocation's diagnostically relevant stdout/stderr and completion metadata before lossy filtering, with bounded retention, access control, and required secret redaction. Redaction and truncation are declared; raw does not mean permission to persist secrets or private prompts.
- Store the exact command, argument array, working directory, tool version, relevant environment identifiers, and upstream completion status without recording credential values.
- `PRESERVE_UPSTREAM_EXIT_STATUS`: retain the child exit code, timeout/signal state, and expected test counts separately from the filter's status. A successful filter cannot convert a failing child into success.
- Bypass compression for exact source reads, exact diffs, test failures, security findings, migration output, release evidence, and any task whose correctness depends on line-level fidelity.
- `FILTER_FAILURE_IS_NOT_COMMAND_FAILURE`: an error, unknown schema, truncation, contradictory count, or verification discrepancy in the proxy invalidates its transformed view; it does not prove that the underlying command failed or never executed.
- `NO_AUTOMATIC_COMMAND_REPLAY`: fall back by retrieving the already captured original output, not by automatically running the command again. Build, test, migration, and remote-write commands can have side effects even when they sound like verification.
- When the original evidence is absent or incomplete, mark the affected claim `UNVERIFIED`. Replay is a separate operation allowed only after current-state readback and proof that the exact action is read-only or safely idempotent within the existing authorization and retry budget. Otherwise defer the action; never duplicate a possibly successful mutation to recover its log.

For LLM review or model delegation:

- retain the bounded input revision/diff and a secret-safe model response receipt;
- map each finding to exact repository evidence;
- verify proposed fixes using project-owned tests and readback;
- record dismissed findings when they reveal a repeatable false-positive pattern;
- do not turn a model critique, a prompt instruction, or a hook delivery receipt into semantic correctness evidence.

## 6. Source, model, and version receipt

Each invocation that can affect a decision or change must record, when applicable and observable:

- adapter and upstream tool name/version/commit;
- source or provider;
- model identifier and reasoning/profile setting;
- endpoint type and account/tier used;
- configuration hash or stable configuration summary;
- repository and project revision;
- permission policy and telemetry state;
- start/end timestamps, child and adapter exit statuses, retries, and output locator;
- deterministic verification command, expected coverage, and result.

`MODEL_NOT_APPLICABLE_FOR_DETERMINISTIC_TOOL`: a local deterministic output filter has no inference model. Record `model: NOT_APPLICABLE` with the reason instead of inventing a model or treating its absence as unknown. Apply the same explicit not-applicable distinction to endpoints or accounts that the operation genuinely does not use.

An unknown tool/version or an unknown model/provider that the operation actually uses permits disposable exploration only. It blocks promotion, mutation, approval, and completion claims until the required identity is established.

`FRESHNESS_BOUND_TO_REVISION_AND_INPUT`: reusable evidence is bound to the exact repository revision or unchanged relevant content hashes, effective inputs, configuration, tool/model versions, and any material external-state observation. Mutation or drift invalidates affected evidence. An unaffected result may be linked as `REUSED_EVIDENCE` with an explicit equivalence basis; neither a conversation summary nor an earlier PASS silently refreshes it.

## 7. Cost and billing boundary

No adapter may silently enable paid credits, upgrade a plan, purchase usage, select a more expensive route, or continue after a quota/billing response changes the expected cost boundary.

Before a cost-bearing invocation, record:

- free/current-plan route and its limits;
- expected marginal cost or explicit inability to estimate it;
- the approved budget owner and ceiling when non-zero cost is allowed;
- stop behavior at quota, rate, or billing boundaries.

Cost evaluation uses total task cost, not a vendor's per-command token-reduction claim. Include retries, raw rereads, validation, latency, setup, maintenance, and failure recovery. Label estimated token counts separately from tokenizer/provider measurements; unavailable measurements remain unknown, not zero.

`TOKEN_MEASUREMENT_KIND`: identify each number as `OBSERVED_PROVIDER`, `OBSERVED_TOKENIZER`, `BYTE_HEURISTIC`, or `UNAVAILABLE`, with the source and method. `ESTIMATE_IS_NOT_PROVIDER_USAGE`: a local bytes-based estimate or tokenizer count is not an observed bill or ChatGPT/Codex quota saving. Record account usage only when it is actually exposed for the relevant run/window; otherwise leave that metric unavailable rather than deriving a percentage from output length. Compare like-for-like measurement kinds and keep unobserved costs explicit.

## 8. Privacy, secrets, and telemetry

- Pass credentials through the platform's secret facility or short-lived environment injection; never commit them.
- Redact secrets before prompts, logs, traces, issue comments, or shared memory.
- Do not record plaintext prompts or repository contents merely to improve recall or debugging.
- Minimize transmitted context to the bounded task.
- Record telemetry, retention, training-use, region, and deletion settings when available.
- Disable optional content telemetry by default for private or unreleased project work.
- Keep authorized diagnostic captures in the approved access-controlled evidence location, not public issues or unrestricted shared memory.
- A local wrapper does not make a remote endpoint local; document the complete data path.

Ambiguous retention, auth, or telemetry blocks mutation and canon-impacting use.

## 9. A/B promotion gate

`READINESS_PRECEDES_TRIAL`: optional use starts disabled. Evaluate version/license, authority, permissions, data flow, cost, bounded execution, and rollback before authorizing an isolated trial. Reuse the existing adoption owner's states: a `CANDIDATE` can become `TRIAL_APPROVED` for an exact task/environment without already possessing the A/B result that the trial is intended to produce. Run safety/fallback smoke checks on disposable inputs before exposing project data.

`A_B_ISOLATED_EQUIVALENT_STATE`: record a `starting_state_hash` or equivalent immutable input identity for both arms. Use separate disposable workspaces, resettable external fixtures, and equivalent model/configuration/permission budgets so one arm's mutations, learned context, or warm cache cannot silently become the other's starting state. Keep one intentional treatment difference: the evaluated adapter/package. Declare order and cache conditions, control or counterbalance them when material, and use predeclared acceptance criteria. For a pure deterministic text filter, two copies of the same captured immutable input may replace separate workspaces; record why no mutable environment exists. Neither arm may modify canonical project state to obtain the comparison.

Compare the raw Base-owned path against the adapter on representative bounded tasks. Record:

- equivalent input and exact revision;
- task success and deterministic verification;
- total input/output tokens where measurable and the measurement method;
- elapsed time and operator interventions;
- retries, crashes, and fallback frequency;
- false positives, false negatives, omissions, and altered evidence;
- marginal cost and exposed data classes.

`TRIAL_EVIDENCE_PRECEDES_ACTIVATION`: only repeated meaningful net benefit, no authority drift or material information loss, and the existing project adoption decision permit `ADOPTED_ACTIVE`. A failed or incomplete trial remains deferred/rejected or trial-scoped; installation or a successful smoke test is not activation. Keep the baseline path operational after promotion.

## 10. Kill switch and rollback

Every adapter requires one command/configuration switch that disables interception and restores the raw path.

Trigger the kill switch when:

- deterministic checks disagree with adapter output;
- raw and transformed evidence cannot be reconciled;
- an applicable model/tool/version cannot be identified;
- billing, auth, telemetry, or retention changes unexpectedly;
- retries exceed the bounded policy;
- output causes scope, canon, or approved-meaning drift;
- the provider is unavailable and blocks ordinary repository work.

Rollback must not require the failed provider. Read current state, disable the adapter, recover original evidence, and use the raw path for the next authorized operation. Re-executing an earlier command remains subject to section 5's no-replay rule. Archive only the secret-safe failure receipt needed for revalidation; preserve repository facts, tests, approved assets, and user changes.

## 11. Adapter profiles

### 11.1 Open Code Review profile

- Advisory line-level review only.
- Use bounded diffs and machine-readable output when available.
- Existing project tests and Base review contracts remain the completion gate.
- Do not transmit secrets or unrelated repository history.
- Endpoint and telemetry configuration must be explicit.
- Its delegated host-model mode is not automatically an independent reviewer. Confirm actual execution mode, reviewer independence, language/ruleset coverage, and cost route before use; GDScript-specific effectiveness is not established by this reference.

### 11.2 RTK profile

- Eligible only for noisy, reconstructable command output with safe original-invocation capture.
- Raw command escape must remain obvious and immediate for subsequent authorized commands.
- Exact failures, diffs, source, security output, migration output, and release evidence bypass the proxy.
- Auto-disable filtering on count mismatch, truncation, schema drift, negative task-cost result, or repeated raw rereads; never auto-repeat the underlying command.
- Record upstream exit status and filter status separately; do not promote a bytes-based token estimate into measured account savings.

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

`FUTURE_ARCHITECTURE_REFERENCE_ONLY` / `NO_NEW_RUNNING_MATE_IMPLEMENTATION`: the shared example is an architectural consideration, not a current build request. It does not authorize a new product, generic orchestration framework, Macro deployment, or project refactor.

If a later separately approved running-mate need exists, compare current implementations first and consider a provider-neutral core with only the ports actually needed for:

- repository authority and revision reads;
- task/decision/status receipts;
- asset and runtime evidence locators;
- model/executor routing;
- review and deterministic verification;
- notifications and human decision gates.

A possible Macro UI adapter must not own the only durable state or recovery path. Keep any genuinely needed connectors replaceable and capability-scoped. Do not merge project canon, agent memory, chat history, and operational telemetry into one undifferentiated store. Do not implement the full example merely because these concerns are listed here.

## 13. Readiness and activation checklist

Before a bounded trial, confirm:

- current owner, project authority, adopted version, and exact authorized scope;
- version/license/data path read from current primary sources;
- overlap and viable alternatives reviewed;
- inspect/mutate/verify capabilities separated;
- proposed argument-array/no-shell, timeout, output cap, retry, exit-status, capture, and task-owned termination controls;
- source/model/version applicability, measurement kinds, cost limits, and secret/telemetry policy;
- isolated equivalent starting states, predeclared criteria, a disposable safety test plan, raw fallback, kill switch, and provider-independent rollback;
- valid existing authorization, or new approval only where scope/risk actually changes.

Before project activation, require actual safety/fallback/rollback results, representative A/B evidence, implemented applicable receipts, and the project's recorded adoption decision. Documentation checks do not prove these runtime controls are implemented. Do not require completed A/B measurements as a prerequisite to the very trial that will obtain them.
