# Godot Local MCP Bridge and End-to-End Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an authenticated loopback Godot Editor Bridge, human approval Dock, and complete Codex/GPT-to-Godot E2E verification that delegates all Scene execution to the existing Base live-editor adapter and denies DeepSeek before project discovery.

**Architecture:** A project-local `@tool` EditorPlugin extends the existing Base live-editor adapter, binds only `127.0.0.1`, publishes a short-lived descriptor outside the repository, authenticates one Gateway session with HMAC, and translates closed Bridge requests into inherited `submit_validated_operation()` calls. Human mutation approval is performed only in a Godot Dock; the Gateway polls the exact operation status and cannot generate approval. Runtime verification uses disposable project copies, then repeats the protocol against Switchy with separate Codex and GPT profiles and a negative DeepSeek profile.

**Tech Stack:** Godot 4.7.1-stable, GDScript, Python 3.12, Gateway package from the companion core plan, MCP Python SDK 2.0.0, JSON Schema Draft 2020-12, `unittest`, GitHub Actions on Ubuntu and Windows.

## Global Constraints

- Complete and review the Gateway Core implementation PR before starting this plan.
- Do not start until Base PR #197 or an equivalent successor is merged and green.
- Do not start until Switchy PR #94 or an equivalent re-pinned successor is green.
- Create a new Bridge implementation branch from then-current Base `main`; do not stack production implementation on the design or Gateway branch.
- Preserve a test-only RED commit before Bridge production files exist.
- Use exact Godot `4.7.1-stable`.
- The Bridge binds only `127.0.0.1`; wildcard, LAN, remote, IPv6-any, HTTP, WebSocket, UDP, and browser access are unsupported.
- The Bridge protocol is `BASE_GODOT_BRIDGE_V1`, not MCP.
- The Gateway remains the only MCP server.
- The Bridge plugin extends the existing `base_live_editor_adapter/plugin.gd` and delegates execution through its public queue/result interfaces.
- The Bridge must not bypass `submit_validated_operation()`, `take_completed_result()`, main-thread execution, stale checks, approval binding, Undo/Redo, save verification, ledger, or evidence.
- The Bridge descriptor and credentials live outside the repository.
- Authorized profiles are exactly `codex` and `gpt-vscode`; `deepseek` is denied before descriptor discovery or tool availability.
- Human approval is required for `node.rename`.
- No MCP or Bridge message can approve its own mutation.
- A test-only approval broker is allowed only in disposable automated fixtures and must be mechanically absent from adoption templates.
- v1 tools remain exactly status, inspect, rename, and operation status.
- No arbitrary file access, script execution, shell, deletion, project settings, addon installation, import mutation, build/export, runtime debugger, or remote access.
- The source project must remain byte-identical in all automated Pilots.
- Windows Runtime and real VS Code/Codex startup are required evidence before any production-readiness discussion.
- Human approval Dock evidence is independent from automated broker evidence.
- Do not modify the Base Skill Registry, released locks, or frozen release snapshots.
- `production_adapter_ready` remains `false`.
- Stop the implementation PR before merge until explicit user authorization.

---

## Planned File Map

### Create

```text
templates/project-operations/godot-local-mcp/
  addons/base_godot_mcp_bridge/
    plugin.cfg
    plugin.gd
    bridge_server.gd
    bridge_session.gd
    bridge_codec.gd
    profile_store.gd
    descriptor_store.gd
    approval_store.gd
    approval_dock.gd
    approval_card.tscn
    adapter_router.gd
    README.md
  GODOT_LOCAL_MCP_ADOPTION_MANIFEST.example.json

examples/godot-local-mcp-bridge-pilot/
  project.godot
  GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json
  scenes/bridge_fixture.tscn
  scripts/bridge_fixture.gd
  addons/base_live_editor_adapter/
  addons/base_godot_mcp_bridge/
  tests/test_approval_broker.gd
  tests/run_bridge_runtime.gd
  .gitignore
  README.md

tools/
  materialize_godot_local_mcp_bridge_pilot.py
  run_godot_local_mcp_bridge_pilot.py
  run_godot_local_mcp_switchy_e2e.py

tests/
  test_godot_local_mcp_bridge_contract.py
  test_godot_local_mcp_bridge_runtime.py
  test_godot_local_mcp_switchy_e2e.py
  fixtures/godot-local-mcp/
    bridge-runtime/
    switchy-e2e/

docs/knowledge/godot/
  GODOT_LOCAL_MCP_BRIDGE.md
  evidence/
    2026-08-06-godot-local-mcp-bridge-runtime.md
    2026-08-06-switchy-local-mcp-e2e.md

.github/workflows/
  validate-godot-local-mcp-bridge.yml
  validate-godot-local-mcp-windows.yml
```

