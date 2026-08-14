from __future__ import annotations

import os
from pathlib import Path
import re
import sys
from typing import Mapping, Sequence

from .test_executor import NetworkExecutionPlan


_PYTHON_EXE = re.compile(r"^python(?:\d+(?:\.\d+)*)?(?:\.exe)?$", re.IGNORECASE)
_SENSITIVE_ENV_MARKERS = (
    "API_KEY",
    "ACCESS_TOKEN",
    "AUTH_TOKEN",
    "PASSWORD",
    "PRIVATE_KEY",
    "CLIENT_SECRET",
)


class PythonUnittestDenyNetworkBoundary:
    """Language-runtime boundary for DENIED `python -m unittest` commands only.

    This is intentionally not a general network sandbox. Unsupported commands and
    policies return ``None`` so ProjectTestExecutor preserves its fail-closed
    NETWORK_POLICY_UNENFORCED behavior.
    """

    boundary_id = "PYTHON_AUDIT_DENY_NETWORK_V1"

    def __init__(self) -> None:
        self.launcher_path = Path(__file__).with_name(
            "python_denied_network_launcher.py"
        ).resolve(strict=True)

    @staticmethod
    def _is_supported_python(executable: str) -> bool:
        if not isinstance(executable, str) or not executable:
            return False
        name = Path(executable.replace("\\", "/")).name
        return bool(_PYTHON_EXE.fullmatch(name))

    @staticmethod
    def _sanitized_environment(environment: Mapping[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in environment.items():
            upper = key.upper()
            if upper == "OPENAI_API_KEY" or any(
                marker in upper for marker in _SENSITIVE_ENV_MARKERS
            ):
                continue
            result[str(key)] = str(value)
        result["LOOP_A2_NETWORK_BOUNDARY"] = (
            PythonUnittestDenyNetworkBoundary.boundary_id
        )
        result["PYTHONDONTWRITEBYTECODE"] = "1"
        result["PYTHONIOENCODING"] = "utf-8"
        result["PYTHONUNBUFFERED"] = "1"
        return result

    def prepare(
        self,
        *,
        policy: str,
        argv: Sequence[str],
        cwd: Path,
        environment: Mapping[str, str],
    ) -> NetworkExecutionPlan | None:
        del cwd  # ProjectTestExecutor owns and validates the working directory.
        if policy != "DENIED":
            return None
        if len(argv) < 4 or any(not isinstance(item, str) for item in argv):
            return None
        if not self._is_supported_python(argv[0]):
            return None
        if tuple(argv[1:3]) != ("-m", "unittest"):
            return None

        test_args = tuple(argv[3:])
        if not test_args or any(not item for item in test_args):
            return None
        # Do not allow unittest to be replaced with arbitrary interpreter flags or
        # inline code after the boundary decision. Test names/options are handled
        # by unittest itself inside the Base-owned launcher.
        if any(item in {"-c", "--command"} for item in test_args):
            return None

        return NetworkExecutionPlan(
            argv=(sys.executable, str(self.launcher_path), *test_args),
            environment=self._sanitized_environment(environment),
            boundary_id=self.boundary_id,
        )
