# Godot Live Editor Contract v2 Static Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` during implementation, `superpowers:requesting-code-review` before readiness, and `superpowers:verification-before-completion` before any completion claim. Use checkbox (`- [ ]`) steps for progress tracking.

**Goal:** Make contract v2 the only active authority for new Godot automation adoption while retaining the merged v1 Godot 4.7.1 Pilot only as explicitly bounded legacy compatibility evidence until a separate real-engine migration succeeds.

**Architecture:** Add v2 JSON Schemas and one executable semantic validator, migrate canonical Godot documents and project templates to independent policy axes, and prevent active routing to v1. Keep the existing v1 Pilot implementation and historical evidence unchanged in this stage. Connect focused tests to existing required CI modules; do not add workflow topology.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.12 `unittest`, `jsonschema==4.26.0`, existing Base GitHub Actions, canonical-reference freshness checks.

## Global constraints

- Do not begin implementation until `BCP-2026-005-godot-live-editor-contract-v2` is merged to main with `APPROVED_FOR_IMPLEMENTATION`, a non-empty `approval_ref`, and a new explicit user authorization to implement rather than merely plan.
- At execution time, re-fetch main and create a fresh isolated branch/worktree from the exact current main commit. Never implement on this planning branch.
- Preserve `skills/SKILL_REGISTRY.json`, Base v9.4.3 and predecessor release locks, and frozen release derivatives byte-for-byte.
- Do not add a broad active Base Skill, universal MCP server, production network bridge, arbitrary shell/script/eval capability, or user-project automation.
- Stage A is static-contract work. Do not modify GDScript behavior or claim v2 Godot runtime success.
- Keep existing v1 Pilot runtime files and captured runtime evidence unchanged except for explicit compatibility labels in surrounding documentation/tests.
- No new GitHub Actions workflow. Existing required aggregate tests must import the focused v2 test class.
- Use TDD: commit a test-only RED state before implementation and record exact RED head and failing test names.
- JSON Schema validates shape and local combinations. Cross-field equality, hash checks, path confinement, output validation, and evidence integrity belong to the semantic validator.
- All validation failures must stop before engine mutation or successful evidence promotion.

---

## Task 1: Lock governance and create the test-only RED state

**Files:**

- Create: `tests/test_godot_live_editor_contract_v2.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `tests/test_local_validation.py`
- Read only: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Read only: `[수정제안서]/BCP-2026-005-godot-live-editor-contract-v2/PROPOSAL.md`

**Interfaces:**

- Input: merged BCP record with exact proposal ID, approved status, and approval reference.
- Output: `GodotLiveEditorContractV2Tests`, discovered by both required aggregate suites.

- [ ] **Step 1: Verify implementation authorization**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path

registry = json.loads(
    Path('[수정제안서]/PROPOSAL_REGISTRY.json').read_text(encoding='utf-8')
)
proposal = next(
    item for item in registry['proposals']
    if item['proposal_id'] == 'BCP-2026-005-godot-live-editor-contract-v2'
)
assert proposal['status'] == 'APPROVED_FOR_IMPLEMENTATION'
assert isinstance(proposal['approval_ref'], str) and proposal['approval_ref']
print(proposal['approval_ref'])
PY
```

Expected: exit `0` and a stable approval URL. Stop when the proposal is absent, unmerged, deferred, rejected, or unapproved.

- [ ] **Step 2: Create v2 test helpers and constants**

Create this public surface in `tests/test_godot_live_editor_contract_v2.py`:

```python
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = ROOT / 'schemas/godot-live-editor-capability-manifest-v2.schema.json'
OPERATION_SCHEMA = ROOT / 'schemas/godot-live-editor-operation-envelope-v2.schema.json'
TEMPLATE_MANIFEST = ROOT / 'templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json'
VALIDATOR = ROOT / 'tools/validate_godot_live_editor_contract.py'
V1_COMPAT = ROOT / 'docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md'


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def closed_object(properties: dict, required: list[str]) -> dict:
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object',
        'additionalProperties': False,
        'required': required,
        'properties': properties,
    }
```

- [ ] **Step 3: Add representative v2 fixtures**

