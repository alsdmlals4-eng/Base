# Local Executor Docker Capability Resolver Design

- Date: 2026-08-15
- Status: `APPROVED_USER_CONTINUATION`
- Tracking Issue: `#419`
- Real failure evidence: Base Issue `#418`

## Problem

Installer v3 completed all local checks and reported:

```text
LOCAL_EXECUTOR_READY
Docker image: READY
Executor: INSTALLED
Background: STARTED
Startup: REGISTERED
```

The first real Blacksmith queue job was then consumed by that same background executor and closed with:

```json
{"status":"BLOCKED","code":"DOCKER_IMAGE_NOT_PRELOADED","run_id":"BS_A2_BURNIN_001"}
```

This proves the control plane/background service reached the runtime Docker gate, while installer readiness and runtime readiness disagreed.

## Root cause class

The runtime currently treats one literal CLI resolution route as the complete capability test:

```text
docker image inspect --format {{.Id}} <reviewed exact digest ref>
```

A reviewed digest must remain immutable, but Docker's multi-platform image model can distinguish a higher-level index from a platform image. Modern Docker also supports platform-specific image inspection. The defect class is therefore the same one captured by `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`: strict acceptance is correct, but discovery must not collapse to one representation when another trusted semantic route exists.

## Decision

### 1. Preserve immutable acceptance

The reviewed reference remains exactly:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

Runtime still never pulls images.

Forbidden:

- tag-only fallback;
- arbitrary local-image enumeration as authority;
- nearest-name/image-age selection;
- internet download from the runtime job;
- unpinned image replacement.

### 2. Add bounded multi-route resolution

Resolver order:

```text
exact reviewed digest-ref inspect
→ if absent, read Docker server OS/architecture
→ normalize only a closed set of known architecture aliases
→ exact same reviewed digest-ref inspect with --platform <server-platform>
→ immutable image ID validation
→ READY | bounded BLOCKED
```

The fallback changes only *how the same reviewed digest is resolved*. It does not broaden which image is accepted.

### 3. Closed platform normalization

Accept only Linux container platforms needed by the reviewed Docker boundary:

```text
linux/amd64
linux/arm64
```

Normalize bounded aliases such as `x86_64 -> amd64` and `aarch64 -> arm64`. Windows-container mode or unknown architecture fails closed because the reviewed project-test boundary is Linux-container based.

### 4. One readiness authority

Add `LocalA2Runtime.preflight()` and make `LocalExecutorService.preflight()` call both:

```text
GitHub control-plane preflight
+ runtime Docker capability preflight
```

The same `_image_id()` resolver is therefore used by:

- explicit installer/updater preflight;
- daemon startup preflight;
- actual job execution.

This removes the previous split-brain state where installer logic could claim Docker image READY while job execution rejected it.

### 5. Stable failure classes

Use stable bounded blockers:

```text
DOCKER_IMAGE_NOT_PRELOADED
DOCKER_PLATFORM_UNSUPPORTED
DOCKER_PLATFORM_INVALID
DOCKER_IMAGE_ID_INVALID
```

No raw Docker stderr is published through the public receipt.

## TDD

RED must prove two currently absent behaviors:

1. exact digest-ref inspect fails but platform-aware inspect of the **same digest ref** succeeds;
2. service preflight must fail when runtime Docker preflight fails, rather than reporting GitHub-only READY.

GREEN must preserve:

- no pull in runtime;
- exact digest constant;
- shell-free subprocess calls;
- closed child env and secret stripping;
- Windows and Ubuntu Local Executor contract suites;
- A3 disabled / Scheduler not configured / no paid API fallback.

## Live validation after merge/update

Repository CI cannot prove the user's Docker Desktop image store. After the repo fix is integrated, provide a no-PowerShell installer/updater v4 that:

1. updates the dedicated Base source from completed `main`;
2. refreshes the editable Local Executor install;
3. ensures the exact reviewed digest is pulled if needed;
4. stops/restarts the background daemon safely;
5. runs the Local Executor's own preflight as the sole final readiness authority;
6. preserves Startup registration and durable log;
7. reports `LOCAL_EXECUTOR_READY` only after that shared preflight passes.

Then requeue Blacksmith `BS_A2_BURNIN_001` using the same operations-only authority package.

## Evidence ceiling

CI evidence proves resolver and preflight contracts only. Live success requires a user-PC queue receipt with `status=PASS`, `code=A2_WAITING_INTEGRATION`, `provider_mode=REAL`, `a3_auto_merge=DISABLED`, and `scheduler=NOT_CONFIGURED`.
