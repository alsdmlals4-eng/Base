# Base C0 Godot Multi-Project Pilot Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task. Use `superpowers:systematic-debugging` for every unexpected failure and `superpowers:verification-before-completion` before completion claims.

**Goal:** Build one reusable, fail-closed Base workflow that validates a project-owned descriptor, proves the caller checkout unchanged, creates a disposable Godot workspace, disables legacy Godot AI only in that workspace, injects the hardened Base transaction adapter, runs the bounded Editor Pilot, and emits byte-verifiable evidence.

**Architecture:** Descriptor validation, source inventory, workspace transformation, shared adapter materialization, Godot execution, and evidence verification are separate Python modules. The existing isolated Editor Pilot and the new project Pilot must use one capability/manifest builder. The reusable workflow is called at an immutable Base C0 commit and separately checks out that same commit; it never depends on `github.action_path`, floating `main`, or an arbitrary command supplied by a project.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, `jsonschema`, Godot 4.7.1 stable Linux headless Editor, GDScript EditorPlugin APIs, GitHub Actions reusable workflows, SHA-256, pytest.

## Authority and immutable-pin rules

- Governing design: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`.
- Plan baseline: Base `9bca3d7504fd48725715d4be27bfa8e266389223`; implementation starts from the then-current Base `main`.
- C0 is blocked until PR #166 is merged or all four equivalent hardening protections are proven on current `main`:
  1. operation IDs containing digits are accepted safely;
  2. atomic replacement never unlinks the prior record before rename succeeds;
  3. approval-required mutation rechecks token binding and expiry at execution;
  4. output validation enforces types and save-mode/hash cross-field semantics.
- After C0 merges, its **merge commit SHA** is recorded once in the Program A execution ledger as `BASE_C0_SHA`.
- Project plans consume that recorded SHA. They must not infer C0 by reading whatever commit later happens to be Base `main`.
- Every project caller uses the same SHA twice:
  - `uses: alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@BASE_C0_SHA`;
  - `with.base_pilot_commit: BASE_C0_SHA`.
- The called workflow checks out Base again at `inputs.base_pilot_commit` and verifies the descriptor contains the same SHA.

## Security and scope constraints

- Canonical addon remains `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/`.
- Existing main Scenes are inspected only. Mutation is confined to `res://.godot-live-editor-pilot/scratch.tscn` in a disposable copy.
- Source repositories retain `project.godot`, product files, legacy addons, Autoloads, saves, inputs, and export settings.
- No descriptor field carries shell text. Behavior checks use a closed enum and validated relative target.
- All child processes use `subprocess.run(argv, shell=False, timeout=...)`.
- No MCP, HTTP, WebSocket, TCP, UDP, named pipe, remote endpoint, runtime debugger, arbitrary GDScript, `Expression`, shell execution, or arbitrary property path is added.
- Godot archive: `Godot_v4.7.1-stable_linux.x86_64.zip`.
- Required archive SHA-256: `c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba`.
- Registry, release locks, v1 Schemas/evidence, frozen derivatives, projects, and Google Sheets remain unchanged.
- `PRODUCTION_ADAPTER_READY` remains `NOT_READY`.

## File responsibility map

### Shared materialization

- Create `tools/godot_editor_adapter_materialization.py`
  - `sha256_file(path: Path) -> str`
  - `build_capabilities() -> list[dict[str, object]]`
  - `build_configured_manifest(destination: Path, project_godot_sha256: str) -> dict[str, object]`
  - `copy_canonical_addon(base_root: Path, destination_project: Path) -> Path`
- Modify `tools/materialize_godot_editor_adapter_pilot.py`
  - preserve its public `materialize(source_root, destination)` behavior;
  - delegate capability and manifest construction to the shared module.

### Descriptor and runner

- Create `schemas/godot-project-pilot-v1.schema.json`
- Create `tools/godot_project_pilot_descriptor.py`
- Create `tools/godot_project_pilot_workspace.py`
- Create `tools/godot_project_pilot_evidence.py`
- Create `tools/godot_multi_project_pilot.py`

### Runtime assets

- Create `templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd`
- Create `templates/project-operations/godot-live-editor/pilot/scratch.tscn`
- Create `templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json`

### CI, docs, and tests

