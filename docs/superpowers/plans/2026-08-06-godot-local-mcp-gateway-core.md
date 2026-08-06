# Godot Local MCP Gateway Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable Python 3.12 MCP stdio Gateway that exposes four bounded Godot tools to authorized Codex and GPT-in-VS-Code profiles, denies DeepSeek and unknown profiles, and talks only to an authenticated fake or real loopback Bridge through a closed framed protocol.

**Architecture:** The Gateway is a separate stdio MCP process built with the official `mcp==2.0.0` SDK. It loads one profile from an owner-only user configuration directory, discovers one exact Godot Bridge descriptor, authenticates with HMAC, maps MCP tool calls to Base v2 operation envelopes, and converts canonical Bridge results back to structured MCP results. This plan stops at a fake-Bridge and protocol-complete Gateway; the actual Godot EditorPlugin is implemented by the companion Bridge/E2E plan.

**Tech Stack:** Python 3.12, `mcp==2.0.0`, `jsonschema==4.26.0`, Pydantic supplied by the MCP SDK, `pip-tools==7.6.0` for hash-locked dependency generation, `unittest`, `asyncio`, JSON Schema Draft 2020-12.

## Global Constraints

- Do not start implementation until Base PR #197 or an equivalent successor is merged and green.
- Do not start implementation until Switchy PR #94 or an equivalent re-pinned successor is green.
- Merge the approved design/plan PR before creating the implementation branch.
- Create a new implementation branch from the then-current Base `main`; do not implement on PR #198.
- Preserve a test-only RED commit before production Gateway files exist.
- Use Python `3.12`.
- Pin the official MCP Python SDK to exactly `mcp==2.0.0`.
- Generate and commit a transitive `--require-hashes` lock with `pip-tools==7.6.0`.
- The Gateway transport exposed to hosts is stdio only.
- The Gateway must not bind a TCP, UDP, HTTP, WebSocket, or named-pipe listener.
- The Gateway may connect only to `127.0.0.1` and only to the port in a verified unexpired Bridge descriptor.
- Protocol stdout contains MCP frames only; diagnostics go to stderr.
- Authorized profile IDs are exactly `codex` and `gpt-vscode`.
- `deepseek`, missing, unknown, disabled, and expired profiles fail before Bridge discovery.
- No active workspace `.vscode/mcp.json` is committed.
- No secret, absolute project path, environment dump, or unrelated process data is returned through an MCP tool.
- v1 tools are exactly `godot_editor_status`, `godot_scene_inspect`, `godot_node_rename`, and `godot_operation_status`.
- No MCP tool can approve a mutation.
- Do not expose arbitrary file access, shell execution, GDScript execution, deletion, project settings, addon installation, import mutation, build/export, runtime debugger, or remote/LAN access.
- Do not modify `skills/SKILL_REGISTRY.json`, released locks, or frozen release snapshots.
- `production_adapter_ready` remains `false`.
- Stop the implementation PR before merge until the user explicitly authorizes it.

---

## Planned File Map

### Create

```text
templates/project-operations/godot-local-mcp/
  README.md
  client-profile.example.json
  bridge-descriptor.example.json
  vscode-profile-mcp.example.json
  codex-registration.example.txt
  gateway/
    pyproject.toml
    requirements.in
    requirements.lock
    src/base_godot_mcp/__init__.py
    src/base_godot_mcp/__main__.py
    src/base_godot_mcp/errors.py
    src/base_godot_mcp/config_paths.py
    src/base_godot_mcp/profile_store.py
    src/base_godot_mcp/schema_store.py
    src/base_godot_mcp/framing.py
    src/base_godot_mcp/bridge_protocol.py
    src/base_godot_mcp/bridge_client.py
    src/base_godot_mcp/tool_models.py
    src/base_godot_mcp/envelope_builder.py
    src/base_godot_mcp/server.py
    src/base_godot_mcp/setup_cli.py

schemas/
  godot-local-mcp-client-profile.schema.json
  godot-local-mcp-bridge-descriptor.schema.json
  godot-local-mcp-bridge-frame.schema.json

tests/
  fixtures/godot-local-mcp/
    profiles/codex.json
    profiles/gpt-vscode.json
    profiles/deepseek.json
    descriptors/valid.json
  test_godot_local_mcp_contract.py
  test_godot_local_mcp_profile_store.py
  test_godot_local_mcp_framing.py
  test_godot_local_mcp_fake_bridge.py
  test_godot_local_mcp_server.py
  test_godot_local_mcp_host_configs.py

tools/
  generate_godot_local_mcp_dependency_lock.py
  run_godot_local_mcp_fake_bridge.py

docs/knowledge/godot/
  GODOT_LOCAL_MCP_GATEWAY.md

.github/workflows/
  validate-godot-local-mcp.yml
```

