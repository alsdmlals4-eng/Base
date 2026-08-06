# Godot Local MCP Gateway Core Scope Amendment

## Status

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approval_time: 2026-08-06T12:37:00+09:00
implementation_branch: agent/godot-local-mcp-gateway-core
production_adapter_ready: false
```

## User direction

Build the Godot MCP itself without returning to unrelated Pilot expansion. The Gateway Core proceeds independently against an authenticated fake Bridge. The real Godot Bridge and project E2E retain their own runtime gates.

## Authoritative v1 tool surface

This list supersedes the four-tool names in the earlier design and plans.

```yaml
tools:
  - godot_doctor
  - godot_status
  - godot_catalog
  - godot_scene_inspect
  - godot_node_rename
  - godot_task_status
```

No other MCP tool is exposed. In particular, no model-callable approval, shell, arbitrary file, arbitrary GDScript, deletion, project-settings mutation, addon installation, build/export, debugger, or network-listener tool exists.

## Gateway Core boundary

The current implementation must deliver:

1. a Python 3.12 stdio MCP server using exactly `mcp==2.0.0`;
2. exact profile authorization for `codex` and `gpt-vscode` and fail-closed denial for `deepseek` and unknown profiles;
3. project identity derived from normalized project path plus `project.godot` SHA-256;
4. closed, bounded tool inputs and structured outputs;
5. a Bridge client abstraction with an authenticated fake Bridge used by protocol tests;
6. in-memory MCP SDK tests and a real stdio subprocess smoke test;
7. host configuration examples that are profile-scoped and do not commit an active workspace `.vscode/mcp.json`.

## Deferred boundary

The following remain outside this Gateway Core PR:

- the real Godot loopback Bridge EditorPlugin;
- the human approval Dock;
- live Godot main-thread execution;
- Switchy or other project end-to-end mutation evidence;
- production readiness claims.

Those items belong to the Bridge/E2E implementation plan after the Gateway Core is reviewed.

## SDK authority

```yaml
python: "3.12"
mcp_python_sdk: "2.0.0"
mcp_protocol_family: "2026-07-28 with SDK compatibility"
transport_to_host: stdio
```

The official SDK imports are:

```python
from mcp import Client
from mcp.server import MCPServer
```

`MCPServer.run()` owns stdio serving. Tests use `Client(server)` for in-memory protocol verification and a subprocess client for real stdio verification.