- Create `.github/workflows/reusable-godot-project-pilot.yml`
- Create `docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md`
- Modify `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Create `tests/test_godot_multi_project_pilot.py`
- Create `tests/test_godot_multi_project_pilot_adversarial.py`
- Create fixtures under `tests/fixtures/godot-project-pilot/`
- Modify `tests/test_local_validation.py`
- Modify `tests/test_v9_machine_contracts.py`
- Modify `.github/reference-freshness.json` only when current coupled-change rules require it.

---

### Task 1: Gate C0 on the hardened transaction adapter

**Files:**
- Create `tests/test_godot_multi_project_pilot.py`
- Read `tests/test_godot_editor_transaction_adapter.py`
- Read `tests/test_godot_editor_transaction_adapter_runtime.py`

- [ ] Write a focused precondition test that inspects the canonical addon for all four hardening protections.
- [ ] Run:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k hardening -q
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
```

- [ ] Expected: all pass. A failure blocks C0; do not weaken the gate.
- [ ] Record one state in the future C0 PR body:

```yaml
editor_adapter_hardening: MERGED_PR_166
# or
editor_adapter_hardening: EQUIVALENT_MAIN_PROOF
```

- [ ] Commit:

```bash
git add tests/test_godot_multi_project_pilot.py
git commit -m "test: gate project Pilots on editor hardening"
```

---

### Task 2: Define the closed descriptor Schema before the loader

**Files:**
- Create `schemas/godot-project-pilot-v1.schema.json`
- Create `templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json`
- Test `tests/test_godot_multi_project_pilot.py`

- [ ] Add RED tests requiring:
  - root and every nested object use `additionalProperties: false`;
  - `base_pilot_commit` is lowercase 40-hex;
  - project state is `EXISTING_GODOT_PROJECT | NOT_CREATED`;
  - exact Godot version/archive hash contract;
  - legacy plugin and Autoload arrays are bounded exact strings;
  - `legacy_disable_mode: TEMPORARY_COPY_ONLY`;
  - `source_mutation_policy: FORBIDDEN`;
  - scratch path is the runner-owned constant;
  - behavior checks use only `PYTHON_UNITTEST_MODULE`, `PYTHON_PYTEST_PATH`, or `GODOT_SCRIPT`;
  - no `command`, `shell`, environment, working-directory, or argument-array field exists;
  - `NOT_CREATED` forces `project_file: null`, `main_scene_source: NOT_APPLICABLE`, no behavior checks, and `expected_platform: NOT_CREATED`.
- [ ] Verify RED:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
```

- [ ] Implement the Schema and a safe `NOT_CREATED` template with a zero placeholder SHA that cannot authorize runtime.
- [ ] Run focused tests and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
git add schemas/godot-project-pilot-v1.schema.json templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json tests/test_godot_multi_project_pilot.py
git commit -m "feat: define closed Godot project Pilot descriptor"
```

---

### Task 3: Implement typed descriptor loading

**Files:**
- Create `tools/godot_project_pilot_descriptor.py`
- Test `tests/test_godot_multi_project_pilot.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class BehaviorCheck:
    kind: Literal["PYTHON_UNITTEST_MODULE", "PYTHON_PYTEST_PATH", "GODOT_SCRIPT"]
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
    def is_runtime_project(self) -> bool: ...

def load_descriptor(path: Path, schema_path: Path | None = None) -> ProjectPilotDescriptor: ...
```

- [ ] Write RED tests for valid loading, unknown keys, path traversal, shell metacharacters, absolute targets, duplicate entries, and `NOT_CREATED` contradictions.
- [ ] Use `jsonschema.Draft202012Validator`; sort errors by JSON path and raise stable `DESCRIPTOR_SCHEMA_INVALID` messages.
- [ ] Add semantic target patterns:
  - unittest module: Python dotted identifier;
  - pytest target: relative `tests/` path, optional `::test_name`;
  - Godot script: relative `res://tests/...gd`.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k descriptor -q
