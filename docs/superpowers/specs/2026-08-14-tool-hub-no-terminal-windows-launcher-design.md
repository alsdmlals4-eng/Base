# Tool Hub No-Terminal Windows Launcher Design

## Status

`APPROVED_FOR_BUILD` — the user approved a desktop icon that starts the existing browser-based Tool Hub without keeping PowerShell open on 2026-08-14.

## Goal

After one bounded transition installation, let the developer start Tool Hub by double-clicking a desktop item. No PowerShell or Command Prompt window remains open. The launcher starts or reuses the loopback Hub, verifies readiness, opens the browser, records local diagnostics, and provides an authenticated UI shutdown path.

## Existing-solution disposition

| Candidate | Disposition | Reason |
| --- | --- | --- |
| Existing FastAPI/browser Tool Hub | `REUSE` | It is the single reviewed UI and process owner; a second native UI would duplicate authority. |
| Repository-local Python 3.12 virtual environment | `REUSE` | It already contains the exact packages used by the verified Hub. |
| `pythonw.exe` plus a private `.pyw` launcher | `BUILD_MINIMAL` | It runs without a console and avoids bundling a second interpreter or unsigned application binary. |
| Per-user Desktop `.lnk` entry | `ADAPT` | The shortcut directly binds the reviewed `pythonw.exe` and private launcher, avoiding unreliable global `.pyw` association state. |
| Windows Shell Link | `REUSE` | The standard per-user shortcut surface provides direct no-console launch without a second packaged executable. <https://learn.microsoft.com/en-us/windows/win32/shell/links> |
| PyInstaller one-folder EXE | `DEFER` | PyInstaller can bundle an interpreter and dependencies, but it creates a separate distribution/update surface. <https://pyinstaller.org/en/stable/usage.html> |
| Unsigned standalone EXE/MSIX | `REJECT_FOR_CURRENT_PHASE` | Unsigned downloads can trigger strong SmartScreen warnings; trusted signing or Store distribution adds a separate release program and possible cost. <https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation> |
| Always-on Windows service or scheduled task | `REJECT` | Unnecessary persistence and lifecycle authority for a single-user local tool. |

## Architecture

The checked-in launcher template uses only the Python standard library. A fixed Tool Hub installation action writes a machine-local launcher configuration and installs a per-user desktop entry.

```text
Desktop "Base Tool Hub"
  -> reviewed .lnk directly invokes pythonw.exe + private launcher
  -> machine-local launcher reads fixed config
  -> validate Base root + venv pythonw + reviewed Hub files
  -> reuse healthy 127.0.0.1:8764 Hub, or spawn it detached
  -> wait for authenticated /api/launcher-status identity
  -> open default browser
```

No PowerShell process is required for normal start, stop, or project onboarding. The existing browser UI remains the only Tool Hub UI.

## Installation boundary

The current Hub gains an authenticated `POST /api/windows-launcher/install` action shown only on supported Windows hosts. The request has no path, command, arguments, or environment fields.

The installer:

1. Verifies the current Base root and repository-local `.venv\Scripts\pythonw.exe` as regular, non-reparse files.
2. Writes `%LOCALAPPDATA%\BaseToolHub\launcher\launcher-config.json` atomically with the Base root fingerprint, expected Base/Tool Registry commit evidence, Hub port, and machine-local project-config path.
3. Writes the reviewed private `Base Tool Hub.pyw` template atomically under the same launcher directory.
4. Resolves the current user's Desktop known folder and atomically installs one user-visible `Base Tool Hub.lnk` through the in-process Windows `IShellLinkW`/`IPersistFile` COM contract, without launching PowerShell or requiring administrator rights.
5. The shortcut directly targets the reviewed `pythonw.exe` with the private launcher as its fixed argument. It never changes global file associations, all-users locations, the Start Menu, or taskbar pins.
6. When upgrading, remove the old Desktop `Base Tool Hub.pyw` only after it byte-matches the reviewed launcher and the new `.lnk` is published. Any mismatched or non-regular legacy entry blocks with a bounded repair state.

The transition from the already installed old Hub requires one final Base update. It can be performed through GitHub Desktop followed by double-clicking the checked-in installer, or by the existing one-block PowerShell path. After launcher installation succeeds, normal use does not require a terminal.

## Launcher behavior

