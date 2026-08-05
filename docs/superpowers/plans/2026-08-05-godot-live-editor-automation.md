# Godot Live Editor Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development for implementation and superpowers:verification-before-completion before any completion claim. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a compact, machine-validatable Godot live-editor automation contract and project adapter that reuse existing Base Skill owners without changing released Registry bytes or v9.4.3 release locks.

**Architecture:** Publish two canonical Godot knowledge documents, two strict JSON Schemas, and a project-local adapter template. Connect them through compact Base/project entrypoints. Use the already-required operating-system regression module for the first RED/GREEN cycle so exact-head GitHub Actions execute the tests without expanding CI topology.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.12 `unittest`, existing Base GitHub Actions and canonical-reference checks.

## Global constraints

- Keep `skills/SKILL_REGISTRY.json` byte-identical with SHA-256 `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- Keep `base-v9.4.3.lock.json`, predecessor release locks, and frozen release derivatives unchanged.
- Do not add a new broad active Base Skill.
- Do not copy Hera source, Unity APIs, C# handlers, UPM paths, or command syntax.
- Do not claim a production Godot EditorPlugin, MCP server, project test runner, physical input, runtime success, or human validation.
- Do not alter open PR #134, #136, or #137 branches or files.
- Keep entrypoints short; canonical details live in the Godot contract and schema files.
- Every timeout/retry/approval/task contract fails closed when identity or evidence is incomplete.

---

### Task 1: Commit approved design and implementation plan

**Files:**
- Create: `docs/superpowers/specs/2026-08-05-godot-live-editor-automation-design.md`
- Create: `docs/superpowers/plans/2026-08-05-godot-live-editor-automation.md`

- [ ] **Step 1: Save the approved design**

Record the three execution paths, existing owner matrix, identity/approval/retry/task/evidence boundaries, testing strategy, rollout, and rollback.

- [ ] **Step 2: Self-review the spec**

Search for `TBD`, `TODO`, placeholders, contradictory ownership, unbounded arbitrary execution, port-only identity, unqualified retry, and unsupported Godot test claims. Fix every confirmed issue before committing.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-08-05-godot-live-editor-automation-design.md \
  docs/superpowers/plans/2026-08-05-godot-live-editor-automation.md
git commit -m "docs: design Godot live editor automation contract"
```

### Task 2: Add failing operating-contract tests

**Files:**
- Modify: `tests/test_game_project_operating_system_structure.py`
- Create later: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Create later: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- Create later: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Create later: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Create later: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Create later: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Create later: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`

**Interfaces:**
- `GameProjectOperatingSystemStructureTests` remains an existing required CI module.
- Tests load both schemas with `Draft202012Validator` and validate the project manifest plus representative request/result envelopes.

- [ ] **Step 1: Add required-path expectations**

Require the two knowledge documents, two schemas, manifest template, project-local adapter Skill, and AGENTS fragment.

- [ ] **Step 2: Add failing contract tests**

Assert the future artifacts contain and enforce:

- `doctor → status → catalog --compact`;
- normalized project path, `project.godot` SHA-256, and project fingerprint identity;
- typed capabilities and the five operation classes;
- approval binding and single-use semantics;
- no blind retry after unknown mutation outcomes;
- `operation_id` and durable `task_id` resume behavior;
- separate engine-input, physical-input, runtime, and human evidence states;
- explicit `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED` behavior;
- routing to existing active owners and no new Base Registry Skill.

- [ ] **Step 3: Commit RED tests only**

```bash
git add tests/test_game_project_operating_system_structure.py
git commit -m "test: define Godot live editor safety contract"
```

- [ ] **Step 4: Open a Draft PR and observe exact-head RED**

Use GitHub Actions as the execution environment because local checkout is blocked by DNS. Expected failure: missing Godot contract/template/schema paths and assertions. Record the exact failing head and failing test names; do not describe unrelated failures as TDD evidence.

### Task 3: Add strict capability and operation schemas

**Files:**
- Create: `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- Create: `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- Create: `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Test: `tests/test_game_project_operating_system_structure.py`

**Interfaces:**
- Capability schema uses Draft 2020-12 and validates a project-owned `NOT_CONFIGURED` or configured manifest.
- Operation schema validates request/result identity, capability, risk class, request hash, approval, task state, result code, and evidence states.

- [ ] **Step 1: Implement capability schema**

Require:

- `schema_version`, `artifact_role`, `configuration_state`, `contract_version`, `adapter_version`;
- normalized project path placeholder, project file hash/fingerprint state, engine compatibility;
- transport binding and loopback/default-off facts;
- catalog freshness metadata;
- unique typed capabilities with execution path, operation class, retry policy, timeout policy, and evidence outputs.

Reject configured manifests with empty identity, unregistered operation classes, automatic retry for non-retryable mutations, or approval-required operations without approval declaration.

- [ ] **Step 2: Implement operation schema**

Require:

- UUID-like or opaque non-empty operation identity;
- project fingerprint and request hash;
- stable operation class;
- approval state and token binding fields when approved;
- task identity/state for long-running work;
- stable result code and explicitly typed evidence states.

- [ ] **Step 3: Add the safe template manifest**

Ship `configuration_state: NOT_CONFIGURED`, no capabilities, no transport endpoint, no claimed test framework, and explicit installation instructions. A valid template must not imply runtime readiness.

- [ ] **Step 4: Check schema behavior**

The regression test must validate the template and representative valid envelopes, then assert rejection of port-only identity, unsafe retry, incomplete approval binding, and unbound task completion.

