# PC-First QA Evidence Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a no-extra-cost localhost QA evidence tool, connected through a minimal reviewed Tool Hub registry, that records developer-only PC image and UX review without pretending Android or external-tester validation happened.

**Architecture:** `tools/qa-evidence-studio` owns immutable project-bound QA sessions and local evidence packets under the existing ignored Asset Vault. `tools/tool-hub` owns only reviewed tool discovery, machine-local project locators, and a typed launcher for the QA tool; it never accepts raw commands. Both are independent FastAPI packages with static browser UIs, exact loopback mutation protection, and no provider calls.

**Tech Stack:** Python 3.10+, FastAPI, Pydantic v2, Uvicorn, pytest, JSON Schema, existing `base-tool-contracts` staging primitives.

## Global Constraints

- Android is `DEFERRED_NOT_CONNECTED` until PC implementation is complete and release preparation begins; it is not a Phase 1 launch or pass target.
- Human validation starts only after image and UX placement is explicitly marked complete.
- The only current human reviewer is `DEVELOPER_OWNER`; no external tester count is required or invented.
- All evidence remains under `<project>/.asset-vault/library/generated/qa-evidence-studio/` and is never committed automatically.
- The tool makes no OpenAI/provider call and adds no paid service dependency.
- Hub requests select only reviewed `tool_id + project_id`; no request supplies shell, argv, environment, interpreter, or output root.
- Existing Expression Studio, Sprite Animation Studio, Figma routing, HiGodot, GUT, Hera, project canon, and protected paths remain unchanged.

---

### Task 1: Reviewed Tool Registry Contract

**Files:**
- Create: `schemas/base-tool-registry-v1.schema.json`
- Create: `tools/TOOL_REGISTRY.json`
- Create: `tools/validate_tool_registry.py`
- Test: `tests/test_tool_registry_contract.py`

**Interfaces:**
- Produces: `load_registry(base_root: Path, registry_path: Path) -> tuple[dict[str, object], ...]`
- Enforces: no raw command, absolute owner path, duplicate tool ID, unknown adapter, or missing owner directory.

- [ ] Write failing behavior tests for a valid registry and each forbidden mutation.
- [ ] Run `pytest tests/test_tool_registry_contract.py -q` and confirm the missing validator failure.
- [ ] Add the schema, three reviewed human-interactive entries, and minimal validator.
- [ ] Run the focused tests and confirm PASS.

### Task 2: Project Locator and Hub Catalog

**Files:**
- Create: `tools/tool-hub/pyproject.toml`
- Create: `tools/tool-hub/src/tool_hub/registry.py`
- Create: `tools/tool-hub/src/tool_hub/projects.py`
- Create: `tools/tool-hub/src/tool_hub/security.py`
- Create: `tools/tool-hub/src/tool_hub/app.py`
- Test: `tools/tool-hub/tests/test_projects.py`
- Test: `tools/tool-hub/tests/test_api.py`

**Interfaces:**
- Produces: `ProjectLocator.register(root: Path) -> ProjectBinding`
- Produces: `create_app(base_root, project_config, test_mode=False) -> FastAPI`
- Enforces: exact v2 adapter `project.project_id`, Git root, locator fingerprint, path redaction, loopback Origin/session/CSRF.

- [ ] Write failing tests for valid registration, v1/mismatched identity rejection, redacted catalog output, and hostile mutation requests.
- [ ] Run focused tests and confirm failure because the package is absent.
- [ ] Implement the minimal locator, registry reader, security boundary, and catalog API.
- [ ] Run focused tests and confirm PASS.

### Task 3: QA Session Domain and Evidence Packet

**Files:**
- Create: `tools/qa-evidence-studio/pyproject.toml`
- Create: `tools/qa-evidence-studio/src/qa_evidence_studio/models.py`
- Create: `tools/qa-evidence-studio/src/qa_evidence_studio/paths.py`
- Create: `tools/qa-evidence-studio/src/qa_evidence_studio/service.py`
- Test: `tools/qa-evidence-studio/tests/test_service.py`

**Interfaces:**
- Produces: `QaEvidenceService.create_session(request) -> dict`
- Produces: `mark_visual_ux_ready(session_id, acknowledgement) -> dict`
- Produces: `record_result(session_id, item_id, status, note) -> dict`
- Produces: `add_image_evidence(session_id, filename, content_type, data) -> dict`
- Produces: `finalize(session_id) -> dict`

