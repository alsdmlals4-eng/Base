# Godot Live Editor v2 Runtime Pilot Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development`, `superpowers:requesting-code-review`, and `superpowers:verification-before-completion`. Use checkbox (`- [ ]`) steps for progress tracking.

**Goal:** Migrate the isolated Godot 4.7.1 Pilot from legacy contract v1 to active contract v2, execute the real Godot binary, regenerate trustworthy evidence, and remove the temporary v1 compatibility surface.

**Architecture:** Preserve the self-contained no-network fixture, but migrate its manifest, envelopes, request normalization, approval binding, task ledger, output validation, evidence hashing, and recovery proof to v2. Run against an exact Godot executable hash. Archive historical v1 evidence and delete v1 schemas only after v2 runtime and repository regressions pass on the same exact head.

**Tech Stack:** Godot `4.7.1.stable.official.a13da4feb`, GDScript, JSON, JSON Schema Draft 2020-12, Python 3.12 `unittest`, `jsonschema==4.26.0`, SHA-256 evidence, existing Base GitHub Actions.

## Global constraints

- Do not begin until Stage A static v2 is merged to main and records `active_contract_template_adapter_v2: true`, `v1_new_adoption_prohibited: true`, and `current_merge_ref_ci: PASS`.
- Re-fetch main and create a fresh isolated branch/worktree. Never implement on either planning branch or the Stage A branch.
- Require an explicit executable path through `GODOT_BIN`. Do not guess a binary from PATH or workspace contents.
- Run `GODOT_BIN --version` and calculate SHA-256 before changing any runtime status.
- Historical executable SHA-256 is `32f8d7596c4b41185512b1c49d69f2da3be018fd784a53e349fa92a98a97bcde`. A different binary requires a newly versioned evidence record; never silently rewrite historical identity.
- Never commit the Godot executable/archive, export templates, `.godot/`, generated UID files, runtime artifact payloads, secrets, absolute sandbox paths, or user project configurations.
- Keep fixture writes under `examples/godot-live-editor-pilot/artifacts/`; reject absolute paths, `..`, missing confinement, and symlink escape.
- No listening socket, remote endpoint, production MCP server, arbitrary shell/script/eval, unrestricted property path, or production runtime bridge.
- EditorPlugin work proves lifecycle and recovery only. It does not prove production main-thread queue, Undo/Redo integration, runtime debugger, project tests, physical input, or human usability.
- Use TDD with a test-only RED commit before changing Pilot implementation.
- Do not delete v1 schemas or compatibility docs until actual Godot v2 runtime tests and static tests pass on the same exact head.
- Preserve Skill Registry and released/frozen Base identities byte-for-byte.

---

## Task 1: Preflight static v2 authority and actual Godot binary

**Files:**

- Read only: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Read only: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Read only: `tools/validate_godot_live_editor_contract.py`
- Read only: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
- Create: `tests/test_godot_live_editor_v2_runtime_pilot.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `tests/test_local_validation.py`

- [ ] **Step 1: Verify Stage A authority**

```bash
python - <<'PY'
import json
from pathlib import Path

