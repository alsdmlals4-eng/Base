# Local Executor Docker Capability Resolver + Installer v4 Evidence

## Identity

- Date: `2026-08-15`
- Tracking issue: `#419`
- Implementation PR: `#420`
- Triggering real job: Base Issue `#418`, run id `BS_A2_BURNIN_001`
- Scope: Local Executor Docker reviewed-image resolution, shared preflight authority, and the one-click Windows installer/updater v4.
- Product authority: unchanged. Blacksmith Phase C product scope remains unselected.

## Real failure evidence

Installer v3 had reported the local environment ready, including Docker and the reviewed image. The running Windows daemon then consumed the first bounded Blacksmith REAL A2 job and published:

```yaml
status: BLOCKED
code: DOCKER_IMAGE_NOT_PRELOADED
provider_mode: REAL
run_id: BS_A2_BURNIN_001
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```

The mismatch showed that bootstrap image readiness and runtime image resolution did not share one semantic authority. This was not an OpenAI/API credential failure; the job reached the Local Executor runtime Docker gate.

## Root cause and bounded fix

The previous runtime accepted only one lookup spelling:

```text
docker image inspect --format {{.Id}} <exact reviewed digest ref>
```

The accepted image identity remains exactly:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

The resolver now uses bounded trusted routes while preserving that immutable acceptance:

```text
exact digest-ref inspect
→ if unavailable, Docker server OS/architecture semantic probe
→ closed Linux platform normalization
→ same exact digest-ref inspect with --platform <server-platform>
→ exact sha256:<64hex> image ID validation
→ READY | bounded BLOCKED
```

No runtime job pulls, enumerates, or substitutes Docker images. `LocalExecutorService.preflight()` now requires both control-plane and runtime Docker readiness.

## TDD chronology

### Runtime/service RED → GREEN

The #420 branch first added tests requiring platform-aware inspection of the same reviewed digest and service-to-runtime preflight delegation. Production then added the bounded resolver, fail-closed platform/image validation, and shared preflight. Before the latest-main reconciliation, the exact implementation head `e0eccdc5582827ac93c1c481b5824466b3dd158e` passed:

- Validate Loop A2 Local Executor `31836589828`: PASS on Ubuntu and Windows.
- Validate Base v9 Operating Contracts `31836589879`: PASS.
- Validate Game Project Operating System `31836589822`: PASS.

### Completed-main reconciliation

PR #416 later advanced completed Base main to `54186b2406676738e6c07aed29bb985c10cb7126`. Its seven bootstrap-policy/learning files had zero path overlap with #420's six resolver files.

#420 incorporated that completed main through merge commit:

```yaml
head_after_reconciliation: 27b0767599a0a1c6db70a28fb9aaa3b14a143530
behind_main: 0
net_pr_files_after_reconciliation: 6
```

Fresh validation on that reconciled head passed:

- Local Executor `31851541357`: PASS.
- Base v9 `31851541355`: PASS.
- Game Project OS `31851541353`: PASS.

### Installer v4 RED

A test-only commit required the one-click updater before the production script existed.

```yaml
head: 7d94bff2a75eb2f11e9d4c37a9648146a4e654a2
workflow: Validate Loop A2 Local Executor
run: 31851656420
ubuntu_job: 94928434675
result: EXPECTED_RED
existing_contracts: 49_PASS
new_v4_contract: ERROR
cause: Base_Loop_A2_Local_Executor_Installer_v4.cmd absent
```

This proved the permanent Local Executor suite actually consumed the new contract.

### Installer v4 GREEN

The v4 updater was then implemented from the actual v3 Golden Path, with the same install/state/startup/log locations but with the executor shared preflight as Docker truth.

At head `6c2faddc82532cae6d34cdd3b8b625b0dfb9f4ba`:

```yaml
workflow: Validate Loop A2 Local Executor
run: 31851800827
ubuntu_contract: PASS
windows_contract: PASS
windows_cmd_contract_parse: PASS
```

The Windows suite executed the `.cmd --contract-test` path rather than merely reading text.

### Owner/evidence coupling RED

Adversarial review then found that the owner document still described the old single-route Docker behavior. A test was added before the owner/evidence update.

```yaml
head: 11c087a6e39c7f87f305fe56fcb63895c902a2fc
workflow: Validate Loop A2 Local Executor
run: 31851870599
ubuntu_job: 94929022245
result: EXPECTED_RED
existing_runtime_v4_contracts: PASS
new_owner_evidence_contract: ERROR
cause: durable resolver/v4 evidence file absent
```

The owner and this evidence record were then updated together.

### Final exact-head before merge

Exact reviewed PR head: `3fa0f178eb464e1c9b5341fe3f4d38b93fd257bd`.

- Validate One-Shot Local Executor Bootstrap `31852115644`: PASS.
- Validate Loop A2 Local Executor `31852115712`: PASS on Ubuntu 24.04 and Windows 2025.
- Validate Base v9 Operating Contracts `31852115709`: PASS including adversarial gate.
- Validate Game Project Operating System `31852115699`: PASS including final `ci-gate`.
- Dependency Review: `NOT_TRIGGERED` on this exact head.
- unresolved review threads: `0`.
- submitted review blockers: `0`.

## Installer/updater v4 behavior

Committed path:

