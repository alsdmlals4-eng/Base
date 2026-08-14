# Tool Hub Windows Studio Child Ownership Design

Issue: #385

## Goal

Replace the current Windows `BLOCKED_PLATFORM` supervisor boundary with a native, fail-closed Windows child process-tree owner while preserving the existing Linux process-group path and all project/startup/health identity checks.

## Existing-solution-first comparison

| Approach | Verdict | Reason |
|---|---|---|
| `taskkill /T` | REJECT | External command, weaker ownership semantics, PID/race surface, and unnecessary shell/tool dependency. |
| `CREATE_NEW_PROCESS_GROUP` only | REJECT | Useful for console control signals but not sufficient as descendant-tree lifetime ownership. |
| Job Object assigned after a running `Popen` | REJECT | Leaves a race where reviewed child code can run before assignment. |
| **Suspended child + Win32 Job Object + resume** | **RECOMMENDED** | The child cannot execute before Job assignment. `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` gives bounded descendant cleanup. |
| Full custom `CreateProcessW` launcher | DEFER | Maximum control but duplicates Python subprocess environment/pipe handling. Use only if the Popen suspended seam proves insufficient. |

## Native ownership sequence

On Windows 10/11-class supported environments:

1. `subprocess.Popen` creates the reviewed Python child with raw Win32 `CREATE_SUSPENDED` plus `CREATE_NO_WINDOW`.
2. A dedicated `WindowsJobOwner` creates an unnamed Job Object.
3. Configure `JOBOBJECT_EXTENDED_LIMIT_INFORMATION.BasicLimitInformation.LimitFlags` with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`.
4. Open the suspended child process by exact PID with the minimum required process rights and call `AssignProcessToJobObject`.
5. Enumerate the new process's threads. Before any thread is resumed there must be exactly one primary thread owned by that PID.
6. Open that thread with `THREAD_SUSPEND_RESUME`, call `ResumeThread`, and close the thread/process helper handles.
7. Keep the Job Object handle exclusively in the `_Child` record until stop/failure cleanup.
8. Stop uses `TerminateJobObject`, waits for the direct process, then closes the Job handle. Failure cleanup closes/terminates the same job. Descendants are never selected by PID scanning for termination.

If any Job creation/configuration/assignment/thread enumeration/resume step fails, close the Job handle and terminate the still-suspended process before returning `START_FAILED`.

## Windows-safe local file/runtime boundary

The current POSIX path assumes `O_NOFOLLOW`, descriptor-bound `/proc/self/fd`, `st_uid`, POSIX modes and `pass_fds`. Windows must not fake those guarantees.

For Windows:

- validate runtime/source/interpreter paths with `lstat`, reject symlinks and `FILE_ATTRIBUTE_REPARSE_POINT` on every relevant path/parent;
- use the exact reviewed `.venv/Scripts/python.exe` and `.venv/Lib/site-packages` layout;
- re-run runtime pin/source identity validation immediately before process creation;
- do not use `pass_fds` or `/proc/self/fd` rewriting;
- use atomic create-only startup publication and reject reparse startup paths;
- startup read verifies a regular non-reparse file, bounded size, exact JSON identity, then health identity;
- keep the documented same-OS-user trust boundary: this is not a hardened sandbox against a malicious process already running as the same user.

Linux keeps descriptor binding, `pass_fds`, UID/mode/link-count checks and process groups unchanged.

## Machine ownership

The existing loopback ownership socket is portable enough for Windows and avoids adding a second external daemon. Permit the same fixed loopback ownership endpoint on Windows; keep unsupported platforms fail-closed.

## Child environment

Windows clean environment retains only reviewed values plus the platform variables required for Python/Win32 startup (`SystemRoot`/`WINDIR` when present). It must not inherit OpenAI/API/provider credentials or arbitrary parent environment values.

## Tests / IRG

Automated contract tests must include:

- Windows environment/runtime/interpreter layout.
- Current pre-implementation RED: Windows real supervisor start is `BLOCKED_PLATFORM`.
- Actual Windows runner starts an authenticated child with descendant; supervisor stop proves direct child + descendant gone.
- Wrong nonce/PID/hash, crash and startup timeout clean the Job tree.
- same key is idempotent.
- two projects × expression/sprite = four independent Windows child PIDs/ports.
- no PowerShell/taskkill/shell fallback.
- Linux full supervisor/adapters/environment regressions stay green.

A Windows runner smoke proves process ownership only. It does not prove real provider generation, Figma delivery, human visual approval, or Godot integration.

## Rollback

Revert the implementation PR. No project data migration occurs; Windows child launching returns to `BLOCKED_PLATFORM`.