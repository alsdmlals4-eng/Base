from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.loop_a2_runtime.authority_snapshot import AuthorityFile, AuthoritySnapshot
from tools.loop_a2_runtime.candidate_verification import (
    CandidateVerificationError,
    ProjectTestCandidateVerifier,
    VerificationEvidenceMailbox,
)
from tools.loop_a2_runtime.codex_cli_transport import (
    CodexCliTransportError,
    VerificationBoundCodexResponsesClient,
)
from tools.loop_a2_runtime.integration import compute_worktree_diff_sha256
from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tools.loop_a2_runtime.test_executor import CommandEvidence, TestSuiteResult
from tools.loop_a2_runtime.workspace_registry import WorkspaceOwnershipRegistry


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=check
    )


class _PassExecutor:
    def __init__(self, *, mutate_workspace: bool = False) -> None:
        self.mutate_workspace = mutate_workspace

    def run_all(
        self,
        *,
        adapter_path: Path,
        worktree_path: Path,
        expected_project_id: str,
        expected_main_sha: str,
    ) -> TestSuiteResult:
        if self.mutate_workspace:
            (worktree_path / "tests/marker.txt").write_text(
                "concurrent-same-path-change\n", encoding="utf-8"
            )
        return TestSuiteResult(
            project_id=expected_project_id,
            expected_main_sha=expected_main_sha,
            status="PASS",
            commands=(
                CommandEvidence(
                    command_id="UNIT",
                    status="PASS",
                    exit_code=0,
                    error_code=None,
                    stdout_sha256="a" * 64,
                    stderr_sha256="b" * 64,
                    stdout_bytes=7,
                    stderr_bytes=0,
                    network_policy="DENIED",
                    network_boundary_id="TEST_BOUNDARY",
                    duration_ms=11,
                ),
            ),
        )


class _Response:
    output_text = "{}"
    usage = None


class _BaseClient:
    def __init__(self) -> None:
        self.responses = self
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response()


class CandidateDiffBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.runtime = self.root / "runtime"
        self.repo.mkdir()
        _git(self.repo, "init", "-b", "main")
        _git(self.repo, "config", "user.name", "Loop Test")
        _git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/marker.txt").write_text("base\n", encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "baseline")
        self.sha = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.request = RunRequest.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_RUN_REQUEST",
                "project_id": "TEST_GAME",
                "run_id": "RUN_DIFF_BINDING_001",
                "package_id": "PACKAGE_001",
                "expected_main_sha": self.sha,
                "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
                "allowed_paths": ["tests/marker.txt"],
                "forbidden_paths": [".github/**"],
                "resource_locks": ["TEST_DOMAIN"],
                "requirement_ids": ["REQ_001"],
                "budgets": {
                    "max_turns": 4,
                    "max_repair_cycles": 1,
                    "timeout_seconds": 30,
                },
                "provider_mode": "REAL",
            }
        )
        self.workspace = self.runtime / self.request.project_id / self.request.run_id
        self.workspace.parent.mkdir(parents=True, exist_ok=True)
        _git(self.repo, "worktree", "add", "--detach", str(self.workspace), self.sha)
        WorkspaceOwnershipRegistry(repo_root=self.repo, runtime_root=self.runtime).claim(
            project_id=self.request.project_id,
            run_id=self.request.run_id,
            expected_main_sha=self.sha,
            workspace=self.workspace,
        )
        (self.workspace / "tests/marker.txt").write_text("builder-change\n", encoding="utf-8")
        adapter_path = "docs/operations/loop/RUNTIME_ADAPTER.json"
        self.snapshot = AuthoritySnapshot(
            project_id=self.request.project_id,
            package_id=self.request.package_id,
            source_main_sha=self.sha,
            capsule_path=self.request.capsule_path,
            runtime_adapter_path=adapter_path,
            files=(
                AuthorityFile(path=self.request.capsule_path, content="{}"),
                AuthorityFile(path=self.request.package_path, content="{}"),
                AuthorityFile(
                    path=adapter_path,
                    content=json.dumps(
                        {
                            "schema_version": 1,
                            "contract_role": "LOOP_RUNTIME_ADAPTER",
                            "project_id": self.request.project_id,
                            "status": "PROJECT_ADAPTER_VALIDATED",
                            "test_commands": [],
                        }
                    ),
                ),
            ),
            snapshot_sha256="c" * 64,
        )
        self.worker = WorkerResult.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_WORKER_RESULT",
                "project_id": self.request.project_id,
                "run_id": self.request.run_id,
                "package_id": self.request.package_id,
                "expected_main_sha": self.sha,
                "role": "BUILDER",
                "status": "COMPLETED",
                "changed_paths": ["tests/marker.txt"],
                "summary": "candidate",
                "usage": {"turns": 1},
                "errors": [],
            }
        )

    def tearDown(self) -> None:
        _git(self.repo, "worktree", "remove", "--force", str(self.workspace), check=False)
        self.temp.cleanup()

    def _verifier(
        self,
        mailbox: VerificationEvidenceMailbox,
        *,
        mutate_workspace: bool = False,
    ) -> ProjectTestCandidateVerifier:
        return ProjectTestCandidateVerifier(
            repo_root=self.repo,
            runtime_root=self.runtime,
            authority_snapshot=self.snapshot,
            executor=_PassExecutor(mutate_workspace=mutate_workspace),
            mailbox=mailbox,
        )

    def test_pass_receipt_records_exact_candidate_diff_digest(self) -> None:
        mailbox = VerificationEvidenceMailbox()
        expected_diff = compute_worktree_diff_sha256(self.workspace)

        result = self._verifier(mailbox).verify(self.request, self.worker)

        self.assertEqual(result.status, "PASS")
        evidence = mailbox.require_pass(self.request)
        self.assertEqual(evidence["candidate_diff_sha256"], expected_diff)

    def test_candidate_content_change_during_verification_blocks_pass_publication(self) -> None:
        mailbox = VerificationEvidenceMailbox()

        result = self._verifier(mailbox, mutate_workspace=True).verify(
            self.request, self.worker
        )

        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(
            result.commands[0].error_code,
            "CANDIDATE_CHANGED_DURING_TEST_VERIFICATION",
        )
        with self.assertRaisesRegex(CandidateVerificationError, "PASS"):
            mailbox.require_pass(self.request)

    def test_critic_rejects_pass_receipt_for_different_same_path_content(self) -> None:
        mailbox = VerificationEvidenceMailbox()
        result = self._verifier(mailbox).verify(self.request, self.worker)
        self.assertEqual(result.status, "PASS")

        (self.workspace / "tests/marker.txt").write_text(
            "changed-after-test\n", encoding="utf-8"
        )
        current_diff = compute_worktree_diff_sha256(self.workspace)
        base = _BaseClient()
        client = VerificationBoundCodexResponsesClient(
            base_client=base,
            run_request=self.request,
            verification_mailbox=mailbox,
        )

        with self.assertRaisesRegex(
            CodexCliTransportError,
            "CRITIC_TEST_EVIDENCE_DIFF_MISMATCH",
        ):
            client.responses.create(
                model="critic-model",
                instructions="critic",
                input=json.dumps(
                    {
                        "project_id": self.request.project_id,
                        "package_id": self.request.package_id,
                        "diff_sha256": current_diff,
                        "diff": "same path, different content",
                    }
                ),
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "review",
                        "strict": True,
                        "schema": {"type": "object"},
                    }
                },
                store=False,
                max_output_tokens=128,
                timeout=30,
            )
        self.assertEqual(base.calls, [])


if __name__ == "__main__":
    unittest.main()
