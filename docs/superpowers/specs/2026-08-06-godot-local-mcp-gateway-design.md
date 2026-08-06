# Godot Local MCP Gateway Design

## Status

```yaml
status: DRAFT_FOR_USER_REVIEW
architecture_direction: APPROVED_IN_CURRENT_CONVERSATION
implementation: NOT_STARTED
implementation_plan: NOT_WRITTEN
base_repository: alsdmlals4-eng/Base
baseline_main: b96d9dfe09ef33a18e9b31113eb480ad7a919b1f
prerequisite_base_pilot_fix: PR_197_OR_EQUIVALENT_GREEN_SUCCESSOR
prerequisite_switchy_regression: PR_94_OR_EQUIVALENT_GREEN_SUCCESSOR
production_adapter_ready: false
```

## User decisions

```yaml
target_engine: Godot
primary_work_environment: Visual Studio Code
authorized_clients:
  codex:
    read: true
    write: true
  gpt_in_vscode:
    read: true
    write: true
unauthorized_clients:
  deepseek:
    mcp_access: false
    godot_read: false
    godot_write: false
```

GPT is used through an authorized VS Code profile. DeepSeek remains an analysis-only model and receives no Godot MCP registration, profile credential, or Bridge session.

## Decision

Build one reusable, client-neutral local MCP Gateway instead of separate Godot integrations for Codex and GPT.

```text
Codex CLI ──────────────┐
                        ├─ MCP over stdio
GPT in authorized VS Code profile ─┘
                                  ↓
                         Godot Local MCP Gateway
                                  ↓
                 authenticated loopback Bridge protocol
                                  ↓
                         Godot Bridge EditorPlugin
                                  ↓
                    Base Live-Editor Adapter v2
                                  ↓
            Scene inspect / guarded rename / ledger / evidence
```

DeepSeek runs in a separate VS Code profile or process environment that has no MCP registration and no Bridge credential.

The MCP Gateway is a protocol adapter and policy enforcement boundary. It does not replace the existing Base live-editor execution core. Godot mutation correctness, main-thread execution, stale-state checks, approval binding, Undo/Redo, save semantics, ledger, evidence, and canonical result hashing remain owned by the existing adapter contract.

## Why this architecture

### Recommended: stdio Gateway plus authenticated Godot Bridge

Advantages:

- Codex and VS Code both consume a standard local MCP server.
- The Gateway has no public listener; each host owns its stdio child process.
- Godot remains responsible for Editor-main-thread execution.
- Client-specific configuration and credentials remain outside project source.
- The same Gateway implementation can serve Codex and GPT without model-specific tool code.
- Existing Base v2 identities, approvals, preconditions, rollback, ledger, and evidence remain authoritative.

Costs:

- A small authenticated local IPC layer is still required between the Gateway process and Godot Editor.
- Strict DeepSeek denial requires VS Code profile/process separation; the server cannot cryptographically identify the underlying language model when multiple models share one host process.

### Rejected: workspace-wide `.vscode/mcp.json`

A shared workspace MCP configuration would expose the Godot tools to every compatible model or agent using that workspace, including DeepSeek. Tool toggles are convenience controls, not a durable model-identity boundary.

Therefore the first release must not commit an active workspace `.vscode/mcp.json`. It provides profile-scoped installation templates instead.

### Rejected: Godot EditorPlugin as the MCP server itself

Running the full MCP lifecycle directly inside Godot would combine JSON-RPC framing, host compatibility, client sessions, Editor state, mutation execution, and recovery in one plugin. It would also make Codex and VS Code lifecycle differences part of the Godot implementation.

The separate Gateway keeps MCP protocol churn out of the Editor execution core.

### Deferred: Windows named-pipe-only design

A named pipe provides a strong local boundary but increases Godot-side portability and test complexity. The first implementation uses authenticated loopback IPC with a closed protocol and may add a named-pipe profile later after Windows evidence exists.

## Security boundary: host profile, not model name