### Modify

```text
.github/validation-requirements.txt
docs/DOCUMENTATION_MAP.md
docs/knowledge/godot/README.md
tests/test_godot_live_editor_contract_v2.py
```

The implementation must reassess these companion paths against the then-current `main` and modify the existing current owner files rather than creating duplicate indexes or validators.

---

### Task 1: Establish the Test-Only RED Contract

**Files:**
- Create: `tests/test_godot_local_mcp_contract.py`
- Create: `tests/test_godot_local_mcp_profile_store.py`
- Create: `tests/test_godot_local_mcp_framing.py`
- Create: `tests/test_godot_local_mcp_fake_bridge.py`
- Create: `tests/test_godot_local_mcp_server.py`
- Create: `tests/test_godot_local_mcp_host_configs.py`
- Modify: the current required Base CI test-discovery owner identified on fresh `main`

**Interfaces:**
- Consumes: approved design and SDK amendment.
- Produces: failing executable contracts for every required Gateway file, profile boundary, framing rule, tool surface, stdout rule, and host configuration rule.

- [ ] **Step 1: Create the static contract test**

Use `unittest.TestCase` and these exact constants:

```python
ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "templates/project-operations/godot-local-mcp"
GATEWAY_ROOT = PACKAGE_ROOT / "gateway"
SCHEMA_ROOT = ROOT / "schemas"

AUTHORIZED_PROFILES = {"codex", "gpt-vscode"}
DENIED_PROFILES = {"deepseek"}
EXPECTED_TOOLS = {
    "godot_editor_status",
    "godot_scene_inspect",
    "godot_node_rename",
    "godot_operation_status",
}
```

Create exact methods:

```python
class GodotLocalMcpContractTests(unittest.TestCase):
    def test_required_gateway_files_exist(self) -> None: ...
    def test_mcp_sdk_is_exactly_2_0_0_and_hash_locked(self) -> None: ...
    def test_schemas_are_closed_draft_2020_12_objects(self) -> None: ...
    def test_only_four_v1_tools_are_declared(self) -> None: ...
    def test_no_model_callable_approval_tool_exists(self) -> None: ...
    def test_no_active_workspace_mcp_config_is_shipped(self) -> None: ...
    def test_gateway_sources_contain_no_listener_or_shell_primitive(self) -> None: ...
    def test_registry_and_release_locks_are_not_part_of_the_change(self) -> None: ...
```

The forbidden source tokens are:

```python
FORBIDDEN_GATEWAY_TOKENS = (
    "asyncio.start_server",
    "socket.listen",
    "HTTPServer",
    "WebSocketServer",
    "subprocess.Popen",
    "subprocess.run",
    "os.system",
    "eval(",
    "exec(",
    "approve_operation",
)
```

Permit `asyncio.open_connection` only in `bridge_client.py`.

- [ ] **Step 2: Create profile-store RED tests**

Define the expected public interface before implementation:

```python
from base_godot_mcp.profile_store import (
    ClientProfile,
    ProfileError,
    load_profile,
)

class GodotLocalMcpProfileStoreTests(unittest.TestCase):
    def test_codex_profile_loads(self) -> None: ...
    def test_gpt_vscode_profile_loads(self) -> None: ...
    def test_deepseek_profile_is_denied_before_descriptor_access(self) -> None: ...
    def test_unknown_profile_is_denied(self) -> None: ...
    def test_disabled_profile_is_denied(self) -> None: ...
    def test_expired_profile_is_denied(self) -> None: ...
    def test_profile_secret_never_appears_in_repr(self) -> None: ...
    def test_profile_file_permissions_fail_closed_on_posix(self) -> None: ...
```

