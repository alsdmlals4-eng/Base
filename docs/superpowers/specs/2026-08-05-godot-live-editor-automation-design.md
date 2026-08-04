# Godot Live Editor Automation Design

## Status

- Original direction approved by the user on 2026-08-05.
- Initial implementation is tracked by PR #152.
- Independent adversarial review exposed four contract defects.
- The hardening amendment is implemented in stacked PR #153 using a test-first RED/GREEN cycle.
- Real Godot CLI, EditorPlugin, runtime, physical-input, and human validation remain outside this Base contract change.

## Problem

Base already owns project intake, operating-system installation and audit, runtime diagnosis, change validation, UI review, long-running task continuity, canonical-reference freshness, and Skill evolution. What is missing is a compact project-level contract for AI workers that must inspect or mutate a live Godot project safely.

Without that contract, each project can invent incompatible commands, identify an Editor by a transient port, retry unknown mutations after a timeout, overclaim test or input evidence, or copy a long engine-specific guide into multiple rule files. A broad new Base Skill would duplicate current owners and increase routing ambiguity.

The first implementation also revealed four deeper defects:

1. `LONG_RUNNING_TASK` was mixed into the same enum as side-effect and approval risk.
2. JSON Schema checked approval/task binding shape but could not prove cross-field equality.
3. Duplicate capability IDs and invalid project-test runner references could pass structural validation.
4. Evidence `kind` and `state` could be combined in misleading ways.

## Decision

Adopt a three-layer pattern:

1. Base keeps existing active Skill ownership unchanged.
2. Base publishes a reusable Godot live-editor contract, strict schemas, a semantic validator, and project template adapter.
3. Each Godot project installs only the adapter and capabilities it actually implements.

The design borrows execution-safety patterns from Hera—bootstrap discovery, compact capabilities, stable error codes, approval binding, operation ledgers, resumable tasks, and evidence-backed verification—but does not copy Unity APIs, C# handlers, UPM packaging, or Hera command syntax.

## Goals

- Provide one compact, project-installable Godot automation contract.
- Separate deterministic headless CLI work, EditorPlugin mutations, and runtime debugger observations.
- Identify the target by normalized project path and `project.godot` fingerprint, never by port alone.
- Require typed registered actions instead of arbitrary remote script execution by default.
- Separate operation side-effect risk from long-running execution lifetime.
- Make approval, timeout, retry, pending, resume, cancellation, and stale-result behavior explicit.
- Validate structural facts with JSON Schema and cross-field identity with an executable semantic validator.
- Distinguish engine-synthesized input from physical OS input and human evidence.
- Keep project test-framework evidence separate from Godot engine self-tests.
- Record exact Godot compatibility and external-tool adoption/removal boundaries.
- Preserve Base v9.4.3 Registry identity, release locks, and existing active Skill boundaries.

## Non-goals

- Do not implement a universal Godot MCP server or production EditorPlugin in Base.
- Do not add a new broad active Base Skill.
- Do not permit arbitrary GDScript or shell execution as a default project capability.
- Do not claim Godot runtime, cross-platform, human-usability, physical-input, or project-test validation from contract files alone.
- Do not modify a game project, Google Sheet, released lock, Registry entry, or frozen release derivative.
- Do not copy Hera source code or Unity-specific commands.

## Architecture

### 1. Deterministic CLI and headless path

Use the Godot executable directly for operations that can be reproduced outside the Editor:

```text
doctor
→ resolve executable and detected version
→ resolve normalized project path and project.godot fingerprint
→ verify declared support range and tool-adoption boundary
→ import or headless command
→ run selected scene or registered project tool
→ build/export/test only when declared
→ capture exit code and bounded logs
```

A project capability names its concrete command, supported engine range, required files, side effects, execution lifetime, timeout behavior, and evidence outputs. The contract never assumes that a generic Godot command is the project's test runner; a project test capability must be declared explicitly.

### 2. Optional EditorPlugin adapter path

Live Scene, Resource, Inspector, or ProjectSettings mutations use a project-owned EditorPlugin adapter:

