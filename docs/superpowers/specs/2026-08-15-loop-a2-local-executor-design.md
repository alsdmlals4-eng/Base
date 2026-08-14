# Loop A2 Unattended Local Executor Design

## Decision

Build the missing local bridge between GPT/Work and the merged subscription-native Loop A2 runtime without modifying any open Tool Hub PR. The first version is a standalone Base-owned Python executor with a no-console Windows entrypoint. A later completed-main Tool Hub slice may consume it through a thin adapter.

## Goal

Enable this bounded flow:

```text
GPT / Work
→ GitHub issue job
→ user's Windows background executor
→ exact Base runtime SHA
→ exact project authority SHA
→ managed project authority checkout
→ merged REAL Loop A2
→ ChatGPT-authenticated Codex Builder
→ deterministic project tests
→ independent Codex Critic
→ bounded receipt
→ GitHub issue comment / terminal job state
→ GPT readback
```

Normal execution must not require a separately billed OpenAI API, an API key, a PowerShell window, or mutation of the user's ordinary project checkout.

## Existing Solution First

### Reuse

- PR #391: authority snapshot separated from the implementation baseline, deterministic project-test PASS before Critic, candidate Diff binding.
- merged `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` and `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` policy.
- BCP-022 pattern: do not destructively clean a user's worktree to obtain executor readiness.
- BCP-023 pattern: classify native process results by exit status + semantic payload + postcondition rather than stderr presence alone.
- BCP-024 pattern: remote authority freshness and local execution evidence may come from separate trusted channels.
- official Codex CLI ChatGPT sign-in and non-interactive execution.
- official Git linked/detached worktree isolation.

### Reject

- direct ChatGPT web/DOM automation;
- API-key fallback;
- arbitrary shell commands carried in queue jobs;
- using the user's active project working tree as the A2 authority/execution workspace;
- modifying open/draft Tool Hub PRs #373/#376/#384/#386/#394 or unrelated #369.

## Benchmark

Checked 2026-08-15 KST:

- OpenAI Help, `Using Codex with your ChatGPT plan`: Codex CLI can sign in with ChatGPT and local workflows run on the user's device.
- OpenAI, `Running Codex safely at OpenAI`: known-good low-risk workflows can be automated inside explicit technical boundaries while higher-risk actions remain explicit.
- Git `git-worktree`: detached linked worktrees are appropriate for isolated temporary implementation/testing without disturbing the main worktree.

ADOPT: non-interactive Codex + bounded local execution.
ADAPT: GitHub is used only as a control-plane job/receipt transport; job bodies cannot inject executable argv.
REJECT: webhook requirement for v1 because it adds an external always-on service and secret surface when bounded polling is sufficient.
DIFFERENTIATOR: authority, runtime code, project baseline, local receipt, and remote job identity are all separately pinned.

## Architecture

### 1. Strict job contract

A queue issue is eligible only when all of the following hold:

- repository is the configured Base control repository;
- issue author is exactly the configured owner login;
- required label is present;
- body is one fenced JSON object with exact known keys;
- `contract_role == LOOP_A2_LOCAL_JOB` and `schema_version == 1`;
- provider is exactly `real`;
- `base_runtime_sha` and `authority_sha` are lowercase 40-hex SHAs;
- target repository is canonical `owner/name`, not a URL supplied to a shell;
- capsule is a normalized repository-relative JSON path;
- run id is bounded `[A-Z0-9_-]`;
- no command, argv, environment, executable path, token, secret, local path, model prompt, or merge instruction is accepted from the job.

The job does not select product scope. The referenced Capsule/Implementation Package remains the only A2 work authority.

### 2. GitHub control-plane adapter

Use the already authenticated `gh` executable through argv-only subprocess calls.

Operations:

```text
gh auth status
→ list open issues with exact queue label
→ parse/validate locally
→ execute at most one claimed job at a time
→ comment sanitized receipt
→ close successful terminal job
```

A failed/blocked job receives a sanitized terminal receipt but must not leak local paths, environment values, Codex credentials, GitHub tokens, raw stdout/stderr, or hidden reasoning.

V1 uses bounded polling; no webhook server is introduced.

### 3. Managed repository state

The executor owns only its state root, defaulting under the user's local application-data directory when installed and a temporary/test root in tests.

For Base and project repositories:

- clone into executor-owned storage if absent;
- verify exact `origin` identity before reuse;
- fetch only through argv-only Git/GitHub operations;
- verify requested SHA exists after fetch;
- create disposable detached worktrees for exact runtime/authority SHAs;
- never reset/restore/clean/stage/rewrite the user's normal project checkout;
- do not search arbitrary local folders for credentials or repositories.

