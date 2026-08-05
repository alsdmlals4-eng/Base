# Godot Live Editor Contract v2 Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add versioned Godot live-editor v2 Schemas, deterministic semantic validation, a fail-closed v1 migration boundary, and updated project templates without implementing a production EditorPlugin, transport server, or runtime bridge.

**Architecture:** Preserve the merged Base-owner → project adapter → project-owned implementation model. Introduce v2 beside v1, validate structure with JSON Schema Draft 2020-12, validate cross-field equality and approval history with a Python semantic validator, then switch the installation template and adapter to v2 only after migration tests pass. Existing v1 Schemas and the Godot 4.7.1 Pilot remain audit-readable and cannot authorize v2 mutation.

**Tech Stack:** Python 3.12, `unittest`, `jsonschema` Draft 2020-12, JSON, Markdown, existing Base GitHub Actions.

## Global Constraints

- Start from `agent/godot-live-editor-contract-v2-reconciliation` after rechecking the latest `main`, PR #157, and related open PRs.
- Keep `schemas/godot-live-editor-capability-manifest-v1.schema.json` and `schemas/godot-live-editor-operation-envelope-v1.schema.json` unchanged.
- Keep `examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` and `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json` unchanged and audit-readable.
- Set v2 `schema_version` to integer `2`; never reinterpret a v1 document as v2.
- Keep `skills/SKILL_REGISTRY.json` byte-identical with released SHA-256 `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- Keep Base v9.4.3 and predecessor release locks and frozen derivatives unchanged.
- Do not add a broad Base active Skill, universal MCP server, production EditorPlugin, runtime debugger bridge, remote endpoint, wildcard bind, arbitrary script execution default, or game-project adoption.
- Keep the core protocol-neutral; MCP is represented only by `contract_snapshot.protocol_profile: MCP` plus an exact `protocol_version`.
- Validate structure before semantics, input before engine action, and output before successful result promotion.
- Use stable machine codes for every semantic rejection; do not rely on free-form exception text.
- Keep runtime, physical-input, and human evidence `NOT_RUN` in this static reconciliation PR.
- Every task follows RED → verify RED → minimal GREEN → verify GREEN → commit.

---

## File Responsibility Map

### Create

- `schemas/godot-live-editor-capability-manifest-v2.schema.json` — v2 project identity, transport, catalog, capabilities, policy axes, input/output Schemas, path access, tests, validation, and adoption metadata.
- `schemas/godot-live-editor-operation-envelope-v2.schema.json` — v2 request, exact identities, contract snapshot, expected/observed preconditions, approval, task, result, and evidence.
- `tools/validate_godot_live_editor_contract_v2.py` — deterministic structural/semantic validation and CLI; no engine execution.
- `tests/test_godot_live_editor_contract_v2.py` — v2 Schema, semantic, migration, transport, evidence, and protected-boundary tests.

### Modify

- `tests/test_godot_live_editor_contract.py` — validate v1 against the preserved Pilot manifest after the installation template switches to v2.
- `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` — switch the safe installation template to `schema_version: 2` only after migration tests are GREEN.
- `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md` — resolve v2 canonical files, use independent policy axes, and fail with `MIGRATION_REQUIRED_V1` for v1 mutation authority.
- `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md` — compact v2 discovery and stop conditions.
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md` — canonical v2 execution model and v1 audit boundary.
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md` — exact binding, stale-state, transport, evidence, and recovery rules.
- `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md` — require v2 semantic validation before readiness can advance.
- `tests/test_local_validation.py` — include v2 tests in local validation discovery.
- `tests/test_v9_machine_contracts.py` — include v2 tests in the Base v9 required suite.

## Exact Python Interfaces

`tools/validate_godot_live_editor_contract_v2.py` exposes these names and signatures:

- `ContractKind = Literal["V1_AUDIT_ONLY", "V2"]`
- `canonical_json_sha256(value: Any) -> str`
- `classify_contract_document(document: Mapping[str, Any]) -> ContractKind`
- `operation_request_material(envelope: Mapping[str, Any]) -> dict[str, Any]`
- `validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]`
- `validate_operation_semantics(manifest: Mapping[str, Any], envelope: Mapping[str, Any], *, prior_operations: Sequence[Mapping[str, Any]] = (), now: datetime | None = None) -> list[str]`
- `validate_contract_pair(manifest: Mapping[str, Any], operation: Mapping[str, Any] | None = None, *, prior_operations: Sequence[Mapping[str, Any]] = (), mode: Literal["AUDIT", "AUTHORIZE"] = "AUTHORIZE", now: datetime | None = None) -> list[str]`

The CLI accepts one `--manifest`, an optional `--operation`, repeatable `--prior-operation`, `--mode AUDIT|AUTHORIZE`, and an optional RFC3339 `--now`. It prints exactly one compact JSON object to stdout:

```json
{"status":"PASS","errors":[]}
```

or:

```json
{"status":"FAIL","errors":["STABLE_MACHINE_CODE"]}
```

Exit code is `0` for PASS and `1` for FAIL. Expected validation failures do not print stack traces or diagnostics to protocol stdout.

---

### Task 1: Wire a Missing-v2 RED Gate Into Required Validation

**Files:**
- Create: `tests/test_godot_live_editor_contract_v2.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: existing `ROOT`, UTF-8 loading, and `unittest` patterns.
- Produces: `GodotLiveEditorContractV2Tests`, imported by local and Base v9 validation suites.

- [ ] **Step 1: Create the initial missing-path test without importing the future validator**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
SEMANTIC_VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract_v2.py"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md"
V2_TEMPLATE = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
V1_PILOT_MANIFEST = ROOT / "examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


