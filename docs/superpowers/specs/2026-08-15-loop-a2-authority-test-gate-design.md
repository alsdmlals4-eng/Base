# Loop A2 Authority Snapshot and Pre-Critic Test Gate Design

## Decision

The first real subscription-native A2 run must preserve the M2 meaning of `source_main_sha`: it is the approved implementation baseline, not the commit that contains the Capsule files. A2 therefore must separate **authority state** from the **execution worktree**.

A REAL A2 Critic must also never review a Builder candidate before deterministic project tests pass. The existing `ProjectTestExecutor` and denied-network boundary remain authoritative; this change wires them into the production REAL path rather than creating a second test system.

## Root-cause evidence

Blacksmith PR #165 created the Universal Capsule on top of baseline `c969c8ed9c6306f60c851fc85ed97e0ffa885305` while recording that baseline as `source_main_sha`. The Capsule does not exist in that baseline commit. Current A2 correctly creates a detached worktree at `expected_main_sha`, but `OpenAIWorkspaceBuilder` then reads Capsule/Package authority from that detached worktree. This conflates two different roots and makes a real post-baseline Capsule unusable.

Current `A2Runtime.run()` also executes Builder → deterministic scope gate → Critic. `ProjectTestExecutor` exists separately, so the subscription design's promised Builder → deterministic test/diff → Critic sequence is not currently true.

## Architecture

### 1. Immutable authority snapshot

Add `tools/loop_a2_runtime/authority_snapshot.py`.

`capture_authority_snapshot(project_root, capsule_relative, request)` performs one bounded capture before the model components are constructed:

1. resolve and validate the current Capsule bundle from the authority checkout;
2. verify that the captured project/package/source SHA/allowed paths/forbidden paths/resource locks/Requirement IDs exactly match the already-derived `RunRequest`;
3. resolve the Capsule, Planning Lock, Visual Lock, Runtime Adapter, Implementation Package, Coverage Ledger, Active Run, and immutable Run through closed project-relative paths;
4. reject symlinks, binary/NUL content, non-UTF-8 data, path escape, missing files, or a changed bundle;
5. store only immutable UTF-8 text plus normalized paths and a canonical SHA-256 snapshot digest.

The snapshot is in-memory runtime authority. It is not copied into the detached product worktree and is not a new approval source.

### 2. Builder context separation

`OpenAIWorkspaceBuilder` gains an optional `authority_snapshot` dependency.

When a snapshot exists:

- trusted Loop authority text comes only from the snapshot;
- allowed tracked implementation context comes from the detached baseline worktree;
- Loop authority paths remain immutable even if absent from the baseline worktree;
- Builder output is still only a structured write plan and host-side deterministic checks still decide whether writes may be applied.

The legacy direct Responses transport keeps backward-compatible snapshot-less behavior for deterministic historical tests. The active subscription factory always supplies a snapshot.

### 3. Candidate verification gate

Add `tools/loop_a2_runtime/candidate_verification.py`.

`ProjectTestCandidateVerifier` is constructed with:

- repository root;
- runtime root;
- immutable authority snapshot;
- `ProjectTestExecutor` configured with an explicit network boundary;
- an in-memory `VerificationEvidenceMailbox`.

For every successful Builder candidate, before Critic:

1. verify durable worktree ownership for project/run/SHA;
2. read the Runtime Adapter JSON from the immutable snapshot, not the baseline worktree;
3. run the existing `ProjectTestExecutor` against the owned Builder worktree;
4. require `PASS`;
5. publish only the bounded canonical test receipt to the mailbox under project/run/package/SHA identity.

`FAIL`, `BLOCKED`, ownership mismatch, invalid adapter, or missing verifier blocks the REAL run before Critic. No automatic retry can bypass this gate.

### 4. ProjectTestExecutor adapter-value entry point

Refactor `ProjectTestExecutor` so the existing file-based `run_all()` delegates to a new value-based entry point. This allows the verifier to supply the already-captured Runtime Adapter object without writing authority files into the execution worktree.

Existing file-based consumers remain unchanged.

### 5. Critic evidence binding

Extend `ReviewMaterial` with optional bounded `test_evidence`.

