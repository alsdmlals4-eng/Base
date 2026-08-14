# Loop A2 Runtime Foundation Evidence

## Identity and ownership

- Tracking: Base issue `#342`.
- M2 dependency: PR `#333` merged before this implementation branch opened.
- M2 main at branch creation: `b1317f2c1b83e57f016ce4efd4e169bf7c0acd90`.
- Other-workstream exclusions: PR `#337` M3 paths and PR `#312` Adapter/visual paths.
- This PR owns only `tools/loop_a2_runtime/**`, `tools/loop_a2.py`, three `loop-a2-*` Schemas, `test_loop_a2_*`, its dedicated Workflow, documentation, and this evidence record.

## TDD and adversarial evidence

1. Initial isolated RED: protocol/runtime modules absent; three test modules failed to import.
2. Initial GREEN: protocol, M2 contract bridge, path scope, stale SHA, redaction, no-progress, independent Critic, Schema and CLI tests passed.
3. Exact-head run `31760783443`: `33` A2 tests passed against the real M2 Template; Fake Provider burn-in completed three consecutive protocol runs with zero out-of-scope writes and zero false completion claims.
4. Adversarial RED run `31760982107`: six intentional failures proved missing system-path protection, Critic requirement/path containment, cumulative Turn budget enforcement, and Worker status/error consistency.
5. The six findings were fixed in Runtime, Protocol, Scope, and Worker Schema.
6. Deadline RED run `31761285512`: the injected Provider elapsed beyond `timeout_seconds` and the unpatched Runtime failed to stop it.
7. The Runtime now detects cumulative elapsed deadline after each Provider call and returns `PROVIDER_TIMEOUT`. Hard termination remains an external Worker Adapter responsibility and is not claimed here.
8. Schema and Python Protocol independently reject contradictory Worker completion/failure evidence.

## Burn-in meaning

The deterministic Fake Provider is a protocol and failure-injection fixture. Its internal success state is not evidence that a repository Diff, PR, merge, runtime result, or player-facing behavior exists.

```yaml
FAKE_PROVIDER_RUNS: 3
OUT_OF_SCOPE_WRITES: 0
FALSE_COMPLETION_CLAIMS: 0
REAL_CODEX_BUILDER: NOT_IMPLEMENTED
REAL_GPT_CRITIC: NOT_IMPLEMENTED
REAL_OPENAI_API: NOT_RUN_USER_DECISION_REQUIRED
```

## Preserved boundaries

The Foundation does not claim:

- Codex SDK execution;
- GPT Critic model behavior;
- hard cancellation of an in-process Provider call;
- isolated Git worktree mutation;
- actual Git Diff collection or project tests;
- PR handoff or postmerge closure;
- Blacksmith, narrative/data, or visual/UI project readiness;
- A3 auto-merge or Scheduler operation.

Final integration evidence is the Ready-state exact HEAD, complete repository workflows, independent P0/P1 review, zero unresolved review threads, merge SHA, postmerge main readback, and push workflows.
