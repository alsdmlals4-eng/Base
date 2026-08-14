from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.loop_a2_runtime.candidate_verification import VerificationEvidenceMailbox
from tools.loop_a2_runtime.openai_transport import (
    GitReviewMaterialSource,
    OpenAITransportError,
    OpenAIWorktreeCritic,
)
from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tools.loop_a2_runtime.test_executor import CommandEvidence, TestSuiteResult
from tools.loop_a2_runtime.workspace_registry import WorkspaceOwnershipRegistry


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=check
    )


class _Response:
    output_text = json.dumps(
        {
            "verdict": "PASS",
            "findings": [],
            "checked_requirement_ids": ["REQ_001"],
        }
    )
    usage = None


class _Responses:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response()


class _Client:
    def __init__(self) -> None:
        self.responses = _Responses()


class CriticTestEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.runtime = self.root / "runtime"
        self.repo.mkdir()
        _git(self.repo, "init", "-b", "main")
        _git(self.repo, "config", "user.name", "Loop Test")
        _git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "scripts/feature").mkdir(parents=True)
        (self.repo / "scripts/feature/a.gd").write_text("before\n", encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "baseline")
        self.sha = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.request = RunRequest.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_RUN_REQUEST",
                "project_id": "TEST_GAME",
                "run_id": "RUN_CRITIC_TEST_001",
                "package_id": "PACKAGE_001",
                "expected_main_sha": self.sha,
                "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
                "allowed_paths": ["scripts/feature/a.gd"],
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
        (self.workspace / "scripts/feature/a.gd").write_text("after\n", encoding="utf-8")
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
                "changed_paths": ["scripts/feature/a.gd"],
                "summary": "candidate",
                "usage": {"turns": 1},
                "errors": [],
            }
        )

    def tearDown(self) -> None:
        _git(self.repo, "worktree", "remove", "--force", str(self.workspace), check=False)
        self.temp.cleanup()

    def _mailbox_with_pass(self) -> VerificationEvidenceMailbox:
        mailbox = VerificationEvidenceMailbox()
        suite = TestSuiteResult(
            project_id=self.request.project_id,
            expected_main_sha=self.sha,
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
                    duration_ms=12,
                ),
            ),
        )
        mailbox.publish_pass(
            self.request,
            suite,
            authority_snapshot_sha256="c" * 64,
        )
        return mailbox

    def test_review_material_requires_matching_pass_receipt_when_mailbox_is_configured(self) -> None:
        empty = VerificationEvidenceMailbox()
        source = GitReviewMaterialSource(
            repo_root=self.repo,
            runtime_root=self.runtime,
            verification_mailbox=empty,
        )

        with self.assertRaisesRegex(OpenAITransportError, "CRITIC_TEST_EVIDENCE_MISSING"):
            source.collect(self.request, self.worker)

    def test_matching_pass_receipt_is_bound_to_material_and_critic_payload(self) -> None:
        mailbox = self._mailbox_with_pass()
        source = GitReviewMaterialSource(
            repo_root=self.repo,
            runtime_root=self.runtime,
            verification_mailbox=mailbox,
        )
        material = source.collect(self.request, self.worker)

        self.assertIsNotNone(material.test_evidence)
        assert material.test_evidence is not None
        self.assertEqual(material.test_evidence["status"], "PASS")
        self.assertEqual(material.test_evidence["run_id"], self.request.run_id)

        client = _Client()
        critic = OpenAIWorktreeCritic(
            client=client,
            model="critic-model",
            material_source=source,
        )
        review = critic.review(self.request, self.worker)
        self.assertEqual(review.verdict, "PASS")
        payload = json.loads(str(client.responses.calls[0]["input"]))
        evidence = payload["test_evidence"]
        self.assertEqual(evidence["status"], "PASS")
        command = evidence["test_suite"]["commands"][0]
        self.assertIn("stdout_sha256", command)
        self.assertIn("stderr_sha256", command)
        self.assertNotIn("stdout", command)
        self.assertNotIn("stderr", command)


if __name__ == "__main__":
    unittest.main()