class GodotLiveEditorContractV2Tests(unittest.TestCase):
    maxDiff = None

    def test_v2_contract_artifacts_exist(self) -> None:
        required = (CAPABILITY_SCHEMA_V2, OPERATION_SCHEMA_V2, SEMANTIC_VALIDATOR, DESIGN)
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)
```

- [ ] **Step 2: Import the class into both required aggregate modules**

Add to `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`:

```python
from tests.test_godot_live_editor_contract_v2 import (
    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
)
```

- [ ] **Step 3: Run the focused RED test**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL listing the two v2 Schema files and semantic validator as missing. If a local checkout is unavailable, push the test-only commit and use the exact-head `ubuntu-contract` job as the RED environment.

- [ ] **Step 4: Confirm the RED is focused**

Inspect the exact-head Actions job. Canonical-reference freshness and generated-artifact checks must pass before the missing-path test fails. Record skipped jobs as skipped, not PASS.

- [ ] **Step 5: Commit the RED gate only**

```bash
git add tests/test_godot_live_editor_contract_v2.py \
  tests/test_local_validation.py \
  tests/test_v9_machine_contracts.py
git commit -m "test: define Godot live editor v2 contract gate"
```

---

### Task 2: Add v2 Structural Schemas and Valid Builders

**Files:**
- Create: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Create: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: JSON Schema Draft 2020-12 and the approved five-axis model.
- Produces: structurally valid v2 manifest and operation builders for later semantic tests.

- [ ] **Step 1: Add deterministic manifest and operation builders**

Add imports:

```python
import copy
from datetime import UTC, datetime

from jsonschema import Draft202012Validator
```

Add `make_valid_manifest()` with this exact shape:

```python
def make_valid_manifest() -> dict:
    input_schema = {
        "type": "object",
        "properties": {"scene_path": {"type": "string", "pattern": "^res://"}},
        "required": ["scene_path"],
        "additionalProperties": False,
    }
    output_schema = {
        "type": "object",
        "properties": {"node_count": {"type": "integer", "minimum": 0}},
        "required": ["node_count"],
        "additionalProperties": False,
    }
    manifest = {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
        "configuration_state": "CONFIGURED",
        "contract_version": "2.0.0",
        "adapter_version": "2.0.0",
        "project_identity": {
            "normalized_project_path": "/workspace/game",
            "project_godot_sha256": "a" * 64,
            "project_fingerprint": "godot-project-a",
        },
        "engine_compatibility": {
            "detected_version": "4.7.1",
            "minimum_version": "4.3",
            "maximum_exclusive_version": "5.0",
        },
        "tool_adoption": {
            "source": "project-owned",
            "exact_version": "2.0.0",
            "telemetry_policy": "DISABLED",
            "external_data_policy": "DENY_BY_DEFAULT",
            "uninstall_procedure": "docs/operations/remove-godot-live-editor.md",
            "rollback_reference": "docs/operations/restore-godot-live-editor.md",
        },
        "transport": {
            "kind": "CLI",
            "enabled": True,
            "bind_host": None,
            "endpoint_identity": "cli-current-process",
            "protocol_profile": "GENERIC",
            "protocol_version": "1.0",
            "access_control": {
                "authentication_mode": "NOT_APPLICABLE",
                "origin_policy": "NOT_APPLICABLE",
                "session_binding": "NOT_APPLICABLE",
                "os_access_control": "CURRENT_USER_ONLY",
            },
        },
        "catalog": {
            "generated_at": "2026-08-05T00:00:00Z",
            "sha256": "b" * 64,
            "freshness_state": "FRESH",
        },
        "project_test_framework": {
            "state": "NOT_CONFIGURED",
            "runner_capability_id": None,
        },
        "capabilities": [
            {
                "capability_id": "scene.inspect",
                "description": "Inspect a bounded scene summary.",
                "execution_path": "CLI_HEADLESS",
                "effect_kind": "READ_ONLY",
                "idempotency": "NOT_APPLICABLE",
                "approval_policy": "NOT_REQUIRED",
                "execution_mode": "SYNCHRONOUS",
                "rollback_policy": "NOT_APPLICABLE",
                "input_schema": input_schema,
                "output_schema": output_schema,
                "input_schema_sha256": "c" * 64,
                "output_schema_sha256": "d" * 64,
                "path_access": {
                    "read_roots": ["res://"],
                    "write_roots": [],
                    "artifact_root": "artifacts/",
                },
                "precondition_policy": "NONE",
                "retry_policy": {
                    "automatic": True,
                    "maximum_attempts": 2,
                    "requires_ledger": False,
                },
                "timeout_policy": {
                    "milliseconds": 10000,
                    "unknown_outcome": "SAFE_TO_RETRY",
                },
                "evidence_outputs": ["ENGINE_STATE"],
                "unsupported_states": ["IMPORTING"],
            }
        ],
        "validation": {
            "contract_state": "CONTRACT_PASS",
            "execution_state": "NOT_RUN",
            "runtime_state": "NOT_RUN",
            "physical_input_state": "NOT_RUN",
            "human_state": "HUMAN_NOT_RUN",
        },
    }
    return manifest
