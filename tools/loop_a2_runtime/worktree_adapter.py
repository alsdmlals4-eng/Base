from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Mapping, Protocol, Sequence

from .protocol import ProtocolError, RunRequest, WorkerResult


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
_DEFAULT_OUTPUT_LIMIT = 1_000_000


class WorkspaceWorker(Protocol):
    def invoke(
        self,
        request: RunRequest,
        *,
        worktree_path: Path,
        repair_cycle: int,
    ) -> WorkerResult:
        ...


def _blocked_result(
    request: RunRequest,
    *,
    code: str,
    message: str,
    changed_paths: tuple[str, ...] = (),
) -> WorkerResult:
    return WorkerResult.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "role": "BUILDER",
            "status": "BLOCKED",
            "changed_paths": list(changed_paths),
            "summary": "isolated worktree execution blocked",
            "usage": {"turns": 0},
            "errors": [{"code": code, "message": message}],
        }
    )


def _safe_worker_environment() -> dict[str, str]:
    environment: dict[str, str] = {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
    }
    for key in _SAFE_INHERITED_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            environment[key] = value
    return environment


class SubprocessWorkspaceWorker:
    """Execute a worker process without shell expansion or inherited credentials."""

    def __init__(
        self,
        argv: Sequence[str],
        *,
        output_limit_bytes: int = _DEFAULT_OUTPUT_LIMIT,
    ) -> None:
        if not argv or any(not isinstance(item, str) or not item for item in argv):
            raise ValueError("argv must be a non-empty sequence of strings")
        if not Path(argv[0]).is_absolute():
            raise ValueError("worker executable must be an absolute path")
        if output_limit_bytes < 1024:
            raise ValueError("output_limit_bytes must be at least 1024")
        self.argv = tuple(argv)
        self.output_limit_bytes = output_limit_bytes

    def invoke(
        self,
        request: RunRequest,
        *,
        worktree_path: Path,
        repair_cycle: int,
    ) -> WorkerResult:
        payload = json.dumps(
            {
                "request": request.to_dict(),
                "repair_cycle": repair_cycle,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
        try:
            completed = subprocess.run(
                self.argv,
                cwd=worktree_path,
                input=payload,
                text=True,
                capture_output=True,
                env=_safe_worker_environment(),
                timeout=request.budgets.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return _blocked_result(
                request,
                code="WORKER_TIMEOUT",
                message="worker process exceeded the bounded timeout",
            )
        except OSError as exc:
            return _blocked_result(
                request,
                code="WORKER_EXECUTION_ERROR",
                message=f"worker process could not start: {type(exc).__name__}",
            )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        if (
            len(stdout.encode("utf-8", errors="replace")) > self.output_limit_bytes
            or len(stderr.encode("utf-8", errors="replace")) > self.output_limit_bytes
        ):
            return _blocked_result(
                request,
                code="WORKER_OUTPUT_LIMIT",
                message="worker output exceeded the bounded limit",
            )
        if completed.returncode != 0:
            return _blocked_result(
                request,
                code="WORKER_EXIT_NONZERO",
                message=f"worker process exited with code {completed.returncode}",
            )
        try:
            value = json.loads(stdout)
            return WorkerResult.from_dict(value)
        except (json.JSONDecodeError, ProtocolError, TypeError, ValueError):
            return _blocked_result(
                request,
                code="WORKER_PROTOCOL_INVALID",
                message="worker stdout was not a valid bounded WorkerResult",
            )


def _git(
    repo: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=check,
    )


def _nul_paths(value: str) -> tuple[str, ...]:
    return tuple(item for item in value.split("\0") if item)


class GitWorktreeBuilderAdapter:
    """Bind Builder claims to actual Git state in an external detached worktree."""

    def __init__(
        self,
        *,
        repo_root: Path,
        runtime_root: Path,
        worker: WorkspaceWorker,
    ) -> None:
        self.repo_root = repo_root.resolve(strict=True)
        if not (self.repo_root / ".git").exists():
            probe = _git(self.repo_root, "rev-parse", "--git-dir", check=False)
            if probe.returncode != 0:
                raise ValueError("repo_root must be a Git repository")
        self.runtime_root = runtime_root.resolve(strict=False)
        if self.runtime_root == self.repo_root or self.repo_root in self.runtime_root.parents:
            raise ValueError("runtime_root must be outside the project repository")
        self.worker = worker

    def workspace_path(self, request: RunRequest) -> Path:
        return self.runtime_root / request.project_id / request.run_id

    def _expected_sha_available(self, request: RunRequest) -> bool:
        completed = _git(
            self.repo_root,
            "cat-file",
            "-e",
            f"{request.expected_main_sha}^{{commit}}",
            check=False,
        )
        return completed.returncode == 0

    def _registered_worktrees(self) -> str:
        return _git(self.repo_root, "worktree", "list", "--porcelain").stdout

    def _ensure_workspace(
        self,
        request: RunRequest,
        *,
        repair_cycle: int,
    ) -> WorkerResult | None:
        workspace = self.workspace_path(request)
        if not self._expected_sha_available(request):
            return _blocked_result(
                request,
                code="EXPECTED_SHA_UNAVAILABLE",
                message="expected main SHA is not available in the source repository",
            )

        if workspace.exists():
            if repair_cycle == 0:
                return _blocked_result(
                    request,
                    code="WORKSPACE_COLLISION",
                    message="runtime workspace already exists before the initial Builder call",
                )
            head = _git(workspace, "rev-parse", "HEAD", check=False)
            if head.returncode != 0 or head.stdout.strip() != request.expected_main_sha:
                return _blocked_result(
                    request,
                    code="WORKSPACE_IDENTITY_MISMATCH",
                    message="existing runtime workspace does not match expected main SHA",
                )
            if str(workspace.resolve()) not in self._registered_worktrees():
                return _blocked_result(
                    request,
                    code="WORKSPACE_NOT_REGISTERED",
                    message="existing runtime workspace is not registered with Git",
                )
            return None

        workspace.parent.mkdir(parents=True, exist_ok=True)
        completed = _git(
            self.repo_root,
            "worktree",
            "add",
            "--detach",
            str(workspace),
            request.expected_main_sha,
            check=False,
        )
        if completed.returncode != 0:
            return _blocked_result(
                request,
                code="WORKTREE_CREATE_FAILED",
                message="Git could not create the isolated worktree",
            )
        return None

    def _actual_changed_paths(self, request: RunRequest) -> tuple[str, ...]:
        workspace = self.workspace_path(request)
        tracked = _git(
            workspace,
            "diff",
            "--name-only",
            "--no-renames",
            "-z",
            "HEAD",
            "--",
        ).stdout
        untracked = _git(
            workspace,
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
        ).stdout
        return tuple(sorted(set(_nul_paths(tracked)) | set(_nul_paths(untracked))))

    def _with_actual_paths(
        self,
        request: RunRequest,
        result: WorkerResult,
        actual_paths: tuple[str, ...],
    ) -> WorkerResult:
        if result.status == "COMPLETED":
            return WorkerResult.from_dict(
                {
                    "schema_version": result.schema_version,
                    "contract_role": result.contract_role,
                    "project_id": result.project_id,
                    "run_id": result.run_id,
                    "package_id": result.package_id,
                    "expected_main_sha": result.expected_main_sha,
                    "role": result.role,
                    "status": result.status,
                    "changed_paths": list(actual_paths),
                    "summary": result.summary,
                    "usage": dict(result.usage),
                    "errors": [],
                }
            )
        return WorkerResult.from_dict(
            {
                "schema_version": result.schema_version,
                "contract_role": result.contract_role,
                "project_id": result.project_id,
                "run_id": result.run_id,
                "package_id": result.package_id,
                "expected_main_sha": result.expected_main_sha,
                "role": result.role,
                "status": result.status,
                "changed_paths": list(actual_paths),
                "summary": result.summary,
                "usage": dict(result.usage),
                "errors": [
                    {"code": item.code, "message": item.message}
                    for item in result.errors
                ],
            }
        )

    def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult:
        blocked = self._ensure_workspace(request, repair_cycle=repair_cycle)
        if blocked is not None:
            return blocked
        workspace = self.workspace_path(request)
        result = self.worker.invoke(
            request,
            worktree_path=workspace,
            repair_cycle=repair_cycle,
        )
        actual_paths = self._actual_changed_paths(request)
        if result.status == "COMPLETED" and set(result.changed_paths) != set(actual_paths):
            return _blocked_result(
                request,
                code="DECLARED_DIFF_MISMATCH",
                message="worker changed-path claims do not match actual Git state",
                changed_paths=actual_paths,
            )
        return self._with_actual_paths(request, result, actual_paths)

    def close(self, request: RunRequest) -> None:
        workspace = self.workspace_path(request)
        if workspace.exists():
            _git(
                self.repo_root,
                "worktree",
                "remove",
                "--force",
                str(workspace),
                check=False,
            )
        _git(self.repo_root, "worktree", "prune", check=False)
        parent = workspace.parent
        try:
            parent.rmdir()
        except OSError:
            pass
