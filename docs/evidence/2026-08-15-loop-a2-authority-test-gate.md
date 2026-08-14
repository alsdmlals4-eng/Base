# Loop A2 Authority Snapshot + Pre-Critic Project Test Gate Evidence

## Scope

Issue `#390`, PR `#391`.

This slice makes the already-merged ChatGPT-authenticated Codex CLI transport structurally executable against a real M2 post-baseline authority bundle and restores the approved deterministic ordering:

```text
validated authority bundle
→ immutable authority snapshot
→ detached implementation-baseline worktree
→ Codex Builder
→ actual Git Diff + deterministic scope gate
→ ProjectTestExecutor under explicit network boundary
→ identity-bound PASS receipt
→ independent Codex Critic with actual diff + bounded test evidence
→ WAITING_INTEGRATION or fail-closed state
```

No live ChatGPT/Codex model call is made by CI or by this evidence slice.

## Root cause 1 — M2 authority root was conflated with the implementation baseline

Blacksmith Universal Capsule migration PR #165 was created on top of baseline:

```text
c969c8ed9c6306f60c851fc85ed97e0ffa885305
```

The new Capsule files record that SHA as `source_main_sha`, because it is the approved implementation baseline. The Capsule files themselves do not exist in that baseline commit.

The previous REAL A2 path correctly created its detached execution worktree at `expected_main_sha`, but Builder authority collection then tried to read Capsule/Package files from that detached baseline worktree. Deterministic tests had hidden this because their authority files were committed into the same synthetic baseline before `expected_main_sha` was calculated.

### Fix

`authority_snapshot.py` now validates and captures the current authority checkout separately from the execution baseline. The snapshot contains closed UTF-8 text for the Capsule, Planning Lock, Visual Lock, Runtime Adapter, Implementation Package, Requirement Coverage Ledger, Active Run, and immutable Run. The detached Builder worktree remains pinned to `source_main_sha` and never receives copied authority files.

Builder context is split:

- trusted Loop authority → immutable snapshot;
- implementation context → tracked allowed files in the detached baseline worktree.

Snapshot authority paths remain write-forbidden even when an overbroad Package allowlist includes one and the path does not exist in the baseline worktree.

## Root cause 2 — ProjectTestExecutor was not part of the REAL Builder → Critic path

The existing `ProjectTestExecutor` and Docker denied-network boundary were already merged and validated, but `A2Runtime.run()` still followed:

```text
Builder → deterministic scope gate → Critic
```

The approved subscription design requires deterministic project-test evidence before Critic.

### Fix

`ProjectTestCandidateVerifier` reuses the existing `ProjectTestExecutor` unchanged:

1. verify durable worktree ownership for project/run/SHA;
2. obtain Runtime Adapter text from the authority snapshot;
3. materialize that exact adapter only in a system temporary directory outside the product worktree;
4. call the existing `ProjectTestExecutor.run_all()` against the owned Builder worktree;
5. publish only canonical PASS evidence to an in-memory mailbox keyed by project/run/package/SHA.

The initial proposal to add a second `run_all_from_value()` executor API was removed after Existing Solution First review showed the existing file-based API already accepts an adapter path outside the worktree.

REAL runtime now fails closed before Builder if no candidate verifier exists. Every initial or repair Builder candidate must pass deterministic scope and project tests before Critic executes. `FAIL`/`BLOCKED` test evidence produces `BLOCKED_UNVERIFIED` and zero Critic calls.

## Critic evidence boundary

Only the active subscription Codex Critic path is extended. The policy-closed generic direct Responses path is not widened for this feature.

The subscription Critic is bound to one exact RunRequest identity and requires the matching project-test PASS receipt before the underlying Codex process can be invoked. The injected receipt contains command status, exit code, network policy/boundary ID, duration, byte counts, and stdout/stderr SHA-256 digests; raw stdout/stderr are not present.

Cross-run Critic reuse and cross-run PASS receipt reuse fail closed.

## Pre-model boundary proof

The candidate verifier has a `preflight()` that parses the snapshot Runtime Adapter and requires every approved project-test network policy to be accepted by the configured `NetworkBoundary.prepare()` implementation.

Subscription factory ordering is:

```text
RunRequest + snapshot identity validation
→ candidate verifier construction
→ project-test boundary preflight
→ ChatGPT Codex auth probe
→ Builder/Critic construction
```

Therefore an unavailable test boundary blocks with `PROJECT_TEST_BOUNDARY_UNAVAILABLE` before `codex login status` or any model turn.

The REAL CLI additionally requires:

- an explicit runtime root outside the project repository;
- an exact local Docker image ID (`sha256:...`) for the denied-network boundary;
- a successfully captured immutable authority snapshot.

The factory is the single ChatGPT-auth gate; a duplicate earlier CLI auth probe was removed after adversarial review.

