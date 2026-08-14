from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.loop_a2_runtime.authority_snapshot import AuthorityFile, AuthoritySnapshot
from tools.loop_a2_runtime.candidate_verification import (
    CandidateVerificationError,
    ProjectTestCandidateVerifier,
    VerificationEvidenceMailbox,
)
from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tools.loop_a2_runtime.test_executor import NetworkExecutionPlan, ProjectTestExecutor
from tools.loop_a2_runtime.workspace_registry import WorkspaceOwnershipRegistry


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=check
    )


class _Boundary:
    boundary_id = "CANDIDATE_TEST_BOUNDARY"

    def prepare(self, *, policy, argv, cwd, environment):
        return NetworkExecutionPlan(
            argv=tuple(argv),
            environment=dict(environment),
            boundary_id=self.boundary_id,
        )


class CandidateVerificationTests(unittest.TestCase):
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
        self.request = self._request("RUN_VERIFY_001")
        self.workspace = self.runtime / self.request.project_id / self.request.run_id
        self.workspace.parent.mkdir(parents=True, exist_ok=True)
        _git(self.repo, "worktree", "add", "--detach", str(self.workspace), self.sha)
        registry = WorkspaceOwnershipRegistry(repo_root=self.repo, runtime_root=self.runtime)
        registry.claim(
            project_id=self.request.project_id,
            run_id=self.request.run_id,
            expected_main_sha=self.sha,
            workspace=self.workspace,
        )
        (self.workspace / "tests/marker.txt").write_text("builder-change\n", encoding="utf-8")

    def tearDown(self) -> None:
        _git(self.repo, "worktree", "remove", "--force", str(self.workspace), check=False)
        self.temp.cleanup()

    def _request(self, run_id: str) -> RunRequest:
        return RunRequest.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_RUN_REQUEST",
                "project_id": "TEST_GAME",
                "run_id": run_id,
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

    def _worker(self) -> WorkerResult:
        return WorkerResult.from_dict(
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

    def _snapshot(self, *, exit_code: int = 0) -> AuthoritySnapshot:
        adapter = {
            "schema_version": 1,
            "contract_role": "LOOP_RUNTIME_ADAPTER",
            "project_id": self.request.project_id,
            "status": "PROJECT_ADAPTER_VALIDATED",
            "engine": {"name": "Fixture", "version": "1"},
            "languages": ["Python"],
            "source_roots": ["tests/"],
            "test_commands": [
                {
                    "command_id": "CANDIDATE_CONTRACT",
                    "argv": [
                        sys.executable,
                        "-c",
                        (
                            "from pathlib import Path; import sys; "
                            "ok = Path('tests/marker.txt').read_text() == 'builder-change\\n'; "
                            f"sys.exit({exit_code} if ok else 9)"
                        ),
                    ],
                    "working_directory": ".",
                    "timeout_seconds": 10,
                    "network": "DENIED",
                }
            ],
            "runtime_commands": [],
            "build_commands": [],
            "protected_paths": ["tests/"],
            "semantic_resource_domains": ["TEST_DOMAIN"],
            "rollback_strategy": "Discard fixture worktree.",
        }
        relative = "docs/operations/loop/RUNTIME_ADAPTER.json"
        capsule = {
            "contract_role": "LOOP_PROJECT_EXECUTION_CAPSULE",
            "project_id": self.request.project_id,
            "source_main_sha": self.sha,
            "runtime_adapter_path": "RUNTIME_ADAPTER.json",
            "implementation_package_path": "IMPLEMENTATION_PACKAGE.json",
        }
        package = {
            "contract_role": "LOOP_IMPLEMENTATION_PACKAGE",
            "project_id": self.request.project_id,
            "package_id": self.request.package_id,
            "source_main_sha": self.sha,
        }
        return AuthoritySnapshot(
            project_id=self.request.project_id,
            package_id=self.request.package_id,
            source_main_sha=self.sha,
            capsule_path=self.request.capsule_path,
            runtime_adapter_path=relative,
            files=(
                AuthorityFile(
                    path=self.request.capsule_path,
                    content=json.dumps(capsule),
                ),
                AuthorityFile(
                    path=self.request.package_path,
                    content=json.dumps(package),
                ),
                AuthorityFile(path=relative, content=json.dumps(adapter)),
            ),
            snapshot_sha256="a" * 64,
        )

    def _verifier(self, snapshot: AuthoritySnapshot, mailbox: VerificationEvidenceMailbox):
        return ProjectTestCandidateVerifier(
            repo_root=self.repo,
            runtime_root=self.runtime,
            authority_snapshot=snapshot,
            executor=ProjectTestExecutor(network_boundary=_Boundary()),
            mailbox=mailbox,
        )

    def test_pass_candidate_publishes_identity_bound_digest_only_receipt(self) -> None:
        mailbox = VerificationEvidenceMailbox()
        result = self._verifier(self._snapshot(), mailbox).verify(
            self.request,
            self._worker(),
        )

        self.assertEqual(result.status, "PASS")
        evidence = mailbox.require_pass(self.request)
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["project_id"], self.request.project_id)
        self.assertEqual(evidence["run_id"], self.request.run_id)
        self.assertEqual(evidence["package_id"], self.request.package_id)
        self.assertEqual(evidence["expected_main_sha"], self.sha)
        self.assertRegex(evidence["receipt_digest"], r"^[0-9a-f]{64}$")
        rendered = json.dumps(evidence)
        self.assertNotIn("builder-change", rendered)
        self.assertNotIn('"stdout"', rendered)
        self.assertNotIn('"stderr"', rendered)

    def test_failed_candidate_never_publishes_pass_receipt(self) -> None:
        mailbox = VerificationEvidenceMailbox()
        result = self._verifier(self._snapshot(exit_code=7), mailbox).verify(
            self.request,
            self._worker(),
        )

        self.assertEqual(result.status, "FAIL")
        with self.assertRaisesRegex(CandidateVerificationError, "PASS"):
            mailbox.require_pass(self.request)

    def test_cross_run_request_cannot_reuse_owned_workspace_or_receipt(self) -> None:
        mailbox = VerificationEvidenceMailbox()
        self._verifier(self._snapshot(), mailbox).verify(self.request, self._worker())
        other = self._request("RUN_VERIFY_002")

        with self.assertRaisesRegex(CandidateVerificationError, "PASS"):
            mailbox.require_pass(other)
        result = self._verifier(self._snapshot(), mailbox).verify(other, self._worker())
        self.assertEqual(result.status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