Assert stable codes:

```python
MCP_CLIENT_PROFILE_REQUIRED
MCP_CLIENT_PROFILE_DENIED
MCP_CLIENT_PROFILE_EXPIRED
MCP_CLIENT_PROFILE_PERMISSION_INVALID
```

Use `BASE_GODOT_MCP_CONFIG_DIR` to redirect all tests into `TemporaryDirectory`.

- [ ] **Step 3: Create framing RED tests**

Require:

```python
HEADER = struct.Struct(">I")
MAX_FRAME_BYTES = 262_144
MAX_JSON_DEPTH = 32
```

Public interface:

```python
async def read_frame(reader: asyncio.StreamReader) -> dict[str, object]: ...
async def write_frame(
    writer: asyncio.StreamWriter,
    payload: Mapping[str, object],
) -> None: ...
def canonical_json_bytes(value: object) -> bytes: ...
def canonical_sha256(value: object) -> str: ...
```

Test truncated header, zero length, oversized length, invalid UTF-8, invalid JSON, non-object root, depth overflow, canonical key ordering, and exact SHA-256 stability.

- [ ] **Step 4: Create fake-Bridge RED tests**

Require:

```python
class BridgeClient:
    async def connect(
        self,
        *,
        profile: ClientProfile,
        descriptor: BridgeDescriptor,
        automation_service_instance_id: str,
    ) -> "BridgeSession": ...

class BridgeSession:
    async def request(
        self,
        message_type: str,
        payload: Mapping[str, object],
        *,
        timeout_seconds: float,
    ) -> dict[str, object]: ...

    async def close(self) -> None: ...
```

Tests must cover valid HMAC challenge/response, wrong secret, replayed nonce, expired descriptor, non-loopback host, profile mismatch, project mismatch, frame limit, idle timeout, and clean close.

- [ ] **Step 5: Create MCP server RED tests**

Use the v2 SDK in-memory client:

```python
from mcp import Client
from base_godot_mcp.server import build_server

class GodotLocalMcpServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_exact_tool_list(self) -> None:
        server = build_server(test_dependencies)
        async with Client(server) as client:
            result = await client.list_tools()
            self.assertEqual(
                {tool.name for tool in result.tools},
                EXPECTED_TOOLS,
            )
```

Add exact tests for:

- structured status result;
- inspect request mapping;
- rename returns `APPROVAL_PENDING` rather than auto-approval;
- operation status is scoped to the authenticated profile;
- DeepSeek profile creation fails before server build;
- tools never return the profile secret;
- no resources or prompts are exposed in v1 unless the SDK requires empty protocol responses;
- unknown tool arguments fail Schema validation.

- [ ] **Step 6: Create host-configuration RED tests**

Require that:

- no `.vscode/mcp.json` exists under the template;
- the VS Code example explicitly says it belongs to a `Godot Authoring` user profile;
- the DeepSeek profile example contains no server registration;
- the Codex example uses the same Gateway executable and `codex` profile;
- host examples contain no real secret;
- setup commands write only outside the repository.

- [ ] **Step 7: Wire the RED modules into mandatory CI**

Add all six modules to the existing required Base contract workflow or add a dedicated workflow that is included by the required `ci-gate`. A newly created workflow that is not connected to required CI is insufficient.

- [ ] **Step 8: Run and record RED**

Run:

```bash
python -m unittest \
  tests.test_godot_local_mcp_contract \
  tests.test_godot_local_mcp_profile_store \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_fake_bridge \
  tests.test_godot_local_mcp_server \
  tests.test_godot_local_mcp_host_configs -v
```

Expected: failures are caused by missing Gateway, schemas, examples, and public interfaces. Syntax errors, incorrect imports in the tests themselves, or unrelated Base regressions invalidate the RED commit.

- [ ] **Step 9: Commit RED only**

```bash
git add tests .github/workflows
git commit -m "test: define local Godot MCP gateway contract"
```

---

### Task 2: Pin the SDK and Define Closed Schemas

