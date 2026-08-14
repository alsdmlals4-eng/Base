@echo off
if /I "%~1"=="--contract-test" (
  echo INSTALLER_V4_CONTRACT_OK
  exit /b 0
)
if /I not "%~1"=="--inner" (
  start "Base Loop A2 Installer v4" "%ComSpec%" /d /k ""%~f0" --inner"
  exit /b
)

setlocal EnableExtensions EnableDelayedExpansion
title Base Loop A2 Local Executor Installer v4

set "INSTALL_ROOT=%LOCALAPPDATA%\BaseLoopA2LocalExecutorApp"
set "BASE_SRC=%INSTALL_ROOT%\Base"
set "VENV=%INSTALL_ROOT%\.venv"
set "STATE_ROOT=%LOCALAPPDATA%\BaseLoopA2LocalExecutor"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "STARTUP_CMD=%STARTUP_DIR%\BaseLoopA2LocalExecutor.cmd"
set "LOG=%USERPROFILE%\Desktop\Base_Loop_A2_Installer.log"
set "IMAGE_REF=python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65"
set "PREFLIGHT_FILE=%TEMP%\base-a2-preflight-%RANDOM%-%RANDOM%.txt"

>"!LOG!" echo Base Loop A2 Local Executor Installer v4
>>"!LOG!" echo Started: %DATE% %TIME%
>>"!LOG!" echo.

echo.
echo ============================================================
echo   Base Loop A2 Local Executor - installer/updater v4
echo ============================================================
echo.
echo Double-click operation: no PowerShell window or manual terminal step is required.
echo This window will stay open even if installation is blocked.
echo Log file:
echo   !LOG!
echo.

echo [0/8] Resolving trusted local commands...
call :resolve GIT_CMD git "%ProgramFiles%\Git\cmd\git.exe"
if errorlevel 1 goto :blocked_git
call :resolve GH_CMD gh "%ProgramFiles%\GitHub CLI\gh.exe"
if errorlevel 1 goto :blocked_gh_command
call :resolve DOCKER_CMD docker "%ProgramFiles%\Docker\Docker\resources\bin\docker.exe"
if errorlevel 1 goto :blocked_docker_command
call :resolve CODEX_CMD codex "%APPDATA%\npm\codex.cmd"
if errorlevel 1 goto :blocked_codex_command
call :resolve POWERSHELL_CMD powershell "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if errorlevel 1 goto :blocked_process_probe
call :resolve_optional NODE_CMD node "%ProgramFiles%\nodejs\node.exe"

for %%I in ("!GIT_CMD!") do set "PATH=%%~dpI;!PATH!"
for %%I in ("!GH_CMD!") do set "PATH=%%~dpI;!PATH!"
for %%I in ("!DOCKER_CMD!") do set "PATH=%%~dpI;!PATH!"
for %%I in ("!CODEX_CMD!") do set "PATH=%%~dpI;!PATH!"
if defined NODE_CMD for %%I in ("!NODE_CMD!") do set "PATH=%%~dpI;!PATH!"

echo [OK] git:    !GIT_CMD!
echo [OK] gh:     !GH_CMD!
echo [OK] docker: !DOCKER_CMD!
echo [OK] codex:  !CODEX_CMD!
if defined NODE_CMD echo [OK] node:   !NODE_CMD!

>>"!LOG!" echo Resolved git=!GIT_CMD!
>>"!LOG!" echo Resolved gh=!GH_CMD!
>>"!LOG!" echo Resolved docker=!DOCKER_CMD!
>>"!LOG!" echo Resolved codex=!CODEX_CMD!
>>"!LOG!" echo Resolved node=!NODE_CMD!

echo.
echo [1/8] GitHub authentication...
"!GH_CMD!" auth status --hostname github.com >>"!LOG!" 2>&1
if errorlevel 1 goto :blocked_gh_auth
echo [OK] GitHub authenticated.

echo.
echo [2/8] Codex ChatGPT authentication...
set "CODEX_STATUS_FILE=%TEMP%\base-a2-codex-status-%RANDOM%-%RANDOM%.txt"
"%ComSpec%" /d /s /c ""!CODEX_CMD!" login status" >"!CODEX_STATUS_FILE!" 2>&1
set "CODEX_RC=!ERRORLEVEL!"
set "CODEX_STATUS="
if exist "!CODEX_STATUS_FILE!" set /p CODEX_STATUS=<"!CODEX_STATUS_FILE!"
if exist "!CODEX_STATUS_FILE!" type "!CODEX_STATUS_FILE!" >>"!LOG!"
if exist "!CODEX_STATUS_FILE!" del /q "!CODEX_STATUS_FILE!" >nul 2>&1
if not "!CODEX_RC!"=="0" goto :blocked_codex_status
if /I not "!CODEX_STATUS!"=="Logged in using ChatGPT" goto :blocked_codex_auth
echo [OK] Codex authenticated using ChatGPT.