git add tools/godot_project_pilot_descriptor.py tests/test_godot_multi_project_pilot.py
git commit -m "feat: load typed Godot Pilot descriptors"
```

---

### Task 4: Extract one shared adapter materializer

**Files:**
- Create `tools/godot_editor_adapter_materialization.py`
- Modify `tools/materialize_godot_editor_adapter_pilot.py`
- Test `tests/test_godot_editor_transaction_adapter_runtime.py`
- Test `tests/test_godot_multi_project_pilot.py`

- [ ] Add RED parity tests proving the shared builder emits exactly `scene.inspect` and `node.rename`, preserves the current closed input/output Schemas, and uses the listener-free `in-process-editor-plugin` profile.
- [ ] Move the existing private hash/capability/manifest helpers without semantic changes.
- [ ] Make the old isolated Pilot materializer delegate to the shared module.
- [ ] Run:

```bash
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_godot_multi_project_pilot.py -k materialization -q
```

- [ ] Commit:

```bash
git add tools/godot_editor_adapter_materialization.py tools/materialize_godot_editor_adapter_pilot.py tests/test_godot_editor_transaction_adapter_runtime.py tests/test_godot_multi_project_pilot.py
git commit -m "refactor: share Godot adapter materialization"
```

---

### Task 5: Implement tracked-source inventory and disposable copy

**Files:**
- Create `tools/godot_project_pilot_workspace.py`
- Create fixtures under `tests/fixtures/godot-project-pilot/`
- Test both new test modules.

**Interfaces:**

```python
def list_tracked_paths(source_root: Path) -> tuple[Path, ...]: ...
def inventory_tracked_files(source_root: Path) -> dict[str, str]: ...
def inventory_digest(inventory: Mapping[str, str]) -> str: ...
def copy_to_workspace(source_root: Path, workspace_root: Path) -> None: ...
def compare_inventories(before: Mapping[str, str], after: Mapping[str, str]) -> tuple[str, ...]: ...
```

- [ ] RED cases:
  - tracked byte modification, deletion, and addition are detected;
  - symlink escape is rejected;
  - `.git`, `.godot`, previous Pilot evidence, `_base_c0`, and cache directories are excluded from the disposable copy;
  - destination must not pre-exist;
  - source and destination cannot overlap.
- [ ] Use `git -C SOURCE ls-files -z` for the authority inventory.
- [ ] Hash bytes in stable path order and derive one canonical inventory digest.
- [ ] Copy the project without `.git`; source writes are never required.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'inventory or workspace' -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k 'inventory or symlink' -q
git add tools/godot_project_pilot_workspace.py tests/fixtures/godot-project-pilot tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: create disposable Godot Pilot workspaces"
```

---

### Task 6: Transform only declared legacy authority in the copy

**Files:**
- Modify `tools/godot_project_pilot_workspace.py`
- Add clean, legacy, and multi-Autoload fixtures.
- Test both new test modules.

**Interface:**

```python
@dataclass(frozen=True)
class ProjectTransformReport:
    main_scene: str
    removed_plugins: tuple[str, ...]
    removed_autoloads: tuple[str, ...]
    preserved_autoloads: tuple[str, ...]
    before_sha256: str
    after_sha256: str

def transform_project_godot(path: Path, descriptor: ProjectPilotDescriptor) -> ProjectTransformReport: ...
```

- [ ] RED cases require exact removal of declared plugin/Autoload entries and byte-preservation of non-target lines.
- [ ] Reject duplicate sections, unsupported multiline plugin values, missing declared targets, residual legacy entries, invalid main Scene, and any request to disable an undeclared project Autoload.
- [ ] Use a strict section-aware line transformer, not a generic INI writer.
- [ ] Stable errors:

```text
PROJECT_GODOT_UNSUPPORTED_FORMAT
DECLARED_LEGACY_PLUGIN_NOT_FOUND
DECLARED_LEGACY_AUTOLOAD_NOT_FOUND
LEGACY_MUTATION_AUTHORITY_ACTIVE
MAIN_SCENE_INVALID
```

- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k transform -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k project_godot -q
git add tools/godot_project_pilot_workspace.py tests/fixtures/godot-project-pilot tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: disable legacy authority in Pilot copies"
```

---

### Task 7: Materialize the runtime and scratch-only wrapper

**Files:**
- Modify `tools/godot_project_pilot_workspace.py`
- Create runtime assets under `templates/project-operations/godot-live-editor/pilot/`
- Test `tests/test_godot_multi_project_pilot.py`

**Interface:**

```python
@dataclass(frozen=True)
class MaterializedWorkspace:
    root: Path
    main_scene: str
    manifest_path: Path
    wrapper_script: Path
    transform_report: ProjectTransformReport