**Files:**
- Create: `templates/project-operations/godot-local-mcp/gateway/pyproject.toml`
- Create: `templates/project-operations/godot-local-mcp/gateway/requirements.in`
- Create: `templates/project-operations/godot-local-mcp/gateway/requirements.lock`
- Create: `tools/generate_godot_local_mcp_dependency_lock.py`
- Create: three JSON Schemas under `schemas/`
- Modify: `.github/validation-requirements.txt`
- Test: `tests/test_godot_local_mcp_contract.py`

**Interfaces:**
- Produces exact SDK dependency and Schema validation surfaces used by every later task.

- [ ] **Step 1: Add exact project metadata**

Use:

```toml
[project]
name = "base-godot-local-mcp"
version = "0.1.0"
requires-python = "==3.12.*"
dependencies = [
  "jsonschema==4.26.0",
  "mcp==2.0.0",
]

[project.scripts]
base-godot-mcp = "base_godot_mcp.__main__:main"
base-godot-mcp-setup = "base_godot_mcp.setup_cli:main"

[build-system]
requires = ["setuptools==80.9.0"]
build-backend = "setuptools.build_meta"
```

- [ ] **Step 2: Add lock input**

`requirements.in` contains exactly:

```text
jsonschema==4.26.0
mcp==2.0.0
```

- [ ] **Step 3: Generate the hash lock deterministically**

The generator runs:

```bash
python -m pip install --disable-pip-version-check "pip-tools==7.6.0"
python -m piptools compile \
  --generate-hashes \
  --allow-unsafe \
  --strip-extras \
  --output-file requirements.lock \
  requirements.in
```

The generator rejects any resulting `mcp` version other than `2.0.0`, any pre-release, editable dependency, VCS URL, local path, un-hashed requirement, or Python marker that excludes Python 3.12 on Linux or Windows.

- [ ] **Step 4: Define the client-profile Schema**

Required fields:

```json
{
  "schema_version": 1,
  "profile_id": "codex",
  "enabled": true,
  "credential_id": "uuid",
  "credential_secret": "base64url-encoded 32 bytes",
  "allowed_projects": ["64 lowercase hex"],
  "allowed_capabilities": [
    "godot.editor.status",
    "scene.inspect",
    "node.rename",
    "operation.status"
  ],
  "expires_at": null
}
```

Use Draft 2020-12, `additionalProperties: false`, exact enum for `profile_id`, unique arrays, and no default that authorizes a missing value.

- [ ] **Step 5: Define the descriptor Schema**

Require exact loopback host `127.0.0.1`, port `1..65535`, RFC 3339 timestamps, 64-hex project fingerprint and path hash, UUID-like instance IDs, protocol `BASE_GODOT_BRIDGE_V1`, and `additionalProperties: false`. Do not include a secret value.

- [ ] **Step 6: Define the frame Schema**

Top-level fields:

```yaml
schema_version: 1
message_id: uuid
message_type: HELLO | CHALLENGE | AUTHENTICATE | AUTHENTICATED | REQUEST | RESPONSE | CLOSE
session_id: uuid_or_null
sent_at: rfc3339
payload: closed_message_specific_object
hmac_sha256: 64_hex_or_null
```

Use conditional JSON Schema branches so each message type has a closed payload.

- [ ] **Step 7: Run focused GREEN and commit**

Run:

```bash
python -m unittest tests.test_godot_local_mcp_contract -v
python tools/validate_godot_live_editor_contract.py
```

Commit:

```bash
git add templates/project-operations/godot-local-mcp/gateway \
        schemas \
        tools/generate_godot_local_mcp_dependency_lock.py \
        .github/validation-requirements.txt \
        tests/test_godot_local_mcp_contract.py
git commit -m "build: pin MCP 2.0 gateway contracts"
```

---

### Task 3: Implement Configuration Paths and Profile Authorization

**Files:**
- Create: `errors.py`, `config_paths.py`, `profile_store.py`, package initializers
- Create: example profile files
- Test: `tests/test_godot_local_mcp_profile_store.py`

**Interfaces:**
- Produces `ClientProfile`, `ProfileError`, `config_root()`, `load_profile()`, `create_profile()`, and `rotate_profile()`.

- [ ] **Step 1: Implement stable errors**