Define `valid_manifest_v2()` and `valid_operation_v2()` with stable values for:

- `schema_version: 2`
- `contract_version` and `adapter_version`: `2.0.0`
- complete project identity and detected Godot version
- project-local tool adoption with version/integrity/license/review records
- secure CLI transport using current-user access
- fresh catalog hash
- one closed read-only `scene.inspect` capability
- instance identity `server-a`, no Editor/runtime session
- complete contract snapshot
- read-only synchronous policy
- `NOT_APPLICABLE` preconditions, approval, and task
- output-schema-valid result data
- evidence entry with stable kind/state/path/hash/producer fields

The fixtures are test data only. They must not imply that a project is configured or runtime-validated.

- [ ] **Step 4: Add RED tests**

Add named tests for:

```text
test_v2_paths_template_and_validator_exist
test_independent_policy_combinations_are_representable
test_read_only_and_irreversible_invalid_combinations_fail
test_transport_profiles_fail_closed
test_duplicate_capability_and_project_test_runner_fail
test_approval_binds_target_snapshot_policy_request_and_preconditions
test_output_schema_mismatch_fails
test_stale_precondition_fails
test_task_result_from_another_instance_or_snapshot_fails
test_evidence_path_and_hash_are_verified
test_active_surfaces_do_not_select_v1
```

The valid policy-combination test must represent:

```text
MUTATION + IDEMPOTENT + REQUIRED + LONG_RUNNING_TASK + SNAPSHOT
```

Invalid cases must include:

- read-only with mutation idempotency or rollback
- mutation with `NOT_APPLICABLE` idempotency
- non-idempotent automatic retry
- irreversible operation without approval
- LOCAL_HTTP without Origin/authentication/session binding
- wildcard/external bind
- duplicate capability ID
- configured project-test runner missing from capabilities or lacking `TEST_RESULT`

- [ ] **Step 5: Connect focused tests to required CI**

Add this import to both aggregate modules:

```python
from tests.test_godot_live_editor_contract_v2 import (
    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
)
```

- [ ] **Step 6: Run and record RED**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
python -m unittest tests.test_v9_machine_contracts -v
```

Expected RED causes: missing v2 schemas, validator, v1 compatibility document, v2 template fields, and semantic rejection behavior. Existing release-integrity checks must remain PASS.

- [ ] **Step 7: Commit RED only**

```bash
git add tests/test_godot_live_editor_contract_v2.py \
  tests/test_v9_machine_contracts.py \
  tests/test_local_validation.py
git commit -m 'test: define Godot live-editor contract v2'
```

---

## Task 2: Add strict v2 JSON Schemas

**Files:**

- Create: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Create: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Test: `tests/test_godot_live_editor_contract_v2.py`

**Interfaces:**

- Input: approved independent policy-axis design.
- Output: Draft 2020-12 schemas for v2 manifest and operation envelope.

- [ ] **Step 1: Implement capability-manifest v2 top-level shape**

Require with `additionalProperties: false`:

```json
[
  "schema_version",
  "artifact_role",
  "configuration_state",
  "contract_version",
  "adapter_version",
  "project_identity",
  "engine_compatibility",
  "tool_adoption",
  "transport",
  "catalog",
  "project_test_framework",
  "capabilities",
  "validation"
]
```

Use constants:

```text
schema_version = 2
artifact_role = GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST
```

A `CONFIGURED` manifest requires complete project identity, detected/minimum/maximum engine versions, exact tool adoption records, enabled secure transport, fresh catalog, and at least one capability. `NOT_CONFIGURED` requires null/unconfigured identity, tool, transport, catalog, test-framework, and an empty capabilities array.

- [ ] **Step 2: Implement capability policy conditions**

Enforce mechanically:

```text
READ_ONLY:
  idempotency = NOT_APPLICABLE
  approval_policy = NOT_REQUIRED
  rollback_policy = NOT_APPLICABLE

MUTATION:
  idempotency = IDEMPOTENT | NON_IDEMPOTENT
  rollback_policy != NOT_APPLICABLE

IDEMPOTENT:
  requires_ledger = true

NON_IDEMPOTENT:
  automatic retry = false
  maximum_attempts <= 1

