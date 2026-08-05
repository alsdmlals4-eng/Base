# Godot Live Editor Contract v2 Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add versioned Godot live-editor v2 Schemas, deterministic semantic validation, a fail-closed v1 migration boundary, and updated project templates without implementing a production EditorPlugin, transport server, or runtime bridge.

**Architecture:** Preserve the merged Base-owner → project adapter → project-owned implementation model. Introduce v2 beside v1, validate structure with JSON Schema Draft 2020-12, validate cross-field equality and history-sensitive approval reuse with a Python semantic validator, then switch the installation template and adapter to v2 only after migration tests pass. Existing v1 Schemas and the Godot 4.7.1 Pilot remain audit-readable and cannot authorize v2 mutation.

**Tech Stack:** Python 3.12, `unittest`, `jsonschema` Draft 2020-12, JSON, Markdown, existing Base GitHub Actions.

## Global Constraints

- Start from `agent/godot-live-editor-contract-v2-reconciliation` after rechecking the latest `main`, PR #157, and related open PRs.
- Keep `schemas/godot-live-editor-capability-manifest-v1.schema.json` and `schemas/godot-live-editor-operation-envelope-v1.schema.json` unchanged.
- Keep `examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` and `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json` audit-readable and unchanged.
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

- `schemas/godot-live-editor-capability-manifest-v2.schema.json` — structural contract for v2 project identity, transport, catalog, capabilities, policy axes, input/output Schemas, tests, validation, and adoption metadata.
- `schemas/godot-live-editor-operation-envelope-v2.schema.json` — structural contract for v2 request, exact identities, contract snapshot, policy, preconditions, approval, task, result, and evidence.
- `tools/validate_godot_live_editor_contract_v2.py` — deterministic semantic validation and CLI; no engine execution.
- `tests/test_godot_live_editor_contract_v2.py` — v2 Schema, semantic, migration, transport, evidence, and protected-boundary tests.

### Modify

- `tests/test_godot_live_editor_contract.py` — point v1 audit tests at the preserved Pilot manifest instead of the installation template after the template switches to v2.
- `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json` — switch the safe installation template to `schema_version: 2` only after v2 migration tests are GREEN.
- `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md` — resolve v2 canonical files, expose policy axes, and fail with `MIGRATION_REQUIRED_V1` for v1 mutation authority.
- `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md` — compact v2 discovery and stop conditions.
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md` — canonical v2 execution model and v1 audit boundary.
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md` — exact binding, stale-state, transport, evidence, and recovery rules.
- `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md` — require v2 semantic validation before production-adapter readiness can advance.
- `tests/test_local_validation.py` — include v2 contract tests in local validation discovery.
- `tests/test_v9_machine_contracts.py` — include v2 contract tests in the Base v9 required contract suite.

## Public Python Interfaces

`tools/validate_godot_live_editor_contract_v2.py` must expose these exact callables:

```python
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Literal

ContractKind = Literal["V1_AUDIT_ONLY", "V2"]


def canonical_json_sha256(value: Any) -> str: ...


def classify_contract_document(document: Mapping[str, Any]) -> ContractKind: ...


def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]: ...


def validate_operation_semantics(
    manifest: Mapping[str, Any],
    envelope: Mapping[str, Any],
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    now: datetime | None = None,
) -> list[str]: ...


def validate_contract_pair(
    manifest: Mapping[str, Any],
    operation: Mapping[str, Any] | None = None,
    *,
    prior_operations: Sequence[Mapping[str, Any]] = (),
    mode: Literal["AUDIT", "AUTHORIZE"] = "AUTHORIZE",
    now: datetime | None = None,
) -> list[str]: ...
```

The CLI interface must be:

```text
python tools/validate_godot_live_editor_contract_v2.py \
  --manifest <path> \
  [--operation <path>] \
  [--prior-operation <path> ...] \
  [--mode AUDIT|AUTHORIZE] \
  [--now <RFC3339 timestamp>]
```

It prints exactly one JSON object to stdout:

```json
{"status":"PASS","errors":[]}
```

or:

```json
{"status":"FAIL","errors":["STABLE_MACHINE_CODE"]}
```

Exit code is `0` for PASS and `1` for FAIL. Diagnostics do not go to protocol stdout.

---

