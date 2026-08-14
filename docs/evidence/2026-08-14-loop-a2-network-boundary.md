# Loop A2 denied-network production boundary evidence

Date: 2026-08-14
Issue: #372
Pull request: #374
Scope owner: Project Test Executor `network: DENIED` production enforcement

## Decision

Use the existing `NetworkBoundary` interface with a Linux Docker `none` execution boundary as the production path for A2 project test commands that declare `network: DENIED`.

`LinuxUnshareDeniedNetworkBoundary` remains an optional fail-closed adapter. GitHub-hosted Ubuntu 24.04 exposes `unshare`, but the production probe on this work observed that unprivileged user/network namespace creation is not permitted. That environment result is not promoted to support.

The Docker path is selected because it gives an OS/container boundary that can execute arbitrary approved command argv without relying on a Python-only network hook. The execution contract uses an exact local image ID and does not pull during child execution.

## Existing-solution and benchmark comparison

| Option | Strength | Hosted-runner reality | Decision |
|---|---|---|---|
| Application/runtime network hook | Small and cheap | Language/runtime specific and bypassable by other executables | Do not use as the general A2 OS boundary |
| `unshare --user --net` | Native Linux namespace isolation | Current GitHub-hosted Ubuntu production probe fails closed because the required unprivileged namespace operation is not permitted | Keep optional; do not claim production support |
| Docker `--network none` | General process/container boundary; only loopback network remains | Proven on the hosted Ubuntu runner used by this repository | Production A2 `DENIED` path |

Primary references used for the design:

- Docker none network driver: https://docs.docker.com/engine/network/drivers/none/
- Docker container run options (`--pull`, `--read-only`, security options): https://docs.docker.com/reference/cli/docker/container/run/
- Docker bind mounts and read-only mounts: https://docs.docker.com/engine/storage/bind-mounts/
- Bazel sandboxing as an industry example combining filesystem isolation with Linux namespaces and optional network isolation: https://bazel.build/docs/sandboxing

The design borrows the boundary pattern, not Bazel implementation code.

## Enforced execution contract

`DockerNoneDeniedNetworkBoundary` accepts only `DENIED` on Linux and requires a local Docker image identifier matching `sha256:<64 hex>`.

The produced child execution plan enforces:

- `--pull never`
- `--network none`
- `--read-only`
- `--cap-drop ALL`
- `--security-opt no-new-privileges`
- `--pids-limit 256`
- bounded writable `/tmp` tmpfs only
- project verification worktree mounted read-only at `/workspace`
- no Docker socket mount
- shell-free argv execution
- a minimal allowlist of child environment variables

The workflow preloads the Python fixture image by the digest observed in the preceding successful production proof:

`python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65`

After preload, the boundary still receives and executes only the exact local immutable image ID. Child execution cannot pull a replacement image.

## TDD and adversarial history

The implementation history deliberately preserved failed assumptions rather than rewriting them as success:

1. RED: production `network_boundary` module absent.
2. GREEN: `unshare` contract implemented and unit-tested.
3. Production probe: GitHub-hosted Ubuntu denied unprivileged user/network namespace creation; adapter remained fail-closed.
4. Adversarial RED: a real Docker `none` path and immutable image contract were required.
5. GREEN: Docker boundary implemented with read-only filesystem/mount, dropped capabilities, no-new-privileges, bounded pids/tmpfs, minimal environment, and `--pull never`.
6. Production proof on PR head `dbbc5adde1a5dfe3dfd178a075815eb303cb91c8`: Docker child observed only `lo` and the dedicated boundary workflow passed.
7. First Project Test Executor E2E attempt on head `307fc3072b35e7b4b8744e3092bcad46a5595ea4` failed before boundary invocation because the workflow harness called nonexistent `run_all(project_root=..., allowed_overlay_paths=...)` keywords. The production API was read back and the harness was corrected to the current `adapter_path`, `worktree_path`, `expected_project_id`, and `expected_main_sha` contract. No boundary PASS was claimed from that failed E2E attempt.

