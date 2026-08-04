# Godot Live Editor Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development for implementation and superpowers:verification-before-completion before any completion claim. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a compact, machine-validatable Godot live-editor automation contract and project adapter that reuse existing Base Skill owners while closing approval, task, capability-catalog, evidence, and external-tool adoption gaps.

**Architecture:** Publish two canonical Godot knowledge documents, two strict JSON Schemas, one cross-field semantic validator, and a project-local adapter template. Structural constraints remain in JSON Schema; identity equality and catalog references are validated by the Python semantic validator. Required GitHub Actions execute the focused tests through existing CI discovery modules.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.12 `unittest`, existing Base GitHub Actions and canonical-reference checks.

## Global Constraints

- Keep `skills/SKILL_REGISTRY.json` byte-identical with SHA-256 `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- Keep `base-v9.4.3.lock.json`, predecessor release locks, and frozen release derivatives unchanged.
- Do not add a new broad active Base Skill.
- Do not copy Hera source, Unity APIs, C# handlers, UPM paths, or command syntax.
- Do not claim a production Godot EditorPlugin, MCP server, project test runner, physical input, runtime success, or human validation.
- Do not alter game project repositories, Google Sheets, or unrelated open PR branches.
- Keep entrypoints short; canonical details live in the Godot contract, schemas, and semantic validator.
- Every timeout, retry, approval, task, evidence, and tool-adoption contract fails closed when identity or evidence is incomplete.
- Represent side-effect risk with `effect_class` and execution lifetime with `execution_mode`; never combine both concerns into one enum.

---

### Task 1: Preserve the approved architecture and conflict boundary

**Files:**
- Modify: `docs/superpowers/specs/2026-08-05-godot-live-editor-automation-design.md`
- Modify: `docs/superpowers/plans/2026-08-05-godot-live-editor-automation.md`

**Interfaces:**
- Parent implementation PR: `#152`, branch `agent/godot-live-editor-automation`.
- Stacked hardening PR: `#153`, branch `agent/godot-live-editor-contract-hardening`.

- [x] **Step 1: Create the hardening branch from exact parent HEAD**

Create `agent/godot-live-editor-contract-hardening` from parent exact HEAD `94573d45682814a4721f55bf08be021f8da25409` so concurrent work on #152 is not overwritten.

- [x] **Step 2: Open a Draft stacked PR**

Target `agent/godot-live-editor-automation` rather than `main`. Keep the PR Draft and state that no PASS is claimed before a fresh GREEN exact head.

- [x] **Step 3: Update the design and plan**

Record the four adversarial findings, orthogonal capability model, semantic validator, evidence-domain constraints, and exact engine/tool-adoption boundaries.

### Task 2: Establish the hardening RED

**Files:**
- Modify: `tests/test_godot_live_editor_contract.py`

**Interfaces:**
- Test module is already imported by existing required CI discovery in `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`.
- Fixtures expose the desired public schema before implementation.

- [x] **Step 1: Replace stale fixtures with the desired contract**

Require:

```yaml
effect_class: READ_ONLY | IDEMPOTENT_MUTATION | APPROVAL_REQUIRED_MUTATION | NON_RETRYABLE_MUTATION
execution_mode: SYNCHRONOUS | LONG_RUNNING_TASK
```

Add exact engine compatibility, external-tool adoption, valid project-test runner, and result-hash fields.

- [x] **Step 2: Add failing adversarial tests**

Cover:

- long-running approval-required and non-retryable operations;
- mismatched approval token bindings;
- mismatched task and result-hash bindings;
- duplicate capability IDs;
- missing or invalid configured project-test runner;
- misleading evidence kind/state pairs;
- missing configured engine/tool-adoption facts.

- [x] **Step 3: Observe exact-head RED**

Exact test-only head: `c02f81eaa4ad9e99c68dbc271b0a5f37054fbb71`.

Required `ubuntu-contract` ran 215 tests and failed with nine intended contract failures: missing `effect_class`/`execution_mode`, missing semantic validator, stale docs/adapter, and schemas that still accepted the old contract. Reference freshness passed before the focused regressions failed.

### Task 3: Split capability risk from execution lifetime

