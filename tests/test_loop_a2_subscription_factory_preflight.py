from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.loop_a2_runtime.authority_snapshot import AuthorityFile, AuthoritySnapshot
from tools.loop_a2_runtime.codex_cli_transport import (
    CodexCliTransportError,
    build_subscription_provider_components,
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
            boundary_id="FACTORY_PREFLIGHT_TEST_BOUNDARY",
        )


class _LoginRunner:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, argv, **kwargs):
        self.calls += 1
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout="Logged in using ChatGPT\n",
            stderr="",
        )


class SubscriptionFactoryPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.runtime = self.root / "runtime"
        self.repo.mkdir()
        _git(self.repo, "init", "-b", "main")
        _git(self.repo, "config", "user.name", "Loop Test")
        _git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "README.md").write_text("baseline\n", encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "baseline")
        self.sha = _git(self.repo, "rev-parse", "HEAD")
        self.request = RunRequest.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_RUN_REQUEST",
                "project_id": "TEST_GAME",
                "run_id": "RUN_FACTORY_PREFLIGHT_001",
                "package_id": "PACKAGE_001",
                "expected_main_sha": self.sha,
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
            "project_id": self.request.project_id,
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
        self.snapshot = AuthoritySnapshot(
            project_id=self.request.project_id,
            package_id=self.request.package_id,
            source_main_sha=self.sha,
            capsule_path=self.request.capsule_path,
            runtime_adapter_path=adapter_path,
            files=(
                AuthorityFile(path=self.request.capsule_path, content="{}"),
                AuthorityFile(path=self.request.package_path, content="{}"),
                AuthorityFile(path=adapter_path, content=json.dumps(adapter)),
            ),
            snapshot_sha256="f" * 64,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_unavailable_project_test_boundary_blocks_before_chatgpt_auth_probe(self) -> None:
        login = _LoginRunner()
        with self.assertRaisesRegex(CodexCliTransportError, "PROJECT_TEST_BOUNDARY_UNAVAILABLE"):
            build_subscription_provider_components(
                repo_root=self.repo,
                runtime_root=self.runtime,
                authority_snapshot=self.snapshot,
                run_request=self.request,
                project_test_executor=ProjectTestExecutor(),
                login_runner=login,
            )
        self.assertEqual(login.calls, 0)

    def test_available_project_test_boundary_allows_factory_construction_after_preflight(self) -> None:
        login = _LoginRunner()
        components = build_subscription_provider_components(
            repo_root=self.repo,
            runtime_root=self.runtime,
            authority_snapshot=self.snapshot,
            run_request=self.request,
            project_test_executor=ProjectTestExecutor(
                network_boundary=_AvailableBoundary()
            ),
            login_runner=login,
        )

        self.assertEqual(login.calls, 1)
        self.assertIsNotNone(components.builder)
        self.assertIsNotNone(components.critic)
        self.assertTrue(components.candidate_verifier.preflight(self.request))

    def test_factory_rejects_snapshot_bound_to_another_run_request(self) -> None:
        value = self.request.to_dict()
        value["package_id"] = "OTHER_PACKAGE"
        other = RunRequest.from_dict(value)
        login = _LoginRunner()
        with self.assertRaisesRegex(CodexCliTransportError, "AUTHORITY_SNAPSHOT_IDENTITY_MISMATCH"):
            build_subscription_provider_components(
                repo_root=self.repo,
                runtime_root=self.runtime,
                authority_snapshot=self.snapshot,
                run_request=other,
                project_test_executor=ProjectTestExecutor(
                    network_boundary=_AvailableBoundary()
                ),
                login_runner=login,
            )
        self.assertEqual(login.calls, 0)


if __name__ == "__main__":
    unittest.main()
