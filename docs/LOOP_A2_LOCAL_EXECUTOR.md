# Loop A2 Local Executor

## Current-use boundary

`RETAINED_EXECUTOR_NOT_DEFAULT_WORK_ROUTE` · `HISTORICAL_RUN_EVIDENCE_NOT_CURRENT_PC_STATUS`

The current role authority is `docs/GPT_CODEX_WORKFLOW_POLICY.md`, including `GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED`. This document retains the bounded v1 executor contract and the exact historical runs below; it does not restore GPT/Work → local Codex as the default project workflow. A project-specific, explicitly adopted executor contract remains authoritative only for its recorded scope and version. Without fresh project adoption and current-machine preflight/readback, classify current use as `UNKNOWN_UNVERIFIED`, not installed, running, or retired by inference.

The installer and daemon descriptions below explain preserved capabilities, not instructions to run them during ordinary project startup. Do not activate Startup, Scheduler, a queue consumer, paid API fallback, or A3 because this file exists. Do not delete a previously adopted installation or reset its state to resolve this documentation boundary.

For ordinary project work, use the current Work router, the existing repository-owned PM receipt and `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md` sections 10–11. `CHECKPOINT_IS_NOT_COMPLETION`: a recovery commit, successful model process, or `WAITING_INTEGRATION` receipt is not runtime/visual acceptance, merge permission, or completed approved work. A fresh headless session rehydrates approved files and remaining tasks; it does not authorize an endless new-goal loop. The PM validator checks recorded consistency, not user-PC liveness or historical executor revalidation.

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

Repository CI proves the queue/parser/repository/runtime/service contracts on Ubuntu and Windows. Real user-PC evidence now additionally proves the v4 shared preflight, registered background startup, ChatGPT-authenticated Codex REAL path, reviewed Docker image path, one non-counting diagnostic PASS, and three counted Blacksmith REAL A2 runs that reached `WAITING_INTEGRATION` without opening A3 or Scheduler.

```yaml
live_v4_user_pc_preflight: PASS
local_executor_background_startup: PASS_REGISTERED
github_auth: PASS
codex_chatgpt_auth: PASS
docker_desktop_and_reviewed_image: PASS
real_local_queue_consumption: OBSERVED_PASS_WAITING_INTEGRATION
real_local_chatgpt_codex_call: PASS
blacksmith_real_burnin_runs: 3
```

Exact live provenance for this completed v1 evidence:

```text
successful_real_a2_base_runtime: f4deebfc06de828cc956e47220e829cd98b1eb09
blacksmith_authority: 6b241f28969410de78156c90cc10f33a067426a2
non_counting_diagnostic: #489 / BS_A2_DIAG_20260817_005
a2_burnin_1: #490 / BS_A2_BURNIN_001_R1
a2_burnin_2: #491 / BS_A2_BURNIN_001_R2
a2_burnin_3: #492 / BS_A2_BURNIN_001_R3
universal_loop_v1_closure_main: 2b8856054573f1a06297ac8e65f5ca009fa2daef
```

The successful burn-ins were executed with Base runtime `f4deebfc...`; the later `2b885605...` commit records their closure evidence and does not retroactively claim those runs used the closure commit. Historical v3 blocker evidence remains valid history but is no longer the current evidence ceiling.

Repository CI alone still cannot promote a future local-machine change to PASS. A future Local Executor/runtime change must again produce exact user-PC evidence; the completed receipts above are authority only for the v1 state they actually exercised.

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

## Docker boundary and shared readiness authority

REAL A2 project tests require the reviewed digest-pinned Python image:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

The runtime resolver keeps acceptance immutable while allowing bounded trusted discovery:

```text
exact reviewed digest-ref inspect
→ if unavailable, docker version semantic probe for Server.Os/Server.Arch
→ closed Linux platform normalization
→ docker image inspect --platform <server-platform> --format {{.Id}} <same exact reviewed digest ref>
→ exact sha256:<64hex> image ID validation
→ READY | bounded BLOCKED
```

Supported reviewed container platforms are `linux/amd64` and `linux/arm64`; the bounded architecture aliases `x86_64 → amd64` and `aarch64 → arm64` are normalized. Unknown, malformed, or non-Linux Docker server platforms fail closed.

Actual REAL A2 job execution **never pulls** an image. It resolves only the reviewed digest and passes the exact immutable local image ID to `tools/loop_a2.py`. If neither trusted inspect route resolves that digest, runtime fails closed as `DOCKER_IMAGE_NOT_PRELOADED`.

`LocalExecutorService.preflight()` is the shared readiness authority for installer/updater and daemon startup. It requires both GitHub control-plane readiness and runtime Docker readiness. Path/image presence claimed by separate bootstrap logic is not enough.

The user-facing v4 updater may perform one bootstrap-only recovery action: when the **shared preflight** itself returns `DOCKER_IMAGE_NOT_PRELOADED`, it may pull the same exact reviewed digest and must rerun the shared preflight. It may not enumerate images, choose a tag-only substitute, or pull on other blocker codes.

## Modes

After the Python package is installed into the dedicated local executor environment:

```text
loop-a2-local-executor preflight
loop-a2-local-executor once
loop-a2-local-executor daemon --poll-seconds 60
```

The `.pyw` Windows entrypoint delegates to the same CLI without requiring a PowerShell window. The v4 one-click updater is committed at:

```text
tools/loop-a2-local-executor/windows/Base_Loop_A2_Local_Executor_Installer_v4.cmd
```

It preserves the existing install/state/startup locations, updates its dedicated Base source to completed `origin/main`, refreshes the editable executor package, safely stops only the executor-owned `pythonw.exe` identity, uses the shared preflight as Docker truth, recreates Startup registration, starts the daemon, and confirms the exact daemon process identity before printing `LOCAL_EXECUTOR_READY`.

The updater uses Windows process inspection internally; the user does not need to open or operate PowerShell. Broad `taskkill /IM pythonw.exe` style process termination is forbidden.

The daemon polling interval is bounded to 15–3600 seconds. V1 uses GitHub polling instead of adding a webhook server and inbound network/secret surface.

## Local prerequisites

The local execution machine needs:

- Python 3.12 dedicated executor environment;
- Git executable;
- GitHub CLI authenticated through its local credential store;
- Codex CLI authenticated with ChatGPT, not API-key fallback;
- Docker Desktop/Engine capable of running the reviewed Linux image.

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
- no arbitrary Docker image scan/tag fallback;
- no broad process kill fallback;
- no claim that CI equals a real user-PC Codex run;
- no modification of unrelated in-progress Tool Hub PRs.

## Rollback

Revert the Local Executor Docker resolver/v4 PR to restore the previous repository implementation. Reversion does not authorize paid API usage or mutate project product/save/visual data. On the user PC, the previous v3 installation remains recoverable through the dedicated install directory and preserved state root; do not delete `%LOCALAPPDATA%\BaseLoopA2LocalExecutor` as part of code rollback.