```

Add `make_valid_operation(manifest: dict | None = None)`; it derives active policy and snapshot fields from the first capability:

```python
def make_valid_operation(manifest: dict | None = None) -> dict:
    manifest = make_valid_manifest() if manifest is None else copy.deepcopy(manifest)
    capability = manifest["capabilities"][0]
    operation = {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": "op-v2-001",
        "capability_id": capability["capability_id"],
        "project_identity": copy.deepcopy(manifest["project_identity"]),
        "instance_identity": {
            "automation_service_instance_id": "service-001",
            "editor_instance_id": None,
            "runtime_session_id": None,
            "runtime_session_state": "NOT_APPLICABLE",
        },
        "contract_snapshot": {
            "contract_version": manifest["contract_version"],
            "adapter_version": manifest["adapter_version"],
            "catalog_sha256": manifest["catalog"]["sha256"],
            "capability_input_schema_sha256": capability["input_schema_sha256"],
            "capability_output_schema_sha256": capability["output_schema_sha256"],
            "protocol_profile": manifest["transport"]["protocol_profile"],
            "protocol_version": manifest["transport"]["protocol_version"],
        },
        "policy": {
            "effect_kind": capability["effect_kind"],
            "idempotency": capability["idempotency"],
            "approval_policy": capability["approval_policy"],
            "execution_mode": capability["execution_mode"],
            "rollback_policy": capability["rollback_policy"],
        },
        "request": {"arguments": {"scene_path": "res://main.tscn"}},
        "request_hash": "e" * 64,
        "idempotency_key": None,
        "preconditions": {
            "expected_target_revision": None,
            "observed_target_revision": None,
            "expected_target_content_sha256": None,
            "observed_target_content_sha256": None,
            "expected_dirty_state": "NOT_APPLICABLE",
            "observed_dirty_state": "NOT_APPLICABLE",
            "expected_scene_path": None,
            "observed_scene_path": None,
            "conflict_policy": "FAIL_CLOSED",
        },
        "approval": {
            "state": "NOT_REQUIRED",
            "token_id": None,
            "token_binding": None,
            "expires_at": None,
            "consumed_by_operation_id": None,
        },
        "task": {
            "task_id": None,
            "state": "NOT_APPLICABLE",
            "created_at": None,
            "last_updated_at": None,
            "ttl_ms": None,
            "poll_interval_ms": None,
            "cancellation_policy": "NOT_SUPPORTED",
            "result_binding": None,
        },
        "result": {
            "success": True,
            "code": "OK",
            "message": "Inspection completed.",
            "data": {"node_count": 3},
            "result_hash": "f" * 64,
            "evidence": [
                {
                    "kind": "ENGINE_STATE",
                    "state": "EXECUTION_PASS",
                    "path": "artifacts/scene-summary.json",
                    "artifact_sha256": "1" * 64,
                    "generated_at": "2026-08-05T00:00:01Z",
                    "producer": "scene.inspect@2.0.0",
                }
            ],
        },
    }
    return operation
```

- [ ] **Step 2: Add structural acceptance and rejection tests**

```python
def test_v2_representative_documents_validate_structurally(self) -> None:
    manifest_errors = list(
        Draft202012Validator(load(CAPABILITY_SCHEMA_V2)).iter_errors(make_valid_manifest())
    )
    operation_errors = list(
        Draft202012Validator(load(OPERATION_SCHEMA_V2)).iter_errors(make_valid_operation())
    )
    self.assertEqual([], manifest_errors)
    self.assertEqual([], operation_errors)


def test_v2_schema_rejects_invalid_axis_and_transport_shapes(self) -> None:
    validator = Draft202012Validator(load(CAPABILITY_SCHEMA_V2))

    invalid = make_valid_manifest()
    invalid["capabilities"][0]["rollback_policy"] = "EDITOR_UNDO_REDO"
    self.assertTrue(list(validator.iter_errors(invalid)))

    invalid = make_valid_manifest()
    invalid["transport"].update(
        {
            "kind": "LOCAL_HTTP",
            "bind_host": "0.0.0.0",
        }
    )
    self.assertTrue(list(validator.iter_errors(invalid)))


def test_v2_operation_schema_rejects_unbound_task_approval_and_evidence(self) -> None:
    validator = Draft202012Validator(load(OPERATION_SCHEMA_V2))

    invalid = make_valid_operation()
    invalid["task"]["task_id"] = "task-not-allowed-for-sync"
    self.assertTrue(list(validator.iter_errors(invalid)))

    invalid = make_valid_operation()
    invalid["policy"]["approval_policy"] = "REQUIRED"
    invalid["approval"]["state"] = "APPROVED"
    self.assertTrue(list(validator.iter_errors(invalid)))

    invalid = make_valid_operation()
    invalid["result"]["evidence"][0]["artifact_sha256"] = None
    self.assertTrue(list(validator.iter_errors(invalid)))
```

- [ ] **Step 3: Run the expanded tests to verify RED**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because the v2 Schemas are absent.

- [ ] **Step 4: Implement the v2 capability Schema**

Use Draft 2020-12, closed objects, and `$defs` for SHA-256, timestamps, identities, transport, access control, JSON object Schema, path access, capability, retry, timeout, evidence kinds, project tests, and validation states.

Encode these conditions with `allOf` and `if/then`:

- `CONFIGURED` requires complete identity, enabled non-disabled transport, fresh catalog, and at least one capability.
- `READ_ONLY` requires `idempotency: NOT_APPLICABLE`, `rollback_policy: NOT_APPLICABLE`, and an empty `write_roots` array.
- `MUTATION` requires idempotency and rollback values other than `NOT_APPLICABLE` and requires a ledger.
- `NON_IDEMPOTENT` or `IRREVERSIBLE` requires no automatic retry and one maximum attempt.
- `LONG_RUNNING_TASK` requires `RESUME_BY_TASK_ID` and a ledger.
- `LOCAL_HTTP` permits only `127.0.0.1` or `::1` and requires explicit Origin, authenticated session, and project-client session binding.
- `CLI` requires null bind host, no ambient authentication, and current-user access.
- input/output Schemas are closed object Schemas.
- path roots allow normalized `res://` and `artifacts/` forms only and reject `..`, absolute OS paths, and wildcard roots.

