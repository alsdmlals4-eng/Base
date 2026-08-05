# Godot Live Editor Contract v2 Static Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make contract v2 the only active authority for new Godot automation adoption while keeping the merged v1 runtime Pilot as explicitly isolated legacy compatibility evidence until a separate real-Godot migration runs.

**Architecture:** Add v2 Draft 2020-12 schemas and one Python semantic validator, then migrate canonical Godot documents and project templates to the independent policy-axis model. Preserve v1 only for the existing isolated Pilot, enforce that isolation with tests, and connect every focused test to existing required CI without changing workflow topology.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.12 `unittest`, `jsonschema==4.26.0`, existing Base GitHub Actions and canonical-reference freshness checks.

## Global Constraints

- Do not start implementation until BCP `BCP-2026-005-godot-live-editor-contract-v2` is merged to main with status `APPROVED_FOR_IMPLEMENTATION`, a non-empty approval reference, and the user explicitly authorizes implementation rather than planning only.
- At execution time, re-fetch main and create a fresh isolated branch/worktree from the exact current main commit; do not reuse the planning branch.
- Preserve `skills/SKILL_REGISTRY.json` byte identity and all Base v9.4.3/predecessor release locks and frozen derivatives.
- Do not add a broad active Base Skill, universal MCP server, production network bridge, or arbitrary script/shell/eval capability.
- Do not edit a user game repository, Google Sheet, uploaded Godot binary, or uploaded project configuration.
- Stage A is static-contract work. Do not edit GDScript behavior or claim v2 Godot runtime success.
- Keep existing v1 Pilot runtime files and historical evidence unchanged except for explicit compatibility labeling in documentation/tests.
- No new GitHub Actions workflow. Required suites discover focused tests through existing Python imports.
- All mutation, approval, target, snapshot, task, output, path, and evidence failures must fail closed before a successful result is promoted.
- Use TDD: commit test-only RED before implementation; record the exact RED head and exact failing tests.

---

### Task 1: Lock governance, baseline, and test-only RED

