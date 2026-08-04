# Godot Live Editor Automation Design

## Status

Approved for implementation by the user on 2026-08-05 after comparing Base v9.4.3 with `NotNull92/hera-agent-unity` and rejecting a direct Unity-to-Godot clone.

## Problem

Base already owns project intake, operating-system installation and audit, runtime diagnosis, change validation, UI review, long-running task continuity, canonical-reference freshness, and Skill evolution. What is missing is a compact project-level contract for AI workers that must inspect or mutate a live Godot project safely.

Without that contract, each project can invent incompatible commands, identify an Editor by a transient port, retry unknown mutations after a timeout, overclaim test or input evidence, or copy a long engine-specific guide into multiple rule files. A broad new Base Skill would duplicate current owners and increase routing ambiguity.

## Decision

Adopt a three-layer pattern:

1. Base keeps existing active Skill ownership unchanged.
2. Base publishes a reusable Godot live-editor contract, schemas, and project template adapter.
3. Each Godot project installs only the adapter and capabilities it actually implements.

The design borrows execution-safety patterns from Hera—bootstrap discovery, compact capabilities, stable error codes, approval binding, operation ledgers, resumable tasks, and evidence-backed verification—but does not copy Unity APIs, C# handlers, UPM packaging, or Hera command syntax.

## Goals

- Provide one compact, project-installable Godot automation contract.
- Separate deterministic headless CLI work, EditorPlugin mutations, and runtime debugger observations.
- Identify the target by normalized project path and `project.godot` fingerprint, never by port alone.
- Require typed registered actions instead of arbitrary remote script execution by default.
- Separate read-only, idempotent, approval-gated, non-retryable, and long-running operations.
- Make timeout, retry, pending, resume, cancellation, and stale-result behavior explicit.
- Distinguish engine-synthesized input from physical OS input evidence.
- Keep project test-framework evidence separate from Godot engine self-tests.
- Preserve Base v9.4.3 Registry identity, release locks, and existing active Skill boundaries.

## Non-goals

- Do not implement a universal Godot MCP server or production EditorPlugin in Base.
- Do not add a new broad active Base Skill.
- Do not permit arbitrary GDScript or shell execution as a default project capability.
- Do not claim Godot runtime, cross-platform, human-usability, physical-input, or project-test validation from contract files alone.
- Do not modify any game project, Google Sheet, released lock, Registry entry, or frozen release derivative.
- Do not copy Hera source code or Unity-specific commands.

## Architecture

### 1. Deterministic CLI and headless path

Use the Godot executable directly for operations that can be reproduced outside the Editor:

```text
doctor
→ resolve executable and version
→ resolve normalized project path and project.godot fingerprint
→ import or headless command
→ run selected scene or registered script tool
→ build/export when declared
→ capture exit code and bounded logs
```

A project capability must name its concrete command, supported engine range, required files, side effects, timeout behavior, and evidence outputs. The contract never assumes that a generic Godot `--test` invocation is the project's test runner; a project test framework must be declared explicitly.

### 2. Optional EditorPlugin adapter path

Live scene, resource, inspector, or project-setting mutations use a project-owned EditorPlugin adapter:

```text
typed action request
→ identity and catalog freshness check
→ risk and approval check
→ serialized main-thread execution
→ EditorUndoRedoManager transaction where supported
→ save/import/refresh boundary
→ compact result envelope
```

The adapter exposes only registered typed actions. A transport can be local HTTP, named pipe, stdio bridge, or another project-approved loopback mechanism; transport choice is project-local and cannot weaken the common identity, approval, retry, or evidence contract.

### 3. Runtime and debugger path

Runtime observation can use an EditorDebuggerPlugin, EditorDebuggerSession, EngineDebugger messages, a project debug API, or bounded logs. Runtime messages remain observational unless the capability explicitly declares a mutation and its approval class.

```text
running game
↔ project runtime debug bridge
↔ Godot Editor debugger session
↔ project adapter
↔ AI worker
```

## Ownership and routing

