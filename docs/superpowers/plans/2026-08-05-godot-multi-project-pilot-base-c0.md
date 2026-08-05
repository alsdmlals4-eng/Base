# Base C0 Godot Multi-Project Pilot Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable, fail-closed Base workflow that validates one project descriptor, proves the caller source tree unchanged, materializes a disposable Godot workspace, disables legacy Godot AI only in that workspace, injects the hardened Base transaction adapter, runs the bounded Editor Pilot, and emits byte-verifiable evidence.

**Architecture:** Descriptor parsing, source inventory, Godot project transformation, adapter materialization, process execution, and evidence verification are separate Python modules. The existing isolated Pilot materializer is refactored to share one capability/manifest builder instead of duplicating the v2 contract. A `workflow_call` GitHub Actions workflow downloads and verifies Godot 4.7.1, invokes the runner without a shell-command surface, and uploads bounded evidence.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, `jsonschema`, `dataclasses`, `subprocess` without `shell=True`, Godot 4.7.1 stable Linux headless Editor, GDScript, GitHub Actions, SHA-256, pytest.

## Global Constraints

- Governing design: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`.
- Plan baseline: Base `9bca3d7504fd48725715d4be27bfa8e266389223`; implementation starts from then-current `main`.
- Base C0 is blocked until PR #166 is merged or equivalent hardening is proven on current `main`.
- Canonical addon remains `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/`.
- Existing isolated Pilot remains valid and must continue to use the same manifest/capability builder.
- The runner writes only under a disposable workspace and an explicit evidence directory.
- The source checkout is inventoried from `git ls-files`; any tracked-byte change is `SOURCE_TREE_MUTATED`.
- No descriptor field may carry an arbitrary shell command.
- Behavior checks are structured profiles, executed with `subprocess.run(argv, shell=False, timeout=...)`.
- Only `scene.inspect` and `node.rename` are authorized.
- The configured main Scene is opened for read-only inspection; mutation targets only `res://.godot-live-editor-pilot/scratch.tscn`.
- A legacy plugin/autoload disable failure is `LEGACY_MUTATION_AUTHORITY_ACTIVE`, never a warning.
- Godot archive version: `4.7.1-stable`.
- Godot Linux archive SHA-256: `c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba`.
- Base creates no network listener.
- Registry, release locks, v1 Schemas, frozen derivatives, project repositories, Google Sheets, Program B transport, and Program C debugger remain unchanged.

---

## File Responsibility Map

### Shared adapter materialization

- Create: `tools/godot_editor_adapter_materialization.py`
  - Owns `sha256_file`, closed capability Schemas, capability catalog, configured v2 manifest generation, and canonical addon copy.
- Modify: `tools/materialize_godot_editor_adapter_pilot.py`
  - Retains the existing CLI/fixture flow but delegates shared logic to the new module.

### Descriptor and workspace

- Create: `schemas/godot-project-pilot-v1.schema.json`
  - Closed machine-readable project adoption contract.
- Create: `tools/godot_project_pilot_descriptor.py`
  - Loads Schema, validates JSON, returns typed immutable dataclasses.
- Create: `tools/godot_project_pilot_workspace.py`
  - Inventories tracked bytes, copies the project, edits only disposable `project.godot`, injects addon/manifest/scratch assets, and compares source inventories.
- Create: `tools/godot_project_pilot_evidence.py`
  - Validates result shape, recomputes physical hashes, bounds logs, and writes final evidence index.
- Create: `tools/godot_multi_project_pilot.py`
  - CLI orchestration only; no parsing or mutation logic beyond calling the focused modules.

### Godot runtime wrapper

- Create: `templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd`
  - Opens the real configured main Scene for `scene.inspect`, then switches to the runner-owned scratch Scene for rename/Undo/save.
- Create: `templates/project-operations/godot-live-editor/pilot/scratch.tscn`
  - Minimal runner-owned mutation target.

### Workflow and project template

- Create: `.github/workflows/reusable-godot-project-pilot.yml`
- Create: `templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json`
- Create: `docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`

### Tests

- Create: `tests/test_godot_multi_project_pilot.py`
- Create: `tests/test_godot_multi_project_pilot_adversarial.py`
- Create fixtures under: `tests/fixtures/godot-project-pilot/`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

---

### Task 1: Freeze the hardening prerequisite with a test-first gate

**Files:**
- Modify: `tests/test_godot_multi_project_pilot.py`
- Read: `tests/test_godot_editor_transaction_adapter.py`
- Read: `tests/test_godot_editor_transaction_adapter_runtime.py`

**Interfaces:**
- Consumes: current transaction adapter source.
- Produces: `assert_editor_adapter_hardening_ready(root: Path) -> None` used by the C0 test suite and runner preflight.

