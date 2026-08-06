# Godot Local MCP Gateway Design Approval and SDK Amendment

## Status

```yaml
design_architecture: APPROVED_BY_USER
approval_time: 2026-08-06T12:15:00+09:00
original_design: docs/superpowers/specs/2026-08-06-godot-local-mcp-gateway-design.md
implementation: NOT_STARTED
implementation_authorization: NOT_GRANTED
production_adapter_ready: false
```

## Scope of this amendment

The user-approved architecture, client permissions, DeepSeek denial boundary, tool surface, approval model, localhost Bridge, prerequisites, and readiness limits remain unchanged.

This amendment corrects one dependency statement that became stale between initial design drafting and written-spec approval.

## MCP Python SDK correction

The original design targeted the stable `mcp` 1.x line because 2.x was described as pre-release at drafting time. The official package now publishes `mcp==2.0.0` as the current stable release and keeps 1.x as a maintenance line.

The implementation authority is therefore:

```yaml
python: "3.12"
mcp_python_sdk: "2.0.0"
mcp_protocol_family: "2026-07-28 or SDK-negotiated compatible revision"
mcp_v1_line: NOT_SELECTED
dependency_locking: EXACT_VERSION_AND_HASHES
```

Implementation must use the current v2 API surface:

```python
from mcp import Client
from mcp.server import MCPServer
```

The stdio server runs through `MCPServer.run()`. Protocol tests use the SDK `Client` in memory and through a real stdio subprocess.

## Plan decomposition

The design is decomposed into two independently reviewable implementation plans:

1. `docs/superpowers/plans/2026-08-06-godot-local-mcp-gateway-core.md`
   - Python stdio Gateway
   - exact profile authorization
   - DeepSeek denial
   - closed schemas
   - authenticated fake-Bridge contract
   - MCP protocol and host configuration evidence

2. `docs/superpowers/plans/2026-08-06-godot-local-mcp-bridge-and-e2e.md`
   - Godot loopback Bridge
   - approval Dock
   - Base adapter delegation
   - actual Godot Runtime
   - Switchy Codex/GPT E2E
   - DeepSeek negative E2E
   - Windows and human evidence

Both plans remain blocked by the prerequisites declared in the original design.

## Prerequisite state at approval

```yaml
base_pr_197:
  state: OPEN_DRAFT
  required_before_implementation: MERGED_AND_GREEN
switchy_pr_94:
  state: OPEN_DRAFT
  required_before_implementation: GREEN_OR_EQUIVALENT_SUCCESSOR
design_plan_pr_198:
  state: OPEN_DRAFT
  merge_authorization: NOT_GRANTED
```

## Authority

When the dependency paragraph in the original design conflicts with this amendment, this amendment is authoritative. No other original design section is superseded.