manifest_schema = json.loads(
    Path('schemas/godot-live-editor-capability-manifest-v2.schema.json').read_text(encoding='utf-8')
)
operation_schema = json.loads(
    Path('schemas/godot-live-editor-operation-envelope-v2.schema.json').read_text(encoding='utf-8')
)
template = json.loads(
    Path('templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json').read_text(encoding='utf-8')
)
assert manifest_schema['properties']['schema_version']['const'] == 2
assert operation_schema['properties']['schema_version']['const'] == 2
assert template['schema_version'] == 2
assert template['contract_version'] == '2.0.0'
assert Path('tools/validate_godot_live_editor_contract.py').is_file()
assert Path('docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md').is_file()
print('STATIC_V2_AUTHORITY_PASS')
PY
```

- [ ] **Step 2: Verify engine identity**

```bash
test -n "${GODOT_BIN:-}"
test -x "$GODOT_BIN"
GODOT_VERSION="$($GODOT_BIN --version | tr -d '\r')"
GODOT_SHA256="$(sha256sum "$GODOT_BIN" | awk '{print $1}')"
printf 'version=%s\nsha256=%s\n' "$GODOT_VERSION" "$GODOT_SHA256"
```

Expected version is `4.7.1.stable.official.a13da4feb`. A version/hash difference requires an explicit compatibility decision and a new evidence filename before continuing.

- [ ] **Step 3: Create runtime test helpers**

Create `tests/test_godot_live_editor_v2_runtime_pilot.py` with:

```python
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.validate_godot_live_editor_contract import validate_operation_semantics

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / 'examples/godot-live-editor-pilot'
MANIFEST = PILOT / 'GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json'
MANIFEST_SCHEMA = ROOT / 'schemas/godot-live-editor-capability-manifest-v2.schema.json'
OPERATION_SCHEMA = ROOT / 'schemas/godot-live-editor-operation-envelope-v2.schema.json'
CLI = PILOT / 'tools/live_editor_cli.gd'
PLUGIN = PILOT / 'addons/base_live_editor_pilot/plugin.gd'


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()
```

`setUpClass` reads `GODOT_BIN`. Absence causes `SkipTest('GODOT_BIN_NOT_CONFIGURED')`; an explicitly configured invalid path is a failure.

- [ ] **Step 4: Add test-only RED cases**

```text
test_fixture_manifest_validates_against_v2_schema
test_read_only_commands_emit_v2_envelopes_and_valid_output
test_approved_idempotent_mutation_binds_instance_snapshot_and_precondition
test_stale_target_precondition_fails_before_state_write
test_changed_catalog_or_output_schema_invalidates_approval
test_output_schema_mismatch_cannot_report_success
test_long_task_start_status_resume_uses_one_receiver_task_id
test_terminal_task_result_binds_instance_snapshot_and_result_hash
test_evidence_files_are_confined_and_hash_verified
test_editor_plugin_lifecycle_emits_v2_hashed_evidence
test_recovery_mode_disables_broken_plugin_and_rotates_instance_identity
test_no_network_listener_or_production_bridge_exists
```

Each command parses exactly one JSON envelope, validates the operation schema, then runs `validate_operation_semantics(...)` with the fixture root.

- [ ] **Step 5: Connect tests to required aggregate suites**

```python
from tests.test_godot_live_editor_v2_runtime_pilot import (
    GodotLiveEditorV2RuntimePilotTests as _GodotLiveEditorV2RuntimePilotTests,
)
```

Add to `tests/test_v9_machine_contracts.py` and `tests/test_local_validation.py`.

- [ ] **Step 6: Run and commit genuine RED**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot -v
```

RED must come from legacy v1 manifest/envelopes and missing v2 behavior, not from a missing engine.

```bash
git add tests/test_godot_live_editor_v2_runtime_pilot.py \
  tests/test_v9_machine_contracts.py \
  tests/test_local_validation.py
git commit -m 'test: define Godot v2 runtime Pilot contract'
```

---

## Task 2: Migrate fixture manifest and deterministic contract snapshot

**Files:**

- Modify: `examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`

- [ ] **Step 1: Apply exact v2 capability policies**

```text
doctor, status, catalog.compact, scene.inspect:
  READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + SYNCHRONOUS + NOT_APPLICABLE

state.write_marker:
  MUTATION + IDEMPOTENT + REQUIRED + SYNCHRONOUS + SNAPSHOT

long task start/resume:
  MUTATION + IDEMPOTENT + REQUIRED + LONG_RUNNING_TASK + SNAPSHOT

task.status:
  READ_ONLY + NOT_APPLICABLE + NOT_REQUIRED + SYNCHRONOUS + NOT_APPLICABLE
```

Use `precondition_policy: REQUIRED` for mutation and `NONE` for read-only/status query.

- [ ] **Step 2: Add closed output schemas**

Minimum output fields:

```text
doctor: project_fingerprint, automation_server_instance_id, catalog_sha256
status: project_fingerprint, automation_server_instance_id, state_revision, dirty_state
catalog.compact: catalog_sha256, capabilities
scene.inspect: scene_path, root_name, root_type, target_revision, target_content_sha256
state.write_marker: marker, state_revision, state_content_sha256, replayed
task.start: task_id, state, created_at
task.status: task_id, state, last_updated_at
task.resume: task_id, state, result_hash
```

- [ ] **Step 3: Generate deterministic schema/catalog hashes**

Use compact sorted JSON SHA-256 in both Python tests and GDScript. Checked-in `catalog.sha256`, capability input schema hash, and output schema hash must match the same canonical representation.

- [ ] **Step 4: Generate instance identity**

The CLI/service generates `automation_server_instance_id`; the EditorPlugin generates `editor_instance_id`. Use random UUID-like identities persisted only within the fixture artifact root for the session lifetime. PID, port, path, title, and timestamp are insufficient as sole identity.

- [ ] **Step 5: Validate manifest and commit**

```bash
python tools/validate_godot_live_editor_contract.py \
  --manifest examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
  --manifest-schema schemas/godot-live-editor-capability-manifest-v2.schema.json
```

Expected: `valid: true`, no issues.