- [ ] **Step 1: Write a failing hardening readiness test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"


def test_editor_adapter_hardening_is_present_before_multi_project_runner() -> None:
    ledger = (ADDON / "operation_ledger.gd").read_text(encoding="utf-8")
    guard = (ADDON / "runtime_contract_guard.gd").read_text(encoding="utf-8")
    registry = (ADDON / "capability_registry.gd").read_text(encoding="utf-8")
    evidence = (ADDON / "evidence_writer.gd").read_text(encoding="utf-8")

    assert "0123456789" in ledger
    assert "DirAccess.rename_absolute" in ledger or "DirAccess.rename" in ledger
    assert "approval_token" in guard
    assert "expires_at" in guard
    assert "saved_scene_sha256" in registry
    assert "save_mode" in registry
    assert "sha256" in evidence
```

- [ ] **Step 2: Run the test on current main**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py::test_editor_adapter_hardening_is_present_before_multi_project_runner -q
```

Expected: PASS only if PR #166 or equivalent hardening is already present. If it fails, stop Base C0 and resolve the hardening PR separately; do not weaken this test.

- [ ] **Step 3: Add a runtime-regression invocation to the preflight**

```python
HARDENING_TESTS = (
    "tests/test_godot_editor_transaction_adapter.py",
    "tests/test_godot_editor_transaction_adapter_runtime.py",
)
```

The implementation PR body must record the exact hardening disposition and test results.

- [ ] **Step 4: Commit the gate**

```bash
git add tests/test_godot_multi_project_pilot.py
git commit -m "test: gate multi-project Pilot on editor adapter hardening"
```

---

### Task 2: Add the closed project Pilot descriptor Schema

**Files:**
- Create: `schemas/godot-project-pilot-v1.schema.json`
- Create: `templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- Consumes: project-owned `.godot-live-editor/project-pilot.json`.
- Produces: a closed descriptor accepted by `load_descriptor(path)`.

- [ ] **Step 1: Write descriptor RED tests**

```python
import json
from pathlib import Path

SCHEMA = ROOT / "schemas/godot-project-pilot-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json"


def test_descriptor_schema_and_template_are_closed() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert schema["additionalProperties"] is False
    assert template["schema_version"] == "1"
    assert template["source_mutation_policy"] == "FORBIDDEN"
    assert template["legacy_disable_mode"] == "TEMPORARY_COPY_ONLY"


def test_descriptor_rejects_arbitrary_command_fields() -> None:
    text = SCHEMA.read_text(encoding="utf-8")
    assert '"command"' not in text
    assert '"shell"' not in text
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
```

Expected: FAIL because Schema and template do not exist.

- [ ] **Step 3: Create the exact root Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/alsdmlals4-eng/Base/schemas/godot-project-pilot-v1.schema.json",
  "title": "Godot Project Pilot Descriptor v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "project_identity",
    "base_pilot_commit",
    "project_state",
    "godot",
    "project_file",
    "main_scene_source",
    "legacy_editor_plugins",
    "legacy_autoloads",
    "legacy_disable_mode",
    "source_mutation_policy",
    "scratch_scene_path",
    "behavior_checks",
    "expected_platform"
  ],
  "properties": {
    "schema_version": {"const": "1"},
    "project_identity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["repository", "project_id"],
      "properties": {
        "repository": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"},
        "project_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]{2,63}$"}
      }
    },
    "base_pilot_commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
    "project_state": {"enum": ["EXISTING_GODOT_PROJECT", "NOT_CREATED"]},
    "godot": {
      "type": "object",
      "additionalProperties": false,
      "required": ["version", "archive_sha256"],
      "properties": {
        "version": {"const": "4.7.1-stable"},
        "archive_sha256": {"const": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"}
      }
    },
    "project_file": {"type": ["string", "null"], "pattern": "^project\\.godot$"},
    "main_scene_source": {"enum": ["application/run/main_scene", "NOT_APPLICABLE"]},
    "legacy_editor_plugins": {
      "type": "array",
      "uniqueItems": true,
      "maxItems": 8,
      "items": {"type": "string", "pattern": "^res://addons/[A-Za-z0-9_./-]+/plugin\\.cfg$"}
    },
    "legacy_autoloads": {
      "type": "array",
      "uniqueItems": true,
      "maxItems": 8,
      "items": {"type": "string", "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,63}$"}
    },
    "legacy_disable_mode": {"const": "TEMPORARY_COPY_ONLY"},
    "source_mutation_policy": {"const": "FORBIDDEN"},
    "scratch_scene_path": {"const": "res://.godot-live-editor-pilot/scratch.tscn"},
    "behavior_checks": {
      "type": "array",
      "maxItems": 5,
      "items": {"$ref": "#/$defs/behaviorCheck"}
    },
    "expected_platform": {"enum": ["PC", "ANDROID", "MOBILE", "MULTI", "NOT_CREATED"]}
  },
  "$defs": {
    "behaviorCheck": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "target", "timeout_seconds"],
      "properties": {
        "kind": {"enum": ["PYTHON_UNITTEST_MODULE", "PYTHON_PYTEST_PATH", "GODOT_SCRIPT"]},
        "target": {"type": "string", "minLength": 1, "maxLength": 200},
        "timeout_seconds": {"type": "integer", "minimum": 5, "maximum": 300}
      }
    }
  },
  "allOf": [
    {
      "if": {"properties": {"project_state": {"const": "NOT_CREATED"}}},
      "then": {
        "properties": {
          "project_file": {"const": null},
          "main_scene_source": {"const": "NOT_APPLICABLE"},
          "behavior_checks": {"maxItems": 0},
          "expected_platform": {"const": "NOT_CREATED"}
        }
      },
      "else": {
        "properties": {
          "project_file": {"const": "project.godot"},
          "main_scene_source": {"const": "application/run/main_scene"}
        }
      }
    }
  ]
}
```

