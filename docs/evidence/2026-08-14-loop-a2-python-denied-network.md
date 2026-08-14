# Loop A2 Python DENIED Network Evidence — 2026-08-14

## Scope

Issue #368 adds a narrow language-runtime network/process escape boundary for Runtime Adapter commands shaped exactly as `python -m unittest ...` with `network: DENIED`.

This is **not** a general OS sandbox. Any unsupported executable, Python `-c`, non-unittest module, `READ_ONLY_APPROVED`, or unknown policy remains blocked by the existing `ProjectTestExecutor` fail-closed behavior and must not be relabeled network-safe.

No OpenAI request, model selection, project product write, A3, Scheduler, PR/merge authority, or general network permission is introduced.

## TDD evidence

### RED 1 — implementation absent

The first test/workflow-only head failed before the intended contract because the dedicated workflow had not installed Base's standard validation requirements (`jsonschema`). The workflow was corrected without product/runtime changes.

Corrected RED head: `f3869b72b505ce58f7c8e0034360a1e5871bc222`.

Dedicated workflow run `31798362875` reached the actual contract and failed all nine tests because `tools.loop_a2_runtime.python_denied_network` did not exist.

### GREEN 1 — Ubuntu enforcement

The first implementation added:

- `PythonUnittestDenyNetworkBoundary`;
- a Base-owned audit-hook launcher;
- exact command-shape validation for `network: DENIED` + `python -m unittest ...`;
- defensive secret stripping in the boundary environment;
- audit denials for `socket.*`, subprocess/process execution and ctypes dynamic-call events;
- fail-closed fallback for unsupported commands/policies.

On head `6f37f95063c152e5164c07f05268d7edbd66ef24`, Ubuntu passed eight contracts and failed only the ctypes probe because Linux `ctypes` import itself triggered `ctypes.dlopen` before the test body. The security behavior was correct; the probe was changed to assert import-time denial.

### Platform adversarial repair — Windows ctypes import

Ubuntu then passed all nine, but Windows still failed the ctypes probe. Windows can import `ctypes` without necessarily emitting the same `ctypes.dlopen` audit event used by Linux.

The boundary was strengthened rather than weakened: audit event `import` now rejects `ctypes` and `_ctypes` roots directly in addition to dynamic-call events. This removes the platform-specific native escape surface.

Final GREEN implementation head before evidence refresh: `3e44b2de8343243c00df7af829aadb42cec7953d`.

Dedicated run `31798668003`:

- Ubuntu 24.04: PASS, 9/9 contracts;
- Windows 2025: PASS, 9/9 contracts.

## Enforced contract

For the supported command shape only, ProjectTestExecutor replaces the project command with a Base-owned launcher using the current validated Python interpreter. Before loading project tests, the launcher installs an audit hook.

The audit hook denies:

- `socket.*` events, including socket creation and resolver/network use;
- `subprocess.*` / `subprocess.Popen`;
- `os.system`;
- process exec/spawn/posix_spawn audit events;
- `pty.spawn`;
- `ctypes` / `_ctypes` import;
- ctypes dynamic loading/symbol/call audit events.

The boundary environment defensively strips `OPENAI_API_KEY` and names containing common API-key/token/password/private-key/client-secret markers, then identifies itself as `PYTHON_AUDIT_DENY_NETWORK_V1`.

## Fail-closed unsupported surface

The boundary deliberately returns no execution plan for:

- non-Python executables;
- `python -c`;
- any module other than exact `python -m unittest`;
- empty unittest argument lists;
- `READ_ONLY_APPROVED`;
- unknown network policy.

ProjectTestExecutor therefore preserves `NETWORK_POLICY_UNENFORCED` for those cases.

## Bounded claim

This is a Python runtime enforcement boundary for a deliberately narrow test command. It is not claimed to provide a general native-process or OS-level sandbox. The initial A2 paid smoke may use it only when the approved Runtime Adapter test command fits the exact supported shape. Native build/runtime commands and broader networking policy still require another enforcement adapter and remain blocked.

## Non-claims

```yaml
live_openai_request: NOT_RUN
paid_api_cost: NOT_RUN
paid_smoke: NOT_RUN
general_os_network_sandbox: NOT_IMPLEMENTED
read_only_approved_network: NOT_IMPLEMENTED
native_test_command_network_boundary: NOT_IMPLEMENTED
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
```
