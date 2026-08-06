# Godot Local MCP Editor Bridge Scope Amendment

## Status

```yaml
status: APPROVED_FOR_IMPLEMENTATION
implementation_branch: agent/godot-local-mcp-editor-bridge
stacked_on: agent/godot-local-mcp-gateway-core
merge_authorization: NOT_GRANTED
production_adapter_ready: false
```

## Scope correction

The user directed the work to build the Godot MCP itself without returning to unrelated Pilot expansion. Therefore:

- Gateway Core and the isolated Editor Bridge fixture proceed independently.
- Base PR #197 and project Pilot work are not modified by this branch.
- Real source-project adoption, Switchy mutation evidence, Windows production evidence, and production-readiness claims remain gated and are not part of this branch.
- The Bridge PR is stacked only because the Gateway Core is not yet merged. It must be retargeted to `main` after the Core is merged.

## Bridge v1 boundary

The Bridge implements only:

```yaml
protocol: BASE_GODOT_BRIDGE_V1
bind_host: 127.0.0.1
capabilities:
  - editor.status
  - capabilities.list
  - scene.inspect
  - node.rename
  - task.status
profiles:
  - codex
  - gpt-vscode
denied_profiles:
  - deepseek
mutation_approval: GODOT_HUMAN_ONLY
```

The Gateway remains the only MCP server. The Godot plugin is a non-MCP authenticated loopback Bridge that extends `base_live_editor_adapter/plugin.gd` and delegates operations through `submit_validated_operation()` and `take_completed_result()`.

## First implementation gate

This branch must prove in an isolated Godot 4.7.1 fixture:

1. loopback-only ephemeral listener;
2. external short-lived descriptor;
3. profile and project fingerprint binding;
4. HMAC handshake and request/response binding;
5. `editor.status`, `capabilities.list`, and `scene.inspect` round trips;
6. `node.rename` returns `APPROVAL_REQUIRED` without applying a mutation;
7. `task.status` returns `PENDING_APPROVAL` for the same operation;
8. source fixture Scene remains byte-identical;
9. no model-callable approval path exists.

Human Dock approval and post-approval rename execution may be implemented after this first runtime gate, but no production-readiness claim is permitted without separate human evidence.
