from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Mapping, Sequence

from .test_executor import NetworkExecutionPlan


_BOUNDARY_ID = "LINUX_UNSHARE_DENIED_V1"
_PROBE_CODE = (
    "import json,socket; "
    "print(json.dumps(sorted(name for _, name in socket.if_nameindex())))"
)


class LinuxUnshareDeniedNetworkBoundary:
    """Enforce Runtime Adapter ``network: DENIED`` with a Linux net namespace.

    The boundary intentionally supports only the closed policy that can be proved by
    this adapter. ``READ_ONLY_APPROVED`` and non-Linux hosts remain unsupported and
    therefore fail closed through ``ProjectTestExecutor``.

    The caller already owns environment sanitization. This class does not add parent
    environment variables or credentials; it forwards exactly the supplied mapping.
    """

    def __init__(
        self,
        *,
        unshare_executable: str | os.PathLike[str] = "unshare",
        python_executable: str | os.PathLike[str] = sys.executable,
        probe_timeout_seconds: int = 5,
    ) -> None:
        requested = str(unshare_executable)
        if not requested:
            raise ValueError("unshare_executable must be non-empty")
        python_value = str(python_executable)
        if not python_value or not Path(python_value).is_absolute():
            raise ValueError("python_executable must be an absolute path")
        if not 1 <= probe_timeout_seconds <= 10:
            raise ValueError("probe_timeout_seconds must be 1..10")
        self._requested_unshare = requested
        self._python_executable = python_value
        self._probe_timeout_seconds = probe_timeout_seconds
        self._resolved_unshare: str | None = None
        self._probe_passed: bool | None = None

    def _resolve_unshare(self) -> str | None:
        if self._resolved_unshare is not None:
            return self._resolved_unshare
        requested = self._requested_unshare
        candidate = Path(requested)
        if candidate.parent != Path("."):
            if not candidate.is_absolute() or not candidate.is_file():
                return None
            if not os.access(candidate, os.X_OK):
                return None
            resolved = str(candidate.resolve(strict=True))
        else:
            found = shutil.which(requested)
            if not found:
                return None
            resolved_path = Path(found)
            if not resolved_path.is_absolute() or not resolved_path.is_file():
                return None
            resolved = str(resolved_path.resolve(strict=True))
        self._resolved_unshare = resolved
        return resolved

    @staticmethod
    def _closed_environment(environment: Mapping[str, str]) -> dict[str, str] | None:
        closed: dict[str, str] = {}
        for key, value in environment.items():
            if not isinstance(key, str) or not key or not isinstance(value, str):
                return None
            closed[key] = value
        return closed

    def _probe(
        self,
        *,
        executable: str,
        cwd: Path,
        environment: Mapping[str, str],
    ) -> bool:
        if self._probe_passed is not None:
            return self._probe_passed
        command = [
            executable,
            "--user",
            "--map-root-user",
            "--net",
            "--",
            self._python_executable,
            "-c",
            _PROBE_CODE,
        ]
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=dict(environment),
                text=True,
                capture_output=True,
                timeout=self._probe_timeout_seconds,
                shell=False,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            self._probe_passed = False
            return False
        if completed.returncode != 0:
            self._probe_passed = False
            return False
        try:
            interfaces = json.loads(completed.stdout.strip())
        except (json.JSONDecodeError, AttributeError):
            self._probe_passed = False
            return False
        self._probe_passed = (
            isinstance(interfaces, list)
            and interfaces == ["lo"]
            and all(isinstance(item, str) for item in interfaces)
        )
        return self._probe_passed

    def prepare(
        self,
        *,
        policy: str,
        argv: Sequence[str],
        cwd: Path,
        environment: Mapping[str, str],
    ) -> NetworkExecutionPlan | None:
        if policy != "DENIED" or platform.system() != "Linux":
            return None
        if not argv or any(not isinstance(item, str) or not item for item in argv):
            return None
        try:
            closed_cwd = cwd.resolve(strict=True)
        except (OSError, RuntimeError):
            return None
        if not closed_cwd.is_dir():
            return None
        closed_environment = self._closed_environment(environment)
        if closed_environment is None:
            return None
        executable = self._resolve_unshare()
        if executable is None:
            return None
        if not self._probe(
            executable=executable,
            cwd=closed_cwd,
            environment=closed_environment,
        ):
            return None
        return NetworkExecutionPlan(
            argv=(
                executable,
                "--user",
                "--map-root-user",
                "--net",
                "--",
                *tuple(argv),
            ),
            environment=closed_environment,
            boundary_id=_BOUNDARY_ID,
        )
