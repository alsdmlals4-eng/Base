# Godot Production Adapter Readiness

## Purpose

This document separates an isolated Godot contract pilot from a production-ready editor automation adapter. A successful CLI fixture or EditorPlugin load marker is evidence for that exact boundary only. It must not be promoted to `PRODUCTION_ADAPTER_READY`.

## Reference architecture

```text
MCP STDIO or project CLI
→ authenticated loopback ingress or local process boundary
→ bounded request queue
→ EDITOR_MAIN_THREAD typed executor
→ EditorUndoRedoManager transaction
→ explicit save / import / refresh boundary
→ atomic operation ledger and bounded evidence
```

The transport handler must never mutate `SceneTree`, `Resource`, `EditorInterface`, or `ProjectSettings` directly. It validates and queues a closed request, then the editor main thread executes the registered capability.

## Machine and runtime gates

A production adapter is ready only when every applicable gate has executable evidence:

```yaml
closed_arguments_schema: CONTRACT_PASS
runtime_request_validation: RUNTIME_PASS
project_identity_and_catalog: RUNTIME_PASS
editor_main_thread_serialization: RUNTIME_PASS
editor_undo_redo_transaction: RUNTIME_PASS
save_and_dirty_state_boundary: RUNTIME_PASS
approval_expiration_and_single_use: RUNTIME_PASS
atomic_operation_ledger: RUNTIME_PASS
loopback_auth_and_bounded_framing: RUNTIME_PASS_OR_NOT_APPLICABLE
plugin_load_unload_cleanup: RUNTIME_PASS
runtime_debugger_bridge: RUNTIME_PASS_OR_NOT_APPLICABLE
physical_input_validation: NOT_RUN_OR_SEPARATE_EVIDENCE
human_editor_usability: HUMAN_PASS
```

`arguments_schema` must be an object schema with `additionalProperties: false`. Runtime validation is still mandatory; handlers do not trust the manifest label alone.

## Approval and ledger ordering

Approval is bound to project fingerprint, capability, operation class, request hash, and operation ID. The adapter compares expiry with current UTC time and records token consumption as single-use.

For a mutation, the durable sequence is:

1. Validate identity, catalog, request, approval, and operation conflict.
2. Atomically persist `STARTED`, request hash, and approval-token consumption.
3. Perform the bounded mutation on the editor main thread.
4. Persist `COMPLETED` or `FAILED` with stable result code and evidence binding.

A failure before task creation uses `NOT_STARTED` with no fabricated `task_id`. A timeout never causes blind mutation replay.

## Editor mutation contract

Scene and resource changes use `EditorPlugin.get_undo_redo()` / `EditorUndoRedoManager` where the capability is undoable. The action registers do/undo methods, commits once, and records whether the edited scene became dirty. Save is explicit and separately evidenced.

A capability that cannot be made undoable declares that limitation, requires the appropriate operation class and approval, and provides a recovery path.

## Transport boundary

- STDIO keeps stdout protocol-only; diagnostics use stderr and credentials come from environment or the invoking client.
- TCP or WebSocket is loopback-only, authenticates the session, limits frame size, connection count, request depth, batch size, and idle lifetime, and closes all peers in `_exit_tree()`.
- Remote HTTP is unsupported by default. An explicitly approved remote adapter requires HTTPS and the current MCP authorization boundary, including OAuth 2.1 where applicable.
- The runtime debugger bridge is an opt-in `EditorDebuggerPlugin` / `EditorDebuggerSession` / `EngineDebugger` capability, not an automatic Autoload.

## Pilot boundary

`examples/godot-live-editor-pilot/` proves typed CLI execution, project identity, catalog freshness, closed requests, approval expiry and single use, idempotent replay, durable task resume, bounded writes, and no-network EditorPlugin lifecycle on Godot 4.7.1.

It does not implement editor main-thread scene mutation, Undo/Redo, authenticated network transport, runtime debugger control, project behavior tests, physical input, or human usability. Its production state is `NOT_READY`.