echo.
echo [3/8] Docker Desktop / Engine...
"!DOCKER_CMD!" version >>"!LOG!" 2>&1
if errorlevel 1 goto :blocked_docker_engine
echo [OK] Docker Engine ready.

echo.
echo [4/8] Python 3.12+...
set "PY_KIND="
set "PY_LAUNCHER="
set "PY_DIRECT="
for /f "delims=" %%I in ('where py 2^>nul') do if not defined PY_LAUNCHER set "PY_LAUNCHER=%%I"
if defined PY_LAUNCHER (
  "!PY_LAUNCHER!" -3.12 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)" >>"!LOG!" 2>&1
  if not errorlevel 1 set "PY_KIND=launcher312"
  if not defined PY_KIND (
    "!PY_LAUNCHER!" -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)" >>"!LOG!" 2>&1
    if not errorlevel 1 set "PY_KIND=launcher3"
  )
)
if not defined PY_KIND (
  for /f "delims=" %%I in ('where python 2^>nul') do if not defined PY_DIRECT set "PY_DIRECT=%%I"
  if not defined PY_DIRECT if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_DIRECT=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  if not defined PY_DIRECT if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PY_DIRECT=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  if defined PY_DIRECT (
    "!PY_DIRECT!" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)" >>"!LOG!" 2>&1
    if not errorlevel 1 set "PY_KIND=direct"
  )
)
if not defined PY_KIND goto :blocked_python
echo [OK] Python 3.12+ found.

echo.
echo [5/8] Stop only the existing executor-owned background daemon...
call :stop_existing_daemon >>"!LOG!" 2>&1
if errorlevel 1 goto :blocked_daemon_stop
echo [OK] Existing owned daemon stopped or none was running.

echo.
echo [6/8] Update Base main and refresh executor environment...
if not exist "!INSTALL_ROOT!" mkdir "!INSTALL_ROOT!" >>"!LOG!" 2>&1
if not exist "!STATE_ROOT!" mkdir "!STATE_ROOT!" >>"!LOG!" 2>&1
if exist "!BASE_SRC!\.git" (
  "!GIT_CMD!" -C "!BASE_SRC!" fetch origin main --prune >>"!LOG!" 2>&1
  if errorlevel 1 goto :blocked_git_sync
  "!GIT_CMD!" -C "!BASE_SRC!" checkout --detach origin/main >>"!LOG!" 2>&1
  if errorlevel 1 goto :blocked_git_sync
) else (
  if exist "!BASE_SRC!" rmdir /s /q "!BASE_SRC!" >>"!LOG!" 2>&1
  "!GIT_CMD!" clone --filter=blob:none --no-tags https://github.com/alsdmlals4-eng/Base.git "!BASE_SRC!" >>"!LOG!" 2>&1
  if errorlevel 1 goto :blocked_git_sync
  "!GIT_CMD!" -C "!BASE_SRC!" checkout --detach origin/main >>"!LOG!" 2>&1
  if errorlevel 1 goto :blocked_git_sync
)
if not exist "!VENV!\Scripts\python.exe" (
  if /I "!PY_KIND!"=="launcher312" "!PY_LAUNCHER!" -3.12 -m venv "!VENV!" >>"!LOG!" 2>&1
  if /I "!PY_KIND!"=="launcher3" "!PY_LAUNCHER!" -3 -m venv "!VENV!" >>"!LOG!" 2>&1
  if /I "!PY_KIND!"=="direct" "!PY_DIRECT!" -m venv "!VENV!" >>"!LOG!" 2>&1
  if errorlevel 1 goto :blocked_venv
)
"!VENV!\Scripts\python.exe" -m pip install --disable-pip-version-check -e "!BASE_SRC!\tools\loop-a2-local-executor" >>"!LOG!" 2>&1
if errorlevel 1 goto :blocked_executor_install
echo [OK] Local Executor refreshed from completed Base main.

echo.
echo [7/8] Executor shared preflight...
call :capture_preflight
if not errorlevel 1 goto :preflight_ready
findstr /C:"DOCKER_IMAGE_NOT_PRELOADED" "!PREFLIGHT_FILE!" >nul 2>&1
if errorlevel 1 goto :blocked_preflight