- [ ] **Step 5: Implement the v2 operation Schema**

Use closed definitions for identities, contract snapshot, policy, typed request container, expected/observed preconditions, approval, task, result, and evidence.

Encode:

- synchronous operations have null task ID and `NOT_APPLICABLE` task state;
- long tasks require a receiver-generated task ID except `NOT_STARTED`;
- approval policy and approval state agree;
- approved operations carry a complete token binding, expiry, and consumed operation ID;
- terminal tasks carry a complete result binding;
- PASS-family evidence has confined path, SHA-256, producer, and timestamp;
- non-PASS evidence has null path and hash;
- unknown contract-owned properties fail.

- [ ] **Step 6: Run structural GREEN tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: Task 1 and Task 2 tests PASS.

- [ ] **Step 7: Commit the structural contract**

```bash
git add schemas/godot-live-editor-capability-manifest-v2.schema.json \
  schemas/godot-live-editor-operation-envelope-v2.schema.json \
  tests/test_godot_live_editor_contract_v2.py
git commit -m "feat: add Godot live editor v2 schemas"
```

---

### Task 3: Add Deterministic Manifest Semantic Validation

**Files:**
- Create: `tools/validate_godot_live_editor_contract_v2.py`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: the v2 capability Schema and policy model.
- Produces: canonical hashing, version classification, and manifest semantic errors.

- [ ] **Step 1: Add failing manifest-semantic tests**

Import:

```python
from tools.validate_godot_live_editor_contract_v2 import (
    canonical_json_sha256,
    classify_contract_document,
    validate_manifest_semantics,
)
```

Add:

```python
def test_canonical_json_hash_is_order_independent(self) -> None:
    self.assertEqual(
        canonical_json_sha256({"a": 1, "b": [2, 3]}),
        canonical_json_sha256({"b": [2, 3], "a": 1}),
    )


def test_manifest_semantics_reject_duplicate_capability_and_hash_mismatch(self) -> None:
    manifest = make_valid_manifest()
    capability = manifest["capabilities"][0]
    capability["input_schema_sha256"] = canonical_json_sha256(capability["input_schema"])
    capability["output_schema_sha256"] = canonical_json_sha256(capability["output_schema"])
    manifest["capabilities"].append(copy.deepcopy(capability))
    self.assertIn("DUPLICATE_CAPABILITY_ID", validate_manifest_semantics(manifest))

    manifest = make_valid_manifest()
    manifest["capabilities"][0]["input_schema_sha256"] = "0" * 64
    self.assertIn(
        "CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH",
        validate_manifest_semantics(manifest),
    )


def test_manifest_semantics_reject_path_and_project_test_runner_gaps(self) -> None:
    manifest = make_valid_manifest()
    manifest["capabilities"][0]["path_access"]["read_roots"] = ["../outside"]
    self.assertIn("CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT", validate_manifest_semantics(manifest))

    manifest = make_valid_manifest()
    manifest["project_test_framework"] = {
        "state": "CONFIGURED",
        "runner_capability_id": "test.project",
    }
    self.assertIn("PROJECT_TEST_RUNNER_NOT_DECLARED", validate_manifest_semantics(manifest))
```

Add a LOCAL_HTTP case with missing Origin/auth/session binding and an invalid input/output Schema case using `Draft202012Validator.check_schema` failure.

- [ ] **Step 2: Run focused tests to verify RED**

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_canonical_json_hash_is_order_independent \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_manifest_semantics_reject_duplicate_capability_and_hash_mismatch \
  -v
```

Expected: import failure because the semantic validator does not exist.

- [ ] **Step 3: Implement canonical hashing and classification**

```python
def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classify_contract_document(document: Mapping[str, Any]) -> ContractKind:
    version = document.get("schema_version")
    if version == 1:
        return "V1_AUDIT_ONLY"
    if version == 2:
        return "V2"
    raise ValueError("UNSUPPORTED_SCHEMA_VERSION")
```

- [ ] **Step 4: Implement ordered manifest semantic validation**

Use `list(dict.fromkeys(errors))` for stable de-duplication. Validate unique capability IDs, valid policy combinations, valid JSON Schemas, exact input/output Schema hashes, normalized path roots, project-test runner uniqueness/evidence/path, and transport-specific security.

Return only these stable codes for covered cases:

```text
CAPABILITY_CATALOG_INVALID
CAPABILITY_ID_INVALID
DUPLICATE_CAPABILITY_ID
POLICY_AXIS_COMBINATION_INVALID
CAPABILITY_INPUT_SCHEMA_INVALID
CAPABILITY_OUTPUT_SCHEMA_INVALID
CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH
CAPABILITY_OUTPUT_SCHEMA_HASH_MISMATCH
CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT
PROJECT_TEST_RUNNER_NOT_DECLARED
PROJECT_TEST_RUNNER_AMBIGUOUS
PROJECT_TEST_RUNNER_EVIDENCE_INVALID
PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID
TRANSPORT_SECURITY_PROFILE_INVALID
```

- [ ] **Step 5: Replace deterministic test hashes with canonical hashes**

At the end of `make_valid_manifest()`:

```python
capability = manifest["capabilities"][0]
capability["input_schema_sha256"] = canonical_json_sha256(capability["input_schema"])
capability["output_schema_sha256"] = canonical_json_sha256(capability["output_schema"])
return manifest
```

- [ ] **Step 6: Run manifest semantic GREEN tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: all structural and manifest semantic tests PASS.

- [ ] **Step 7: Commit manifest semantics**

```bash
git add tools/validate_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract_v2.py
git commit -m "feat: validate Godot v2 manifest semantics"
```

---

### Task 4: Add Exact Operation, Approval, Task, Output, and Evidence Validation

**Files:**
- Modify: `tools/validate_godot_live_editor_contract_v2.py`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: one v2 manifest, one operation, optional prior operations, and an injectable clock.
- Produces: exact request/snapshot/approval/task/result/evidence semantic validation.

- [ ] **Step 1: Implement and test authoritative request material**

Add to the validator:

```python
def operation_request_material(envelope: Mapping[str, Any]) -> dict[str, Any]:
    request = envelope.get("request")
    arguments = request.get("arguments") if isinstance(request, Mapping) else None
    return {
        "capability_id": envelope.get("capability_id"),
        "project_identity": envelope.get("project_identity"),
        "instance_identity": envelope.get("instance_identity"),
        "contract_snapshot": envelope.get("contract_snapshot"),
        "policy": envelope.get("policy"),
        "preconditions": envelope.get("preconditions"),
        "arguments": arguments,
    }