```text
tools/loop-a2-local-executor/windows/Base_Loop_A2_Local_Executor_Installer_v4.cmd
```

The user-facing flow is double-click/no-manual-terminal and preserves the durable desktop log. It:

1. resolves trusted Git/GitHub CLI/Docker/Codex/Python surfaces;
2. verifies GitHub auth and exact ChatGPT Codex auth;
3. verifies Docker Engine availability;
4. safely stops only the previous executor-owned `pythonw.exe` identified by exact executable path + executor module + exact state root;
5. fetches completed Base `origin/main` into the dedicated install source without resetting/cleaning the user's normal checkout;
6. refreshes the editable Local Executor package;
7. runs the **shared preflight**;
8. only when that preflight reports `DOCKER_IMAGE_NOT_PRELOADED`, pulls the same exact reviewed digest and reruns shared preflight;
9. recreates the existing Startup command, starts the daemon, and confirms the exact daemon process identity;
10. prints `LOCAL_EXECUTOR_READY` only after those checks pass.

The updater does not use a broad `taskkill /IM pythonw.exe`, arbitrary image enumeration, tag-only fallback, or paid/API-key fallback.

## Adversarial review

### Attack: does multi-route resolution weaken immutable image acceptance?

No. Both inspect routes use the same exact reviewed digest. The only normalized value is a closed server platform (`linux/amd64` or `linux/arm64` plus bounded aliases). The returned image ID must still match exact `sha256:<64hex>` syntax.

### Attack: can a runtime job silently pull or select another image?

No. Pulling remains absent from runtime. The v4 bootstrap can pull only the exact reviewed digest and only after shared preflight returns `DOCKER_IMAGE_NOT_PRELOADED`.

### Attack: can updater restart kill unrelated Python applications?

The broad process-name kill is forbidden. v4 selects `pythonw.exe` only when executable path equals the dedicated executor venv and the command line contains both `loop_a2_local_executor.cli` and the exact executor state root.

### Attack: can the updater claim READY before the new daemon is present?

No. It performs bounded process-identity confirmation after daemon start. Failed confirmation returns `INSTALLATION_BLOCKED` and preserves the durable log.

### Attack: does this reopen paid provider, A3, Scheduler, or product scope?

No. The provider remains ChatGPT-authenticated Codex with no API-key fallback. A3 stays disabled, Scheduler not configured, and Blacksmith product scope remains unselected.

## Merge and postmerge closure

PR #420 was squash-merged from exact reviewed head `3fa0f178eb464e1c9b5341fe3f4d38b93fd257bd`.

```yaml
merged_main: 118f40c6ecc29ec98ca3265b67cf4fec4abb45c4
tracking_issue_419: CLOSED_COMPLETED
same_goal_open_pr_after_merge: NONE
```

Fresh push validation on exact merged main:

- Validate Loop A2 Local Executor `31852250061`: PASS on Ubuntu 24.04 + Windows 2025.
- Validate Base v9 Operating Contracts `31852250070`: base-v9-contract PASS + adversarial-gate PASS.
- Validate Game Project Operating System `31852250010`: docs-validation PASS, Ubuntu contract PASS, publication validation PASS, Windows publication/Tool Hub smoke PASS, final `ci-gate` PASS.

Merged-main readback confirms:

- runtime still resolves the exact reviewed digest through direct inspect, then the bounded Docker server-platform route only if required;
- service still requires both control-plane and runtime preflight before returning `LOCAL_EXECUTOR_READY`;
- merged v4 is present at the committed Windows path and preserves the shared-preflight/owned-daemon contract.

`POST_CHANGE_MONITOR_LOOP` found no same-goal duplicate, no code/runtime conflict, and no missing active consumer after the two historical plan/evidence status lines were synchronized by the closure follow-up. Repository implementation classification: `NO_MATERIAL_FOLLOWUP` after that status sync.

## Implementation Reality Gate

Repository evidence now supports:

```yaml
runtime_platform_aware_same_digest_resolver: MERGED_MAIN_VALIDATED
service_runtime_shared_preflight: MERGED_MAIN_VALIDATED
installer_v4_repository_contract: MERGED_MAIN_VALIDATED
installer_v4_windows_cmd_parse: PASS
repository_postmerge_validation: PASS
tracking_issue_419: CLOSED_COMPLETED
real_a2_burnin_runs: 0
live_v4_user_pc_preflight: NOT_RUN
blacksmith_burnin_retry: NOT_RUN_AFTER_V4
```

Repository CI does **not** prove the user's current Docker Desktop image store, current Windows process state, or a successful subscription-native Builder/Critic run. Those require the user to run v4 and the resulting real queue receipt.

## Remaining live sequence

```text
user runs merged-main v4
→ require LOCAL_EXECUTOR_READY
→ re-read current Base main and Blacksmith authority SHA
→ requeue BS_A2_BURNIN_001
→ require PASS / A2_WAITING_INTEGRATION REAL receipt
→ count real burn-in #1
→ repeat #2 and #3
→ verify omission/drift/unauthorized addition = 0
```

A3 and Scheduler remain outside this gate.

## Rollback

Revert PR #420 to remove the resolver/shared-preflight/v4 repository implementation. The paid API path remains forbidden. User product/save/visual data is not migrated by this change. The local executor state root is preserved and should not be deleted as part of repository rollback.