### Modify

```text
templates/project-operations/godot-local-mcp/README.md
templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md
docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md
docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md
docs/DOCUMENTATION_MAP.md
tests/test_godot_live_editor_contract_v2.py
```

The exact companion owner files must be re-evaluated on fresh `main`. Extend existing canonical documents and tests instead of adding duplicate authority.

---

### Task 1: Establish Test-Only RED for the Bridge and Runtime

**Files:**
- Create: three Bridge/E2E Python test modules
- Create: minimal runtime fixture descriptors under `tests/fixtures/`
- Modify: required CI discovery owner

**Interfaces:**
- Consumes: reviewed Gateway Core package interfaces.
- Produces: failing contract and Runtime tests for Bridge files, loopback binding, descriptor lifecycle, approval Dock, adapter delegation, and E2E profile behavior.

- [ ] **Step 1: Define static Bridge contract tests**

Use exact methods:

```python
class GodotLocalMcpBridgeContractTests(unittest.TestCase):
    def test_required_bridge_files_exist(self) -> None: ...
    def test_bridge_plugin_extends_existing_adapter(self) -> None: ...
    def test_bridge_binds_only_ipv4_loopback(self) -> None: ...
    def test_bridge_protocol_is_not_mcp(self) -> None: ...
    def test_bridge_never_calls_executor_directly(self) -> None: ...
    def test_rename_requires_human_approval(self) -> None: ...
    def test_no_approval_tool_or_remote_endpoint_exists(self) -> None: ...
    def test_test_approval_broker_is_absent_from_adoption_template(self) -> None: ...
    def test_descriptor_path_is_outside_res_and_user(self) -> None: ...
    def test_adoption_manifest_is_not_configured_by_default(self) -> None: ...
```

Require source strings:

```gdscript
extends "res://addons/base_live_editor_adapter/plugin.gd"
const BIND_HOST := "127.0.0.1"
const PROTOCOL := "BASE_GODOT_BRIDGE_V1"
```

Forbid:

```text
0.0.0.0
::
WebSocket
HTTPServer
PacketPeerUDP
OS.execute
Expression.new
GDScript.new
_editor_transaction_executor
```

The test may permit inherited adapter internals only through `super`, `submit_validated_operation`, `take_completed_result`, `availability`, and `editor_instance_id`.

- [ ] **Step 2: Define Runtime test interface**

```python
class GodotLocalMcpBridgeRuntimeTests(unittest.TestCase):
    def test_missing_godot_reports_skipped_not_configured(self) -> None: ...

    @unittest.skipUnless(
        os.environ.get("GODOT_BIN"),
        "SKIPPED_NOT_CONFIGURED: set GODOT_BIN to exact Godot 4.7.1",
    )
    def test_actual_bridge_runtime(self) -> None: ...
```

Required result flags:

```python
REQUIRED_FLAGS = (
    "bridge_loopback_only_pass",
    "descriptor_outside_repository_pass",
    "descriptor_expiry_pass",
    "profile_codex_auth_pass",
    "profile_gpt_vscode_auth_pass",
    "profile_deepseek_denied_pass",
    "wrong_hmac_block_pass",
    "replay_nonce_block_pass",
    "cross_profile_session_block_pass",
    "status_pass",
    "scene_inspect_pass",
    "rename_approval_pending_pass",
    "rename_after_approval_pass",
    "cross_profile_approval_reuse_block_pass",
    "stale_state_block_pass",
    "request_tamper_block_pass",
    "queue_capacity_pass",
    "undo_restore_pass",
    "saved_hash_pass",
    "source_integrity_pass",
    "cleanup_pass",
)
```

- [ ] **Step 3: Define Switchy E2E RED**

Require a runner interface:

```text
python tools/run_godot_local_mcp_switchy_e2e.py \
  --project <switchy-checkout> \
  --godot <godot-4.7.1> \
  --gateway <gateway-python> \
  --report <report.json>
```

Expected profiles:

```yaml
codex: E2E_PASS
gpt-vscode: E2E_PASS
deepseek: MCP_CLIENT_PROFILE_DENIED
```

The test requires existing Switchy project behavior checks after restoration and a source inventory equality result.

- [ ] **Step 4: Wire RED into required CI**

The static test must run on all relevant changes. Runtime tests are guarded by exact binaries and fixtures. A workflow that is not connected to required `ci-gate` is insufficient.

- [ ] **Step 5: Run RED and commit**

```bash
python -m unittest \
  tests.test_godot_local_mcp_bridge_contract \
  tests.test_godot_local_mcp_bridge_runtime \
  tests.test_godot_local_mcp_switchy_e2e -v
```