| Concern | Existing owner | Godot adapter responsibility |
|---|---|---|
| Installation, capability inventory, legacy reconciliation | `managing-game-project-operating-system` | install and verify project-local adapter files and manifest |
| Runtime reproduction and isolation | `diagnosing-game-engine-runtime-failures` | supply compact status, logs, scene/node/signal evidence, and exact reproduction action |
| Static/runtime/regression evidence | `reviewing-and-validating-project-changes` | execute only declared validation capabilities and report truthful states |
| UI and interaction evidence | `auditing-and-refining-ui-art` | label engine input, physical input, screenshot, viewport, and human evidence separately |
| Pending and resumable execution | `maintaining-long-running-task-continuity` | persist `operation_id`, `task_id`, state, result identity, and resume boundary |
| Manifest, schema, adapter, and documentation drift | `auditing-canonical-reference-freshness` | fail closed on stale catalog or contract mismatch |
| Future Skill extraction | `evolving-project-discipline-skills` | promote only after repeated project evidence proves an independent boundary |

The project-local `godot-live-editor-operations` adapter is not added to the Base active Skill Registry. It routes engine operations to existing Base owners and is installed only in projects that actually expose compatible capabilities.

## Capability manifest

`GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` is the machine-readable source for adapter capabilities.

Required top-level facts:

```yaml
schema_version:
artifact_role:
contract_version:
adapter_version:
project_identity:
  normalized_project_path:
  project_godot_sha256:
  project_fingerprint:
engine_compatibility:
transport:
catalog:
capabilities:
validation:
```

Each capability declares:

```yaml
capability_id:
description:
execution_path: CLI_HEADLESS | EDITOR_PLUGIN | RUNTIME_DEBUGGER
operation_class: READ_ONLY | IDEMPOTENT_MUTATION | APPROVAL_REQUIRED_MUTATION | NON_RETRYABLE_MUTATION | LONG_RUNNING_TASK
idempotency_key_required:
approval_required:
arguments_schema:
timeout_policy:
retry_policy:
evidence_outputs:
unsupported_states:
```

An empty template is valid only as `NOT_CONFIGURED`; it cannot imply that a bridge, command, test runner, screenshot path, or export target exists.

## Operation envelope

Every invocation and result use a stable envelope. AI workers branch on `code`, not mutable message wording.

```yaml
schema_version:
operation_id:
project_fingerprint:
capability_id:
operation_class:
request_hash:
approval:
  state: NOT_REQUIRED | REQUIRED | APPROVED | REJECTED | EXPIRED
  token_binding:
task:
  task_id:
  state: NOT_APPLICABLE | QUEUED | RUNNING | PENDING | COMPLETED | FAILED | CANCELLED | STALE
result:
  success:
  code:
  message:
  data:
  evidence:
```

Stable codes include at minimum:

- `PROJECT_IDENTITY_MISMATCH`
- `CAPABILITY_NOT_DECLARED`
- `CATALOG_STALE`
- `ADAPTER_VERSION_MISMATCH`
- `APPROVAL_REQUIRED`
- `APPROVAL_TOKEN_MISMATCH`
- `UNSAFE_RETRY_BLOCKED`
- `TASK_PENDING`
- `TASK_RESULT_STALE`
- `ENGINE_STATE_UNSUPPORTED`
- `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`
- `PHYSICAL_INPUT_EVIDENCE_BLOCKED`

## Bootstrap and identity

Before engine work, the adapter follows:

```text
doctor
→ status
→ catalog --compact
→ exact normalized project path match
→ project.godot hash and project fingerprint match
→ adapter and contract version match
→ requested capability and operation class match
```

A port, process ID, window title, or directory-name substring is only a transient hint. Supplying multiple selectors requires all of them to resolve to the same project. Ambiguity or mismatch fails closed before any mutation.

## Approval and mutation safety

