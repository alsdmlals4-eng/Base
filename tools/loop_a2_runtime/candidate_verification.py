from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import tempfile
from typing import Any

from .authority_snapshot import AuthoritySnapshot, AuthoritySnapshotError
from .evidence import canonical_receipt
from .integration import compute_worktree_diff_sha256
from .protocol import RunRequest, WorkerResult
from .test_executor import CommandEvidence, ProjectTestExecutor, TestSuiteResult
from .workspace_registry import WorkspaceOwnershipError, WorkspaceOwnershipRegistry


_EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()


class CandidateVerificationError(RuntimeError):
    pass


class VerificationEvidenceMailbox:
    """In-memory, identity- and candidate-diff-bound PASS receipts for Critic."""

    def __init__(self) -> None:
        self._receipts: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        self._workspaces: dict[tuple[str, str, str, str], Path] = {}

    @staticmethod
    def _key(request: RunRequest) -> tuple[str, str, str, str]:
        return (
            request.project_id,
            request.run_id,
            request.package_id,
            request.expected_main_sha,
        )

    def publish_pass(
        self,
        request: RunRequest,
        result: TestSuiteResult,
        *,
        authority_snapshot_sha256: str,
        candidate_diff_sha256: str,
        workspace_path: Path | None = None,
    ) -> dict[str, Any]:
        if result.status != "PASS":
            raise CandidateVerificationError("candidate test PASS evidence is required")
        if (
            result.project_id != request.project_id
            or result.expected_main_sha != request.expected_main_sha
        ):
            raise CandidateVerificationError("candidate test PASS identity differs from request")
        if (
            not isinstance(candidate_diff_sha256, str)
            or len(candidate_diff_sha256) != 64
            or any(character not in "0123456789abcdef" for character in candidate_diff_sha256)
        ):
            raise CandidateVerificationError("candidate Diff SHA-256 is invalid")
        payload = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_CANDIDATE_TEST_EVIDENCE",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "authority_snapshot_sha256": authority_snapshot_sha256,
            "candidate_diff_sha256": candidate_diff_sha256,
            "status": "PASS",
            "test_suite": result.to_dict(),
        }
        receipt = canonical_receipt(payload)
        key = self._key(request)
        self._receipts[key] = receipt
        if workspace_path is not None:
            self._workspaces[key] = Path(workspace_path).resolve(strict=False)
        else:
            self._workspaces.pop(key, None)
        return dict(receipt)

    def require_pass(self, request: RunRequest) -> dict[str, Any]:
        key = self._key(request)
        receipt = self._receipts.get(key)
        if receipt is None or receipt.get("status") != "PASS":
            raise CandidateVerificationError(
                "candidate test PASS evidence is unavailable for this request"
            )
        workspace = self._workspaces.get(key)
        if workspace is not None:
            if not workspace.is_dir():
                raise CandidateVerificationError(
                    "candidate worktree disappeared after project-test PASS"
                )
            try:
                current_diff_sha256 = compute_worktree_diff_sha256(workspace)
            except (OSError, subprocess.SubprocessError, ValueError) as exc:
                raise CandidateVerificationError(
                    "candidate Diff cannot be re-attested after project-test PASS"
                ) from exc
            if current_diff_sha256 != receipt.get("candidate_diff_sha256"):
                raise CandidateVerificationError(
                    "candidate Diff changed after project-test PASS"
                )
        return dict(receipt)


