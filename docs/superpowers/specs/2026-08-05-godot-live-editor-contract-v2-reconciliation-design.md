# Godot Live Editor Contract v2 Reconciliation Design

## Status

- Date: 2026-08-05
- State: `APPROVED`
- Approved by user: 2026-08-05
- Base: `main@83683eecaaeaf415bf629fe5a1231fc6cef575f3`
- Predecessor: merged PR #152
- Supersedes: divergent Draft PRs #153 and #154
- Scope: static contract reconciliation only
- Implementation: not started
- Implementation plan: `docs/superpowers/plans/2026-08-05-godot-live-editor-contract-v2-reconciliation.md`

## Decision

Preserve the architecture merged in PR #152:

```text
existing Base Skill owners
→ reusable Godot safety contract and Schemas
→ project-local capability manifest and thin adapter
→ project-owned CLI / EditorPlugin / runtime-debugger implementation
```

Before implementing a production adapter, replace the mixed v1 `operation_class` model with a protocol-neutral v2 model whose policy axes are independent and mechanically validated.

Do not add a broad Base active Skill, universal MCP server, remote endpoint, arbitrary script execution default, or production-readiness claim.

## Why v2 is required

The v1 classes combine unrelated concerns:

```text
READ_ONLY
IDEMPOTENT_MUTATION
APPROVAL_REQUIRED_MUTATION
NON_RETRYABLE_MUTATION
LONG_RUNNING_TASK
```

They cannot represent common combinations without exceptions, including:

- an idempotent mutation that still requires approval;
- a long-running read-only inspection;
- a long-running approved mutation;
- a reversible non-idempotent mutation;
- an irreversible synchronous operation.

PR #152 safely handles the tested Pilot, but production Editor and runtime adapters need a model that does not infer approval, retry, lifetime, or rollback from one overloaded enum.

PR #153 also demonstrated that JSON Schema shape alone cannot prove equality between active request, approval, task, ledger, and result bindings. PR #154 described a broader v2 model but was based on a pre-merge branch and duplicated the #152 ancestry. This specification preserves their confirmed findings without merging either divergent branch.

## Goals

- Separate effect, idempotency, approval, execution lifetime, and rollback.
- Bind approved and durable operations to exact project, service, Editor/runtime instance, contract snapshot, request, and precondition state.
- Add semantic validation for equality and cross-field rules that JSON Schema cannot express.
- Validate both capability input and output data.
- Prevent stale observations from overwriting newer Editor or file state.
- Keep local transport disabled until its security profile is fully declared.
- Preserve v1 audit evidence without granting it v2 mutation authority.
- Preserve Registry bytes, release locks, and existing Skill ownership.

## Non-goals

- No real MCP server in static reconciliation PR A.
- No production EditorPlugin or runtime debugger bridge.
- No game-project installation.
- No remote or wildcard network binding.
- No unrestricted GDScript, expression, shell, file, property-path, or ProjectSettings execution.
- No physical-input or human-usability claim.
- No Registry, release-lock, or frozen-release update.

## Contract v2 policy axes

Every capability declares all five axes.

### Effect kind

```yaml
effect_kind: READ_ONLY | MUTATION
```

- `READ_ONLY` cannot change project files, Editor state, runtime state, external systems, or durable operation state except bounded diagnostic access records.
- `MUTATION` declares idempotency, approval, rollback, retry, precondition, ledger, and evidence behavior.

### Idempotency