`GitReviewMaterialSource` may consume the verification mailbox. For the active subscription path it requires a PASS receipt with the same project/run/package/expected SHA. `OpenAIWorktreeCritic` includes that bounded receipt in its structured input alongside the actual diff and diff digest.

No Builder transcript, hidden model state, raw test stdout/stderr, API key, or shell output is added.

### 6. REAL runtime invariant

`A2Runtime` gains an optional `candidate_verifier` dependency.

- `provider_mode=FAKE`: existing behavior remains compatible; verifier is optional.
- `provider_mode=REAL`: a candidate verifier is mandatory at execution time.
- after every initial/repair Builder scope PASS, verification must PASS before Critic runs.
- verification failure produces `BLOCKED_UNVERIFIED` with bounded finding codes/evidence and zero Critic calls.

This prevents a future REAL provider factory from accidentally bypassing deterministic project tests.

### 7. Subscription CLI wiring

The real CLI sequence becomes:

```text
current authority checkout
→ build RunRequest from validated Capsule
→ capture immutable AuthoritySnapshot
→ ChatGPT Codex auth gate
→ build subscription components with AuthoritySnapshot + CandidateVerifier
→ detached worktree at expected_main_sha
→ Builder
→ actual Diff/scope gate
→ ProjectTestCandidateVerifier
→ PASS receipt mailbox
→ independent Critic with diff + test receipt
→ WAITING_INTEGRATION or fail-closed state
```

The CLI does not select a product package, activate A3, configure Scheduler, or fall back to paid API usage.

## Network boundary

This design does not weaken project-test network policy. `ProjectTestExecutor` still requires an explicit enforceable boundary. If no compatible boundary is configured, REAL A2 stops before Critic with `BLOCKED_UNVERIFIED`.

The existing Docker `network:none` implementation remains the current production denied-network boundary where supported. Windows-host transport support is a separate portability concern and must not be falsely inferred from Linux evidence.

## Blacksmith burn-in boundary

Blacksmith currently records:

```yaml
next_package: UNSELECTED_USER_DECISION_REQUIRED
product_writer_gate: CLOSED_NO_ACTIVE_A2
```

Therefore this Base fix must not select a Phase C product package. After Base postmerge closure, a separate Blacksmith `A2_BURNIN_TEST_ONLY` operations/test package may be prepared only if it:

- changes no `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot` product surface;
- leaves `next_package` unselected;
- has `visual_impact: NONE`;
- exists solely to prove Builder → deterministic test → independent Critic orchestration.

## TDD requirements

### Authority regression

Create a real temporary Git fixture with:

1. baseline commit containing implementation/test files;
2. later authority commit adding Capsule bundle files whose `source_main_sha` points to baseline;
3. detached A2 worktree at baseline.

RED must prove current Builder authority collection fails because the Capsule is absent from the baseline worktree. GREEN must prove the snapshot supplies authority without copying it into the worktree.

### Verification regression

Require:

- REAL runtime with no verifier → blocked before Critic;
- project-test FAIL/BLOCKED → blocked before Critic;
- PASS receipt → Critic invoked once;
- repair Builder candidate → tests rerun before the next Critic call;
- receipt identity mismatch/stale mailbox entry → Critic blocked;
- raw stdout/stderr absent from Critic payload;
- FAKE runtime regressions remain green.

### Adversarial review

Attack:

- authority snapshot captured from a different request;
- authority-root symlink/path escape;
- authority mutation after capture;
- Builder attempt to write an authority path absent from baseline;
- Critic invocation without PASS test receipt;
- stale/cross-run verification receipt reuse;
- test command mutation of verification workspace;
- network policy unenforced;
- paid API fallback;
- A3/Scheduler accidental activation.

## Claim ceiling

CI proves deterministic construction and fail-closed orchestration only. It does not claim a real ChatGPT subscription model call. The machine-readable checkpoint remains `LOCAL_SMOKE_GATED` until a local authenticated execution receipt exists.

## Rollback

Revert the eventual M4.10 PR. The no-paid-API policy remains in force. No Blacksmith product data migration or Planning/Visual approval is changed by this Base slice.