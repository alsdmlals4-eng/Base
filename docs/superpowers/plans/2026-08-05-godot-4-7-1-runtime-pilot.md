# Godot 4.7.1 Runtime Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify an isolated Godot 4.7.1 fixture that exercises the Base live-editor identity, approval, idempotency, task-resume, and EditorPlugin lifecycle contracts.

**Architecture:** A self-contained example project exposes typed commands through one headless GDScript entrypoint and stores bounded state under its own `artifacts/` directory. Python tests invoke the user-supplied Godot binary locally, while repository CI validates static structure, schemas, and checked-in evidence metadata without depending on that binary.

**Tech Stack:** Godot 4.7.1 GDScript, JSON, Python 3.12 `unittest`, JSON Schema Draft 2020-12, GitHub Actions.

## Global Constraints

- Never modify the four uploaded `project.godot` files.
- Never commit the 144 MB Godot executable or archive.
- All fixture writes stay under `examples/godot-live-editor-pilot/artifacts/`.
- No network listener, arbitrary shell, arbitrary script action, or path outside the fixture.
- Runtime claims must name the exact binary SHA-256 and command.
- Original project runtime remains `NOT_RUN` because referenced files were not supplied.

---

### Task 1: Runtime fixture contract test

**Files:**
- Create: `tests/test_godot_live_editor_runtime_pilot.py`
- Create: `examples/godot-live-editor-pilot/project.godot`
- Create: `examples/godot-live-editor-pilot/main.tscn`
- Create: `examples/godot-live-editor-pilot/scripts/pilot_main.gd`
- Create: `examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`

**Interfaces:**
- Consumes: Base capability-manifest schema.
- Produces: a schema-valid configured fixture with a loadable main scene.

- [ ] Write a failing repository test that requires the fixture paths, configured manifest, loopback-disabled transport, exact capability IDs, and bounded artifact root.
- [ ] Run the focused test and confirm it fails because the fixture does not exist.
- [ ] Add the minimum project, scene, script, and configured manifest.
- [ ] Run the focused test and confirm it passes.
- [ ] Commit the fixture contract.

### Task 2: Headless command entrypoint

**Files:**
- Create: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`

**Interfaces:**
- Consumes: command name and JSON request path from Godot user arguments.
- Produces: one JSON operation envelope on stdout and bounded files under `artifacts/`.

- [ ] Add failing tests for `doctor`, `status`, `catalog.compact`, and `scene.inspect` using the uploaded Godot binary.
- [ ] Run the tests and verify the expected missing-script failure.
- [ ] Implement the four read-only commands with project identity verification.
- [ ] Run the tests and verify all read-only commands pass.
- [ ] Commit the read-only CLI.

### Task 3: Approved idempotent mutation

**Files:**
- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`

**Interfaces:**
- Consumes: operation ID, marker, request hash, idempotency key, and approval binding.
- Produces: `artifacts/pilot_state.json` and `artifacts/operation_ledger.json`.

- [ ] Add failing tests that reject missing approval, accept a matching binding, and replay the same idempotency key without duplicate mutation.
- [ ] Run the tests and verify rejection/implementation failures.
- [ ] Implement the minimum approval comparison, bounded write, and ledger replay.
- [ ] Run the focused and existing contract tests.
- [ ] Commit the mutation capability.

### Task 4: Durable task start and resume

**Files:**
- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`

**Interfaces:**
- Consumes: long-task operation ID and approval binding.
- Produces: a durable task entry that transitions `PENDING` to `COMPLETED`.

- [ ] Add failing tests for start-once, `TASK_PENDING`, same-task resume, and bound completion result.
- [ ] Run the tests and confirm missing behavior.
- [ ] Implement `task.start` and `task.resume` using the same ledger.
- [ ] Run all pilot tests.
- [ ] Commit task continuity.

### Task 5: EditorPlugin lifecycle

**Files:**
- Create: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.cfg`
- Create: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.gd`
- Modify: `examples/godot-live-editor-pilot/project.godot`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`

**Interfaces:**
- Consumes: Godot headless editor startup.
- Produces: `artifacts/editor_plugin_loaded.json`.

- [ ] Add a failing test that starts the editor headlessly and expects the bounded plugin marker.
- [ ] Run it and confirm the plugin marker is absent.
- [ ] Implement a no-network EditorPlugin that writes only the lifecycle marker.
- [ ] Run the editor lifecycle test and full pilot suite.
- [ ] Commit the plugin proof.

### Task 6: Compatibility samples and evidence

**Files:**
- Create: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md`
- Create: `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `tests/test_local_validation.py`

**Interfaces:**
- Consumes: uploaded binary/config hashes and completed runtime logs.
- Produces: exact evidence states and CI-discoverable static validation.

- [ ] Add failing tests for evidence fields, binary SHA-256, original project names, and honest `NOT_RUN` boundaries.
- [ ] Generate the evidence summary from actual commands and logs.
- [ ] Connect the focused test to existing required CI modules.
- [ ] Run local tests and exact-head GitHub Actions.
- [ ] Commit evidence and report remaining limits.