### Task 4: Add canonical Godot contract and security guide

**Files:**
- Create: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Create: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- Test: `tests/test_game_project_operating_system_structure.py`

- [ ] **Step 1: Write the automation contract**

Cover scope, architecture, bootstrap, identity, compact catalog, capability classes, command batching, bounded output, operation envelope, task lifecycle, validation loop, evidence states, installation, and failure reporting.

- [ ] **Step 2: Write the security and recovery guide**

Cover loopback/default-off transport, typed-action allowlists, path confinement, approval binding, request hashing, idempotency, operation ledger, unknown timeout reconciliation, process/endpoint/project distinctions, task result freshness, rollback limitations, and secret redaction.

- [ ] **Step 3: Remove Unity-only assumptions**

The canonical Godot documents must not instruct projects to use UnityEngine objects, UPM, C# Editor handlers, Unity domain reloads, EventSystem, or Hera commands. Comparative attribution may name Hera only as a benchmark.

### Task 5: Add the compact project adapter and routing

**Files:**
- Create: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Create: `templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md`
- Modify: `START_HERE.md`
- Modify: `templates/project-operations/.agents/skills/base-project-router/SKILL.md`
- Modify: `tests/test_game_project_operating_system_structure.py`

**Interfaces:**
- Adapter modes: `bootstrap`, `observe`, `mutate`, `validate`, `resume`, `recover`.
- Adapter reads the project manifest and routes policy ownership to existing Base Skills.

- [ ] **Step 1: Write the project-local Skill**

Keep the body compact. It must:

- fail closed when the manifest is absent, `NOT_CONFIGURED`, invalid, stale, or identity-mismatched;
- select one registered capability only;
- map operation classes to approval/retry behavior;
- emit one operation envelope and bounded evidence;
- route runtime diagnosis, change validation, UI evidence, long tasks, freshness, and installation to existing owners;
- prohibit automatic approval and unsafe mutation retry.

- [ ] **Step 2: Write the AGENTS fragment**

Provide only the discovery sequence, canonical manifest/Skill/contract paths, stop conditions, and report shape. Do not duplicate the full contract.

- [ ] **Step 3: Add compact Base and project routes**

Add one auxiliary route in `START_HERE.md` and one project-router paragraph that reads the adapter only after Base adapter validation succeeds. Keep the Base router free of reusable engine workflow details.

- [ ] **Step 4: Assert non-registration**

Tests must prove `godot-live-editor-operations` is absent from `skills/SKILL_REGISTRY.json` and exists only as a project template adapter.

### Task 6: Run GREEN validation and fix confirmed failures

**Files:**
- Verify all changed files.

- [ ] **Step 1: Run focused tests where execution is available**

```bash
python -m unittest tests.test_game_project_operating_system_structure -v
python -m unittest \
  tests.test_reference_freshness \
  tests.test_skill_routing_governance \
  tests.test_skill_package_integrity \
  tests.test_skill_system_coverage \
  -v
```

Local execution remains `BLOCKED_ENVIRONMENT` if a checkout cannot be obtained. Do not convert static connector inspection into a local PASS.

- [ ] **Step 2: Inspect exact-head GitHub Actions**

Require success for the Base operating contract, game-project operating-system validation, required CI gate, documentation/whitespace validation, and any other triggered workflow. Record skipped jobs as `SKIPPED_NOT_REQUIRED`, not PASS.

- [ ] **Step 3: Verify protected identity and scope**

```bash
sha256sum skills/SKILL_REGISTRY.json

git diff --name-only main...HEAD

git diff --check main...HEAD
```

Confirm no release lock, frozen derivative, unrelated prompt/tutorial file, or project repository changed.

### Task 7: Adversarial review and regression recheck

**Files:**
- Modify only confirmed findings.

- [ ] **Step 1: Attack the design**

Test these failure hypotheses:

- port or process ID can override project identity;
- stale catalog or adapter version can still execute;
- arbitrary script execution is available by default;
- approval can be reused with changed arguments;
- a timeout can start a duplicate mutation/test/export;
- a completed task result can be attached to a different project or operation;
- engine input is reported as physical input;
- Godot engine self-tests are reported as project tests;
- file existence is reported as runtime or human success;
- project adapter becomes a duplicate Base active Skill;
- long documentation is copied into entrypoints.

- [ ] **Step 2: Validate criticism**

Classify findings as `MUST_FIX`, `SHOULD_FIX`, `NICE_TO_HAVE`, or `REJECTED_CRITIQUE`. Fix only reproducible contract weaknesses; reject requests that add an unproven universal bridge or unrelated refactor.

- [ ] **Step 3: Regression recheck**

Re-fetch the exact head, rerun required checks, compare changed-file scope, and verify unresolved review threads are zero before any readiness claim.

### Task 8: Final Draft PR evidence

**Files:**
- Update Draft PR body only; do not merge.

- [ ] **Step 1: Report exact scope**

List every changed file and distinguish design, contract, schema, template, routing, and test changes.

- [ ] **Step 2: Report truthful evidence**

Separate:

```yaml
contract_and_schema_validation:
exact_head_github_actions:
local_checkout_and_tests:
godot_cli_runtime:
godot_editor_plugin_runtime:
project_test_framework:
physical_input:
human_usability:
```

- [ ] **Step 3: Keep Draft boundaries**

Leave the PR Draft because a real Godot project pilot, EditorPlugin runtime, physical-input validation, and human validation are outside this Base contract PR. Merge requires a separate user request and exact-head review.