- [ ] **Step 4: Create a safe `NOT_CREATED` template**

The checked-in template uses `project_state: NOT_CREATED`, `base_pilot_commit` set to forty zeroes, no behavior checks, and no runtime claim. Project plans replace it with an exact merged C0 SHA.

- [ ] **Step 5: Run tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
git add schemas/godot-project-pilot-v1.schema.json templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json tests/test_godot_multi_project_pilot.py
git commit -m "feat: define closed Godot project Pilot descriptor"
```

---

### Task 3: Implement typed descriptor loading and semantic checks

**Files:**
- Create: `tools/godot_project_pilot_descriptor.py`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- `load_descriptor(path: Path, schema_path: Path | None = None) -> ProjectPilotDescriptor`
- `validate_descriptor_document(document: Mapping[str, object], schema: Mapping[str, object]) -> tuple[str, ...]`
- `ProjectPilotDescriptor.repository: str`
- `ProjectPilotDescriptor.is_runtime_project: bool`

- [ ] **Step 1: Write RED tests for typed loading**

```python
from tools.godot_project_pilot_descriptor import load_descriptor


def test_load_descriptor_returns_immutable_typed_contract(tmp_path: Path) -> None:
    path = tmp_path / "project-pilot.json"
    path.write_text(json.dumps(valid_descriptor()), encoding="utf-8")
    descriptor = load_descriptor(path)
    assert descriptor.repository == "alsdmlals4-eng/example"
    assert descriptor.is_runtime_project is True
    assert descriptor.behavior_checks == ()


def test_descriptor_rejects_wrong_repo_and_path_traversal(tmp_path: Path) -> None:
    document = valid_descriptor()
    document["project_identity"]["repository"] = "../escape"
    path = tmp_path / "project-pilot.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="DESCRIPTOR_SCHEMA_INVALID"):
        load_descriptor(path)
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k load_descriptor -q
```

- [ ] **Step 3: Implement immutable dataclasses**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

BehaviorKind = Literal[
    "PYTHON_UNITTEST_MODULE",
    "PYTHON_PYTEST_PATH",
    "GODOT_SCRIPT",
]

@dataclass(frozen=True)
class BehaviorCheck:
    kind: BehaviorKind
    target: str
    timeout_seconds: int

@dataclass(frozen=True)
class ProjectPilotDescriptor:
    repository: str
    project_id: str
    base_pilot_commit: str
    project_state: str
    godot_version: str
    godot_archive_sha256: str
    project_file: str | None
    main_scene_source: str
    legacy_editor_plugins: tuple[str, ...]
    legacy_autoloads: tuple[str, ...]
    scratch_scene_path: str
    behavior_checks: tuple[BehaviorCheck, ...]
    expected_platform: str

    @property
    def is_runtime_project(self) -> bool:
        return self.project_state == "EXISTING_GODOT_PROJECT"
```

Use `jsonschema.Draft202012Validator`. Sort all errors by JSON path and raise one `ValueError` prefixed `DESCRIPTOR_SCHEMA_INVALID:`. Add semantic checks that each Python module/path and Godot script target matches a conservative pattern and contains no whitespace, shell metacharacter, absolute path, or `..` segment.