The Gateway cannot trust a string such as `client_id: gpt` supplied by a caller. It also cannot reliably distinguish GPT from DeepSeek when both are running behind the same VS Code agent host.

Strict denial therefore uses configuration and process isolation:

```text
VS Code profile: Godot Authoring
- GPT enabled
- profile-scoped Godot MCP registration
- gpt-vscode credential

Codex CLI
- independent MCP registration
- codex credential

VS Code profile: DeepSeek Analysis
- no Godot MCP registration
- no Godot Bridge credential
- no automatic MCP discovery from the authoring profile
```

Required rules:

1. No active Godot MCP server configuration is committed to the game workspace.
2. Codex and GPT receive different profile credentials generated outside the repository.
3. DeepSeek receives neither credential.
4. The Gateway rejects missing, unknown, disabled, expired, or mismatched client profiles.
5. Every operation records the authenticated client profile in the ledger and evidence.
6. A profile credential identifies an authorized local host profile, not a cryptographically attested model.
7. If GPT and DeepSeek share one host/profile with the same tool registry, strict DeepSeek denial is `BLOCKED_CONFIGURATION`.

This design does not claim protection against malicious software already running with the same OS user permissions. That requires a stronger OS sandbox, separate user account, VM, or container boundary.

## Components

### 1. Godot Local MCP Gateway

A Python 3.12 stdio MCP server using the stable official MCP Python SDK line, pinned exactly during implementation. The design target is the stable `mcp` 1.x line rather than the pre-release 2.x line.

Responsibilities:

- MCP initialization and capability negotiation;
- `tools/list` and `tools/call`;
- protocol-only stdout and diagnostic-only stderr;
- authenticated client-profile loading;
- exact project and Editor discovery;
- MCP arguments to Base operation-envelope conversion;
- approval-pending and operation-status mapping;
- canonical Base result to MCP result conversion;
- bounded timeouts, message sizes, depth, queueing, and shutdown;
- no direct Godot file mutation;
- no arbitrary command or script execution.

The Gateway starts once per MCP host session. Codex and GPT normally run separate Gateway processes with separate `automation_service_instance_id` values.

### 2. Client profile store

Credentials and profile metadata live outside the repository in the current user's configuration directory.

Conceptual record:

```yaml
profile_id: codex | gpt-vscode
profile_version: 1
enabled: true
credential_id: random_uuid
credential_secret: random_256_bit_value
allowed_projects:
  - exact_project_fingerprint
allowed_capabilities:
  - godot.editor.status
  - scene.inspect
  - node.rename
expires_at: optional
```

Rules:

- secrets are never committed, printed to stdout, included in evidence, or accepted through MCP tool arguments;
- profile files require current-user-only permissions where supported;
- profile creation and rotation are explicit setup commands;
- disabling or rotating a profile invalidates new sessions;
- profile identity is bound to each operation and terminal result.

### 3. Godot Bridge EditorPlugin

A project-local EditorPlugin installed from a pinned Base template. It owns only the external local Bridge boundary and delegates validated operations to the existing Base live-editor adapter.

Responsibilities:

- bind only to `127.0.0.1` on an ephemeral port;
- generate a new Bridge instance ID and one-time session secret on each Editor start;
- publish a short-lived owner-only discovery descriptor outside the repository;
- authenticate Gateway challenge/response with HMAC;
- bind Gateway session to exact project fingerprint, Bridge instance, Editor instance, client profile, and service instance;
- enforce request size, nesting depth, connection count, batch, idle, and deadline limits;
- reject browser or unapproved Origin values;
- accept only closed Base operation envelopes;
- call the Base adapter on the Editor main thread;
- expose approval requests in a Godot Editor dock;
- return bounded canonical results;
- close the endpoint and invalidate all sessions on plugin disable or Editor exit.

The Bridge is not an MCP server. Its protocol is a smaller project-local authenticated request/result protocol carrying Base v2 envelopes.

### 4. Godot approval dock

Model-issued mutation requests cannot approve themselves.

For `approval_policy: REQUIRED`:

1. Gateway submits the exact normalized request without an approval token.
2. Bridge validates shape, identity, capability, request hash, and current preconditions.
3. Bridge returns `APPROVAL_REQUIRED` and displays a bounded approval card in Godot.
4. The card shows client profile, capability, target Scene/Node, old/new value, save mode, current dirty state, request hash prefix, and expiry.
5. The user selects `Approve once` or `Reject` inside Godot.
6. Bridge creates a single-use token bound to the existing Base v2 approval fields.
7. Gateway polls operation status or resubmits the exact operation identity.
8. Any changed request, stale precondition, expired approval, different client, project, Bridge, Editor, service, or contract snapshot is rejected.

No MCP tool named `approve_operation` is exposed in v1. Approval authority remains outside the model tool surface.

### 5. Discovery descriptor

The Bridge writes a short-lived descriptor under the current user's temporary/configuration directory, never under the project repository.

Conceptual descriptor:

```yaml
schema_version: 1
project_fingerprint: sha256
normalized_project_path_hash: sha256
bridge_instance_id: uuid
editor_instance_id: uuid
bind_host: 127.0.0.1
port: ephemeral_integer
protocol: BASE_GODOT_BRIDGE_V1
issued_at: rfc3339
expires_at: rfc3339
secret_reference: local_owner_only_reference
```

The descriptor does not treat port, PID, process name, or window title as identity. The Gateway must prove possession of the session secret and match the exact project fingerprint.

Stale descriptors are ignored and safely removable.

## Initial MCP tool surface

The first version exposes only capabilities already supported by the validated execution core plus a bounded status surface.

### `godot_editor_status`

Effect: read-only.

Returns:

```yaml
connected: boolean
project_fingerprint: bounded_hash
editor_instance_id: uuid_or_null
bridge_instance_id: uuid_or_null
adapter_version: string_or_null
active_scene_path: res_path_or_null
dirty_state: CLEAN | DIRTY | UNKNOWN
client_profile_id: codex | gpt-vscode
network_scope: LOOPBACK_ONLY
production_adapter_ready: false
```

It does not reveal absolute source paths, secrets, arbitrary environment variables, complete process lists, or unrelated open projects.

### `godot_scene_inspect`

Maps to Base `scene.inspect`.

Input is a closed object with an optional bounded Scene path selector. By default it inspects the selected active Scene. Output is filtered to the declared Scene tree contract and bounded by node count, depth, and response size.

### `godot_node_rename`

Maps to Base `node.rename`.

Input:

```yaml
scene_path: exact_res_path
node_path: exact_node_path
new_name: validated_node_name
save_mode: KEEP_DIRTY | SAVE_CURRENT_SCENE
expected_scene_revision: required
expected_scene_sha256: required_when_saved
expected_dirty_state: required
operation_id: client_generated_uuid
```

Behavior:

- always requires human approval in Godot;
- fails closed on stale state;
- records client profile and exact contract snapshot;
- uses one Editor Undo/Redo transaction;
- `SAVE_CURRENT_SCENE` requires stricter clean/dirty and physical-hash verification;
- does not silently discard or save unrelated user changes.

### `godot_operation_status`

Effect: read-only.

Returns only the authenticated client's bounded operation state:

```yaml
state: APPROVAL_PENDING | QUEUED | RUNNING | COMPLETED | FAILED | REJECTED | STALE
code: stable_code
approval_expires_at: optional
result: optional_declared_output
result_hash: optional_sha256
```

A client cannot enumerate another client profile's operations.

## Explicitly excluded from v1

```yaml
excluded:
  - arbitrary_file_read
  - arbitrary_file_write
  - arbitrary_gdscript_execution
  - arbitrary_expression_evaluation
  - shell_or_terminal_execution
  - node_delete
  - resource_delete
  - project_godot_edit
  - project_settings_mutation
  - addon_installation
  - import_pipeline_mutation
  - build_or_export
  - runtime_debugger
  - remote_or_lan_access
  - wildcard_bind
  - automatic_model_approval
  - deepseek_access
  - undo_arbitrary_human_action
```

