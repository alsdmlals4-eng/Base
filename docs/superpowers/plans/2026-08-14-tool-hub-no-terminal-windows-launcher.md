# Tool Hub No-Terminal Windows Launcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install a per-user desktop entry that starts or reopens Base Tool Hub without keeping PowerShell or Command Prompt open.

**Architecture:** Keep the existing FastAPI browser Hub as the only UI and add a small standard-library `.pyw` launcher plus an authenticated installer. The launcher uses the reviewed repository-local `pythonw.exe`, validates exact local identity, reuses a healthy loopback Hub or starts it detached, and opens the browser only after authenticated readiness.

**Tech Stack:** Python 3.12 standard library, FastAPI, Uvicorn `Server`, Windows `pythonw.exe`, vanilla HTML/CSS/JavaScript, pytest, GitHub Actions `windows-latest`.

## Global Constraints

- Normal use must not require an open PowerShell or Command Prompt window.
- Do not add PyInstaller, MSIX, installer frameworks, signing, services, scheduled tasks, tray applications, or admin rights.
- The browser cannot supply paths, executables, ports, argv, environment variables, or PIDs.
- Bind and open only exact `http://127.0.0.1:8764`.
- Never kill or reuse a process merely because it occupies port 8764; require exact authenticated Hub identity.
- Preserve Host, exact Origin, session cookie, and CSRF checks.
- Never store provider, Figma, or Git credentials or raw environment dumps.
- Installing the launcher does not make Windows Studio children, Figma placement, provider generation, or image/UX quality verified.

---

### Task 1: Windows launcher installation contract

**Files:**
- Create: `tools/tool-hub/src/tool_hub/windows_launcher.py`
- Create: `tools/tool-hub/src/tool_hub/windows_launcher_entry.pyw`
- Test: `tools/tool-hub/tests/test_windows_launcher.py`

**Interfaces:**
- Produces: `WindowsLauncherInstaller.install() -> LauncherInstallation`
- Produces: `LauncherInstallation.public_view() -> {state, desktop_entry}` where `desktop_entry` is a display label, never an absolute path.
- Internal config fields: schema version, Base root fingerprint, Base root, project config, expected Hub identity, port 8764, interpreter fingerprint, owner digest.

- [ ] **Step 1: Write failing installer tests**

  Cover non-Windows blocking, exact `%LOCALAPPDATA%` files, Desktop known-folder resolution, regular/non-reparse `pythonw.exe`, `.pyw` association mismatch, atomic writes, duplicate install, changed root/interpreter/owner, no request-controlled values, bounded public states, and no secrets in config.

- [ ] **Step 2: Run focused tests and confirm RED**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_windows_launcher.py`

  Expected: import failure for `tool_hub.windows_launcher`.

- [ ] **Step 3: Implement the installer**

  Use per-user fixed locations, component-safe reads, atomic replacement, and the checked-in template. Resolve the Windows Desktop known folder without changing associations or system settings.

- [ ] **Step 4: Run focused tests and confirm GREEN**

  Run the Task 1 command.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): install no-console Windows launcher"`

### Task 2: Healthy reuse and detached cold start

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/windows_launcher_entry.pyw`
- Test: `tools/tool-hub/tests/test_windows_launcher_runtime.py`

**Interfaces:**
- Produces: `run_launcher(config_path: Path) -> int`
- Internal helpers: exact launcher lock, authenticated health probe, detached spawn, bounded wait, browser open, bounded native error.

- [ ] **Step 1: Write failing runtime tests**

  Cover healthy reuse, one PID under duplicate invocation, wrong service on port, detached flags, fixed argv/minimal env, startup timeout, early exit, changed fingerprints, reparse config/log paths, bounded diagnostics, and browser opening only after exact health.

- [ ] **Step 2: Run tests and confirm RED**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_windows_launcher_runtime.py`

- [ ] **Step 3: Implement minimal runtime behavior**

  Use only standard-library modules. On Windows use detached/no-window creation flags and redirect output to bounded local log files. Do not invoke Git or pip.

