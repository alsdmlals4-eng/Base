# Loop A2 Windows Docker DENIED Boundary Evidence

## Identity

- Tracking issue: `#400`
- PR: `#401`
- Source main: `f71f6c14f4a7119cfa7c0bf29097c04fd1c7adaf`
- Consumer discovered by post-change review: merged unattended local executor from PR `#398`.
- Goal: let the Windows-first local executor reach the existing reviewed Docker `network: DENIED` project-test boundary without weakening that boundary.

## Root cause

`DockerNoneDeniedNetworkBoundary.prepare()` rejected every non-Linux host before resolving Docker:

```python
if policy != "DENIED" or platform.system() != "Linux":
    return None
```

The local executor is Windows-first, so a REAL A2 run on the user's Windows machine would have reached `NETWORK_POLICY_UNENFORCED` even when Docker Desktop could execute the existing digest-pinned Linux container plan.

This is a consumer/platform omission, not a Blacksmith product or authority defect.

## External benchmark

Primary Docker documentation checked on 2026-08-15 KST:

- Docker `none` network driver documents that a container started with `--network none` has no network connectivity other than loopback.
- Docker bind-mount documentation describes Docker Desktop handling host paths through its Linux VM and supports read-only bind mounts with `--mount`.

These sources justify allowing the existing Docker boundary to be constructed from Windows; they do not prove Docker Desktop is installed or running on the user's machine.

## TDD RED

### Initial routing error

The first Windows workflow ran the entire historical network-boundary test module. Because some old Linux-only fixtures intentionally use `/usr/bin/*` while mocking `platform.system()`, Windows reported unrelated fixture failures. Production was still untouched.

The workflow was corrected to run only the new Windows-host contract. This was a test-routing correction, not a weakening of the acceptance rule.

### Focused RED

Exact test-only head: `78a1eac716608495c491ed2d49b141ea18cb0d1c`

Focused workflow: `31826389585`

Result: exactly one test ran and failed:

```text
test_windows_host_constructs_same_docker_none_boundary_plan ... FAIL
AssertionError: None is not an instance of NetworkExecutionPlan
Ran 1 test
FAILED (failures=1)
```

The failure occurred because production still rejected `platform.system() == "Windows"` before Docker inspection.

## Minimal GREEN

Production changed only the Docker host gate:

```python
platform.system() != "Linux"
```

became:

```python
platform.system() not in {"Linux", "Windows"}
```

`LinuxUnshareDeniedNetworkBoundary` remains Linux-only.

Implementation head before this evidence document: `1e75b7b593bf8088bdefa88232de08dc05e206b3`.

### Windows contract

Workflow `31826483002`: PASS on `windows-2025`.

The contract requires the Windows-host plan to retain:

- exact immutable image ID inspection;
- `--pull never`;
- `--network none`;
- `--read-only`;
- `--cap-drop ALL`;
- `--security-opt no-new-privileges`;
- PID limit;
- tmpfs;
- read-only `--mount` of the exact working directory to `/workspace`;
- shell-free process construction;
- boundary identity `DOCKER_NONE_DENIED_V1`.

### Linux real-boundary regression

Existing workflow `31826482953` passed through the full real Linux proof:

- boundary contract tests PASS;
- optional `unshare` observation remains separate;
- digest-pinned Python image preloaded for CI proof;
- real Docker `--network none` exposes only loopback;
- ProjectTestExecutor consumes the Docker DENIED boundary end to end;
- whitespace validation PASS.

This proves the Windows host-support change did not weaken the already-validated Linux container boundary.

## Adversarial review

Validated attack lenses:

- **unsupported host broadening:** macOS/Darwin remains fail-closed;
- **policy broadening:** `READ_ONLY_APPROVED` remains fail-closed;
- **Linux unshare drift:** unchanged and still Linux-only;
- **automatic image pull:** still absent; execution plan requires `--pull never` and exact preloaded image ID;
- **shell/path rewriting:** no shell is introduced and Windows host path is passed as the exact resolved bind source;
- **container privilege escalation:** read-only root, cap drop, no-new-privileges, PID limit and tmpfs remain unchanged;
- **secret/environment broadening:** container environment allowlist remains unchanged;
- **product scope:** no project product repository is modified by this Base fix.

## Implementation Reality Gate

Proved by CI:

- Windows host can construct the same reviewed Docker none-network plan;
- unsupported hosts and unsupported policy remain fail-closed;
- Linux real Docker none-network behavior remains validated end to end;
- the security argv and environment boundary remain unchanged except host eligibility.

Not proved here:

- Docker Desktop is installed or running on the user's Windows PC;
- the reviewed image is preloaded on that PC;
- a live Windows Docker container executed there;
- a ChatGPT-authenticated Codex Builder/Critic turn occurred there;
- Blacksmith REAL burn-in run 1/2/3 occurred.

Those remain local execution evidence.

## Preserved policy

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_package_selection: FORBIDDEN
```

## Rollback

Revert the eventual #401 squash merge. The previous behavior fails closed on Windows; no project data or product migration is involved.