```python
class StableCode(str, Enum):
    MCP_CLIENT_PROFILE_REQUIRED = "MCP_CLIENT_PROFILE_REQUIRED"
    MCP_CLIENT_PROFILE_DENIED = "MCP_CLIENT_PROFILE_DENIED"
    MCP_CLIENT_PROFILE_EXPIRED = "MCP_CLIENT_PROFILE_EXPIRED"
    MCP_CLIENT_PROFILE_PERMISSION_INVALID = "MCP_CLIENT_PROFILE_PERMISSION_INVALID"
    BRIDGE_NOT_FOUND = "BRIDGE_NOT_FOUND"
    BRIDGE_DESCRIPTOR_STALE = "BRIDGE_DESCRIPTOR_STALE"
    BRIDGE_AUTHENTICATION_FAILED = "BRIDGE_AUTHENTICATION_FAILED"
    BRIDGE_SESSION_MISMATCH = "BRIDGE_SESSION_MISMATCH"
    BRIDGE_FRAME_LIMIT_EXCEEDED = "BRIDGE_FRAME_LIMIT_EXCEEDED"
    BRIDGE_IDLE_TIMEOUT = "BRIDGE_IDLE_TIMEOUT"

@dataclass(frozen=True)
class GatewayError(Exception):
    code: StableCode
    message: str
```

`GatewayError.__str__()` returns the stable code plus a non-secret message.

- [ ] **Step 2: Implement platform config roots**

Priority:

1. `BASE_GODOT_MCP_CONFIG_DIR` when explicitly set;
2. Windows `%LOCALAPPDATA%/BaseGodotMcp`;
3. macOS `~/Library/Application Support/BaseGodotMcp`;
4. Linux `${XDG_CONFIG_HOME:-~/.config}/base-godot-mcp`.

Reject roots inside the current Git repository.

- [ ] **Step 3: Implement the immutable profile model**

```python
@dataclass(frozen=True, repr=False)
class ClientProfile:
    profile_id: Literal["codex", "gpt-vscode"]
    enabled: bool
    credential_id: UUID
    credential_secret: bytes
    allowed_projects: frozenset[str]
    allowed_capabilities: frozenset[str]
    expires_at: datetime | None

    def __repr__(self) -> str:
        return (
            "ClientProfile("
            f"profile_id={self.profile_id!r}, "
            f"credential_id={str(self.credential_id)!r}, "
            "credential_secret=<redacted>)"
        )
```

- [ ] **Step 4: Implement fail-closed loading**

`load_profile(profile_id, config_root=None, now=None)` validates the Schema, exact ID, enabled flag, expiry, 32-byte decoded secret, allowed capabilities, project fingerprints, and owner-only permissions. It checks authorization before reading descriptors.

- [ ] **Step 5: Implement setup and rotation**

`create_profile()` supports only `codex` and `gpt-vscode`, generates 32 random bytes with `secrets.token_bytes(32)`, writes atomically, and sets mode `0o600` on POSIX. `rotate_profile()` replaces both credential ID and secret and returns only the profile path and credential ID.

- [ ] **Step 6: Add examples with inert values**

Examples use `"credential_secret": "REPLACE_USING_SETUP_COMMAND"` and `"enabled": false`; contract tests ensure examples cannot pass runtime validation.

- [ ] **Step 7: Run tests and commit**

```bash
python -m unittest tests.test_godot_local_mcp_profile_store -v
git add templates/project-operations/godot-local-mcp tests/test_godot_local_mcp_profile_store.py
git commit -m "feat: authorize local Godot MCP profiles"
```

---

### Task 4: Implement Framing, Descriptor Validation, and Fake Bridge

**Files:**
- Create: `schema_store.py`, `framing.py`, `bridge_protocol.py`, `bridge_client.py`
- Create: `tools/run_godot_local_mcp_fake_bridge.py`
- Test: framing and fake-Bridge modules

**Interfaces:**
- Produces `BridgeDescriptor`, `BridgeClient`, `BridgeSession`, canonical hashing, and a test-only fake server.

- [ ] **Step 1: Implement Schema loading**

Resolve Schemas from the installed package root without accepting caller-supplied paths. Cache validators and return all validation errors sorted by JSON path.

- [ ] **Step 2: Implement canonical JSON and length framing**

Use UTF-8 JSON with sorted keys, compact separators, no NaN/Infinity, four-byte big-endian length, 262,144-byte maximum, and a 32-level depth check before application handling.