echo Reviewed image is not ready for the Docker server platform; pulling the exact pinned digest...
"!DOCKER_CMD!" pull "!IMAGE_REF!" >>"!LOG!" 2>&1
if errorlevel 1 goto :blocked_docker_image

echo Executor shared preflight after exact image pull...
call :capture_preflight
if errorlevel 1 goto :blocked_preflight

:preflight_ready
if exist "!PREFLIGHT_FILE!" del /q "!PREFLIGHT_FILE!" >nul 2>&1
echo [OK] Shared Local Executor preflight passed.

echo.
echo [8/8] Background start + Windows startup registration...
if not exist "!STARTUP_DIR!" mkdir "!STARTUP_DIR!" >>"!LOG!" 2>&1
for %%I in ("!GIT_CMD!") do set "GIT_DIR=%%~dpI"
for %%I in ("!GH_CMD!") do set "GH_DIR=%%~dpI"
for %%I in ("!DOCKER_CMD!") do set "DOCKER_DIR=%%~dpI"
for %%I in ("!CODEX_CMD!") do set "CODEX_DIR=%%~dpI"
set "NODE_DIR="
if defined NODE_CMD for %%I in ("!NODE_CMD!") do set "NODE_DIR=%%~dpI"

>"!STARTUP_CMD!" echo @echo off
>>"!STARTUP_CMD!" echo set "PATH=!GIT_DIR!;!GH_DIR!;!DOCKER_DIR!;!CODEX_DIR!;!NODE_DIR!;%%PATH%%"
>>"!STARTUP_CMD!" echo start "" "!VENV!\Scripts\pythonw.exe" -m loop_a2_local_executor.cli --state-root "!STATE_ROOT!" daemon --poll-seconds 60
>>"!STARTUP_CMD!" echo exit /b 0

set "PATH=!GIT_DIR!;!GH_DIR!;!DOCKER_DIR!;!CODEX_DIR!;!NODE_DIR!;!PATH!"
start "" "!VENV!\Scripts\pythonw.exe" -m loop_a2_local_executor.cli --state-root "!STATE_ROOT!" daemon --poll-seconds 60

set /a DAEMON_TRIES=0
:wait_for_daemon
set /a DAEMON_TRIES+=1
call :confirm_daemon >>"!LOG!" 2>&1
if not errorlevel 1 goto :daemon_ready
if !DAEMON_TRIES! GEQ 10 goto :blocked_daemon_start
timeout /t 1 /nobreak >nul
goto :wait_for_daemon

:daemon_ready
>>"!LOG!" echo LOCAL_EXECUTOR_DAEMON_RUNNING
>>"!LOG!" echo LOCAL_EXECUTOR_READY

echo.
echo ============================================================
echo   LOCAL_EXECUTOR_READY
echo ============================================================
echo.
echo GitHub:       READY
echo Codex:        READY (ChatGPT)
echo Docker:       READY
echo Docker image: READY (shared executor preflight)
echo Executor:     INSTALLED / UPDATED
echo Background:   STARTED
echo Startup:      REGISTERED
echo.
echo Send this exact text to ChatGPT:
echo.
echo LOCAL_EXECUTOR_READY
echo.
echo Log:
echo   !LOG!
echo.
echo This window will remain open. Close it manually when finished.
goto :end

:capture_preflight
"!VENV!\Scripts\loop-a2-local-executor.exe" --state-root "!STATE_ROOT!" preflight >"!PREFLIGHT_FILE!" 2>&1
set "PREFLIGHT_RC=!ERRORLEVEL!"
if exist "!PREFLIGHT_FILE!" type "!PREFLIGHT_FILE!" >>"!LOG!"
if exist "!PREFLIGHT_FILE!" type "!PREFLIGHT_FILE!"
exit /b !PREFLIGHT_RC!

:stop_existing_daemon
if not exist "!VENV!\Scripts\pythonw.exe" exit /b 0
set "BASE_A2_EXPECTED_PYTHONW=!VENV!\Scripts\pythonw.exe"
set "BASE_A2_STATE_ROOT=!STATE_ROOT!"
"!POWERSHELL_CMD!" -NoLogo -NoProfile -NonInteractive -Command "$ErrorActionPreference='Stop'; $expected=[IO.Path]::GetFullPath($env:BASE_A2_EXPECTED_PYTHONW); $state=[IO.Path]::GetFullPath($env:BASE_A2_STATE_ROOT); Get-CimInstance Win32_Process -Filter \"Name='pythonw.exe'\" | ForEach-Object { if ($_.ExecutablePath -and $_.CommandLine) { try { $exe=[IO.Path]::GetFullPath($_.ExecutablePath); if (($exe -ieq $expected) -and $_.CommandLine.Contains('loop_a2_local_executor.cli') -and $_.CommandLine.Contains($state)) { Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop } } catch { throw } } }"
set "STOP_RC=!ERRORLEVEL!"
set "BASE_A2_EXPECTED_PYTHONW="
set "BASE_A2_STATE_ROOT="
exit /b !STOP_RC!