Additional Godot capabilities require separate design, contract, TDD, approval, rollback, and real-project evidence.

## End-to-end data flow

### Session startup

```text
authorized host starts Gateway over stdio
→ Gateway loads profile credential outside repo
→ MCP initialize
→ Gateway locates matching unexpired Bridge descriptor
→ authenticated HMAC challenge/response
→ exact project + Bridge + Editor + service + client session binding
→ tools available
```

### Read operation

```text
tools/call godot_scene_inspect
→ closed MCP input validation
→ Base envelope construction
→ Bridge authentication and snapshot validation
→ Base adapter queue
→ Editor main-thread inspect
→ output Schema validation
→ canonical result hash
→ MCP tool result
```

### Mutation operation

```text
tools/call godot_node_rename
→ closed input and stale precondition validation
→ APPROVAL_REQUIRED
→ Godot approval dock
→ user Approve once
→ single-use approval token
→ exact operation resumes
→ EditorUndoRedoManager transaction
→ optional save + physical hash
→ ledger and evidence
→ canonical result
→ MCP tool result
```

### Concurrent Codex and GPT requests

- each Gateway has a distinct service instance and authenticated profile;
- the Bridge serializes mutations through the existing bounded adapter queue;
- read requests remain bounded by the same queue policy;
- stale revisions cause `TARGET_STATE_CONFLICT` rather than last-writer-wins;
- approvals are not transferable across Codex and GPT;
- one client cannot poll or replay another client's operation.

## Stable failure codes

Reuse existing Base codes where applicable and add a small Bridge/Gateway namespace.

```yaml
existing:
  - PROJECT_IDENTITY_MISMATCH
  - CONTRACT_SNAPSHOT_MISMATCH
  - APPROVAL_REQUIRED
  - APPROVAL_TOKEN_MISMATCH
  - APPROVAL_TOKEN_REUSED
  - TARGET_STATE_CONFLICT
  - OUTPUT_SCHEMA_MISMATCH
  - QUEUE_FULL

new:
  - MCP_CLIENT_PROFILE_REQUIRED
  - MCP_CLIENT_PROFILE_DENIED
  - MCP_CLIENT_PROFILE_EXPIRED
  - MCP_STDOUT_PROTOCOL_VIOLATION
  - BRIDGE_NOT_FOUND
  - BRIDGE_DESCRIPTOR_STALE
  - BRIDGE_AUTHENTICATION_FAILED
  - BRIDGE_SESSION_MISMATCH
  - BRIDGE_ORIGIN_DENIED
  - BRIDGE_FRAME_LIMIT_EXCEEDED
  - BRIDGE_IDLE_TIMEOUT
  - APPROVAL_REJECTED_BY_USER
  - MODEL_PROFILE_ISOLATION_REQUIRED
```

DeepSeek or any unregistered client receives `MCP_CLIENT_PROFILE_DENIED` before project discovery or tool execution.

## Configuration and installation model

### Codex

Provide a generated stdio MCP registration that launches the common Gateway with the Codex profile reference. The exact host configuration location and syntax are verified against the current Codex release during implementation and are not hard-coded into the Base contract.

### GPT in VS Code

Provide a VS Code user-profile MCP configuration template for a dedicated `Godot Authoring` profile. It launches the same Gateway with the `gpt-vscode` profile reference.

The active configuration is stored in the VS Code profile, not the project workspace. This prevents a DeepSeek analysis profile from inheriting the server through workspace configuration.

### DeepSeek

Provide no Godot MCP registration. Disable MCP auto-discovery between the authorized authoring profile and the DeepSeek analysis profile where the host supports it. DeepSeek may continue to inspect normal repository files through its existing analysis environment, but it cannot call the Godot Gateway.

### Project adoption

A project adopts:

- a pinned Bridge plugin and existing adapter;
- a configured project capability Manifest;
- project-specific allowed capabilities and roots;
- installation/removal instructions;
- runtime and recovery tests.

It does not commit client secrets or an active multi-model VS Code MCP registration.