Expected failures are missing production files and runners. Commit only tests and CI wiring:

```bash
git add tests .github/workflows
git commit -m "test: define Godot local MCP Bridge contract"
```

---

### Task 2: Define Project Adoption and Shared Configuration Contract

**Files:**
- Create: adoption manifest example
- Create: fixture manifests
- Modify: existing Godot contract tests and AGENTS fragment
- Test: Bridge contract module

**Interfaces:**
- Produces a fail-closed project adoption contract used by the Bridge and materializer.

- [ ] **Step 1: Define the adoption manifest**

Use:

```json
{
  "schema_version": 1,
  "artifact_role": "GODOT_LOCAL_MCP_ADOPTION_MANIFEST",
  "configuration_state": "NOT_CONFIGURED",
  "bridge_protocol": "BASE_GODOT_BRIDGE_V1",
  "bridge_plugin_version": "0.1.0",
  "adapter_version": "2",
  "allowed_profile_ids": ["codex", "gpt-vscode"],
  "allowed_capabilities": [
    "godot.editor.status",
    "scene.inspect",
    "node.rename",
    "operation.status"
  ],
  "bind_host": "127.0.0.1",
  "port_policy": "EPHEMERAL",
  "discovery_ttl_seconds": 120,
  "idle_timeout_seconds": 30,
  "max_frame_bytes": 262144,
  "max_json_depth": 32,
  "max_connections": 2,
  "max_in_flight_per_session": 64,
  "approval_ttl_seconds": 60,
  "test_approval_broker": false,
  "production_adapter_ready": false
}
```

The checked-in template stays `NOT_CONFIGURED`.

- [ ] **Step 2: Define capability Manifest integration**

A configured disposable fixture uses the existing Base v2 Manifest with:

- execution path `EDITOR_PLUGIN`;
- transport kind `PROJECT_DEFINED`;
- in-process adapter endpoint remains unchanged;
- Bridge security lives in the separate adoption manifest;
- status and operation-status are read-only;
- inspect maps to existing `scene.inspect`;
- rename maps to existing `node.rename` and requires approval.

Do not weaken the existing adapter Manifest to make it a network listener.

- [ ] **Step 3: Define the configuration root shared with Python**

Godot resolves:

1. `BASE_GODOT_MCP_CONFIG_DIR`;
2. Windows `%LOCALAPPDATA%/BaseGodotMcp`;
3. macOS `~/Library/Application Support/BaseGodotMcp`;
4. Linux `${XDG_CONFIG_HOME:-~/.config}/base-godot-mcp`.

The Bridge refuses `res://`, `user://` inside the project, or any path nested in the repository.

- [ ] **Step 4: Update operating documentation boundary**

The AGENTS fragment states:

```yaml
mcp_gateway: PROJECT_OPTIONAL
bridge_default: NOT_CONFIGURED
workspace_mcp_config: FORBIDDEN
deepseek_access: DENIED
mutation_approval: GODOT_HUMAN_ONLY
production_adapter_ready: false
```

- [ ] **Step 5: Run tests and commit**

```bash
python -m unittest tests.test_godot_local_mcp_bridge_contract -v
git add templates/project-operations/godot-local-mcp \
        templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md \
        tests/test_godot_local_mcp_bridge_contract.py
git commit -m "build: define local MCP Bridge adoption contract"
```

---

### Task 3: Implement Codec, Profile Store, and Descriptor Store in GDScript

**Files:**
- Create: `bridge_codec.gd`, `profile_store.gd`, `descriptor_store.gd`
- Test: static contract and fixture Runtime script

**Interfaces:**
- Produces canonical JSON, frame codec, profile loading, descriptor creation/expiry, and HMAC helpers.

- [ ] **Step 1: Implement canonical JSON parity**

Port the existing adapter canonical JSON algorithm without creating a second semantic authority. Add fixture vectors shared with Python and require byte-identical canonical output and SHA-256.

- [ ] **Step 2: Implement frame parsing state**

```gdscript
const HEADER_BYTES := 4
const MAX_FRAME_BYTES := 262_144
const MAX_JSON_DEPTH := 32

func feed_bytes(bytes: PackedByteArray) -> Array[Dictionary]:
    ...
```

The parser handles partial headers and bodies, multiple frames, invalid lengths, invalid UTF-8, non-Dictionary JSON, depth overflow, and connection-local reset.

- [ ] **Step 3: Implement profile loading**

```gdscript
func load_profile(profile_id: String, project_fingerprint: String) -> Dictionary:
    ...
```

Reject IDs other than `codex` and `gpt-vscode` before reading a file. Validate enabled, expiry, allowed project, capability set, credential ID, and decoded 32-byte secret. Never include the secret in returned diagnostics.

