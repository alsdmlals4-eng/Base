# Tool Hub Project Picker and Windows Registration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a human-readable eight-project picker and make project registration work safely on Windows while leaving child tools fail-closed.

**Architecture:** Project names are a read-only projection of Base's canonical committed Figma routing registry. Registration sends both the expected project ID and the user's local Git root; the locator validates the v2 adapter and stores only a machine-local binding. `validate_project_identity` dispatches to the existing Linux descriptor validator or a Windows portable validator with reparse rejection, committed-blob checks, bounded reads, snapshot revalidation, and sanitized Git execution.

**Tech Stack:** Python 3.12, FastAPI/Pydantic, vanilla HTML/CSS/JavaScript, pytest, Git, Windows `lstat` reparse metadata, GitHub Actions `windows-latest`.

## Global Constraints

- The project picker is discovery only and cannot create project identity or authorize Figma mutation.
- Registration must require exact selected ID ↔ committed v2 adapter ID equality.
- Public responses must not expose absolute local paths, Git stderr, environment variables, tokens, or Figma credentials.
- Existing Linux descriptor-bound validation remains unchanged except for explicit platform dispatch.
- Windows child tools remain `BLOCKED_PLATFORM`; this plan does not implement Job Object launch or Studio staging.
- No paid API/provider call, Figma mutation, project source mutation, or Android work.

---

### Task 1: Canonical known-project projection

**Files:**
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/figma_routing.py`
- Modify: `tools/base-tool-contracts/tests/test_figma_routing.py`
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/tests/test_api.py`

**Interfaces:**
- Produces: `ProjectFigmaRegistry.public_projects() -> list[dict[str, str]]` containing only `project_id`, `display_name`, and `routing_state`.
- Produces: `/api/catalog.known_projects` from the canonical committed registry.

- [ ] **Step 1: Write failing projection tests.** Assert all eight canonical IDs/display names are returned, archived entries are not selectable, local paths and Figma URLs/keys are absent, and the API preserves separate `known_projects` and registered `projects` arrays.
- [ ] **Step 2: Run focused tests and verify RED.**

```bash
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests/test_figma_routing.py tools/tool-hub/tests/test_api.py
```

- [ ] **Step 3: Implement the minimal read-only projection.** Load the canonical registry during app creation, call `assert_canonical(base_root)`, and return only bounded public fields.
- [ ] **Step 4: Re-run focused tests and verify GREEN.**
- [ ] **Step 5: Commit the task.**

### Task 2: Expected-project registration contract

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/projects.py`
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/tests/test_projects.py`
- Modify: `tools/tool-hub/tests/test_api.py`

**Interfaces:**
- Changes: `ProjectLocator.register(project_root: Path, expected_project_id: str) -> ProjectBinding`.
- Changes: `POST /api/projects` body to `{ "project_id": str, "project_root": str }`.

- [ ] **Step 1: Write failing tests.** A matching expected ID registers; a different adapter ID returns `PROJECT_IDENTITY_MISMATCH`; an unknown catalog ID returns `PROJECT_CATALOG_ENTRY_REQUIRED`; errors remain path-redacted.
- [ ] **Step 2: Run the focused tests and verify RED.**

```bash
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_projects.py tools/tool-hub/tests/test_api.py
```

- [ ] **Step 3: Implement exact ID binding.** Reject registration before config write unless the requested ID exists in the known-project catalog and the identity validator returns that same ID.
- [ ] **Step 4: Update existing callers/fixtures to send the expected ID; re-run focused tests GREEN.**
- [ ] **Step 5: Commit the task.**

### Task 3: Human-readable picker UI

**Files:**
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Modify: `tools/tool-hub/web/styles.css`
- Modify: `tools/tool-hub/tests/test_web_contract.py`

**Interfaces:**
- Consumes: `catalog.known_projects`, `catalog.projects`, and `POST /api/projects` expected-ID contract.
- Produces: accessible `#known-project` select, `#project-root`, and separate `#registered-project-list` controls.

- [ ] **Step 1: Write failing web contract tests.** Require the labeled select, separate registered list, text-only rendering, exact selected ID submission, no local path in the DOM after refresh, and no inline/raw command surface.
- [ ] **Step 2: Run the focused web test and verify RED.**

```bash
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_web_contract.py
```