IRREVERSIBLE:
  approval_policy = REQUIRED
  automatic retry = false
  maximum_attempts <= 1

LONG_RUNNING_TASK:
  requires_ledger = true
  unknown_outcome = RESUME_BY_TASK_ID

SYNCHRONOUS:
  unknown_outcome != RESUME_BY_TASK_ID
```

Require closed object `input_schema` and `output_schema`, `precondition_policy`, timeout/retry policy, non-empty evidence outputs, and unsupported states.

- [ ] **Step 3: Implement transport-specific conditions**

```text
LOCAL_HTTP:
  host = 127.0.0.1 | ::1
  origin = EXPLICIT_ALLOWLIST
  authentication = SESSION_TOKEN | OAUTH_2_1
  session binding = PROJECT_CLIENT_SESSION

CLI:
  no bind host
  no HTTP auth/origin/session fields
  CURRENT_USER_ONLY OS access

STDIO_BRIDGE:
  no bind host or HTTP Origin
  CURRENT_USER_ONLY OS access

NAMED_PIPE:
  no bind host
  OS peer credential and/or CURRENT_USER_ONLY access
```

Remote and wildcard hosts remain unrepresentable.

- [ ] **Step 4: Implement operation-envelope v2 shape**

Require:

```json
[
  "schema_version",
  "artifact_role",
  "operation_id",
  "capability_id",
  "arguments",
  "project_identity",
  "instance_identity",
  "contract_snapshot",
  "policy",
  "request_hash",
  "idempotency_key",
  "preconditions",
  "approval",
  "task",
  "result"
]
```

Constrain:

- project/server/Editor/runtime identity fields
- complete policy object
- null/non-null idempotency key by policy
- precondition shape with fixed `conflict_policy: FAIL_CLOSED`
- approval state, token binding, and expiry shape
- synchronous task `NOT_APPLICABLE` versus long-task lifecycle
- terminal task result binding and result hash
- evidence kind/state family, relative path, SHA-256, timestamp, and producer

Schema does not attempt cross-object equality; semantic validation handles equality and content hashes.

- [ ] **Step 5: Run schema-focused tests**

```bash
python -m unittest \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_independent_policy_combinations_are_representable \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_read_only_and_irreversible_invalid_combinations_fail \
  tests.test_godot_live_editor_contract_v2.GodotLiveEditorContractV2Tests.test_transport_profiles_fail_closed \
  -v
```

Expected: structural tests pass; semantic equality/hash tests remain RED.

- [ ] **Step 6: Commit schemas**

```bash
git add schemas/godot-live-editor-capability-manifest-v2.schema.json \
  schemas/godot-live-editor-operation-envelope-v2.schema.json
git commit -m 'feat: add Godot live-editor v2 schemas'
```

---

## Task 3: Add executable semantic validation

**Files:**

- Create: `tools/validate_godot_live_editor_contract.py`
- Modify: `tests/test_godot_live_editor_contract_v2.py`

**Public interfaces:**

```python
@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str


def canonical_sha256(value: object) -> str: ...

def validate_manifest_semantics(manifest: Mapping[str, object]) -> list[ValidationIssue]: ...

def validate_operation_semantics(
    manifest: Mapping[str, object],
    operation: Mapping[str, object],
    project_root: Path | None = None,
) -> list[ValidationIssue]: ...

def validate_contract_files(...) -> list[ValidationIssue]: ...

def main(argv: list[str] | None = None) -> int: ...
```

- [ ] **Step 1: Implement deterministic hashing**

```python
def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(',', ':'),
    ).encode('utf-8')
    return sha256(encoded).hexdigest()
```

- [ ] **Step 2: Validate manifest semantics**

Detect with stable codes:

- duplicate capability IDs
- missing/ambiguous configured test runner
- runner lacking `TEST_RESULT` evidence
- invalid nested input/output JSON Schemas using `Draft202012Validator.check_schema`
- cross-axis contradictions not fully expressed by Schema
- transport profile contradictions
- undeclared/unsafe paths or execution paths

- [ ] **Step 3: Implement confined file verification**

```python
def resolve_confined(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise ValueError('PATH_OUTSIDE_APPROVED_ROOT')
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / relative).resolve(strict=True)
    if candidate == resolved_root or resolved_root not in candidate.parents:
        raise ValueError('PATH_OUTSIDE_APPROVED_ROOT')
    return candidate