```

At the end of `make_valid_operation()`:

```python
operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
operation["result"]["result_hash"] = canonical_json_sha256(operation["result"]["data"])
return operation
```

Test that changing any argument, expected precondition, observed precondition, identity, snapshot, or policy changes the request hash.

- [ ] **Step 2: Add exact mutation helpers for approval and stale-state tests**

```python
def make_mutation_manifest() -> dict:
    manifest = make_valid_manifest()
    capability = manifest["capabilities"][0]
    capability.update(
        {
            "capability_id": "state.write_marker",
            "description": "Write one approved marker.",
            "effect_kind": "MUTATION",
            "idempotency": "IDEMPOTENT",
            "approval_policy": "REQUIRED",
            "execution_mode": "SYNCHRONOUS",
            "rollback_policy": "SNAPSHOT",
            "input_schema": {
                "type": "object",
                "properties": {"marker": {"type": "string", "minLength": 1}},
                "required": ["marker"],
                "additionalProperties": False,
            },
            "output_schema": {
                "type": "object",
                "properties": {"written": {"const": True}},
                "required": ["written"],
                "additionalProperties": False,
            },
            "path_access": {
                "read_roots": ["res://", "artifacts/"],
                "write_roots": ["artifacts/"],
                "artifact_root": "artifacts/",
            },
            "precondition_policy": "REQUIRED",
            "retry_policy": {
                "automatic": False,
                "maximum_attempts": 1,
                "requires_ledger": True,
            },
            "timeout_policy": {
                "milliseconds": 10000,
                "unknown_outcome": "RECONCILE_BEFORE_RETRY",
            },
            "evidence_outputs": ["ENGINE_STATE", "LOG"],
        }
    )
    capability["input_schema_sha256"] = canonical_json_sha256(capability["input_schema"])
    capability["output_schema_sha256"] = canonical_json_sha256(capability["output_schema"])
    return manifest


def make_approved_mutation(
    manifest: dict,
    *,
    operation_id: str,
    token_id: str,
) -> dict:
    operation = make_valid_operation(manifest)
    operation["operation_id"] = operation_id
    operation["request"] = {"arguments": {"marker": "approved"}}
    operation["idempotency_key"] = "marker-approved"
    operation["preconditions"] = {
        "expected_target_revision": "revision-1",
        "observed_target_revision": "revision-1",
        "expected_target_content_sha256": "2" * 64,
        "observed_target_content_sha256": "2" * 64,
        "expected_dirty_state": "CLEAN",
        "observed_dirty_state": "CLEAN",
        "expected_scene_path": "res://main.tscn",
        "observed_scene_path": "res://main.tscn",
        "conflict_policy": "FAIL_CLOSED",
    }
    operation["result"]["data"] = {"written": True}
    operation["result"]["result_hash"] = canonical_json_sha256(operation["result"]["data"])
    operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
    operation["approval"] = {
        "state": "APPROVED",
        "token_id": token_id,
        "token_binding": {
            "operation_id": operation_id,
            "capability_id": operation["capability_id"],
            "project_identity": copy.deepcopy(operation["project_identity"]),
            "instance_identity": copy.deepcopy(operation["instance_identity"]),
            "contract_snapshot": copy.deepcopy(operation["contract_snapshot"]),
            "policy": copy.deepcopy(operation["policy"]),
            "request_hash": operation["request_hash"],
            "preconditions": copy.deepcopy(operation["preconditions"]),
        },
        "expires_at": "2026-08-05T00:01:00Z",
        "consumed_by_operation_id": operation_id,
    }
    return operation
```

- [ ] **Step 3: Add failing operation-semantic tests**

```python
def test_operation_semantics_reject_stale_state_and_output_mismatch(self) -> None:
    manifest = make_mutation_manifest()
    operation = make_approved_mutation(
        manifest,
        operation_id="op-v2-001",
        token_id="token-1",
    )
    operation["preconditions"]["observed_target_revision"] = "revision-2"
    operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
    operation["approval"]["token_binding"]["request_hash"] = operation["request_hash"]
    operation["approval"]["token_binding"]["preconditions"] = copy.deepcopy(
        operation["preconditions"]
    )
    self.assertIn(
        "TARGET_STATE_CONFLICT",
        validate_operation_semantics(manifest, operation),
    )

    operation = make_approved_mutation(
        manifest,
        operation_id="op-v2-002",
        token_id="token-2",
    )
    operation["result"]["data"] = {"written": "yes"}
    self.assertIn(
        "OUTPUT_SCHEMA_MISMATCH",
        validate_operation_semantics(manifest, operation),
    )