### Task 1: Wire a Missing-v2 RED Gate Into Required Validation

**Files:**
- Create: `tests/test_godot_live_editor_contract_v2.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**
- Consumes: existing `ROOT`, `read`, `load`, and `unittest` patterns from `tests/test_godot_live_editor_contract.py`.
- Produces: `GodotLiveEditorContractV2Tests`, imported by local and Base v9 validation suites.

- [ ] **Step 1: Create the initial missing-path test without importing the future validator**

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
SEMANTIC_VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract_v2.py"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md"


class GodotLiveEditorContractV2Tests(unittest.TestCase):
    def test_v2_contract_artifacts_exist(self) -> None:
        required = (CAPABILITY_SCHEMA_V2, OPERATION_SCHEMA_V2, SEMANTIC_VALIDATOR, DESIGN)
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)
```

- [ ] **Step 2: Import the new class into both required aggregate modules**

Add to `tests/test_local_validation.py`:

```python
from tests.test_godot_live_editor_contract_v2 import (
    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
)
```

Add the same import to `tests/test_v9_machine_contracts.py`.

- [ ] **Step 3: Run focused RED locally when a checkout is available**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because the two v2 Schema files and semantic validator do not exist. If local checkout execution is unavailable, push the test-only commit and use the exact-head `ubuntu-contract` job as the RED environment.

- [ ] **Step 4: Confirm unrelated required checks remain green before the focused failure**

Inspect the exact-head Actions run. Record that canonical-reference freshness and generated-artifact checks pass before the v2 missing-path assertion fails. Do not report unrelated skipped jobs as PASS.

- [ ] **Step 5: Commit the RED gate only**

```bash
git add \
  tests/test_godot_live_editor_contract_v2.py \
  tests/test_local_validation.py \
  tests/test_v9_machine_contracts.py
git commit -m "test: define Godot live editor v2 contract gate"
```

---

### Task 2: Add v2 Structural Schemas and Representative Builders

**Files:**
- Create: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Create: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: JSON Schema Draft 2020-12 and the exact policy axes from the approved design.
- Produces: structurally valid v2 manifest and operation documents for semantic tasks.

- [ ] **Step 1: Add reusable v2 builders to the test module**

Add imports:

```python
import copy
import json
from datetime import UTC, datetime

from jsonschema import Draft202012Validator
```

