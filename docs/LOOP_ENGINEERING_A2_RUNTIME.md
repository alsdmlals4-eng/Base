# Loop Engineering A2 Runtime Foundation

## Status

This package is the provider-neutral, fail-closed foundation for bounded A2 execution. It does not call a real model, create a worktree, push, merge, schedule work, or select the next product package.

## Authority

A run request must be derived from a valid Project Execution Capsule and its approved Implementation Package. Callers cannot provide broader `allowed_paths`, weaker `forbidden_paths`, different Resource Locks, a different project, or a different authority SHA.

```text
Planning Lock + Visual Lock + Package + Coverage
→ M2 bundle validation
→ A2 Run Request
→ Builder result
→ deterministic scope gate
→ read-only Critic result
→ WAITING_INTEGRATION or a fail-closed state
```

## Implemented states

```text
STALE_BASE_SHA
PROVIDER_FAILURE
QUARANTINED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
NO_PROGRESS
REPAIR_LIMIT
WAITING_INTEGRATION
```

`WAITING_INTEGRATION` is not merge evidence. PR creation, Required Checks, review threads, merge SHA and postmerge readback remain later integration responsibilities.

## Provider boundary

- `FAKE` is deterministic and is used for protocol, scope, retry, redaction and burn-in tests.
- `REAL` requires both an explicit paid-provider approval gate and configured transport.
- No API key, authorization header, secret, hidden reasoning or full environment is written into receipts.
- Builder output is never accepted before project/run/package/SHA identity and changed-path validation.
- Critic `PASS` cannot override deterministic findings.

## Preserved decisions

```yaml
A3_AUTO_MERGE: DISABLED
SCHEDULER: NOT_CONFIGURED
AUTOMATIC_PACKAGE_SELECTION: FORBIDDEN
PLANNING_APPROVAL: HUMAN_ONLY
VISUAL_APPROVAL: HUMAN_ONLY
PROJECT_PRODUCT_MUTATION_IN_BASE_TESTS: NONE
```

## Deferred integration

The deterministic SHADOW Kernel is owned by a separate workstream. This foundation uses separate files and will integrate through a reviewed public interface only after that work reaches `main`.
