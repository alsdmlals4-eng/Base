# Base Live Editor Adapter

Project-local, network-disabled Godot 4.7 Editor transaction adapter for the Base live-editor v2 contract.

## Boundary

This addon contains no MCP server, socket, HTTP/WebSocket listener, remote endpoint, background thread, Autoload, arbitrary GDScript, expression, shell command, or unrestricted property mutation.

It accepts only an already validated v2 operation envelope through the in-process `submit_validated_operation()` method. The active Manifest must be `CONFIGURED`, version 2, and use `transport.kind: DISABLED` with `enabled: false`.

Supported capabilities:

- `scene.inspect`
- `node.rename` with `KEEP_DIRTY` or `SAVE_CURRENT_SCENE`

## Installation

1. Copy `base_live_editor_adapter/` into `res://addons/`.
2. Configure `res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` with exact project identity, catalog hashes, closed input/output Schemas, and the two declared EditorPlugin capabilities.
3. Validate the Manifest and every operation with the pinned Base v2 Schema and semantic validator.
4. Enable `Base Live Editor Adapter` in Godot Project Settings → Plugins.
5. Submit only prevalidated envelopes from project-owned in-process tooling.

The addon remains unavailable with `ADAPTER_NOT_CONFIGURED` for a missing, malformed, v1, `NOT_CONFIGURED`, transport-enabled, identity-incomplete, or capability-empty Manifest.

## Execution and evidence

The Editor frame performs fresh state observation, `TARGET_STATE_CONFLICT` checking, atomic STARTED ledger persistence, one `EditorUndoRedoManager` action, dirty/save handling, filesystem update, physical byte hashing, output validation, evidence write, and one terminal `COMPLETED` or `FAILED` record.

`KEEP_DIRTY` does not claim a saved-file hash. `SAVE_CURRENT_SCENE` succeeds only after `save_scene()`, `update_file()`, and physical SHA-256 verification.

## Recovery and removal

On plugin startup failure:

1. stop all operation submission;
2. launch Godot with `--recovery-mode`;
3. disable the addon or remove `res://addons/base_live_editor_adapter/`;
4. verify normal Editor startup;
5. regenerate the Editor instance ID and any required approval before resuming.

Removing this addon does not remove operation/evidence records under `res://artifacts/godot-live-editor/`; archive or delete them only through the project retention policy.

## Readiness

This addon proves only PR B's in-process Editor transaction boundary. Authenticated transport, optional MCP mapping, runtime debugger, two structurally different real-project pilots, Windows production operation, physical input, and human usability remain separate gates. `PRODUCTION_ADAPTER_READY` remains `NOT_READY`.
