# Godot Live Editor Contract v2 Reconciliation Design

## Status

- Date: 2026-08-05
- State: `APPROVED_DIRECTION_WRITTEN_SPEC_REVIEW_PENDING`
- Parent PR: `#152 feat: add Godot live editor automation contract`
- Parent branch: `agent/godot-live-editor-automation`
- Parent exact HEAD at branch creation: `e065fe2b7c7f9a07558eb5dea99db09d0beb6a10`
- Reconciliation branch: `agent/godot-live-editor-contract-v2-design`
- Prior hardening PR: `#153 feat: harden Godot live-editor contracts`
- Scope: design and later static contract reconciliation only
- Runtime pilot implementation: separate follow-up after v2 static GREEN

## Decision Summary

Keep the approved ownership model:

```text
existing Base Skill owners
→ reusable Godot automation safety contract
→ project-local capability manifest and thin adapter
→ project-owned CLI / EditorPlugin / runtime-debugger implementation
```

Do not add a new broad Base Skill, universal MCP server, production runtime bridge, arbitrary script execution default, or remote network endpoint.

Replace the draft v1 operation model with a v2 model that separates independent policy axes, binds approvals and results to the exact execution target and contract snapshot, validates transport security by transport kind, validates structured outputs, and prevents stale observation from overwriting newer Editor state.

PR #153 remains historical evidence until v2 implementation reaches GREEN. It must not be merged or force-rebased into the moving parent. After v2 is integrated into #152, #153 may be closed as superseded with its useful findings preserved in history.

## Problem Statement

The draft v1 contract mixes independent meanings in one `operation_class` enum:

```text
READ_ONLY
IDEMPOTENT_MUTATION
APPROVAL_REQUIRED_MUTATION
NON_RETRYABLE_MUTATION
LONG_RUNNING_TASK
```

This model cannot faithfully represent common combinations such as:

- an idempotent mutation that still requires user approval;
- a long-running read-only inspection;
- a long-running approved mutation;
- a non-idempotent long-running operation;
- a reversible mutation that differs from an irreversible mutation.

The latest parent fix permits approval metadata for an idempotent mutation, but it does not remove the underlying mixed-axis model. The v2 contract must solve the model rather than add more exceptions.

Additional gaps remain:

- project identity does not uniquely identify the active automation server, Editor process, or runtime debugger session;
- approval tokens do not bind to the catalog and capability schema version that the user reviewed;
- loopback HTTP does not mechanically require Origin validation, authentication, and session binding;
- capabilities declare input schemas but not output schemas;
- mutations do not carry stale-state preconditions;
- task records lack a small generic lifecycle profile suitable for mapping to MCP Tasks without making MCP mandatory;
- recovery does not explicitly route Editor startup failures through Godot recovery mode;
- file-backed evidence lacks a mandatory content hash.

## Design Principles

1. **Orthogonal policy axes** — side effect, idempotency, approval, lifetime, and rollback are separate.
2. **Fail closed before engine action** — Schema and semantic validation run before CLI, EditorPlugin, or runtime mutation.
3. **Exact target binding** — project, automation server, Editor instance, runtime session, capability snapshot, request, and preconditions are part of the authoritative request identity.
4. **Protocol-neutral core** — Base owns generic execution safety; MCP is an optional profile mapping.
5. **Typed capabilities only** — no arbitrary code, expression, shell, script, or unrestricted property path default.
6. **Evidence is not readiness** — a valid contract or connected endpoint does not imply Editor, game runtime, physical input, or human usability success.
7. **Recovery before retry** — unknown outcomes are reconciled; irreversible or non-idempotent operations are never blindly retried.
8. **Project ownership** — real commands and Godot integration remain project-specific.
9. **Minimum active surface** — no Registry or broad router expansion unless existing routing cannot select the project adapter.

## Scope Boundary

### Included

- v2 capability-manifest design;
- v2 operation-envelope design;
- semantic validator obligations;
- transport security profile;
- execution-target and contract-snapshot identity;
- structured output validation;
- task lifecycle core and optional MCP mapping;
- mutation preconditions and conflict handling;
- evidence integrity fields;
- Godot recovery-mode contract;
- migration and PR reconciliation strategy;
- executable static and adversarial test requirements.

### Excluded

