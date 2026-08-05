# Godot Editor Transaction Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and prove a project-local, network-disabled Godot 4.7 EditorPlugin adapter that accepts only prevalidated v2 operation envelopes, revalidates exact editor state on the Editor main thread, applies a bounded `EditorUndoRedoManager` transaction, and records save/refresh/evidence outcomes without claiming production transport readiness.

**Architecture:** The canonical addon lives in the project-operations template and is materialized into an isolated v2 Editor pilot for runtime proof. `plugin.gd` is only the composition root; queueing, runtime contract checks, state observation, capability typing, undo/redo execution, atomic ledger writes, and evidence hashing are separate focused scripts. There is no socket, HTTP, WebSocket, MCP, Autoload, background thread, arbitrary property path, arbitrary script execution, or remote endpoint in this PR.

**Tech Stack:** Godot 4.7.x GDScript EditorPlugin APIs, `EditorUndoRedoManager`, `EditorInterface`, `EditorFileSystem`, Python 3.12, pytest, existing Godot live-editor v2 JSON Schemas and Python semantic validator.

## Global Constraints

- Base main baseline at plan creation: `339a48be688e312b7894e1f2372aecfe0ee3f6f4`.
- Governing proposal: `BCP-2026-005-godot-live-editor-contract-v2`, state `APPROVED_FOR_IMPLEMENTATION`.
- Governing design: `docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md`, state `APPROVED`.
- PR A static v2 contract is already merged through PR #161.
- Supported runtime target for this Pilot: exact Godot `4.7.x`; record the exact version string and executable SHA-256 when runtime evidence is generated.
- The adapter is project-local under `res://addons/base_live_editor_adapter/` after materialization.
- Transport remains `DISABLED`; no listener or protocol server is introduced.
- Only `scene.inspect` and `node.rename` are implemented in PR B. Additional mutations require a later reviewed capability.
- `node.rename` accepts only a relative `NodePath`, a validated node name, and `save_mode: KEEP_DIRTY | SAVE_CURRENT_SCENE`.
- The final stale-state observation and engine action occur in one `_process()` call on the Editor main thread.
- Every mutation writes `STARTED` atomically before `commit_action()` and then writes exactly one `COMPLETED` or `FAILED` record.
- `EditorUndoRedoManager` is obtained from `EditorPlugin.get_undo_redo()`; direct `UndoRedo` replacement is forbidden.
- Dirty state is observed through `EditorInterface.get_unsaved_scenes()` and scene revision through the edited root's `EditorUndoRedoManager` history version.
- Saving uses `EditorInterface.save_scene()` and refresh uses `EditorInterface.get_resource_filesystem().update_file(scene_path)`; no full scan or reimport is called for a `.tscn` save.
- Static evidence hash validation from PR A remains distinct from actual artifact-byte SHA-256 verification performed by `evidence_writer.gd`.
- Existing v1 Schemas and `examples/godot-live-editor-pilot/` evidence remain byte-identical.
- `skills/SKILL_REGISTRY.json`, release locks, frozen derivatives, workflow topology, user projects, binaries, archives, UID files, and Google Sheets are excluded.
- Runtime, physical-input, and human evidence remain `NOT_RUN` if no exact Godot executable is available.
- `PRODUCTION_ADAPTER_READY` remains `NOT_READY` after this PR because authenticated transport, runtime debugger, two real-project pilots, Windows production operation, physical input, and human usability are separate gates.

---

## File Responsibility Map

### Canonical project template addon

- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/plugin.cfg`: Godot addon metadata only.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/plugin.gd`: composition root, manifest loading, editor-instance identity, in-process submission, one-request-per-frame processing, cleanup.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/request_queue.gd`: bounded FIFO and duplicate-operation rejection; no Godot object mutation.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/runtime_contract_guard.gd`: exact manifest/envelope/instance/snapshot/policy/approval checks before enqueue and immediately before execution.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_state_probe.gd`: current scene path, dirty state, disk SHA-256, undo-history revision, target-node confinement.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/capability_registry.gd`: closed capability allowlist and typed argument/output validation for `scene.inspect` and `node.rename`.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/operation_ledger.gd`: atomic STARTED/terminal JSON records and exact idempotent replay lookup.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/evidence_writer.gd`: confined JSON evidence writes and physical file-byte SHA-256 calculation.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_transaction_executor.gd`: main-thread state recheck, ledger ordering, `EditorUndoRedoManager` action, save/update, output/evidence validation.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md`: installation, no-network boundary, supported capabilities, recovery and removal.

### Isolated runtime Pilot

- `examples/godot-live-editor-v2-editor-pilot/project.godot`
- `examples/godot-live-editor-v2-editor-pilot/main.tscn`
- `examples/godot-live-editor-v2-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- `examples/godot-live-editor-v2-editor-pilot/addons/base_live_editor_adapter_pilot/plugin.cfg`
- `examples/godot-live-editor-v2-editor-pilot/addons/base_live_editor_adapter_pilot/plugin.gd`
- `examples/godot-live-editor-v2-editor-pilot/.gitignore`
- `tools/materialize_godot_editor_adapter_pilot.py`

### Tests and docs

- `tests/test_godot_editor_transaction_adapter.py`
- `tests/test_godot_editor_transaction_adapter_runtime.py`
- `tests/test_local_validation.py`
- `tests/test_v9_machine_contracts.py`
- `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-editor-transaction-pilot.md` only after actual runtime execution.

---

### Task 1: Add the PR B RED contract gate

**Files:**
- Create: `tests/test_godot_editor_transaction_adapter.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: merged PR A files under `schemas/`, `tools/`, and the approved design/readiness documents.
- Produces: required CI failures until every canonical addon file and safety marker exists.

- [ ] **Step 1: Write the missing-artifact RED test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"

REQUIRED = {
    "plugin.cfg",
    "plugin.gd",
    "request_queue.gd",
    "runtime_contract_guard.gd",
    "editor_state_probe.gd",
    "capability_registry.gd",
    "operation_ledger.gd",
    "evidence_writer.gd",
    "editor_transaction_executor.gd",
    "README.md",
}


def test_editor_transaction_adapter_files_exist() -> None:
    assert ADDON.is_dir()
    assert REQUIRED == {path.name for path in ADDON.iterdir() if path.is_file()}
```

- [ ] **Step 2: Add required and forbidden source markers**

```python
def test_adapter_has_required_editor_transaction_markers() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in ADDON.glob("*.gd"))
    for required in (
        "EditorPlugin",
        "get_undo_redo()",
        "EditorInterface.get_unsaved_scenes()",
        "EditorInterface.save_scene()",
        "get_resource_filesystem().update_file",
        "TARGET_STATE_CONFLICT",
        "STARTED",
        "COMPLETED",
        "FAILED",
        "MAX_PENDING",
    ):
        assert required in source

    for forbidden in (
        "TCPServer",
        "WebSocketPeer",
        "HTTPServer",
        "PacketPeerUDP",
        "Thread.new",
        "OS.execute",
        "GDScript.new",
        "Expression.new",
    ):
        assert forbidden not in source
```

- [ ] **Step 3: Wire the test into both required suites**

Follow the import/aggregation pattern already used for `test_godot_live_editor_contract_v2` in `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`.

- [ ] **Step 4: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
```

Expected: only the new PR B artifact/marker checks fail; existing PR A and Base tests remain green.

- [ ] **Step 5: Commit the test-only RED**

```bash
git add tests/test_godot_editor_transaction_adapter.py tests/test_local_validation.py tests/test_v9_machine_contracts.py
git commit -m "test: require Godot editor transaction adapter"
```

---

### Task 2: Implement the bounded queue and runtime guard