```

Verify file-backed PASS evidence exists, stays under the approved root after symlink resolution, and matches `artifact_sha256`.

- [ ] **Step 4: Validate operation semantics**

The validator must:

1. resolve exactly one declared capability;
2. compare operation policy with the declared capability;
3. compare project identity, relevant instance identity, and complete contract snapshot across the top level, approval token, task result binding, and ledger/result binding;
4. recompute normalized request hash from capability ID, arguments, target identity, snapshot, policy, and preconditions;
5. validate `result.data` against the declared output schema;
6. recompute terminal result hash;
7. reject inactive/wrong runtime sessions;
8. reject stale preconditions;
9. verify file-backed evidence when a project root is provided.

Use stable codes including:

```text
CAPABILITY_NOT_DECLARED
DUPLICATE_CAPABILITY_ID
PROJECT_TEST_RUNNER_INVALID
PROJECT_IDENTITY_MISMATCH
AUTOMATION_INSTANCE_MISMATCH
EDITOR_INSTANCE_MISMATCH
RUNTIME_SESSION_INACTIVE
RUNTIME_SESSION_MISMATCH
CONTRACT_SNAPSHOT_MISMATCH
APPROVAL_TOKEN_MISMATCH
APPROVAL_EXPIRED
REQUEST_HASH_MISMATCH
OUTPUT_SCHEMA_MISMATCH
TARGET_STATE_CONFLICT
TASK_RESULT_STALE
RESULT_HASH_MISMATCH
PATH_OUTSIDE_APPROVED_ROOT
EVIDENCE_HASH_MISMATCH
TRANSPORT_SECURITY_MISMATCH
```

- [ ] **Step 5: Add a fail-closed CLI**

Arguments:

```text
--manifest PATH
--manifest-schema PATH
--operation PATH (optional)
--operation-schema PATH (required with --operation)
--project-root PATH (optional)
```

Output:

```json
{
  "valid": false,
  "issues": [
    {"code": "...", "path": "...", "message": "..."}
  ]
}
```

Exit `0` for no issues, `1` for validation issues, `2` for unreadable/invalid CLI inputs.

- [ ] **Step 6: Run semantic adversarial tests**

```bash
python -m unittest tests.test_godot_live_editor_contract_v2 -v
```

Expected: identity/snapshot/output/task/path/evidence tests pass; missing docs/template migration tests remain RED.

- [ ] **Step 7: Commit validator**

```bash
git add tools/validate_godot_live_editor_contract.py \
  tests/test_godot_live_editor_contract_v2.py
git commit -m 'feat: validate Godot live-editor v2 semantics'
```

---

## Task 4: Migrate active canonical documents and project templates

**Files:**

- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Modify: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Modify: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
- Modify: `tests/test_godot_live_editor_contract.py`
- Modify: `tests/test_godot_live_editor_idempotent_approval.py`

- [ ] **Step 1: Migrate canonical terminology and behavior**

Replace active `operation_class` guidance with:

```text
effect_kind
idempotency
approval_policy
execution_mode
rollback_policy
```

Add exact target/snapshot binding, closed output validation, stale-state preconditions, task core, evidence hashes, transport conditions, stable error codes, and Godot `--recovery-mode` handling.

Keep evidence boundaries explicit:

```yaml
production_network_mcp_transport: NOT_IMPLEMENTED
editor_main_thread_mutation_queue: NOT_IMPLEMENTED
editor_undo_redo_transaction: NOT_IMPLEMENTED
runtime_debugger_bridge: NOT_IMPLEMENTED
project_test_framework: NOT_CONFIGURED
physical_input_validation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: false
```

- [ ] **Step 2: Replace the active template with safe v2 NOT_CONFIGURED data**

The template must use `schema_version: 2`, `contract_version: 2.0.0`, `adapter_version: 2.0.0`, null identity/tool/endpoint/catalog fields, unconfigured access policies, no capabilities, and no runtime/adoption claim.

- [ ] **Step 3: Migrate the project-local adapter**

Required workflow:

```text
validate PROJECT_BASE_ADAPTER pin
→ load v2 manifest
→ validate v2 JSON Schema
→ run semantic validator
→ resolve exactly one typed capability
→ observe target and build preconditions
→ obtain approval when required
→ execute declared path
→ validate output
→ hash evidence/result
→ validate final envelope
→ report states and rollback
```

Stop on v1 selection outside the isolated legacy Pilot. Never auto-upgrade a user project's manifest in place.

- [ ] **Step 4: Keep the AGENTS fragment compact**

Include only discovery paths, validation commands, stop codes, approved roots, and report fields. Do not copy the canonical contract into the fragment.

- [ ] **Step 5: Migrate active static tests**

Update `tests/test_godot_live_editor_contract.py` to load v2 schemas/template. Update the idempotent approval test to prove this combination:

```text
MUTATION + IDEMPOTENT + REQUIRED + SYNCHRONOUS + SNAPSHOT
```

and bind approval to target identity, snapshot, policy, request hash, and preconditions.

- [ ] **Step 6: Run active-contract tests**

```bash
python -m unittest \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_idempotent_approval \
  tests.test_godot_live_editor_contract_v2 \
  -v
