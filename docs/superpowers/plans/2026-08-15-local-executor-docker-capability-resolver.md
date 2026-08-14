# Local Executor Docker Capability Resolver Implementation Plan

> Execute with TDD and exact-head verification. Unrelated open/in-progress PR branches remain read-only.

**Goal:** Make installer/daemon/job Docker readiness use one bounded capability resolver so a valid reviewed multi-platform image is not rejected only because one literal inspect route differs.

**Initial Base:** `10c4cbb8a530c43bcc0c72cc1ff41d49b766de8e`

**Completed-main reconciliation:** PR #416 was later merged; this branch absorbed completed `main@54186b2406676738e6c07aed29bb985c10cb7126` through merge commit `27b0767599a0a1c6db70a28fb9aaa3b14a143530` without changing the resolver file set.

## Task 1 — RED: platform-aware reviewed-image fallback

**Files**
- Modify `tools/loop-a2-local-executor/tests/test_runtime.py`

- [x] Add `test_image_resolution_retries_same_digest_with_daemon_platform`.
- [x] First fake result: exact `docker image inspect` returns nonzero.
- [x] Second fake result: `docker version --format {{.Server.Os}}/{{.Server.Arch}}` returns `linux/amd64`.
- [x] Third fake result: `docker image inspect --platform linux/amd64 --format {{.Id}} <same exact reviewed ref>` returns immutable image ID.
- [x] Assert no `pull`, tag-only reference, image list, or arbitrary scan appears.
- [x] Observe dedicated Local Executor CI RED against current production code.

## Task 2 — RED: preflight must include runtime Docker readiness

**Files**
- Modify `tools/loop-a2-local-executor/tests/test_service.py`

- [x] Extend runtime fake with `preflight()` call tracking.
- [x] Add test requiring `LocalExecutorService.preflight()` to call control-plane preflight and runtime preflight.
- [x] Add test requiring runtime blocker to propagate rather than returning `GH_CONTROL_PLANE_READY`.
- [x] Observe RED before production implementation.

## Task 3 — GREEN: runtime resolver

**Files**
- Modify `tools/loop-a2-local-executor/src/loop_a2_local_executor/runtime.py`

- [x] Split one-route image lookup into bounded helpers.
- [x] Exact reviewed ref inspect remains first route.
- [x] On not-found only, query bounded Docker server platform.
- [x] Normalize closed Linux architecture aliases only.
- [x] Retry the same reviewed digest ref with `--platform`.
- [x] Validate output as exact immutable `sha256:<64hex>` image ID.
- [x] Do not pull in runtime.
- [x] Add `preflight()` that resolves the reviewed image and returns a bounded readiness mapping without leaking paths/secrets.

## Task 4 — GREEN: service readiness authority

**Files**
- Modify `tools/loop-a2-local-executor/src/loop_a2_local_executor/service.py`
- Test `tools/loop-a2-local-executor/tests/test_service.py`

- [x] `service.preflight()` calls GitHub control plane then runtime preflight.
- [x] Return `LOCAL_EXECUTOR_READY` only when both succeed.
- [x] Existing `once()` behavior and public receipts remain unchanged.

## Task 5 — Regression and adversarial gate

- [x] Windows Local Executor suite PASS before final documentation checkpoint.
- [x] Ubuntu Local Executor suite PASS before final documentation checkpoint.
- [x] Existing missing-image case still blocks and never pulls.
- [x] Unknown/non-Linux platform fails closed.
- [x] Invalid image ID fails closed.
- [x] Child env still excludes API/GitHub secrets.
- [x] Base v9 + adversarial PASS before final documentation checkpoint.
- [x] Game Project OS final `ci-gate` PASS before final documentation checkpoint; Windows smoke follows workflow risk classification.
- [ ] Fresh exact-head Local Executor + Base v9/adversarial + Game Project OS `ci-gate` PASS after this plan/status sync.
- [ ] Dependency Review PASS if emitted for the final exact head; otherwise record `NOT_TRIGGERED` rather than inventing a pass.
- [ ] Review threads 0 and no blocking review submission at final merge gate.

## Task 6 — integrate repo fix, then local v4 updater

- [x] Re-read `main`; absorb only completed-main changes.
- [x] Leave unrelated open/in-progress PR branches untouched.
- [x] Integrate the resolver implementation according to the active user-approved continuation workflow.
- [x] Create a no-manual-PowerShell Windows installer/updater v4 based on the recovered v3 Golden Path.
- [x] v4 updates `%LOCALAPPDATA%\BaseLoopA2LocalExecutorApp\Base`, refreshes the editable package, and safely restarts only the executor-owned daemon identity.
- [x] v4 reports Docker image READY only after the executor's own shared preflight passes.
- [x] Preserve `%LOCALAPPDATA%\BaseLoopA2LocalExecutor` state root, Startup registration, and Desktop durable log.
- [x] TDD installer v4 RED observed: Local Executor run `31851656420`, existing 49 contracts PASS, only v4 file absence failed.
- [x] Installer v4 GREEN observed: Local Executor run `31851800827`, Ubuntu + Windows PASS including Windows `.cmd --contract-test` parse.
- [x] Owner/evidence coupling RED observed: Local Executor run `31851870599`, existing runtime/v4 contracts PASS, missing durable resolver evidence failed.
- [x] Update `docs/LOOP_A2_LOCAL_EXECUTOR.md` and durable resolver/v4 evidence to match actual runtime semantics and claim ceiling.
- [ ] Squash merge #420 from the final reviewed exact head and complete postmerge readback on `main`.

## Task 7 — live burn-in retry

This remains a real user-PC gate and must not be marked complete by repository CI.

- [ ] User runs the merged-main v4 updater and supplies `LOCAL_EXECUTOR_READY` output.
- [ ] Requeue `BS_A2_BURNIN_001` against the then-current reviewed Base runtime and Blacksmith authority `6b241f28969410de78156c90cc10f33a067426a2` after re-reading both SHAs.
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
- [ ] Run #2 and #3 only after #1 is closed with preserved omission/drift/unauthorized-addition boundaries.

## Current claim ceiling

```yaml
runtime_same_digest_platform_resolver: IMPLEMENTED
service_shared_preflight: IMPLEMENTED
installer_v4_repository_contract: IMPLEMENTED
installer_v4_windows_cmd_parse: PASS
live_v4_user_pc_preflight: NOT_RUN
blacksmith_real_a2_burnin_runs: 0
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```