```text
typed action request
→ project identity and catalog freshness
→ JSON Schema validation
→ semantic validation
→ effect_class and execution_mode selection
→ approval and retry gate
→ serialized main-thread execution
→ EditorUndoRedoManager transaction where supported
→ save/import/refresh boundary
→ compact result envelope
```

The adapter exposes only registered typed actions. A transport can be local HTTP, named pipe, stdio bridge, or another project-approved loopback mechanism; transport choice is project-local and cannot weaken the common identity, approval, retry, or evidence contract.

### 3. Runtime and debugger path

Runtime observation can use an EditorDebuggerPlugin, EditorDebuggerSession, EngineDebugger messages, a project debug API, or bounded logs. Runtime messages remain observational unless the capability explicitly declares a mutation `effect_class` and satisfies its approval boundary.

```text
running game
↔ project runtime debug bridge
↔ Godot Editor debugger session
↔ project adapter
↔ AI worker
```

### 4. Structural and semantic validation

```text
JSON Schema
→ required fields, types, enums, conditional shapes

semantic validator
→ duplicate capability IDs
→ project-test runner resolution
→ approval token equality
→ terminal task/result equality
```

The canonical semantic validator is `tools/validate_godot_live_editor_contract.py`. A project resolves it through the validated Base adapter pin; it does not copy a stale private version.

## Ownership and routing

| Concern | Existing owner | Godot adapter responsibility |
|---|---|---|
| Installation, capability inventory, legacy reconciliation | `managing-game-project-operating-system` | install and verify project-local adapter files and manifest |
| Runtime reproduction and isolation | `diagnosing-game-engine-runtime-failures` | supply compact status, logs, Scene/Node/signal evidence, and exact reproduction action |
| Static/runtime/regression evidence | `reviewing-and-validating-project-changes` | execute only declared validation capabilities and report truthful states |
| UI and interaction evidence | `auditing-and-refining-ui-art` | label engine input, physical input, screenshot, viewport, and human evidence separately |
| Pending and resumable execution | `maintaining-long-running-task-continuity` | persist `operation_id`, `task_id`, state, result identity, and resume boundary |
| Manifest, schema, adapter, validator, and documentation drift | `auditing-canonical-reference-freshness` | fail closed on stale catalog or contract mismatch |
| Future Skill extraction | `evolving-project-discipline-skills` | promote only after repeated project evidence proves an independent boundary |

The project-local `godot-live-editor-operations` adapter is not added to the Base active Skill Registry. It routes engine operations to existing Base owners and is installed only in projects that actually expose compatible capabilities.

## Capability manifest

`GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` is the machine-readable source for adapter capabilities.

Required top-level facts:

```yaml
schema_version:
artifact_role:
configuration_state:
contract_version:
adapter_version:
project_identity:
  normalized_project_path:
  project_godot_sha256:
  project_fingerprint:
engine_compatibility:
  detected_version:
  minimum_version:
  maximum_exclusive_version:
tool_adoption:
  source_type:
  source_reference:
  version_pin:
  telemetry_policy:
  external_data_policy:
  uninstall_reference:
  rollback_reference:
transport:
catalog:
project_test_framework:
capabilities:
validation:
```

A `NOT_CONFIGURED` template contains null or disabled values, no capability, no endpoint, and no runtime claim. A `CONFIGURED` manifest requires exact project identity, detected/supported engine versions, enabled loopback transport, fresh catalog, at least one capability, and complete tool-adoption/removal facts.

## Orthogonal capability model

Each capability declares:

```yaml
capability_id:
description:
execution_path: CLI_HEADLESS | EDITOR_PLUGIN | RUNTIME_DEBUGGER
effect_class: READ_ONLY | IDEMPOTENT_MUTATION | APPROVAL_REQUIRED_MUTATION | NON_RETRYABLE_MUTATION
execution_mode: SYNCHRONOUS | LONG_RUNNING_TASK
idempotency_key_required:
approval_required:
arguments_schema:
timeout_policy:
retry_policy:
evidence_outputs:
unsupported_states:
```

`effect_class` determines side effects, approval, idempotency, and retry risk. `execution_mode` determines whether a durable task is required. They are intentionally independent:

- `READ_ONLY + LONG_RUNNING_TASK`: a long project test or capture.
- `APPROVAL_REQUIRED_MUTATION + LONG_RUNNING_TASK`: an export or bounded generation operation.
- `NON_RETRYABLE_MUTATION + LONG_RUNNING_TASK`: an irreversible package or publication operation.

Long-running execution never removes an approval or no-retry requirement.

## Project-test runner integrity

When `project_test_framework.state` is `CONFIGURED`:

- `runner_capability_id` exists exactly once in the capability catalog.
- The runner uses `CLI_HEADLESS` or `EDITOR_PLUGIN`.
- The runner declares `TEST_RESULT` evidence.

Violations fail closed with stable semantic codes:

- `PROJECT_TEST_RUNNER_NOT_DECLARED`
- `PROJECT_TEST_RUNNER_EVIDENCE_INVALID`
- `PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID`

## Operation envelope

Every invocation and result use a stable envelope. AI workers branch on `code`, not mutable message wording.

```yaml
schema_version:
operation_id:
project_fingerprint:
capability_id:
effect_class:
execution_mode:
request_hash:
approval:
  state: NOT_REQUIRED | REQUIRED | APPROVED | REJECTED | EXPIRED
  token_binding:
task:
  task_id:
  state: NOT_APPLICABLE | QUEUED | RUNNING | PENDING | COMPLETED | FAILED | CANCELLED | STALE
  result_binding:
result:
  success:
  code:
  message:
  data:
  result_hash:
  evidence:
```

The semantic validator enforces:

- Approval token project, capability, request hash, and `effect_class` equal top-level request values.
- Terminal task project, capability, operation, and task identity equal the envelope.
- Terminal task binding hash equals `result.result_hash`.

Stable codes include at minimum:

- `PROJECT_IDENTITY_MISMATCH`
- `CAPABILITY_NOT_DECLARED`
- `DUPLICATE_CAPABILITY_ID`
- `CATALOG_STALE`
- `ADAPTER_VERSION_MISMATCH`
- `APPROVAL_REQUIRED`
- `APPROVAL_TOKEN_MISMATCH`
- `UNSAFE_RETRY_BLOCKED`
- `TASK_PENDING`
- `TASK_RESULT_STALE`
- `TASK_RESULT_HASH_MISMATCH`
- `ENGINE_STATE_UNSUPPORTED`
- `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`
- `PROJECT_TEST_RUNNER_NOT_DECLARED`
- `PROJECT_TEST_RUNNER_EVIDENCE_INVALID`
- `PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID`
- `PHYSICAL_INPUT_EVIDENCE_BLOCKED`

## Bootstrap and identity

Before engine work, the adapter follows:

```text
doctor
→ status
→ catalog --compact
→ exact normalized project path match
→ project.godot hash and project fingerprint match
→ detected and supported Godot version match
→ tool source/version/data/removal boundary present
→ adapter and contract version match
→ requested capability effect_class and execution_mode match
→ schema and semantic validation pass
```

A port, process ID, window title, or directory-name substring is only a transient hint. Supplying multiple selectors requires all of them to resolve to the same project. Ambiguity or mismatch fails closed before any mutation.

## Approval and mutation safety

- Approval tokens bind project fingerprint, capability ID, normalized arguments, request hash, `effect_class`, and expiration.
- Approval is single-use unless the project contract explicitly allows a bounded batch.
- An approved request resumes with the exact normalized request. Changing an argument requires a new preflight.
- Unknown timeout outcomes are never treated as safe-to-retry.
- Only read-only calls, proven idempotent calls with a matching idempotency key, or ledger-backed resume operations can retry under their declared rules.
- `APPROVAL_REQUIRED_MUTATION` and `NON_RETRYABLE_MUTATION` never automatically retry, including when long-running.
- Editor mutations should use undo/redo transactions where the Godot API supports them and must report when rollback is unavailable.

## Long-running tasks and recovery

Long-running import, build, export, test, or capture work returns a durable `task_id` before the initiating request can time out.

```text
start once
→ persist operation and task identity
→ return RUNNING or PENDING
→ task status or resume reads the same durable record
→ never start a duplicate run while the original may still exist
→ bind final result to project, capability, operation, task, and result hash
```