```yaml
idempotency: NOT_APPLICABLE | IDEMPOTENT | NON_IDEMPOTENT
```

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` uses `IDEMPOTENT` or `NON_IDEMPOTENT`.
- `IDEMPOTENT` requires an idempotency key and durable ledger.
- `NON_IDEMPOTENT` forbids automatic retry.
- Idempotency never removes an approval requirement.

### Approval policy

```yaml
approval_policy: NOT_REQUIRED | REQUIRED
```

- Approval is independent of idempotency and execution lifetime.
- `REQUIRED` binds normalized request, exact target identity, contract snapshot, policy axes, preconditions, and expiry.
- Approval is single-use except for an exact replay of the same completed idempotent operation.
- Changed arguments, instance, catalog, Schema, precondition, or operation identity require renewed approval.

### Execution mode

```yaml
execution_mode: SYNCHRONOUS | LONG_RUNNING_TASK
```

- `SYNCHRONOUS` has no durable task ID.
- `LONG_RUNNING_TASK` creates one receiver-generated durable task before the initial response and uses status/resume instead of duplicate start.
- Lifetime does not weaken approval, retry, rollback, or evidence rules.

### Rollback policy

```yaml
rollback_policy:
  NOT_APPLICABLE | EDITOR_UNDO_REDO | SNAPSHOT | MANUAL | IRREVERSIBLE
```

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` selects one non-null rollback policy.
- `EDITOR_UNDO_REDO` requires one explicit `EditorUndoRedoManager` transaction boundary.
- `SNAPSHOT` requires a named pre-change snapshot and tested restore path.
- `MANUAL` requires an operator-readable recovery reference.
- `IRREVERSIBLE` always requires approval and forbids automatic retry.

## Representative combinations

```text
READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + SYNCHRONOUS + NOT_APPLICABLE
READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + LONG_RUNNING_TASK + NOT_APPLICABLE
MUTATION + IDEMPOTENT + NOT_REQUIRED + SYNCHRONOUS + EDITOR_UNDO_REDO
MUTATION + IDEMPOTENT + REQUIRED + LONG_RUNNING_TASK + SNAPSHOT
MUTATION + NON_IDEMPOTENT + REQUIRED + SYNCHRONOUS + MANUAL
MUTATION + NON_IDEMPOTENT + REQUIRED + SYNCHRONOUS + IRREVERSIBLE
```

Invalid combinations fail before engine execution.

## Exact execution identity

Retain project identity:

```yaml
project_identity:
  normalized_project_path:
  project_godot_sha256:
  project_fingerprint:
```

Add instance identity:

```yaml
instance_identity:
  automation_service_instance_id:
  editor_instance_id:
  runtime_session_id:
  runtime_session_state: NOT_APPLICABLE | ACTIVE | INACTIVE
```

Rules:

- every automation-service start creates a new service instance ID;
- Editor capabilities require the selected Editor instance ID;
- runtime capabilities require an active runtime session ID;
- port, PID, process name, window title, and folder substring remain non-authoritative hints;
- approval, ledger, task, and result bindings repeat all relevant identity fields.

## Contract snapshot binding

Every operation carries:

```yaml
contract_snapshot:
  contract_version:
  adapter_version:
  catalog_sha256:
  capability_input_schema_sha256:
  capability_output_schema_sha256:
  protocol_profile: GENERIC | MCP
  protocol_version:
```

The canonical request hash includes normalized arguments, project and instance identity, contract snapshot, policy axes, and expected/observed preconditions.

Any snapshot change invalidates old approval and pending mutation authority. Semantic validation proves equality between top-level snapshot and approval, ledger, task, and terminal result bindings.

## Capability Manifest v2

A configured capability declares:

```yaml
capability_id:
description:
execution_path: CLI_HEADLESS | EDITOR_PLUGIN | RUNTIME_DEBUGGER

effect_kind:
idempotency:
approval_policy:
execution_mode:
rollback_policy:

input_schema:
output_schema:
input_schema_sha256:
output_schema_sha256:
path_access:
precondition_policy: NONE | OPTIONAL | REQUIRED
retry_policy:
timeout_policy:
evidence_outputs:
unsupported_states:
```

Additional rules:

- capability IDs are unique;
- input and output Schemas are closed typed objects;
- Schema hashes match canonical Schema content;
- undeclared capability execution is impossible;
- project-test runner references resolve exactly once and declare `TEST_RESULT` evidence;
- read/write roots stay within normalized `res://` or `artifacts/` boundaries;
- transport requirements match the selected execution path;
- configured manifests record detected/supported Godot versions, exact tool pin, telemetry policy, uninstall procedure, and rollback reference.

## Operation Envelope v2

```yaml
schema_version: 2
artifact_role: GODOT_LIVE_EDITOR_OPERATION_ENVELOPE
operation_id:
capability_id:
project_identity:
instance_identity:
contract_snapshot:
policy:
request:
  arguments:
request_hash:
idempotency_key:
preconditions:
approval:
task:
result:
```

The envelope carries a declared capability and typed data, never an arbitrary executable command.

## Stale-state protection

Mutations of Scene, Resource, Inspector, ProjectSettings, imported assets, or other human-editable state carry expected and execution-time observed values:

```yaml
preconditions:
  expected_target_revision:
  observed_target_revision:
  expected_target_content_sha256:
  observed_target_content_sha256:
  expected_dirty_state: NOT_APPLICABLE | CLEAN | DIRTY
  observed_dirty_state: NOT_APPLICABLE | CLEAN | DIRTY
  expected_scene_path:
  observed_scene_path:
  conflict_policy: FAIL_CLOSED
```

- Any expected/observed mismatch returns `TARGET_STATE_CONFLICT` before mutation.
- The client re-observes and obtains renewed approval when required.
- A dirty Scene is never silently saved or overwritten.
- One approval or rollback boundary cannot hide unrelated batch mutations.
- PR B must perform the final comparison and engine action on the Editor main thread without an unguarded interleaving window.

## Semantic validator

JSON Schema validates shape. A deterministic Python validator enforces semantics before engine action and before successful result promotion.

It rejects:

- duplicate or ambiguous capabilities;
- invalid policy-axis combinations;
- identity and contract-snapshot mismatch;
- input/output Schema or Schema-hash mismatch;
- request-hash mismatch;
- missing or conflicting preconditions;
- reused, expired, wrong-instance, or wrong-precondition approval;
- terminal task results without exact operation and result-hash binding;
- missing, ambiguous, unsafe, or evidence-incomplete project-test runners;
- transport configurations that violate their security profile;
- PASS evidence without confined path and SHA-256;
- output data that fails the capability output Schema.

History-sensitive approval reuse is checked against prior operation envelopes supplied to the validator.

## Transport profiles

The Base core remains protocol-neutral.

```yaml
transport.kind:
  DISABLED | CLI | LOCAL_HTTP | NAMED_PIPE | STDIO_BRIDGE | PROJECT_DEFINED
```

- Default is `DISABLED`.
- `CLI` has no listener.
- `LOCAL_HTTP` binds only to `127.0.0.1` or `::1` and requires explicit Origin allowlist, session authentication, bounded framing, and project-client session binding.
- `NAMED_PIPE` requires current-user or OS peer-credential enforcement.
- `STDIO_BRIDGE` requires current-process ownership and separates protocol stdout from diagnostics stderr.
- `PROJECT_DEFINED` cannot weaken identity, approval, path, output, audit, or evidence rules.
- Remote and wildcard bind remain unsupported by the Base default contract.
- MCP is an optional protocol profile layered on a valid transport, not the Base execution core.

## Generic task lifecycle

```yaml
task.state:
  NOT_APPLICABLE | NOT_STARTED | QUEUED | RUNNING | INPUT_REQUIRED |
  PENDING | COMPLETED | FAILED | CANCELLED | STALE
```

- receiver generates task ID;
- start is persisted once before initial response;
- exact idempotent replay returns the same task;
- terminal states require exact result identity and result hash;
- cancellation support is declared, never assumed;
- task expiry does not imply rollback;
- `INPUT_REQUIRED` cannot continue without explicit new input.