## Proposed Base ownership

Base owns reusable contracts and reference templates, not a universal always-running production service.

Proposed implementation surfaces:

```text
templates/project-operations/godot-local-mcp/
  gateway/
  addons/base_godot_mcp_bridge/
  client-profile.example.json
  vscode-profile-mcp.example.json
  README.md

schemas/
  godot-local-mcp-client-profile.schema.json
  godot-local-mcp-bridge-descriptor.schema.json
  godot-local-mcp-bridge-message.schema.json

docs/knowledge/godot/
  GODOT_LOCAL_MCP_GATEWAY.md

tests/
  test_godot_local_mcp_contract.py
  test_godot_local_mcp_gateway.py
  test_godot_local_mcp_bridge_runtime.py
```

The implementation plan must reassess this file map against the then-current Base main and PR #197 result before creating files.

## Dependency policy

- Python 3.12.
- Official MCP Python SDK stable 1.x, exact version and hashes pinned in implementation.
- Do not adopt the pre-release MCP Python SDK 2.x in v1.
- Runtime dependencies must be minimal and hash-locked.
- Godot Bridge uses Godot 4.7.1 APIs already available to the project.
- No Node.js runtime is required for the Gateway.
- MCP Inspector or a protocol conformance client is a development/test dependency, not a production runtime dependency.

## Testing strategy

### Phase 1: static and fake-Bridge TDD

Test-only RED precedes implementation.

Coverage:

- closed Schemas and semantic validation;
- protocol stdout contains MCP frames only;
- stderr diagnostics contain no secrets;
- Codex and GPT profiles accepted independently;
- DeepSeek, unknown, disabled, expired, or missing profiles denied;
- no workspace-active VS Code MCP configuration shipped;
- exact capability allowlist;
- request/result hash and snapshot mapping;
- frame, depth, batch, connection, and idle limits;
- approval cannot be generated through an MCP tool;
- fake Bridge challenge/response and replay rejection.

### Phase 2: actual Godot 4.7.1 Bridge Runtime

In a disposable fixture:

- Bridge starts only in Editor mode;
- binds loopback only;
- descriptor is outside the repository and expires;
- wrong HMAC, project, client, service, Bridge, and Editor identities fail;
- read-only status and Scene inspect pass;
- rename remains pending until a test-only approval broker approves the exact request;
- stale, tampered, expired, cross-client, replayed, and queue-full cases fail without mutation;
- Undo/Redo, dirty state, save, physical SHA-256, ledger, evidence, and cleanup pass;
- source project remains unchanged.

The test-only approval broker cannot be present in production builds.

### Phase 3: MCP protocol verification

Verify:

- initialize and negotiated protocol version;
- tools/list exact set;
- tools/call input and output Schema behavior;
- structured errors;
- host disconnect and restart;
- stdout/stderr separation;
- Codex-like and VS Code-like stdio client harnesses.

Use the official stable SDK conformance behavior and MCP Inspector where practical.

### Phase 4: Switchy E2E

After PR #197 and the corresponding Switchy Pilot regression are green:

```text
Codex-like MCP client
→ stdio Gateway
→ authenticated Godot Bridge
→ existing Base adapter
→ actual Switchy disposable project
→ inspect
→ approval-pending rename
→ approved rename
→ Undo/save/restore
→ existing 65+ project tests
→ source integrity
```

Repeat with the `gpt-vscode` profile.

Negative E2E:

- `deepseek` profile denied before discovery;
- Codex approval cannot authorize GPT request;
- GPT stale observation cannot overwrite Codex change;
- no active workspace MCP configuration is required.

### Phase 5: Windows and human approval UI

Because the user's primary environment is Windows and VS Code:

- Windows GitHub runner or equivalent exact Godot 4.7.1 Runtime evidence;
- real VS Code `Godot Authoring` profile startup;
- real Codex registration startup;
- Godot approval dock manual approval/rejection;
- Editor restart, stale descriptor cleanup, credential rotation, and recovery mode;
- DeepSeek profile confirms no server registration or discovered tools.