```

- [ ] **Step 7: Commit active migration**

```bash
git add docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md \
  docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md \
  docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md \
  templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json \
  templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md \
  templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md \
  tests/test_godot_live_editor_contract.py \
  tests/test_godot_live_editor_idempotent_approval.py
git commit -m 'feat: migrate active Godot automation contract to v2'
```

---

## Task 5: Isolate v1 as legacy Pilot compatibility only

**Files:**

- Create: `docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md`
- Modify: `docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md`
- Modify: `docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md`
- Modify: `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md`
- Modify: `tests/test_godot_live_editor_runtime_contract_hardening.py`
- Modify: `tests/test_godot_live_editor_runtime_pilot.py`
- Preserve unchanged: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Preserve unchanged: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Preserve unchanged: `examples/godot-live-editor-pilot/**`

- [ ] **Step 1: Write the compatibility boundary**

Declare:

```yaml
authority: LEGACY_PILOT_COMPAT_ONLY
new_project_adoption: PROHIBITED
template_selection: V2_ONLY
runtime_evidence_generation: HISTORICAL_V1
v2_runtime_migration: NOT_RUN
deletion_gate: V2_RUNTIME_PILOT_GREEN
```

List the exact allowed v1 files and tests. New active template/adapter/canonical documents are not on the allowlist.

- [ ] **Step 2: Label historical Pilot evidence honestly**

Add prominent facts without modifying captured hashes/counts:

```yaml
contract_generation: V1_LEGACY_PILOT
historical_godot_execution: PASS
v2_contract_static: SEPARATE
v2_godot_execution: NOT_RUN
production_adapter_ready: false
```

- [ ] **Step 3: Add a v1 authority allowlist test**

Scan active docs/templates/tools/tests and reject active references to the v1 schema paths or `schema_version: 1` outside the explicit Pilot compatibility allowlist. Exclude `.git`, `.godot`, binaries, and historical migration prose.

- [ ] **Step 4: Make Pilot tests explicitly legacy**

Rename local constants to `LEGACY_MANIFEST_SCHEMA` and `LEGACY_OPERATION_SCHEMA`; preserve test file/class names for CI continuity. Assert the active project template is v2.

- [ ] **Step 5: Run legacy isolation tests**

```bash
python -m unittest \
  tests.test_godot_live_editor_runtime_contract_hardening \
  tests.test_godot_live_editor_runtime_pilot \
  tests.test_godot_live_editor_contract_v2 \
  -v
```

Runtime cases requiring an unavailable Godot binary remain explicit skips, not PASS.

- [ ] **Step 6: Commit legacy isolation**

```bash
git add docs/knowledge/godot/GODOT_LIVE_EDITOR_V1_COMPATIBILITY.md \
  docs/superpowers/specs/2026-08-05-godot-4-7-1-runtime-pilot-design.md \
  docs/superpowers/plans/2026-08-05-godot-4-7-1-runtime-pilot.md \
  docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md \
  tests/test_godot_live_editor_runtime_contract_hardening.py \
  tests/test_godot_live_editor_runtime_pilot.py \
  tests/test_godot_live_editor_contract_v2.py
git commit -m 'docs: isolate Godot v1 runtime Pilot compatibility'
```

---

## Task 6: Run full regression and adversarial review

**Files:** Modify only confirmed findings; update Draft implementation PR evidence after verification.

- [ ] **Step 1: Run focused and aggregate suites**

```bash
python -m unittest \
  tests.test_godot_live_editor_contract \
  tests.test_godot_live_editor_contract_v2 \
  tests.test_godot_live_editor_idempotent_approval \
  tests.test_godot_live_editor_runtime_contract_hardening \
  tests.test_godot_live_editor_runtime_pilot \
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

- [ ] **Step 2: Verify protected bytes and changed-file scope**

```bash
git diff --check main...HEAD
git diff --name-status main...HEAD
git diff --exit-code main...HEAD -- skills/SKILL_REGISTRY.json
git diff --exit-code main...HEAD -- 'release/**' 'docs/releases/**'
sha256sum skills/SKILL_REGISTRY.json
```

Confirm no executable/archive, `.godot/`, generated runtime artifact, user project, Google Sheet payload, or new workflow is tracked.

- [ ] **Step 3: Attack the implementation**

Require fail-closed results for:

```text
approval reuse after catalog/schema/adapter/protocol change
approval reuse on another server/Editor/runtime instance
inactive runtime session
idempotent mutation without ledger
non-idempotent or irreversible automatic retry
LOCAL_HTTP without Origin/auth/session controls
session ID treated as authentication
open input/output schema
output mismatch promoted to success
stale revision/hash or unexpected dirty Scene
path traversal and symlink escape
PASS evidence without content hash
terminal task result from another instance/snapshot
active v1 selection
runtime/human readiness inferred from static files
```

Classify findings as `MUST_FIX`, `SHOULD_FIX`, `NICE_TO_HAVE`, or `REJECTED_CRITIQUE`; fix all reproducible MUST_FIX and Important issues.

- [ ] **Step 4: Request independent code review**

Provide exact base/head SHAs, approved spec, BCP/approval reference, changed files, test results, protected boundaries, and known NOT_RUN evidence. Do not claim independent review when none is available.

- [ ] **Step 5: Verify current-main merge ref and GitHub Actions**

Re-fetch main immediately before final verification. When main moved, test a fresh merge ref. Require:

```yaml
Validate Base v9 Operating Contracts: SUCCESS
Validate Game Project Operating System: SUCCESS
canonical reference freshness: SUCCESS
contract and governance regressions: SUCCESS
required ci-gate: SUCCESS
unresolved review threads: 0
```

Runtime jobs skipped for missing local Godot are `SKIPPED_NOT_CONFIGURED`.

- [ ] **Step 6: Update Draft PR evidence without merging**

```yaml
static_v2_schema: PASS
semantic_validator: PASS
active_template_and_adapter: V2
v1_authority: LEGACY_PILOT_COMPAT_ONLY
historical_v1_godot_runtime: PRESERVED
v2_godot_runtime: NOT_RUN
production_adapter_ready: false
registry_and_release_locks: UNCHANGED
merge: NOT_AUTHORIZED
```

---

## Stage A completion gate

```yaml
bcp_merged_and_approved: true
implementation_authorized: true
current_main_reconciled: true
test_only_red_recorded: true
v2_schema_green: true
semantic_validator_green: true
active_contract_template_adapter_v2: true
v1_new_adoption_prohibited: true
legacy_pilot_static_regression_green: true
v2_runtime_claim: NOT_RUN
repository_regressions_green: true
current_merge_ref_ci: PASS
unresolved_must_fix: 0
unresolved_review_threads: 0
registry_release_locks_unchanged: true
```

The implementation PR remains Draft until a separate user merge authorization. Stage B follows `docs/superpowers/plans/2026-08-05-godot-live-editor-v2-runtime-pilot-migration.md`.