- [ ] **Step 3: Implement the picker and registered-project buttons.** Preserve CSRF/origin behavior, reset path input only after successful registration, retain project-scoped child states, and show `BLOCKED_PLATFORM` truthfully on Windows.
- [ ] **Step 4: Run web tests plus `node --check tools/tool-hub/web/app.js` GREEN.**
- [ ] **Step 5: Commit the task.**

### Task 4: Windows portable project identity validation

**Files:**
- Create: `tools/base-tool-contracts/src/base_tool_contracts/windows_project_identity.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/project_identity.py`
- Modify: `tools/base-tool-contracts/tests/test_project_identity.py`
- Modify: `tools/tool-hub/tests/test_projects.py`

**Interfaces:**
- Produces: `validate_windows_project_identity(project_root, expected_project_id, base_root) -> ProjectIdentityEvidence`.
- Changes: `validate_project_identity` dispatches to the portable validator only on `sys.platform == "win32"`; Linux retains the existing descriptor validator.

- [ ] **Step 1: Write failing tests with an explicit platform injection seam.** Cover valid path-with-spaces, exact Git root, ID mismatch, missing/uncommitted/dirty adapter, CRLF semantic JSON, reparse component rejection, changed adapter snapshot, Base pin failure, non-gitignored vault, and public error redaction.
- [ ] **Step 2: Run focused tests and verify RED.**

```bash
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests/test_project_identity.py tools/tool-hub/tests/test_projects.py
```

- [ ] **Step 3: Implement bounded portable validation.** Walk every path component with `lstat`, reject symlink/reparse metadata, use the trusted Git executable with fixed arguments/environment, compare adapter semantic JSON to `HEAD`, run the canonical `--hub-identity-check`, then recheck root and adapter identity/bytes before producing the fingerprint.
- [ ] **Step 4: Re-run focused tests and all Linux identity regressions GREEN.**
- [ ] **Step 5: Commit the task.**

### Task 5: Real Windows registration smoke and documentation

**Files:**
- Modify: `tools/tool-hub/tests/test_windows_catalog_smoke.py`
- Modify: `tools/tool-hub/README.md`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `tests/test_game_project_operating_system.py`

**Interfaces:**
- Consumes: real `python -m tool_hub.app` on `windows-latest`.
- Produces: two registered path-with-spaces fixture projects and a catalog assertion that all three child tools remain `BLOCKED_PLATFORM`.

- [ ] **Step 1: Extend the Windows smoke first.** Build two committed v2 project fixtures, start a separate Hub process, register both by expected ID, assert the two public entries and no path leakage, and assert all tool launch states remain blocked.
- [ ] **Step 2: Run locally and verify the new smoke is skipped only because the host is not Windows; run its static workflow contract RED if the workflow wiring is incomplete.**
- [ ] **Step 3: Update README with the picker workflow and precise evidence ceiling.** Do not instruct the user to treat registration as child execution.
- [ ] **Step 4: Run all affected local suites.**

```bash
PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests
PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests
node --check tools/tool-hub/web/app.js
.venv/bin/python -m pytest -q tests/test_game_project_operating_system.py
git diff --check
```

- [ ] **Step 5: Commit the task.**

### Task 6: Review, PR, and exact-head evidence

**Files:**
- Modify only if findings require minimal in-scope corrections.

**Interfaces:**
- Produces: exact-head review evidence, GitHub PR, Windows workflow result, and rollback note.

- [ ] **Step 1: Run `attack -> validate-critique -> minimal-fix -> regression-recheck`.** Attack catalog authority, ID mismatch, path disclosure, reparse traversal, CRLF, dirty adapter, project-config drift, and false Windows readiness.
- [ ] **Step 2: Re-run all affected suites after the final diff and verify a clean worktree except intended commits.**
- [ ] **Step 3: Publish a PR through the GitHub connector and wait for exact-head `platform-smoke-windows`, contract, dependency, and `ci-gate` results.**
- [ ] **Step 4: Merge only with P0/P1 zero, unresolved review threads zero, and exact-head checks green; otherwise report the blocker without claiming completion.**
- [ ] **Step 5: Read back merged main and report registration, child execution, Figma, and image/UX evidence as separate statuses.**

## Plan self-review

- Spec coverage: project discovery, exact-ID registration, Windows validation, UI, redaction, real Windows smoke, fail-closed child state, rollback, and next gate each map to one task.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type consistency: `known_projects`, `projects`, `ProjectLocator.register(root, expected_id)`, and the portable validator names are consistent across tasks.
- Scope: Job Objects, Studio staging, Figma mutation, provider generation, game UX judgment, and Android remain explicitly outside this plan.
