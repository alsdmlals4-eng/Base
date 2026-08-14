# Loop A2 Authority Snapshot and Pre-Critic Test Gate Implementation Plan

> **For agentic workers:** Use TDD, exact-head evidence, and adversarial review. This plan records the implementation actually selected after Existing Solution First and root-cause review.

**Goal:** Make the ChatGPT-authenticated REAL A2 path executable against an M2 post-baseline authority bundle while requiring deterministic project-test PASS before every Critic turn.

**Architecture:** Capture the validated M2 authority bundle into an immutable in-memory snapshot separate from the detached implementation-baseline worktree. Reuse the existing file-based `ProjectTestExecutor` unchanged by transiently materializing the captured Runtime Adapter outside the product worktree. Bind the resulting canonical PASS receipt to one run identity and inject that digest-only evidence only into the subscription Codex Critic path.

**Tech Stack:** Python 3.12 standard library, existing Loop M2 contracts, Loop A2 runtime/worktree ownership, ProjectTestExecutor, Docker denied-network boundary injection, Codex CLI transport, unittest, GitHub Actions.

## Global constraints

- Separately billed OpenAI API calls remain forbidden.
- `source_main_sha` / `expected_main_sha` remain the approved implementation baseline.
- Authority files are never copied into the detached product worktree.
- REAL Critic execution is forbidden until deterministic project tests PASS.
- REAL factory construction must prove the test network boundary before ChatGPT auth probing or model use.
- FAKE runtime behavior remains backward compatible.
- A3 auto-merge remains `DISABLED`; Scheduler remains `NOT_CONFIGURED`; automatic product-package selection remains forbidden.
- CI never makes a live ChatGPT/Codex model call.
- Open/draft PR #369 and all unrelated open PRs remain untouched.

---

## Task 1 — Immutable authority snapshot

**Files**

- `tools/loop_a2_runtime/authority_snapshot.py`
- `tools/loop_a2_runtime/__init__.py`
- `tests/test_loop_a2_authority_snapshot.py`

- [x] Create a real Git fixture where the implementation baseline predates the Capsule bundle.
- [x] Confirm RED because the snapshot module does not exist.
- [x] Validate the current authority bundle before capture.
- [x] Capture Capsule, Planning Lock, Visual Lock, Runtime Adapter, Package, Coverage, Active Run, and immutable Run as closed UTF-8 text.
- [x] Reject symlinks, path escape, NUL/binary content, invalid UTF-8, missing files, and request/bundle identity mismatch.
- [x] Compute canonical snapshot SHA-256.

**TDD evidence**

- RED head `6a116a2d5c73a81bf36a9367c04d659ce089cc81`, A2 run `31814067869`.
- GREEN head `fd21d86edaa587a745e448953921a78b708100e3`, A2 run `31814199267`.

## Task 2 — Separate Builder authority from execution baseline

**Files**

- `tools/loop_a2_runtime/openai_transport.py`
- `tools/loop_a2_runtime/codex_cli_transport.py`
- `tests/test_loop_a2_authority_context.py`
- `tests/test_loop_a2_codex_cli_transport.py`

- [x] Create a detached baseline worktree where the Capsule is absent.
- [x] Confirm RED because Builder has no authority-snapshot input.
- [x] Read trusted Loop authority only from the snapshot while reading allowed implementation context from the detached worktree.
- [x] Keep snapshot authority paths immutable even if an overbroad Package allowlist contains them.
- [x] Keep legacy direct Responses tests backward compatible.
- [x] Require an immutable snapshot in the active subscription provider factory.

**TDD evidence**

- Authority-context RED head `1be3a36aad5510b59b441d8114f422f63a283b1c`, run `31814310262`.
- Factory-contract RED head `2a2426c694f52774c2feaee2139f6026d7f3a1a2`, run `31814877204`.
- GREEN head `f4682a3dc194b3ba2ca02c9448f777b9d8309252`, run `31814994369`.

## Task 3 — Reuse ProjectTestExecutor through an owned candidate verifier

**Files**

- `tools/loop_a2_runtime/candidate_verification.py`
- `tools/loop_a2_runtime/__init__.py`
- `tests/test_loop_a2_candidate_verification.py`
- `tests/test_loop_a2_candidate_preflight.py`

### Existing Solution First correction

An initial proposal added `ProjectTestExecutor.run_all_from_value()`. Review showed that existing `run_all(adapter_path=..., worktree_path=...)` does **not** require the Runtime Adapter path to live inside the product worktree. The new API and its test were deleted before production adoption.

Decision: **REUSE**, not REFACTOR.

- [x] Verify durable worktree ownership for project/run/SHA.
- [x] Read Runtime Adapter text from immutable authority snapshot.
- [x] Materialize it only in a system temporary directory outside the product worktree.
- [x] Call existing `ProjectTestExecutor.run_all()` unchanged.
- [x] Preserve its disposable verification worktree, change overlay, network enforcement, mutation detection, timeout, and digest-only stdout/stderr evidence.
- [x] Publish PASS only to an identity-bound in-memory `VerificationEvidenceMailbox`.
- [x] Reject cross-run receipt/workspace reuse.
- [x] Add `preflight()` that proves every Runtime Adapter network policy can be prepared without running project tests or invoking a model.