**Files:**
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/request_queue.gd`
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/runtime_contract_guard.gd`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `enqueue(envelope: Dictionary) -> Dictionary`
- `pop_next() -> Dictionary`
- `size() -> int`
- `clear() -> void`
- `configure(manifest: Dictionary, project_fingerprint: String, editor_instance_id: String) -> void`
- `validate_for_enqueue(envelope: Dictionary) -> PackedStringArray`
- `validate_before_execute(envelope: Dictionary, observation: Dictionary) -> PackedStringArray`

- [ ] **Step 1: Add queue and guard tests**

```python
def test_queue_is_bounded_and_rejects_duplicates() -> None:
    source = (ADDON / "request_queue.gd").read_text(encoding="utf-8")
    assert "const MAX_PENDING := 64" in source
    assert "QUEUE_FULL" in source
    assert "DUPLICATE_OPERATION_ID" in source


def test_guard_rechecks_exact_v2_bindings() -> None:
    source = (ADDON / "runtime_contract_guard.gd").read_text(encoding="utf-8")
    for marker in (
        "schema_version",
        "project_fingerprint",
        "automation_service_instance_id",
        "editor_instance_id",
        "contract_snapshot",
        "capability_id",
        "approval",
        "request_hash",
        "TARGET_STATE_CONFLICT",
    ):
        assert marker in source
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 3: Implement `request_queue.gd`**

```gdscript
@tool
extends RefCounted

const MAX_PENDING := 64

var _items: Array[Dictionary] = []
var _operation_ids: Dictionary = {}

func enqueue(envelope: Dictionary) -> Dictionary:
    var operation_id := str(envelope.get("operation_id", ""))
    if operation_id.is_empty():
        return {"ok": false, "code": "OPERATION_ID_REQUIRED"}
    if _operation_ids.has(operation_id):
        return {"ok": false, "code": "DUPLICATE_OPERATION_ID"}
    if _items.size() >= MAX_PENDING:
        return {"ok": false, "code": "QUEUE_FULL"}
    _items.push_back(envelope.duplicate(true))
    _operation_ids[operation_id] = true
    return {"ok": true, "code": "QUEUED"}

func pop_next() -> Dictionary:
    if _items.is_empty():
        return {}
    var envelope: Dictionary = _items.pop_front()
    _operation_ids.erase(str(envelope.get("operation_id", "")))
    return envelope

func size() -> int:
    return _items.size()

func clear() -> void:
    _items.clear()
    _operation_ids.clear()
```

- [ ] **Step 4: Implement fail-closed `runtime_contract_guard.gd`**

The enqueue guard rejects non-v2 roots, mismatched project/editor identity, unknown capabilities, unsupported execution modes, unresolved approval, and contract snapshot mismatches. The execute guard reruns enqueue checks and compares each expected precondition with the fresh observation.

```gdscript
func validate_before_execute(envelope: Dictionary, observation: Dictionary) -> PackedStringArray:
    var errors := validate_for_enqueue(envelope)
    var preconditions: Dictionary = envelope.get("preconditions", {})
    var pairs := [
        ["expected_target_revision", observation.get("target_revision")],
        ["expected_target_content_sha256", observation.get("target_content_sha256")],
        ["expected_dirty_state", observation.get("dirty_state")],
        ["expected_scene_path", observation.get("scene_path")],
    ]
    for pair in pairs:
        if preconditions.get(pair[0]) != pair[1]:
            errors.append("TARGET_STATE_CONFLICT")
            break
    return errors
```

- [ ] **Step 5: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
git add templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/request_queue.gd templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/runtime_contract_guard.gd tests/test_godot_editor_transaction_adapter.py
git commit -m "feat: add bounded Godot editor request gate"
```

---

### Task 3: Add exact Editor state observation and typed capabilities

**Files:**
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_state_probe.gd`
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/capability_registry.gd`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `observe(editor_interface: EditorInterface, undo_redo: EditorUndoRedoManager, target_path: NodePath) -> Dictionary`
- Observation keys: `scene_path`, `dirty_state`, `target_content_sha256`, `target_revision`, `target_node`.
- `validate_arguments(capability_id: String, arguments: Dictionary) -> PackedStringArray`
- `validate_output(capability_id: String, output: Dictionary) -> PackedStringArray`
- `inspect_scene(editor_interface: EditorInterface, observation: Dictionary) -> Dictionary`
- `resolve_rename_target(scene_root: Node, arguments: Dictionary) -> Dictionary`