- [ ] **Step 4: Run tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
git add tools/godot_project_pilot_descriptor.py tests/test_godot_multi_project_pilot.py
git commit -m "feat: load typed Godot Pilot descriptors"
```

---

### Task 4: Extract one shared adapter manifest/materialization module

**Files:**
- Create: `tools/godot_editor_adapter_materialization.py`
- Modify: `tools/materialize_godot_editor_adapter_pilot.py`
- Test: `tests/test_godot_editor_transaction_adapter_runtime.py`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- `sha256_file(path: Path) -> str`
- `build_capabilities() -> list[dict[str, object]]`
- `build_configured_manifest(destination: Path, project_godot_sha256: str) -> dict[str, object]`
- `copy_canonical_addon(base_root: Path, destination_project: Path) -> Path`
- Existing `materialize(source_root: Path, destination: Path) -> Path` remains callable.

- [ ] **Step 1: Add parity RED tests**

```python
from tools.godot_editor_adapter_materialization import (
    build_capabilities,
    build_configured_manifest,
)


def test_shared_manifest_builder_preserves_existing_pilot_contract(tmp_path: Path) -> None:
    project = tmp_path / "project.godot"
    project.write_text("config_version=5\n", encoding="utf-8")
    manifest = build_configured_manifest(tmp_path, sha256_file(project))
    assert [item["capability_id"] for item in manifest["capabilities"]] == [
        "scene.inspect",
        "node.rename",
    ]
    assert manifest["transport"]["endpoint_identity"] == "in-process-editor-plugin"
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k shared_manifest -q
```

- [ ] **Step 3: Move existing private helpers without semantic change**

Move the current `_sha256_file`, `_closed_schema`, `_capabilities`, and `_manifest` implementations from `materialize_godot_editor_adapter_pilot.py` into the new module. Rename them to the public interfaces above. Keep capability IDs, Schemas, hashes, transport profile, versions, and engine compatibility byte-for-byte equivalent.

- [ ] **Step 4: Make the old materializer delegate**

```python
from tools.godot_editor_adapter_materialization import (
    build_configured_manifest,
    copy_canonical_addon,
    sha256_file,
)
```

The isolated Pilot's output and tests must remain unchanged.

- [ ] **Step 5: Verify old and new paths**

```bash
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_godot_multi_project_pilot.py -k manifest -q
```

- [ ] **Step 6: Commit**

```bash
git add tools/godot_editor_adapter_materialization.py tools/materialize_godot_editor_adapter_pilot.py tests/test_godot_editor_transaction_adapter_runtime.py tests/test_godot_multi_project_pilot.py
git commit -m "refactor: share Godot adapter materialization"
```

---

### Task 5: Implement tracked-source inventory and disposable copy

**Files:**
- Create: `tools/godot_project_pilot_workspace.py`
- Create fixtures: `tests/fixtures/godot-project-pilot/clean-project/`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- `list_tracked_paths(source_root: Path) -> tuple[Path, ...]`
- `inventory_tracked_files(source_root: Path) -> dict[str, str]`
- `copy_to_workspace(source_root: Path, workspace_root: Path) -> None`
- `compare_inventories(before: Mapping[str, str], after: Mapping[str, str]) -> tuple[str, ...]`

- [ ] **Step 1: Write inventory RED tests**

```python
def test_inventory_detects_tracked_byte_change(git_fixture: Path) -> None:
    before = inventory_tracked_files(git_fixture)
    (git_fixture / "project.godot").write_text("changed\n", encoding="utf-8")
    after = inventory_tracked_files(git_fixture)
    assert compare_inventories(before, after) == ("project.godot",)