- a real MCP server;
- a universal Godot EditorPlugin implementation;
- network exposure outside loopback or approved local IPC;
- modification of a user game project;
- production export control bridge;
- physical-input automation;
- human usability claims;
- runtime pilot implementation in the same change set;
- Base Registry or release-lock changes.

## Architecture

```text
Agent client
→ protocol adapter: generic CLI/JSON or optional MCP profile
→ project-local automation service
→ v2 Schema validation
→ v2 semantic validation
→ exact target and snapshot verification
→ typed project capability
→ Godot CLI / EditorPlugin / runtime debugger
→ structured output validation
→ evidence hashing and result binding
→ operation ledger / task lifecycle
```

Validation failure stops before an engine action. Output validation failure returns a failed envelope and must not be promoted to successful evidence.

## Contract v2 Model

### 1. Effect Kind

```yaml
effect_kind:
  READ_ONLY
  MUTATION
```

Rules:

- `READ_ONLY` must not modify project files, Editor state, runtime state, external systems, or durable ledgers other than bounded diagnostic access records.
- `MUTATION` must declare idempotency, approval, rollback, retry, precondition, and evidence behavior.

### 2. Idempotency

```yaml
idempotency:
  NOT_APPLICABLE
  IDEMPOTENT
  NON_IDEMPOTENT
```

Rules:

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` uses `IDEMPOTENT` or `NON_IDEMPOTENT`.
- `IDEMPOTENT` requires an idempotency key and operation ledger.
- `NON_IDEMPOTENT` forbids automatic retry.
- Idempotency does not imply approval is unnecessary.

### 3. Approval Policy

```yaml
approval_policy:
  NOT_REQUIRED
  REQUIRED
```

Rules:

- Approval is independent of idempotency and execution lifetime.
- `REQUIRED` must bind to the exact normalized request, target identity, contract snapshot, preconditions, and effect policy.
- Expired, mismatched, reused for another snapshot, or wrong-instance approval fails closed.
- `IRREVERSIBLE` rollback policy always requires approval.

### 4. Execution Mode

```yaml
execution_mode:
  SYNCHRONOUS
  LONG_RUNNING_TASK
```

Rules:

- `SYNCHRONOUS` finishes in the request lifetime and uses no durable task ID.
- `LONG_RUNNING_TASK` creates one durable receiver-generated task ID, records a ledger entry before returning, and supports status/resume.
- Lifetime does not weaken approval or retry policy.

### 5. Rollback Policy

```yaml
rollback_policy:
  NOT_APPLICABLE
  EDITOR_UNDO_REDO
  SNAPSHOT
  MANUAL
  IRREVERSIBLE
```

Rules:

- `READ_ONLY` uses `NOT_APPLICABLE`.
- `MUTATION` must select one non-null policy.
- `EDITOR_UNDO_REDO` requires a single explicit Editor transaction boundary.
- `SNAPSHOT` requires a named pre-change snapshot and verified restore path.
- `MANUAL` requires an operator-readable recovery reference.
- `IRREVERSIBLE` requires approval, forbids automatic retry, and requires an explicit stop condition before execution.

## Valid Combination Examples

```text
READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + SYNCHRONOUS + NOT_APPLICABLE
READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + LONG_RUNNING_TASK + NOT_APPLICABLE
MUTATION + IDEMPOTENT + NOT_REQUIRED + SYNCHRONOUS + EDITOR_UNDO_REDO
MUTATION + IDEMPOTENT + REQUIRED + SYNCHRONOUS + SNAPSHOT
MUTATION + IDEMPOTENT + REQUIRED + LONG_RUNNING_TASK + SNAPSHOT
MUTATION + NON_IDEMPOTENT + REQUIRED + LONG_RUNNING_TASK + MANUAL
MUTATION + NON_IDEMPOTENT + REQUIRED + SYNCHRONOUS + IRREVERSIBLE
```

Invalid combinations fail Schema or semantic validation rather than being interpreted by prose.

## Execution Target Identity

### Project Identity

Retain:

```yaml
project_identity:
  normalized_project_path:
  project_godot_sha256:
  project_fingerprint:
```

### Instance Identity

Add:

```yaml
instance_identity:
  automation_server_instance_id:
  editor_instance_id:
  runtime_session_id:
  runtime_session_state:
    NOT_APPLICABLE
    ACTIVE
    INACTIVE