- [ ] **Step 3: Implement descriptor discovery**

Search only `<config_root>/bridges/*.json`. Filter by exact allowed project fingerprint, `127.0.0.1`, unexpired timestamp, and protocol. Zero matches returns `BRIDGE_NOT_FOUND`; multiple current matches for the same project returns `BRIDGE_SESSION_MISMATCH`.

- [ ] **Step 4: Implement handshake material**

```python
def authentication_material(
    *,
    challenge_nonce: str,
    bridge_instance_id: str,
    editor_instance_id: str,
    automation_service_instance_id: str,
    profile_id: str,
    project_fingerprint: str,
) -> bytes:
    ...
```

Compute `hmac.new(profile.credential_secret, material, hashlib.sha256).hexdigest()`.

The Bridge challenge nonce is single-use and the client never sends the raw secret.

- [ ] **Step 5: Implement bounded connection**

Use only:

```python
reader, writer = await asyncio.wait_for(
    asyncio.open_connection("127.0.0.1", descriptor.port),
    timeout=3.0,
)
```

Handshake timeout is 3 seconds, request timeout default is 10 seconds, idle timeout is 30 seconds, and one Gateway session permits at most 64 in-flight operations.

- [ ] **Step 6: Implement the fake Bridge**

The fake server is test-only, binds `127.0.0.1`, validates the exact framing/handshake, and returns deterministic status, inspect, approval-pending, operation-status, stale, queue-full, and tamper responses. It must live under `tools/` and be excluded from project adoption templates.

- [ ] **Step 7: Run tests and commit**

```bash
python -m unittest \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_fake_bridge -v
git add templates/project-operations/godot-local-mcp/gateway \
        tools/run_godot_local_mcp_fake_bridge.py \
        tests/test_godot_local_mcp_framing.py \
        tests/test_godot_local_mcp_fake_bridge.py
git commit -m "feat: add authenticated fake Godot Bridge protocol"
```

---

### Task 5: Implement Tool Models and Base Envelope Mapping

**Files:**
- Create: `tool_models.py`
- Create: `envelope_builder.py`
- Test: server and contract modules

**Interfaces:**
- Produces closed Pydantic models and `build_base_envelope()`.

- [ ] **Step 1: Define closed tool models**

Every model uses:

```python
model_config = ConfigDict(extra="forbid", strict=True)
```

Required models:

```python
EditorStatusResult
SceneInspectInput
SceneInspectResult
NodeRenameInput
OperationStatusInput
OperationStatusResult
GatewayToolError
```

Constrain `res://` paths, node paths, name length, UUID operation ID, 64-hex hashes, enum save mode, and bounded Scene output.

- [ ] **Step 2: Define the capability map**

```python
TOOL_TO_CAPABILITY = {
    "godot_editor_status": "godot.editor.status",
    "godot_scene_inspect": "scene.inspect",
    "godot_node_rename": "node.rename",
    "godot_operation_status": "operation.status",
}
```

No dynamic capability name is accepted.

- [ ] **Step 3: Implement envelope construction**

```python
def build_base_envelope(
    *,
    tool_name: str,
    arguments: Mapping[str, object],
    profile: ClientProfile,
    descriptor: BridgeDescriptor,
    automation_service_instance_id: str,
    bridge_snapshot: Mapping[str, object],
) -> dict[str, object]:
    ...
```

The function copies exact project and Editor identity from the authenticated descriptor/snapshot, never from MCP arguments. It computes the canonical request hash after policy, snapshot, and preconditions are fixed.

- [ ] **Step 4: Encode mutation approval state**

Initial rename envelopes use:

```yaml
approval:
  state: PENDING
  token_id: null
  consumed_by_operation_id: null
  token_binding: null
  expires_at: null
```

The Gateway cannot manufacture `APPROVED`. A pending response maps to `APPROVAL_PENDING`.

- [ ] **Step 5: Verify hashes against the existing Base canonical algorithm**

Add shared fixture vectors used by Python and the existing GDScript canonical JSON algorithm. Require identical SHA-256 for nested dictionaries, arrays, booleans, null, Unicode, integers, and strings.