```bash
git add examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
  examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'feat: migrate Godot Pilot manifest to v2'
```

---

## Task 3: Migrate read-only envelopes and structured output validation

**Files:**

- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`

- [ ] **Step 1: Centralize v2 envelope construction**

Provide helpers for project identity, instance identity, contract snapshot, capability policy, preconditions, task state, canonical JSON/SHA-256, evidence, and final operation envelope. Every envelope uses schema version 2.

- [ ] **Step 2: Validate output before success**

Unknown output keys, missing required fields, or wrong types return `OUTPUT_SCHEMA_MISMATCH`. They emit no PASS evidence and cannot promote a task to terminal success.

- [ ] **Step 3: Return stable observation preconditions**

`status` and `scene.inspect` return content-derived `target_revision`, `target_content_sha256`, and dirty-state facts for later mutation preconditions.

- [ ] **Step 4: Run focused runtime tests**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_read_only_commands_emit_v2_envelopes_and_valid_output \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_output_schema_mismatch_cannot_report_success \
  -v
```

- [ ] **Step 5: Commit**

```bash
git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'feat: emit validated Godot v2 read-only envelopes'
```

---

## Task 4: Implement approved idempotent mutation and stale-state protection

**Files:**

- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`

- [ ] **Step 1: Recompute canonical request identity**

Hash exactly:

```json
{
  "capability_id": "state.write_marker",
  "arguments": {},
  "project_identity": {},
  "instance_identity": {},
  "contract_snapshot": {},
  "policy": {},
  "preconditions": {}
}
```

Never trust a client-provided request hash without recomputation.

- [ ] **Step 2: Validate approval before durable start**

Reject mismatched/expired approval with stable codes. Approval must bind project, server/Editor target, complete snapshot, policy, request hash, and preconditions. Record token consumption and STARTED ledger atomically before state mutation.

- [ ] **Step 3: Enforce preconditions**

Compare requested revision, content hash, and expected dirty state to current state. `TARGET_STATE_CONFLICT` writes no marker and does not consume an approval for a mutation that never began.

- [ ] **Step 4: Preserve exact idempotent replay**

Same key and canonical request return the stored result with `replayed: true`. Same key with changed arguments, target, snapshot, policy, or preconditions returns `IDEMPOTENCY_KEY_CONFLICT`.

- [ ] **Step 5: Hash state, evidence, and result**

All successful file-backed evidence has a confined relative path and SHA-256. Validate output before calculating terminal result hash.

- [ ] **Step 6: Run adversarial mutation tests**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_approved_idempotent_mutation_binds_instance_snapshot_and_precondition \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_stale_target_precondition_fails_before_state_write \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_changed_catalog_or_output_schema_invalidates_approval \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_evidence_files_are_confined_and_hash_verified \
  -v
```

- [ ] **Step 7: Commit**

```bash
git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'feat: enforce Godot v2 mutation bindings'
```

---

## Task 5: Implement generic v2 task lifecycle

**Files:**

- Modify: `examples/godot-live-editor-pilot/tools/live_editor_cli.gd`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`

- [ ] **Step 1: Persist one receiver-generated task before response**

`task.start` creates one durable task with state, timestamps, TTL, polling interval, cancellation policy, and null result binding before returning `TASK_PENDING`.

- [ ] **Step 2: Keep status read-only**

`task.status` verifies project/server/snapshot identity and returns state without advancing the task.

- [ ] **Step 3: Resume the same task only**

`task.resume` requires matching task ID, operation lineage, server instance, contract snapshot, and renewed approval when continuation changes approved scope. Wrong target/snapshot fails with `TASK_RESULT_STALE` or identity mismatch.

- [ ] **Step 4: Bind terminal result**

Terminal result binding contains project/instance identity, snapshot, capability, operation, task ID, and result hash. Terminal state without exact binding is invalid.

- [ ] **Step 5: Prove start-once behavior**

Repeated identical start returns the same task ID. Conflicting start creates no second task.

- [ ] **Step 6: Run focused task tests**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_long_task_start_status_resume_uses_one_receiver_task_id \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_terminal_task_result_binds_instance_snapshot_and_result_hash \
  -v
```

- [ ] **Step 7: Commit**

```bash
git add examples/godot-live-editor-pilot/tools/live_editor_cli.gd \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'feat: migrate Godot Pilot tasks to v2'
```

---

## Task 6: Prove EditorPlugin lifecycle and recovery-mode behavior

**Files:**

- Modify: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.gd`
- Modify: `examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.cfg`
- Modify: `examples/godot-live-editor-pilot/project.godot`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`

- [ ] **Step 1: Emit hashed lifecycle evidence**