- [ ] **Step 1: Add state and confinement tests**

```python
def test_state_probe_uses_editor_owned_state() -> None:
    source = (ADDON / "editor_state_probe.gd").read_text(encoding="utf-8")
    for marker in (
        "EditorInterface.get_unsaved_scenes()",
        "get_object_history_id",
        "get_history_undo_redo",
        "get_version()",
        "HashingContext.HASH_SHA256",
        "ProjectSettings.globalize_path",
    ):
        assert marker in source


def test_registry_allows_only_inspect_and_rename() -> None:
    source = (ADDON / "capability_registry.gd").read_text(encoding="utf-8")
    assert '"scene.inspect"' in source
    assert '"node.rename"' in source
    assert "UNKNOWN_CAPABILITY" in source
    assert "ABSOLUTE_NODE_PATH_FORBIDDEN" in source
    assert "NODE_OUTSIDE_EDITED_SCENE" in source
    assert "INVALID_NODE_NAME" in source
    assert "set_indexed" not in source
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 3: Implement scene observation**

Use the active edited scene root only. Disk content hash is `null` for a new unsaved scene. Dirty state comes from `EditorInterface.get_unsaved_scenes()`. Revision is `<history_id>:<undo_version>`.

```gdscript
func observe(editor_interface: EditorInterface, undo_redo: EditorUndoRedoManager, target_path: NodePath) -> Dictionary:
    var root := editor_interface.get_edited_scene_root()
    if root == null:
        return {"error": "EDITED_SCENE_REQUIRED"}
    var scene_path := str(root.scene_file_path)
    var target := root.get_node_or_null(target_path)
    if target == null or not (target == root or root.is_ancestor_of(target)):
        return {"error": "TARGET_NODE_NOT_FOUND"}
    var history_id := undo_redo.get_object_history_id(root)
    var history := undo_redo.get_history_undo_redo(history_id)
    return {
        "scene_path": scene_path,
        "dirty_state": "DIRTY" if EditorInterface.get_unsaved_scenes().has(scene_path) else "CLEAN",
        "target_content_sha256": _sha256_file(scene_path),
        "target_revision": "%s:%s" % [history_id, history.get_version()],
        "target_node": target,
    }
```

- [ ] **Step 4: Implement closed capability validation**

`scene.inspect` accepts `{}` only. `node.rename` requires exactly `node_path`, `new_name`, and `save_mode`. Reject absolute paths, `..`, empty names, names longer than 128 characters, and names containing `. : @ / " %`. Resolve the target only under the active scene root.

- [ ] **Step 5: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
git add templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_state_probe.gd templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/capability_registry.gd tests/test_godot_editor_transaction_adapter.py
git commit -m "feat: observe Godot editor state and type capabilities"
```

---

### Task 4: Add atomic ledger and physical evidence hashing

**Files:**
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/operation_ledger.gd`
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/evidence_writer.gd`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `configure(root_path: String) -> void`
- `record_started(envelope: Dictionary, observation: Dictionary) -> Dictionary`
- `record_terminal(operation_id: String, state: String, result: Dictionary) -> Dictionary`
- `read_record(operation_id: String) -> Dictionary`
- `write_json(name: String, payload: Dictionary) -> Dictionary`
- `sha256_file(res_path: String) -> Variant`

- [ ] **Step 1: Add atomicity tests**

```python
def test_ledger_and_evidence_are_atomic_and_confined() -> None:
    ledger = (ADDON / "operation_ledger.gd").read_text(encoding="utf-8")
    evidence = (ADDON / "evidence_writer.gd").read_text(encoding="utf-8")
    for source in (ledger, evidence):
        assert "ProjectSettings.globalize_path" in source
        assert ".tmp" in source
        assert "rename_absolute" in source
    assert "HashingContext.HASH_SHA256" in evidence
    assert "LEDGER_STATE_INVALID" in ledger
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 3: Implement confined atomic JSON writes**