```

Rules:

- `automation_server_instance_id` is regenerated on every automation service start.
- `editor_instance_id` identifies the current Editor process when an Editor is required.
- `runtime_session_id` identifies the selected debugger/runtime session.
- Runtime actions require `runtime_session_state: ACTIVE`.
- Port, PID, window title, folder substring, and process name are hints only.
- Approval, ledger, task, and result bindings include the instance fields relevant to the capability execution path.
- Reconnecting to a new service or Editor instance invalidates an old approval unless the operation is explicitly re-approved.

## Contract Snapshot Binding

Every operation carries:

```yaml
contract_snapshot:
  contract_version:
  adapter_version:
  catalog_sha256:
  capability_schema_sha256:
  output_schema_sha256:
  protocol_profile:
    GENERIC
    MCP
  protocol_version:
```

Rules:

- `request_hash` is calculated from the canonical normalized arguments, target identity, contract snapshot, and preconditions.
- Approval token binding repeats and must equal the top-level snapshot.
- Ledger and task result binding repeat and must equal the active snapshot.
- A changed catalog, capability schema, output schema, adapter, protocol profile, or target instance invalidates prior approval.
- Semantic validation performs equality checks that JSON Schema cannot express.

## Capability Manifest v2

Each capability declares:

```yaml
capability_id:
description:
execution_path:
  CLI_HEADLESS
  EDITOR_PLUGIN
  RUNTIME_DEBUGGER

effect_kind:
idempotency:
approval_policy:
execution_mode:
rollback_policy:

input_schema:
output_schema:

precondition_policy:
  NONE
  OPTIONAL
  REQUIRED

retry_policy:
  automatic:
  maximum_attempts:
  requires_ledger:

timeout_policy:
  milliseconds:
  unknown_outcome:
    SAFE_TO_RETRY
    RECONCILE_BEFORE_RETRY
    RESUME_BY_TASK_ID
    FAIL_CLOSED

evidence_outputs:
unsupported_states:
```

Semantic validation additionally enforces:

- duplicate `capability_id` rejection;
- project-test runner reference existence and `TEST_RESULT` evidence;
- valid cross-axis combinations;
- input and output Schema object validity;
- transport requirements for the selected execution path;
- no path outside approved project or artifact roots;
- no undeclared capability execution.

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
  target_revision:
  target_content_sha256:
  expected_dirty_state:
    NOT_APPLICABLE
    CLEAN
    DIRTY
  expected_scene_path:
  conflict_policy: FAIL_CLOSED

approval:
  state:
    NOT_REQUIRED
    REQUIRED
    APPROVED
    REJECTED
    EXPIRED
  token_binding:
  expires_at:

task:
result:
  success:
  code:
  message:
  data:
  result_hash:
  evidence:
```

The operation envelope does not carry an arbitrary executable command. It carries a declared `capability_id` and typed data validated against the manifest input Schema.

## Stale-State and Concurrent-Edit Protection

Mutation capabilities use preconditions when they touch Scene, Resource, Inspector, ProjectSettings, imported assets, or other human-editable state.

Rules:

- observation returns a stable revision or content hash suitable for a later mutation precondition;
- the mutation repeats the observed revision/hash and expected dirty state;
- mismatch returns `TARGET_STATE_CONFLICT` before mutation;
- conflict policy is fixed to `FAIL_CLOSED` in v2;
- the agent must re-observe and obtain renewed approval when required;
- a dirty Editor Scene is never silently saved or overwritten;
- batch actions cannot hide separate rollback or approval boundaries.

## Transport Security Profile

### Common Fields

```yaml
transport:
  kind:
    DISABLED
    CLI
    LOCAL_HTTP
    NAMED_PIPE
    STDIO_BRIDGE
    PROJECT_DEFINED
  enabled:
  bind_host:
  endpoint_identity:
  protocol_profile:
  protocol_version:
  access_control:
    authentication_mode:
      NOT_APPLICABLE
      SESSION_TOKEN
      OAUTH_2_1
      OS_PEER_CREDENTIAL
    origin_policy:
      NOT_APPLICABLE
      EXPLICIT_ALLOWLIST
    session_binding:
      NOT_APPLICABLE
      PROJECT_CLIENT_SESSION
    os_access_control:
      NOT_APPLICABLE
      CURRENT_USER_ONLY
```