Automated test approval is not human evidence. Until a person uses the dock successfully, status remains `HUMAN_NOT_RUN`.

## Evidence and readiness

Keep independent states:

```yaml
static_contract: PASS_OR_FAIL
mcp_protocol: PASS_OR_FAIL
fake_bridge: PASS_OR_FAIL
godot_bridge_runtime_linux: PASS_OR_FAIL
godot_bridge_runtime_windows: PASS_OR_NOT_RUN
switchy_codex_e2e: PASS_OR_NOT_RUN
switchy_gpt_vscode_e2e: PASS_OR_NOT_RUN
deepseek_denial: PASS_OR_NOT_RUN
human_approval_dock: HUMAN_PASS_OR_HUMAN_NOT_RUN
second_project_e2e: PASS_OR_NOT_RUN
remote_transport: NOT_IMPLEMENTED
production_adapter_ready: false
```

One Switchy result does not establish universal project compatibility. Production readiness requires a structurally different second project, Windows operation, human approval UI evidence, recovery evidence, and resolved security review.

## Prerequisites and sequencing

Implementation must not begin until:

```yaml
written_design_reviewed_by_user: true
implementation_plan_approved_by_user: true
base_pilot_staging_fix: MERGED_AND_GREEN
switchy_reusable_pilot_regression: GREEN
fresh_base_main_recorded: true
no_conflicting_mcp_or_bridge_implementation_pr: true
```

Recommended sequence:

1. finish Base PR #197 or its green successor;
2. finish Switchy PR #94 or re-pin it to the green successor;
3. merge this design/plan documentation after explicit approval;
4. implement protocol-only Gateway with fake Bridge using TDD;
5. implement authenticated Godot Bridge and approval dock;
6. run MCP protocol, Godot, Switchy Codex, GPT, and DeepSeek-denial E2E;
7. run Windows and human approval UI checks;
8. run a structurally different second-project Pilot;
9. decide whether capability expansion or production adoption is justified.

## Definition of Done for the first implementation PR

```yaml
test_only_red_history: REQUIRED
exact_head_ci: PASS
mcp_stdio_initialize_tools_call: PASS
codex_profile: PASS
gpt_vscode_profile: PASS
deepseek_profile: DENIED
loopback_only: PASS
bridge_mutual_authentication: PASS
godot_scene_inspect: PASS
godot_node_rename_approval_pending: PASS
godot_node_rename_after_external_approval: PASS
cross_client_approval_reuse: BLOCKED
stale_and_tamper_cases: BLOCKED
source_integrity: PASS
switchy_project_regression: PASS
windows_runtime: PASS_OR_EXPLICIT_NOT_RUN
human_approval_ui: HUMAN_PASS_OR_HUMAN_NOT_RUN
second_project: NOT_RUN_ALLOWED_FOR_FIRST_PR
production_adapter_ready: false
merge_authorization: NOT_GRANTED
```

The first implementation PR stops before merge and before adding broader mutation capabilities.

## Recovery and uninstall

- Stop Gateway processes.
- Disable the project-local Bridge plugin.
- Delete stale discovery descriptors and rotate client profile credentials.
- Start Godot with `--recovery-mode` when normal plugin startup fails.
- Remove the project-local Bridge and adapter according to the pinned adoption manifest.
- Verify normal Editor startup and existing project tests.
- Never reuse pre-recovery Bridge, Editor, service, or approval identities.

## Self-review

```yaml
placeholder_scan: PASS
contradiction_scan: PASS
scope: SINGLE_GATEWAY_AND_BRIDGE_V1
model_identity_claim: EXPLICITLY_LIMITED_TO_HOST_PROFILE_IDENTITY
workspace_config_leak: BLOCKED_BY_PROFILE_SCOPED_INSTALLATION
deepseek_denial_boundary: EXPLICIT
human_approval_boundary: EXPLICIT
existing_base_contract_reuse: REQUIRED
pr_197_dependency: EXPLICIT
implementation_started: false
production_claim: false
```