Write to `<target>.tmp`, flush/close, remove a stale destination, then `DirAccess.rename_absolute(temp, target)`. Reject names containing `/`, `\\`, or `..`. Never write outside `res://artifacts/godot-live-editor/`.

- [ ] **Step 4: Enforce ledger transitions**

`record_started()` rejects an existing different request hash and returns exact replay metadata for an existing `COMPLETED` record with the same request hash. `record_terminal()` rejects missing STARTED state and accepts only `COMPLETED` or `FAILED`.

- [ ] **Step 5: Hash physical bytes**

```gdscript
func sha256_file(res_path: String) -> Variant:
    if res_path.is_empty() or not res_path.begins_with("res://"):
        return null
    var file := FileAccess.open(res_path, FileAccess.READ)
    if file == null:
        return null
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    while file.get_position() < file.get_length():
        context.update(file.get_buffer(min(65536, file.get_length() - file.get_position())))
    return context.finish().hex_encode()
```

- [ ] **Step 6: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
git add templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/operation_ledger.gd templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/evidence_writer.gd tests/test_godot_editor_transaction_adapter.py
git commit -m "feat: add atomic Godot operation evidence"
```

---

### Task 5: Implement the main-thread transaction executor

**Files:**
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_transaction_executor.gd`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `configure(editor_interface, undo_redo, guard, registry, probe, ledger, evidence) -> void`
- `execute(envelope: Dictionary) -> Dictionary`
- Result keys: `success`, `code`, `message`, `data`, `evidence`.

- [ ] **Step 1: Add ordering tests**

```python
def test_executor_orders_precondition_ledger_undo_save_and_terminal_state() -> None:
    source = (ADDON / "editor_transaction_executor.gd").read_text(encoding="utf-8")
    markers = [
        "validate_before_execute",
        "record_started",
        "create_action",
        "add_do_property",
        "add_undo_property",
        "commit_action",
        "mark_scene_as_unsaved",
        "save_scene",
        "update_file",
        "sha256_file",
        "record_terminal",
    ]
    positions = [source.index(marker) for marker in markers]
    assert positions == sorted(positions)
```

- [ ] **Step 2: Add fail-closed code tests**

```python
def test_executor_has_stable_failure_codes() -> None:
    source = (ADDON / "editor_transaction_executor.gd").read_text(encoding="utf-8")
    for code in (
        "TARGET_STATE_CONFLICT",
        "LEDGER_START_FAILED",
        "UNDO_REDO_BUSY",
        "SAVE_FAILED",
        "OUTPUT_SCHEMA_INVALID",
        "EVIDENCE_WRITE_FAILED",
    ):
        assert code in source
```

- [ ] **Step 3: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 4: Implement read-only `scene.inspect`**

Observe the active scene, return only `scene_path`, `root_name`, `child_count`, `dirty_state`, `target_revision`, and `target_content_sha256`, validate the output through the registry, and write bounded evidence. Do not create a mutation ledger record.

- [ ] **Step 5: Implement `node.rename` as one action**

```gdscript
func _rename_node(envelope: Dictionary, observation: Dictionary) -> Dictionary:
    if _undo_redo.is_committing_action():
        return _failure("UNDO_REDO_BUSY")
    var arguments: Dictionary = envelope["request"]["arguments"]
    var target: Node = observation["target_node"]
    var old_name := target.name
    var new_name := StringName(arguments["new_name"])

    _undo_redo.create_action("Base Live Editor: Rename Node", UndoRedo.MERGE_DISABLE, target)
    _undo_redo.add_do_property(target, &"name", new_name)
    _undo_redo.add_undo_property(target, &"name", old_name)
    _undo_redo.commit_action()
    EditorInterface.mark_scene_as_unsaved()
```