### Conditional Rules

- `LOCAL_HTTP` binds only to `127.0.0.1` or `::1` and requires:
  - `origin_policy: EXPLICIT_ALLOWLIST`;
  - `authentication_mode: SESSION_TOKEN` or `OAUTH_2_1`;
  - `session_binding: PROJECT_CLIENT_SESSION`;
  - secrets stored outside the manifest and repository.
- `STDIO_BRIDGE` requires current-process ownership and does not accept HTTP Origin fields.
- `NAMED_PIPE` requires `OS_PEER_CREDENTIAL` or `CURRENT_USER_ONLY` access control.
- `CLI` uses no listening endpoint and no ambient network credential.
- `PROJECT_DEFINED` cannot weaken the common identity, approval, path, output, audit, and evidence rules.
- Remote and wildcard bind remain unsupported in the Base default contract.
- Session IDs are routing identifiers, not authentication by themselves.

## Structured Output Validation

Capabilities declare both `input_schema` and `output_schema`.

Execution order:

```text
validate input
→ validate semantic bindings
→ execute typed capability
→ validate result.data against output_schema
→ calculate result_hash
→ create evidence and ledger binding
```

An output mismatch returns `OUTPUT_SCHEMA_MISMATCH`, records no successful evidence, and blocks task completion promotion.

## Generic Task Core

```yaml
task:
  task_id:
  state:
    NOT_APPLICABLE
    QUEUED
    RUNNING
    INPUT_REQUIRED
    PENDING
    COMPLETED
    FAILED
    CANCELLED
    STALE
  created_at:
  last_updated_at:
  ttl_ms:
  poll_interval_ms:
  cancellation_policy:
    NOT_SUPPORTED
    SAFE_BEFORE_COMMIT
    SUPPORTED
  result_binding:
```

Rules:

- task IDs are generated by the receiver and unique within the automation server instance;
- start is recorded once before the initial response;
- repeated start with the same idempotency identity returns the same task;
- terminal states require an exact result binding and result hash;
- task expiration does not imply operation rollback;
- cancellation support is declared, never assumed;
- `INPUT_REQUIRED` does not permit hidden continuation without new user or client input.

### Optional MCP Mapping

When `protocol_profile: MCP`, the adapter maps the generic task core to the supported MCP Tasks extension version. MCP-specific fields are not required for `GENERIC` CLI, stdio, pipe, or custom adapters.

The Base core must not depend on a single MCP draft version. The exact MCP profile version is pinned in `contract_snapshot.protocol_version` and the project tool adoption record.

## Evidence Integrity

Each evidence entry declares:

```yaml
kind:
state:
path:
artifact_sha256:
generated_at:
producer:
```

Rules:

- evidence kind and state families remain mechanically constrained;
- file-backed PASS evidence requires a confined path and SHA-256;
- `NOT_RUN`, `NOT_CONFIGURED`, and `BLOCKED_ENVIRONMENT` use no artifact path or hash;
- evidence producer identifies the capability and tool version, not a human-readable free-form claim;
- human validation remains separate from engine, runtime, screenshot, input, and contract evidence;
- successful Editor connection is not runtime or human evidence.

## Godot Recovery Contract

For EditorPlugin or tool-script startup failure:

```text
normal Editor startup fails
→ stop automation mutation
→ start Godot with --recovery-mode
→ disable or remove the project-local plugin
→ mark operational state BLOCKED_RECOVERY
→ restore declared snapshot or manual rollback reference
→ validate normal Editor startup
→ issue a new automation server instance ID
→ require renewed approval before mutation
```

Recovery mode is an emergency path, not evidence that the integration is healthy. Recovery actions remain bounded to the project-local adapter/plugin and declared artifact roots.

## Tool Adoption Record

A configured project retains:

```yaml
tool_adoption:
  source_type:
    OFFICIAL
    OPEN_SOURCE
    COMMERCIAL
    PROJECT_LOCAL
    CUSTOM
  source_reference:
  version_pin:
  telemetry_policy:
  external_data_policy:
  uninstall_reference:
  rollback_reference:
```

Add:

```yaml
  integrity_reference:
  license_reference:
  vulnerability_reviewed_at:
```