def test_workspace_copy_never_contains_git_metadata(git_fixture: Path, tmp_path: Path) -> None:
    destination = tmp_path / "pilot"
    copy_to_workspace(git_fixture, destination)
    assert not (destination / ".git").exists()
    assert (destination / "project.godot").exists()
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k inventory -q
```

- [ ] **Step 3: Implement tracked inventory**

```python
def list_tracked_paths(source_root: Path) -> tuple[Path, ...]:
    completed = subprocess.run(
        ["git", "-C", str(source_root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return tuple(
        Path(item.decode("utf-8"))
        for item in completed.stdout.split(b"\0")
        if item
    )


def inventory_tracked_files(source_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in list_tracked_paths(source_root):
        path = (source_root / relative).resolve()
        path.relative_to(source_root.resolve())
        result[relative.as_posix()] = sha256_file(path)
    return result
```

Reject symlinks that resolve outside the checkout. Copy tracked files and required untracked project directories only by walking the source tree with `.git`, `.godot`, existing Pilot artifacts, and cache directories excluded.

- [ ] **Step 4: Run tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'inventory or workspace_copy' -q
git add tools/godot_project_pilot_workspace.py tests/fixtures/godot-project-pilot tests/test_godot_multi_project_pilot.py
git commit -m "feat: create disposable Godot Pilot workspaces"
```

---

### Task 6: Implement bounded `project.godot` transformation

**Files:**
- Modify: `tools/godot_project_pilot_workspace.py`
- Add fixture: `tests/fixtures/godot-project-pilot/legacy-project/project.godot`
- Test: `tests/test_godot_multi_project_pilot.py`
- Test: `tests/test_godot_multi_project_pilot_adversarial.py`

**Interfaces:**
- `transform_project_godot(path: Path, plugins: tuple[str, ...], autoloads: tuple[str, ...]) -> ProjectTransformReport`
- `ProjectTransformReport.removed_plugins: tuple[str, ...]`
- `ProjectTransformReport.removed_autoloads: tuple[str, ...]`
- `ProjectTransformReport.main_scene: str`

- [ ] **Step 1: Write RED tests for exact removal and preservation**

```python
def test_transform_removes_only_declared_legacy_authority(tmp_path: Path) -> None:
    project = copy_fixture("legacy-project", tmp_path)
    before = project.read_text(encoding="utf-8")
    report = transform_project_godot(
        project,
        ("res://addons/godot_ai/plugin.cfg",),
        ("_mcp_game_helper",),
    )
    after = project.read_text(encoding="utf-8")
    assert "res://addons/godot_ai/plugin.cfg" not in after
    assert "_mcp_game_helper" not in after
    assert 'UrbanLegendState="*res://scripts/core/urban_legend_state.gd"' in after
    assert report.main_scene.startswith("res://")
    assert "[rendering]" in before and "[rendering]" in after
```

- [ ] **Step 2: Add adversarial cases**

Reject duplicate sections, multiline plugin arrays the parser cannot round-trip, missing declared plugin/autoload, absolute main Scene paths, and any post-transform residual legacy entry. Error codes are exact:

```text
PROJECT_GODOT_UNSUPPORTED_FORMAT
DECLARED_LEGACY_PLUGIN_NOT_FOUND
DECLARED_LEGACY_AUTOLOAD_NOT_FOUND
LEGACY_MUTATION_AUTHORITY_ACTIVE
MAIN_SCENE_INVALID
```

- [ ] **Step 3: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k transform -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k project_godot -q
```

- [ ] **Step 4: Implement a section-aware line transformer**

Use exact section headers and key parsing. Do not use a generic INI writer because Godot values are not standard INI values and rewriting the whole file would create unnecessary drift. Parse the one `enabled=PackedStringArray(...)` value with a strict quoted-string regex, remove only exact plugin paths, and preserve every non-target line byte-for-byte.

- [ ] **Step 5: Verify and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k transform -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k project_godot -q
git add tools/godot_project_pilot_workspace.py tests/fixtures/godot-project-pilot/legacy-project tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: disable legacy Godot authority in Pilot copies"
```

---

### Task 7: Materialize the adapter, manifest, and scratch Pilot assets

**Files:**
- Modify: `tools/godot_project_pilot_workspace.py`
- Create: `templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd`
- Create: `templates/project-operations/godot-live-editor/pilot/scratch.tscn`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- `materialize_runtime_workspace(base_root: Path, workspace_root: Path, descriptor: ProjectPilotDescriptor) -> MaterializedWorkspace`
- `MaterializedWorkspace.main_scene: str`
- `MaterializedWorkspace.manifest_path: Path`
- `MaterializedWorkspace.wrapper_script: Path`

- [ ] **Step 1: Write materialization RED tests**

```python
def test_runtime_materialization_injects_only_runner_owned_assets(tmp_path: Path) -> None:
    workspace = prepare_clean_workspace(tmp_path)
    result = materialize_runtime_workspace(ROOT, workspace, runtime_descriptor())
    assert (workspace / "addons/base_live_editor_adapter/plugin.cfg").is_file()
    assert result.manifest_path.is_file()
    assert (workspace / ".godot-live-editor-pilot/scratch.tscn").is_file()
    assert result.main_scene == "res://game/main/main.tscn"
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k runtime_materialization -q
```

- [ ] **Step 3: Implement workspace materialization**

Actions, in order:

1. Validate `project.godot` and resolve the configured main Scene.
2. Disable declared legacy entries in the disposable copy.
3. Copy the canonical addon through `copy_canonical_addon()`.
4. Add `res://addons/base_live_editor_adapter/plugin.cfg` to the disposable `[editor_plugins]` list.
5. Copy the wrapper and scratch Scene under `.godot-live-editor-pilot/`.
6. Generate the configured v2 manifest bound to the disposable absolute path and disposable `project.godot` SHA-256.
7. Run `validate_contract_pair(manifest, mode="AUTHORIZE")` and fail on any error.
8. Verify the source checkout inventory is still unchanged.

- [ ] **Step 4: Implement the wrapper contract**

`multi_project_pilot.gd` must:

```text
open the configured main Scene
wait until the edited scene is available
submit scene.inspect and record the result
open runner-owned scratch.tscn
submit node.rename KEEP_DIRTY
call Editor undo and verify the old name
submit node.rename SAVE_CURRENT_SCENE
verify the saved physical SHA-256 and terminal ledger
write artifacts/godot-project-pilot/runtime-result.json
quit with 0 only when every required assertion passes
```

The script must never submit `node.rename` while the real main Scene is active.

- [ ] **Step 5: Run static tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'materialization or wrapper' -q
git add tools/godot_project_pilot_workspace.py templates/project-operations/godot-live-editor/pilot tests/test_godot_multi_project_pilot.py
git commit -m "feat: materialize isolated project Pilot runtime"
```

---

### Task 8: Implement bounded process execution and behavior-check profiles

**Files:**
- Create: `tools/godot_multi_project_pilot.py`
- Test: `tests/test_godot_multi_project_pilot.py`
- Test: `tests/test_godot_multi_project_pilot_adversarial.py`

**Interfaces:**
- `run_pilot(base_root: Path, source_root: Path, descriptor_path: Path, godot_bin: Path, output_dir: Path) -> int`
- `run_behavior_check(check: BehaviorCheck, project_root: Path, godot_bin: Path) -> ProcessRecord`
- CLI exits `0` for PASS, `2` for descriptor/preflight failure, `3` for runtime failure, `4` for source mutation, and `5` for evidence verification failure.

- [ ] **Step 1: Write execution RED tests**

```python
def test_behavior_checks_never_use_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda argv, **kwargs: calls.append((argv, kwargs)) or fake_success())
    run_behavior_check(BehaviorCheck("PYTHON_UNITTEST_MODULE", "tests.test_contract", 30), ROOT, Path("godot"))
    assert calls[0][1]["shell"] is False
    assert calls[0][0] == [sys.executable, "-m", "unittest", "tests.test_contract", "-v"]
```

- [ ] **Step 2: Add profile mapping**

```python
def argv_for_check(check: BehaviorCheck, godot_bin: Path) -> list[str]:
    if check.kind == "PYTHON_UNITTEST_MODULE":
        return [sys.executable, "-m", "unittest", check.target, "-v"]
    if check.kind == "PYTHON_PYTEST_PATH":
        return [sys.executable, "-m", "pytest", check.target, "-q"]
    if check.kind == "GODOT_SCRIPT":
        return [str(godot_bin), "--headless", "--path", ".", "--script", check.target]
    raise ValueError("BEHAVIOR_CHECK_KIND_UNSUPPORTED")
```

- [ ] **Step 3: Implement orchestration order**

```text
load descriptor
verify current repository identity from GITHUB_REPOSITORY when present
inventory source
create temporary workspace outside source
materialize runtime or emit NOT_APPLICABLE for NOT_CREATED
run behavior checks in source read-only mode
run Godot Editor Pilot in disposable workspace
verify runtime evidence
re-inventory source
write final evidence index
return bounded exit code
```

Use `tempfile.TemporaryDirectory(prefix="base-godot-project-pilot-")`. Capture stdout/stderr, truncate each to 1 MiB, and record truncation flags.

- [ ] **Step 4: Add adversarial timeout and output-bound tests**

Verify a timeout produces `PROCESS_TIMEOUT`, no retry, and a nonzero final state. Verify logs larger than 1 MiB are truncated with SHA-256 of the full captured bytes computed before truncation.

- [ ] **Step 5: Run and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'behavior or run_pilot' -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k 'shell or timeout or output' -q
git add tools/godot_multi_project_pilot.py tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: run bounded multi-project Godot Pilots"
```

---

### Task 9: Implement physical evidence verification

**Files:**
- Create: `tools/godot_project_pilot_evidence.py`
- Test: `tests/test_godot_multi_project_pilot.py`
- Test: `tests/test_godot_multi_project_pilot_adversarial.py`

**Interfaces:**
- `verify_runtime_evidence(workspace: Path, runtime_result_path: Path) -> VerifiedRuntimeEvidence`
- `write_final_evidence(output_dir: Path, descriptor: ProjectPilotDescriptor, ...) -> Path`

- [ ] **Step 1: Write evidence RED tests**

```python
def test_evidence_recomputes_saved_scene_hash(tmp_path: Path) -> None:
    scene = tmp_path / ".godot-live-editor-pilot/scratch.tscn"
    scene.parent.mkdir(parents=True)
    scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
    result = runtime_result(saved_scene_sha256=sha256_file(scene))
    verified = verify_runtime_evidence(tmp_path, write_result(tmp_path, result))
    assert verified.saved_scene_sha256 == sha256_file(scene)


def test_evidence_rejects_declared_hash_without_matching_bytes(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="ARTIFACT_BYTE_HASH_MISMATCH"):
        verify_runtime_evidence(tmp_path, write_mismatched_result(tmp_path))
```

- [ ] **Step 2: Define final result fields**

```json
{
  "schema_version": "1",
  "repository": "owner/repo",
  "source_commit": "40-hex",
  "base_pilot_commit": "40-hex",
  "project_state": "EXISTING_GODOT_PROJECT",
  "project_load": "PASS",
  "main_scene_inspect": "PASS",
  "scratch_scene_rename": "PASS",
  "editor_undo": "PASS",
  "scratch_scene_save": "PASS",
  "physical_sha256": "PASS",
  "source_tree_unchanged": "PASS",
  "legacy_mutation_authority": "DISABLED_IN_WORKSPACE_ONLY",
  "base_network_listener": false,
  "runtime_result_sha256": "64-hex",
  "saved_scene_sha256": "64-hex",
  "source_before_sha256": "64-hex",
  "source_after_sha256": "64-hex",
  "evidence_files": []
}
```

For `NOT_CREATED`, runtime fields are `NOT_APPLICABLE` and no Godot process is executed.

- [ ] **Step 3: Verify every referenced file physically**

Paths must resolve under the explicit output directory or workspace. Reject absolute paths, traversal, symlink escape, duplicate evidence roles, missing files, malformed JSON, and mismatched hashes.

- [ ] **Step 4: Run and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k evidence -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k evidence -q
git add tools/godot_project_pilot_evidence.py tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: verify physical Godot Pilot evidence"
```

---

### Task 10: Add the reusable GitHub Actions workflow

**Files:**
- Create: `.github/workflows/reusable-godot-project-pilot.yml`
- Test: `tests/test_godot_multi_project_pilot.py`

**Interfaces:**
- Caller input: `descriptor_path` default `.godot-live-editor/project-pilot.json`.
- Caller input: `artifact_retention_days` integer, default `14`, max `30`.
- No secrets are required.
- Produces artifact name `godot-project-pilot-${{ github.repository_id }}-${{ github.sha }}`.

- [ ] **Step 1: Write workflow RED assertions**

```python
def test_reusable_workflow_is_workflow_call_only_and_pinned() -> None:
    text = (ROOT / ".github/workflows/reusable-godot-project-pilot.yml").read_text(encoding="utf-8")
    assert "workflow_call:" in text
    assert "pull_request:" not in text
    assert "permissions:\n  contents: read" in text
    assert "Godot_v4.7.1-stable_linux.x86_64.zip" in text
    assert "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba" in text
    assert "tools/godot_multi_project_pilot.py" in text
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k reusable_workflow -q
```

- [ ] **Step 3: Implement the workflow**

```yaml
name: Reusable Godot Project Pilot

on:
  workflow_call:
    inputs:
      descriptor_path:
        type: string
        required: false
        default: .godot-live-editor/project-pilot.json
      artifact_retention_days:
        type: number
        required: false
        default: 14

permissions:
  contents: read

jobs:
  project-pilot:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install validator dependency
        run: python -m pip install --disable-pip-version-check jsonschema==4.23.0 pytest==8.3.5
      - name: Download exact Godot
        run: |
          curl --fail --location --retry 3 --output godot.zip \
            https://github.com/godotengine/godot-builds/releases/download/4.7.1-stable/Godot_v4.7.1-stable_linux.x86_64.zip
          echo "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba  godot.zip" | sha256sum --check -
          unzip -q godot.zip
          chmod +x Godot_v4.7.1-stable_linux.x86_64
      - name: Run bounded project Pilot
        env:
          BASE_ROOT: ${{ github.action_path }}
        run: |
          python "$BASE_ROOT/tools/godot_multi_project_pilot.py" \
            --base-root "$BASE_ROOT" \
            --source-root "$GITHUB_WORKSPACE" \
            --descriptor "$GITHUB_WORKSPACE/${{ inputs.descriptor_path }}" \
            --godot-bin "$GITHUB_WORKSPACE/Godot_v4.7.1-stable_linux.x86_64" \
            --output-dir "$GITHUB_WORKSPACE/.godot-live-editor/pilot-evidence"
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: godot-project-pilot-${{ github.repository_id }}-${{ github.sha }}
          path: .godot-live-editor/pilot-evidence/
          if-no-files-found: error
          retention-days: ${{ inputs.artifact_retention_days }}
```

Because `github.action_path` is not populated for reusable workflows, the final implementation must first check out Base itself at the workflow's own immutable ref into `_base_c0` using `actions/checkout@v4` with `repository: alsdmlals4-eng/Base` and `ref: ${{ github.workflow_ref }}` parsing is forbidden. Instead, the caller supplies `base_pilot_commit`, and the called workflow checks out Base at that exact input after confirming it matches the descriptor. Add this required input:

```yaml
base_pilot_commit:
  type: string
  required: true
```

Then use:

```yaml
- uses: actions/checkout@v4
  with:
    repository: alsdmlals4-eng/Base
    ref: ${{ inputs.base_pilot_commit }}
    path: _base_c0
```

The runner receives `--base-root "$GITHUB_WORKSPACE/_base_c0"`.

- [ ] **Step 4: Add workflow pin-consistency validation**

Before runtime, compare the input SHA with the descriptor's `base_pilot_commit`; mismatch is `BASE_PILOT_COMMIT_MISMATCH`.

- [ ] **Step 5: Run tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k workflow -q
git add .github/workflows/reusable-godot-project-pilot.yml tests/test_godot_multi_project_pilot.py
git commit -m "ci: add reusable Godot project Pilot workflow"
```

---

### Task 11: Wire required suites, docs, and adversarial regression

**Files:**
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Create: `docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Modify: `.github/reference-freshness.json` only if current coupled-change rules require it.

**Interfaces:**
- Consumes: all C0 artifacts.
- Produces: required CI discovery and truthful readiness documentation.

- [ ] **Step 1: Import both new test modules into required suites**

Follow the existing aggregation pattern used for `test_godot_editor_transaction_adapter`.

- [ ] **Step 2: Write the guide**

The guide must include:

```text
source checkout versus disposable workspace
exact Base SHA pin
legacy Godot AI source-preservation rule
real main Scene read-only rule
scratch-only mutation rule
source inventory and physical evidence rules
allowed result states
project PR allowed/forbidden paths
rollback and artifact retention
Program B/C exclusions
```

- [ ] **Step 3: Update readiness truthfully**

Add:

```yaml
multi_project_pilot_runner: STATIC_PASS
real_project_pilots: NOT_RUN
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
production_adapter_ready: NOT_READY
```

Do not mark real-project runtime PASS in Base C0.

- [ ] **Step 4: Run full focused and aggregate tests**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
```

- [ ] **Step 5: Run placeholder and forbidden-surface scans**

```bash
rg -n 'TODO|TBD|implement later|fill in details' \
  tools/godot_*pilot* schemas/godot-project-pilot-v1.schema.json \
  .github/workflows/reusable-godot-project-pilot.yml \
  docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md
rg -n 'shell=True|OS.execute|TCPServer|WebSocket|HTTPServer|PacketPeerUDP|Thread.new|Expression.new' \
  tools/godot_*pilot* templates/project-operations/godot-live-editor/pilot
```

Expected: no placeholder matches and no forbidden runtime surface.

- [ ] **Step 6: Commit**

```bash
git add tests/test_local_validation.py tests/test_v9_machine_contracts.py docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md .github/reference-freshness.json
git commit -m "docs: connect Godot multi-project Pilot contracts"
```

---

### Task 12: Validate exact head and prepare the Base C0 Draft PR

**Files:**
- No new production files.

**Interfaces:**
- Consumes: complete C0 branch.
- Produces: a reviewable Draft PR and, after explicit approval, one immutable Base C0 merge SHA.

- [ ] **Step 1: Run complete local validation**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] **Step 2: Verify protected boundaries**

Confirm no changes to:

```text
skills/SKILL_REGISTRY.json
released Registry lock/hash
v1 Schemas
existing v1 Pilot evidence
release locks/frozen derivatives
project repositories
Google Sheets
Program B/C files
```

- [ ] **Step 3: Open a Draft PR**

The PR body records:

```yaml
hardening_pr_166_or_equivalent: exact state and evidence
real_project_runtime: NOT_RUN
source_project_mutation: NOT_APPLICABLE_IN_BASE_C0
workflow_pin_contract: STATIC_PASS
production_adapter_ready: NOT_READY
merge_authorization: NOT_GRANTED
```

- [ ] **Step 4: Require exact-head GitHub Actions**

Required:

```text
Validate Base v9 Operating Contracts: SUCCESS
Validate Game Project Operating System: SUCCESS
unresolved review threads: 0
changed-file inventory matches plan
branch behind main: 0
```

- [ ] **Step 5: Merge only after explicit approval**

Use squash merge with expected head SHA. Record the resulting Base C0 main SHA; all project plans consume that immutable value.
