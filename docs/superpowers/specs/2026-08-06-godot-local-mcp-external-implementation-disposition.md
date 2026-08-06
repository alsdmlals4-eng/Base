# Godot Local MCP External Implementation Disposition

## Status

```yaml
status: REVIEWED
review_date: 2026-08-06
merge_authorization: NOT_GRANTED
production_adapter_ready: false
recommended_single_authority:
  gateway: Base PR #201
  godot_bridge: Base PR #202 after Core review and merge
```

This document records the required comparison against existing public Godot agent implementations and the handoff from the earlier Base/Switchy work. It prevents a second MCP server or Godot Bridge from becoming a competing authority.

## Exact reviewed snapshots

```yaml
hera_agent_godot:
  repository: NotNull92/hera-agent-godot
  commit: 7c4ee23a24b493b5d64c8114ce1a04988f1d537d
  version_line: v1.0.0
  license: MIT

hi_godot:
  repository: hi-godot/godot-ai
  commit: 678b16a6a0a335cf80cbb7d3f85c183cd3e616de
  version: 3.1.2
  license: MIT

base_gateway:
  repository: alsdmlals4-eng/Base
  branch: agent/godot-local-mcp-gateway-core
  pull_request: 201
  head: 1b6f31353c9ffd737e3d1bac9337a8ee5a5e99ca

base_bridge_checkpoint:
  repository: alsdmlals4-eng/Base
  branch: agent/godot-local-mcp-editor-bridge
  pull_request: 202
  head: d858d4df5efdbd57563f57487ce97feb57e416de
  state: PARTIAL_WIP_CHECKPOINT
```

## Classification summary

| Implementation | Actual role | Disposition | Reason |
|---|---|---|---|
| Base Gateway PR #201 | closed six-tool MCP stdio Gateway | `REUSE` and retain as authority | already matches client isolation, project fingerprint, exact tool surface, result redaction, and authenticated Bridge direction |
| Base Bridge PR #202 | authenticated Godot-side Bridge | `REFACTOR` before continuation | correct architectural role, but the checkpoint is incomplete and approval/editor binding is not yet sufficient |
| Hera Agent Godot | low-token Go CLI plus localhost HTTP Godot addon | `ABSORB` selected patterns; `ARCHIVE` as competing authority | explicitly not MCP; broad all-or-nothing editor authority and `eval` conflict with Base v1 |
| HiGodot / Godot AI | broad FastMCP HTTP server plus loopback WebSocket Godot plugin | `ABSORB` selected patterns; `REFACTOR` if code is ported; `ARCHIVE` as competing authority | mature lifecycle and tests, but broad tool surface, optional/compatibility WebSocket auth, URL/LAN modes, and no Base human-approval boundary conflict with Base v1 |
| Base PR #198 | design and implementation plans only | retain as historical design input, then mark superseded by PR #201 after approval | PR #201 already carries the approved documents and executable implementation; merging both would duplicate authority |

## Architecture comparison

| Dimension | Base PR #201 / #202 | Hera Agent Godot | HiGodot / Godot AI |
|---|---|---|---|
| Host protocol | exact `mcp==2.0.0`, stdio | shell CLI, no MCP | FastMCP, HTTP plus stdio attach bridge |
| Godot transport | authenticated length-prefixed JSON over loopback | localhost HTTP `/rpc` | Python server to Godot plugin over loopback WebSocket |
| Tool surface | exactly 6 tools | broad CLI commands including `eval` | about 43 MCP tools exposing 120+ operations |
| Client identity | exact `codex` and `gpt-vscode` profiles | one optional shared token, no model profile split | MCP client configuration and editor sessions, not Base profile authorization |
| DeepSeek denial | deny before profile file lookup | not represented | not represented as a denied client identity |
| Project binding | normalized path plus `project.godot` SHA-256 fingerprint | absolute project path in heartbeat | project path/session metadata, not Base fingerprint binding |
| Editor binding | required by design; incomplete in Bridge checkpoint | process/instance heartbeat | session ID and editor PID; no Base approval-token binding |
| Mutation approval | Godot-human-only, no model approval tool | no per-command human approval; authorized client has editor authority | write/readiness gating, but no Base Godot-human approval token lifecycle found |
| Dangerous operations | excluded | `eval` and broad editor/game mutation exist | deletion, script/file/project settings, autoload and broad mutation operations exist |
| Remote access | forbidden | loopback only | loopback default, optional LAN allow-list mode |
| Undo/evidence authority | existing Base Adapter v2 | implementation-specific editor operations | plugin batch/UndoRedo patterns, not Base ledger/evidence contract |

## Reuse without change

The following Base implementation remains authoritative:

1. `MCPServer` stdio server and exact six-tool registration.
2. `codex` and `gpt-vscode` profile allowlist and pre-discovery `deepseek` denial.
3. project fingerprint derived from resolved project root and `project.godot` bytes.
4. bounded tool inputs and method-specific result redaction.
5. HMAC-authenticated loopback frame protocol with bounded object frames.
6. no model-callable approval tool.
7. real stdio subprocess test and authenticated fake-Bridge end-to-end test.
8. existing Base Live-Editor Adapter v2 as the only Scene execution, Undo, save, ledger, evidence, and canonical-result authority.

## Absorb into Gateway

### From Hera

- compact result shaping and explicit low-token output budgets;
- optional shell/CLI diagnostic wrapper as a separate operator convenience, never as a second execution authority;
- command documentation that agents can load on demand instead of expanding the MCP tool surface.