def test_operation_semantics_reject_cross_operation_approval_reuse(self) -> None:
    manifest = make_mutation_manifest()
    prior = make_approved_mutation(
        manifest,
        operation_id="op-v2-001",
        token_id="token-1",
    )
    current = make_approved_mutation(
        manifest,
        operation_id="op-v2-002",
        token_id="token-1",
    )
    errors = validate_operation_semantics(
        manifest,
        current,
        prior_operations=[prior],
        now=datetime(2026, 8, 5, 0, 0, 30, tzinfo=UTC),
    )
    self.assertIn("APPROVAL_TOKEN_REUSED", errors)
```

Add table-driven cases for undeclared capability, policy mismatch, project/service/Editor/runtime identity mismatch, old catalog/Schema hash, invalid request arguments, request hash mismatch, missing required precondition, expired approval, token binding mismatch, terminal task binding mismatch, result hash mismatch, PASS evidence outside `artifacts/`, and evidence without hash.

- [ ] **Step 4: Run operation tests to verify RED**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: the new semantic assertions fail because operation validation is absent.

- [ ] **Step 5: Implement exact capability, policy, identity, and snapshot checks**

Build a unique capability index. Compare all five axes and these snapshot fields:

```text
contract_version
adapter_version
catalog_sha256
capability_input_schema_sha256
capability_output_schema_sha256
protocol_profile
protocol_version
```

Require `editor_instance_id` for `EDITOR_PLUGIN`, an active `runtime_session_id` for `RUNTIME_DEBUGGER`, and neither for `CLI_HEADLESS` unless project policy explicitly requires it.

Return:

```text
CAPABILITY_NOT_DECLARED
CAPABILITY_AMBIGUOUS
POLICY_MISMATCH
PROJECT_IDENTITY_MISMATCH
INSTANCE_IDENTITY_INVALID
CONTRACT_SNAPSHOT_MISMATCH
```

- [ ] **Step 6: Implement input, request hash, and stale-state checks**

Validate `request.arguments` with the selected input Schema. Recompute `request_hash`. When `precondition_policy` is `REQUIRED`, require expected and observed revision/hash/dirty/scene values. Compare every non-null expected value with its observed partner before engine action.

Return:

```text
REQUEST_SCHEMA_INVALID
REQUEST_HASH_MISMATCH
PRECONDITION_REQUIRED
TARGET_STATE_CONFLICT
```

- [ ] **Step 7: Implement approval equality, expiry, and history checks**

For approved operations, token binding equals operation ID, capability, project/instance identity, snapshot, policy, request hash, and preconditions. Parse timezone-aware expiry. Reject a token ID found in a different prior operation. Permit only an exact completed idempotent replay whose operation ID, request hash, idempotency key, capability, and completed result hash all match.

Return:

```text
APPROVAL_REQUIRED
APPROVAL_TOKEN_MISMATCH
APPROVAL_EXPIRED
APPROVAL_TOKEN_REUSED
```

- [ ] **Step 8: Implement task, output, result, and evidence checks**

For terminal tasks, require exact operation, project, service instance, task ID, and result hash binding. Validate result data against output Schema and recompute result hash. Constrain PASS evidence to the capability artifact root and require SHA-256.

Return:

```text
TASK_RESULT_STALE
TASK_RESULT_HASH_MISMATCH
OUTPUT_SCHEMA_MISMATCH
RESULT_HASH_MISMATCH
EVIDENCE_KIND_STATE_INVALID
EVIDENCE_PATH_OUTSIDE_ARTIFACT_ROOT
EVIDENCE_HASH_MISSING
```

- [ ] **Step 9: Run focused and preserved-v1 GREEN tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
python -m unittest tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_runtime_pilot -v
```

Expected: v2 tests PASS and preserved v1/Pilot tests remain PASS.

- [ ] **Step 10: Commit operation semantics**

```bash
git add tools/validate_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract_v2.py
git commit -m "feat: validate Godot v2 operation bindings"
```

---

### Task 5: Add the CLI and Fail-closed v1 Audit Migration

**Files:**
- Modify: `tools/validate_godot_live_editor_contract_v2.py`
- Modify: `tests/test_godot_live_editor_contract_v2.py`
- Modify: `tests/test_godot_live_editor_contract.py`
- Modify: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`

**Interfaces:**
- Consumes: v1 audit documents and v2 manifest/operation documents.
- Produces: `validate_contract_pair`, deterministic CLI output, and explicit v1 audit/authority states.

- [ ] **Step 1: Add migration, template, and CLI RED tests**

```python
def test_v1_is_audit_readable_but_cannot_authorize_v2_mutation(self) -> None:
    v1 = load(V1_PILOT_MANIFEST)
    self.assertEqual("V1_AUDIT_ONLY", classify_contract_document(v1))
    self.assertEqual([], validate_contract_pair(v1, mode="AUDIT"))
    self.assertIn(
        "V1_MUTATION_AUTHORITY_REJECTED",
        validate_contract_pair(v1, mode="AUTHORIZE"),
    )


def test_installation_template_is_safe_v2_not_configured(self) -> None:
    template = load(V2_TEMPLATE)
    self.assertEqual(2, template["schema_version"])
    self.assertEqual("NOT_CONFIGURED", template["configuration_state"])
    self.assertEqual([], template["capabilities"])
    self.assertFalse(template["transport"]["enabled"])
    self.assertEqual("NOT_RUN", template["validation"]["runtime_state"])
    self.assertEqual("HUMAN_NOT_RUN", template["validation"]["human_state"])
