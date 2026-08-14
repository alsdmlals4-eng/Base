#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest


_DENIED_EXACT_EVENTS = {
    "subprocess.Popen",
    "os.system",
    "os.exec",
    "os.posix_spawn",
    "os.spawn",
    "pty.spawn",
    "ctypes.dlopen",
    "ctypes.dlsym",
    "ctypes.call_function",
}
_DENIED_PREFIXES = (
    "socket.",
    "subprocess.",
)


def _audit(event: str, args: tuple[object, ...]) -> None:
    del args
    if event in _DENIED_EXACT_EVENTS or any(
        event.startswith(prefix) for prefix in _DENIED_PREFIXES
    ):
        raise PermissionError(
            f"Loop A2 DENIED network boundary blocked audit event: {event}"
        )


def main() -> int:
    if os.environ.get("LOOP_A2_NETWORK_BOUNDARY") != "PYTHON_AUDIT_DENY_NETWORK_V1":
        raise SystemExit("Loop A2 network boundary marker is missing")

    sys.addaudithook(_audit)
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
    sys.argv = ["python -m unittest", *sys.argv[1:]]
    program = unittest.main(module=None, exit=False)
    return 0 if program.result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