A stale heartbeat does not by itself prove that the Editor or task failed. Recovery checks process ownership, project identity, endpoint reachability, durable task state, result identity, and result hash separately.

## Evidence boundaries

Evidence `kind` and `state` are domain-bound:

| Kind | Valid success/failure family |
|---|---|
| `CONTRACT` | `CONTRACT_PASS / CONTRACT_FAIL` |
| `ENGINE_STATE`, `SCREENSHOT`, `LOG`, `TEST_RESULT`, `EXPORT` | `EXECUTION_PASS / EXECUTION_FAIL` |
| `RUNTIME` | `RUNTIME_PASS / RUNTIME_FAIL` |
| `ENGINE_INPUT` | `ENGINE_INPUT_PASS / ENGINE_INPUT_FAIL` |
| `PHYSICAL_INPUT` | `PHYSICAL_INPUT_PASS / PHYSICAL_INPUT_FAIL` |
| `HUMAN` | `HUMAN_PASS / HUMAN_FAIL` |

A passing evidence record requires an artifact path. `NOT_RUN`, `NOT_CONFIGURED`, `BLOCKED_ENVIRONMENT`, and `HUMAN_NOT_RUN` remain explicit and cannot be promoted by file existence. A screenshot cannot prove physical clicking, accessibility, performance, or human comprehension.

## Documentation strategy

- Keep reusable contract and security rationale in `docs/knowledge/godot/`.
- Keep structural schemas in `schemas/`.
- Keep cross-field semantics in one canonical validator under `tools/`.
- Keep project manifest, adapter Skill, and short AGENTS fragment under `templates/project-operations/`.
- Keep root and project entrypoints compact; do not copy the full contract.
- Resolve Base contract files through the validated Base adapter pin.

## Testing strategy

The hardening TDD cycle uses `tests/test_godot_live_editor_contract.py`, which is already connected to required CI discovery modules.

Tests cover:

- valid `NOT_CONFIGURED` template and representative configured manifest;
- orthogonal `effect_class` and `execution_mode` combinations;
- port-only identity and external bind rejection;
- configured engine/tool-adoption requirements;
- unsafe retry and missing ledger rejection;
- approval/task structural requirements;
- approval/task cross-field semantic mismatches;
- duplicate capability IDs and project-test runner integrity;
- evidence kind/state pairings;
- compact routing to existing owners and non-registration as a new Base Skill;
- unchanged Registry and release locks through existing Base tests.

The exact test-only RED head must fail for the intended missing contract. The implementation exact head must pass focused and repository-level GitHub Actions before any completion claim.

## Acceptance criteria

- The project template supplies a valid inert `NOT_CONFIGURED` manifest.
- `effect_class` and `execution_mode` are separate throughout schema, documentation, adapter, tests, and reporting.
- Long-running approval/non-retryable operations preserve their risk rules.
- Semantic validator rejects mismatched approval and task bindings.
- Semantic validator rejects duplicate capability IDs and invalid project-test runner references.
- Evidence kind/state distortions are rejected structurally.
- Configured manifests include exact engine and tool-adoption/removal boundaries.
- Existing Base owners are linked without adding a broad active Skill or changing Registry bytes.
- The RED failure and GREEN success are observed on exact PR heads in GitHub Actions.
- Base v9.4.3 release locks and Registry SHA-256 remain unchanged.
- Godot runtime and human evidence remain `NOT_RUN` until a real project pilot.

## Rollout

1. Land the hardened contract, schemas, validator, templates, routing, and regression tests in Base through PR #152/#153.
2. Pilot the template in one Godot project with a minimal read-only/headless capability set.
3. Evaluate an existing Godot MCP or project adapter with exact source/version/data/removal boundaries.
4. Add EditorPlugin mutations only after identity, approval, ledger, semantic binding, and rollback tests pass in that project.
5. Compare at least two project pilots before considering a new shared active Skill or common executable adapter.

## Rollback

Revert the hardening specification/plan changes, Godot knowledge documents, schemas, semantic validator, project template files, adapter/AGENTS changes, and focused contract tests together. No Registry, release-lock, project data, or Google Sheet migration is required because those surfaces remain protected and unchanged.