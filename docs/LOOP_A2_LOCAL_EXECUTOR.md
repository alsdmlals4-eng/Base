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

## Resilient local capability discovery

`CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`: 로컬 bootstrap에서 환경 의존 도구의 존재를 판정할 때 특정 파일명·확장자 하나를 실제 capability보다 높은 gate로 두지 않는다. Windows에서는 같은 명령이 `.exe`, `.cmd`, `.bat` 또는 package-manager shim으로 제공될 수 있으므로, 가능한 경우 다음처럼 **trusted discovery route**를 순서대로 사용한다.

```text
required capability
→ current command resolution / PATHEXT
→ explicitly configured trusted executable path when present
→ known trusted standard install location when appropriate
→ semantic readiness probe
→ READY | bounded BLOCKED
```

예를 들어 Codex 요구사항은 `codex.exe`라는 파일 자체가 아니라 **ChatGPT-authenticated Codex CLI capability**다. `codex` 명령을 신뢰 가능한 Windows command resolution으로 찾은 뒤 `codex login status` 같은 **semantic readiness probe**를 실행하고, 실제 readiness 결과가 계약과 일치할 때만 READY로 판정한다. path 존재만으로 readiness를 PASS로 올리지 않는다.

이 유연성은 보안 완화가 아니다. **discovery는 넓게, authority와 acceptance는 좁게** 유지한다. repository/project identity, exact SHA, trusted author, ChatGPT authentication, reviewed Docker image, protected path, no-paid-API/no-API-key-fallback 같은 권위·보안 조건은 계속 엄격하다.

허용되는 discovery는 현재 command resolver/PATHEXT, 명시적으로 승인된 configuration path, Base가 아는 trusted standard installation location처럼 출처가 제한된 후보뿐이다. 다음은 금지한다.

- 전체 디스크에서 같은 이름의 arbitrary executable 탐색;
- 출처를 확인하지 않은 binary/shim 자동 선택;
- command discovery 실패를 이유로 임의 binary 자동 다운로드;
- ChatGPT auth 실패 시 API key 또는 별도 결제 provider fallback;
- reviewed/pinned Docker boundary를 태그 기반 임의 이미지로 대체.

`DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`: 사용자 PC bootstrap은 실패 시 원인 증거가 사라지지 않게 해야 한다. 최소한 **사용자가 직접 닫기 전까지 유지되는 terminal failure state** 또는 **durable bounded diagnostic log** 중 하나를 제공하고, 가능하면 둘 다 제공한다. 로그에는 stable blocker code와 비밀이 아닌 상태만 남기며 token, credential, raw private file content는 기록하지 않는다.

따라서 bootstrap이 막히면 먼저 실제 실패 capability와 probe 결과를 보존하고, 사용자가 이미 성공시킨 capability를 단일 path/extension 가정 때문에 다시 설치하라고 요구하지 않는다.

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
