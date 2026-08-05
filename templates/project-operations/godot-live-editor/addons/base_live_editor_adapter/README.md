# Base Live Editor Adapter

Project-local, network-disabled Godot 4.7 Editor transaction adapter for the Base live-editor v2 contract.

## Boundary

This addon contains no MCP server, socket, HTTP/WebSocket listener, remote endpoint, background thread, Autoload, arbitrary GDScript, expression, shell command, or unrestricted property mutation.

It accepts only an already validated v2 operation envelope through the in-process `submit_validated_operation()` method. The active Manifest must be `CONFIGURED`, version 2, and declare the exact local profile below:

```yaml
transport:
  kind: PROJECT_DEFINED
  enabled: true
  bind_host: null
  endpoint_identity: in-process-editor-plugin
  access_control:
    authentication_mode: NOT_APPLICABLE
    origin_policy: NOT_APPLICABLE
    session_binding: NOT_APPLICABLE
    os_access_control: CURRENT_USER_ONLY
```

Here `enabled: true` means that the project-owned in-process execution channel is active. It does **not** enable a network listener; `network_listener_enabled` remains `false`.

Supported capabilities:

- `scene.inspect`
- `node.rename` with `KEEP_DIRTY` or `SAVE_CURRENT_SCENE`

## Installation

1. Copy `base_live_editor_adapter/` into `res://addons/`.
2. Configure `res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` with exact project identity, catalog hashes, closed input/output Schemas, the exact in-process profile, and the two declared EditorPlugin capabilities.
3. Validate the Manifest and every operation with the pinned Base v2 Schema and semantic validator.
4. Enable `Base Live Editor Adapter` in Godot Project Settings → Plugins.
5. Submit only prevalidated envelopes from project-owned in-process tooling.

The addon remains unavailable with `ADAPTER_NOT_CONFIGURED` for a missing, malformed, v1, `NOT_CONFIGURED`, identity-incomplete, capability-empty, network-bound, or non-exact transport profile.

## Execution and evidence

The Editor frame performs fresh state observation, `TARGET_STATE_CONFLICT` checking, full approval-token binding and expiry checking, atomic STARTED ledger persistence, one `EditorUndoRedoManager` action, dirty/save handling, filesystem update, physical byte hashing, typed output validation, evidence write, and one terminal `COMPLETED` or `FAILED` record.

`KEEP_DIRTY` requires `DIRTY` output and does not claim a saved-file hash. `SAVE_CURRENT_SCENE` succeeds only after `save_scene()`, `update_file()`, physical SHA-256 verification, `CLEAN` output, and a valid saved-file hash.

## Efficiency boundary

- pending requests and retained results are both bounded to 64 entries;
- at most one request is executed per Editor frame;
- operation and evidence identifiers are capped at 128 ASCII-safe characters;
- file hashing streams 64 KiB chunks instead of loading the full file into memory;
- ledger and evidence JSON are compact rather than pretty-printed.

Fresh stale-state checks still hash the active Scene file, so observation cost is linear in the Scene file size. Large projects must measure this in their own Pilot rather than treating the static limits as performance proof.

## Recovery and removal

On plugin startup failure:

1. stop all operation submission;
2. launch Godot with `--recovery-mode`;
3. disable the addon or remove `res://addons/base_live_editor_adapter/`;
4. verify normal Editor startup;
5. regenerate the Editor instance ID and any required approval before resuming.

Removing this addon does not remove operation/evidence records under `res://artifacts/godot-live-editor/`; archive or delete them only through the project retention policy.

## Readiness

This addon proves only PR B's in-process Editor transaction boundary after actual Runtime execution. Authenticated transport, optional MCP mapping, runtime debugger, two structurally different real-project pilots, Windows production operation, physical input, and human usability remain separate gates. `PRODUCTION_ADAPTER_READY` remains `NOT_READY`.