**Files:**
- Modify: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Modify: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Modify: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Test: `tests/test_godot_live_editor_contract.py`

**Interfaces:**
- Capability schema produces `effect_class` and `execution_mode`.
- Operation envelope consumes the same exact names.

- [x] **Step 1: Replace `operation_class` in the capability schema**

Require orthogonal `effect_class` and `execution_mode` fields. Preserve:

- approval requirement for approval/non-retryable mutations;
- idempotency key and ledger requirement for idempotent mutations;
- no automatic retry for approval/non-retryable mutations;
- durable ledger, `RESUME_BY_TASK_ID`, and no automatic retry for long tasks.

- [x] **Step 2: Replace `operation_class` in the operation envelope**

Require the same two fields. Make task shape depend only on `execution_mode`; make approval state depend only on `effect_class`.

- [x] **Step 3: Add terminal result hash**

Require terminal task results to expose `result.result_hash` and a result binding containing the same identity fields.

- [x] **Step 4: Keep the template inert**

Set `configuration_state: NOT_CONFIGURED`, null engine/tool values, disabled transport, empty catalog, no project-test runner, and no capability.

### Task 4: Add cross-field semantic validation

**Files:**
- Create: `tools/validate_godot_live_editor_contract.py`
- Test: `tests/test_godot_live_editor_contract.py`

**Interfaces:**

```python
def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]: ...
def validate_operation_semantics(envelope: Mapping[str, Any]) -> list[str]: ...
```

- [x] **Step 1: Validate capability catalog identities**

Return `DUPLICATE_CAPABILITY_ID` when one ID appears more than once.

- [x] **Step 2: Validate configured project-test runner references**

Require exactly one matching capability, a supported execution path, and `TEST_RESULT` evidence. Return stable codes rather than prose-only failures.

- [x] **Step 3: Validate approval equality**

For `APPROVED`, require token project, capability, request hash, and `effect_class` to equal top-level values. Return `APPROVAL_TOKEN_MISMATCH` on any difference.

- [x] **Step 4: Validate terminal task equality**

Require result-binding project, capability, operation, and task identity to equal the envelope. Require binding hash to equal `result.result_hash`.

- [x] **Step 5: Add a CLI**

Support `--manifest` and `--operation`, emit machine-readable JSON, and return non-zero on semantic failure.

### Task 5: Constrain evidence truthfulness

**Files:**
- Modify: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Test: `tests/test_godot_live_editor_contract.py`

- [x] **Step 1: Add kind-specific state families**

Map:

```text
CONTRACT → CONTRACT_*
ENGINE_STATE / SCREENSHOT / LOG / TEST_RESULT / EXPORT → EXECUTION_*
RUNTIME → RUNTIME_*
ENGINE_INPUT → ENGINE_INPUT_*
PHYSICAL_INPUT → PHYSICAL_INPUT_*
HUMAN → HUMAN_*
```

- [x] **Step 2: Reject misleading combinations**

Reject `HUMAN + CONTRACT_PASS` and `SCREENSHOT + PHYSICAL_INPUT_PASS`.

- [x] **Step 3: Require artifact paths for PASS**

Passing evidence must name an artifact path. `NOT_RUN`, `NOT_CONFIGURED`, `BLOCKED_ENVIRONMENT`, and `HUMAN_NOT_RUN` must not fabricate one.

### Task 6: Add exact engine and tool-adoption boundaries

**Files:**
- Modify: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Modify: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Test: `tests/test_godot_live_editor_contract.py`

- [x] **Step 1: Require exact configured engine facts**

Configured manifests require `detected_version`, `minimum_version`, and `maximum_exclusive_version`.

- [x] **Step 2: Require tool source and version pin**

Configured manifests require `source_type`, source reference, and exact version pin.

- [x] **Step 3: Require data and removal policy**

Configured manifests require telemetry policy, external-data policy, uninstall reference, and rollback reference.

- [x] **Step 4: Preserve NOT_CONFIGURED safety**

The Base template keeps every adoption field null or `NOT_CONFIGURED` and claims no runtime readiness.

### Task 7: Synchronize canonical documentation and project adapter

**Files:**
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Modify: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
- Test: `tests/test_godot_live_editor_contract.py`

- [x] **Step 1: Update the canonical automation contract**