Rules:

- mutable branch names are not exact version pins;
- external telemetry or data transfer requires an explicit allowlist and user-approved policy;
- install success is not adoption success;
- trial, adopt, adapt, reject, and build-custom decisions remain owned by the existing Godot asset/plugin evaluation Skill.

## Error Codes

The v2 validator and adapter use stable codes including:

```text
CAPABILITY_NOT_DECLARED
DUPLICATE_CAPABILITY_ID
CONTRACT_VERSION_MISMATCH
ADAPTER_VERSION_MISMATCH
CATALOG_STALE
CAPABILITY_SCHEMA_MISMATCH
OUTPUT_SCHEMA_MISMATCH
PROJECT_IDENTITY_MISMATCH
AUTOMATION_INSTANCE_MISMATCH
EDITOR_INSTANCE_MISMATCH
RUNTIME_SESSION_INACTIVE
RUNTIME_SESSION_MISMATCH
APPROVAL_REQUIRED
APPROVAL_TOKEN_MISMATCH
APPROVAL_EXPIRED
TARGET_STATE_CONFLICT
UNSAFE_RETRY_BLOCKED
TASK_RESULT_STALE
TRANSPORT_SECURITY_MISMATCH
PATH_OUTSIDE_APPROVED_ROOT
RECOVERY_REQUIRED
```

Message text may change; automation branches on stable codes.

## Runtime Pilot Relationship

The existing Godot 4.7.1 runtime pilot design and plan were written against draft v1. They remain blocked until v2 static reconciliation reaches GREEN.

The v2 implementation plan must update the pilot documents so the later pilot proves at least:

- approved idempotent mutation under the independent approval axis;
- exact automation server and Editor instance binding;
- catalog and capability schema snapshot binding;
- stale precondition rejection;
- structured output validation;
- long-task start/status/resume with the generic task core;
- EditorPlugin load and disable through recovery mode;
- honest limits for network MCP, runtime debugger, physical input, and human usability.

No uploaded user game project is modified by the contract reconciliation.

## Migration Strategy

The v1 files exist only in open Draft PR work and are not a released Base contract. Therefore v2 does not maintain two active schemas.

Implementation will:

1. introduce `schema_version: 2` and `contract_version: 2.0.0`;
2. rename active Schema files to explicit `-v2.schema.json` paths;
3. update the template manifest, adapter, AGENTS fragment, contract docs, tests, and validator to v2;
4. remove active references to draft v1 paths from the parent change set;
5. preserve v1 history through Git and PR history rather than active compatibility files;
6. keep Registry and released Base locks unchanged;
7. close #153 as superseded only after current-parent v2 GREEN evidence exists.

## PR and Branch Strategy

1. This design branch starts from exact parent HEAD `e065fe2b7c7f9a07558eb5dea99db09d0beb6a10`.
2. The design PR targets `agent/godot-live-editor-automation`, not `main`.
3. This phase adds only the written design specification.
4. After written-spec approval, create a detailed implementation plan on the same design branch.
5. Before implementation, re-fetch the latest parent HEAD and open related PRs.
6. If the parent moved, create a fresh implementation branch from its latest exact HEAD and bring the approved spec/plan forward without force-updating another chat's branch.
7. Run TDD with a test-only RED commit before implementation.
8. Validate the current parent+implementation merge ref, not only the feature head.
9. Do not merge, retarget, close, or force-update #152 or #153 without explicit integration approval.

## Test Design

### Policy-Axis Tests

- approved idempotent mutation is valid;
- unapproved capability with `approval_policy: REQUIRED` fails;
- read-only cannot declare mutation idempotency or rollback;
- mutation cannot use `idempotency: NOT_APPLICABLE`;
- non-idempotent operation cannot automatically retry;
- irreversible mutation requires approval and forbids retry;
- long-running read-only and long-running approved mutation are both representable.

### Identity and Snapshot Tests

- wrong automation server instance fails;
- inactive or wrong runtime session fails;
- changed catalog hash invalidates approval;
- changed capability or output Schema hash invalidates approval;
- changed adapter/protocol version invalidates approval;
- task result from another instance or snapshot fails.

### Transport Tests