On `_enter_tree`, write a confined record with project fingerprint, server identity when supplied, new Editor identity, Godot version, plugin version, `network_listener_enabled: false`, timestamp, producer, and artifact hash.

- [ ] **Step 2: Create a temporary controlled plugin failure**

Use a temporary fixture copy or artifact-root test marker. Never commit a permanently broken plugin.

- [ ] **Step 3: Invoke official recovery mode**

```bash
"$GODOT_BIN" --headless --editor --recovery-mode \
  --path examples/godot-live-editor-pilot --quit
```

Disable/remove only fixture-local plugin registration, record `BLOCKED_RECOVERY`, and remain inside the fixture.

- [ ] **Step 4: Rotate instance identity and approval**

After recovery, normal startup creates new server/Editor identities. Pre-recovery approval must fail.

- [ ] **Step 5: Restore and verify normal startup**

Restore declared plugin configuration from a bounded snapshot and verify normal headless Editor startup and new no-network lifecycle evidence.

- [ ] **Step 6: Run recovery tests**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_editor_plugin_lifecycle_emits_v2_hashed_evidence \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_recovery_mode_disables_broken_plugin_and_rotates_instance_identity \
  tests.test_godot_live_editor_v2_runtime_pilot.GodotLiveEditorV2RuntimePilotTests.test_no_network_listener_or_production_bridge_exists \
  -v
```

- [ ] **Step 7: Commit**

```bash
git add examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.gd \
  examples/godot-live-editor-pilot/addons/base_live_editor_pilot/plugin.cfg \
  examples/godot-live-editor-pilot/project.godot \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'test: prove Godot v2 Editor recovery lifecycle'
```

---

## Task 7: Generate versioned v2 runtime evidence

**Files:**

- Create: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot-v2.md`
- Create: `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE_V2.json`
- Modify: `tests/test_godot_live_editor_v2_runtime_pilot.py`
- Preserve until retirement: historical v1 evidence files

- [ ] **Step 1: Capture exact command inventory**

Record argument arrays, repo-relative working directory, exit code, stdout/stderr artifact hash, and execution time. Redact absolute temporary paths and secrets.

- [ ] **Step 2: Generate v2 evidence JSON**

Require exact engine version/hash, contract/manifest/schema/validator hashes, test counts, captured envelope hashes, evidence file hashes, and explicit limits.

- [ ] **Step 3: Write human-readable evidence**

Separate actual runtime states from NOT_RUN/NOT_IMPLEMENTED boundaries:

```yaml
static_v2_contract: PASS
actual_godot_cli: PASS_or_FAIL
actual_editor_plugin_lifecycle: PASS_or_FAIL
recovery_mode: PASS_or_FAIL
original_user_projects_runtime: NOT_RUN
production_network_mcp: NOT_IMPLEMENTED
runtime_debugger_bridge: NOT_IMPLEMENTED
project_test_framework: NOT_CONFIGURED
physical_input: NOT_RUN
human_usability: HUMAN_NOT_RUN
production_adapter_ready: false
```

- [ ] **Step 4: Add consistency tests**

Verify hashes, captured-envelope count, no absolute paths, no secret-like keys, and agreement between JSON and Markdown claims.

- [ ] **Step 5: Run full configured runtime suite**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_v2_runtime_pilot -v
```

Configured isolated-Pilot cases must not skip. Original user projects, physical input, and human usability remain evidence states rather than Pilot test skips.

- [ ] **Step 6: Commit evidence**

```bash
git add docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot-v2.md \
  examples/godot-live-editor-pilot/RUNTIME_EVIDENCE_V2.json \
  tests/test_godot_live_editor_v2_runtime_pilot.py
git commit -m 'docs: record Godot v2 runtime Pilot evidence'
```

---

## Task 8: Retire v1 compatibility after v2 runtime GREEN

**Files:**

- Delete: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Delete: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Delete: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
- Delete: old v1 Pilot evidence JSON after v2 replacement is verified
- Migrate/remove: `tests/test_godot_live_editor_runtime_contract_hardening.py`
- Migrate/remove: `tests/test_godot_live_editor_runtime_pilot.py`
- Modify aggregate test imports and historical Pilot documents

- [ ] **Step 1: Verify deletion gate**

Immediately rerun configured v2 runtime, semantic, static, and evidence tests. Stop if any configured case fails or skips.

- [ ] **Step 2: Move useful legacy assertions**

Preserve no-network, readiness-boundary, path-confinement, and evidence-honesty assertions in the v2 test module. Do not keep duplicate modules only for history.

- [ ] **Step 3: Delete v1 authority atomically**

Delete v1 schemas, compatibility doc, obsolete v1 test modules, and replaced v1 evidence. Update aggregate imports in the same commit.

- [ ] **Step 4: Preserve historical traceability**

Historical Markdown points to merged commit `83683eecaaeaf415bf629fe5a1231fc6cef575f3` and the v2 replacement, without presenting deleted v1 paths as current instructions.

- [ ] **Step 5: Prove no active v1 reference remains**

```bash
git grep -nE \
  'godot-live-editor-(capability-manifest|operation-envelope)-v1|"schema_version"[[:space:]]*:[[:space:]]*1' \
  -- ':!docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md' \
     ':!docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md'