- [ ] Write failing tests proving initial `PREPARING_VISUAL_UX`, permanent Phase 1 Android deferral, developer-only reviewer, and blocked premature results.
- [ ] Write failing tests proving readiness acknowledgement, result transitions, image hashing, deterministic packet contents, and finalize outcomes.
- [ ] Run focused tests and confirm the domain package is absent.
- [ ] Implement the smallest state machine and Asset Vault writes needed to pass.
- [ ] Run focused tests and confirm PASS.

### Task 4: QA Localhost API and Usable Browser UI

**Files:**
- Create: `tools/qa-evidence-studio/src/qa_evidence_studio/security.py`
- Create: `tools/qa-evidence-studio/src/qa_evidence_studio/app.py`
- Create: `tools/qa-evidence-studio/web/index.html`
- Create: `tools/qa-evidence-studio/web/app.js`
- Create: `tools/qa-evidence-studio/web/styles.css`
- Test: `tools/qa-evidence-studio/tests/test_api.py`
- Test: `tools/qa-evidence-studio/tests/test_web_contract.py`

**Interfaces:**
- Produces: `/api/config`, `/api/status`, `/api/sessions`, readiness, result, evidence, finalize endpoints.
- Produces: CLI with `--project-root`, `--project-id`, `--port`, `--launch-nonce`, and atomic `--startup-file` report.

- [ ] Write failing API tests for project binding, lifecycle, upload bounds, child identity, and hostile request rejection.
- [ ] Write failing UI behavior contract tests for visible precondition, Android deferral, reviewer role, and no false-complete copy.
- [ ] Run focused tests and confirm failure.
- [ ] Implement API, port-zero startup, and the minimal Korean browser workflow.
- [ ] Run focused tests and confirm PASS.

### Task 5: Typed Hub Launcher Vertical Slice

**Files:**
- Create: `tools/tool-hub/src/tool_hub/launcher.py`
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Create: `tools/tool-hub/web/index.html`
- Create: `tools/tool-hub/web/app.js`
- Create: `tools/tool-hub/web/styles.css`
- Test: `tools/tool-hub/tests/test_launcher.py`
- Test: `tools/tool-hub/tests/test_web_contract.py`

**Interfaces:**
- Produces: `QaEvidenceLauncher.start(ProjectBinding) -> ChildIdentity`
- Produces: idempotent `(qa-evidence-studio, project_id)` child binding and authenticated status comparison.
- Enforces: `shell=False`, clean environment allowlist, bound port 0, exact nonce/tool/project identity, no raw command endpoint.

- [ ] Write failing tests for real child startup, two distinct projects, idempotent repeat start, malformed startup report, and registry adapter rejection.
- [ ] Run focused tests and confirm failure.
- [ ] Implement the typed launcher and browser launch control.
- [ ] Run focused tests and confirm PASS.

### Task 6: Documentation, Sample Evidence, and Regression

**Files:**
- Create: `tools/qa-evidence-studio/README.md`
- Create: `tools/tool-hub/README.md`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Create: `docs/reviews/2026-08-13-pc-first-qa-evidence-studio-adversarial-review.md`

**Interfaces:**
- Documents exact Windows PowerShell setup, current validation status, Android deferral, external tester absence, rollback, and safe local outputs.

- [ ] Run a temporary real Git project through Hub registration and a real QA child process.
- [ ] Import a repository-owned sample image, record PC checklist results, and export the evidence packet; label this tool-flow validation, not product visual-quality approval.
- [ ] Run QA, Hub, registry, existing Studio, root regression, and trusted local validation commands.
- [ ] Perform `attack -> validate-critique -> minimal-fix -> regression-recheck`; record P0/P1 and unverified Windows/real-project items honestly.
- [ ] Commit only intended files, publish a PR from the exact reviewed head, verify checks and unresolved threads, then merge only that exact head.

## Self-Review

- Spec coverage: PC-first review, visual/UX gate, developer-only reviewer, Android deferral, local evidence, Hub integration, security, sample flow, rollback, and no-cost requirement each map to a task.
- Placeholder scan: no implementation placeholder is used as a completion criterion; deferred Android is an explicit product boundary with a later gate.
- Type consistency: registry adapter ID is `qa_evidence_studio`; project identity is always the v2 adapter `project.project_id`; session writes are owned by `QaEvidenceService`.