```

Add a subprocess test that invokes AUDIT and AUTHORIZE modes, parses exactly one stdout JSON object, and asserts exit codes `0` and `1`.

- [ ] **Step 2: Run migration tests to verify RED**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because pair validation, CLI behavior, and v2 template switch are absent.

- [ ] **Step 3: Implement `validate_contract_pair`**

Use this exact behavior:

```python
def validate_contract_pair(
    manifest: Mapping[str, Any],
    operation: Mapping[str, Any] | None = None,
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    mode: Literal["AUDIT", "AUTHORIZE"] = "AUTHORIZE",
    now: datetime | None = None,
) -> list[str]:
    kind = classify_contract_document(manifest)
    if kind == "V1_AUDIT_ONLY":
        if mode == "AUDIT" and operation is None:
            return []
        return ["V1_MUTATION_AUTHORITY_REJECTED"]

    errors = validate_manifest_structure(manifest)
    errors.extend(validate_manifest_semantics(manifest))
    if operation is not None:
        errors.extend(validate_operation_structure(operation))
        errors.extend(
            validate_operation_semantics(
                manifest,
                operation,
                prior_operations=prior_operations,
                now=now,
            )
        )
    return list(dict.fromkeys(errors))
```

Add private structural helpers that return `MANIFEST_SCHEMA_INVALID` and `OPERATION_SCHEMA_INVALID` instead of raw `jsonschema` messages.

- [ ] **Step 4: Implement the exact CLI**

Use `argparse`, repeatable `--prior-operation`, enum choices for mode, and RFC3339 parsing for `--now`. Print compact JSON once. Convert unsupported versions, malformed JSON, and invalid timestamps into stable error codes.

- [ ] **Step 5: Switch the installation template to safe v2**

The v2 template is `NOT_CONFIGURED`, transport-disabled, capability-empty, and evidence-neutral. It includes null project identity, detected engine version, tool source/version, uninstall procedure, rollback reference, and catalog values. It uses telemetry `DISABLED`, external data `DENY_BY_DEFAULT`, protocol profile `GENERIC`, and current-user OS access.

- [ ] **Step 6: Preserve v1 tests and move template evidence coverage to v2**

In `tests/test_godot_live_editor_contract.py`:

- replace the v1 `MANIFEST` constant with `V1_PILOT_MANIFEST` pointing to the preserved Pilot manifest;
- rename the v1 template validation test to `test_v1_pilot_manifest_and_representative_configured_manifest_validate`;
- validate `V1_PILOT_MANIFEST` against the v1 Schema;
- remove the template-specific evidence-state test from the v1 class because the installation template is now v2.

The new v2 test `test_installation_template_is_safe_v2_not_configured` preserves and extends the removed evidence-state coverage.

- [ ] **Step 7: Run migration and backward-audit GREEN tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_runtime_pilot -v
```

Expected: v2 template validates, v1 remains audit-readable, and v1 authorize mode fails closed.

- [ ] **Step 8: Commit migration behavior and template switch**

```bash
git add tools/validate_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract.py \
  templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json
git commit -m "feat: add fail-closed Godot v1 to v2 migration"
```

---

### Task 6: Update Canonical Contracts and the Project Adapter

**Files:**
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Modify: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: implemented v2 files and migration behavior.
- Produces: compact canonical discovery and project-local execution rules.

- [ ] **Step 1: Add documentation and adapter RED assertions**

Assert the canonical docs and adapter include:

```text
effect_kind
idempotency
approval_policy
execution_mode
rollback_policy
contract_snapshot
capability_input_schema_sha256
capability_output_schema_sha256
TARGET_STATE_CONFLICT
OUTPUT_SCHEMA_MISMATCH
MIGRATION_REQUIRED_V1
V1_AUDIT_ONLY
EditorUndoRedoManager
--recovery-mode
```

Assert the adapter references both v2 Schemas and `tools/validate_godot_live_editor_contract_v2.py`. Assert `operation_class` appears only in an explicitly historical v1 migration paragraph.

- [ ] **Step 2: Run documentation tests to verify RED**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because canonical docs and adapter still describe v1 as active.

- [ ] **Step 3: Update the automation contract**

Define the five axes, exact identity, request material, expected/observed preconditions, input/output validation order, task lifecycle, evidence separation, and `MIGRATION_REQUIRED_V1`. Preserve v1 only as audit history.

- [ ] **Step 4: Update security and recovery**

Define exact binding equality, token expiry/reuse, stale-state comparison, path confinement, transport-specific access control, result/evidence hashing, and recovery-mode invalidation of old service/Editor approvals.

- [ ] **Step 5: Update production readiness**

Readiness cannot advance unless v2 Schema and semantic validation pass, v1 mutation authority is rejected, and future PRs prove the Editor main-thread queue and Undo/Redo transaction. Keep production adapter state `NOT_READY`.

- [ ] **Step 6: Update the adapter and AGENTS fragment**

Use this sequence:

```text
validate Base adapter pin
→ classify manifest version
→ reject v1 mutation with MIGRATION_REQUIRED_V1
→ validate v2 Schema
→ validate v2 semantics
→ verify target and snapshot
→ execute one typed capability
→ validate output
→ bind result and evidence
```

Keep existing Base owner routing unchanged. Do not add a Registry Skill.