class ProjectTestCandidateVerifier:
    """Verify an owned Builder worktree with the immutable Runtime Adapter snapshot."""

    def __init__(
        self,
        *,
        repo_root: Path | str,
        runtime_root: Path | str,
        authority_snapshot: AuthoritySnapshot,
        executor: ProjectTestExecutor,
        mailbox: VerificationEvidenceMailbox,
    ) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self.runtime_root = Path(runtime_root).resolve(strict=False)
        self.authority_snapshot = authority_snapshot
        self.executor = executor
        self.mailbox = mailbox
        self.registry = WorkspaceOwnershipRegistry(
            repo_root=self.repo_root,
            runtime_root=self.runtime_root,
        )

    @staticmethod
    def _blocked(request: RunRequest, code: str) -> TestSuiteResult:
        return TestSuiteResult(
            project_id=request.project_id,
            expected_main_sha=request.expected_main_sha,
            status="BLOCKED",
            commands=(
                CommandEvidence(
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
                ),
            ),
        )

    def _snapshot_matches(self, request: RunRequest) -> bool:
        return (
            self.authority_snapshot.project_id == request.project_id
            and self.authority_snapshot.package_id == request.package_id
            and self.authority_snapshot.source_main_sha == request.expected_main_sha
            and self.authority_snapshot.capsule_path == request.capsule_path
            and request.package_path in self.authority_snapshot.paths
            and self.authority_snapshot.runtime_adapter_path
            in self.authority_snapshot.paths
        )

    @staticmethod
    def _worker_matches(request: RunRequest, worker: WorkerResult) -> bool:
        return (
            worker.project_id == request.project_id
            and worker.run_id == request.run_id
            and worker.package_id == request.package_id
            and worker.expected_main_sha == request.expected_main_sha
            and worker.status == "COMPLETED"
        )

    def preflight(self, request: RunRequest) -> bool:
        """Prove the configured network boundary can prepare every approved test command.

        This runs before Builder model usage. It may resolve/probe the boundary (for
        example, inspect the pinned local Docker image) but it never executes a
        project test command or creates the Builder worktree.
        """
        if not self._snapshot_matches(request):
            return False
        try:
            adapter = self.authority_snapshot.parsed_object(
                self.authority_snapshot.runtime_adapter_path
            )
        except AuthoritySnapshotError:
            return False
        if adapter.get("project_id") != request.project_id:
            return False
        commands = adapter.get("test_commands")
        if not isinstance(commands, list) or not commands:
            return False
        environment = {
            "CI": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1",
        }
        for command in commands:
            if not isinstance(command, dict):
                return False
            raw_argv = command.get("argv")
            policy = command.get("network")
            if (
                not isinstance(raw_argv, list)
                or not raw_argv
                or any(not isinstance(item, str) or not item for item in raw_argv)
                or not isinstance(policy, str)
            ):
                return False
            plan = self.executor.network_boundary.prepare(
                policy=policy,
                argv=tuple(raw_argv),
                cwd=self.repo_root,
                environment=environment,
            )
            if plan is None:
                return False
        return True

    def verify(
        self,
        request: RunRequest,
        worker_result: WorkerResult,
    ) -> TestSuiteResult:
        if not self._snapshot_matches(request):
            return self._blocked(request, "AUTHORITY_SNAPSHOT_IDENTITY_MISMATCH")
        if not self._worker_matches(request, worker_result):
            return self._blocked(request, "CANDIDATE_WORKER_IDENTITY_MISMATCH")

        workspace = self.runtime_root / request.project_id / request.run_id
        try:
            self.registry.verify(
                project_id=request.project_id,
                run_id=request.run_id,
                expected_main_sha=request.expected_main_sha,
                workspace=workspace,
            )
        except WorkspaceOwnershipError:
            return self._blocked(request, "CANDIDATE_WORKSPACE_OWNERSHIP_INVALID")

        try:
            adapter_text = self.authority_snapshot.text(
                self.authority_snapshot.runtime_adapter_path
            )
        except AuthoritySnapshotError:
            return self._blocked(request, "CANDIDATE_RUNTIME_ADAPTER_MISSING")

        try:
            diff_before = compute_worktree_diff_sha256(workspace)
            with tempfile.TemporaryDirectory(prefix="loop-a2-authority-adapter-") as temp:
                adapter_path = Path(temp) / "RUNTIME_ADAPTER.json"
                adapter_path.write_text(adapter_text, encoding="utf-8", newline="")
                result = self.executor.run_all(
                    adapter_path=adapter_path,
                    worktree_path=workspace,
                    expected_project_id=request.project_id,
                    expected_main_sha=request.expected_main_sha,
                )
            diff_after = compute_worktree_diff_sha256(workspace)
        except (OSError, subprocess.SubprocessError, ValueError):
            return self._blocked(request, "CANDIDATE_TEST_EXECUTION_ERROR")

        if diff_after != diff_before:
            return self._blocked(
                request,
                "CANDIDATE_CHANGED_DURING_TEST_VERIFICATION",
            )

        if result.status == "PASS":
            try:
                self.mailbox.publish_pass(
                    request,
                    result,
                    authority_snapshot_sha256=self.authority_snapshot.snapshot_sha256,
                    candidate_diff_sha256=diff_before,
                    workspace_path=workspace,
                )
            except CandidateVerificationError:
                return self._blocked(request, "CANDIDATE_TEST_EVIDENCE_INVALID")
        return result