:confirm_daemon
set "BASE_A2_EXPECTED_PYTHONW=!VENV!\Scripts\pythonw.exe"
set "BASE_A2_STATE_ROOT=!STATE_ROOT!"
"!POWERSHELL_CMD!" -NoLogo -NoProfile -NonInteractive -Command "$ErrorActionPreference='Stop'; $expected=[IO.Path]::GetFullPath($env:BASE_A2_EXPECTED_PYTHONW); $state=[IO.Path]::GetFullPath($env:BASE_A2_STATE_ROOT); $found=$false; Get-CimInstance Win32_Process -Filter \"Name='pythonw.exe'\" | ForEach-Object { if ($_.ExecutablePath -and $_.CommandLine) { try { $exe=[IO.Path]::GetFullPath($_.ExecutablePath); if (($exe -ieq $expected) -and $_.CommandLine.Contains('loop_a2_local_executor.cli') -and $_.CommandLine.Contains($state)) { $found=$true } } catch {} } }; if ($found) { Write-Output 'LOCAL_EXECUTOR_DAEMON_RUNNING'; exit 0 } else { exit 2 }"
set "CONFIRM_RC=!ERRORLEVEL!"
set "BASE_A2_EXPECTED_PYTHONW="
set "BASE_A2_STATE_ROOT="
exit /b !CONFIRM_RC!

:blocked_git
call :blocked "git command was not found."
goto :end
:blocked_gh_command
call :blocked "gh command was not found."
goto :end
:blocked_docker_command
call :blocked "docker command was not found. Docker Desktop may need a restart."
goto :end
:blocked_codex_command
call :blocked "codex command was not found. Trusted command resolution and the standard npm shim were checked."
goto :end
:blocked_process_probe
call :blocked "Windows process identity probe is unavailable; the updater will not use a broad process kill fallback."
goto :end
:blocked_gh_auth
call :blocked "GitHub CLI authentication is not ready."
goto :end
:blocked_codex_status
call :blocked "Codex login status command failed."
goto :end
:blocked_codex_auth
call :blocked "Codex is not authenticated using ChatGPT. Status: !CODEX_STATUS!"
goto :end
:blocked_docker_engine
call :blocked "Docker Desktop is installed but the Docker Engine is not reachable."
goto :end
:blocked_python
call :blocked "Python 3.12 or newer was not found."
goto :end
:blocked_daemon_stop
call :blocked "The existing owned Local Executor daemon could not be stopped safely."
goto :end
:blocked_git_sync
call :blocked "Base repository clone/update failed; no reset or clean fallback was used."
goto :end
:blocked_venv
call :blocked "Dedicated Python environment creation failed."
goto :end
:blocked_executor_install
call :blocked "Loop A2 Local Executor package refresh failed."
goto :end
:blocked_docker_image
call :blocked "The exact reviewed Docker image could not be downloaded after the shared preflight reported DOCKER_IMAGE_NOT_PRELOADED."
goto :end
:blocked_preflight
call :blocked "Local Executor shared preflight failed. See the log for the bounded blocker code."
goto :end
:blocked_daemon_start
call :blocked "The exact Local Executor background daemon identity was not observed after startup."
goto :end

:blocked
echo.
echo ============================================================
echo   INSTALLATION_BLOCKED
echo ============================================================
echo.
echo [BLOCKED] %~1
echo.
echo Log:
echo   !LOG!
echo.
>>"!LOG!" echo.
>>"!LOG!" echo [BLOCKED] %~1
exit /b 0

:resolve
set "%~1="
for /f "delims=" %%I in ('where %~2 2^>nul') do if not defined %~1 set "%~1=%%I"
if not defined %~1 if exist "%~3" set "%~1=%~3"
if not defined %~1 exit /b 1
exit /b 0

:resolve_optional
set "%~1="
for /f "delims=" %%I in ('where %~2 2^>nul') do if not defined %~1 set "%~1=%%I"
if not defined %~1 if exist "%~3" set "%~1=%~3"
exit /b 0

:end
if exist "!PREFLIGHT_FILE!" del /q "!PREFLIGHT_FILE!" >nul 2>&1
echo.
echo You may close this window manually.
echo If blocked, send me the [BLOCKED] line or the log file contents.
echo.
