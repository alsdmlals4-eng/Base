# Provisional Integration Reconciliation — Adversarial Review

Date: 2026-08-15
Scope: Issue #423 / PR #425 governance only

## Reviewed claim

An explicitly authorized integration PR may continue from the latest exact `main` even when open owner PRs overlap, provided owner branches remain read-only and the integration PR cannot merge until overlap ownership is resolved and semantic reconciliation is revalidated.

## Attack matrix

| Attack | Result | Control |
|---|---|---|
| Treat ordinary continuous work as permission to duplicate an owner PR | BLOCKED | `provisional_integration_authorized` requires explicit user authorization; default remains `DUPLICATE_WORK` / `WAITING_RESOURCE`. |
| Mark overlapping work `CLEAR` to hide conflict | BLOCKED | Approved overlap remains `PROVISIONAL_INTEGRATION`, never `CLEAR`. |
| Push fixes directly to the owner PR to make integration easier | BLOCKED | Owner PR branches are explicitly read-only; all provisional writes stay on the isolated integration branch. |
| Reuse an old owner head after that PR changes | BLOCKED | `owner_pr_head_shas` are recorded and owner/main changes trigger immediate reread + reconciliation. |
| Resolve only textual merge conflicts while keeping a weaker stale implementation | BLOCKED BY CONTRACT | Reconciliation is semantic/contract based and must preserve the current stronger canonical security/cost/platform behavior. |
| Reuse CI from a pre-reconciliation head | BLOCKED | Exact-head validation is required after every reconciliation. |
| Merge the integration PR while an overlapping owner remains open and unresolved | BLOCKED | Merge gate requires each owner to be merged+absorbed, handed off/superseded, or explicitly replaced by user authorization. |
| Use provisional integration to bypass Existing Solution First | BLOCKED | Existing owner implementations must be recorded and compared; the mechanism is for absorb/reconcile work, not untracked replacement. |
| Let an unrelated merged PR move `main` while continuing from a stale integration base | BLOCKED | Material main advance triggers reconcile and a fresh preflight. |
| Treat GitHub mergeability as proof of semantic compatibility | BLOCKED | Auto-merge/textual mergeability does not lower overlap to `CLEAR` or satisfy semantic reconciliation. |

## Findings

- P0: 0
- P1: 0
- P2: 0

### Accepted residual risk

`PROVISIONAL_INTEGRATION` deliberately permits temporary duplicate implementation on an isolated branch. This increases reconciliation work and can temporarily make the integration diff larger. The risk is bounded by exact owner-head tracking, read-only owner branches, mandatory reconciliation on owner/main changes, and the unresolved-owner merge block.

## TDD evidence

- RED: workflow run `31852789710`; the focused test failed because `PROVISIONAL_INTEGRATION` was absent from Base governance.
- GREEN: workflow run `31852960596`; the same focused test passed after the minimal contract was implemented.

## IRG ceiling

This review proves only repository governance text + executable regression coverage. It does not yet prove the subsequent Tool Hub integration PR can reconcile #373/#376/#386 without product regressions; that must be demonstrated on the integration PR exact head with its own Windows/Linux/runtime/Figma evidence.