The Base runtime worktree executes `tools/loop_a2.py` at `base_runtime_sha`. The project authority worktree supplies the validated post-baseline Capsule bundle at `authority_sha`.

### 4. Docker denied-network image

The existing REAL A2 CLI requires an exact local immutable Docker image ID. V1 may discover only the Base-reviewed digest-pinned image reference:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

Rules:

- inspect local image first;
- if absent, fail closed in v1 rather than silently pulling during a work run;
- installer/preflight may preload the pinned digest explicitly;
- pass only the resulting exact `sha256:<64hex>` image ID to `loop_a2.py`.

This preserves the merged `--pull never` execution boundary.

### 5. A2 invocation

The executor derives `observed_main_sha` from the validated Capsule `source_main_sha` in the exact authority checkout, then runs:

```text
<python> <exact-base-runtime>/tools/loop_a2.py run
  --project-root <exact-authority-worktree>
  --runtime-root <executor-owned-external-runtime-root>
  --capsule <job capsule>
  --run-id <job run id>
  --observed-main-sha <capsule source_main_sha>
  --provider real
  --denied-network-docker-image-id <verified local immutable image id>
```

No user-provided argv extension is permitted.

Successful process execution is not sufficient. The stdout object must be a bounded Loop receipt with `state == WAITING_INTEGRATION`, `provider_mode == REAL`, `a3_auto_merge == DISABLED`, and `scheduler == NOT_CONFIGURED` before the job is marked successful.

### 6. Windows background entrypoint

Provide a `.pyw` entrypoint so the executor can run without a console window. V1 exposes:

- `once`: process at most one eligible job and exit;
- `daemon`: poll at a bounded interval of at least 15 seconds;
- `preflight`: report only non-secret readiness classifications.

Automatic Windows-startup registration is intentionally separated from the core executor. CI can validate the no-console entrypoint shape, but actual user-PC startup registration remains a local installation action and must not be falsely claimed from GitHub CI.

## Security and authority invariants

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
arbitrary_remote_command: FORBIDDEN
user_worktree_mutation: FORBIDDEN
queue_author: EXACT_OWNER_ONLY
base_runtime_sha: REQUIRED
project_authority_sha: REQUIRED
capsule_authority: REQUIRED
product_scope_selection: FORBIDDEN
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```

## Error handling

Fail closed with stable codes for:

- missing/untrusted `gh` or Git;
- GitHub auth unavailable;
- untrusted issue author/label/body;
- stale or unavailable exact SHA;
- origin mismatch;
- unsafe path/run id;
- missing Codex ChatGPT authentication (surfaced by REAL A2);
- pinned Docker image unavailable or identity mismatch;
- nonzero REAL A2 process;
- malformed/oversized receipt;
- receipt state/identity/policy mismatch;
- GitHub receipt publication failure.

A blocker in one job does not authorize execution of another broader job.

## Testing

TDD fixtures must prove:

1. malicious/untrusted issue bodies cannot inject argv or paths;
2. only exact owner + label jobs are eligible;
3. managed repository reuse requires exact origin identity;
4. exact runtime/authority SHA checks happen before A2 invocation;
5. Docker image discovery accepts only the reviewed digest and exact image ID;
6. generated A2 argv contains only host-derived values;
7. API/GitHub secret environment keys are stripped from child execution;
8. successful receipt must preserve REAL/A3/Scheduler invariants;
9. sanitized GitHub receipt contains no local absolute path, raw stdout/stderr, token, key, or hidden reasoning;
10. `.pyw` entrypoint imports and delegates without shell/PowerShell dependence;
11. existing Loop A2 and Base operating-contract regressions remain green.

## Implementation Reality Gate

CI completion may claim:

```yaml
strict_job_contract: PASS
queue_adapter_contract: PASS
managed_repo_exact_sha_contract: PASS
a2_argv_contract: PASS
receipt_sanitization_contract: PASS
windows_no_console_entrypoint_contract: PASS
real_local_chatgpt_codex_call: NOT_RUN
real_blacksmith_burnin_runs: 0
```

A real local smoke remains `NOT_RUN` until the user's Windows machine runs this executor with valid local GitHub/Codex/Docker state.

## Rollback

Revert the implementation PR. Queue issues are control-plane records only. No product migration, Planning/Visual change, A3 activation, Scheduler configuration, or API billing permission is part of this slice.