- [ ] **Step 4: Implement descriptor creation**

```gdscript
func create_descriptor(
    config_root: String,
    project_fingerprint: String,
    bridge_instance_id: String,
    editor_instance_id: String,
    port: int,
    ttl_seconds: int,
) -> Dictionary:
    ...
```

Write atomically to `<config_root>/bridges/<project_fingerprint>-<bridge_instance_id>.json`. Use `127.0.0.1`, protocol constant, hashed normalized project path, issued/expiry timestamps, and no secret.

- [ ] **Step 5: Implement cleanup**

On exit, delete only the exact current descriptor. On startup, remove expired descriptors matching the same project fingerprint; do not delete current descriptors for another Editor instance.

- [ ] **Step 6: Run fixture parser/profile tests and commit**

```bash
<GODOT_BIN> --headless --path examples/godot-local-mcp-bridge-pilot \
  --script res://tests/run_bridge_runtime.gd -- --phase codec-profile
git add templates/project-operations/godot-local-mcp/addons/base_godot_mcp_bridge \
        examples/godot-local-mcp-bridge-pilot
git commit -m "feat: add Bridge framing and discovery stores"
```

---

### Task 4: Implement the Loopback Bridge Server and HMAC Session

**Files:**
- Create: `bridge_server.gd`, `bridge_session.gd`
- Create: minimal `plugin.cfg`, `plugin.gd`
- Test: Runtime module and fixture

**Interfaces:**
- Produces a loopback server with two connections maximum and authenticated `BridgeSession` objects.

- [ ] **Step 1: Create plugin metadata**

```ini
[plugin]
name="Base Godot MCP Bridge"
description="Authenticated local Bridge to the Base live-editor adapter"
author="Base"
version="0.1.0"
script="plugin.gd"
```

- [ ] **Step 2: Extend the existing adapter**

```gdscript
@tool
extends "res://addons/base_live_editor_adapter/plugin.gd"

const BridgeServer = preload("bridge_server.gd")
var _bridge_server

func _enter_tree() -> void:
    super._enter_tree()
    if not availability().get("available", false):
        return
    _bridge_server = BridgeServer.new()
    ...
```

`_exit_tree()` closes the Bridge and descriptor before calling `super._exit_tree()`.

- [ ] **Step 3: Bind only loopback**

Create `TCPServer`, call `listen(0, "127.0.0.1")`, require success, then read `get_local_port()`. If the engine does not assign port 0 on exact Godot 4.7.1, choose a cryptographically random port in `49152..65535`, try at most 32 distinct ports, and record the observed behavior in evidence.

A test inspects the bound host through connection behavior: `127.0.0.1` succeeds; the machine's non-loopback address fails.

- [ ] **Step 4: Accept bounded connections**

Poll from `_process()`. Maximum two active peers. Reject additional peers without allocating a session. Require peer host `127.0.0.1`.

- [ ] **Step 5: Implement challenge/response**

Flow:

```text
HELLO(profile_id, service_instance_id, project_fingerprint)
→ CHALLENGE(random_nonce, bridge/editor IDs)
→ AUTHENTICATE(hmac)
→ AUTHENTICATED(session_id, expiry)
```

The HMAC covers nonce, Bridge, Editor, service, profile, project, protocol, and credential ID. Store nonce consumption; replay returns `BRIDGE_AUTHENTICATION_FAILED`.

- [ ] **Step 6: Bind session identity**

Every request repeats session ID, client profile ID, service ID, Bridge ID, Editor ID, and project fingerprint. Exact mismatch returns `BRIDGE_SESSION_MISMATCH`.

- [ ] **Step 7: Enforce limits**

- handshake: 3 seconds;
- idle: 30 seconds;
- frame: 262,144 bytes;
- JSON depth: 32;
- two connections;
- 64 in-flight operations per session;
- 124-frame maximum wait for adapter results in automated fixtures;
- no persistent background thread.

- [ ] **Step 8: Run Runtime tests and commit**

```bash
python tools/run_godot_local_mcp_bridge_pilot.py \
  --godot <GODOT_BIN> \
  --phase transport-auth \
  --report /tmp/bridge-auth.json
git add templates/project-operations/godot-local-mcp/addons/base_godot_mcp_bridge \
        examples/godot-local-mcp-bridge-pilot \
        tests/test_godot_local_mcp_bridge_runtime.py \
        tools/run_godot_local_mcp_bridge_pilot.py
git commit -m "feat: authenticate the Godot loopback Bridge"
```

---

### Task 5: Implement Adapter Routing for Status and Scene Inspection