**TDD evidence**

- Initial verifier RED run `31815137760` exposed the absent verifier/new entry surface.
- Corrected minimal candidate verifier and fixture were GREEN by run `31815599142`.
- Boundary preflight was GREEN at head `aeb8303f7cb10c2be0acfc463db2729e0cbc2af7`, run `31816628879`.

## Task 4 — Require project-test PASS before every REAL Critic turn

**Files**

- `tools/loop_a2_runtime/runner.py`
- `tools/loop_a2_runtime/codex_cli_transport.py`
- `tests/test_loop_a2_real_verification_gate.py`
- `tests/test_loop_a2_critic_test_evidence.py`
- `tests/test_loop_a2_subscription_factory_preflight.py`

- [x] REAL runtime without a candidate verifier blocks before Builder usage with `PROJECT_TEST_GATE_REQUIRED`.
- [x] After every Builder scope PASS, run candidate verification before Critic.
- [x] Project-test `FAIL` or `BLOCKED` produces `BLOCKED_UNVERIFIED` and zero Critic calls.
- [x] Repair candidates rerun project tests before every subsequent Critic turn.
- [x] Keep FAKE runtime unchanged.
- [x] Bind the exact run's canonical PASS receipt into subscription Codex Critic input.
- [x] Do not modify the policy-closed generic paid Responses Critic path solely for this evidence feature.
- [x] Reject cross-run subscription Critic reuse.
- [x] Ensure Critic evidence contains digests/byte counts, not raw stdout/stderr.
- [ ] Enforce candidate-verifier `preflight()` inside the subscription factory **before** ChatGPT auth probe. This is the final GREEN step for Task 4.

**TDD evidence**

- REAL verifier RED run `31815599142`: exactly the new verifier requirements failed while prior A2 tests stayed green.
- Subscription Critic evidence RED run `31815852833`; implementation was narrowed to the subscription-only wrapper after adversarial minimality review.
- REAL verifier + Critic evidence GREEN head `c547a50619a28f126419868e6c25d2c21fe3c9d3`, A2 run `31816365245`.
- Factory preflight RED head `a6784ce2acdda4489ec97ff4fb501b7d2972a603`, A2 run `31817037705`: 229 tests, 228 PASS, only missing factory preflight failed.

## Task 5 — Wire REAL CLI

**Files**

- `tools/loop_a2.py`
- `tests/test_loop_a2_subscription_cli_entrypoint.py`

- [x] Require explicit external `--runtime-root`.
- [x] Require exact `--denied-network-docker-image-id sha256:...` before authority capture/auth/factory.
- [x] Capture authority snapshot after validated RunRequest derivation and before provider auth.
- [x] Construct `DockerNoneDeniedNetworkBoundary` + `ProjectTestExecutor` explicitly.
- [x] Pass snapshot, bound RunRequest, and executor to the subscription provider factory.
- [x] Construct REAL `A2Runtime` with the factory candidate verifier.
- [x] Preserve no-paid-API policy and no A3/Scheduler/package-selection behavior.

**TDD evidence**

- CLI RED head `041ec2602d65efd736982dd5137fbbc1600d4e33`, A2 run `31816690779`: existing A2 contracts passed; five new CLI contracts failed because snapshot/boundary wiring was absent.
- CLI wiring head `8a7a4c18c732c9d259bab2c850d09d134524ffd6` passed the new CLI contracts before the final factory-preflight RED was added.

## Task 6 — Exact-head adversarial verification and merge

- [ ] Finish factory preflight GREEN.
- [ ] Create `docs/evidence/2026-08-15-loop-a2-authority-test-gate.md` with root cause, RED/GREEN, exact head, claim ceiling, and run IDs.
- [ ] Run focused A2 Foundation and subscription/OpenAI transport regressions.
- [ ] Attack authority mismatch/symlink/authority write, stale/cross-run receipt, test bypass, repair bypass, boundary unavailable, secret leakage, paid fallback, A3/Scheduler activation.
- [ ] Run Base-v9/adversarial, Game Project OS final `ci-gate`, and Dependency Review when triggered on one exact head.
- [ ] Confirm changed-file scope and unresolved review threads `0`.
- [ ] If `main` moved, absorb only completed `main` changes into this branch, prove diff unchanged, and repeat exact-head checks.
- [ ] Mark PR #391 ready and squash merge with expected-head protection.
- [ ] Read back merged `main` and require postmerge Base-v9/adversarial + Game Project OS success.
- [ ] Close issue #390 with durable exact-head/merge/postmerge evidence.

## Claim ceiling

This PR may claim deterministic CI construction and fail-closed orchestration only. It must not claim:

```yaml
real_chatgpt_subscription_model_call: NOT_RUN
blacksmith_real_a2_burnin: NOT_RUN
paid_openai_api: FORBIDDEN
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_package_selection: FORBIDDEN
```

After Base postmerge closure, the next independent step is a Blacksmith `A2_BURNIN_TEST_ONLY` operations/test package plus a local-executor path; it must leave the Phase C product package unselected.