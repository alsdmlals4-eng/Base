from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import time
from typing import Mapping, Protocol, Sequence

from tools.loop_contracts.schema_validation import validate_schema

from .evidence import canonical_receipt


_SAFE_INHERITED_ENV_KEYS = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "LANG",
    "LC_ALL",
)
_EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()


@dataclass(frozen=True)
class NetworkExecutionPlan:
    argv: tuple[str, ...]
    environment: Mapping[str, str]
    boundary_id: str


class NetworkBoundary(Protocol):
    def prepare(
        self,
        *,
        policy: str,
        argv: Sequence[str],
        cwd: Path,
        environment: Mapping[str, str],
    ) -> NetworkExecutionPlan | None:
        ...


class UnavailableNetworkBoundary:
    """Fail closed until a reviewed network-enforcement adapter is supplied."""

    def prepare(
        self,
        *,
        policy: str,
        argv: Sequence[str],
        cwd: Path,
        environment: Mapping[str, str],
    ) -> NetworkExecutionPlan | None:
        return None


@dataclass(frozen=True)
class CommandEvidence:
    command_id: str
    status: str
    exit_code: int | None
    error_code: str | None
    stdout_sha256: str
    stderr_sha256: str
    stdout_bytes: int
    stderr_bytes: int
    network_policy: str
    network_boundary_id: str
    duration_ms: int

    def to_dict(self) -> dict[str, object]:
        return {
            "command_id": self.command_id,
            "status": self.status,
            "exit_code": self.exit_code,
            "error_code": self.error_code,
            "stdout_sha256": self.stdout_sha256,
            "stderr_sha256": self.stderr_sha256,
            "stdout_bytes": self.stdout_bytes,
            "stderr_bytes": self.stderr_bytes,
            "network_policy": self.network_policy,
            "network_boundary_id": self.network_boundary_id,
            "duration_ms": self.duration_ms,
        }


@dataclass(frozen=True)
class TestSuiteResult:
    project_id: str
    expected_main_sha: str
    status: str
    commands: tuple[CommandEvidence, ...]

    def to_dict(self) -> dict[str, object]:
        return canonical_receipt(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_PROJECT_TEST_EVIDENCE",
                "project_id": self.project_id,
                "expected_main_sha": self.expected_main_sha,
                "status": self.status,
                "commands": [item.to_dict() for item in self.commands],
            }
        )


def _safe_environment() -> dict[str, str]:
    environment: dict[str, str] = {
        "CI": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
    }
    for key in _SAFE_INHERITED_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            environment[key] = value
    return environment


def _precheck_evidence(code: str) -> CommandEvidence:
    return CommandEvidence(
        command_id="PRECHECK",
        status="BLOCKED",
        exit_code=None,
        error_code=code,
        stdout_sha256=_EMPTY_SHA256,
        stderr_sha256=_EMPTY_SHA256,
        stdout_bytes=0,
        stderr_bytes=0,
        network_policy="NOT_RUN",
        network_boundary_id="NOT_RUN",
        duration_ms=0,
    )


def _safe_relative_text(value: str) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized):
        return None
    parts = PurePosixPath(normalized).parts
    if ".." in parts:
        return None
    return normalized


def _resolve_inside(root: Path, relative: str) -> Path | None:
    normalized = _safe_relative_text(relative)
    if normalized is None:
        return None
    candidate = (root / normalized).resolve(strict=False)
    resolved_root = root.resolve(strict=True)
    if candidate != resolved_root and resolved_root not in candidate.parents:
        return None
    return candidate