**Files:**
- Create: `adapter_router.gd`
- Modify: Bridge plugin/server
- Test: fixture and Python Runtime module

**Interfaces:**
- Produces Bridge `REQUEST` handlers for status, inspect, and operation status.

- [ ] **Step 1: Implement bounded editor status**

Return only:

```yaml
connected
project_fingerprint
editor_instance_id
bridge_instance_id
adapter_version
active_scene_path
dirty_state
client_profile_id
network_scope: LOOPBACK_ONLY
production_adapter_ready: false
```

No absolute project path or secret.

- [ ] **Step 2: Implement inspect mapping**

Build the exact Base v2 envelope using authenticated session identity and current adapter snapshot. Call inherited:

```gdscript
submit_validated_operation(envelope)
```

Poll only through:

```gdscript
take_completed_result(operation_id)
```

Filter output to the declared maximum node count, depth, and response bytes.

- [ ] **Step 3: Implement operation status scope**

Maintain a bounded Bridge-side map keyed by `(profile_id, service_instance_id, operation_id)`. A different profile or service receives no existence signal beyond a generic denied/not-found response.

- [ ] **Step 4: Verify no executor bypass**

Static and Runtime tests must prove the Bridge never calls `_executor`, `EditorTransactionExecutor`, Scene mutation APIs, or file writes for status/inspect.

- [ ] **Step 5: Run tests and commit**

```bash
python tools/run_godot_local_mcp_bridge_pilot.py \
  --godot <GODOT_BIN> \
  --phase read-tools \
  --report /tmp/bridge-read.json
git add templates/project-operations/godot-local-mcp/addons/base_godot_mcp_bridge \
        examples/godot-local-mcp-bridge-pilot \
        tests
git commit -m "feat: route bounded read tools into the Base adapter"
```

---

### Task 6: Implement Human Approval Store and Godot Dock

**Files:**
- Create: `approval_store.gd`, `approval_dock.gd`, `approval_card.tscn`
- Modify: plugin/router
- Test: contract and Runtime fixture

**Interfaces:**
- Produces pending approval records, one-time user decisions, exact Base approval tokens, and a Dock UI.

- [ ] **Step 1: Define pending approval model**

Each record contains:

```yaml
operation_id
client_profile_id
automation_service_instance_id
capability_id
scene_path
node_path
old_value
new_value
save_mode
expected_revision
expected_sha256
expected_dirty_state
request_hash
contract_snapshot_hash
created_at
expires_at
state: PENDING | APPROVED | REJECTED | EXPIRED | CONSUMED
```

Maximum pending approvals: 16.

- [ ] **Step 2: Create the Dock**

The card displays client profile, capability, target, old/new value, save mode, dirty state, request hash prefix, and expiry. Buttons:

```text
Approve once
Reject
```

No “always approve”, batch approve, hidden default, keyboard shortcut without focus, or model-callable path.

- [ ] **Step 3: Generate the exact token after user action**

On approval, construct:

```yaml
state: APPROVED
token_id: approval-<random>
consumed_by_operation_id: exact_operation_id
token_binding: exact_adapter_guard_binding
expires_at: now_plus_60_seconds
```

Use the existing guard's required fields and canonical hashes. Token generation lives inside Godot and is not exposed through the Bridge protocol.

- [ ] **Step 4: Resume the exact operation**

The Gateway polls `godot_operation_status`. The Bridge resumes only the stored immutable envelope with the generated token. Changed arguments or identity cannot replace the stored envelope.

- [ ] **Step 5: Implement rejection and expiry**

Reject returns `APPROVAL_REJECTED_BY_USER`; expiry returns `APPROVAL_EXPIRED`. Both remove mutation authority and leave Scene/ledger/evidence unchanged except a bounded approval decision audit record.

- [ ] **Step 6: Add test-only broker isolation**

The fixture may instantiate `tests/test_approval_broker.gd` only when:

```text
BASE_GODOT_MCP_TEST_APPROVAL=1
```

The adoption template, plugin package, and production workflow must not contain or import the broker.

- [ ] **Step 7: Run automated approval tests and commit**

```bash
BASE_GODOT_MCP_TEST_APPROVAL=1 \
python tools/run_godot_local_mcp_bridge_pilot.py \
  --godot <GODOT_BIN> \
  --phase approval \
  --report /tmp/bridge-approval.json
git add templates/project-operations/godot-local-mcp/addons/base_godot_mcp_bridge \
        examples/godot-local-mcp-bridge-pilot \
        tests
git commit -m "feat: require Godot-side approval for MCP mutations"
```

Automated broker PASS is `TEST_APPROVAL_PASS`, not human evidence.

---

### Task 7: Implement Rename, Undo, Save, and Adversarial Cases

