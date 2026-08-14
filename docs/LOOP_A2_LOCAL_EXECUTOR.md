# Loop A2 Local Executor

## Purpose

`tools/loop-a2-local-executor` is the local bridge between GPT/Work and the merged subscription-native Loop A2 runtime.

It is designed for this flow:

```text
GPT / Work
→ bounded GitHub issue job
→ user's Windows local executor
→ exact Base runtime SHA
→ exact project authority SHA
→ managed detached worktrees
→ ChatGPT-authenticated Codex Builder
→ deterministic project tests
→ independent Codex Critic
→ sanitized GitHub receipt
→ GPT readback
```

It does **not** authorize separately billed OpenAI API usage, product-scope selection, A3 auto-merge, or Scheduler activation.

## Current evidence ceiling

Repository CI proves the queue/parser/repository/runtime/service contracts on Ubuntu and Windows. It does not prove that the user's local Windows machine has run Codex, Docker, GitHub auth, or the daemon.

```yaml
real_local_chatgpt_codex_call: NOT_RUN
windows_startup_registration: NOT_RUN
blacksmith_real_burnin_runs: 0
```

## Queue job

Only an open issue in `alsdmlals4-eng/Base` with the configured queue label and exact trusted author is eligible. The body must contain only one JSON fence:

```json
{
  "schema_version": 1,
  "contract_role": "LOOP_A2_LOCAL_JOB",
  "target_repository": "alsdmlals4-eng/Blacksmith",
  "base_runtime_sha": "<40 lowercase hex>",
  "authority_sha": "<40 lowercase hex>",
  "capsule": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
  "run_id": "BS_A2_BURNIN_001",
  "provider": "real"
}
```

The job cannot contain command lines, argv, environment variables, local paths, prompts, tokens, merge instructions, or new product scope. The referenced Capsule and Implementation Package remain the execution authority.

## Local state boundary

The executor uses only its own managed state root for clones, detached worktrees, and A2 runtime state. It does not reset, restore, clean, stage, or rewrite the user's ordinary project checkout.

Default Windows state root:

```text
%LOCALAPPDATA%\BaseLoopA2LocalExecutor
```

Repository identity is host-derived from validated `owner/name` as `https://github.com/<owner>/<repo>.git`; a job cannot inject a clone URL.

## Docker boundary

REAL A2 project tests require the reviewed digest-pinned Python image:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

Work execution performs only `docker image inspect` and passes the exact local `sha256:<64hex>` image ID to `tools/loop_a2.py`. It does not pull an image during a job. If the reviewed image is absent, the job fails closed as `DOCKER_IMAGE_NOT_PRELOADED`.

## Modes

After the Python package is installed into the dedicated local executor environment:

```text
loop-a2-local-executor preflight
loop-a2-local-executor once
loop-a2-local-executor daemon --poll-seconds 60
```

The `.pyw` Windows entrypoint delegates to the same CLI without requiring a PowerShell window. Actual installation and Windows startup registration are local machine actions and remain `NOT_RUN` until performed on the user's PC.

The daemon polling interval is bounded to 15–3600 seconds. V1 uses GitHub polling instead of adding a webhook server and inbound network/secret surface.

## Local prerequisites

The local execution machine needs:

- Python 3.12 dedicated executor environment;
- Git executable;
- GitHub CLI authenticated through its local credential store;
- Codex CLI authenticated with ChatGPT, not API-key fallback;
- Docker with the reviewed digest-pinned image already present.

The executor strips `OPENAI_API_KEY`, `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`, `OPENAI_BASE_URL`, `GH_TOKEN`, and `GITHUB_TOKEN` from the REAL A2 child environment. Existing local credential stores remain the intended authentication source.

## Public receipts

Only allowlisted non-secret fields are posted back to the queue issue. Raw stdout/stderr, local absolute paths, tokens, model reasoning, changed file contents, and credentials are not copied into the public receipt.

A successful local job must preserve:

```yaml
state: WAITING_INTEGRATION
provider_mode: REAL
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```

Anything else fails closed and is not reported as successful automation.

## Non-goals

- no paid OpenAI API;
- no API-key fallback;
- no automatic Planning or Visual approval;
- no automatic product-package selection;
- no A3 auto-merge;
- no Scheduler;
- no mutation of the user's normal working tree;
- no claim that CI equals a real user-PC Codex run;
- no modification of in-progress Tool Hub PRs.

## Rollback

Revert the local-executor implementation PR. Queue issues are control-plane records only; reverting does not require product, save, Planning, Visual, or asset rollback.