The earlier direct-boundary head is evidence for the direct boundary only. It is not the final integration or merge verdict.

## Integration Reality Gate

A direct Docker wrapper PASS is insufficient to claim that the actual Project Test Executor consumes the boundary. The canonical workflow therefore performs an end-to-end fixture run through `ProjectTestExecutor`.

The E2E fixture:

1. creates a disposable Git repository and exact committed baseline;
2. creates a valid `LOOP_RUNTIME_ADAPTER` with one `network: DENIED` test command;
3. injects a parent `OPENAI_API_KEY` sentinel that must not reach the child;
4. invokes the real `ProjectTestExecutor` with `DockerNoneDeniedNetworkBoundary`;
5. verifies inside the child that the interface list is exactly `['lo']`, the secret sentinel is absent, and a numeric outbound IP connection cannot be established;
6. requires the Executor receipt to report `PASS`, `DENIED`, and `DOCKER_NONE_DENIED_V1`;
7. verifies the source checkout is unchanged after the disposable verification run.

The command itself stays silent. The Executor keeps only bounded digest/byte-count evidence, consistent with its existing stdout/stderr evidence contract.

### Completion claim ceiling

The repository change is not complete merely because this file exists. Final completion requires all of the following on the reviewed exact PR head and then on merged `main` where applicable:

- dedicated denied-network workflow PASS;
- A2 Runtime Foundation PASS;
- Base v9 contract and adversarial gate PASS;
- Game Project Operating System required gate PASS;
- Dependency Review PASS;
- unresolved review threads = 0;
- expected-head merge;
- postmerge `main` readback of the retained boundary and evidence;
- postmerge required push checks PASS.

If a required evidence layer is missing, the verdict remains `IMPLEMENTATION_UNVERIFIED` or `BLOCKED_UNVERIFIED` rather than being inferred from code presence.

## Exact-head failure remediation recorded during this PR

On head `dbbc5adde1a5dfe3dfd178a075815eb303cb91c8`:

- the dedicated denied-network workflow passed;
- A2 Runtime Foundation passed;
- Dependency Review passed;
- Base v9 failed because this new workflow used stale immutable SHAs for `actions/checkout` and `actions/setup-python` compared with the current Base allowlist;
- Game Project Operating System failed only in the Windows publication smoke because Mermaid/Puppeteer timed out waiting for the Chrome websocket endpoint.

The current `main` push at `15fcce9d598b7deb0b4c60d2e330f7404a6a8db1` passed both Base v9 and Game Project Operating System, so the Windows publication timeout is treated as an unrelated transient execution failure, not as permission to modify publication code in this PR.

This PR corrects only the stale Action pins and the missing Executor E2E evidence. If the unrelated Windows timeout recurs on the final exact head, the correct response is to retry/diagnose that workflow without broadening #372 into publication changes.

## Concurrent work boundary

Open PR #369 implements a narrower Python-unittest denied-network mechanism in different files. This PR does not edit, close, re-author, or claim to supersede that in-progress work. #374 owns the general Linux Docker OS/container boundary and its evidence only.

## Explicitly not proven here

- no OpenAI API request is executed;
- no paid provider cost is incurred;
- no API credential is stored in the repository;
- `READ_ONLY_APPROVED` network mode remains fail-closed in this boundary;
- non-Linux Docker production enforcement is not claimed;
- no real Blacksmith A2 burn-in run is claimed;
- A3 auto-merge and Scheduler remain outside this scope.

The first paid provider smoke remains gated by issue #352 and requires its separate user credential/cost decision.

## Rollback

The change has no data migration. Rollback is to revert the #374 squash merge. Existing Project Test Executor behavior will then return to requiring an externally supplied enforceable boundary; no project content or provider state needs restoration.