**Files:**
- Modify: router, approval store, fixture tests, runner
- Test: actual Bridge Runtime

**Interfaces:**
- Produces complete rename execution through the inherited Base adapter and exact restoration evidence.

- [ ] **Step 1: Submit approved rename**

After approval, call only `submit_validated_operation(approved_envelope)`. Require queued operation ID and no direct Node mutation.

- [ ] **Step 2: Verify dirty rename**

For `KEEP_DIRTY`, verify changed node name, dirty state, ledger, evidence, result hash, then Editor Undo and original name.

- [ ] **Step 3: Verify saved rename**

For `SAVE_CURRENT_SCENE`, verify physical Scene SHA-256 equals result evidence. Undo, save, refresh, and require original semantic state and byte restoration in the disposable fixture.

When Godot serialization changes equivalent bytes, use the previously validated disposable-copy exact-byte restoration procedure only inside the runner-owned temporary project and only for the approved target Scene.

- [ ] **Step 4: Implement attack matrix**

Require exact blocked codes:

```yaml
wrong_hmac: BRIDGE_AUTHENTICATION_FAILED
replayed_nonce: BRIDGE_AUTHENTICATION_FAILED
cross_profile_session: BRIDGE_SESSION_MISMATCH
cross_profile_approval: APPROVAL_BINDING_MISMATCH
expired_approval: APPROVAL_EXPIRED
tampered_request: REQUEST_HASH_MISMATCH
stale_observation: TARGET_STATE_CONFLICT
request_65: QUEUE_FULL
deepseek: MCP_CLIENT_PROFILE_DENIED
```

Every blocked mutation leaves Scene bytes/name unchanged and creates no mutation-completed evidence.

- [ ] **Step 5: Verify cleanup**

Close Gateway, disable plugin, and exit Editor. Require listener closed, descriptor deleted, sessions invalid, pending approvals expired/rejected, and pre-exit identities unusable after restart.

- [ ] **Step 6: Run full fixture Runtime and commit**

```bash
python tools/run_godot_local_mcp_bridge_pilot.py \
  --godot <GODOT_BIN> \
  --report /tmp/godot-local-mcp-bridge.json
git add templates/project-operations/godot-local-mcp \
        examples/godot-local-mcp-bridge-pilot \
        tests \
        tools/run_godot_local_mcp_bridge_pilot.py
git commit -m "feat: execute guarded MCP rename through Godot"
```

---

### Task 8: Verify MCP 2.0 Through the Real Bridge

**Files:**
- Modify: Python Bridge runner and Gateway tests
- Create: evidence document
- Test: real subprocess E2E

**Interfaces:**
- Produces actual MCP initialize/list/call evidence against Godot rather than a fake server.

- [ ] **Step 1: Materialize a disposable fixture**

Copy the fixture outside the Base repository, install the exact adapter and Bridge package, generate configured manifests, create temporary Codex/GPT profiles, and preserve source inventory.

- [ ] **Step 2: Start Godot Editor headless**

```bash
<GODOT_BIN> --editor --headless --path <temporary-project> --quit-after 1200
```

Wait for a valid descriptor, not merely process startup.

- [ ] **Step 3: Start Gateway over stdio**

Use the installed hash-locked Gateway environment and MCP SDK `Client` stdio transport. Execute initialize and exact tools/list.

- [ ] **Step 4: Run tool sequence**

For each authorized profile:

```text
godot_editor_status
→ godot_scene_inspect
→ godot_node_rename
→ APPROVAL_PENDING
→ test broker or human approval
→ godot_operation_status
→ COMPLETED
```

- [ ] **Step 5: Run negative profile sequence**

Attempt `deepseek` before descriptor lookup and require `MCP_CLIENT_PROFILE_DENIED`. Assert the Godot Bridge received no connection.

- [ ] **Step 6: Record evidence and commit**

Evidence separates:

```yaml
mcp_protocol: PASS
fake_bridge: PASS
actual_bridge: PASS
test_approval: PASS
human_approval: HUMAN_NOT_RUN
production_adapter_ready: false
```

Commit:

```bash
git add docs/knowledge/godot/evidence \
        tests \
        tools
git commit -m "test: prove MCP 2.0 through the Godot Bridge"
```

---

### Task 9: Run Switchy Codex and GPT End-to-End

**Files:**
- Create/modify: `run_godot_local_mcp_switchy_e2e.py`
- Create: Switchy evidence document
- Test: Switchy E2E module
- No permanent Switchy product modifications in the Base implementation PR

**Interfaces:**
- Produces actual-project evidence for both authorized profiles and one denied profile.

- [ ] **Step 1: Gate on the current green Switchy baseline**