def materialize_runtime_workspace(base_root: Path, workspace_root: Path, descriptor: ProjectPilotDescriptor) -> MaterializedWorkspace: ...
```

- [ ] RED tests require canonical addon copy, configured manifest validation, Base plugin activation only in the disposable `project.godot`, scratch Scene creation, and exact main Scene resolution.
- [ ] Wrapper sequence:
  1. open the configured main Scene;
  2. submit `scene.inspect` and store output;
  3. open runner-owned scratch Scene;
  4. submit `node.rename` with `KEEP_DIRTY`;
  5. invoke Editor Undo and verify old name;
  6. submit `node.rename` with `SAVE_CURRENT_SCENE`;
  7. verify terminal ledger and saved bytes;
  8. write `artifacts/godot-project-pilot/runtime-result.json`;
  9. quit nonzero on any failed assertion.
- [ ] The wrapper must mechanically refuse mutation while the real main Scene is active.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'materialize or wrapper' -q
git add tools/godot_project_pilot_workspace.py templates/project-operations/godot-live-editor/pilot tests/test_godot_multi_project_pilot.py
git commit -m "feat: materialize scratch-only project Pilot runtime"
```

---

### Task 8: Implement bounded process execution

**Files:**
- Create `tools/godot_multi_project_pilot.py`
- Test both new modules.

**Interfaces:**

```python
def argv_for_check(check: BehaviorCheck, godot_bin: Path) -> list[str]: ...
def run_behavior_check(check: BehaviorCheck, project_root: Path, godot_bin: Path) -> ProcessRecord: ...
def run_pilot(base_root: Path, source_root: Path, descriptor_path: Path, godot_bin: Path, output_dir: Path, source_commit: str) -> int: ...
```

- [ ] Closed argv mapping:

```python
if check.kind == "PYTHON_UNITTEST_MODULE":
    argv = [sys.executable, "-m", "unittest", check.target, "-v"]
elif check.kind == "PYTHON_PYTEST_PATH":
    argv = [sys.executable, "-m", "pytest", check.target, "-q"]
elif check.kind == "GODOT_SCRIPT":
    argv = [str(godot_bin), "--headless", "--path", ".", "--script", check.target]
```

- [ ] All calls use `shell=False`, explicit cwd, timeout, and bounded environment.
- [ ] Orchestration order:

```text
load descriptor
verify repository identity and exact Base pin
inventory source
run declared behavior checks against source
create disposable workspace outside tracked source
transform and materialize runtime
run Godot Editor Pilot
verify runtime evidence
re-inventory source
write final evidence
```

- [ ] Capture complete output bytes for hashing, but retain at most 1 MiB per stream and record truncation.
- [ ] Exit codes:
  - `0` PASS;
  - `2` descriptor/preflight;
  - `3` runtime or behavior failure;
  - `4` source mutation;
  - `5` evidence verification.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k 'process or run_pilot' -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k 'shell or timeout or output' -q
git add tools/godot_multi_project_pilot.py tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: run bounded multi-project Godot Pilots"
```

---

### Task 9: Verify physical evidence

**Files:**
- Create `tools/godot_project_pilot_evidence.py`
- Test both new modules.

**Interfaces:**

```python
def verify_runtime_evidence(workspace: Path, runtime_result_path: Path) -> VerifiedRuntimeEvidence: ...
def write_final_evidence(output_dir: Path, descriptor: ProjectPilotDescriptor, source_commit: str, ...) -> Path: ...
```

- [ ] RED cases: wrong saved-scene hash, ledger mismatch, missing file, path traversal, symlink escape, duplicate evidence role, malformed JSON, wrong repository, and source-before/source-after mismatch.
- [ ] Final evidence records at least:

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
  "source_after_sha256": "64-hex"
}
```

- [ ] `NOT_CREATED` emits `NOT_APPLICABLE` runtime fields and never starts Godot.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k evidence -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -k evidence -q
git add tools/godot_project_pilot_evidence.py tests/test_godot_multi_project_pilot.py tests/test_godot_multi_project_pilot_adversarial.py
git commit -m "feat: verify physical project Pilot evidence"
```

---

### Task 10: Add the final reusable workflow

**Files:**
- Create `.github/workflows/reusable-godot-project-pilot.yml`
- Test `tests/test_godot_multi_project_pilot.py`

**Authoritative workflow shape:**

```yaml
name: Reusable Godot Project Pilot

