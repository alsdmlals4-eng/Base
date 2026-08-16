from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
from typing import Callable, Mapping

from .job import LocalA2Job


REVIEWED_TEST_IMAGE_REF = "python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65"
_IMAGE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_CHILD_ENV = (
    "PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "TMPDIR",
    "LANG", "LC_ALL", "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "CODEX_HOME",
)
_PLATFORM_ALIASES = {
    "amd64": "amd64",
    "x86_64": "amd64",
    "arm64": "arm64",
    "aarch64": "arm64",
}


class LocalRuntimeError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


def _child_environment() -> dict[str, str]:
    result: dict[str, str] = {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
    }
    for key in _CHILD_ENV:
        value = os.environ.get(key)
        if value:
            result[key] = value
    return result


Runner = Callable[..., subprocess.CompletedProcess[str]]


class LocalA2Runtime:
    def __init__(
        self,
        *,
        store: object,
        runner: Runner = subprocess.run,
        python_executable: str,
        docker_executable: str = "docker",
        base_repository: str = "alsdmlals4-eng/Base",
        output_limit_bytes: int = 1_000_000,
    ) -> None:
        if not python_executable or not docker_executable:
            raise ValueError("python_executable and docker_executable are required")
        if output_limit_bytes < 1024:
            raise ValueError("output_limit_bytes must be at least 1024")
        self.store = store
        self.runner = runner
        self.python_executable = python_executable
        self.docker_executable = docker_executable
        self.base_repository = base_repository
        self.output_limit_bytes = output_limit_bytes
        self._preflight_image_id: str | None = None

    def _run(self, argv: tuple[str, ...], *, timeout: int) -> subprocess.CompletedProcess[str]:
        try:
            return self.runner(
                list(argv),
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                shell=False,
                env=_child_environment(),
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise LocalRuntimeError("LOCAL_PROCESS_EXECUTION_FAILED", "local bounded process did not complete") from exc

    def _validated_image_id(self, stdout: str) -> str:
        if len(stdout.encode("utf-8", errors="replace")) > 256:
            raise LocalRuntimeError("DOCKER_IMAGE_ID_INVALID", "Docker image identity output is invalid")
        image_id = stdout.strip()
        if _IMAGE_ID.fullmatch(image_id) is None:
            raise LocalRuntimeError("DOCKER_IMAGE_ID_INVALID", "Docker did not return an immutable image ID")
        return image_id

    def _inspect_reviewed_image(self, *, platform: str | None = None) -> str | None:
        argv: tuple[str, ...]
        if platform is None:
            argv = (
                self.docker_executable,
                "image",
                "inspect",
                "--format",
                "{{.Id}}",
                REVIEWED_TEST_IMAGE_REF,
            )
        else:
            argv = (
                self.docker_executable,
                "image",
                "inspect",
                "--platform",
                platform,
                "--format",
                "{{.Id}}",
                REVIEWED_TEST_IMAGE_REF,
            )
        completed = self._run(argv, timeout=10)
        if completed.returncode != 0:
            return None
        return self._validated_image_id(completed.stdout or "")

    def _docker_server_platform(self) -> str:
        completed = self._run(
            (
                self.docker_executable,
                "version",
                "--format",
                "{{.Server.Os}}/{{.Server.Arch}}",
            ),
            timeout=10,
        )
        if completed.returncode != 0:
            raise LocalRuntimeError("DOCKER_PLATFORM_INVALID", "Docker server platform could not be determined")
        stdout = completed.stdout or ""
        if len(stdout.encode("utf-8", errors="replace")) > 128:
            raise LocalRuntimeError("DOCKER_PLATFORM_INVALID", "Docker server platform output is invalid")
        raw = stdout.strip().casefold()
        if raw.count("/") != 1:
            raise LocalRuntimeError("DOCKER_PLATFORM_INVALID", "Docker server platform output is invalid")
        os_name, architecture = raw.split("/", 1)
        normalized_arch = _PLATFORM_ALIASES.get(architecture)
        if os_name != "linux" or normalized_arch is None:
            raise LocalRuntimeError("DOCKER_PLATFORM_UNSUPPORTED", "reviewed project-test image requires a supported Linux container platform")
        return f"linux/{normalized_arch}"

    def _image_id(self) -> str:
        direct = self._inspect_reviewed_image()
        if direct is not None:
            return direct
        platform = self._docker_server_platform()
        platform_image = self._inspect_reviewed_image(platform=platform)
        if platform_image is None:
            raise LocalRuntimeError(
                "DOCKER_IMAGE_NOT_PRELOADED",
                "reviewed digest-pinned test image is not locally available for the Docker server platform",
            )
        return platform_image

    def _execution_image_id(self) -> str:
        image_id = self._preflight_image_id
        if image_id is None:
            return self._image_id()
        completed = self._run(
            (
                self.docker_executable,
                "image",
                "inspect",
                "--format",
                "{{.Id}}",
                image_id,
            ),
            timeout=10,
        )
        if completed.returncode != 0:
            raise LocalRuntimeError(
                "DOCKER_IMAGE_NOT_PRELOADED",
                "preflight-verified immutable test image is no longer locally available",
            )
        verified = self._validated_image_id(completed.stdout or "")
        if verified != image_id:
            raise LocalRuntimeError("DOCKER_IMAGE_ID_INVALID", "preflight-verified Docker image identity changed")
        return verified

    def preflight(self) -> dict[str, str]:
        self._preflight_image_id = self._image_id()
        return {"status": "READY", "code": "DOCKER_REVIEWED_IMAGE_READY"}

    def _capsule(self, project_root: Path, job: LocalA2Job) -> tuple[str, str]:
        current = project_root
        for part in job.capsule.split("/"):
            current = current / part
            try:
                if current.is_symlink():
                    raise LocalRuntimeError(
                        "CAPSULE_UNAVAILABLE",
                        "Capsule path must not traverse symlinks",
                    )
            except OSError as exc:
                raise LocalRuntimeError("CAPSULE_UNAVAILABLE", "exact authority Capsule is unavailable") from exc
        path = current
        try:
            resolved_root = project_root.resolve(strict=True)
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise LocalRuntimeError("CAPSULE_UNAVAILABLE", "exact authority Capsule is unavailable") from exc
        if resolved == resolved_root or resolved_root not in resolved.parents or not resolved.is_file():
            raise LocalRuntimeError("CAPSULE_UNAVAILABLE", "Capsule path is not a regular file inside authority root")
        try:
            value = json.loads(resolved.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise LocalRuntimeError("CAPSULE_INVALID", "Capsule JSON could not be read") from exc
        if not isinstance(value, dict):
            raise LocalRuntimeError("CAPSULE_INVALID", "Capsule must be an object")
        source_sha = value.get("source_main_sha")
        project_id = value.get("project_id")
        if not isinstance(source_sha, str) or _SHA.fullmatch(source_sha) is None:
            raise LocalRuntimeError("CAPSULE_SOURCE_SHA_INVALID", "Capsule source_main_sha is invalid")
        if not isinstance(project_id, str) or not project_id:
            raise LocalRuntimeError("CAPSULE_PROJECT_INVALID", "Capsule project_id is invalid")
        return project_id, source_sha

    def _validate_receipt(
        self,
        value: object,
        *,
        job: LocalA2Job,
        project_id: str,
        source_sha: str,
    ) -> dict[str, object]:
        if not isinstance(value, dict):
            raise LocalRuntimeError("A2_RECEIPT_INVALID", "A2 output is not an object")
        required = {
            "contract_role": "LOOP_A2_RUN_RECEIPT",
            "project_id": project_id,
            "run_id": job.run_id,
            "expected_main_sha": source_sha,
            "state": "WAITING_INTEGRATION",
            "provider_mode": "REAL",
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }
        if any(value.get(key) != expected for key, expected in required.items()):
            raise LocalRuntimeError("A2_RECEIPT_INVALID", "A2 receipt identity or policy state differs")
        digest = value.get("receipt_digest")
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            raise LocalRuntimeError("A2_RECEIPT_INVALID", "A2 receipt digest is invalid")
        package_id = value.get("package_id")
        if not isinstance(package_id, str) or not package_id:
            raise LocalRuntimeError("A2_RECEIPT_INVALID", "A2 package identity is invalid")
        return dict(value)

    def execute(self, job: LocalA2Job) -> dict[str, object]:
        with self.store.exact_worktree(self.base_repository, job.base_runtime_sha, "base") as base_root:
            with self.store.exact_worktree(job.target_repository, job.authority_sha, "authority") as project_root:
                project_id, source_sha = self._capsule(Path(project_root), job)
                image_id = self._execution_image_id()
                runtime_root = Path(self.store.runtime_root)
                runtime_root.mkdir(parents=True, exist_ok=True)
                loop_cli = Path(base_root) / "tools" / "loop_a2.py"
                if not loop_cli.is_file():
                    raise LocalRuntimeError("BASE_RUNTIME_INVALID", "exact Base runtime does not contain tools/loop_a2.py")
                argv = (
                    self.python_executable,
                    str(loop_cli),
                    "run",
                    "--project-root", str(project_root),
                    "--runtime-root", str(runtime_root),
                    "--capsule", job.capsule,
                    "--run-id", job.run_id,
                    "--observed-main-sha", source_sha,
                    "--provider", "real",
                    "--denied-network-docker-image-id", image_id,
                )
                completed = self._run(argv, timeout=900)
                stdout = completed.stdout or ""
                stderr = completed.stderr or ""
                if (
                    len(stdout.encode("utf-8", errors="replace")) > self.output_limit_bytes
                    or len(stderr.encode("utf-8", errors="replace")) > self.output_limit_bytes
                ):
                    raise LocalRuntimeError("A2_OUTPUT_LIMIT", "REAL A2 output exceeded the bounded limit")
                if completed.returncode != 0:
                    raise LocalRuntimeError("A2_EXECUTION_BLOCKED", "REAL A2 process did not reach an eligible terminal state")
                try:
                    value = json.loads(stdout)
                except json.JSONDecodeError as exc:
                    raise LocalRuntimeError("A2_RECEIPT_INVALID", "REAL A2 stdout was not one JSON receipt") from exc
                return self._validate_receipt(
                    value,
                    job=job,
                    project_id=project_id,
                    source_sha=source_sha,
                )