## TDD evidence

### Authority snapshot

- RED head `6a116a2d5c73a81bf36a9367c04d659ce089cc81`, A2 run `31814067869`: new authority module absent; existing A2 tests remained green.
- GREEN head `fd21d86edaa587a745e448953921a78b708100e3`, A2 run `31814199267`.

### Detached baseline authority context

- RED head `1be3a36aad5510b59b441d8114f422f63a283b1c`, A2 run `31814310262`: Builder had no authority-snapshot input.
- Factory contract RED head `2a2426c694f52774c2feaee2139f6026d7f3a1a2`, A2 run `31814877204`.
- GREEN head `f4682a3dc194b3ba2ca02c9448f777b9d8309252`, A2 run `31814994369`.

### Candidate verification and REAL gate

- Candidate verifier RED run `31815137760`.
- Candidate verifier GREEN / REAL verifier RED run `31815599142`.
- Subscription Critic evidence RED run `31815852833`.
- REAL verifier + Critic evidence GREEN head `c547a50619a28f126419868e6c25d2c21fe3c9d3`, A2 run `31816365245`.
- Candidate boundary preflight GREEN head `aeb8303f7cb10c2be0acfc463db2729e0cbc2af7`, run `31816628879`.

### REAL CLI / factory ordering

- CLI RED head `041ec2602d65efd736982dd5137fbbc1600d4e33`, A2 run `31816690779`: five new snapshot/boundary wiring contracts failed while existing contracts remained green.
- Factory-preflight RED head `a6784ce2acdda4489ec97ff4fb501b7d2972a603`, A2 run `31817037705`: 229 tests, 228 PASS; only missing preflight failed.
- Factory-preflight GREEN head `afbd8c4aea6be4f349840cef9562a946595fb383`, A2 run `31817231052`.
- Duplicate CLI auth-gate RED head `7300729894afeb445feb46c85fa69e20fafe4c92`, A2 run `31817450064`: only the new single-auth-gate expectations failed.
- CLI single-auth-gate fix head `a662aae63fc86d8a7c3970c13abf9b728764e101`.

## Adversarial follow-up findings

### Authority capture TOCTOU

Attack: change a schema-valid protected Planning meaning after canonical bundle validation but before snapshot text capture.

- RED head `f6536546dba357bc7af9ae71f637b4202e14aab2`, A2 run `31817831145`: the new mutation test failed because no exception was raised; other A2 regressions stayed green.
- Fix: capture the exact authority byte/text set before validation, run the canonical M2 validator, reread the exact same set, require byte/text equality, re-resolve Capsule references, and construct the snapshot only from the stable pre-validation set.

### Provider-only dependency pollution

Attack: run the existing dedicated OpenAI transport workflow, whose intentionally narrow environment installs provider dependencies but not the Base documentation/schema validation dependency set.

- Run `31817556060` and follow-up `31817761299` exposed import-time `jsonschema` coupling caused by eager authority-validator imports.
- Fix: keep `tools.loop_a2_runtime.__init__` dependency-light and lazy-load the canonical M2 bundle validator only when a real authority snapshot is captured.
- Head `cb97a5459a4b951d5c55b9242fa0d97d4910933`, dedicated OpenAI transport run `31817950690`: PASS.
- Same head A2 Foundation run `31817950827`: PASS, including the TOCTOU regression.

## Preserved authority and security limits

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
live_chatgpt_codex_call: NOT_RUN
local_subscription_smoke: NOT_RUN
blacksmith_real_a2_burnin_runs: 0
blacksmith_product_package_selection: UNCHANGED_UNSELECTED
blacksmith_product_mutation: NONE
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_package_selection: FORBIDDEN
```

The current PR does not change Blacksmith, Planning Lock meaning, Visual Lock meaning, Figma, product data/code/scenes/assets, GitHub repository settings, A3, or Scheduler.

## Final validation rule

The merge decision is based on one final PR head after current Base `main` is incorporated and this evidence file is present. Required evidence is recorded durably in PR #391 / issue #390:

- A2 Runtime Foundation PASS;
- OpenAI transport regression PASS;
- Base-v9/adversarial PASS;
- Game Project Operating System final `ci-gate` PASS;
- Dependency Review PASS when triggered;
- unresolved review threads `0`;
- exact changed-file audit;
- expected-head squash merge;
- postmerge Base-v9/adversarial + Game Project Operating System PASS.

## Next boundary after merge

A real model call still requires the user's local machine to have a ChatGPT-authenticated Codex CLI and the approved Docker test-boundary image available. The next repository-side step is a Blacksmith `A2_BURNIN_TEST_ONLY` operations/test package and Base Local Executor path. It must leave `next_package` unselected and must not mutate Blacksmith product surfaces.