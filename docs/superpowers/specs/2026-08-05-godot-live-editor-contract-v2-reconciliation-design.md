# Godot Live Editor Contract v2 Reconciliation Design

## Status

- Date: 2026-08-05
- State: `WRITTEN_SPEC_REVIEW_PENDING`
- Base: `main@83683eecaaeaf415bf629fe5a1231fc6cef575f3`
- Predecessor: merged PR #152
- Supersedes: divergent Draft PRs #153 and #154
- Scope: static contract reconciliation only
- Implementation: not started

## Decision

Preserve the architecture merged in PR #152:

```text
existing Base Skill owners
→ reusable Godot safety contract and schemas
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

This cannot represent common operations without exceptions, including:

- an idempotent mutation that still requires approval;
- a long-running read-only inspection;
- a long-running approved mutation;
- a reversible non-idempotent mutation;
- an irreversible synchronous operation.

PR #152 safely handles the tested Pilot, but production Editor and runtime adapters need a model that does not infer approval, retry, lifetime, or rollback from one overloaded enum.

PR #153 additionally demonstrated that JSON Schema shape alone cannot prove equality between the active request and approval, task, ledger, and result bindings. PR #154 described a broader v2 model but was based on a pre-merge branch and duplicated the full #152 ancestry. This specification preserves their confirmed findings without merging either divergent branch.

## Goals

- Separate side effects, idempotency, approval, lifetime, and rollback.
- Bind every approved or durable operation to the exact project, service, Editor/runtime instance, contract snapshot, request, and precondition state.
- Add semantic validation for equality and cross-field rules that JSON Schema cannot express.
- Validate both capability input and output data.
- Prevent stale observations from overwriting newer Editor or file state.
- Keep local transport disabled until its security profile is fully declared.
- Migrate without silently changing the meaning of v1 manifests or captured evidence.
- Preserve Registry bytes, release locks, and existing Skill ownership.

## Non-goals

- No real MCP server in the v2 reconciliation PR.
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
- `MUTATION` requires explicit idempotency, approval, rollback, retry, precondition, ledger, and evidence behavior.

### Idempotency

```yaml
idempotency: NOT_APPLICABLE | IDEMPOTENT | NON_IDEMPOTENT
```

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` uses `IDEMPOTENT` or `NON_IDEMPOTENT`.
- `IDEMPOTENT` requires an idempotency key and durable operation ledger.
- `NON_IDEMPOTENT` forbids automatic retry.
- Idempotency never implies that approval is unnecessary.

### Approval policy

```yaml
approval_policy: NOT_REQUIRED | REQUIRED
```

- Approval is independent of idempotency and execution lifetime.
- `REQUIRED` binds the exact normalized request, target identity, contract snapshot, policy axes, preconditions, and expiry.
- Approval is single-use except for an exact replay of the same completed idempotent operation.
- A changed argument, instance, catalog, Schema, precondition, or operation identity requires renewed approval.

### Execution mode

```yaml
execution_mode: SYNCHRONOUS | LONG_RUNNING_TASK
```

- `SYNCHRONOUS` has no durable task ID.
- `LONG_RUNNING_TASK` creates one receiver-generated durable task before the initial response and uses status/resume rather than duplicate start.
- Execution lifetime does not weaken approval, retry, rollback, or evidence rules.

### Rollback policy

```yaml
rollback_policy:
  NOT_APPLICABLE | EDITOR_UNDO_REDO | SNAPSHOT | MANUAL | IRREVERSIBLE
```

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` must select a non-null rollback policy.
- `EDITOR_UNDO_REDO` requires one explicit `EditorUndoRedoManager` transaction boundary.
- `SNAPSHOT` requires a named pre-change snapshot and tested restore path.
- `MANUAL` requires an operator-readable recovery reference.
- `IRREVERSIBLE` always requires approval and forbids automatic retry.

## Valid representative combinations

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

### Project identity

Retain the v1 project identity:

```yaml
project_identity:
  normalized_project_path:
  project_godot_sha256:
  project_fingerprint:
```

### Instance identity

Add instance identity:

```yaml
instance_identity:
  automation_service_instance_id:
  editor_instance_id:
  runtime_session_id:
  runtime_session_state: NOT_APPLICABLE | ACTIVE | INACTIVE
```

Rules:

- A new automation-service process creates a new service instance ID.
- Editor capabilities require the selected Editor instance ID.
- Runtime capabilities require an active runtime session ID.
- Port, PID, process name, window title, and folder substring remain non-authoritative hints.
- Approval, ledger, task, and result bindings repeat all relevant identity fields.

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

The canonical request hash includes normalized arguments, project and instance identity, contract snapshot, policy axes, and preconditions.

Any snapshot change invalidates old approval and pending mutation authority. Semantic validation must prove equality between the top-level snapshot and approval, ledger, task, and terminal result bindings.

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

precondition_policy: NONE | OPTIONAL | REQUIRED
retry_policy:
timeout_policy:
evidence_outputs:
unsupported_states:
```

Additional manifest rules:

- capability IDs are unique;
- input and output Schemas are closed typed object Schemas;
- undeclared capability execution is impossible;
- project-test runner references resolve exactly once and declare `TEST_RESULT` evidence;
- file paths stay within approved project or artifact roots;
- transport requirements match the selected execution path;
- a configured manifest records detected/supported Godot versions, exact tool pin, telemetry policy, uninstall procedure, and rollback reference.

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
  effect_kind:
  idempotency:
  approval_policy:
  execution_mode:
  rollback_policy:

request_hash:
idempotency_key:
preconditions:
approval:
task:
result:
```

The envelope carries a declared capability and typed data, never an arbitrary executable command.

## Stale-state protection

Mutations of Scene, Resource, Inspector, ProjectSettings, imported assets, or other human-editable state use observation-derived preconditions:

```yaml
preconditions:
  target_revision:
  target_content_sha256:
  expected_dirty_state: NOT_APPLICABLE | CLEAN | DIRTY
  expected_scene_path:
  conflict_policy: FAIL_CLOSED
```

- A mismatch returns `TARGET_STATE_CONFLICT` before mutation.
- The client re-observes and obtains renewed approval when required.
- A dirty Scene is never silently saved or overwritten.
- One approval or rollback boundary cannot hide unrelated batch mutations.

## Semantic validator

JSON Schema validates structure. A separate deterministic validator enforces semantics.

The validator must reject:

- duplicate capability IDs;
- invalid policy-axis combinations;
- top-level/request/approval/ledger/task/result identity mismatch;
- catalog or input/output Schema hash mismatch;
- reused, expired, wrong-instance, or wrong-precondition approval;
- terminal task results without exact operation and result-hash binding;
- configured project-test runners that are missing, ambiguous, outside allowed roots, or lack `TEST_RESULT` evidence;
- transport configurations that do not satisfy their transport-specific security profile;
- PASS evidence without a confined artifact path and SHA-256;
- output data that fails the capability output Schema.

The validator runs before engine action and again before successful result promotion.

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
- MCP is an optional protocol profile layered on a valid transport; it is not the Base execution core.

## Generic task lifecycle

```yaml
task.state:
  NOT_APPLICABLE | NOT_STARTED | QUEUED | RUNNING | INPUT_REQUIRED |
  PENDING | COMPLETED | FAILED | CANCELLED | STALE
```

- The receiver generates the task ID.
- Start is persisted once before the initial response.
- An exact idempotent replay returns the same task.
- Terminal states require exact result identity and result hash.
- Cancellation support is declared, never assumed.
- Task expiry does not imply rollback.
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

- Kind/state pairs are mechanically constrained.
- File-backed PASS evidence requires a confined path and SHA-256.
- `NOT_RUN`, `NOT_CONFIGURED`, and `BLOCKED_ENVIRONMENT` have no artifact path or hash.
- Producer identifies the capability and exact tool version.
- Contract, execution, runtime, engine input, physical input, screenshot, project test, and human evidence remain separate.

## Godot recovery boundary

A project-local EditorPlugin or tool-script startup failure follows:

```text
stop mutation
→ start Godot with --recovery-mode
→ disable or remove the project-local adapter
→ mark BLOCKED_RECOVERY
→ restore the declared snapshot or manual recovery path
→ verify normal Editor startup
→ issue new service and Editor instance IDs
→ require renewed approval
```

Recovery-mode startup is recovery evidence, not production runtime success.

## Migration from v1

Do not rewrite v1 Schema meaning in place.

- Add versioned v2 capability and operation Schemas.
- Add the semantic validator alongside v2.
- Keep v1 schemas and captured Pilot evidence readable for audit and regression.
- Switch project templates to v2 only after v2 RED/GREEN tests and migration tests pass.
- A v1 configured manifest may be inspected during migration but cannot authorize production Editor mutation through a v2 adapter.
- The adapter reports an explicit migration-required state rather than guessing v1 intent.
- Remove v1 only through a later release decision with consumer inventory and compatibility evidence.

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

PR A uses TDD and must include:

- Schema rejection tests for invalid axis combinations;
- semantic equality tests for approval, ledger, task, and result bindings;
- duplicate capability and ambiguous test-runner rejection;
- input/output Schema validation tests;
- stale-state conflict tests;
- transport-profile security tests;
- evidence kind/state/path/hash tests;
- v1 audit-read compatibility and v1 mutation-authority rejection;
- unchanged Registry blob and release locks;
- exact-head required GitHub Actions and zero unresolved review threads.

Runtime and human evidence remain `NOT_RUN` in PR A.

## Acceptance criteria

- The written model represents all representative combinations without exception fields.
- Invalid combinations and binding mismatches fail before engine action.
- v1 audit evidence remains readable while v1 cannot silently authorize v2 mutation.
- Project templates and adapters do not switch until tests prove migration behavior.
- No new Base active Skill, universal server, project adoption, Registry change, or release-lock change occurs.
- Production adapter readiness remains `NOT_READY` after PR A.

## Relationship to PR #153 and PR #154

After this design PR is opened:

- close #153 as superseded, preserving its hardening findings in this specification;
- close #154 as superseded, preserving its orthogonal-axis and identity/snapshot model here;
- do not merge or rebase either divergent branch;
- implementation begins only after the user approves this written specification and a separate TDD implementation plan is committed.

## Rollback

Close the design PR and delete only its isolated branch. The merged v1 contract and Pilot on main remain unchanged. No project, Registry, release-lock, or Google Sheet rollback is required.