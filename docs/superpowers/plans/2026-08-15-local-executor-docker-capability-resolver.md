# Local Executor Docker Capability Resolver Implementation Plan

> Execute with TDD and exact-head verification. Open/in-progress PR branches remain read-only.

**Goal:** Make installer/daemon/job Docker readiness use one bounded capability resolver so a valid reviewed multi-platform image is not rejected only because one literal inspect route differs.

**Base:** `10c4cbb8a530c43bcc0c72cc1ff41d49b766de8e`

## Task 1 — RED: platform-aware reviewed-image fallback

**Files**
- Modify `tools/loop-a2-local-executor/tests/test_runtime.py`

- [ ] Add `test_image_resolution_retries_same_digest_with_daemon_platform`.
- [ ] First fake result: exact `docker image inspect` returns nonzero.
- [ ] Second fake result: `docker version --format {{.Server.Os}}/{{.Server.Arch}}` returns `linux/amd64`.
- [ ] Third fake result: `docker image inspect --platform linux/amd64 --format {{.Id}} <same exact reviewed ref>` returns immutable image ID.
- [ ] Assert no `pull`, tag-only reference, image list, or arbitrary scan appears.
- [ ] Observe dedicated Local Executor CI RED against current production code.

## Task 2 — RED: preflight must include runtime Docker readiness

**Files**
- Modify `tools/loop-a2-local-executor/tests/test_service.py`

- [ ] Extend runtime fake with `preflight()` call tracking.
- [ ] Add test requiring `LocalExecutorService.preflight()` to call control-plane preflight and runtime preflight.
- [ ] Add test requiring runtime blocker to propagate rather than returning `GH_CONTROL_PLANE_READY`.
- [ ] Observe RED before production implementation.

## Task 3 — GREEN: runtime resolver

**Files**
- Modify `tools/loop-a2-local-executor/src/loop_a2_local_executor/runtime.py`

- [ ] Split one-route image lookup into bounded helpers.
- [ ] Exact reviewed ref inspect remains first route.
- [ ] On not-found only, query bounded Docker server platform.
- [ ] Normalize closed Linux architecture aliases only.
- [ ] Retry the same reviewed digest ref with `--platform`.
- [ ] Validate output as exact immutable `sha256:<64hex>` image ID.
- [ ] Do not pull in runtime.
- [ ] Add `preflight()` that resolves the reviewed image and returns a bounded readiness mapping without leaking paths/secrets.

## Task 4 — GREEN: service readiness authority

**Files**
- Modify `tools/loop-a2-local-executor/src/loop_a2_local_executor/service.py`
- Test `tools/loop-a2-local-executor/tests/test_service.py`

- [ ] `service.preflight()` calls GitHub control plane then runtime preflight.
- [ ] Return `LOCAL_EXECUTOR_READY` only when both succeed.
- [ ] Existing `once()` behavior and public receipts remain unchanged.

## Task 5 — Regression and adversarial gate

- [ ] Windows Local Executor suite PASS.
- [ ] Ubuntu Local Executor suite PASS.
- [ ] Existing missing-image case still blocks and never pulls.
- [ ] Unknown/non-Linux platform fails closed.
- [ ] Invalid image ID fails closed.
- [ ] Child env still excludes API/GitHub secrets.
- [ ] Base v9 + adversarial PASS.
- [ ] Game Project OS final `ci-gate` PASS including Windows smoke when emitted.
- [ ] Dependency Review PASS.
- [ ] Review threads 0.

## Task 6 — integrate repo fix, then local v4 updater

- [ ] Re-read `main`; absorb only completed-main changes.
- [ ] Do not modify open PR #416 or older active PR branches.
- [ ] Integrate the fix according to the active user-approved continuation workflow.
- [ ] Create a no-PowerShell Windows installer/updater v4 based on the existing v3 Golden Path.
- [ ] v4 updates `%LOCALAPPDATA%\BaseLoopA2LocalExecutorApp\Base`, refreshes the editable package, and restarts the daemon.
- [ ] v4 reports Docker image READY only after the executor's own shared preflight passes.
- [ ] Preserve `%LOCALAPPDATA%\BaseLoopA2LocalExecutor` state root, Startup registration, and Desktop durable log.

## Task 7 — live burn-in retry

- [ ] User runs v4 and supplies `LOCAL_EXECUTOR_READY` output.
- [ ] Requeue `BS_A2_BURNIN_001` against current reviewed Base runtime and Blacksmith authority `6b241f28969410de78156c90cc10f33a067426a2`.
- [ ] Require public receipt:

```yaml
status: PASS
code: A2_WAITING_INTEGRATION
provider_mode: REAL
a2_state: WAITING_INTEGRATION
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```

- [ ] Only then count REAL burn-in run 1 as successful and update the machine-readable readiness checkpoint.