- [ ] **Step 6: Run tests and commit**

```bash
python -m unittest tests.test_godot_local_mcp_server -v
git add templates/project-operations/godot-local-mcp/gateway \
        tests/test_godot_local_mcp_server.py \
        tests/fixtures/godot-local-mcp
git commit -m "feat: map MCP tools to Base operation envelopes"
```

---

### Task 6: Implement the MCP 2.0 Stdio Server

**Files:**
- Create: `server.py`, `__main__.py`
- Test: `tests/test_godot_local_mcp_server.py`

**Interfaces:**
- Produces `build_server(dependencies) -> MCPServer` and the `base-godot-mcp` stdio entrypoint.

- [ ] **Step 1: Define explicit dependencies**

```python
@dataclass(frozen=True)
class ServerDependencies:
    profile: ClientProfile
    bridge_session_factory: BridgeSessionFactory
    automation_service_instance_id: str
    stderr: TextIO
```

Tests inject a fake session; production builds it from profile and descriptor discovery.

- [ ] **Step 2: Build the server**

```python
from mcp.server import MCPServer

def build_server(dependencies: ServerDependencies) -> MCPServer:
    server = MCPServer("Base Godot Local MCP")
    ...
    return server
```

Register exactly four `@server.tool()` functions.

- [ ] **Step 3: Map Bridge errors to structured tool results**

Return a bounded structured object:

```yaml
ok: false
code: STABLE_CODE
message: non_secret_message
retryable: false
operation_id: optional_uuid
```

Do not include exception tracebacks in tool results. Write diagnostic tracebacks to stderr only when `BASE_GODOT_MCP_DEBUG=1`, with secret redaction.

- [ ] **Step 4: Enforce stdout purity**

`__main__.py` configures all logging to stderr before imports that could log, loads the profile, creates a unique `automation_service_instance_id`, and calls:

```python
server.run()
```

Any non-protocol stdout write in tests fails `MCP_STDOUT_PROTOCOL_VIOLATION`.

- [ ] **Step 5: Test in memory**

Use `Client(server)` to verify initialize, list tools, calls, structured content, input rejection, approval pending, operation polling, profile isolation, and disconnect cleanup.

- [ ] **Step 6: Test real stdio**

Start:

```bash
python -m base_godot_mcp --profile codex
```

through the MCP SDK stdio client transport with a temporary profile and fake Bridge. Require initialize and four calls. Kill the fake Bridge and require a bounded `BRIDGE_NOT_FOUND` or connection failure, not a hung process.

- [ ] **Step 7: Commit**

```bash
git add templates/project-operations/godot-local-mcp/gateway \
        tests/test_godot_local_mcp_server.py
git commit -m "feat: serve bounded Godot tools over MCP stdio"
```

---

### Task 7: Add Host Setup, DeepSeek Isolation, Documentation, and CI

**Files:**
- Create: `setup_cli.py`, examples, README, knowledge guide
- Modify: documentation indexes and required CI
- Test: host-config and full Gateway tests

**Interfaces:**
- Produces setup commands for Codex and a VS Code `Godot Authoring` profile without committing active workspace configuration.

- [ ] **Step 1: Implement setup commands**

Supported commands:

```text
base-godot-mcp-setup profile create --profile codex --project-fingerprint <sha256>
base-godot-mcp-setup profile create --profile gpt-vscode --project-fingerprint <sha256>
base-godot-mcp-setup profile rotate --profile <authorized-profile>
base-godot-mcp-setup profile disable --profile <authorized-profile>
base-godot-mcp-setup host codex --profile codex
base-godot-mcp-setup host vscode --profile gpt-vscode
base-godot-mcp-setup doctor --profile <authorized-profile>
```

The CLI rejects `--profile deepseek`.

- [ ] **Step 2: Verify current Codex registration syntax**

On the implementation environment:

```bash
codex --version
codex mcp --help
codex mcp add --help
```

Record the version and exact accepted registration command in bounded evidence. The generated Codex example must be accepted by `codex mcp list` without embedding a secret in the repository. Bedrock-backed Codex configurations where MCP namespace tools are unavailable are recorded as unsupported for this v1 integration rather than treated as PASS.

- [ ] **Step 3: Generate the VS Code profile example**

