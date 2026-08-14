from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.loop_a2_runtime.authority_snapshot import AuthorityFile, AuthoritySnapshot
from tools.loop_a2_runtime.candidate_verification import (
    ProjectTestCandidateVerifier,
    VerificationEvidenceMailbox,
)
from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.test_executor import (
    NetworkExecutionPlan,
    ProjectTestExecutor,
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    ).stdout.strip()


class _AvailableBoundary:
    def prepare(self, *, policy, argv, cwd, environment):
        if policy != "DENIED":
            return None
        return NetworkExecutionPlan(
            argv=tuple(argv),
            environment=dict(environment),
            boundary_id="PREFLIGHT_TEST_BOUNDARY",
        )


class CandidatePreflightTests(unittest.TestCase):
    def test_preflight_proves_all_runtime_adapter_network_policies_before_builder(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            runtime = root / "runtime"
            repo.mkdir()
            _git(repo, "init", "-b", "main")
            _git(repo, "config", "user.name", "Loop Test")
            _git(repo, "config", "user.email", "loop@example.invalid")
            (repo / "README.md").write_text("baseline\n", encoding="utf-8")
            _git(repo, "add", ".")
            _git(repo, "commit", "-m", "baseline")
            sha = _git(repo, "rev-parse", "HEAD")
            request = RunRequest.from_dict(
                {
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_RUN_REQUEST",
                    "project_id": "TEST_GAME",
                    "run_id": "RUN_PREFLIGHT_001",
                    "package_id": "PACKAGE_001",
                    "expected_main_sha": sha,
                    "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                    "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
                    "allowed_paths": ["README.md"],
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
            adapter_path = "docs/operations/loop/RUNTIME_ADAPTER.json"
            adapter = {
                "schema_version": 1,
                "contract_role": "LOOP_RUNTIME_ADAPTER",
                "project_id": request.project_id,
                "status": "PROJECT_ADAPTER_VALIDATED",
                "engine": {"name": "Fixture", "version": "1"},
                "languages": ["Python"],
                "source_roots": ["tests/"],
                "test_commands": [
                    {
                        "command_id": "UNIT",
                        "argv": ["python", "-c", "pass"],
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
            snapshot = AuthoritySnapshot(
                project_id=request.project_id,
                package_id=request.package_id,
                source_main_sha=sha,
                capsule_path=request.capsule_path,
                runtime_adapter_path=adapter_path,
                files=(
                    AuthorityFile(path=request.capsule_path, content="{}"),
                    AuthorityFile(path=request.package_path, content="{}"),
                    AuthorityFile(path=adapter_path, content=json.dumps(adapter)),
                ),
                snapshot_sha256="d" * 64,
            )

            available = ProjectTestCandidateVerifier(
                repo_root=repo,
                runtime_root=runtime,
                authority_snapshot=snapshot,
                executor=ProjectTestExecutor(network_boundary=_AvailableBoundary()),
                mailbox=VerificationEvidenceMailbox(),
            )
            unavailable = ProjectTestCandidateVerifier(
                repo_root=repo,
                runtime_root=runtime,
                authority_snapshot=snapshot,
                executor=ProjectTestExecutor(),
                mailbox=VerificationEvidenceMailbox(),
            )

            self.assertTrue(available.preflight(request))
            self.assertFalse(unavailable.preflight(request))


if __name__ == "__main__":
    unittest.main()