Add helpers with these exact top-level fields:

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
    return {
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
                "input_schema_sha256": "INPUT_SCHEMA_HASH",
                "output_schema_sha256": "OUTPUT_SCHEMA_HASH",
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
```

The test helper replaces `INPUT_SCHEMA_HASH` and `OUTPUT_SCHEMA_HASH` with `canonical_json_sha256` after Task 3 adds the validator import. Until then, use the known 64-character test placeholders `"c" * 64` and `"d" * 64`.

Add an operation builder whose typed input is explicit:

```python
def make_valid_operation() -> dict:
    return {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": "op-v2-001",
        "capability_id": "scene.inspect",
        "project_identity": {
            "normalized_project_path": "/workspace/game",
            "project_godot_sha256": "a" * 64,
            "project_fingerprint": "godot-project-a",
        },
        "instance_identity": {
            "automation_service_instance_id": "service-001",
            "editor_instance_id": None,
            "runtime_session_id": None,
            "runtime_session_state": "NOT_APPLICABLE",
        },
        "contract_snapshot": {
            "contract_version": "2.0.0",
            "adapter_version": "2.0.0",
            "catalog_sha256": "b" * 64,
            "capability_input_schema_sha256": "c" * 64,
            "capability_output_schema_sha256": "d" * 64,
            "protocol_profile": "GENERIC",
            "protocol_version": "1.0",
        },
        "policy": {
            "effect_kind": "READ_ONLY",
            "idempotency": "NOT_APPLICABLE",
            "approval_policy": "NOT_REQUIRED",
            "execution_mode": "SYNCHRONOUS",
            "rollback_policy": "NOT_APPLICABLE",
        },
        "request": {"arguments": {"scene_path": "res://main.tscn"}},
        "request_hash": "e" * 64,
        "idempotency_key": None,
        "preconditions": {
            "target_revision": None,
            "target_content_sha256": None,
            "expected_dirty_state": "NOT_APPLICABLE",
            "expected_scene_path": None,
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
```

- [ ] **Step 2: Add structural acceptance and rejection tests**

Add tests for:

```python
def test_v2_representative_documents_validate_structurally(self) -> None:
    self.assertEqual([], list(Draft202012Validator(load(CAPABILITY_SCHEMA_V2)).iter_errors(make_valid_manifest())))
    self.assertEqual([], list(Draft202012Validator(load(OPERATION_SCHEMA_V2)).iter_errors(make_valid_operation())))


def test_v2_schema_rejects_mixed_axis_and_unsafe_transport_shapes(self) -> None:
    manifest_validator = Draft202012Validator(load(CAPABILITY_SCHEMA_V2))

    invalid = make_valid_manifest()
    invalid["capabilities"][0]["effect_kind"] = "READ_ONLY"
    invalid["capabilities"][0]["rollback_policy"] = "EDITOR_UNDO_REDO"
    self.assertTrue(list(manifest_validator.iter_errors(invalid)))

    invalid = make_valid_manifest()
    invalid["transport"]["kind"] = "LOCAL_HTTP"
    invalid["transport"]["bind_host"] = "0.0.0.0"
    self.assertTrue(list(manifest_validator.iter_errors(invalid)))
```

Add operation rejection tests for a synchronous operation with a task ID, an approved operation without complete token binding, a PASS evidence entry without path/hash, and an unknown top-level field.

- [ ] **Step 3: Run the expanded tests to verify RED**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because the future schemas are absent or do not validate the representative documents.

- [ ] **Step 4: Implement the v2 capability Schema**

The Schema must use:

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Godot Live Editor Capability Manifest v2","type":"object","additionalProperties":false}
```

Require every top-level field used by `make_valid_manifest()`. Define closed `$defs` for SHA-256, RFC3339 timestamps, project identity, transport access control, JSON object Schema, capability, retry policy, timeout policy, evidence kind, project-test framework, and validation states.

Encode these structural conditions with `allOf` and `if/then`:

- `configuration_state: CONFIGURED` requires non-null project identity, enabled non-disabled transport, fresh catalog, and at least one capability.
- `READ_ONLY` requires `idempotency: NOT_APPLICABLE` and `rollback_policy: NOT_APPLICABLE`.
- `MUTATION` requires idempotency other than `NOT_APPLICABLE`, rollback other than `NOT_APPLICABLE`, and `retry_policy.requires_ledger: true`.
- `NON_IDEMPOTENT` or `IRREVERSIBLE` requires `retry_policy.automatic: false` and `maximum_attempts: 1`.
- `LONG_RUNNING_TASK` requires `timeout_policy.unknown_outcome: RESUME_BY_TASK_ID` and ledger use.
- `LOCAL_HTTP` allows only `127.0.0.1` or `::1` and requires explicit Origin, authenticated session, and project-client session binding.
- `CLI` requires `bind_host: null`, `authentication_mode: NOT_APPLICABLE`, and current-user access.
- Every `input_schema` and `output_schema` is a closed object Schema with `additionalProperties: false`.

- [ ] **Step 5: Implement the v2 operation Schema**

Require every top-level field used by `make_valid_operation()`. Define closed `$defs` for exact identities, contract snapshot, policy, request arguments, preconditions, approval, task, result, and evidence.

Encode these structural conditions:

- `SYNCHRONOUS` requires task state `NOT_APPLICABLE` and null task ID.
- `LONG_RUNNING_TASK` requires a non-null task ID for all states except `NOT_STARTED`; `NOT_STARTED` has null task ID and result binding.
- `approval_policy: NOT_REQUIRED` requires approval state `NOT_REQUIRED` and null token data.
- `approval_policy: REQUIRED` forbids approval state `NOT_REQUIRED`.
- `approval.state: APPROVED` requires token ID, complete token binding, expiry, and consumed operation ID.
- terminal task states require non-null result binding and result hash.
- file-backed PASS evidence requires confined relative path, SHA-256, producer, and timestamp.
- non-PASS evidence states require null path and hash.
- `additionalProperties: false` applies recursively to all contract-owned objects.

- [ ] **Step 6: Run structural GREEN tests**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: all Task 1 and Task 2 tests PASS.

- [ ] **Step 7: Commit the structural contract**

```bash
git add \
  schemas/godot-live-editor-capability-manifest-v2.schema.json \
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
- Consumes: v2 manifest Schema and the approved v2 policy model.
- Produces: `canonical_json_sha256`, `classify_contract_document`, and `validate_manifest_semantics`.

- [ ] **Step 1: Add failing hash and manifest-semantic tests**

Import the future module only after Task 2 files exist:

```python
from tools.validate_godot_live_editor_contract_v2 import (
    canonical_json_sha256,
    classify_contract_document,
    validate_manifest_semantics,
)
```

Add tests that assert:

```python
def test_canonical_json_hash_is_order_independent(self) -> None:
    self.assertEqual(
        canonical_json_sha256({"a": 1, "b": [2, 3]}),
        canonical_json_sha256({"b": [2, 3], "a": 1}),
    )


def test_manifest_semantics_reject_duplicate_capability_and_schema_hash_mismatch(self) -> None:
    manifest = make_valid_manifest()
    capability = manifest["capabilities"][0]
    capability["input_schema_sha256"] = canonical_json_sha256(capability["input_schema"])
    capability["output_schema_sha256"] = canonical_json_sha256(capability["output_schema"])
    duplicate = copy.deepcopy(capability)
    manifest["capabilities"].append(duplicate)
    self.assertIn("DUPLICATE_CAPABILITY_ID", validate_manifest_semantics(manifest))

    manifest = make_valid_manifest()
    manifest["capabilities"][0]["input_schema_sha256"] = "0" * 64
    self.assertIn("CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH", validate_manifest_semantics(manifest))
```

Add cases for invalid policy-axis combinations, configured project-test runner missing or ambiguous, missing `TEST_RESULT`, path outside approved roots, and transport-specific security mismatch.

- [ ] **Step 2: Run manifest semantic tests to verify RED**

Run:

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_canonical_json_hash_is_order_independent \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_manifest_semantics_reject_duplicate_capability_and_schema_hash_mismatch \
  -v
```

Expected: import failure because `tools/validate_godot_live_editor_contract_v2.py` does not exist.

- [ ] **Step 3: Implement canonical hashing and version classification**

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

- [ ] **Step 4: Implement manifest semantic error accumulation**

Use ordered de-duplication:

```python
def _unique(errors: list[str]) -> list[str]:
    return list(dict.fromkeys(errors))
```

`validate_manifest_semantics` must return stable codes including:

```text
CAPABILITY_CATALOG_INVALID
CAPABILITY_ID_INVALID
DUPLICATE_CAPABILITY_ID
POLICY_AXIS_COMBINATION_INVALID
CAPABILITY_INPUT_SCHEMA_INVALID
CAPABILITY_OUTPUT_SCHEMA_INVALID
CAPABILITY_INPUT_SCHEMA_HASH_MISMATCH
CAPABILITY_OUTPUT_SCHEMA_HASH_MISMATCH
PROJECT_TEST_RUNNER_NOT_DECLARED
PROJECT_TEST_RUNNER_AMBIGUOUS
PROJECT_TEST_RUNNER_EVIDENCE_INVALID
PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID
CAPABILITY_PATH_OUTSIDE_ALLOWED_ROOT
TRANSPORT_SECURITY_PROFILE_INVALID
```

Perform JSON Schema object validity checks with `Draft202012Validator.check_schema` for every input/output Schema. Enforce exact hash equality with `canonical_json_sha256`. Keep runtime state and approval history out of manifest validation.

- [ ] **Step 5: Replace placeholder hashes in `make_valid_manifest`**

After creating the builder dictionary, set:

```python
capability = manifest["capabilities"][0]
capability["input_schema_sha256"] = canonical_json_sha256(capability["input_schema"])
capability["output_schema_sha256"] = canonical_json_sha256(capability["output_schema"])
return manifest
```

- [ ] **Step 6: Run manifest semantic GREEN tests**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: structural and manifest semantic tests PASS; operation semantic tests are not yet present.

- [ ] **Step 7: Commit manifest semantic validation**

```bash
git add \
  tools/validate_godot_live_editor_contract_v2.py \
  tests/test_godot_live_editor_contract_v2.py
git commit -m "feat: validate Godot v2 manifest semantics"
```

---

### Task 4: Add Exact Operation, Approval, Task, Output, and Evidence Validation

**Files:**
- Modify: `tools/validate_godot_live_editor_contract_v2.py`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**
- Consumes: a structurally valid v2 manifest, one operation envelope, optional prior operation envelopes, and an injectable clock.
- Produces: `validate_operation_semantics` and exact request/result binding checks.

- [ ] **Step 1: Make the operation builder calculate authoritative hashes**

Add this helper to the validator:

```python
def operation_request_material(envelope: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "capability_id": envelope.get("capability_id"),
        "project_identity": envelope.get("project_identity"),
        "instance_identity": envelope.get("instance_identity"),
        "contract_snapshot": envelope.get("contract_snapshot"),
        "policy": envelope.get("policy"),
        "preconditions": envelope.get("preconditions"),
        "arguments": (
            envelope.get("request", {}).get("arguments")
            if isinstance(envelope.get("request"), Mapping)
            else None
        ),
    }
```

Update `make_valid_operation` after construction:

```python
operation["request_hash"] = canonical_json_sha256(operation_request_material(operation))
operation["result"]["result_hash"] = canonical_json_sha256(operation["result"]["data"])
return operation
```

- [ ] **Step 2: Add failing operation-semantic tests**

Add exact tests for:

- undeclared capability;
- operation policy differs from manifest capability policy;
- project identity, instance identity, catalog hash, or input/output Schema hash mismatch;
- request arguments fail the capability input Schema;
- request hash mismatch;
- required precondition missing or stale state represented by mismatched revision/hash;
- approved token binding differs from operation/request/snapshot/preconditions;
- expired approval using injected `now`;
- token ID reused by a different prior operation;
- exact completed idempotent replay remains allowed;
- task terminal binding differs from operation, service instance, task ID, or result hash;
- result data fails output Schema;
- PASS evidence has a path outside `artifacts/` or wrong artifact hash shape.

Representative token-reuse test:

```python
def test_operation_semantics_reject_cross_operation_approval_reuse(self) -> None:
    manifest = make_valid_manifest()
    operation = make_approved_mutation(manifest, operation_id="op-v2-002", token_id="token-1")
    prior = make_approved_mutation(manifest, operation_id="op-v2-001", token_id="token-1")
    errors = validate_operation_semantics(
        manifest,
        operation,
        prior_operations=[prior],
        now=datetime(2026, 8, 5, 0, 0, 30, tzinfo=UTC),
    )
    self.assertIn("APPROVAL_TOKEN_REUSED", errors)
```

- [ ] **Step 3: Run operation semantic tests to verify RED**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: new operation-semantic assertions fail because `validate_operation_semantics` is absent or incomplete.

- [ ] **Step 4: Implement capability selection and exact policy/snapshot checks**

Create a unique capability index and reject absence or ambiguity. Compare all five policy axes and these snapshot fields against the selected manifest/capability:

```text
contract_version
adapter_version
catalog_sha256
capability_input_schema_sha256
capability_output_schema_sha256
protocol_profile
protocol_version
```

Return stable codes:

```text
CAPABILITY_NOT_DECLARED
CAPABILITY_AMBIGUOUS
POLICY_MISMATCH
PROJECT_IDENTITY_MISMATCH
INSTANCE_IDENTITY_INVALID
CONTRACT_SNAPSHOT_MISMATCH
```

- [ ] **Step 5: Implement typed input, request hash, and precondition checks**

Validate `request.arguments` with the selected capability `input_schema`. Recompute `request_hash` from `operation_request_material`. For `precondition_policy: REQUIRED`, require a target revision or target content SHA-256 and exact expected Scene/dirty-state fields. Return:

```text
REQUEST_SCHEMA_INVALID
REQUEST_HASH_MISMATCH
PRECONDITION_REQUIRED
TARGET_STATE_CONFLICT
```

`TARGET_STATE_CONFLICT` is emitted when the operation carries an explicit observed/current comparison object and they differ. The validator does not query Godot; the project adapter supplies both values in the envelope before engine action.

- [ ] **Step 6: Implement approval equality, expiry, and prior-operation reuse checks**

For approved operations, token binding repeats and exactly equals:

```text
operation_id
capability_id
project_identity
instance_identity
contract_snapshot
policy
request_hash
preconditions
```

Parse RFC3339 expiry with timezone awareness. Compare `token_id` across `prior_operations`. Allow only an exact replay where prior and current operation IDs, request hashes, idempotency keys, capability IDs, and completed result hashes all match. Return:

```text
APPROVAL_REQUIRED
APPROVAL_TOKEN_MISMATCH
APPROVAL_EXPIRED
APPROVAL_TOKEN_REUSED
```

- [ ] **Step 7: Implement task, output, result-hash, and evidence checks**

For terminal tasks, require exact operation, project, service instance, task ID, and result hash binding. Validate `result.data` with the selected capability `output_schema`, then recompute the result hash from canonical result data. Confine file-backed PASS evidence to `artifacts/` relative paths and require SHA-256.

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

- [ ] **Step 8: Run focused and full GREEN tests**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
python -m unittest tests.test_godot_live_editor_contract tests.test_godot_live_editor_runtime_pilot -v
```

Expected: v2 tests PASS and the preserved v1/Pilot suites remain PASS.

- [ ] **Step 9: Commit operation semantics**

```bash
git add \
  tools/validate_godot_live_editor_contract_v2.py \
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
- Consumes: v1 audit documents, v2 manifest/operation documents, and semantic functions from Tasks 3–4.
- Produces: `validate_contract_pair`, deterministic CLI output, `V1_AUDIT_ONLY`, and `V1_MUTATION_AUTHORITY_REJECTED` behavior.

- [ ] **Step 1: Add migration and CLI RED tests**

Use the preserved Pilot manifest as the v1 audit input:

```python
V1_PILOT_MANIFEST = ROOT / "examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
V2_TEMPLATE = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
```

Add tests:

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
```

Add a subprocess test that invokes the CLI with `--mode AUDIT` and `--mode AUTHORIZE`, parses exactly one stdout JSON object, and asserts exit codes `0` and `1` respectively.

- [ ] **Step 2: Run migration tests to verify RED**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because `validate_contract_pair`, CLI behavior, and the v2 template switch are absent.

- [ ] **Step 3: Implement `validate_contract_pair`**

Behavior:

```python
def validate_contract_pair(...):
    kind = classify_contract_document(manifest)
    if kind == "V1_AUDIT_ONLY":
        return [] if mode == "AUDIT" and operation is None else ["V1_MUTATION_AUTHORITY_REJECTED"]
    errors = validate_manifest_semantics(manifest)
    if operation is not None:
        errors.extend(
            validate_operation_semantics(
                manifest,
                operation,
                prior_operations=prior_operations,
                now=now,
            )
        )
    return _unique(errors)
```

Before semantics, load and apply the correct JSON Schema for each v2 document. Emit `MANIFEST_SCHEMA_INVALID` or `OPERATION_SCHEMA_INVALID` rather than raw validator text.

- [ ] **Step 4: Implement the exact CLI**

Use `argparse`, repeatable `--prior-operation`, enum choices for `--mode`, and RFC3339 parsing for `--now`. Print compact JSON once. Do not print stack traces for expected validation failures.

- [ ] **Step 5: Switch the installation template to safe v2**

The template contains:

```json
{
  "schema_version": 2,
  "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
  "configuration_state": "NOT_CONFIGURED",
  "contract_version": "2.0.0",
  "adapter_version": "2.0.0",
  "project_identity": {
    "normalized_project_path": null,
    "project_godot_sha256": null,
    "project_fingerprint": null
  },
  "engine_compatibility": {
    "detected_version": null,
    "minimum_version": "4.3",
    "maximum_exclusive_version": "5.0"
  },
  "tool_adoption": {
    "source": null,
    "exact_version": null,
    "telemetry_policy": "DISABLED",
    "external_data_policy": "DENY_BY_DEFAULT",
    "uninstall_procedure": null,
    "rollback_reference": null
  },
  "transport": {
    "kind": "DISABLED",
    "enabled": false,
    "bind_host": null,
    "endpoint_identity": null,
    "protocol_profile": "GENERIC",
    "protocol_version": null,
    "access_control": {
      "authentication_mode": "NOT_APPLICABLE",
      "origin_policy": "NOT_APPLICABLE",
      "session_binding": "NOT_APPLICABLE",
      "os_access_control": "CURRENT_USER_ONLY"
    }
  },
  "catalog": {
    "generated_at": null,
    "sha256": null,
    "freshness_state": "NOT_CONFIGURED"
  },
  "project_test_framework": {
    "state": "NOT_CONFIGURED",
    "runner_capability_id": null
  },
  "capabilities": [],
  "validation": {
    "contract_state": "CONTRACT_PASS",
    "execution_state": "NOT_RUN",
    "runtime_state": "NOT_RUN",
    "physical_input_state": "NOT_RUN",
    "human_state": "HUMAN_NOT_RUN"
  }
}
```

- [ ] **Step 6: Preserve v1 tests by pointing them at v1 Pilot evidence**

In `tests/test_godot_live_editor_contract.py`, replace the v1 `MANIFEST` constant with:

```python
V1_PILOT_MANIFEST = ROOT / "examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
```

Rename the v1 template test to `test_v1_pilot_manifest_and_representative_configured_manifest_validate` and validate `V1_PILOT_MANIFEST` against the v1 Schema. Keep the existing v1 representative manifest builder and runtime Pilot tests unchanged.

- [ ] **Step 7: Run migration and backward-audit GREEN tests**

Run:

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_runtime_pilot \
  -v
```

Expected: v2 template validates, v1 audit remains readable, and v1 authorize mode fails closed.

- [ ] **Step 8: Commit migration behavior and template switch**

```bash
git add \
  tools/validate_godot_live_editor_contract_v2.py \
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
- Consumes: the implemented v2 files and migration behavior.
- Produces: compact canonical discovery and project-local execution rules that reference v2 without copying the full contract.

- [ ] **Step 1: Add documentation and adapter RED assertions**

Require these exact terms across the canonical docs and adapter:

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

Require the adapter to reference:

```text
schemas/godot-live-editor-capability-manifest-v2.schema.json
schemas/godot-live-editor-operation-envelope-v2.schema.json
tools/validate_godot_live_editor_contract_v2.py
```

Assert the adapter no longer treats `operation_class` as the active v2 authority. Historical migration prose may name it only inside a v1 explanation.

- [ ] **Step 2: Run documentation RED tests**

Run:

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: FAIL because the canonical docs and adapter still describe v1 as active.

- [ ] **Step 3: Update the automation contract**

Add a compact v2 authority section that defines the five axes, exact identity, request material, input/output validation order, task lifecycle, evidence separation, and `MIGRATION_REQUIRED_V1`. Preserve the v1 section as audit history, not active mutation authority.

- [ ] **Step 4: Update security and recovery**

Define exact binding equality, token expiry/reuse, stale-state preconditions, transport-specific access control, result/evidence hashing, and recovery-mode invalidation of old service/Editor approvals.

- [ ] **Step 5: Update production readiness**

Production readiness cannot advance unless:

```text
v2_schema_validation: PASS
v2_semantic_validation: PASS
v1_mutation_authority: REJECTED
editor_main_thread_queue: PASS
editor_undo_redo_transaction: PASS
```

Keep the last two states `NOT_IMPLEMENTED` in this PR.

- [ ] **Step 6: Update the project adapter and AGENTS fragment**

Replace the v1 class table with the five policy axes. The adapter sequence becomes:

```text
validate Base adapter pin
→ classify manifest version
→ reject v1 mutation with MIGRATION_REQUIRED_V1
→ validate v2 Schema
→ validate v2 semantics
→ verify exact target and snapshot
→ execute one typed capability
→ validate output
→ bind result/evidence
```

Keep existing Base owner routing unchanged. Do not add a Registry Skill.

- [ ] **Step 7: Run documentation and routing GREEN tests**

Run:

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_adapter_resolution \
  -v
```

Expected: PASS.

- [ ] **Step 8: Commit canonical and adapter updates**

```bash
git add \
  docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md \
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
- Modify only confirmed failures in the files already listed.
- Update: PR #157 body after exact-head verification.

**Interfaces:**
- Consumes: complete static v2 reconciliation.
- Produces: exact-head evidence, protected-boundary proof, and a Draft PR ready for implementation review.

- [ ] **Step 1: Run focused contract suites**

Run:

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_idempotent_approval \
  tests.test_godot_live_editor_runtime_contract_hardening \
  tests.test_godot_live_editor_adapter_resolution \
  tests.test_godot_live_editor_runtime_pilot \
  -v
```

Expected: PASS; runtime cases requiring an unavailable uploaded binary report their existing explicit skip state rather than PASS.

- [ ] **Step 2: Run required aggregate validation**

Run:

```bash
python -m unittest tests.test_v9_machine_contracts -v
python -m unittest tests.test_local_validation -v
```

Then run the repository’s existing canonical-reference, publication/generation, documentation/whitespace, and required CI commands through the standard GitHub Actions workflows.

- [ ] **Step 3: Attack the v2 contract with an adversarial matrix**

Add or confirm tests for every hypothesis:

```text
read-only capability declares mutation rollback
mutation declares NOT_APPLICABLE idempotency
non-idempotent or irreversible mutation enables automatic retry
long task omits durable task binding
approval binds a different service or Editor instance
approval binds an old catalog or Schema hash
approval token is reused across operation IDs
request arguments contain undeclared fields
result data violates output Schema
request hash omits preconditions
stale target state reaches mutation authority
LOCAL_HTTP uses wildcard/external bind or no Origin/auth/session binding
STDIO writes diagnostics to protocol stdout
PASS evidence lacks artifact path/hash
v1 manifest receives v2 mutation authority
v1 Pilot evidence is rewritten
Registry or release locks change
project adapter becomes a Base active Skill
```

Classify each result as `MUST_FIX`, `SHOULD_FIX`, `REJECTED_CRITIQUE`, or `DEFERRED_TO_PR_B/C/D`. Fix only reproducible PR A contract weaknesses.

- [ ] **Step 4: Verify protected files and scope**

Run:

```bash
sha256sum skills/SKILL_REGISTRY.json
git diff --name-only main...HEAD
git diff --check main...HEAD
```

Confirm:

- Registry SHA-256 remains `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`;
- no release lock or frozen derivative changed;
- v1 Schema and Pilot evidence files are unchanged;
- no game project, Google Sheet, GitHub workflow topology, binary, archive, runtime artifact, or generated Godot UID entered the diff.

- [ ] **Step 5: Inspect exact-head GitHub Actions**

Require success for:

```text
Validate Base v9 Operating Contracts
Validate Game Project Operating System
Validate Evidence-Based Game Development Knowledge
Validate Game UX UI System
```

Within the project operating workflow, require canonical-reference freshness, contract/governance regressions, docs/whitespace, publication/generation, and required `ci-gate`. Record Windows smoke as `SKIPPED_NOT_REQUIRED` when that is the actual result.

- [ ] **Step 6: Recheck PR metadata and review state**

Confirm the PR targets `main`, is mergeable, has zero unresolved review threads, and has not moved from the exact tested head. If `main` advanced, reconcile from latest main without force-pushing unrelated history, then rerun all required checks.

- [ ] **Step 7: Update PR #157 evidence without merging**

The PR body reports:

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

When adversarial review finds a real defect, commit each coherent correction with its regression test. Do not create a cleanup commit when no file changed.

---

## Plan Self-review Results

### Spec coverage

- Orthogonal policy axes: Tasks 2–4.
- Exact project/service/Editor/runtime identity: Tasks 2 and 4.
- Contract and input/output Schema snapshot binding: Tasks 2–4.
- Semantic equality validation: Tasks 3–4.
- Stale-state preconditions: Tasks 2 and 4.
- Transport-specific local security: Tasks 2–3 and Task 7.
- Generic task lifecycle: Tasks 2 and 4.
- Evidence integrity: Tasks 2 and 4.
- Godot recovery mode: Task 6.
- Non-destructive v1 migration: Task 5.
- Registry/release-lock protection: Task 7.
- Production adapter exclusion: Global Constraints and Tasks 6–7.

### Placeholder scan

The plan contains no incomplete requirement markers or unspecified implementation steps. Every code-producing task names files, interfaces, commands, expected outcomes, and commit boundaries.

### Type and naming consistency

The plan consistently uses:

```text
schema_version: 2
capability.input_schema / output_schema
capability_input_schema_sha256 / capability_output_schema_sha256
request.arguments
validate_manifest_semantics
validate_operation_semantics
validate_contract_pair
prior_operations
MIGRATION_REQUIRED_V1
V1_MUTATION_AUTHORITY_REJECTED
```

No v2 implementation step uses the v1 `operation_class` as active authority.