The full method must run final observation/guard, STARTED ledger, commit, postcondition check, optional save/update/hash, closed output validation, evidence write, and terminal ledger in that order.

- [ ] **Step 6: Keep save policies distinct**

- `KEEP_DIRTY`: active scene appears in `get_unsaved_scenes()` after commit; no saved-file hash change is claimed.
- `SAVE_CURRENT_SCENE`: `save_scene()` returns `OK`, `update_file(scene_path)` runs, and physical bytes are hashed.
- A scene path changed since preflight returns `TARGET_STATE_CONFLICT`.

- [ ] **Step 7: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
git add templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/editor_transaction_executor.gd tests/test_godot_editor_transaction_adapter.py
git commit -m "feat: execute Godot editor undo transactions"
```

---

### Task 6: Compose the network-disabled EditorPlugin template

**Files:**
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/plugin.cfg`
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/plugin.gd`
- Create: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Modify: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `submit_validated_operation(envelope: Dictionary) -> Dictionary`
- `take_completed_result(operation_id: String) -> Dictionary`

- [ ] **Step 1: Add plugin composition tests**

```python
def test_plugin_is_composition_only_and_network_disabled() -> None:
    source = (ADDON / "plugin.gd").read_text(encoding="utf-8")
    assert "extends EditorPlugin" in source
    assert "func submit_validated_operation(envelope: Dictionary) -> Dictionary:" in source
    assert "func _process(_delta: float) -> void:" in source
    assert "execute(envelope)" in source
    assert "_queue.clear()" in source
    assert "network_listener_enabled" in source
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 3: Implement lifecycle**

`_enter_tree()` loads `res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`, requires schema version 2 and `transport.kind == "DISABLED"`, generates a new editor instance ID, configures modules, and enables processing. `submit_validated_operation()` guards then queues a deep copy. `_process()` pops at most one request. `_exit_tree()` disables processing, clears queue/results, and releases references.

- [ ] **Step 4: Fail closed when unconfigured**

Missing, malformed, v1, `NOT_CONFIGURED`, or transport-enabled manifest leaves the plugin loaded but unavailable with `ADAPTER_NOT_CONFIGURED`; it must not invent identity or capabilities.

- [ ] **Step 5: Document installation/removal**

The README, adapter Skill, and AGENTS fragment must instruct operators to copy the canonical addon, configure/validate v2, enable the plugin, submit only already validated in-process envelopes, and use `--recovery-mode` to disable/remove a broken adapter. They must state that no MCP/server/transport is included and readiness remains false.

- [ ] **Step 6: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py tests/test_godot_live_editor_contract_v2_docs.py -q
git add templates/project-operations/godot-live-editor templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md tests/test_godot_editor_transaction_adapter.py
git commit -m "feat: add project-local Godot editor adapter template"
```

---

### Task 7: Build the isolated v2 Editor runtime Pilot

**Files:**
- Create: `examples/godot-live-editor-v2-editor-pilot/project.godot`
- Create: `examples/godot-live-editor-v2-editor-pilot/main.tscn`
- Create: `examples/godot-live-editor-v2-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Create: `examples/godot-live-editor-v2-editor-pilot/addons/base_live_editor_adapter_pilot/plugin.cfg`
- Create: `examples/godot-live-editor-v2-editor-pilot/addons/base_live_editor_adapter_pilot/plugin.gd`
- Create: `examples/godot-live-editor-v2-editor-pilot/.gitignore`
- Create: `tools/materialize_godot_editor_adapter_pilot.py`
- Create: `tests/test_godot_editor_transaction_adapter_runtime.py`
- Test: `tests/test_godot_editor_transaction_adapter.py`

**Interfaces:**
- `materialize(source_root: Path, destination: Path) -> Path`
- Runtime result: `artifacts/godot-live-editor/editor_transaction_pilot_result.json`.
- Result fields: `status`, `engine_version`, `editor_instance_id`, `inspect_pass`, `rename_keep_dirty_pass`, `undo_pass`, `rename_save_pass`, `saved_scene_sha256`, `ledger_states`, `network_listener_enabled`.

