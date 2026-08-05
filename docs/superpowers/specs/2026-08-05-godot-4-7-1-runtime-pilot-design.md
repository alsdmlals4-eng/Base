# Godot 4.7.1 Runtime Pilot Design

## Status

- Date: 2026-08-05
- Parent contract: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Target branch: `agent/godot-live-editor-automation`
- User-provided engine: Godot `4.7.1.stable.official.a13da4feb`
- Scope: isolated Base fixture and evidence; no user game project mutation

## Goal

Prove that the Base Godot live-editor contract can drive a real Godot 4.7.1 binary through a small, self-contained project without claiming unsupported game integration, network MCP readiness, physical-input evidence, or human usability.

## Inputs

The user supplied one Linux x86-64 Godot archive and four standalone `project.godot` files:

- `Blacksmith`
- `urban-legend`
- `새 게임 프로젝트`
- `십보강호: 전투 POC`

The referenced scenes, scripts, addons, resources, and export templates were not supplied. Therefore the original projects are compatibility samples only. They must not be edited or reported as runnable.

## Chosen approach

Create `examples/godot-live-editor-pilot/` as an isolated fixture owned by Base tests. It contains:

- a minimal Godot 4.7 project and scene;
- a headless GDScript command entrypoint;
- a bounded state file and operation ledger;
- an EditorPlugin whose only runtime proof is safe load/unload in headless editor mode;
- a configured capability manifest derived from the Base schema;
- no listening socket, arbitrary shell, arbitrary script execution, or filesystem access outside the fixture.

The fixture implements only the smallest useful capability set:

1. `doctor`
2. `status`
3. `catalog.compact`
4. `scene.inspect`
5. `state.write_marker`
6. `task.start`
7. `task.resume`

## Identity

The command entrypoint calculates identity from:

```text
normalized project path
+ project.godot SHA-256
+ deterministic project fingerprint
```

The expected fingerprint is stored in the configured manifest. A mismatch fails before mutation.

## Mutation and approval

`state.write_marker` writes only `res://artifacts/pilot_state.json`.

The request contains:

- operation ID;
- capability ID;
- normalized marker value;
- request hash;
- idempotency key;
- approval token bound to the project fingerprint, capability, request hash, and operation class.

Missing or mismatched approval fails without writing the state file. Repeating the same idempotency key returns the existing ledger result.

## Long-running task simulation

`task.start` creates one durable task ledger entry and returns `TASK_PENDING`. It does not repeat an existing operation. `task.resume` completes that same task and binds its result to project, capability, operation, and task IDs.

This proves start-once/resume mechanics without pretending to run a real export or import pipeline.

## EditorPlugin proof

The fixture plugin performs no network action. During headless editor startup it writes a bounded marker under `res://artifacts/`, then unloads cleanly. This is evidence of EditorPlugin lifecycle compatibility only, not live remote control.

## Tests and evidence

A Python integration test runs the uploaded Godot binary against the fixture and checks:

- engine version;
- project import;
- `doctor`, `status`, and compact catalog;
- scene inspection;
- approval rejection;
- approved idempotent mutation and replay;
- task start and resume;
- headless EditorPlugin load marker;
- stable JSON envelopes and bounded artifact paths.

Repository CI cannot rely on the uploaded binary. Static repository tests validate fixture structure, manifest/schema compatibility, and evidence metadata. Runtime logs are committed as an evidence summary with the binary SHA-256 and exact commands, not as a claim that all user projects ran.

## Evidence boundaries

```yaml
uploaded_engine_binary: EXECUTION_PASS
isolated_cli_headless_fixture: RUNTIME_PASS
isolated_editor_plugin_load: RUNTIME_PASS
original_project_configs_parse: EXECUTION_PASS
original_project_scenes_and_scripts: NOT_PROVIDED
original_projects_runtime: NOT_RUN
network_mcp_transport: NOT_IMPLEMENTED
runtime_debugger_bridge: NOT_IMPLEMENTED
project_test_framework: NOT_CONFIGURED
physical_input_validation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
```

## Non-goals

- Do not add the Godot executable or archive to Git.
- Do not modify any uploaded `project.godot`.
- Do not enable or reproduce `addons/godot_ai`.
- Do not create a universal EditorPlugin server in Base.
- Do not expose a remote or wildcard network endpoint.
- Do not claim the four original games run.