Record exact Switchy main, exact Base Pilot prerequisite commit, Godot version, existing behavior-test command, target Scene, target node, and protected paths. Abort on drift rather than selecting another target.

- [ ] **Step 2: Materialize outside both repositories**

Create a full temporary Switchy copy. Install the Base adapter, Bridge, configured manifests, and test-only approval broker only in the temporary copy. Hash protected source paths before and after.

- [ ] **Step 3: Run Codex-profile E2E**

Use the `codex` profile through a real stdio Gateway process:

```text
status PASS
inspect PASS
rename APPROVAL_PENDING
approve exact request
rename PASS
Undo/save/restore PASS
existing project tests PASS
source integrity PASS
```

- [ ] **Step 4: Run GPT-profile E2E**

Repeat from a fresh temporary copy and new Editor/Gateway instances with `gpt-vscode`. Do not reuse Codex approval, service, session, descriptor, or operation IDs.

- [ ] **Step 5: Run cross-client negative cases**

- Codex approval applied to GPT operation;
- GPT stale observation after Codex change;
- GPT polling Codex operation;
- DeepSeek profile start;
- copied/renamed profile file;
- shared profile configuration declaration.

Require fail-closed codes and no source mutation.

- [ ] **Step 6: Run existing Switchy behavior tests**

Use the repository's current command and discover current case/assertion counts. Require zero failures after restoration. Do not hard-code historical counts as authority.

- [ ] **Step 7: Record evidence**

```yaml
switchy_codex_e2e: PASS_OR_FAIL
switchy_gpt_vscode_e2e: PASS_OR_FAIL
deepseek_denial: PASS_OR_FAIL
cross_client_approval_reuse: BLOCKED_OR_FAIL
source_integrity: PASS_OR_FAIL
project_regression: PASS_OR_FAIL
human_approval: HUMAN_NOT_RUN
production_adapter_ready: false
```

- [ ] **Step 8: Commit Base-side runner/evidence**

Do not commit temporary Switchy files, credentials, `.godot`, runtime descriptors, or profile secrets.

```bash
git add tools/run_godot_local_mcp_switchy_e2e.py \
        tests/test_godot_local_mcp_switchy_e2e.py \
        docs/knowledge/godot/evidence/2026-08-06-switchy-local-mcp-e2e.md
git commit -m "test: validate Codex and GPT MCP against Switchy"
```

Any required Switchy adoption change uses a separate Switchy PR and separate user approval.

---

### Task 10: Validate Windows, Real Host Registration, and Human Approval Dock

**Files:**
- Modify: Windows workflow, docs, evidence
- No secret or machine-specific active configuration committed

**Interfaces:**
- Produces primary-environment evidence and explicit human status.

- [ ] **Step 1: Add Windows CI**

Use Python 3.12 and exact Godot 4.7.1. Install the hash-locked Gateway dependencies, run static/profile/framing/fake-Bridge tests, start the actual Bridge fixture, and execute MCP calls.

- [ ] **Step 2: Verify Windows config paths and cleanup**

Require `%LOCALAPPDATA%\BaseGodotMcp`, owner-profile separation instructions, atomic profile rotation, descriptor deletion, port closure, and Editor restart.

- [ ] **Step 3: Verify real Codex registration**

Record:

```bash
codex --version
codex mcp --help
codex mcp list
```

Start the Gateway with the `codex` profile and call status/inspect. Record unsupported Codex provider configurations separately.

- [ ] **Step 4: Verify real VS Code `Godot Authoring` profile**

Create or select a dedicated user profile, add the generated GPT registration to that profile only, and verify the four tools appear. Open the separate `DeepSeek Analysis` profile and verify no Godot tools or registration exist.

- [ ] **Step 5: Perform human Dock test**

A person:

1. observes the exact pending rename card;
2. verifies client, target, old/new value, save mode, dirty state, hash, and expiry;
3. approves once;
4. confirms the Scene change and Undo;
5. rejects a second request;
6. restarts Editor and confirms old approval/session invalidation.

Record `HUMAN_PASS` only with human confirmation. Automated clicks or broker runs remain `HUMAN_NOT_RUN`.

- [ ] **Step 6: Perform recovery test**

Break plugin startup in the disposable fixture, launch `--recovery-mode`, disable/remove Bridge, clean stale descriptors, rotate profiles, restore normal Editor startup, and verify old identities fail.

- [ ] **Step 7: Update evidence**

Separate:

```yaml
windows_gateway_runtime
windows_godot_bridge_runtime
real_codex_registration
real_vscode_gpt_registration
deepseek_profile_tool_absence
human_approval_dock
recovery_mode
```

No field inherits PASS from Linux or automated broker evidence.

