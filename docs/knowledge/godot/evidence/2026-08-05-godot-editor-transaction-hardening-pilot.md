# Godot Editor Transaction Adapter Hardening Pilot Evidence

## Scope

This record covers the adversarial hardening layered on the merged PR #165 Editor transaction adapter.

```yaml
repository: alsdmlals4-eng/Base
pull_request: 166
runtime_reviewed_head: d88917d404958f8036d4e9e4f6b4f11e4092a096
base_main: 48273f79ab261a1f064adfc7431c99a74a22c33a
engine: 4.7.1.stable.official.a13da4feb
mode: --editor --headless
platform: Linux x86_64
production_adapter_ready: false
```

The Pilot exercises only the project-owned in-process `PROJECT_DEFINED / in-process-editor-plugin` profile. It does not add or validate a socket, HTTP, WebSocket, MCP, remote endpoint, background thread, or Autoload.

## Binary identity

The locally materialized official Godot archive and executable were verified before execution.

```yaml
archive: Godot_v4.7.1-stable_linux.x86_64.zip
archive_sha256: c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba
executable_sha256: 32f8d7596c4b41185512b1c49d69f2da3be018fd784a53e349fa92a98a97bcde
reported_version: 4.7.1.stable.official.a13da4feb
```

## TDD RED evidence

### Contract and static RED

Test-only commit `acb0f60cd3b96ba4de8b9760ef5f48ec3b77d3fd` was run through the required Base workflow before production fixes.

```yaml
tests_run: 171
failures: 8
errors: 1
skipped: 1
generated_and_integrity_checks_before_failure: PASS
```

The failures reproduced these defects:

- normal operation IDs containing digits were rejected;
- ledger and evidence replacement removed the previous destination before rename;
- runtime approval validation omitted full token binding and expiry;
- output validation checked keys but not types or save-mode/hash relationships;
- the configured in-process Pilot profile conflicted with the earlier disabled transport representation;
- the actual Runtime test correctly skipped without `GODOT_BIN`.

### Actual Godot Runtime RED

The first hardening Runtime attempt loaded Godot 4.7.1 but failed before Plugin initialization.

```yaml
process_exit_status: 0
runtime_result: MISSING
parse_errors:
  - request_hash dynamic return type could not be inferred
  - expected result-hash dynamic return type could not be inferred
```

Both Pilot variables were changed to explicit `String` declarations and covered by static regression checks before rerunning.

## Implemented hardening

- recompute canonical request material and reject `REQUEST_HASH_MISMATCH` before enqueue and before execution;
- bind approval to operation, capability, project, instance, snapshot, policy, request hash and preconditions;
- parse RFC 3339 `Z` and numeric-offset approval expiry fail-closed;
- validate output types and `KEEP_DIRTY` / `SAVE_CURRENT_SCENE` cross-field semantics;
- accept bounded ASCII-safe operation/evidence identifiers with digits;
- replace atomic JSON records without unlinking the prior target first;
- emit canonical `result_hash` and RFC 3339 evidence/ledger timestamps;
- preserve one canonical JSON/hash implementation in the runtime guard;
- add a stale-precondition negative Runtime case;
- add an actual 64-request bounded queue/throughput Runtime case.

## Actual Runtime GREEN

The hardened Pilot completed with no stderr and exit status 0.

```yaml
status: PASS
scene_inspect: PASS
node_rename_keep_dirty: PASS
editor_undo: PASS
node_rename_save_current_scene: PASS
stale_state_block: PASS
stale_code: TARGET_STATE_CONFLICT
canonical_result_hash: PASS
ledger_states: [COMPLETED, COMPLETED]
queue_capacity_64: PASS
request_65: QUEUE_FULL
batch_64_completed: 64
network_listener_enabled: false
saved_scene_byte_sha256: PASS
```

The stale request produced no mutation and no mutation ledger entry.

## Efficiency evidence

Three fresh isolated Editor runs executed the 64-request read-only batch after the mutation and stale-state cases.

```yaml
runs: 3
passes: 3
batch_size: 64
batch_elapsed_usec:
  - 444705
  - 444301
  - 444063
batch_elapsed_usec_median: 444301
throughput_ops_per_second_median: 144.0
per_operation_usec_median: 6942.2
process_wall_ms:
  - 8486
  - 3747
  - 3756
```

The throughput includes the deliberate one-request-per-Editor-frame policy and evidence generation in a minimal Scene. It is not a large-project benchmark. Scene observation hashes the active `.tscn`, so cost remains linear in Scene file size.

Two longer repeated-process loops stalled on their eighth clean Editor launch before project initialization and produced no Plugin stderr or result. A fresh standalone launch immediately passed. This is recorded as `EDITOR_PROCESS_SOAK_FLAKE: BLOCKED_ENVIRONMENT`, not as adapter PASS or adapter failure. Process-start soak reliability is therefore not proven by this evidence.

## Evidence boundaries

The exact repository materializer was statically validated by GitHub CI. The hardening Runtime replay used the exact Runtime file blobs and an equivalent isolated configured in-process Manifest because external repository archive download was unavailable in the execution container.

```yaml
exact_runtime_file_blobs: VERIFIED
isolated_godot_runtime_path: PASS
exact_materializer_to_runtime_replay_on_hardening_head: NOT_RUN
large_project_performance: NOT_RUN
real_project_pilots: NOT_RUN
windows_production_operation: NOT_RUN
production_transport: NOT_IMPLEMENTED
mcp_profile: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
physical_input: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

## Verdict

The closed in-process adapter functions under the isolated Godot 4.7.1 Editor Pilot, rejects stale requests, preserves canonical hash and approval boundaries, enforces its queue ceiling, and completes the bounded 64-request batch consistently in completed runs. This supports PR B hardening readiness only; it does not satisfy production transport, real-project adoption, Windows, soak, or human usability gates.
