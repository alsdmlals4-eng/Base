# Tool Hub Managed Project Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a user select one reviewed project and have Tool Hub safely find or clone its exact GitHub repository without typing a local path.

**Architecture:** Extend the existing canonical Figma routing registry with a validated repository pointer, then add one Tool Hub onboarding service that owns bounded discovery, transactional clone, identity validation, Asset Vault initialization, and locator registration. The browser sends only a reviewed `project_id`; it never supplies a URL, filesystem path, Git option, command, or environment variable.

**Tech Stack:** Python 3.12, FastAPI, Pydantic, standard-library filesystem/process APIs, Git CLI with fixed argv, vanilla HTML/CSS/JavaScript, pytest, JSON Schema.

## Global Constraints

- Reuse `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`; do not create a second project catalog.
- Default Windows managed root is `%USERPROFILE%\Documents\GitHub`.
- Never recursively scan a drive or the whole user profile.
- Never fetch, pull, reset, clean, checkout, migrate, overwrite, merge into, or delete an existing repository.
- Clone only the exact reviewed HTTPS GitHub URL with `shell=False` and a minimal environment.
- The request body contains no URL, path, branch, command, option, or environment field.
- Create `.asset-vault/library` only when the checkout's committed ignore rules already ignore `.asset-vault/`; never edit `.gitignore` or tracked files.
- Figma data is routing metadata only; onboarding does not call or mutate Figma.
- Public responses contain bounded states only and never expose absolute paths, Git stderr, commands, environment, credentials, or staging names.
- Preserve manual `POST /api/projects` registration as a compatibility fallback until a separate removal approval.

---

### Task 1: Canonical repository pointers

**Files:**
- Modify: `schemas/project-figma-target-registry-v1.schema.json`
- Modify: `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/figma_routing.py`
- Test: `tools/base-tool-contracts/tests/test_figma_routing.py`
- Test: `tests/test_project_figma_workspace_registry.py`

**Interfaces:**
- Produces: `ProjectRepositoryPointer(project_id, display_name, repository_url, repository_name, routing_state)`
- Produces: `ProjectFigmaRegistry.repository_pointer(project_id) -> ProjectRepositoryPointer`
- Changes: `ProjectFigmaRegistry.public_projects()` includes `repository_name`, not the full URL.

- [ ] **Step 1: Write failing schema and loader tests**

  Add tests asserting all eight exact project/URL tuples, rejecting credentials, query, fragment, non-HTTPS, non-GitHub hosts, duplicate repository URLs, and mismatched `.git` repository names.

- [ ] **Step 2: Run the focused tests and confirm RED**

  Run: `PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests/test_figma_routing.py tests/test_project_figma_workspace_registry.py`

  Expected: failures for missing `repository_url` and missing `repository_pointer`.

- [ ] **Step 3: Implement the exact schema and loader contract**

  Require `repository_url` and validate it as `https://github.com/<owner>/<repo>.git` with no userinfo, port, query, or fragment. Derive `repository_name` from the final path component; do not accept it from the browser.

- [ ] **Step 4: Run focused tests and confirm GREEN**

  Run the Task 1 command and require zero failures.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): add reviewed project repository pointers"`

### Task 2: Bounded discovery and public state model

**Files:**
- Create: `tools/tool-hub/src/tool_hub/onboarding.py`
- Modify: `tools/tool-hub/src/tool_hub/projects.py`
- Test: `tools/tool-hub/tests/test_onboarding.py`

**Interfaces:**
- Produces: `OnboardingState(project_id: str, state: str, detail: str).public_view() -> dict[str, str]`
- Produces: `ProjectOnboardingService.status(project_id: str) -> OnboardingState`
- Produces: `ProjectOnboardingService.onboard(project_id: str) -> OnboardingState`
- Consumes: `ProjectFigmaRegistry.repository_pointer(project_id)` and `ProjectLocator.register(path, project_id)`.

- [ ] **Step 1: Write failing bounded-discovery tests**

  Cover saved locator, exact `<Documents/GitHub>/<repo>`, exact `<source/repos>/<repo>`, absent checkout, wrong origin, wrong adapter ID, path occupied by a non-repository, and symlink/reparse candidates. Assert no recursive enumeration and no public absolute paths.

