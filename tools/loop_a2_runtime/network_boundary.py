from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
from typing import Mapping, Sequence

from .test_executor import NetworkExecutionPlan


_UNSHARE_BOUNDARY_ID = "LINUX_UNSHARE_DENIED_V1"
_DOCKER_BOUNDARY_ID = "DOCKER_NONE_DENIED_V1"
_IMAGE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PROBE_CODE = (
    "import json,socket; "
    "print(json.dumps(sorted(name for _, name in socket.if_nameindex())))"
)


def _closed_environment(environment: Mapping[str, str]) -> dict[str, str] | None:
    closed: dict[str, str] = {}
    for key, value in environment.items():
        if (
            not isinstance(key, str)
            or _ENV_NAME.fullmatch(key) is None
            or not isinstance(value, str)
            or "\x00" in value
        ):
            return None
        closed[key] = value
    return closed


def _resolve_executable(requested: str) -> str | None:
    candidate = Path(requested)
    if candidate.parent != Path("."):
        if not candidate.is_absolute() or not candidate.is_file():
            return None
        if not os.access(candidate, os.X_OK):
            return None
        return str(candidate.resolve(strict=True))
    found = shutil.which(requested)
    if not found:
        return None
    resolved_path = Path(found)
    if not resolved_path.is_absolute() or not resolved_path.is_file():
        return None
    return str(resolved_path.resolve(strict=True))


class LinuxUnshareDeniedNetworkBoundary:
    """Optional Linux ``unshare`` implementation for ``network: DENIED``.

    Support is capability-probed because many hosted runners disable unprivileged
    user/network namespaces. Unsupported hosts fail closed through ProjectTestExecutor.
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
        if self._resolved_unshare is None:
            self._resolved_unshare = _resolve_executable(self._requested_unshare)
        return self._resolved_unshare

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
        closed_environment = _closed_environment(environment)
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
            boundary_id=_UNSHARE_BOUNDARY_ID,
        )


class DockerNoneDeniedNetworkBoundary:
    """Run DENIED project tests in a preloaded immutable Docker image.

    The boundary never pulls or builds an image. Callers must preload an image and
    pass its exact local ``sha256:<64 hex>`` image ID. The test working directory is
    the only host path mounted into the container and is mounted read-only. Docker's
    ``none`` network driver supplies only loopback; all Linux capabilities are dropped.
    """

    def __init__(
        self,
        *,
        image_id: str,
        docker_executable: str | os.PathLike[str] = "docker",
        inspect_timeout_seconds: int = 5,
    ) -> None:
        if not isinstance(image_id, str) or _IMAGE_ID.fullmatch(image_id) is None:
            raise ValueError("image_id must be an immutable sha256 Docker image ID")
        requested = str(docker_executable)
        if not requested:
            raise ValueError("docker_executable must be non-empty")
        if not 1 <= inspect_timeout_seconds <= 10:
            raise ValueError("inspect_timeout_seconds must be 1..10")
        self.image_id = image_id
        self._requested_docker = requested
        self._inspect_timeout_seconds = inspect_timeout_seconds
        self._resolved_docker: str | None = None
        self._image_verified: bool | None = None

    def _resolve_docker(self) -> str | None:
        if self._resolved_docker is None:
            self._resolved_docker = _resolve_executable(self._requested_docker)
        return self._resolved_docker

    def _verify_local_image(
        self,
        *,
        executable: str,
        cwd: Path,
        environment: Mapping[str, str],
    ) -> bool:
        if self._image_verified is not None:
            return self._image_verified
        try:
            completed = subprocess.run(
                [
                    executable,
                    "image",
                    "inspect",
                    "--format",
                    "{{.Id}}",
                    self.image_id,
                ],
                cwd=cwd,
                env=dict(environment),
                text=True,
                capture_output=True,
                timeout=self._inspect_timeout_seconds,
                shell=False,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            self._image_verified = False
            return False
        self._image_verified = (
            completed.returncode == 0
            and completed.stdout.strip() == self.image_id
        )
        return self._image_verified

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
        cwd_text = str(closed_cwd)
        if any(character in cwd_text for character in (",", "\n", "\r", "\x00")):
            return None
        closed_environment = _closed_environment(environment)
        if closed_environment is None:
            return None
        executable = self._resolve_docker()
        if executable is None:
            return None
        if not self._verify_local_image(
            executable=executable,
            cwd=closed_cwd,
            environment=closed_environment,
        ):
            return None

        docker_env: list[str] = []
        for key in sorted(closed_environment):
            docker_env.extend(("--env", key))
        mount = f"type=bind,src={cwd_text},dst={cwd_text},readonly"
        return NetworkExecutionPlan(
            argv=(
                executable,
                "run",
                "--rm",
                "--pull",
                "never",
                "--network",
                "none",
                "--read-only",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges",
                "--pids-limit",
                "256",
                "--tmpfs",
                "/tmp:rw,nosuid,nodev,size=64m",
                "--mount",
                mount,
                "--workdir",
                cwd_text,
                *docker_env,
                self.image_id,
                *tuple(argv),
            ),
            environment=closed_environment,
            boundary_id=_DOCKER_BOUNDARY_ID,
        )