- [ ] **Step 1: Add materialization test**

```python
def test_pilot_materializer_copies_canonical_addon(tmp_path: Path) -> None:
    from tools.materialize_godot_editor_adapter_pilot import materialize

    project = materialize(ROOT, tmp_path / "pilot")
    copied = project / "addons/base_live_editor_adapter"
    assert (copied / "plugin.gd").read_bytes() == (ADDON / "plugin.gd").read_bytes()
    assert not list(project.rglob("*.uid"))
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 3: Implement materializer**

Copy the immutable fixture and canonical addon to a temporary directory. Recompute temporary `project.godot` hash and manifest project fingerprint; run `tools.validate_godot_live_editor_contract_v2.validate_contract_pair()` before returning. Never edit checked-in fixture files.

- [ ] **Step 4: Implement Pilot wrapper**

The wrapper extends `res://addons/base_live_editor_adapter/plugin.gd`, calls `super._enter_tree()`, opens `res://main.tscn`, and uses deferred calls to:

1. submit `scene.inspect`;
2. submit `node.rename` with `KEEP_DIRTY` using fresh observations;
3. call the exact scene history `undo()` and confirm `Target` is restored;
4. submit `node.rename` with `SAVE_CURRENT_SCENE`;
5. verify saved bytes and STARTED/COMPLETED ledger states;
6. write the Pilot result and quit the editor.

No test hook is added to the canonical addon.

- [ ] **Step 5: Implement explicit runtime skip**

```python
GODOT_BIN = os.environ.get("GODOT_BIN")
pytestmark = pytest.mark.skipif(
    not GODOT_BIN,
    reason="SKIPPED_NOT_CONFIGURED: set GODOT_BIN to exact Godot 4.7.x executable",
)
```

- [ ] **Step 6: Run static materializer tests**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
```

- [ ] **Step 7: Run actual Editor runtime when available**

```bash
GODOT_BIN=/absolute/path/to/godot python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -v
```

The test first checks `godot --version` for `4.7.`, hashes the executable, then runs:

```text
<godot> --editor --headless --path <materialized-project> --quit-after 600
```

Expected: exit 0, Pilot `status == "PASS"`, all behavior booleans true, listener false, and saved bytes equal the reported SHA-256.

- [ ] **Step 8: Commit Pilot**

```bash
git add examples/godot-live-editor-v2-editor-pilot tools/materialize_godot_editor_adapter_pilot.py tests/test_godot_editor_transaction_adapter.py tests/test_godot_editor_transaction_adapter_runtime.py
git commit -m "test: prove Godot editor transaction adapter"
```

---

### Task 8: Run adversarial closure and record truthful readiness

**Files:**
- Modify: `tests/test_godot_editor_transaction_adapter.py`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Create only after runtime execution: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-editor-transaction-pilot.md`

**Interfaces:**
- Produces the final PR B gate matrix.
- Does not change PR A Schemas, Registry, release locks, v1 Pilot evidence, or workflows.

- [ ] **Step 1: Add adversarial cases**

Cover:

```text
queue overflow -> QUEUE_FULL
duplicate pending operation -> DUPLICATE_OPERATION_ID
wrong editor instance -> EDITOR_INSTANCE_MISMATCH
unknown capability -> UNKNOWN_CAPABILITY
absolute or escaping NodePath -> fail closed
changed scene path/revision/hash/dirty state -> TARGET_STATE_CONFLICT
second request during action -> processed next frame only
UndoRedo already committing -> UNDO_REDO_BUSY
ledger STARTED failure -> no engine mutation
save failure -> FAILED ledger, no success evidence
extra/missing output fields -> OUTPUT_SCHEMA_INVALID
evidence path escape -> EVIDENCE_PATH_INVALID
plugin disable -> queue/results cleared
network API scan -> none
```

- [ ] **Step 2: Recheck protected paths**