- [ ] **Step 7: Run documentation and routing GREEN tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_adapter_resolution -v
```

Expected: PASS.

- [ ] **Step 8: Commit canonical and adapter updates**

```bash
git add docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md \
  docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md \
  docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md \
  templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md \
  templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md \
  tests/test_godot_live_editor_contract_v2.py
git commit -m "docs: activate Godot live editor v2 contract"
```

---

### Task 7: Close Required CI, Protected Boundaries, and Adversarial Cases

**Files:**
- Modify only confirmed failures in files already listed.
- Update PR #157 body after exact-head verification.

**Interfaces:**
- Consumes: complete static v2 reconciliation.
- Produces: exact-head evidence and a Draft PR ready for implementation review.

- [ ] **Step 1: Run focused contract suites**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_idempotent_approval \
  tests.test_godot_live_editor_runtime_contract_hardening \
  tests.test_godot_live_editor_adapter_resolution \
  tests.test_godot_live_editor_runtime_pilot -v
```

Expected: PASS. Runtime cases requiring an unavailable uploaded binary retain their explicit skip state.

- [ ] **Step 2: Run required aggregate validation**

```bash
python -m unittest tests.test_v9_machine_contracts -v
python -m unittest tests.test_local_validation -v
```

Then use the standard GitHub Actions workflows for canonical-reference, publication/generation, documentation/whitespace, and required CI validation.

- [ ] **Step 3: Attack the contract with the complete adversarial matrix**

Confirm tests reject:

```text
read-only mutation rollback
mutation with NOT_APPLICABLE idempotency
non-idempotent or irreversible automatic retry
long task without durable task binding
approval for a different service, Editor, runtime, catalog, or Schema
cross-operation approval token reuse
undeclared request arguments
invalid output data
request hash that omits expected or observed preconditions
stale target revision, content, dirty state, or Scene path
LOCAL_HTTP wildcard bind or missing Origin/auth/session binding
STDIO diagnostics on protocol stdout
PASS evidence without confined path and SHA-256
v1 mutation authority
v1 Pilot evidence modification
Registry or release-lock modification
project adapter registration as a Base active Skill
```

Classify each result as `MUST_FIX`, `SHOULD_FIX`, `REJECTED_CRITIQUE`, or `DEFERRED_TO_PR_B/C/D`. Fix only reproducible PR A weaknesses.

- [ ] **Step 4: Verify protected files and scope**

```bash
sha256sum skills/SKILL_REGISTRY.json
git diff --name-only main...HEAD
git diff --check main...HEAD
```

Confirm the Registry SHA-256 remains `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`; release locks, v1 Schemas, and Pilot evidence are unchanged; and no game project, Google Sheet, workflow topology, binary, archive, runtime artifact, or generated Godot UID entered the diff.

- [ ] **Step 5: Inspect exact-head GitHub Actions**

Require success for:

```text
Validate Base v9 Operating Contracts
Validate Game Project Operating System
Validate Evidence-Based Game Development Knowledge
Validate Game UX UI System
```

Within the project operating workflow require canonical-reference freshness, contract/governance regressions, docs/whitespace, publication/generation, and required `ci-gate`. Record Windows smoke as `SKIPPED_NOT_REQUIRED` when applicable.

- [ ] **Step 6: Recheck PR metadata and review state**

Confirm PR #157 targets `main`, is mergeable, has zero unresolved review threads, and remains on the exact tested head. If main advanced, reconcile from latest main without force-pushing unrelated history and rerun all checks.

- [ ] **Step 7: Update PR #157 evidence without merging**

Report:

```yaml
written_spec: APPROVED
implementation_plan: ADDED
v2_schema_validation: PASS
v2_semantic_validation: PASS
v1_audit_readability: PASS
v1_mutation_authority: REJECTED
exact_head_github_actions: PASS
registry_and_release_locks: UNCHANGED
godot_runtime_reexecution: NOT_REQUIRED_FOR_STATIC_PR_A
production_editor_adapter: NOT_IMPLEMENTED
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
physical_input: NOT_RUN
human_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

Keep PR #157 Draft until the static implementation is reviewed and the user explicitly authorizes merge.

- [ ] **Step 8: Commit only confirmed final corrections**

Commit each coherent defect correction with its regression test. Do not create an empty cleanup commit.

---

## Plan Self-review Results

### Spec coverage

- Orthogonal policy axes: Tasks 2–4.
- Exact project/service/Editor/runtime identity: Tasks 2 and 4.
- Contract and input/output Schema snapshot binding: Tasks 2–4.
- Semantic equality and approval history: Tasks 3–4.
- Stale-state expected/observed comparison: Tasks 2 and 4.
- Transport-specific local security: Tasks 2–3 and 7.
- Generic task lifecycle: Tasks 2 and 4.
- Evidence integrity and path confinement: Tasks 2–4.
- Godot recovery mode: Task 6.
- Non-destructive v1 migration: Task 5.
- Registry/release-lock protection: Task 7.
- Production adapter exclusion: Global Constraints and Tasks 6–7.

### Incompleteness scan

Every code-producing task names files, exact interfaces, commands, expected outcomes, stable error codes, and commit boundaries. Temporary test values are explicitly replaced by canonical hashes before semantic GREEN.

### Type and naming consistency

The plan consistently uses:

```text
schema_version: 2
capability.input_schema and capability.output_schema
capability_input_schema_sha256 and capability_output_schema_sha256
request.arguments
expected_* and observed_* precondition fields
validate_manifest_semantics
validate_operation_semantics
validate_contract_pair
prior_operations
MIGRATION_REQUIRED_V1
V1_MUTATION_AUTHORITY_REJECTED
```

No v2 step uses the v1 `operation_class` as active authority.