Document the orthogonal fields, semantic validator, project-test runner integrity, result hash, evidence mapping, and tool-adoption boundary.

- [x] **Step 2: Update security and recovery**

Document long-running mutations retaining approval/retry risk, semantic binding checks, catalog uniqueness, telemetry/external transfer policy, and uninstall/rollback requirements.

- [x] **Step 3: Update the project adapter**

Fail closed when Schema or semantic validation fails. Report `effect_class` and `execution_mode`, not the obsolete combined class.

- [x] **Step 4: Keep the AGENTS fragment compact**

Add only discovery order, stop conditions, semantic validator, new fields, and report shape. Do not duplicate the long contract.

### Task 8: Run fresh GREEN validation

**Files:**
- Verify all changed files.

- [ ] **Step 1: Inspect the current stacked PR exact head**

Confirm #153 still targets `agent/godot-live-editor-automation` and identify any concurrent parent commits. If the parent advanced only in disjoint files, preserve the stacked structure; otherwise reconcile before claiming GREEN.

- [ ] **Step 2: Run exact-head GitHub Actions**

Require the current #153 head to execute:

- `Validate Base v9 Operating Contracts`;
- `Validate Game Project Operating System`;
- required `ci-gate` and its required jobs.

Expected: zero test failures. Record Windows smoke as `SKIPPED_NOT_REQUIRED` when the workflow classifies it as unnecessary.

- [ ] **Step 3: Inspect focused job logs**

Verify `tests.test_godot_live_editor_contract` actually ran and all new adversarial tests passed. A green workflow that skipped the focused module is not accepted.

- [ ] **Step 4: Verify schema and semantic fixtures**

Confirm the valid configured manifest and operation pass, while all mismatched fixtures fail with the intended stable code.

### Task 9: Adversarial regression and protected-scope review

**Files:**
- Modify only confirmed findings.

- [ ] **Step 1: Attack the hardened design**

Test these hypotheses:

- long-running mutation bypasses approval;
- long-running non-retryable task can automatically retry;
- approval token binds to a different project, capability, request, or effect;
- terminal task result binds to a different project, capability, operation, task, or result hash;
- duplicate capability IDs survive;
- configured test runner is absent or lacks test evidence;
- screenshot or human evidence claims another evidence domain;
- configured engine/tool adoption values are blank;
- project adapter becomes a duplicate Base active Skill;
- Registry or release locks changed.

- [ ] **Step 2: Compare changed-file scope**

Compare #153 to its current base branch. Expected hardening files:

```text
docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md
docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md
docs/superpowers/plans/2026-08-05-godot-live-editor-automation.md
docs/superpowers/specs/2026-08-05-godot-live-editor-automation-design.md
schemas/godot-live-editor-capability-manifest-v1.schema.json
schemas/godot-live-editor-operation-envelope-v1.schema.json
templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md
templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json
templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md
tests/test_godot_live_editor_contract.py
tools/validate_godot_live_editor_contract.py
```

No Registry, release lock, frozen derivative, unrelated prompt/tutorial file, or project repository may appear.

- [ ] **Step 3: Recheck exact head and review threads**

Re-fetch the exact head after any fix, rerun required checks, and verify unresolved review threads are zero before readiness wording.

### Task 10: Final Draft PR evidence and parent handoff

**Files:**
- Update Draft PR #153 body.
- Add one parent PR #152 comment.

- [ ] **Step 1: Record RED and GREEN heads**

State the test-only RED head and final reviewed GREEN head separately.

- [ ] **Step 2: Report truthful evidence**

Separate:

```yaml
contract_and_schema_validation:
semantic_validation:
exact_head_github_actions:
local_checkout_and_tests:
godot_cli_runtime:
godot_editor_plugin_runtime:
project_test_framework_integration:
physical_input:
human_usability:
```

- [ ] **Step 3: Keep Draft boundaries**

Leave #153 and #152 Draft. Do not merge. Real Godot project pilot, EditorPlugin runtime, physical-input validation, and human validation remain outside this Base contract hardening.

- [ ] **Step 4: Link the parent PR**

Comment on #152 with the stacked PR, exact head, resolved findings, protected scope, and remaining runtime evidence limits.