- [ ] **Step 8: Commit and review**

```bash
git add .github/workflows/validate-godot-local-mcp-windows.yml \
        docs/knowledge/godot \
        tests
git commit -m "test: validate local Godot MCP on Windows"
```

---

### Task 11: Documentation, Adversarial Review, and Draft PR Closure

**Files:**
- Modify: canonical knowledge/security/readiness/docs indexes
- Finalize: README and evidence
- No product or Registry changes

**Interfaces:**
- Produces one reviewed Draft Bridge implementation PR ready for owner decision.

- [ ] **Step 1: Update canonical docs**

Document:

- MCP Gateway vs Bridge vs adapter ownership;
- profile-based—not model-attested—identity;
- Codex/GPT authorization;
- DeepSeek isolation;
- status/inspect/rename/status tools;
- Godot-only human approval;
- localhost/HMAC/session limits;
- installation, rotation, recovery, uninstall;
- evidence boundaries and production false.

- [ ] **Step 2: Perform final adversarial review**

Attack:

- same VS Code profile shared by GPT/DeepSeek;
- malicious same-OS-user process;
- descriptor symlink/path traversal;
- port substitution;
- stale descriptor;
- HMAC replay;
- profile rotation during session;
- session fixation;
- approval after Scene drift;
- cross-client approval;
- queue saturation;
- partial frame and connection stall;
- Editor exit during mutation;
- stdout secret;
- evidence path leakage;
- recovery identity reuse;
- Switchy source change;
- test broker present in production package.

Classify unresolved same-OS-user impersonation as an explicit trust-boundary limitation, not a fixed property.

- [ ] **Step 3: Run complete exact-head verification**

```bash
python -m unittest \
  tests.test_godot_local_mcp_contract \
  tests.test_godot_local_mcp_profile_store \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_fake_bridge \
  tests.test_godot_local_mcp_server \
  tests.test_godot_local_mcp_host_configs \
  tests.test_godot_local_mcp_bridge_contract \
  tests.test_godot_local_mcp_bridge_runtime \
  tests.test_godot_local_mcp_switchy_e2e -v
python tools/validate_godot_live_editor_contract.py
python tools/validate_canonical_references.py
git diff --check
```

Run actual Godot, Windows, Switchy, and host commands separately and record exact outputs.

- [ ] **Step 4: Verify protected scope**

Require no changes to:

```text
skills/SKILL_REGISTRY.json
released lock files
frozen release snapshots
unrelated project templates
Switchy product code in the Base PR
active workspace .vscode/mcp.json
```

- [ ] **Step 5: Open the Bridge Draft PR**

Body:

```yaml
design_pr: 198
gateway_core_pr: exact_merged_pr
bridge_protocol: BASE_GODOT_BRIDGE_V1
mcp_sdk: 2.0.0
linux_bridge_runtime: PASS_OR_NOT_RUN
windows_bridge_runtime: PASS_OR_NOT_RUN
switchy_codex_e2e: PASS_OR_NOT_RUN
switchy_gpt_vscode_e2e: PASS_OR_NOT_RUN
deepseek_denial: PASS_OR_NOT_RUN
human_approval_dock: HUMAN_PASS_OR_HUMAN_NOT_RUN
second_project: NOT_RUN
production_adapter_ready: false
merge_authorization: NOT_GRANTED
```

- [ ] **Step 6: Wait for exact-head CI and stop**

Require zero unresolved review threads and no `MUST_FIX`. Do not merge, add broader tools, install in a production project, or claim readiness without explicit user authorization.

---

## Self-Review Result

```yaml
spec_coverage:
  loopback_bridge: tasks_3_4
  profile_authentication: tasks_2_3_4
  adapter_delegation: tasks_4_5_7
  godot_human_approval: task_6
  status_inspect_rename_operation_status: tasks_5_7
  adversarial_identity_and_replay: tasks_4_7_11
  actual_mcp_through_bridge: task_8
  switchy_codex_gpt_e2e: task_9
  deepseek_denial: tasks_1_4_8_9_10
  windows_primary_environment: task_10
  human_and_recovery_evidence: task_10
  second_project: explicitly_deferred_after_first_implementation_pr
  production_readiness: explicitly_false
placeholder_scan: PASS
type_consistency: PASS
implementation_started: false
implementation_authorization: false
production_adapter_ready: false
```

## Execution Handoff

Execute only after the Gateway Core PR is reviewed and merged, all declared prerequisites are green, and the user explicitly approves Bridge implementation. Use `superpowers:subagent-driven-development` or `superpowers:executing-plans`, with reviewer checkpoints after Tasks 1, 4, 6, 8, 9, and 10. Stop at the independent Draft Bridge PR.