The example explains that it belongs in the `Godot Authoring` user profile and launches:

```text
python -m base_godot_mcp --profile gpt-vscode
```

It includes no secret and no workspace-relative auto-registration. The guide requires a separate `DeepSeek Analysis` profile with no Godot MCP entry.

- [ ] **Step 4: Write the knowledge guide**

Document architecture, configuration roots, profile security boundary, tool contracts, approval pending behavior, recovery, uninstall, evidence states, and the limitation that profile identity is not cryptographic model attestation.

- [ ] **Step 5: Add dedicated CI**

Linux CI:

```bash
python -m pip install --require-hashes \
  -r templates/project-operations/godot-local-mcp/gateway/requirements.lock
python -m unittest \
  tests.test_godot_local_mcp_contract \
  tests.test_godot_local_mcp_profile_store \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_fake_bridge \
  tests.test_godot_local_mcp_server \
  tests.test_godot_local_mcp_host_configs -v
```

Windows CI runs profile path, permission behavior where enforceable, fake Bridge, in-memory MCP, and stdio process tests. Platform-specific permission limitations must be explicit, not silently skipped.

- [ ] **Step 6: Run the complete Gateway verification**

```bash
python -m unittest \
  tests.test_godot_local_mcp_contract \
  tests.test_godot_local_mcp_profile_store \
  tests.test_godot_local_mcp_framing \
  tests.test_godot_local_mcp_fake_bridge \
  tests.test_godot_local_mcp_server \
  tests.test_godot_local_mcp_host_configs -v
python tools/validate_godot_live_editor_contract.py
python tools/validate_canonical_references.py
git diff --check
```

- [ ] **Step 7: Perform adversarial review**

Attack:

- DeepSeek profile name case/Unicode/path tricks;
- symlinked profile or descriptor;
- expired descriptor;
- copied Codex profile used as GPT;
- stdout secret or logging contamination;
- malformed JSON depth and size;
- HMAC replay;
- descriptor port substitution;
- project fingerprint mismatch;
- fake approval field in MCP arguments;
- hidden fifth tool;
- workspace `.vscode/mcp.json`;
- Bridge unavailable and disconnect races.

Every reproduced issue gets a failing test before a fix.

- [ ] **Step 8: Commit documentation and CI**

```bash
git add templates/project-operations/godot-local-mcp \
        docs/knowledge/godot \
        docs/DOCUMENTATION_MAP.md \
        tests \
        .github/workflows
git commit -m "docs: operationalize the local Godot MCP gateway"
```

- [ ] **Step 9: Open an independent Draft implementation PR and stop**

The PR body records:

```yaml
design_pr: 198
gateway_protocol: MCP_2_0_STDIO
fake_bridge: PASS_OR_NOT_RUN
codex_profile: PASS_OR_NOT_RUN
gpt_vscode_profile: PASS_OR_NOT_RUN
deepseek_profile: DENIED_OR_NOT_RUN
actual_godot_bridge: NOT_IMPLEMENTED_IN_THIS_PR
production_adapter_ready: false
merge_authorization: NOT_GRANTED
```

Wait for exact-head CI and user review. Do not merge and do not begin the actual Bridge plan on the same branch.

---

## Self-Review Result

```yaml
spec_coverage:
  mcp_stdio_gateway: tasks_4_6
  sdk_2_0_pin: task_2
  codex_and_gpt_profiles: tasks_3_7
  deepseek_denial: tasks_1_3_7
  closed_tool_surface: tasks_1_5_6
  approval_not_model_callable: tasks_1_5_6
  authenticated_bridge_contract: task_4
  stdout_stderr_separation: tasks_1_6
  host_configuration: task_7
  dependency_hash_lock: task_2
  no_workspace_registration: tasks_1_7
  actual_godot_bridge: explicitly_deferred_to_companion_plan
placeholder_scan: PASS
type_consistency: PASS
implementation_started: false
implementation_authorization: false
production_adapter_ready: false
```

## Execution Handoff

After the prerequisites, design/plan merge, and explicit implementation approval, execute this plan on a new Base branch using `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Use reviewer checkpoints after Tasks 1, 3, 4, 6, and 7. Stop at the independent Draft Gateway PR.
