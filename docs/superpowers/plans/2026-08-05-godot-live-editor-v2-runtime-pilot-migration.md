# Godot Live Editor v2 Runtime Pilot Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the isolated Godot 4.7.1 Pilot from legacy contract v1 to active contract v2, execute the real Godot binary, regenerate trustworthy evidence, and remove the temporary v1 compatibility surface.

**Architecture:** Keep the existing self-contained fixture and no-network CLI/EditorPlugin boundary, but migrate its manifest, request normalization, approval binding, durable task ledger, output validation, evidence hashing, and recovery proof to v2. Run all changes against an exact Godot executable hash, preserve the historical v1 evidence as an archived record, and delete v1 schemas only after the new runtime and repository regressions are GREEN.

**Tech Stack:** Godot `4.7.1.stable.official.a13da4feb`, GDScript, JSON, JSON Schema Draft 2020-12, Python 3.12 `unittest`, `jsonschema==4.26.0`, SHA-256 evidence, existing Base GitHub Actions.

## Global Constraints

- Do not begin until the static v2 reconciliation is merged to main and its completion gate records `active_contract_template_adapter_v2: true`, `v1_new_adoption_prohibited: true`, and `current_merge_ref_ci: PASS`.
- Re-fetch main and create a fresh isolated branch/worktree at execution time. Do not reuse the static implementation or planning branch.
- A usable Godot executable is mandatory. Run `godot --version`, calculate its SHA-256, and compare it to the declared evidence before changing any runtime status.
- When the executable differs from the historical Pilot executable SHA-256 `32f8d7596c4b41185512b1c49d69f2da3be018fd784a53e349fa92a98a97bcde`, create a new evidence record with the new hash; never silently rewrite the historical binary identity.
- Never commit the Godot executable, archive, export templates, `.godot/`, generated UID files, runtime artifact contents, tokens, absolute sandbox paths, or user project configurations.
- Keep all fixture writes under `examples/godot-live-editor-pilot/artifacts/`; reject absolute paths, `..`, and symlink escape.
- No listening socket, remote endpoint, production MCP server, arbitrary shell, arbitrary script, or unrestricted expression/property execution.
- The EditorPlugin remains a lifecycle/recovery proof only. Do not claim production main-thread mutation queue, Undo/Redo integration, runtime debugger, project test framework, physical input, or human usability.
- Use TDD with a test-only RED commit before modifying the Pilot implementation.
- Do not delete v1 schemas or compatibility documentation until the migrated v2 Pilot passes actual Godot runtime tests and static repository tests on the same exact head.
- Preserve `skills/SKILL_REGISTRY.json`, Base v9.4.3/predecessor release locks, and frozen release derivatives byte-for-byte.

---

### Task 1: Preflight the static v2 authority and actual Godot binary

**Files:**
- Read only: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Read only: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Read only: `tools/validate_godot_live_editor_contract.py`
- Read only: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
- Read only: `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json`
- Create at RED stage: `tests/test_godot_live_editor_v2_runtime_pilot.py`
- Modify at RED stage: `tests/test_v9_machine_contracts.py`
- Modify at RED stage: `tests/test_local_validation.py`

**Interfaces:**
- Consumes: active v2 schemas and semantic validator from Stage A.
- Produces: exact `GODOT_BIN`, `GODOT_VERSION`, `GODOT_SHA256`, and a required-CI-discovered `GodotLiveEditorV2RuntimePilotTests` suite.

- [ ] **Step 1: Verify Stage A completion facts**

Run:

```bash
+python - <<'PY'
+import json
+from pathlib import Path
+
+manifest_schema = json.loads(Path('schemas/godot-live-editor-capability-manifest-v2.schema.json').read_text(encoding='utf-8'))
+operation_schema = json.loads(Path('schemas/godot-live-editor-operation-envelope-v2.schema.json').read_text(encoding='utf-8'))
+template = json.loads(Path('templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json').read_text(encoding='utf-8'))
+
+assert manifest_schema['properties']['schema_version']['const'] == 2
+assert operation_schema['properties']['schema_version']['const'] == 2
+assert template['schema_version'] == 2
+assert template['contract_version'] == '2.0.0'
+assert Path('tools/validate_godot_live_editor_contract.py').is_file()
+assert Path('docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md').is_file()
+print('STATIC_V2_AUTHORITY_PASS')
+PY
+```
+
+Expected: `STATIC_V2_AUTHORITY_PASS`. Stop when any v2 authority surface is missing or still Draft-only.
+
+- [ ] **Step 2: Resolve and hash the Godot executable**
+
+Use an explicit environment variable, never a guessed executable:
+
+```bash
+test -n "${GODOT_BIN:-}"
+test -x "$GODOT_BIN"
+GODOT_VERSION="$($GODOT_BIN --version | tr -d '\r')"
+GODOT_SHA256="$(sha256sum "$GODOT_BIN" | awk '{print $1}')"
+printf 'version=%s\nsha256=%s\n' "$GODOT_VERSION" "$GODOT_SHA256"
+```
+
+Expected version: `4.7.1.stable.official.a13da4feb`. A different version or hash is not automatically rejected, but it requires a newly named evidence record and compatibility decision before runtime execution.
+
+- [ ] **Step 3: Add the v2 runtime test module and helpers**
+
+Create `tests/test_godot_live_editor_v2_runtime_pilot.py` with:
+
+```python
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import shutil
+import subprocess
+import tempfile
+import unittest
+from pathlib import Path
+
+from jsonschema import Draft202012Validator
+
+from tools.validate_godot_live_editor_contract import validate_operation_semantics
+
+ROOT = Path(__file__).resolve().parents[1]
+PILOT = ROOT / "examples/godot-live-editor-pilot"
+MANIFEST = PILOT / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
+MANIFEST_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
+OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
+CLI = PILOT / "tools/live_editor_cli.gd"
+PLUGIN_CFG = PILOT / "addons/base_live_editor_pilot/plugin.cfg"
+PLUGIN = PILOT / "addons/base_live_editor_pilot/plugin.gd"
+
+
+def load(path: Path) -> dict:
+    return json.loads(path.read_text(encoding="utf-8"))
+
+
+def sha256_file(path: Path) -> str:
+    digest = hashlib.sha256()
+    with path.open("rb") as handle:
+        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
+            digest.update(chunk)
+    return digest.hexdigest()
+```
+
+The test class `setUpClass` must read `GODOT_BIN`, verify that it is executable, and use `raise unittest.SkipTest("GODOT_BIN_NOT_CONFIGURED")` only when the variable is absent. An invalid configured path is a test failure, not a skip.
+
+- [ ] **Step 4: Add test-only RED requirements**
+
+Add these tests before implementation:
+
+```text
+test_fixture_manifest_validates_against_v2_schema
+test_read_only_commands_emit_v2_envelopes_and_valid_output
+test_approved_idempotent_mutation_binds_instance_snapshot_and_precondition
+test_stale_target_precondition_fails_before_state_write
+test_changed_catalog_or_output_schema_invalidates_approval
+test_output_schema_mismatch_cannot_report_success
+test_long_task_start_status_resume_uses_one_receiver_task_id
+test_terminal_task_result_binds_instance_snapshot_and_result_hash
+test_evidence_files_are_confined_and_hash_verified
+test_editor_plugin_lifecycle_emits_v2_hashed_evidence
+test_recovery_mode_disables_broken_plugin_and_rotates_instance_identity
+test_no_network_listener_or_production_bridge_exists
+```
+
+Each command invocation must parse exactly one JSON envelope from stdout, validate it with the operation v2 schema, then call `validate_operation_semantics(...)` with the fixture root.
+
+- [ ] **Step 5: Wire the test into required aggregate suites**
+
+Add:
+
+```python
+from tests.test_godot_live_editor_v2_runtime_pilot import (
+    GodotLiveEditorV2RuntimePilotTests as _GodotLiveEditorV2RuntimePilotTests,
+)
+```
+
+to both `tests/test_v9_machine_contracts.py` and `tests/test_local_validation.py`.
+
+- [ ] **Step 6: Run RED and commit tests only**
+
+Run:
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest tests.test_godot_live_editor_v2_runtime_pilot -v
+```
+
+Expected: failures caused by the legacy v1 manifest/envelopes, absent v2 target/snapshot/precondition/output fields, and missing recovery proof. Do not accept a RED caused only by a missing Godot binary.
+
+Commit:
+
+```bash
+git add tests/test_godot_live_editor_v2_runtime_pilot.py \
+  tests/test_v9_machine_contracts.py \
+  tests/test_local_validation.py
+git commit -m "test: define Godot v2 runtime Pilot contract"
+```
+
+---
+
+### Task 2: Migrate the fixture manifest and deterministic contract snapshot
+
+**Files:**
+- Modify: `examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
+- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+
+**Interfaces:**
+- Produces: `schema_version: 2`, `contract_version: 2.0.0`, exact v2 capability policies, closed input/output schemas, deterministic catalog/capability/output hashes, and a startup-generated automation instance ID.
+
+- [ ] **Step 1: Define the v2 Pilot capability policy table**
+
+Use these exact policies:
+
+```text
+doctor, status, catalog.compact, scene.inspect:
+  effect_kind = READ_ONLY
+  idempotency = NOT_APPLICABLE
+  approval_policy = NOT_REQUIRED
+  execution_mode = SYNCHRONOUS
+  rollback_policy = NOT_APPLICABLE
+  precondition_policy = NONE
+
+state.write_marker:
+  effect_kind = MUTATION
+  idempotency = IDEMPOTENT
+  approval_policy = REQUIRED
+  execution_mode = SYNCHRONOUS
+  rollback_policy = SNAPSHOT
+  precondition_policy = REQUIRED
+
+task.start, task.status, task.resume:
+  effect_kind = MUTATION
+  idempotency = IDEMPOTENT
+  approval_policy = REQUIRED
+  execution_mode = LONG_RUNNING_TASK
+  rollback_policy = SNAPSHOT
+  precondition_policy = REQUIRED
+```
+
+Add `task.status` as an explicit read/query capability only when the v2 semantic model permits a read-only long-task status query; otherwise keep `task.status` read-only and separate from mutation start/resume.
+
+- [ ] **Step 2: Add closed output schemas**
+
+Define a closed output schema for every capability. Minimum required outputs:
+
+```text
+doctor: project_fingerprint, automation_server_instance_id, catalog_sha256
+status: project_fingerprint, automation_server_instance_id, state_revision, dirty_state
+catalog.compact: catalog_sha256, capabilities[]
+scene.inspect: scene_path, root_name, root_type, target_revision, target_content_sha256
+state.write_marker: marker, state_revision, state_content_sha256, replayed
+task.start: task_id, state, created_at
+task.status: task_id, state, last_updated_at
+task.resume: task_id, state, result_hash
+```
+
+- [ ] **Step 3: Generate deterministic snapshot hashes**
+
+In the test harness, calculate:
+
+```python
+def canonical_sha256(value: object) -> str:
+    return hashlib.sha256(
+        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
+    ).hexdigest()
+```
+
+The checked-in manifest's `catalog.sha256`, each capability schema hash, and output schema hash must equal the canonical representation used by the CLI. Tests fail when hand-edited hashes drift.
+
+- [ ] **Step 4: Add service/Editor instance identity generation**
+
+The headless CLI must create one `automation_server_instance_id` at process/service startup and expose it through `doctor` and every envelope. The EditorPlugin must produce an `editor_instance_id` for its own startup session. Do not derive either identity solely from PID, port, path, or timestamp; generate a random UUID-like value and persist it only under the fixture artifact root for the process/session lifetime.
+
+- [ ] **Step 5: Validate the migrated manifest**
+
+Run:
+
+```bash
+python tools/validate_godot_live_editor_contract.py \
+  --manifest examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
+  --manifest-schema schemas/godot-live-editor-capability-manifest-v2.schema.json
+```
+
+Expected JSON: `{"valid": true, "issues": []}`.
+
+- [ ] **Step 6: Commit manifest/snapshot migration**
+
+```bash
+git add examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
+  examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "feat: migrate Godot Pilot manifest to v2"
+```
+
+---
+
+### Task 3: Migrate read-only envelopes and output validation
+
+**Files:**
+- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+
+**Interfaces:**
+- Consumes: manifest capability definitions and contract snapshot.
+- Produces: v2 read-only envelopes for `doctor`, `status`, `catalog.compact`, and `scene.inspect`.
+
+- [ ] **Step 1: Centralize v2 envelope construction**
+
+Add GDScript helpers with these responsibilities:
+
+```text
+build_project_identity()
+build_instance_identity(editor_instance_id = null, runtime_session_id = null)
+build_contract_snapshot(capability_id)
+build_policy(capability_id)
+build_preconditions_not_applicable()
+build_task_not_applicable()
+canonical_json(value)
+sha256_json(value)
+build_evidence(kind, state, relative_path, producer)
+build_operation_envelope(...)
+```
+
+Every envelope uses `schema_version: 2` and `artifact_role: GODOT_LIVE_EDITOR_OPERATION_ENVELOPE`.
+
+- [ ] **Step 2: Validate output before success**
+
+Implement a minimal closed-schema validator for the fixture's declared output schemas or route result data through a deterministic project-local validation helper. Unknown output keys, missing required keys, or wrong primitive types must return:
+
+```json
+{
+  "success": false,
+  "code": "OUTPUT_SCHEMA_MISMATCH"
+}
+```
+
+and must not emit PASS evidence.
+
+- [ ] **Step 3: Return observation preconditions**
+
+`status` and `scene.inspect` must return stable `target_revision`, `target_content_sha256`, and dirty-state facts that later mutation requests repeat. Use content-derived hashes, not only timestamps.
+
+- [ ] **Step 4: Run read-only runtime tests**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_read_only_commands_emit_v2_envelopes_and_valid_output \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_output_schema_mismatch_cannot_report_success \
+  -v
+```
+
+Expected: PASS with operation-schema and semantic-validator confirmation.
+
+- [ ] **Step 5: Commit read-only migration**
+
+```bash
+git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "feat: emit validated Godot v2 read-only envelopes"
+```
+
+---
+
+### Task 4: Implement v2 approved idempotent mutation and stale-state protection
+
+**Files:**
+- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+
+**Interfaces:**
+- Consumes: exact project/instance/snapshot/policy/precondition binding and approval expiry.
+- Produces: durable STARTED/COMPLETED/FAILED operation records, one state mutation per idempotency identity, and exact replay results.
+
+- [ ] **Step 1: Define canonical request identity**
+
+Calculate `request_hash` from exactly:
+
+```json
+{
+  "capability_id": "state.write_marker",
+  "arguments": {"marker": "..."},
+  "project_identity": {},
+  "instance_identity": {},
+  "contract_snapshot": {},
+  "policy": {},
+  "preconditions": {}
+}
+```
+
+Use sorted compact JSON and SHA-256. The CLI must recompute this value; never trust the client-provided hash.
+
+- [ ] **Step 2: Validate approval before durable mutation start**
+
+Reject with stable codes when any binding differs:
+
+```text
+APPROVAL_REQUIRED
+APPROVAL_EXPIRED
+PROJECT_IDENTITY_MISMATCH
+AUTOMATION_INSTANCE_MISMATCH
+CONTRACT_SNAPSHOT_MISMATCH
+APPROVAL_TOKEN_MISMATCH
+```
+
+Token consumption and a STARTED ledger record must be written atomically before the marker state changes.
+
+- [ ] **Step 3: Enforce preconditions**
+
+Before writing, compare requested `target_revision`, `target_content_sha256`, and expected dirty state to current state. On mismatch return `TARGET_STATE_CONFLICT`, write no state mutation, and do not consume approval for a mutation that never started.
+
+- [ ] **Step 4: Preserve exact idempotent replay**
+
+The same idempotency key plus same canonical request identity returns the previously stored terminal result with `replayed: true`. The same key with changed target, snapshot, policy, preconditions, or arguments returns `IDEMPOTENCY_KEY_CONFLICT`.
+
+- [ ] **Step 5: Hash mutation evidence and result**
+
+Write the bounded state and ledger files, hash the final bytes, create evidence entries with relative paths and hashes, validate `result.data`, and calculate the terminal `result_hash`. The semantic validator must accept the completed envelope.
+
+- [ ] **Step 6: Run mutation adversarial tests**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_approved_idempotent_mutation_binds_instance_snapshot_and_precondition \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_stale_target_precondition_fails_before_state_write \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_changed_catalog_or_output_schema_invalidates_approval \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_evidence_files_are_confined_and_hash_verified \
+  -v
+```
+
+- [ ] **Step 7: Commit mutation migration**
+
+```bash
+git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "feat: enforce Godot v2 mutation bindings"
+```
+
+---
+
+### Task 5: Implement the generic v2 task lifecycle
+
+**Files:**
+- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+
+**Interfaces:**
+- Produces: receiver-generated `task_id`, `QUEUED/RUNNING/PENDING/COMPLETED/FAILED/CANCELLED/STALE` records, status query, exact result binding, TTL and poll interval metadata.
+
+- [ ] **Step 1: Persist one task before returning**
+
+`task.start` validates approval and preconditions, creates one receiver-generated task ID, writes a durable task record with:
+
+```json
+{
+  "task_id": "...",
+  "state": "PENDING",
+  "created_at": "...",
+  "last_updated_at": "...",
+  "ttl_ms": 3600000,
+  "poll_interval_ms": 250,
+  "cancellation_policy": "SAFE_BEFORE_COMMIT",
+  "result_binding": null
+}
+```
+
+and returns `TASK_PENDING`.
+
+- [ ] **Step 2: Add status without hidden mutation**
+
+`task.status` is read-only. It verifies project/server/snapshot identity and returns the stored state. It must not advance or complete the task.
+
+- [ ] **Step 3: Resume the same task**
+
+`task.resume` requires the original task ID, active server instance, matching contract snapshot, matching operation lineage, and renewed approval when the approved request scope requires continuation. A different instance or snapshot returns `TASK_RESULT_STALE` or `AUTOMATION_INSTANCE_MISMATCH`.
+
+- [ ] **Step 4: Bind terminal result**
+
+On completion, set `last_updated_at`, `state: COMPLETED`, and a result binding containing project identity, instance identity, contract snapshot, capability, operation, task ID, and result hash. A terminal state without exact binding is invalid.
+
+- [ ] **Step 5: Prove start-once and replay**
+
+Repeated start with the same idempotency identity returns the same task ID. A conflicting start never creates a second task.
+
+- [ ] **Step 6: Run task runtime tests**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_long_task_start_status_resume_uses_one_receiver_task_id \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_terminal_task_result_binds_instance_snapshot_and_result_hash \
+  -v
+```
+
+- [ ] **Step 7: Commit task migration**
+
+```bash
+git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "feat: migrate Godot Pilot tasks to v2"
+```
+
+---
+
+### Task 6: Prove EditorPlugin lifecycle and recovery-mode behavior
+
+**Files:**
+- Modify: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.gd`
+- Modify: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.cfg`
+- Modify: `examples/godot-live-editor-pilot/project.godot`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+
+**Interfaces:**
+- Produces: hashed Editor lifecycle evidence with one `editor_instance_id`; a deterministic broken-plugin fixture; verified recovery-mode disable and normal restart.
+
+- [ ] **Step 1: Emit v2 Editor lifecycle evidence**
+
+On `_enter_tree`, generate an `editor_instance_id` and write a confined lifecycle record containing project fingerprint, automation server instance ID when supplied, Editor instance ID, Godot version, plugin version, `network_listener_enabled: false`, generated time, and producer identity. Hash the record and expose the hash to the test harness.
+
+- [ ] **Step 2: Add an intentionally broken test-only plugin state**
+
+The test must create the broken state in a temporary copy of the fixture or through a test-only marker under `artifacts/`; do not commit a permanently broken plugin. Normal editor startup must fail or report the controlled plugin failure.
+
+- [ ] **Step 3: Invoke recovery mode explicitly**
+
+Run:
+
+```bash
+"$GODOT_BIN" --headless --editor --recovery-mode --path examples/godot-live-editor-pilot --quit
+```
+
+The recovery workflow disables/removes only the fixture-local plugin registration, records `BLOCKED_RECOVERY`, and does not modify files outside the fixture.
+
+- [ ] **Step 4: Rotate identity and require renewed approval**
+
+After recovery, normal Editor startup generates a new `editor_instance_id` and automation server instance ID. A pre-recovery approval token must fail on the new instance.
+
+- [ ] **Step 5: Re-enable and verify normal startup**
+
+Restore the declared plugin configuration from a bounded snapshot, run normal headless Editor startup, and verify the new lifecycle evidence and no-network marker.
+
+- [ ] **Step 6: Run lifecycle/recovery tests**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_editor_plugin_lifecycle_emits_v2_hashed_evidence \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_recovery_mode_disables_broken_plugin_and_rotates_instance_identity \
+  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_no_network_listener_or_production_bridge_exists \
+  -v
+```
+
+- [ ] **Step 7: Commit lifecycle/recovery proof**
+
+```bash
+git add examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.gd \
+  examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.cfg \
+  examples/godot-live-editor-pilot/project.godot \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "test: prove Godot v2 Editor recovery lifecycle"
+```
+
+---
+
+### Task 7: Regenerate versioned runtime evidence
+
+**Files:**
+- Create: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot-v2.md`
+- Create: `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE_V2.json`
+- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
+- Preserve: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md`
+- Preserve: historical `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json` until final v1 deletion commit
+
+**Interfaces:**
+- Consumes: actual command outputs/logs from Tasks 2–6.
+- Produces: exact binary/version/command/test/envelope/evidence hashes and honest NOT_RUN boundaries.
+
+- [ ] **Step 1: Capture exact runtime command inventory**
+
+Record each executed command as an argument array, working directory relative to repo root, exit code, stdout/stderr artifact hash, and execution time. Redact absolute temporary paths and environment secrets.
+
+- [ ] **Step 2: Generate the v2 evidence JSON from results**
+
+Require:
+
+```json
+{
+  "schema_version": 2,
+  "artifact_role": "GODOT_LIVE_EDITOR_RUNTIME_EVIDENCE",
+  "engine_version": "4.7.1.stable.official.a13da4feb",
+  "engine_executable_sha256": "...",
+  "contract_version": "2.0.0",
+  "manifest_sha256": "...",
+  "operation_schema_sha256": "...",
+  "semantic_validator_sha256": "...",
+  "test_result": {"passed": 0, "failed": 0, "skipped": 0},
+  "captured_envelopes": [],
+  "evidence_files": [],
+  "limits": {}
+}
+```
+
+Every referenced artifact uses a repository-relative placeholder/path and SHA-256. Do not commit ephemeral artifact payloads unless the approved evidence policy explicitly requires them.
+
+- [ ] **Step 3: Write the human-readable evidence report**
+
+Separate:
+
+```yaml
+static_v2_contract: PASS
+actual_godot_cli: PASS_or_FAIL
+actual_editor_plugin_lifecycle: PASS_or_FAIL
+recovery_mode: PASS_or_FAIL
+original_user_projects_runtime: NOT_RUN
+production_network_mcp: NOT_IMPLEMENTED
+runtime_debugger_bridge: NOT_IMPLEMENTED
+project_test_framework: NOT_CONFIGURED
+physical_input: NOT_RUN
+human_usability: HUMAN_NOT_RUN
+production_adapter_ready: false
+```
+
+- [ ] **Step 4: Add evidence consistency tests**
+
+Verify version/hash fields, captured-envelope count, result/evidence hashes, no absolute paths, no secret-like keys, and agreement between JSON and Markdown claims.
+
+- [ ] **Step 5: Run the full actual runtime suite**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest tests.test_godot_live_editor_v2_runtime_pilot -v
+```
+
+Expected: all configured cases pass with no runtime skip. Skips for original user projects, physical input, and human usability remain state fields, not skipped test cases in the isolated Pilot suite.
+
+- [ ] **Step 6: Commit v2 evidence**
+
+```bash
+git add docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot-v2.md \
+  examples/godot-live-editor-pilot/RUNTIME_EVIDENCE_V2.json \
+  tests/test_godot_live_editor_v2_runtime_pilot.py
+git commit -m "docs: record Godot v2 runtime Pilot evidence"
+```
+
+---
+
+### Task 8: Retire v1 compatibility after v2 runtime GREEN
+
+**Files:**
+- Delete: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
+- Delete: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
+- Delete: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
+- Delete: `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json`
+- Modify or remove: `tests/test_godot_live_editor_runtime_contract_hardening.py`
+- Modify or remove: `tests/test_godot_live_editor_runtime_pilot.py`
+- Modify: `tests/test_v9_machine_contracts.py`
+- Modify: `tests/test_local_validation.py`
+- Modify: Pilot v1 design/plan/evidence documents to point to the archived Git commit and v2 replacement without remaining active v1 paths
+
+**Interfaces:**
+- v2 becomes the only repository schema and runtime Pilot authority.
+- Historical v1 proof remains recoverable through Git history and the merged main commit `83683eecaaeaf415bf629fe5a1231fc6cef575f3`.
+
+- [ ] **Step 1: Verify the deletion gate**
+
+Run the actual v2 runtime suite, semantic validator, focused static suites, and evidence consistency tests immediately before deletion. Stop if any configured runtime test fails or is skipped.
+
+- [ ] **Step 2: Migrate useful legacy assertions**
+
+Move still-relevant no-network, readiness-boundary, and path-confinement assertions into `tests/test_godot_live_editor_v2_runtime_pilot.py`. Do not preserve duplicate test modules solely for history.
+
+- [ ] **Step 3: Delete v1 active files**
+
+Delete the two v1 schemas, legacy compatibility document, old runtime evidence JSON, and obsolete v1-only tests. Update aggregate suite imports in the same commit so required CI remains importable.
+
+- [ ] **Step 4: Preserve history references without active authority**
+
+Update historical v1 Markdown documents to say:
+
+```yaml
+historical_commit: 83683eecaaeaf415bf629fe5a1231fc6cef575f3
+superseded_by: GODOT_LIVE_EDITOR_RUNTIME_EVIDENCE v2
+active_schema_version: 2
+```
+
+Do not leave links to deleted files as current instructions.
+
+- [ ] **Step 5: Prove no active v1 reference remains**
+
+Run:
+
+```bash
+git grep -nE 'godot-live-editor-(capability-manifest|operation-envelope)-v1|"schema_version"[[:space:]]*:[[:space:]]*1' -- \
+  ':!docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md' \
+  ':!docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md'
+```
+
+Expected: no active code/template/schema/test match. Historical prose may mention the version name but must not present a usable active path.
+
+- [ ] **Step 6: Commit v1 retirement atomically**
+
+```bash
+git add -A schemas docs/knowledge/godot examples/godot-live-editor-pilot tests
+git commit -m "refactor: retire Godot live-editor contract v1"
+```
+
+---
+
+### Task 9: Full verification, adversarial review, and Draft PR evidence
+
+**Files:**
+- Modify only reproducible findings.
+- Update the Draft runtime-migration PR body after verification.
+
+**Interfaces:**
+- Produces: exact-head runtime evidence, repository regression evidence, current-main merge-ref evidence, and zero unresolved MUST_FIX findings.
+
+- [ ] **Step 1: Run all focused and aggregate tests**
+
+```bash
+GODOT_BIN="$GODOT_BIN" python -m unittest \
+  tests.test_godot_live_editor_contract \
+  tests.test_godot_live_editor_contract_v2 \
+  tests.test_godot_live_editor_idempotent_approval \
+  tests.test_godot_live_editor_v2_runtime_pilot \
+  tests.test_v9_machine_contracts \
+  tests.test_local_validation \
+  -v
+
+python -m unittest \
+  tests.test_reference_freshness \
+  tests.test_skill_routing_governance \
+  tests.test_skill_package_integrity \
+  tests.test_skill_system_coverage \
+  -v
+```
+
+- [ ] **Step 2: Verify repository integrity and absence of generated leakage**
+
+```bash
+git diff --check main...HEAD
+git diff --name-status main...HEAD
+git diff --exit-code main...HEAD -- skills/SKILL_REGISTRY.json
+git diff --exit-code main...HEAD -- 'release/**' 'docs/releases/**'
+git ls-files | grep -E '(^|/)(\.godot|artifacts)/|Godot.*(zip|tar|exe)$' && exit 1 || true
+```
+
+- [ ] **Step 3: Run the final adversarial attack set**
+
+Require fail-closed behavior for:
+
+```text
+wrong project/server/Editor/runtime identity
+stale catalog, capability input schema, or output schema hash
+approval expiry and cross-operation token reuse
+same idempotency key with changed arguments/preconditions
+mutation before STARTED ledger persistence
+stale revision/hash and unexpected dirty state
+output mismatch promoted to success
+result/evidence hash tampering
+path traversal, absolute path, and symlink escape
+duplicate task start and stale task result replay
+recovery using a pre-recovery approval
+network listener or production bridge leakage
+v1 schema/reference resurrection
+runtime/human readiness overclaim
+```
+
+- [ ] **Step 4: Request independent review with exact evidence**
+
+Provide the reviewer the current base/head SHAs, changed files, approved spec/BCP, exact Godot version/hash, RED/GREEN heads, test output, runtime evidence hashes, known limits, and rollback. Fix all confirmed Critical/Important findings.
+
+- [ ] **Step 5: Re-fetch main and test the current merge ref**
+
+When main moved, create and test a fresh merge ref. Require all triggered required workflows and `ci-gate` to succeed on the current relationship. Do not reuse old PR #152 or Stage A CI as Stage B evidence.
+
+- [ ] **Step 6: Update the Draft PR without merging**
+
+Report:
+
+```yaml
+active_contract_version: 2.0.0
+v1_repository_authority: REMOVED
+godot_binary_version: exact value
+godot_binary_sha256: exact value
+v2_cli_runtime: PASS
+v2_editor_plugin_lifecycle: PASS
+v2_recovery_mode: PASS
+semantic_validator: PASS
+repository_regressions: PASS
+original_user_projects_runtime: NOT_RUN
+production_network_mcp: NOT_IMPLEMENTED
+runtime_debugger_bridge: NOT_IMPLEMENTED
+project_test_framework: NOT_CONFIGURED
+physical_input: NOT_RUN
+human_usability: HUMAN_NOT_RUN
+production_adapter_ready: false
+registry_release_locks: UNCHANGED
+merge: NOT_AUTHORIZED
+```
+
+---
+
+## Completion Gate
+
+Stage B is complete only when:
+
+```yaml
+static_v2_stage_merged: true
+actual_godot_binary_verified: true
+test_only_red_recorded: true
+fixture_manifest_v2: true
+read_only_v2_runtime_green: true
+approved_idempotent_mutation_v2_green: true
+stale_precondition_rejection_green: true
+output_validation_green: true
+generic_task_lifecycle_green: true
+editor_lifecycle_green: true
+recovery_mode_green: true
+v2_evidence_hashes_verified: true
+v1_active_files_removed: true
+repository_regressions_green: true
+current_merge_ref_ci: PASS
+unresolved_must_fix: 0
+unresolved_review_threads: 0
+registry_release_locks_unchanged: true
+production_adapter_ready: false
+```
+
+The PR remains Draft until the user separately authorizes merge. Passing this isolated Pilot does not authorize production MCP transport or adoption in a user game project.
