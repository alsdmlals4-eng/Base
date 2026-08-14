# Loop Engineering A2 Runtime Foundation

## Status

This package is the provider-neutral, fail-closed foundation for bounded A2 execution. It does not call a real model, create a worktree, push, merge, schedule work, or select the next product package.

## Authority

A run request must be derived from a valid Project Execution Capsule and its approved Implementation Package. Callers cannot provide broader `allowed_paths`, weaker `forbidden_paths`, different Resource Locks, a different project, omitted Requirement IDs, or a different authority SHA.

```text
Planning Lock + Visual Lock + Package + Coverage
→ M2 bundle validation
→ A2 Run Request
→ Builder result
→ identity / cumulative budget / deadline / scope gate
→ read-only Critic result
→ Critic authority and coverage gate
→ WAITING_INTEGRATION or a fail-closed state
```

The A2 runtime independently protects repository-control surfaces even if a malformed Package tries to allow them:

```text
.git/**
.github/**
AGENTS.md
SECURITY.md
```

The Critic cannot introduce a Requirement ID or path outside the approved Package. A Critic `PASS` must cover exactly the approved Requirement IDs, contain no Findings, and cannot override any deterministic failure.

## Implemented states

```text
STALE_BASE_SHA
PROVIDER_FAILURE
PROVIDER_TIMEOUT
BUDGET_EXCEEDED
QUARANTINED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
NO_PROGRESS
REPAIR_LIMIT
WAITING_INTEGRATION
```

`WAITING_INTEGRATION` is not merge evidence. For `provider_mode=FAKE`, it is only a deterministic protocol simulation and is never evidence that a repository Diff exists. PR creation, exact-head Required Checks, review threads, merge SHA, postmerge main readback, and product Runtime evidence remain separate responsibilities.

## Provider boundary

- `FAKE` is deterministic and is used only for protocol, scope, retry, redaction, failure injection, and three-run burn-in tests.
- `REAL` requires both an explicit paid-provider approval gate and configured transport.
- The real Codex Builder and GPT Critic are not implemented by this foundation.
- No API key, authorization header, access/refresh token, client secret, hidden reasoning, or full environment is written into receipts.
- Builder and Critic project/run/package/SHA identity must match the Run Request.
- Builder Turn usage is cumulative across repairs and cannot exceed `max_turns`.
- The Foundation detects an elapsed Run deadline after each Provider call and blocks further verification as `PROVIDER_TIMEOUT`.
- An actual external Worker Adapter must additionally terminate its subprocess or transport at the deadline; this Foundation does not claim hard cancellation of an in-process Provider call.
- `COMPLETED` Worker results cannot contain errors. `FAILED` and `BLOCKED` results must include bounded error evidence.

## Preserved decisions

```yaml
A3_AUTO_MERGE: DISABLED
SCHEDULER: NOT_CONFIGURED
AUTOMATIC_PACKAGE_SELECTION: FORBIDDEN
PLANNING_APPROVAL: HUMAN_ONLY
VISUAL_APPROVAL: HUMAN_ONLY
PROJECT_PRODUCT_MUTATION_IN_BASE_TESTS: NONE
REAL_PROVIDER: NOT_RUN_USER_DECISION_REQUIRED
```

## Deferred integration

The deterministic SHADOW Kernel is owned by a separate workstream. This Foundation uses separate files and will integrate through a reviewed public interface only after that work reaches `main`.

The following remain separate implementation slices:

```text
real Codex SDK Builder transport
real read-only GPT Critic transport
hard subprocess/transport timeout
isolated Git worktree mutation
actual Git Diff collection
project test execution
PR handoff
postmerge closure
cross-project pilots
```