```

Expected: no active code/template/schema/test match. Historical prose may name v1 but not provide active authority paths.

- [ ] **Step 6: Commit retirement**

```bash
git add -A schemas docs/knowledge/godot examples/godot-live-editor-pilot tests
git commit -m 'refactor: retire Godot live-editor contract v1'
```

---

## Task 9: Full verification and adversarial review

- [ ] **Step 1: Run focused and aggregate suites**

```bash
GODOT_BIN="$GODOT_BIN" python -m unittest \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_idempotent_approval \
  tests.test_godot_live_editor_v2_runtime_pilot \
  tests.test_v9_machine_contracts \
  tests.test_local_validation \
  -v

python -m unittest \
  tests.test_reference_freshness \
  tests.test_skill_routing_governance \
  tests.test_skill_package_integrity \
  tests.test_skill_system_coverage \
  -v
```

- [ ] **Step 2: Verify repository integrity**

```bash
git diff --check main...HEAD
git diff --name-status main...HEAD
git diff --exit-code main...HEAD -- skills/SKILL_REGISTRY.json
git diff --exit-code main...HEAD -- 'release/**' 'docs/releases/**'
git ls-files | grep -E '(^|/)(\.godot|artifacts)/|Godot.*(zip|tar|exe)$' && exit 1 || true
```

- [ ] **Step 3: Run final adversarial attacks**

Require fail-closed behavior for:

```text
wrong project/server/Editor/runtime identity
stale catalog/input/output schema hash
approval expiry and cross-operation token reuse
same idempotency key with changed arguments/preconditions
mutation before STARTED ledger persistence
stale revision/hash and unexpected dirty state
output mismatch promoted to success
result/evidence hash tampering
path traversal, absolute path, symlink escape
duplicate task start and stale task result replay
pre-recovery approval after identity rotation
network listener or production bridge leakage
v1 schema/reference resurrection
runtime/human readiness overclaim
```

- [ ] **Step 4: Request independent review**

Provide exact base/head, approved spec/BCP, Godot version/hash, RED/GREEN heads, changed files, test output, evidence hashes, known limits, and rollback. Fix every confirmed Critical/Important issue.

- [ ] **Step 5: Verify fresh main merge ref and GitHub Actions**

Re-fetch main. When it moved, test a fresh merge ref. Require all triggered required workflows and `ci-gate` to pass. Old PR #152 or Stage A CI is not Stage B evidence.

- [ ] **Step 6: Update Draft PR without merging**

```yaml
active_contract_version: 2.0.0
v1_repository_authority: REMOVED
godot_binary_version: exact value
godot_binary_sha256: exact value
v2_cli_runtime: PASS
v2_editor_plugin_lifecycle: PASS
v2_recovery_mode: PASS
semantic_validator: PASS
repository_regressions: PASS
original_user_projects_runtime: NOT_RUN
production_network_mcp: NOT_IMPLEMENTED
runtime_debugger_bridge: NOT_IMPLEMENTED
project_test_framework: NOT_CONFIGURED
physical_input: NOT_RUN
human_usability: HUMAN_NOT_RUN
production_adapter_ready: false
registry_release_locks: UNCHANGED
merge: NOT_AUTHORIZED
```

---

## Stage B completion gate

```yaml
static_v2_stage_merged: true
actual_godot_binary_verified: true
test_only_red_recorded: true
fixture_manifest_v2: true
read_only_v2_runtime_green: true
approved_idempotent_mutation_v2_green: true
stale_precondition_rejection_green: true
output_validation_green: true
generic_task_lifecycle_green: true
editor_lifecycle_green: true
recovery_mode_green: true
v2_evidence_hashes_verified: true
v1_active_files_removed: true
repository_regressions_green: true
current_merge_ref_ci: PASS
unresolved_must_fix: 0
unresolved_review_threads: 0
registry_release_locks_unchanged: true
production_adapter_ready: false
```

The runtime-migration PR remains Draft until separate merge authorization. Passing the isolated Pilot does not authorize production MCP transport or adoption in a user game project.