- [ ] **Step 4: Run focused tests and confirm GREEN**

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): start and reuse Hub without a console"`

### Task 3: Exact launcher health and graceful server shutdown

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Test: `tools/tool-hub/tests/test_api.py`
- Test: `tools/tool-hub/tests/test_windows_launcher_runtime.py`

**Interfaces:**
- Adds: `GET /api/launcher-status` with tool ID, root fingerprint, config fingerprint, port, and process ID.
- Adds: authenticated `POST /api/shutdown` with an empty body.
- Adds: explicit `run_server(...)` using `uvicorn.Server`; the endpoint requests `server.should_exit=True` after acknowledgement.

- [ ] **Step 1: Write failing API/lifecycle tests**

  Assert exact health identity, wrong-config rejection, shutdown Origin/session/CSRF gates, extra shutdown fields rejection, supervisor stop before listener exit, and no browser-supplied PID.

- [ ] **Step 2: Run focused tests and confirm RED**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_api.py tools/tool-hub/tests/test_windows_launcher_runtime.py`

- [ ] **Step 3: Implement explicit server ownership**

  Inject a shutdown callback into `create_app`; production `main` owns one explicit `uvicorn.Server`. The endpoint schedules only that server's `should_exit` flag.

- [ ] **Step 4: Run focused and supervisor regression tests**

  Run the Task 3 command plus `tools/tool-hub/tests/test_supervisor.py`.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): add authenticated desktop lifecycle"`

### Task 4: Install, repair, and shutdown UI

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Modify: `tools/tool-hub/web/styles.css`
- Test: `tools/tool-hub/tests/test_api.py`
- Test: `tools/tool-hub/tests/test_web_contract.py`

**Interfaces:**
- Adds: authenticated empty-body `POST /api/windows-launcher/install`.
- Changes: `/api/config` includes bounded launcher state only.

- [ ] **Step 1: Write failing UI/API tests**

  Assert Windows-only install/repair button, launcher state copy, no path input, explicit shutdown confirmation, empty payloads, exact CSRF enforcement, and no implication that Studio/Figma/quality verification is complete.

- [ ] **Step 2: Run focused tests and confirm RED**

- [ ] **Step 3: Implement the controls**

  Add `바탕화면 실행 아이콘 설치/복구` and `Tool Hub 종료`. Keep platform-blocked tool cards unchanged.

- [ ] **Step 4: Run focused tests and JavaScript syntax check**

  Run API/web tests and `node --check tools/tool-hub/web/app.js`.

- [ ] **Step 5: Commit**

  `git commit -m "feat(tool-hub): add desktop launcher controls"`

### Task 5: Real Windows no-terminal smoke and docs

**Files:**
- Create: `tools/tool-hub/tests/test_windows_launcher_smoke.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `tools/tool-hub/README.md`
- Modify: `START_HERE.md`

**Interfaces:**
- Adds a `windows-latest` smoke that installs the `.pyw`, starts it with `pythonw.exe`, verifies one exact Hub PID on repeated launch, shuts down through authenticated API, and confirms port/process termination.

- [ ] **Step 1: Write smoke and documentation contract tests**

- [ ] **Step 2: Run locally and confirm the real Windows smoke skips outside Windows**

  Run: `PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_windows_launcher_smoke.py tools/tool-hub/tests/test_web_contract.py`

- [ ] **Step 3: Add the exact Windows workflow invocation and beginner guide**

  Document the one-time transition and subsequent double-click/start/stop flow. Keep remaining Windows Studio child, Figma, and visual quality gates explicit.

- [ ] **Step 4: Run the complete validation matrix**

  Run shared contracts, Tool Hub, Expression, Sprite, QA, root contract tests, both JavaScript checks, `pip check`, and `git diff --check` separately.

- [ ] **Step 5: Commit**

  `git commit -m "test(tool-hub): verify no-terminal Windows lifecycle"`
