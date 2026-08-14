# Loop A2 Worktree and Actual Diff Evidence

## Scope

This follow-up to PR #343 extends only the A2-owned paths from issue #342. It does not modify the M3 SHADOW Kernel, Project Adapter/visual-tool paths, planning or visual canon, project product repositories, A3, or scheduling.

## TDD RED 1 — production module absent

- Test-only head: `612eb932f35b8031dfea35f296cf78510ac0becb`.
- Dedicated run: `31766922876` / expected failure.
- Existing A2 Foundation tests passed before the new test module failed to import.
- Expected cause: `tools.loop_a2_runtime.worktree_adapter` did not exist.

The new acceptance surface required:

1. external detached Git worktree mutation;
2. actual Git Diff as authoritative changed-path evidence;
3. declared-vs-actual Diff mismatch failure;
4. hard timeout of the direct subprocess Worker;
5. no parent `OPENAI_API_KEY` inheritance;
6. actual out-of-scope Diff quarantine before Critic;
7. expected-SHA availability before Worker execution;
8. external worktree cleanup;
9. runtime root outside the source repository.

## GREEN 1 — isolated FAKE execution

- Production module added: `tools/loop_a2_runtime/worktree_adapter.py`.
- Head: `1c66d6f24f882fa375e1ec64c4d39cab6d71b570`.
- Dedicated run: `31767051300` / PASS.
- Result: `58` A2 tests passed, existing three-run Fake Provider burn-in passed, and whitespace validation passed.

The adapter creates a detached worktree at the approved SHA, runs a bounded argv-based subprocess with an allowlisted environment, then replaces Worker changed-path claims with paths derived from actual Git state. The source repository remains clean.

## Adversarial RED 2 — unsandboxed REAL reuse

Independent review found that the generic subprocess adapter had no OS sandbox even though its environment excluded credentials. A caller could still pass `provider_mode=REAL`, creating an unsafe future reuse path.

- Test head: `4950bd59175a4720e2a4ab7eee24612325518fb8`.
- Dedicated run: `31767143764` / expected failure.
- Result: `59` tests ran; the new `test_subprocess_worker_refuses_real_provider_mode` alone failed because the Worker returned `COMPLETED` instead of a fail-closed block.

## GREEN 2 — FAKE-only subprocess boundary

`SubprocessWorkspaceWorker` now rejects any request whose `provider_mode` is not `FAKE` before executing the subprocess.

```text
REAL request
→ WORKER_PROVIDER_MODE_UNSUPPORTED
→ no model transport
→ no credential injection
→ no integration claim
```

- Fix head: `0f75e555bdece5c27fde59051000d7f14c05056f`.
- Dedicated run: `31767282740` / PASS.
- Result: `59` tests passed, three-run Fake Provider burn-in passed, and whitespace validation passed.

## Evidence meaning

This slice proves:

- a real local Git worktree is used for deterministic FAKE mutation tests;
- actual Git state, not the Worker declaration, owns changed-path evidence;
- out-of-scope actual changes are blocked before Critic;
- parent OpenAI credentials are not inherited by the Worker environment;
- the direct subprocess is terminated on the configured timeout;
- the unsandboxed subprocess adapter cannot run `provider_mode=REAL`;
- the source repository is not modified by the isolated Worker;
- cleanup removes the external worktree.

It does **not** prove:

```yaml
REAL_CODEX_BUILDER: NOT_IMPLEMENTED
REAL_GPT_CRITIC: NOT_IMPLEMENTED
REAL_OPENAI_API: NOT_RUN_USER_DECISION_REQUIRED
GENERAL_OS_SANDBOX: NOT_IMPLEMENTED
ARBITRARY_PROCESS_TREE_TERMINATION: NOT_CLAIMED
PROJECT_TEST_COMMAND_EXECUTION: NOT_IMPLEMENTED
PR_HANDOFF: NOT_IMPLEMENTED
POSTMERGE_CLOSURE: NOT_IMPLEMENTED
CROSS_PROJECT_PILOT: NOT_RUN
A3_AUTO_MERGE: DISABLED
SCHEDULER: NOT_CONFIGURED
```

## Final integration gate

The final PR head must pass the dedicated A2 suite, Base-v9 contract/adversarial gate, Game Project OS including Windows and final `ci-gate`, have unresolved review threads `0`, preserve current-main compatibility, and use expected-head squash merge. Postmerge main readback and push workflows remain mandatory.

## Rollback

Revert the eventual worktree/Diff follow-up squash merge. No project product data, planning canon, visual canon, or asset migration is involved.