- Approval tokens bind project fingerprint, capability ID, normalized arguments, request hash, operation class, and expiration.
- Approval is single-use unless the project contract explicitly allows a bounded batch.
- An approved request resumes with the exact normalized request. Changing an argument requires a new preflight.
- Unknown timeout outcomes are never treated as safe-to-retry.
- Only read-only calls, proven idempotent calls with a matching idempotency key, or ledger-backed resume operations can retry automatically.
- Non-retryable mutations require explicit reconciliation of current state before a new operation.
- Editor mutations should use undo/redo transactions where the Godot API supports them and must report when rollback is unavailable.

## Long-running tasks and recovery

Long-running import, build, export, test, or capture work returns a durable `task_id` before the initiating request can time out.

```text
start once
→ persist operation and task identity
→ return RUNNING or PENDING
→ task status or resume reads the same durable record
→ never start a duplicate run while the original may still exist
→ bind final result to project fingerprint, capability, and operation ID
```

A stale heartbeat does not by itself prove that the Editor or task failed. Recovery checks process ownership, project identity, endpoint reachability, durable task state, and result freshness separately.

## Evidence boundaries

Validation states remain separate:

- `CONTRACT_PASS`: schemas and static contract are valid.
- `EXECUTION_PASS`: a declared command completed successfully in the named environment.
- `RUNTIME_PASS`: target Godot runtime behavior was observed.
- `ENGINE_INPUT_PASS`: Godot-level input dispatch was observed.
- `PHYSICAL_INPUT_PASS`: OS/window input was independently observed.
- `HUMAN_PASS`: a named human validation was performed.
- `NOT_RUN`, `NOT_CONFIGURED`, `BLOCKED_ENVIRONMENT`, and `HUMAN_NOT_RUN` are never promoted by file existence.

Screenshots prove rendered output only for the named viewport, frame, platform, and capture path. They do not prove physical clicking, accessibility, performance, or human comprehension.

## Documentation strategy

- Keep the reusable contract and safety rationale in `docs/knowledge/godot/`.
- Keep schemas in `schemas/`.
- Keep the project manifest, adapter Skill, and short AGENTS fragment under `templates/project-operations/`.
- Keep the root `START_HERE.md` route to one line and do not copy the full contract into Base entrypoints.
- Tool-specific project files should point to the project adapter or root AGENTS rules instead of duplicating the full body.

## Testing strategy

The first RED commit modifies the already-required `tests/test_game_project_operating_system_structure.py` so GitHub Actions actually executes the new expectations. Tests require:

- contract, security guide, schemas, template manifest, adapter Skill, and AGENTS fragment;
- JSON Schema Draft 2020-12 validation of the template and representative operation envelopes;
- bootstrap, identity, approval, retry, task-resume, and evidence-boundary terms;
- explicit routing to existing owners and explicit non-registration as a new broad Base Skill;
- absence of Unity-only APIs and unsafe default arbitrary-script claims;
- unchanged released Registry SHA-256 and release locks through existing Base tests.

Focused standalone tests may be added only if they are connected to an existing required workflow or required regression module. Test files that CI never executes are not accepted as evidence.

## Acceptance criteria

- The project template supplies a valid `NOT_CONFIGURED` manifest and compact adapter Skill.
- Capability and operation schemas reject port-only identity, missing action class, unsafe retry declarations, incomplete approval binding, and unbound task results.
- Existing Base owners are linked without adding a broad active Skill or changing Registry bytes.
- Entry points remain compact and route to one canonical contract.
- The RED failure and GREEN success are observed on exact PR heads in GitHub Actions.
- Base v9.4.3 release locks and Registry SHA-256 remain unchanged.
- Godot runtime and human evidence remain `NOT_RUN` until a real project pilot.

## Rollout

1. Land the contract, schemas, templates, routing, and regression tests in Base as a Draft PR.
2. Pilot the template in one Godot project with a minimal read-only/headless capability set.
3. Add EditorPlugin mutations only after identity, approval, ledger, and rollback tests pass in that project.
4. Compare at least two project pilots before considering a new shared active Skill or common executable adapter.

## Rollback

Revert the specification, implementation plan, Godot knowledge documents, schemas, project template files, compact routing changes, and focused operating regression together. No Registry, release-lock, project data, or Google Sheet migration is required because those surfaces remain protected and unchanged.
