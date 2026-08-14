# Loop Engineering A2 Runtime Foundation

## Status

This package is the provider-neutral, fail-closed foundation for bounded A2 execution. The base Foundation is merged, and a follow-up worktree adapter now proves FAKE-mode isolated Git mutation and actual Diff attestation. It still does not call a real model, push or merge project work, schedule work, or select the next product package.

## Authority

A run request must be derived from a valid Project Execution Capsule and its approved Implementation Package. Callers cannot provide broader `allowed_paths`, weaker `forbidden_paths`, different Resource Locks, a different project, omitted Requirement IDs, or a different authority SHA.

```text
Planning Lock + Visual Lock + Package + Coverage
→ M2 bundle validation
→ A2 Run Request
→ isolated FAKE worktree Builder
→ actual Git Diff attestation
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

`WAITING_INTEGRATION` is not merge evidence. For `provider_mode=FAKE`, it is only a deterministic execution/evidence state. PR creation, exact-head Required Checks, review threads, merge SHA, postmerge main readback, and product Runtime evidence remain separate responsibilities.

## FAKE worktree and Diff boundary

The follow-up `GitWorktreeBuilderAdapter` provides a bounded local execution surface for deterministic tests:

- the tested source repository remains clean while mutation occurs in an external detached Git worktree;
- the requested `expected_main_sha` must already exist in the source repository;
- the runtime root must be outside the project repository;
- changed-path evidence is collected from Git (`git diff ... HEAD` plus **all** untracked files, including ignored untracked files), not trusted from Worker claims;
- declared-vs-actual changed-path mismatch fails closed;
- actual out-of-scope changes reach the existing deterministic Runtime scope gate before Critic execution;
- subprocess execution uses argv directly without shell expansion;
- the subprocess receives a small allowlisted environment and does not inherit `OPENAI_API_KEY` or general parent secrets;
- a bounded subprocess timeout returns `WORKER_TIMEOUT`;
- cleanup removes only external worktrees created by the current Adapter instance and preserves unowned path collisions.

This generic subprocess adapter is intentionally **FAKE-only**. A `provider_mode=REAL` request returns `WORKER_PROVIDER_MODE_UNSUPPORTED` before the subprocess runs. A later real-provider adapter requires a separately reviewed sandbox/credential/transport boundary.

Worktree ownership is currently process-local to the Adapter instance. Automatic recovery/reuse of a worktree after process restart is **not implemented**; a durable resume checkpoint and lease handoff are separate work.

The timeout proves termination of the direct worker process used by this adapter. It does not claim a general OS sandbox or guaranteed process-tree termination for arbitrary descendants.

## Provider boundary

- `FAKE` is deterministic and is used only for protocol, scope, retry, redaction, failure injection, isolated-worktree, actual-Diff, and burn-in tests.
- `REAL` requires both an explicit paid-provider approval gate and a separately implemented sandboxed transport.
- The real Codex Builder and GPT Critic are not implemented by the current runtime.
- No API key, authorization header, access/refresh token, client secret, hidden reasoning, or full environment is written into receipts.
- Builder and Critic project/run/package/SHA identity must match the Run Request.
- Builder Turn usage is cumulative across repairs and cannot exceed `max_turns`.
- The core Runtime detects an elapsed Run deadline after each Provider call and blocks further verification as `PROVIDER_TIMEOUT`.
- The FAKE subprocess adapter additionally enforces a direct subprocess timeout.
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

The deterministic SHADOW Kernel is owned by a separate workstream. This A2 work continues on isolated files and may integrate through a reviewed public interface only after that work reaches `main`.

The following remain separate implementation slices:

```text
sandboxed real Codex SDK Builder transport
real read-only GPT Critic transport
durable worktree resume / lease handoff after process restart
project test-command execution and evidence capture
PR handoff
postmerge closure
cross-project pilots
```