on:
  workflow_call:
    inputs:
      base_pilot_commit:
        type: string
        required: true
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
      - name: Check out caller project
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Check out exact Base C0
        uses: actions/checkout@v4
        with:
          repository: alsdmlals4-eng/Base
          ref: ${{ inputs.base_pilot_commit }}
          path: _base_c0
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install pinned validator dependencies
        run: python -m pip install --disable-pip-version-check jsonschema==4.23.0 pytest==8.3.5
      - name: Download and verify Godot
        working-directory: ${{ runner.temp }}
        run: |
          curl --fail --location --retry 3 --output godot.zip \
            https://github.com/godotengine/godot-builds/releases/download/4.7.1-stable/Godot_v4.7.1-stable_linux.x86_64.zip
          echo "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba  godot.zip" | sha256sum --check -
          unzip -q godot.zip
          chmod +x Godot_v4.7.1-stable_linux.x86_64
      - name: Verify pin and run bounded Pilot
        run: |
          python _base_c0/tools/godot_multi_project_pilot.py \
            --base-root "$GITHUB_WORKSPACE/_base_c0" \
            --source-root "$GITHUB_WORKSPACE" \
            --source-commit "$GITHUB_SHA" \
            --expected-base-commit "${{ inputs.base_pilot_commit }}" \
            --descriptor "$GITHUB_WORKSPACE/${{ inputs.descriptor_path }}" \
            --godot-bin "${RUNNER_TEMP}/Godot_v4.7.1-stable_linux.x86_64" \
            --output-dir "$GITHUB_WORKSPACE/.godot-live-editor/pilot-evidence"
      - name: Upload bounded evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: godot-project-pilot-${{ github.repository_id }}-${{ github.sha }}
          path: .godot-live-editor/pilot-evidence/
          if-no-files-found: error
          retention-days: ${{ inputs.artifact_retention_days }}
```

- [ ] RED tests require `workflow_call` only, exact `base_pilot_commit` input, two checkouts, no `github.action_path`, no floating Base ref, pinned archive hash, read-only permission, and runner invocation.
- [ ] Runner preflight compares:
  - workflow input SHA;
  - descriptor `base_pilot_commit`;
  - checked-out Base `git rev-parse HEAD`.
  Any mismatch is `BASE_PILOT_COMMIT_MISMATCH`.
- [ ] Validate retention input is 1–30 before artifact upload.
- [ ] Run and commit:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -k workflow -q
git add .github/workflows/reusable-godot-project-pilot.yml tests/test_godot_multi_project_pilot.py
git commit -m "ci: add reusable Godot project Pilot workflow"
```

---

### Task 11: Connect required suites and readiness docs

**Files:**
- Modify required aggregate tests.
- Create `docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md`.
- Modify `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`.

- [ ] Import both new test modules into `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`.
- [ ] Guide must document source/disposable roots, immutable C0 ledger, legacy source preservation, real-main read-only rule, scratch-only mutation, evidence limits, result states, project allowed paths, rollback, and Program B/C exclusions.
- [ ] Readiness state after C0:

```yaml
multi_project_pilot_runner: STATIC_PASS
real_project_pilots: NOT_RUN
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
production_adapter_ready: NOT_READY
```

- [ ] Run:

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
```

- [ ] Run placeholder/forbidden-surface scans and `git diff --check`.
- [ ] Commit the docs and required-suite wiring.

---

### Task 12: Review and merge Base C0

- [ ] Run full unittest/pytest regression and exact changed-file inventory.
- [ ] Confirm Registry, release locks, v1 Schemas/evidence, project repositories, and Program B/C files are unchanged.
- [ ] Open a Draft PR with hardening disposition, TDD RED/GREEN evidence, runtime status `NOT_RUN`, and `production_adapter_ready: NOT_READY`.
- [ ] Require exact-head:

```text
Validate Base v9 Operating Contracts: SUCCESS
Validate Game Project Operating System: SUCCESS
focused and adversarial Pilot tests: SUCCESS
branch behind main: 0
unresolved review threads: 0
```

- [ ] After explicit approval, squash merge with expected head SHA.
- [ ] Record the resulting merge commit as the sole `BASE_C0_SHA` in the Program A execution ledger. Later Base `main` movement must not change this value.