1. Load the bounded config from `%LOCALAPPDATA%` without following reparse links.
2. Validate required string fields, exact loopback port `8764`, Base root fingerprint, `.venv` interpreter identity, reviewed Tool Registry, and Hub owner bytes before every start.
3. Probe `http://127.0.0.1:8764/api/launcher-status` with a short timeout.
4. If the endpoint returns the exact Tool Hub identity and root/config fingerprints, open the browser and exit the launcher.
5. If the port is occupied by any other service or identity, show a native Windows error and do not kill or reuse it.
6. If the port is free, start the reviewed interpreter with a fixed argv, detached from the console, with a minimal environment and logs redirected to new bounded files under `%LOCALAPPDATA%\BaseToolHub\logs`.
7. Poll until exact health succeeds or the child exits/timeout occurs. Open the browser only after success.
8. On failure, show a native Windows message box containing a bounded reason code and the local log folder location, never raw secrets or arbitrary child output.

The launcher does not run `git pull`, `pip install`, edit Base, change branches, kill unrelated processes, or infer readiness from process existence alone.

## Server lifecycle and shutdown

`tool_hub.app` exposes an authenticated, CSRF-protected `POST /api/shutdown` action only for the exact local session. The UI shows `Tool Hub 종료` and requires a confirmation click.

The application owns an explicit Uvicorn `Server` instance. Shutdown sets `server.should_exit`, stops owned Studio children through the existing supervisor lifecycle, flushes logs/config, closes the listener, and returns a bounded acknowledgement before exit. It never kills a PID supplied by the browser.

Closing the browser does not stop the Hub. A later desktop launch reuses the healthy process. This is deliberate so the user can close and reopen the UI without restarting child tools. Windows logout or reboot naturally terminates the user process tree.

## Security and authority

- Bind only `127.0.0.1`; no LAN or remote access.
- Preserve exact Host/Origin/session/CSRF checks.
- No browser-controlled executable, working directory, port, environment, command, Git option, or destination path.
- Do not place provider keys, Figma credentials, Git credentials, or full environment dumps in config/logs.
- Reject symlink/reparse components and changed owner/interpreter/registry evidence before spawn.
- Use an exclusive per-user launcher lock so repeated double-clicks converge on one Hub.
- Treat the same Windows user and device administrator as trusted, matching the current `HARDENED_RUNTIME_DEFERRED` boundary.
- Installing a launcher proves orchestration only. It does not make Windows Studio children, Figma placement, paid provider generation, or image/UX quality verified.

## User-visible states

- `설치됨`: desktop launcher config and entry match the current verified Base root.
- `업데이트 필요`: Base/venv owner identity changed; reinstall the launcher from a verified Hub.
- `실행 중`: exact Hub health verified.
- `포트 충돌`: port 8764 belongs to another process/identity; no automatic kill.
- `설치 복구 필요`: config, interpreter, or launcher evidence is missing/invalid.

## Verification

- TDD tests for install payload rejection, fixed paths, atomic config/template writes, known-folder resolution, duplicate install, and uninstall/repair behavior.
- Launcher tests for healthy reuse, cold start, repeated double-click, wrong service on port, startup timeout, early child exit, changed Base/interpreter/registry, reparse paths, bounded logs, and native bounded error reporting.
- Server tests for authenticated shutdown, missing/wrong CSRF, unrelated PID non-acceptance, supervisor stop ordering, listener close, and restart after shutdown.
- Real `windows-latest` smoke opens the Desktop `.lnk`, verifies exact HTTP identity, launches it again to reuse one PID, requests UI shutdown, and verifies the process/listener are gone.
- Live user-PC smoke closes PowerShell, double-clicks the desktop entry, opens the browser, closes/reopens the browser, and shuts down from the UI.

## Exclusions and next gate

- No Microsoft Store submission, MSIX, code-signing purchase, updater service, scheduled task, system service, tray application, or native replacement UI.
- No automatic Base update or dependency installation during normal launch.
- No Windows Expression/Sprite/QA child enablement in this sub-project. That remains the next Job Object/process-tree phase.
- No Figma mutation, Android testing, or actual game image/UX judgment.

## Rollback

Remove the desktop/Start Menu entry and `%LOCALAPPDATA%\BaseToolHub\launcher` configuration. Revert the installer, launcher, health, and shutdown code. The existing PowerShell/module launch remains available, project locator data is preserved, and no project repository or Figma file is changed.