**Files:**
- Create: `tests/test_godot_live_editor_contract_v2.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `tests/test_local_validation.py`
- Read only: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Read only: `[수정제안서]/BCP-2026-005-godot-live-editor-contract-v2/PROPOSAL.md`

**Interfaces:**
- Consumes: merged BCP record with `proposal_id == "BCP-2026-005-godot-live-editor-contract-v2"`, `status == "APPROVED_FOR_IMPLEMENTATION"`, and a non-empty `approval_ref`.
- Produces: `GodotLiveEditorContractV2Tests`, imported by both required aggregate suites.

- [ ] **Step 1: Verify the implementation authorization gate**

+Run:
+
+```bash
+python - <<'PY'
+import json
+from pathlib import Path
+
+registry = json.loads(Path('[수정제안서]/PROPOSAL_REGISTRY.json').read_text(encoding='utf-8'))
+proposal = next(
+    item for item in registry['proposals']
+    if item['proposal_id'] == 'BCP-2026-005-godot-live-editor-contract-v2'
+)
+assert proposal['status'] == 'APPROVED_FOR_IMPLEMENTATION'
+assert isinstance(proposal['approval_ref'], str) and proposal['approval_ref']
+print(proposal['approval_ref'])
+PY
+```
+
+Expected: exit `0` and print the stable approval URL. Stop if the proposal is absent, unmerged, deferred, rejected, or lacks approval.
+
+- [ ] **Step 2: Create v2 test helpers and path constants**
+
+Create `tests/test_godot_live_editor_contract_v2.py` with these public helpers and constants:
+
+```python
+from __future__ import annotations
+
+import copy
+import json
+import tempfile
+import unittest
+from hashlib import sha256
+from pathlib import Path
+
+from jsonschema import Draft202012Validator
+
+ROOT = Path(__file__).resolve().parents[1]
+MANIFEST_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
+OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
+TEMPLATE_MANIFEST = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
+VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract.py"
+V1_COMPAT = ROOT / "docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md"
+
+
+def load(path: Path) -> dict:
+    return json.loads(path.read_text(encoding="utf-8"))
+
+
+def closed_object(properties: dict, required: list[str]) -> dict:
+    return {
+        "$schema": "https://json-schema.org/draft/2020-12/schema",
+        "type": "object",
+        "additionalProperties": False,
+        "required": required,
+        "properties": properties,
+    }
+```
+
+- [ ] **Step 3: Add representative v2 fixtures**
+
+Define `valid_manifest_v2()` and `valid_operation_v2()` with exact values:
+
+```python
+def valid_manifest_v2() -> dict:
+    empty = closed_object({}, [])
+    return {
+        "schema_version": 2,
+        "artifact_role": "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST",
+        "configuration_state": "CONFIGURED",
+        "contract_version": "2.0.0",
+        "adapter_version": "2.0.0",
+        "project_identity": {
+            "normalized_project_path": "/workspace/game",
+            "project_godot_sha256": "a" * 64,
+            "project_fingerprint": "project-a",
+        },
+        "engine_compatibility": {
+            "detected_version": "4.7.1.stable.official.a13da4feb",
+            "minimum_version": "4.7.1",
+            "maximum_exclusive_version": "4.8.0",
+        },
+        "tool_adoption": {
+            "source_type": "PROJECT_LOCAL",
+            "source_reference": "res://tools/live_editor_cli.gd",
+            "version_pin": "sha256:" + "b" * 64,
+            "integrity_reference": "sha256:" + "b" * 64,
+            "license_reference": "project-local",
+            "vulnerability_reviewed_at": "2026-08-05T00:00:00Z",
+            "telemetry_policy": "DISABLED",
+            "external_data_policy": "NO_EXTERNAL_TRANSFER",
+            "uninstall_reference": "docs/uninstall.md",
+            "rollback_reference": "docs/rollback.md",
+        },
+        "transport": {
+            "kind": "CLI",
+            "enabled": True,
+            "bind_host": None,
+            "endpoint_identity": "res://tools/live_editor_cli.gd",
+            "protocol_profile": "GENERIC",
+            "protocol_version": "2.0.0",
+            "access_control": {
+                "authentication_mode": "NOT_APPLICABLE",
+                "origin_policy": "NOT_APPLICABLE",
+                "session_binding": "NOT_APPLICABLE",
+                "os_access_control": "CURRENT_USER_ONLY",
+            },
+        },
+        "catalog": {
+            "generated_at": "2026-08-05T00:00:00Z",
+            "sha256": "c" * 64,
+            "freshness_state": "FRESH",
+        },
+        "project_test_framework": {
+            "state": "NOT_CONFIGURED",
+            "runner_capability_id": None,
+        },
+        "capabilities": [{
+            "capability_id": "scene.inspect",
+            "description": "Inspect one bounded scene summary.",
+            "execution_path": "CLI_HEADLESS",
+            "effect_kind": "READ_ONLY",
+            "idempotency": "NOT_APPLICABLE",
+            "approval_policy": "NOT_REQUIRED",
+            "execution_mode": "SYNCHRONOUS",
+            "rollback_policy": "NOT_APPLICABLE",
+            "input_schema": empty,
+            "output_schema": closed_object({"scene_path": {"type": "string"}}, ["scene_path"]),
+            "precondition_policy": "NONE",
+            "timeout_policy": {"milliseconds": 10000, "unknown_outcome": "SAFE_TO_RETRY"},
+            "retry_policy": {"automatic": True, "maximum_attempts": 2, "requires_ledger": False},
+            "evidence_outputs": ["ENGINE_STATE"],
+            "unsupported_states": ["IMPORTING"],
+        }],
+        "validation": {
+            "contract_state": "CONTRACT_PASS",
+            "execution_state": "NOT_RUN",
+            "runtime_state": "NOT_RUN",
+            "physical_input_state": "NOT_RUN",
+            "human_state": "HUMAN_NOT_RUN",
+        },
+    }
+```
+
+The operation fixture must contain top-level project, instance, snapshot, policy, preconditions, approval, task, result hash, and evidence fields. Use `automation_server_instance_id: "server-a"`, `runtime_session_state: "NOT_APPLICABLE"`, and `protocol_profile: "GENERIC"` so equality tests have stable values.
+
+- [ ] **Step 4: Add RED policy-axis and authority tests**
+
+Add tests with these names and assertions:
+
+```python
+class GodotLiveEditorContractV2Tests(unittest.TestCase):
+    maxDiff = None
+
+    def test_v2_paths_template_and_validator_exist(self) -> None:
+        required = (MANIFEST_SCHEMA, OPERATION_SCHEMA, TEMPLATE_MANIFEST, VALIDATOR, V1_COMPAT)
+        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])
+
+    def test_independent_policy_combinations_are_representable(self) -> None:
+        validator = Draft202012Validator(load(MANIFEST_SCHEMA))
+        manifest = valid_manifest_v2()
+        capability = manifest["capabilities"][0]
+        capability.update({
+            "effect_kind": "MUTATION",
+            "idempotency": "IDEMPOTENT",
+            "approval_policy": "REQUIRED",
+            "execution_mode": "LONG_RUNNING_TASK",
+            "rollback_policy": "SNAPSHOT",
+            "precondition_policy": "REQUIRED",
+            "retry_policy": {"automatic": False, "maximum_attempts": 1, "requires_ledger": True},
+            "timeout_policy": {"milliseconds": 10000, "unknown_outcome": "RESUME_BY_TASK_ID"},
+        })
+        self.assertEqual([], list(validator.iter_errors(manifest)))
+
+    def test_read_only_and_irreversible_invalid_combinations_fail(self) -> None:
+        validator = Draft202012Validator(load(MANIFEST_SCHEMA))
+        read_only = valid_manifest_v2()
+        read_only["capabilities"][0]["idempotency"] = "IDEMPOTENT"
+        self.assertTrue(list(validator.iter_errors(read_only)))
+
+        irreversible = valid_manifest_v2()
+        capability = irreversible["capabilities"][0]
+        capability.update({
+            "effect_kind": "MUTATION",
+            "idempotency": "NON_IDEMPOTENT",
+            "approval_policy": "NOT_REQUIRED",
+            "rollback_policy": "IRREVERSIBLE",
+            "retry_policy": {"automatic": True, "maximum_attempts": 2, "requires_ledger": False},
+        })
+        self.assertTrue(list(validator.iter_errors(irreversible)))
+```
+
+Also add failing tests for LOCAL_HTTP without Origin/auth/session binding, wrong instance/snapshot approval, duplicate capability IDs, missing project-test runner evidence, output mismatch, stale precondition, evidence hash mismatch, and v1 references outside the legacy allowlist.
+
+- [ ] **Step 5: Connect the RED suite to required CI**
+
+Add imports:
+
+```python
+from tests.test_godot_live_editor_contract_v2 import (
+    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
+)
+```
+
+to both `tests/test_v9_machine_contracts.py` and `tests/test_local_validation.py`.
+
+- [ ] **Step 6: Run and record RED**
+
+Run:
+
+```bash
+python -m unittest tests.test_godot_live_editor_contract_v2 -v
+python -m unittest tests.test_v9_machine_contracts -v
+```
+
+Expected: failures for missing v2 schemas, validator, compatibility document, v2 template fields, and semantic rejection behavior. Existing release-integrity checks must remain PASS.
+
+- [ ] **Step 7: Commit RED only**
+
+```bash
+git add tests/test_godot_live_editor_contract_v2.py \
+  tests/test_v9_machine_contracts.py \
+  tests/test_local_validation.py
+git commit -m "test: define Godot live-editor contract v2"
+```
+
+---
+
+### Task 2: Add strict v2 schemas
+
+**Files:**
+- Create: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
+- Create: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
+- Test: `tests/test_godot_live_editor_contract_v2.py`
+
+**Interfaces:**
+- Consumes: Draft 2020-12 and the exact enums in the approved specification.
+- Produces: schema-valid v2 manifests/envelopes; cross-document equality remains the semantic validator's responsibility.
+
+- [ ] **Step 1: Implement the capability-manifest v2 shape**
+
+Require these top-level keys with `additionalProperties: false`:
+
+```json
+[
+  "schema_version", "artifact_role", "configuration_state",
+  "contract_version", "adapter_version", "project_identity",
+  "engine_compatibility", "tool_adoption", "transport", "catalog",
+  "project_test_framework", "capabilities", "validation"
+]
+```
+
+Use constants `schema_version: 2`, `artifact_role: GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST`, and semver `contract_version/adapter_version`. A configured manifest requires complete identity, detected/min/max engine versions, exact tool version/integrity/license/review records, enabled secure transport, fresh catalog, and at least one capability. `NOT_CONFIGURED` requires null identity/tool/transport/catalog fields and an empty capability array.
+
+- [ ] **Step 2: Implement capability policy conditions**
+
+Enforce this matrix through `allOf` conditions:
+
+```text
+READ_ONLY:
+  idempotency = NOT_APPLICABLE
+  approval_policy = NOT_REQUIRED
+  rollback_policy = NOT_APPLICABLE
+
+MUTATION:
+  idempotency = IDEMPOTENT | NON_IDEMPOTENT
+  rollback_policy != NOT_APPLICABLE
+
+IDEMPOTENT:
+  retry_policy.requires_ledger = true
+
+NON_IDEMPOTENT:
+  retry_policy.automatic = false
+  retry_policy.maximum_attempts <= 1
+
+IRREVERSIBLE:
+  approval_policy = REQUIRED
+  retry_policy.automatic = false
+  retry_policy.maximum_attempts <= 1
+
+LONG_RUNNING_TASK:
+  retry_policy.requires_ledger = true
+  timeout_policy.unknown_outcome = RESUME_BY_TASK_ID
+
+SYNCHRONOUS:
+  timeout_policy.unknown_outcome != RESUME_BY_TASK_ID
+```
+
+Require closed object `input_schema` and `output_schema` declarations and a non-empty `evidence_outputs` array.
+
+- [ ] **Step 3: Implement transport-kind conditions**
+
+Enforce:
+
+```text
+LOCAL_HTTP:
+  bind_host = 127.0.0.1 | ::1
+  origin_policy = EXPLICIT_ALLOWLIST
+  authentication_mode = SESSION_TOKEN | OAUTH_2_1
+  session_binding = PROJECT_CLIENT_SESSION
+
+CLI:
+  bind_host = null
+  authentication_mode = NOT_APPLICABLE
+  origin_policy = NOT_APPLICABLE
+  session_binding = NOT_APPLICABLE
+  os_access_control = CURRENT_USER_ONLY
+
+STDIO_BRIDGE:
+  bind_host = null
+  origin_policy = NOT_APPLICABLE
+  os_access_control = CURRENT_USER_ONLY
+
+NAMED_PIPE:
+  bind_host = null
+  authentication_mode = OS_PEER_CREDENTIAL | NOT_APPLICABLE
+  os_access_control = CURRENT_USER_ONLY
+```
+
+Keep wildcard/external hosts unrepresentable.
+
+- [ ] **Step 4: Implement operation-envelope v2 shape**
+
+Require:
+
+```json
+[
+  "schema_version", "artifact_role", "operation_id", "capability_id",
+  "project_identity", "instance_identity", "contract_snapshot", "policy",
+  "request_hash", "idempotency_key", "preconditions", "approval",
+  "task", "result"
+]
+```
+
+The operation schema must structurally constrain:
+
+- instance identity and active runtime state;
+- exact policy enums;
+- null/non-null idempotency key by policy;
+- precondition shape and fixed `conflict_policy: FAIL_CLOSED`;
+- approval state/token/expiry shape;
+- synchronous `NOT_APPLICABLE` task versus long-task lifecycle;
+- terminal task result binding and `result_hash`;
+- evidence kind/state family, confined relative path shape, file hash, generation time, and producer.
+
+- [ ] **Step 5: Run schema-only GREEN checks**
+
+Run:
+
+```bash
+python -m unittest \
+  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_independent_policy_combinations_are_representable \
+  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_read_only_and_irreversible_invalid_combinations_fail \
+  -v
+```
+
+Expected: policy and transport structural tests pass; semantic equality tests still fail because the validator does not exist.
+
+- [ ] **Step 6: Commit schemas**
+
+```bash
+git add schemas/godot-live-editor-capability-manifest-v2.schema.json \
+  schemas/godot-live-editor-operation-envelope-v2.schema.json
+git commit -m "feat: add Godot live-editor v2 schemas"
+```
+
+---
+
+### Task 3: Add executable semantic validation
+
+**Files:**
+- Create: `tools/validate_godot_live_editor_contract.py`
+- Modify: `tests/test_godot_live_editor_contract_v2.py`
+
+**Interfaces:**
+- Produces: `ValidationIssue`, `canonical_sha256`, `validate_manifest_semantics`, `validate_operation_semantics`, `validate_contract_files`, and a CLI `main(argv: list[str] | None = None) -> int`.
+- Returns all reproducible issues; the CLI exits `0` only when the issue list is empty.
+
+- [ ] **Step 1: Define deterministic types and hashing**
+
+Use this exact public surface:
+
+```python
+from __future__ import annotations
+
+import argparse
+import json
+from dataclasses import dataclass
+from hashlib import sha256
+from pathlib import Path
+from typing import Any, Mapping, Sequence
+
+from jsonschema import Draft202012Validator
+
+
+@dataclass(frozen=True)
+class ValidationIssue:
+    code: str
+    path: str
+    message: str
+
+
+def canonical_sha256(value: Any) -> str:
+    encoded = json.dumps(
+        value,
+        ensure_ascii=False,
+        sort_keys=True,
+        separators=(",", ":"),
+    ).encode("utf-8")
+    return sha256(encoded).hexdigest()
+```
+
+- [ ] **Step 2: Implement manifest semantics**
+
+Implement:
+
+```python
+def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[ValidationIssue]:
+```
+
+It must emit stable codes for duplicate capability IDs, missing/ambiguous project-test runner, runner without `TEST_RESULT`, invalid policy combinations not expressible in Schema, invalid nested input/output schemas, and transport profile contradictions.
+
+Validate each nested schema with `Draft202012Validator.check_schema(...)`; report `INPUT_SCHEMA_INVALID` or `OUTPUT_SCHEMA_INVALID` with the capability array index.
+
+- [ ] **Step 3: Implement path and evidence verification**
+
+Use canonical confinement:
+
+```python
+def resolve_confined(root: Path, relative: str) -> Path:
+    candidate = (root / relative).resolve(strict=True)
+    resolved_root = root.resolve(strict=True)
+    if candidate == resolved_root or resolved_root not in candidate.parents:
+        raise ValueError("PATH_OUTSIDE_APPROVED_ROOT")
+    return candidate
+
+
+def file_sha256(path: Path) -> str:
+    digest = sha256()
+    with path.open("rb") as handle:
+        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
+            digest.update(chunk)
+    return digest.hexdigest()
+```
+
+Reject traversal, absolute paths, symlink escape, missing artifacts, and hash mismatch. Do not follow a path outside the supplied project root.
+
+- [ ] **Step 4: Implement operation equality and output validation**
+
+Implement:
+
+```python
+def validate_operation_semantics(
+    manifest: Mapping[str, Any],
+    operation: Mapping[str, Any],
+    project_root: Path | None = None,
+) -> list[ValidationIssue]:
+```
+
+The function must:
+
+1. resolve exactly one declared capability;
+2. compare operation policy with that capability;
+3. compare project identity, instance identity, and complete contract snapshot across top level, approval binding, task result binding, and ledger/result binding;
+4. recompute the normalized request hash from capability ID, arguments, target identity, snapshot, policy, and preconditions;
+5. validate `result.data` against the declared output schema;
+6. recompute `result_hash` from terminal result data and evidence metadata;
+7. verify file-backed PASS evidence when `project_root` is supplied;
+8. reject inactive/wrong runtime sessions, stale preconditions, and terminal task results from another instance/snapshot.
+
+Use stable codes from the approved spec, including `CAPABILITY_NOT_DECLARED`, `APPROVAL_TOKEN_MISMATCH`, `AUTOMATION_INSTANCE_MISMATCH`, `EDITOR_INSTANCE_MISMATCH`, `RUNTIME_SESSION_MISMATCH`, `CONTRACT_SNAPSHOT_MISMATCH`, `OUTPUT_SCHEMA_MISMATCH`, `TARGET_STATE_CONFLICT`, `TASK_RESULT_STALE`, `RESULT_HASH_MISMATCH`, `PATH_OUTSIDE_APPROVED_ROOT`, and `EVIDENCE_HASH_MISMATCH`.
+
+- [ ] **Step 5: Add a fail-closed CLI**
+
+Accept:
+
+```text
+--manifest PATH
+--manifest-schema PATH
+--operation PATH (optional)
+--operation-schema PATH (required with --operation)
+--project-root PATH (optional)
+```
+
+Print JSON:
+
+```json
+{
+  "valid": false,
+  "issues": [{"code": "...", "path": "...", "message": "..."}]
+}
+```
+
+Return `0` for no issues, `1` for validation issues, and `2` for unreadable/invalid CLI inputs.
+
+- [ ] **Step 6: Run semantic adversarial tests**
+
+Run:
+
+```bash
+python -m unittest tests.test_godot_live_editor_contract_v2 -v
+```
+
+Expected: instance/snapshot/output/task/path/evidence tests pass. Tests for missing docs/template migration remain RED.
+
+- [ ] **Step 7: Commit validator**
+
+```bash
+git add tools/validate_godot_live_editor_contract.py \
+  tests/test_godot_live_editor_contract_v2.py
+git commit -m "feat: validate Godot live-editor v2 semantics"
+```
+
+---
+
+### Task 4: Migrate active documents and project templates to v2
+
+**Files:**
+- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
+- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
+- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
+- Modify: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
+- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
+- Modify: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
+- Modify: `tests/test_godot_live_editor_contract.py`
+- Modify: `tests/test_godot_live_editor_idempotent_approval.py`
+
+**Interfaces:**
+- Active canonical paths select `*-v2.schema.json` and `contract_version: 2.0.0`.
+- Project adapter runs JSON Schema validation, then `tools/validate_godot_live_editor_contract.py`, before engine action.
+
+- [ ] **Step 1: Migrate canonical terminology**
+
+Replace active `operation_class` guidance with the five policy axes. Add exact target/snapshot binding, closed output validation, stale-state preconditions, task core, evidence hashes, transport conditions, stable error codes, and `--recovery-mode` flow.
+
+Keep these boundaries explicit:
+
+```yaml
+production_network_mcp_transport: NOT_IMPLEMENTED
+editor_main_thread_mutation_queue: NOT_IMPLEMENTED
+editor_undo_redo_transaction: NOT_IMPLEMENTED
+runtime_debugger_bridge: NOT_IMPLEMENTED
+project_test_framework: NOT_CONFIGURED
+physical_input_validation: NOT_RUN
+human_editor_usability: HUMAN_NOT_RUN
+production_adapter_ready: false
+```
+
+- [ ] **Step 2: Replace the project template with a safe v2 manifest**
+
+Set:
+
+```json
+{
+  "schema_version": 2,
+  "configuration_state": "NOT_CONFIGURED",
+  "contract_version": "2.0.0",
+  "adapter_version": "2.0.0",
+  "project_identity": {
+    "normalized_project_path": null,
+    "project_godot_sha256": null,
+    "project_fingerprint": null
+  },
+  "capabilities": []
+}
+```
+
+Include all required v2 engine, tool-adoption, transport/access-control, catalog, project-test, and validation fields with null or `NOT_CONFIGURED` values. The template must validate but must not imply an installed tool, enabled endpoint, runtime evidence, or adoption decision.
+
+- [ ] **Step 3: Migrate the project-local adapter**
+
+The adapter workflow must be:
+
+```text
+validate PROJECT_BASE_ADAPTER pin
+→ load v2 template/manifest
+→ validate v2 JSON Schema
+→ run semantic validator
+→ resolve exactly one typed capability
+→ observe target and compute preconditions
+→ obtain approval when policy requires it
+→ execute through declared path
+→ validate structured output
+→ hash evidence/result
+→ validate again
+→ report exact states and rollback
+```
+
+Stop on v1 manifest selection except in the isolated legacy Pilot path. Never auto-upgrade a user project manifest in place.
+
+- [ ] **Step 4: Keep the AGENTS fragment compact**
+
+List only discovery paths, validation commands, stop codes, approved-root facts, and report fields. Do not copy the full canonical contract into the fragment.
+
+- [ ] **Step 5: Migrate active static tests**
+
+Update `tests/test_godot_live_editor_contract.py` to load v2 schemas and the v2 template. Update `tests/test_godot_live_editor_idempotent_approval.py` so the valid case is:
+
+```text
+effect_kind = MUTATION
+idempotency = IDEMPOTENT
+approval_policy = REQUIRED
+execution_mode = SYNCHRONOUS
+rollback_policy = SNAPSHOT
+```
+
+and proves the approval token binds to target identity, contract snapshot, policy, request hash, and preconditions.
+
+- [ ] **Step 6: Run active-contract tests**
+
+Run:
+
+```bash
+python -m unittest \
+  tests.test_godot_live_editor_contract \
+  tests.test_godot_live_editor_idempotent_approval \
+  tests.test_godot_live_editor_contract_v2 \
+  -v
+```
+
+Expected: all active v2 tests pass; legacy Pilot tests remain unchanged.
+
+- [ ] **Step 7: Commit active migration**
+
+```bash
+git add docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md \
+  docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md \
+  docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md \
+  templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
+  templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md \
+  templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md \
+  tests/test_godot_live_editor_contract.py \
+  tests/test_godot_live_editor_idempotent_approval.py
+git commit -m "feat: migrate active Godot automation contract to v2"
+```
+
+---
+
+### Task 5: Isolate v1 as legacy Pilot compatibility only
+
+**Files:**
+- Create: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
+- Modify: `docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md`
+- Modify: `docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md`
+- Modify: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md`
+- Modify: `tests/test_godot_live_editor_runtime_contract_hardening.py`
+- Modify: `tests/test_godot_live_editor_runtime_pilot.py`
+- Preserve unchanged: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
+- Preserve unchanged: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
+- Preserve unchanged: `examples/godot-live-editor-pilot/**`
+
+**Interfaces:**
+- v1 is a frozen compatibility dependency for the existing Pilot only.
+- No active template, adapter, canonical contract, or new project adoption route may select v1.
+
+- [ ] **Step 1: Write the compatibility boundary**
+
+The new document must state:
+
+```yaml
+authority: LEGACY_PILOT_COMPAT_ONLY
+new_project_adoption: PROHIBITED
+template_selection: V2_ONLY
+runtime_evidence_generation: HISTORICAL_V1
+v2_runtime_migration: NOT_RUN
+deletion_gate: V2_RUNTIME_PILOT_GREEN
+```
+
+List the exact allowed v1 references:
+
+```text
+schemas/godot-live-editor-capability-manifest-v1.schema.json
+schemas/godot-live-editor-operation-envelope-v1.schema.json
+examples/godot-live-editor-pilot/**
+tests/test_godot_live_editor_runtime_contract_hardening.py
+tests/test_godot_live_editor_runtime_pilot.py
+docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md
+docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md
+docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md
+```
+
+- [ ] **Step 2: Mark Pilot evidence honestly**
+
+Add prominent notes to Pilot design/plan/evidence:
+
+```yaml
+contract_generation: V1_LEGACY_PILOT
+historical_godot_execution: PASS
+v2_contract_static: SEPARATE
+v2_godot_execution: NOT_RUN
+production_adapter_ready: false
+```
+
+Do not edit captured counts/hashes as though v2 ran.
+
+- [ ] **Step 3: Add a v1 reference allowlist test**
+
+In `tests/test_godot_live_editor_contract_v2.py`, scan tracked text under active docs/templates/tools/tests and fail when `-v1.schema.json` or `schema_version": 1` appears outside the exact allowlist. Exclude `.git`, `.godot`, binary files, and historical PR/design text that quotes v1 only as migration history.
+
+- [ ] **Step 4: Make Pilot tests explicitly legacy**
+
+Rename local constants, not files/classes, so tests read `LEGACY_MANIFEST_SCHEMA` and `LEGACY_OPERATION_SCHEMA`. Add assertions that the v1 compatibility document exists and that the active template is schema version 2.
+
+- [ ] **Step 5: Run legacy isolation and Pilot static tests**
+
+Run:
+
+```bash
+python -m unittest \
+  tests.test_godot_live_editor_runtime_contract_hardening \
+  tests.test_godot_live_editor_runtime_pilot \
+  tests.test_godot_live_editor_contract_v2 \
+  -v
+```
+
+Expected: static tests pass. Runtime cases requiring an unavailable Godot binary remain explicit skips, not PASS.
+
+- [ ] **Step 6: Commit legacy isolation**
+
+```bash
+git add docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md \
+  docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md \
+  docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md \
+  docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md \
+  tests/test_godot_live_editor_runtime_contract_hardening.py \
+  tests/test_godot_live_editor_runtime_pilot.py \
+  tests/test_godot_live_editor_contract_v2.py
+git commit -m "docs: isolate Godot v1 runtime Pilot compatibility"
+```
+
+---
+
+### Task 6: Full regression, adversarial review, and exact-head evidence
+
+**Files:**
+- Modify only confirmed findings from review.
+- Update Draft implementation PR body after verification.
+
+**Interfaces:**
+- Consumes: all previous task commits.
+- Produces: exact-head and current-main merge-ref evidence with zero unresolved MUST_FIX findings.
+
+- [ ] **Step 1: Run focused and repository suites**
+
+Run:
+
+```bash
+python -m unittest \
+  tests.test_godot_live_editor_contract \
+  tests.test_godot_live_editor_contract_v2 \
+  tests.test_godot_live_editor_idempotent_approval \
+  tests.test_godot_live_editor_runtime_contract_hardening \
+  tests.test_godot_live_editor_runtime_pilot \
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
+- [ ] **Step 2: Verify protected bytes and file scope**
+
+Run:
+
+```bash
+git diff --check main...HEAD
+git diff --name-status main...HEAD
+git diff --exit-code main...HEAD -- skills/SKILL_REGISTRY.json
+git diff --exit-code main...HEAD -- 'release/**' 'docs/releases/**'
+sha256sum skills/SKILL_REGISTRY.json
+```
+
+Confirm no `.godot/`, runtime artifact, Godot executable/archive, user project file, temporary payload, or new workflow is tracked.
+
+- [ ] **Step 3: Execute adversarial review hypotheses**
+
+Attempt and require fail-closed results for:
+
+```text
+approval reused after catalog/schema/adapter/protocol change
+approval reused on another automation or Editor instance
+inactive/wrong runtime session
+idempotent mutation without ledger
+non-idempotent or irreversible automatic retry
+LOCAL_HTTP without Origin/auth/session controls
+session ID treated as authentication
+open input or output schema
+output mismatch promoted to success
+stale revision/hash or unexpected dirty Scene
+path traversal and symlink escape
+PASS evidence without artifact hash
+terminal task result from another instance/snapshot
+v1 selected by active template/adapter
+runtime/human readiness inferred from static v2 files
+```
+
+Classify every finding as `MUST_FIX`, `SHOULD_FIX`, `NICE_TO_HAVE`, or `REJECTED_CRITIQUE`. Fix all reproducible MUST_FIX and Important findings before continuing.
+
+- [ ] **Step 4: Request independent code review**
+
+Provide the reviewer only:
+
+```text
+base SHA
+head SHA
+approved spec path
+BCP ID and approval reference
+changed-file inventory
+test commands/results
+protected boundaries
+known NOT_RUN evidence
+```
+
+Do not claim independent review when no reviewer is available.
+
+- [ ] **Step 5: Verify current merge ref and GitHub Actions**
+
+Re-fetch main immediately before final verification. If main moved, create/test a fresh merge ref; do not rely on old exact-head results. Require:
+
+```yaml
+Validate Base v9 Operating Contracts: SUCCESS
+Validate Game Project Operating System: SUCCESS
+canonical reference freshness: SUCCESS
+contract and governance regressions: SUCCESS
+required ci-gate: SUCCESS
+unresolved review threads: 0
+```
+
+Record runtime jobs skipped for missing local Godot as `SKIPPED_NOT_CONFIGURED`.
+
+- [ ] **Step 6: Update PR evidence without merging**
+
+Report:
+
+```yaml
+static_v2_schema: PASS
+semantic_validator: PASS
+active_template_and_adapter: V2
+v1_authority: LEGACY_PILOT_COMPAT_ONLY
+historical_v1_godot_runtime: PRESERVED
+v2_godot_runtime: NOT_RUN
+production_adapter_ready: false
+registry_and_release_locks: UNCHANGED
+merge: NOT_AUTHORIZED
+```
+
+- [ ] **Step 7: Final verification commit only when needed**
+
+Commit only reproducible review fixes or evidence-document corrections. Do not create a cosmetic commit merely to change timestamps.
+
+---
+
+## Completion Gate
+
+Stage A is complete only when:
+
+```yaml
+bcp_merged_and_approved: true
+implementation_authorized: true
+current_main_reconciled: true
+test_only_red_recorded: true
+v2_schema_green: true
+semantic_validator_green: true
+active_contract_template_adapter_v2: true
+v1_new_adoption_prohibited: true
+legacy_pilot_static_regression_green: true
+v2_runtime_claim: NOT_RUN
+repository_regressions_green: true
+current_merge_ref_ci: PASS
+unresolved_must_fix: 0
+unresolved_review_threads: 0
+registry_release_locks_unchanged: true
+```
+
+The implementation PR remains Draft until the user separately authorizes merge. Stage B runtime migration is governed by `docs/superpowers/plans/2026-08-05-godot-live-editor-v2-runtime-pilot-migration.md`.
