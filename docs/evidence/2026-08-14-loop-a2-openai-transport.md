# Loop A2 OpenAI Transport Evidence — 2026-08-14

## Scope

Issue #364 implements the bounded REAL-provider transport required before paid smoke gate #352. This change uses the official OpenAI Python SDK Responses interface, but **does not make a live or paid API request**.

The model never receives filesystem, shell, GitHub, merge, release, secret-management, A3, or Scheduler tool authority. Builder output is only a structured UTF-8 text write proposal; local deterministic code remains the sole writer to the isolated worktree after scope, authority, path, symlink, output-size, and byte-budget checks. Critic is read-only and is bound to an ownership-verified Git worktree, exact HEAD, actual changed paths, and stable diff digest.

## RED / GREEN history

### RED 1 — module and model-selection gate

Test-only head: `8cf74ef46d39ac585eec2d7ecc1faf6d94513a4a`

Dedicated run `31794675997` failed only because:

- `tools.loop_a2_runtime.openai_transport` did not exist;
- approval + API-key presence alone still opened the REAL provider gate.

GREEN 1 required explicit non-empty `LOOP_A2_BUILDER_MODEL` and `LOOP_A2_CRITIC_MODEL` values and rejected identical model IDs. Dedicated run `31794759605` passed.

### RED 2 — Builder/Critic behavior

Head: `831c446c79ef331e43a830952bd0307ebaf2a40e`

Dedicated run `31795000552` produced four expected contract failures for missing Builder/ReviewMaterial/Critic surfaces while the existing gate tests remained green.

GREEN 2 added:

- structured Responses request shape with strict JSON schema;
- `store=false`;
- bounded `max_output_tokens` and request timeout;
- local allowed-path write application;
- actual Git changed-path reporting instead of model claims;
- prompt credential redaction;
- read-only Critic identity binding and usage counters.

### RED 3 — adversarial provider boundary

Corrected explicit RED head: `87008650cba8fcc24923ee4df7ea8af17e3c0aa1`

Dedicated run `31795321435` produced eight expected failures for missing:

- bounded response bytes;
- symlink-specific fail-closed classification;
- Critic repair mailbox;
- ownership-bound Git review material source;
- diff attestation and diff-size limits;
- lazy REAL provider component factory;
- pinned provider SDK validation.

GREEN 3 head `feb14151649070c42ea4aa98e17aae975fb39201` passed dedicated run `31795526816` with 15 transport/adversarial contracts plus local `openai==3.0.0` Responses surface validation and no network request.

### RED 4 — immutable Loop authority

Head: `2eb85b010aaceb2dc950ae99362265917d968687`

Dedicated run `31795690133` passed the previous 15 contracts and failed exactly one new authority test: an intentionally overbroad caller allowlist could still permit a model proposal to overwrite `PLANNING_LOCK.json`.

GREEN 4 makes the following immutable to the Builder independently of the caller allowlist:

- Project Execution Capsule;
- Planning Lock;
- Visual Lock;
- Runtime Adapter;
- Implementation Package;
- Requirement Coverage Ledger;
- Active Run pointer;
- immutable run record referenced by the Capsule.

All proposed writes are prevalidated before the first mutation, so one authority-path violation blocks the whole plan. The path is checked again immediately before and after each local write.

### Core A2 regression isolation

Provider-only SDK verification initially appeared in the core A2 discovery suite even though that workflow intentionally installs only core validation dependencies. On head `e7a53b134a3ba60a3fe5199f7c889e83a5cd4e7e`, all provider contracts, Base-v9 and Dependency Review were green, but core A2 failed only because the optional `openai` package was absent.

The test boundary was corrected so:

- `Validate Loop A2 OpenAI Transport` installs `requirements-loop-a2-provider.txt` and must exercise the actual SDK surface;
- core A2 may run without the optional SDK and explicitly skips only that SDK-presence probe;
- all provider logic tests remain part of normal core A2 discovery.

After that correction, A2 Foundation run `31796013240` passed the full discovered A2 suite and the required fake-provider burn-in.

## Implemented transport boundary

### Builder

- REAL provider gate must pass before SDK client construction.
- Builder and Critic models must be explicitly selected and distinct.
- official SDK client creation is lazy; importing the module never creates a client or sends a request.
- prompt input contains bounded locked-contract material plus tracked allowed-path UTF-8 text context only.
- exact configured `OPENAI_API_KEY` value and matching secret-like tokens are redacted before prompt construction.
- no `tools` parameter is supplied to the model.
- output must match a strict structured write-plan schema.
- deletes, renames, binary writes, authority writes, out-of-scope writes, unsafe paths, symlink targets, oversized context/output/writes, and malformed responses fail closed.
- WorkerResult changed paths come from actual Git state after local writes.

### Critic

- has no mutation API.
- ownership receipt must verify.
- worktree must still be registered in Git.
- worktree HEAD must equal `expected_main_sha`.
- worker-declared changed paths must exactly match actual Git state.
- each reviewed changed file must be UTF-8 text and non-symlinked.
- actual diff has a byte limit and stable pre/post digest.
- Critic receives approved requirements, actual changed paths, diff digest, and diff text only.
- existing A2 runtime still quarantines Critic requirement/path expansion and requires complete requirement coverage for PASS.
- bounded MUST_FIX findings may be carried into the next approved repair cycle through an in-memory mailbox.

## Provider dependency

`requirements-loop-a2-provider.txt` pins:

```text
openai==3.0.0
```

The dedicated CI installs this pin and verifies that the instantiated SDK exposes `client.responses.create` without sending a request.

## Preserved limits / non-claims

```yaml
live_openai_request: NOT_RUN
paid_api_cost: NOT_RUN
api_key_value_in_repo_or_chat: NONE
builder_model_selected_for_paid_smoke: NOT_SELECTED
critic_model_selected_for_paid_smoke: NOT_SELECTED
blacksmith_real_a2_run: NOT_RUN
real_provider_burnin_runs: 0
push_or_pr_permission_in_provider: NONE
model_filesystem_or_shell_tools: NONE
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_scope_selection: FORBIDDEN
```

Actual paid smoke remains gated by Base issue #352 and requires explicit credential use, Builder model, independent Critic model, bounded cost, and one low-risk Package approval.