def _git_bytes(repo: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    return completed.stdout


def _untracked_paths(repo: Path) -> tuple[str, ...]:
    value = _git_bytes(repo, "ls-files", "--others", "-z")
    return tuple(sorted(item.decode("utf-8") for item in value.split(b"\0") if item))


def _workspace_state_digest(repo: Path) -> str:
    digest = hashlib.sha256()
    digest.update(b"TRACKED\0")
    digest.update(_git_bytes(repo, "diff", "--binary", "--no-ext-diff", "HEAD", "--"))
    digest.update(b"\0UNTRACKED\0")
    for relative in _untracked_paths(repo):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        path = repo / relative
        if path.is_symlink():
            digest.update(b"SYMLINK\0")
            digest.update(os.readlink(path).encode("utf-8", errors="replace"))
        elif path.is_file():
            digest.update(b"FILE\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        else:
            digest.update(b"OTHER\0")
        digest.update(b"\0")
    return digest.hexdigest()


def _worktree_head(repo: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


class ProjectTestExecutor:
    def __init__(
        self,
        *,
        network_boundary: NetworkBoundary | None = None,
        output_limit_bytes: int = 1_000_000,
    ) -> None:
        if output_limit_bytes < 1024:
            raise ValueError("output_limit_bytes must be at least 1024")
        self.network_boundary = network_boundary or UnavailableNetworkBoundary()
        self.output_limit_bytes = output_limit_bytes

    def _blocked(
        self,
        *,
        project_id: str,
        expected_main_sha: str,
        code: str,
    ) -> TestSuiteResult:
        return TestSuiteResult(
            project_id=project_id,
            expected_main_sha=expected_main_sha,
            status="BLOCKED",
            commands=(_precheck_evidence(code),),
        )

    def run_all(
        self,
        *,
        adapter_path: Path,
        worktree_path: Path,
        expected_project_id: str,
        expected_main_sha: str,
    ) -> TestSuiteResult:
        worktree = worktree_path.resolve(strict=True)
        if _worktree_head(worktree) != expected_main_sha:
            return self._blocked(
                project_id=expected_project_id,
                expected_main_sha=expected_main_sha,
                code="TEST_WORKTREE_SHA_MISMATCH",
            )
        try:
            value = json.loads(adapter_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self._blocked(
                project_id=expected_project_id,
                expected_main_sha=expected_main_sha,
                code="TEST_ADAPTER_INVALID",
            )
        if not isinstance(value, dict):
            return self._blocked(
                project_id=expected_project_id,
                expected_main_sha=expected_main_sha,
                code="TEST_ADAPTER_INVALID",
            )
        if value.get("project_id") != expected_project_id:
            return self._blocked(
                project_id=expected_project_id,
                expected_main_sha=expected_main_sha,
                code="TEST_ADAPTER_PROJECT_MISMATCH",
            )

        commands = value.get("test_commands")
        if isinstance(commands, list):
            for command in commands:
                if isinstance(command, dict):
                    working_directory = command.get("working_directory")
                    if not isinstance(working_directory, str) or _safe_relative_text(working_directory) is None:
                        evidence = CommandEvidence(
                            command_id=str(command.get("command_id", "UNKNOWN")),
                            status="BLOCKED",
                            exit_code=None,
                            error_code="TEST_WORKING_DIRECTORY_UNSAFE",
                            stdout_sha256=_EMPTY_SHA256,
                            stderr_sha256=_EMPTY_SHA256,
                            stdout_bytes=0,
                            stderr_bytes=0,
                            network_policy=str(command.get("network", "UNKNOWN")),
                            network_boundary_id="NOT_RUN",
                            duration_ms=0,
                        )
                        return TestSuiteResult(
                            project_id=expected_project_id,
                            expected_main_sha=expected_main_sha,
                            status="BLOCKED",
                            commands=(evidence,),
                        )

        if validate_schema("loop-runtime-adapter-v1.schema.json", value, str(adapter_path)):
            return self._blocked(
                project_id=expected_project_id,
                expected_main_sha=expected_main_sha,
                code="TEST_ADAPTER_INVALID",
            )

        results: list[CommandEvidence] = []
        for command in value["test_commands"]:
            evidence = self._run_command(worktree, command)
            results.append(evidence)
            if evidence.status != "PASS":
                suite_status = "FAIL" if evidence.status == "FAIL" else "BLOCKED"
                return TestSuiteResult(
                    project_id=expected_project_id,
                    expected_main_sha=expected_main_sha,
                    status=suite_status,
                    commands=tuple(results),
                )
        return TestSuiteResult(
            project_id=expected_project_id,
            expected_main_sha=expected_main_sha,
            status="PASS",
            commands=tuple(results),
        )

    def _run_command(self, worktree: Path, command: Mapping[str, object]) -> CommandEvidence:
        command_id = str(command["command_id"])
        network_policy = str(command["network"])
        cwd = _resolve_inside(worktree, str(command["working_directory"]))
        if cwd is None or not cwd.is_dir():
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=None,
                error_code="TEST_WORKING_DIRECTORY_UNSAFE",
                stdout_sha256=_EMPTY_SHA256,
                stderr_sha256=_EMPTY_SHA256,
                stdout_bytes=0,
                stderr_bytes=0,
                network_policy=network_policy,
                network_boundary_id="NOT_RUN",
                duration_ms=0,
            )

        argv = tuple(str(item) for item in command["argv"])
        executable = argv[0].replace("\\", "/")
        if ".." in PurePosixPath(executable).parts:
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=None,
                error_code="TEST_EXECUTABLE_UNSAFE",
                stdout_sha256=_EMPTY_SHA256,
                stderr_sha256=_EMPTY_SHA256,
                stdout_bytes=0,
                stderr_bytes=0,
                network_policy=network_policy,
                network_boundary_id="NOT_RUN",
                duration_ms=0,
            )

        environment = _safe_environment()
        plan = self.network_boundary.prepare(
            policy=network_policy,
            argv=argv,
            cwd=cwd,
            environment=environment,
        )
        if plan is None:
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=None,
                error_code="NETWORK_POLICY_UNENFORCED",
                stdout_sha256=_EMPTY_SHA256,
                stderr_sha256=_EMPTY_SHA256,
                stdout_bytes=0,
                stderr_bytes=0,
                network_policy=network_policy,
                network_boundary_id="UNAVAILABLE",
                duration_ms=0,
            )

        before_digest = _workspace_state_digest(worktree)
        started = time.monotonic()
        try:
            completed = subprocess.run(
                plan.argv,
                cwd=cwd,
                capture_output=True,
                env=dict(plan.environment),
                timeout=int(command["timeout_seconds"]),
                check=False,
            )
            duration_ms = int((time.monotonic() - started) * 1000)
            stdout = completed.stdout or b""
            stderr = completed.stderr or b""
        except subprocess.TimeoutExpired as exc:
            duration_ms = int((time.monotonic() - started) * 1000)
            stdout = exc.stdout or b""
            stderr = exc.stderr or b""
            return CommandEvidence(
                command_id=command_id,
                status="TIMEOUT",
                exit_code=None,
                error_code="TEST_TIMEOUT",
                stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                stdout_bytes=len(stdout),
                stderr_bytes=len(stderr),
                network_policy=network_policy,
                network_boundary_id=plan.boundary_id,
                duration_ms=duration_ms,
            )
        except OSError:
            duration_ms = int((time.monotonic() - started) * 1000)
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=None,
                error_code="TEST_EXECUTION_ERROR",
                stdout_sha256=_EMPTY_SHA256,
                stderr_sha256=_EMPTY_SHA256,
                stdout_bytes=0,
                stderr_bytes=0,
                network_policy=network_policy,
                network_boundary_id=plan.boundary_id,
                duration_ms=duration_ms,
            )

        after_digest = _workspace_state_digest(worktree)
        if before_digest != after_digest:
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=completed.returncode,
                error_code="TEST_MUTATED_WORKSPACE",
                stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                stdout_bytes=len(stdout),
                stderr_bytes=len(stderr),
                network_policy=network_policy,
                network_boundary_id=plan.boundary_id,
                duration_ms=duration_ms,
            )
        if len(stdout) > self.output_limit_bytes or len(stderr) > self.output_limit_bytes:
            return CommandEvidence(
                command_id=command_id,
                status="BLOCKED",
                exit_code=completed.returncode,
                error_code="TEST_OUTPUT_LIMIT",
                stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                stdout_bytes=len(stdout),
                stderr_bytes=len(stderr),
                network_policy=network_policy,
                network_boundary_id=plan.boundary_id,
                duration_ms=duration_ms,
            )
        if completed.returncode != 0:
            status = "FAIL"
            error_code = "TEST_EXIT_NONZERO"
        else:
            status = "PASS"
            error_code = None
        return CommandEvidence(
            command_id=command_id,
            status=status,
            exit_code=completed.returncode,
            error_code=error_code,
            stdout_sha256=hashlib.sha256(stdout).hexdigest(),
            stderr_sha256=hashlib.sha256(stderr).hexdigest(),
            stdout_bytes=len(stdout),
            stderr_bytes=len(stderr),
            network_policy=network_policy,
            network_boundary_id=plan.boundary_id,
            duration_ms=duration_ms,
        )
