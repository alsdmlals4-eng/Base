# Loop A2 Python DENIED Network Evidence — 2026-08-14

## Scope

Issue #368. Add a narrow language-runtime network/process escape boundary for Runtime Adapter commands shaped exactly as `python -m unittest ...` with `network: DENIED`.

This is not a general OS sandbox. Any unsupported executable, Python `-c`, non-unittest module, `READ_ONLY_APPROVED`, or unknown policy remains blocked by the existing `ProjectTestExecutor` fail-closed behavior.

## RED

Test/workflow-only start. Expected failure: `tools.loop_a2_runtime.python_denied_network` does not exist. Tests also require Ubuntu/Windows behavior for normal unittest execution plus socket, subprocess/os.system, ctypes, secret-inheritance, and unsupported-command probes.

No OpenAI API request, model selection, project product write, A3, Scheduler, or network permission is introduced by this RED.