No changed path may match:

```text
skills/SKILL_REGISTRY.json
schemas/*-v1.schema.json
examples/godot-live-editor-pilot/**
releases/**
**/*.zip
**/*.exe
**/*.uid
.github/workflows/**
```

- [ ] **Step 3: Run focused and required static suites**

```bash
python -m pytest \
  tests/test_godot_editor_transaction_adapter.py \
  tests/test_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract_v2_adversarial.py \
  tests/test_godot_live_editor_contract_v2_docs.py \
  tests/test_local_validation.py \
  tests/test_v9_machine_contracts.py -q
```

Expected: all PASS.

- [ ] **Step 4: Run runtime suite or record exact skip**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -v
```

With `GODOT_BIN`, all runtime cases must pass and the evidence doc is generated from observed values. Without it, tests report `SKIPPED_NOT_CONFIGURED` and no runtime PASS document is created.

- [ ] **Step 5: Update readiness**

Without Godot:

```yaml
editor_main_thread_queue: STATIC_PASS
editor_undo_redo_transaction: STATIC_PASS
godot_4_7_editor_pilot: SKIPPED_NOT_CONFIGURED
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
real_project_pilots: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

Only after actual execution:

```yaml
editor_main_thread_queue: RUNTIME_PASS
editor_undo_redo_transaction: RUNTIME_PASS
save_import_refresh_boundary: RUNTIME_PASS
artifact_byte_hash_verification: RUNTIME_PASS
godot_4_7_editor_pilot: RUNTIME_PASS
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
real_project_pilots: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

- [ ] **Step 6: Run exact-head GitHub Actions**

Require success for `Validate Base v9 Operating Contracts`, `Validate Game Project Operating System`, `ubuntu-contract`, `docs-validation`, `publication-validation`, and `ci-gate`. Windows smoke may be `SKIPPED_NOT_REQUIRED` only when change classification explicitly excludes it. Unresolved review threads must be zero.

- [ ] **Step 7: Commit closure**

```bash
git add tests/test_godot_editor_transaction_adapter.py docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md docs/knowledge/godot/evidence
git commit -m "docs: record Godot editor adapter evidence"
```

---

## Plan Self-Review

### Spec coverage

- Main-thread bounded queue: Tasks 2, 5, 6.
- Typed Scene/Node operations: Tasks 3 and 5.
- Final expected/observed stale-state check: Tasks 2, 3, 5.
- `EditorUndoRedoManager` transaction: Task 5.
- Dirty/save/filesystem refresh evidence: Tasks 3, 5, 7.
- Atomic STARTED/terminal ledger: Tasks 4 and 5.
- Actual file-byte SHA-256: Tasks 4, 5, 7.
- Plugin load/unload cleanup: Tasks 6 and 7.
- No network listener: Tasks 1, 6, 8.
- Exact Godot runtime boundary: Tasks 7 and 8.
- Protected v1/Registry/release boundaries: Task 8.
- Production readiness remains false: Global constraints and Task 8.

### Placeholder scan

The plan contains no incomplete requirement or undefined helper. Features left for PR C/PR D are explicit exclusions rather than deferred PR B steps.

### Type and name consistency

- Queue: `enqueue`, `pop_next`, `size`, `clear`.
- Guard: `configure`, `validate_for_enqueue`, `validate_before_execute`.
- Observation: `scene_path`, `dirty_state`, `target_content_sha256`, `target_revision`, `target_node`.
- Ledger states: `STARTED`, `COMPLETED`, `FAILED`.
- Capabilities: `scene.inspect`, `node.rename`.
- Save modes: `KEEP_DIRTY`, `SAVE_CURRENT_SCENE`.
- Runtime result: `artifacts/godot-live-editor/editor_transaction_pilot_result.json`.

## Execution Gate

This plan is documentation only. Implementation begins on a fresh branch from then-current main after the user reviews this committed plan and explicitly selects inline or subagent-driven execution. No merge is authorized by plan approval alone.
