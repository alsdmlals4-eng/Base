# Tool Hub Windows Studio Child Ownership Implementation Plan

**Goal:** Make the existing Tool Hub Studio supervisor actually runnable on Windows using a suspended-process Win32 Job Object owner, without weakening Linux behavior or project/startup/health identity.

**Architecture:** Add a narrow `windows_process_owner.py` that owns Win32 Job handles and suspended-child resume. Make environment/adapters choose reviewed Windows path semantics instead of POSIX `/proc/pass_fds`. Integrate through `ProcessSupervisor` with OS-specific spawn/terminate seams and prove the real process tree on `windows-latest`.

## Constraints

- Do not modify open PR #373, #376, or #384.
- No PowerShell, `taskkill`, shell, or arbitrary process fallback.
- Preserve Linux behavior and tests.
- Windows API code stays in one dedicated module.
- No provider/Figma/product work in this PR.
- Exact-head CI + P0/P1=0 required before merge.

### Task 1 — RED: real Windows process ownership contract

Files:
- Create `tools/tool-hub/tests/test_windows_process_owner.py`
- Create `.github/workflows/validate-tool-hub-windows-child.yml`

Test on Windows that the current supervisor cannot start a healthy child and records `BLOCKED_PLATFORM`. Also define expected post-GREEN descendant cleanup behavior. Run Linux supervisor regression in the same workflow.

### Task 2 — Windows native Job owner

Files:
- Create `tools/tool-hub/src/tool_hub/windows_process_owner.py`
- Test `tools/tool-hub/tests/test_windows_process_owner.py`

Implement:
- unnamed `CreateJobObjectW`
- `SetInformationJobObject(JobObjectExtendedLimitInformation)` with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`
- exact PID `OpenProcess` + `AssignProcessToJobObject`
- Toolhelp thread enumeration + `OpenThread` + `ResumeThread`
- `TerminateJobObject` and `CloseHandle`
- fail-closed cleanup if any step fails.

### Task 3 — Windows-safe environment and launch binding

Files:
- Modify `tools/tool-hub/src/tool_hub/environment.py`
- Modify `tools/tool-hub/src/tool_hub/adapters.py`
- Add/modify corresponding tests.

Implement Windows reviewed paths:
- `.venv/Scripts/python.exe`
- `.venv/Lib/site-packages`
- reject symlink/reparse paths/parents
- no `/proc/self/fd`, no `pass_fds`
- preserve runtime pin validation immediately before spawn
- retain `SystemRoot`/`WINDIR` only when needed, without inheriting secrets.

### Task 4 — Supervisor OS-specific spawn/termination

Files:
- Modify `tools/tool-hub/src/tool_hub/supervisor.py`
- Modify/add supervisor tests.

Linux: current `start_new_session=True`, process-group kill.
Windows: `CREATE_SUSPENDED | CREATE_NO_WINDOW`, no `pass_fds`, attach Job, resume, store owner in `_Child`, terminate via Job.

Machine ownership: allow the fixed loopback owner socket on Windows; unsupported OS remains blocked.

Startup-file read: keep POSIX nofollow/UID/link-count path; Windows uses regular-file + no-reparse + bounded exact identity checks.

### Task 5 — Real Windows four-child smoke

Create a Windows-only smoke that starts two projects with expression/sprite fixture child specs, proves four unique PIDs/ports, starts descendants, then `stop_all()` and verifies every process is gone. Add crash/wrong-identity cleanup cases.

### Task 6 — Adversarial review and merge gate

Attack:
- child executes before Job assignment
- descendant escape
- pre-existing/nested job behavior
- handle leak
- PID reuse termination
- startup reparse attack
- path layout drift
- secret inheritance
- Windows failure breaking Linux
- stop race / concurrent same-key start

Record `attack -> validate critique -> minimal correction -> regression recheck` in `docs/reviews/2026-08-14-tool-hub-windows-child-adversarial-review.md`.

Before merge:
- dedicated Windows workflow PASS
- Linux supervisor/adapters/environment regressions PASS
- required Base checks PASS on exact head
- unresolved threads 0
- P0/P1 0

Post-merge IRG must re-read main and distinguish `WINDOWS_STUDIO_CHILD_VERIFIED` from still-unverified provider/Figma/game claims.