### From HiGodot

- client-owned stdio `attach` lifecycle and safe Windows no-console launch patterns, after the Core transport is stable;
- session-owned pending-response routing so one session cannot resolve another session's request;
- malformed-frame resilience that fails the affected request without unnecessarily destroying unrelated sessions;
- domain exclusion, deferred schema loading, and rollup tools only if the Base surface later grows beyond the fixed v1 six tools;
- generated client configuration tests and port-owner classification patterns.

## Absorb into Godot Bridge

### From Hera

- atomic external discovery/heartbeat publication and the Windows retry insight for temporary destination absence;
- main-loop queue handoff pattern;
- local screenshot comparison and runtime QA ideas as later typed capabilities, not v1 tools.

### From HiGodot

- readiness snapshots on every response and live re-probe before write rejection;
- bounded wait for transient import state, while failing fast for play mode or non-transient states;
- session registry, duplicate-session rejection, connection ownership of pending responses, and request-scoped timeout handling;
- multi-OS Godot test layers, real-render screenshot smoke, and live port-conflict smoke;
- plugin/server version mismatch diagnostics and conservative external-process ownership rules.

## Must refactor before any external code is ported

Any absorbed code must be adapted to all of the following Base invariants:

1. exact six-tool v1 surface;
2. `mcp==2.0.0` stdio host boundary;
3. no HTTP MCP endpoint and no LAN mode;
4. mandatory profile credential, project fingerprint, Bridge instance, Editor instance, descriptor nonce, session, and request binding;
5. replay rejection and per-request descriptor-expiry validation;
6. `deepseek` denial before descriptor or project discovery;
7. mutation approval generated only by a Godot human Dock and bound to the exact client, project, Editor, request hash, target state, and expiry;
8. all Scene execution delegated to Base Adapter v2;
9. no arbitrary shell, GDScript evaluation, file access, deletion, project settings, addon installation, build/export, or runtime debugger in v1;
10. retained MIT copyright and permission notices for any substantial copied code.

## Must remove or never introduce

- Hera `/rpc` as a second execution transport;
- Hera `eval` or all-or-nothing shared-token authority;
- HiGodot HTTP MCP URL mode as the Base default or fallback;
- HiGodot optional/omittable WebSocket token behavior;
- HiGodot `--allow-host` LAN access;
- automatic client configuration that writes an active project `.vscode/mcp.json`;
- broad delete, arbitrary script/file, project settings, autoload, export, or game-eval surfaces;
- any `approve_operation` or equivalent model-callable approval route;
- a second Godot plugin that bypasses Base Adapter v2.

## Current Base gaps found by the comparison

### Gateway PR #201

```yaml
transitive_hash_lock: MISSING
windows_private_config_acl_verification: NOT_IMPLEMENTED
descriptor_expiry_recheck_per_request: MISSING
editor_instance_binding: MISSING_FROM_GATEWAY_HANDSHAKE
malformed_protocol_matrix: PARTIAL
real_codex_startup: NOT_RUN
real_gpt_vscode_startup: NOT_RUN
deepseek_host_profile_e2e: NOT_RUN
windows_runtime: NOT_RUN
```

### Bridge PR #202 checkpoint

```yaml
plugin_entrypoint: MISSING
loopback_server: MISSING
adapter_envelope_router: MISSING
human_approval_binding:
  client_profile: INCOMPLETE
  project: INCOMPLETE
  editor_instance: INCOMPLETE
  target_state: INCOMPLETE
  expiry: PARTIAL
profile_file_os_acl: NOT_IMPLEMENTED
descriptor_file_os_acl: NOT_IMPLEMENTED
godot_runtime_test: NOT_RUN
```

The checkpoint `human_approved` state is not sufficient approval authority and must not be treated as executable authorization.

## Missing from all reviewed implementations

No reviewed implementation provides the complete Base combination of:

- exact Codex/GPT profile isolation with explicit DeepSeek exclusion;
- cryptographic project and Editor instance binding;
- Godot-human-only one-shot approval bound to request hash and stale Scene state;
- Base Adapter v2 Undo, save verification, ledger, evidence, and canonical result hash;
- real Codex and GPT-in-VS-Code E2E plus negative DeepSeek and Windows evidence.

Therefore replacing Base wholesale with Hera or HiGodot would remove required guarantees rather than complete the work.

## PR and sequencing decision

```yaml
pr_197:
  action: leave untouched in this MCP workstream
  current_role: project Pilot prerequisite for production adoption evidence

switchy_pr_94:
  action: leave untouched until PR #197 has a green successor
  current_role: project Pilot regression evidence

pr_198:
  action: do not merge in parallel with PR #201
  recommended_later_state: SUPERSEDED_BY_PR_201

pr_201:
  action: continue as single Gateway authority
  next_work:
    - add transitive hash lock
    - bind Editor instance
    - recheck descriptor expiry
    - expand malformed/adversarial tests
    - add Windows private-config strategy

pr_202:
  action: freeze at WIP checkpoint until PR #201 is reviewed and merge-authorized
  next_work_after_core:
    - replace simplistic approval state with full bound approval record
    - implement plugin/server/router
    - run isolated Godot 4.7.1 E2E
```

The isolated Gateway can progress independently of PR #197. Actual project adoption, real source-project mutation, and any production-readiness discussion remain gated on corrected Pilot evidence, Switchy re-pin, Windows runtime, human approval usability, and a second distinct project.