- loopback HTTP without Origin allowlist fails;
- loopback HTTP without authentication fails;
- loopback HTTP without client/session binding fails;
- wildcard or external bind fails;
- stdio does not accept HTTP-only security claims;
- named pipe without current-user or peer-credential restriction fails.

### Data and Concurrency Tests

- output not matching `output_schema` fails;
- stale target revision or content hash fails before mutation;
- unexpected dirty Scene state fails;
- path traversal or symlink escape fails;
- successful evidence without a confined artifact hash fails.

### Task Tests

- receiver creates one task ID;
- repeated idempotent start returns the same task;
- terminal state requires exact result binding;
- `INPUT_REQUIRED` requires explicit continuation input;
- unsupported cancellation fails without claiming cancellation;
- expired task does not claim rollback.

### Recovery Tests

- plugin-start failure routes to recovery-required state;
- recovery documentation includes `--recovery-mode`;
- post-recovery mutation requires a new instance identity and approval;
- production export contains no automation bridge.

### Regression and Routing Tests

- existing non-Godot work does not select the project adapter;
- normal asset/plugin evaluation remains owned by the existing evaluation Skill;
- Registry blob and release locks remain unchanged;
- required CI discovers and executes focused tests;
- canonical-reference freshness passes;
- no unresolved `MUST_FIX` remains at the reviewed exact HEAD.

## Expected Implementation Surfaces

Final file scope must be revalidated against the latest parent before implementation. Expected surfaces are:

```text
docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md
docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md
docs/superpowers/specs/2026-08-05-godot-live-editor-automation-design.md
docs/superpowers/plans/2026-08-05-godot-live-editor-automation.md
docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md
docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md
schemas/godot-live-editor-capability-manifest-v2.schema.json
schemas/godot-live-editor-operation-envelope-v2.schema.json
templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json
templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md
templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md
tools/validate_godot_live_editor_contract.py
tests/test_godot_live_editor_contract.py
tests/test_godot_live_editor_idempotent_approval.py
required existing CI discovery modules only when needed
```

No new workflow topology is planned. Focused tests must be connected to existing required suites.

## Adversarial Review Checklist

Before GREEN, attack the design and implementation for:

- approval bypass through another policy combination;
- stale approval after catalog or schema change;
- stale endpoint, Editor, or runtime session reuse;
- DNS rebinding and unauthenticated loopback HTTP;
- session fixation or session ID treated as authentication;
- dirty Scene overwrite and concurrent human edits;
- path canonicalization and symlink escape;
- arbitrary script or command smuggling through typed fields;
- output Schema bypass and false successful evidence;
- task duplication, stale result replay, and unsupported cancellation claims;
- irreversible operation retry;
- plugin startup failure and incomplete uninstall;
- production bridge leakage;
- Registry, release-lock, or unrelated PR drift;
- CI success on an old head rather than the current merge ref.

## Merge Readiness Gates

The v2 reconciliation is merge-ready only when all are true:

```yaml
written_spec_approved: true
implementation_plan_current: true
latest_parent_reconciled: true
focused_tdd_red_recorded: true
focused_tdd_green: true
semantic_validator_green: true
repository_regressions_green: true
current_merge_ref_ci: PASS
canonical_reference_freshness: PASS
unresolved_must_fix: 0
unresolved_review_threads: 0
registry_and_release_locks_unchanged: true
runtime_readiness_claim: false
```

The contract PR may merge without a real Godot runtime pilot only when the evidence explicitly remains static-contract-only and no runtime readiness or project adoption is claimed.

## Benchmark References

The design extracts reusable principles rather than copying APIs or product-specific commands:

- Unity CLI and Pipeline: structured command discovery and an observe/act/verify loop against Editor and development Player.
- MCP tool contracts: separate behavioral annotations, structured input/output schemas, transport security, and optional task extension mapping.
- Godot official extension points: CLI/headless operation, EditorPlugin, EditorDebuggerPlugin sessions, main-thread Editor changes, UndoRedo, and `--recovery-mode`.

Reference URLs:

- https://unity.com/blog/meet-the-unity-cli
- https://modelcontextprotocol.io/specification/2025-11-25/schema
- https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
- https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks
- https://docs.godotengine.org/en/stable/classes/class_editordebuggerplugin.html
- https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html

These references are benchmarking inputs. Base remains protocol-neutral and project-owned at the execution layer.