- [ ] **Step 2: Run the tests and confirm RED**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_onboarding.py`

  Expected: import failure for `tool_hub.onboarding`.

- [ ] **Step 3: Implement discovery and state mapping**

  Use exact derived candidate names only. Compare `git remote get-url origin` to the reviewed URL after canonical GitHub HTTPS normalization. Map all internal failures to `REGISTERED`, `FOUND_UNREGISTERED`, `CLONE_AVAILABLE`, `PROJECT_SETUP_REQUIRED`, `PATH_OCCUPIED`, or `IDENTITY_MISMATCH` without including paths.

- [ ] **Step 4: Run focused and locator regression tests**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_onboarding.py tools/tool-hub/tests/test_projects.py`

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): discover reviewed projects automatically"`

### Task 3: Transactional clone and Asset Vault bootstrap

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/onboarding.py`
- Test: `tools/tool-hub/tests/test_onboarding.py`

**Interfaces:**
- Adds: per-project in-process lock and fixed Git runner injected only by tests.
- Adds: internal `_clone_and_register(pointer) -> ProjectBinding` transaction.

- [ ] **Step 1: Write failing clone transaction tests**

  Cover fixed argv, `shell=False`, minimal environment, successful clone/identity/register, effective ignore validation, absent ignore rule, duplicate clicks, clone error classification, credential/auth error classification, final-path race, wrong origin, wrong project ID, staging quarantine, and no locator write on failure.

- [ ] **Step 2: Run focused tests and confirm RED**

  Run the Task 2 focused command and confirm failures are caused by missing clone behavior.

- [ ] **Step 3: Implement minimal transactional clone**

  Clone into an exclusive random sibling, validate the complete checkout, initialize only ignored `.asset-vault/library`, publish by atomic rename to an absent destination, revalidate, then write the locator. Existing paths remain untouched.

- [ ] **Step 4: Run all onboarding tests and confirm GREEN**

  Run Task 2's combined command.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): clone reviewed projects transactionally"`

### Task 4: API and human-friendly project cards

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Modify: `tools/tool-hub/web/styles.css`
- Test: `tools/tool-hub/tests/test_api.py`
- Test: `tools/tool-hub/tests/test_web_contract.py`

**Interfaces:**
- Adds: `POST /api/projects/{project_id}/onboard` with an empty body.
- Changes: `/api/catalog.known_projects[]` adds `local_state` and `action_label`.
- Preserves: authenticated Origin/session/CSRF checks on every mutation.

- [ ] **Step 1: Write failing API and web contract tests**

  Assert project cards show name/state/action, no local path field is required, the onboarding request contains only the URL project ID, unknown IDs fail, extra request fields fail, repeated clicks are disabled, and manual registration remains server-compatible but is no longer the primary UI.

- [ ] **Step 2: Run focused tests and confirm RED**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_api.py tools/tool-hub/tests/test_web_contract.py`

- [ ] **Step 3: Implement the API and cards**

  Wire the single onboarding service into the catalog and endpoint. Render a project list with `PC에서 찾기`, `자동 설치 및 연결`, `연결됨`, or `조치 필요`, and never render or request an absolute path.

- [ ] **Step 4: Run focused tests and JavaScript syntax check**

  Run the Task 4 test command and `node --check tools/tool-hub/web/app.js`.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): add one-click project onboarding UI"`

### Task 5: Windows smoke, operating docs, and closeout

**Files:**
- Modify: `tools/tool-hub/tests/test_windows_catalog_smoke.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `tools/tool-hub/README.md`
- Modify: `START_HERE.md`

**Interfaces:**
- Adds a Windows smoke that discovers one exact checkout and clones one local fixture repository through the public endpoint, without a browser path.

- [ ] **Step 1: Write the Windows smoke and documentation contract assertions**

- [ ] **Step 2: Run Linux-portable portions and confirm expected Windows skip**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_windows_catalog_smoke.py tools/tool-hub/tests/test_web_contract.py`

- [ ] **Step 3: Update workflow and beginner documentation**

  Document exact states, non-destructive behavior, GitHub Desktop authentication fallback, and that Figma is not changed by onboarding.

- [ ] **Step 4: Run the full verification matrix**

  Run Tool Hub, shared contracts, root registry tests, JavaScript syntax, `pip check`, and `git diff --check` as separate commands.

- [ ] **Step 5: Commit**

  `git commit -m "test(tool-hub): verify managed Windows onboarding"`