## Evidence integrity

Each evidence entry declares:

```yaml
kind:
state:
path:
artifact_sha256:
generated_at:
producer:
```

- kind/state pairs are mechanically constrained;
- file-backed PASS evidence requires a confined path and SHA-256;
- `NOT_RUN`, `NOT_CONFIGURED`, and `BLOCKED_ENVIRONMENT` have no artifact path or hash;
- producer identifies capability and exact tool version;
- contract, execution, runtime, engine input, physical input, screenshot, project test, and human evidence remain separate.

## Godot recovery boundary

A project-local EditorPlugin or tool-script startup failure follows:

```text
stop mutation
→ start Godot with --recovery-mode
→ disable or remove the project-local adapter
→ mark BLOCKED_RECOVERY
→ restore declared snapshot or manual recovery path
→ verify normal Editor startup
→ issue new service and Editor instance IDs
→ require renewed approval
```

Recovery-mode startup is recovery evidence, not production runtime success.

## Migration from v1

Do not rewrite v1 Schema meaning in place.

- add versioned v2 capability and operation Schemas;
- add semantic validator alongside v2;
- keep v1 Schemas and captured Pilot evidence readable for audit and regression;
- switch project installation template to v2 only after v2 RED/GREEN and migration tests pass;
- a v1 configured manifest may be inspected in `AUDIT` mode but cannot authorize v2 mutation;
- the adapter reports `MIGRATION_REQUIRED_V1` rather than guessing v1 intent;
- remove v1 only through a later release decision with consumer inventory and compatibility evidence.

## Delivery decomposition

### PR A — static v2 reconciliation

- v2 Schemas;
- semantic validator;
- v2 template manifest and adapter contract;
- migration rules and adversarial tests;
- no production server or project installation.

### PR B — Editor transaction adapter

- main-thread request queue;
- typed Scene/Node operations;
- `EditorUndoRedoManager`;
- dirty/save/import/refresh evidence;
- no network listener required.

### PR C — authenticated local transport and optional MCP profile

- bounded loopback or local IPC transport;
- authentication, session binding, framing, cleanup, and diagnostics separation;
- MCP mapping without weakening the generic contract.

### PR D — runtime debugger and real project pilots

- debugger-session identity;
- runtime observation capabilities;
- project behavior tests;
- at least two structurally different Godot project pilots;
- Windows, physical-input, and human checks remain separate gates.

## Testing strategy

PR A uses TDD and includes:

- Schema rejection for invalid axis combinations;
- semantic equality tests for approval, ledger, task, and result bindings;
- duplicate capability and ambiguous test-runner rejection;
- input/output Schema and hash validation;
- stale-state conflict tests;
- transport-profile security tests;
- evidence kind/state/path/hash tests;
- v1 audit-read compatibility and v1 mutation-authority rejection;
- unchanged Registry blob, release locks, v1 Schemas, and Pilot evidence;
- exact-head required GitHub Actions and zero unresolved review threads.

Runtime and human evidence remain `NOT_RUN` in PR A.

## Acceptance criteria

- The model represents all representative combinations without exception fields.
- Invalid combinations and binding mismatches fail before engine action.
- Expected/observed stale-state mismatch fails closed.
- v1 audit evidence remains readable while v1 cannot silently authorize v2 mutation.
- Project templates and adapters switch only after migration tests pass.
- No new Base active Skill, universal server, project adoption, Registry change, or release-lock change occurs.
- Production adapter readiness remains `NOT_READY` after PR A.

## Relationship to PR #153 and PR #154

- Both divergent Draft PRs are closed without merge.
- Their confirmed hardening and v2-model findings are preserved in this approved specification and implementation plan.
- Neither branch is rebased or merged into the current branch.

## Rollback

Close PR #157 and delete only its isolated branch. The merged v1 contract and Pilot on main remain unchanged. No project, Registry, release-lock, or Google Sheet rollback is required.