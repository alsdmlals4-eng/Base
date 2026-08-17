# Universal Loop v1 Closure Learning Reuse Design

Issue: #497
Baseline: `2b8856054573f1a06297ac8e65f5ca009fa2daef`

## Goal

Reuse the completed Universal Loop v1 REAL A2 closure lessons through existing Base validation and canonical-freshness owners, while synchronizing one stale current operational consumer. Do not create a new broad Skill and do not modify any unrelated in-progress PR branch.

## Existing-solution decision

The reusable behavior already has canonical owners:

- `reviewing-and-validating-project-changes: claim-and-intent-verification` owns completion claims, exact execution evidence, exact-head and postmerge proof.
- `auditing-canonical-reference-freshness` owns current-vs-historical consumer classification, propagation gaps, and stale mutable state.
- `skills/SKILL_LEARNING_LOG.md` owns reusable failure/decision records.

Therefore the correct design is **ABSORB**, not BUILD_NEW.

## Reusable rules

### 1. Machine evidence correction

When a handoff/chat/worker summary conflicts with exact repository or terminal machine evidence, the summary is counterevidence, not authority. Correct the derived record before final closure and bind the final claim to the exact issue/run/SHA/receipt identity.

### 2. Test-consumption proof

A workflow starting because `tests/**` changed does not prove the new test ran. Completion evidence must show the actual command/discovery path consumed the test. For a new regression, an expected RED caused by the intended missing behavior is the preferred proof.

### 3. Successor-aware mutable state

Historical PR/SHA/run provenance remains exact and immutable. Tests or documents that read a `CURRENT_MUTABLE` checkpoint must not permanently freeze a former `NOT_RUN`, `0`, or readiness ceiling after stronger successor evidence is verified. A state transition requires updating the affected current consumers while preserving historical evidence records.

### 4. Latest exact-head validation

When multiple runs exist for the same PR, only evidence for the current exact head may close the gate. Stale-head, cancelled, superseded, zero-step, queued, or still-running runs cannot be substituted for the latest exact-head required gate.

### 5. Bounded zero-escape claims

A statement such as `omission_escape = 0`, `drift_escape = 0`, or `unauthorized_addition_escape = 0` is valid only for the exact approved package, scope, authority, and evidence window that was measured. It must not be generalized to game-wide quality or unrelated product surfaces.

## Current-state drift to repair

`docs/LOOP_A2_LOCAL_EXECUTOR.md` is an active operational document, not historical evidence. Its `Current evidence ceiling` still claims:

- `live_v4_user_pc_preflight: NOT_RUN`
- `real_local_chatgpt_codex_call: NOT_COMPLETED`
- `blacksmith_real_burnin_runs: 0`

The machine checkpoint on completed main already records live Local Executor/ChatGPT Codex/Docker/subscription PASS and three counted REAL A2 burn-ins. This active consumer must be synchronized.

Historical plans, evidence records, PR bodies, and old run descriptions keep their at-the-time values.

## Files

- Modify `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- Modify `skills/auditing-canonical-reference-freshness/SKILL.md`
- Modify `skills/SKILL_LEARNING_LOG.md`
- Modify `docs/LOOP_A2_LOCAL_EXECUTOR.md`
- Modify `tests/test_claim_and_intent_verification_contract.py`
- Modify `tests/test_reference_freshness.py`

No Registry, runtime/provider, Tool Hub implementation, Blacksmith product, A3, Scheduler, or paid-provider policy change.

## Verification strategy

1. Add regression assertions first.
2. Prove RED against the unchanged production/reference documents.
3. Add only the new rules and current-state synchronization required by those tests.
4. Run the same focused tests and canonical reference freshness.
5. Require Base-v9/adversarial and Game Project Operating System exact-head PASS.
6. Recheck current completed main, same-goal PRs, unresolved review threads, and changed-file scope.
7. Squash merge with expected head, then require main readback and postmerge CI.

## External benchmark fit

GitHub Actions concurrency documentation treats older runs in the same concurrency group as replaceable/cancellable when newer work exists, supporting latest-head validation rather than stale-run reuse. SLSA provenance treats verifiable source/process identity as the basis for tracing an artifact, supporting exact SHA/run/digest-bound closure evidence. These references inform the evidence model but do not override Base repository authority.
