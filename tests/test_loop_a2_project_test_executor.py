from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.loop_a2_runtime.test_executor import (
    NetworkExecutionPlan,
    ProjectTestExecutor,
)


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


class TestFixtureNetworkBoundary:
    boundary_id = "TEST_FIXTURE_NO_REAL_NETWORK_CLAIM"

    def prepare(self, *, policy, argv, cwd, environment):
        return NetworkExecutionPlan(
            argv=tuple(argv),
            environment=dict(environment),
            boundary_id=self.boundary_id,
        )


class ProjectTestExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Loop Test")
        git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/marker.txt").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "base")
        self.sha = git(self.repo, "rev-parse", "HEAD")
        self.adapter_path = self.repo / "RUNTIME_ADAPTER.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_adapter(self, commands, *, project_id: str = "TEST_GAME") -> None:
        value = {
            "schema_version": 1,
            "contract_role": "LOOP_RUNTIME_ADAPTER",
            "project_id": project_id,
            "status": "PROJECT_ADAPTER_VALIDATED",
            "engine": {"name": "Fixture", "version": "1"},
            "languages": ["Python"],
            "source_roots": ["tests/"],
            "test_commands": commands,
            "runtime_commands": [],
            "build_commands": [],
            "protected_paths": ["tests/"],
            "semantic_resource_domains": ["TEST_DOMAIN"],
            "rollback_strategy": "Discard fixture worktree.",
        }
        self.adapter_path.write_text(
            json.dumps(value, indent=2) + "\n",
            encoding="utf-8",
        )

    def command(
        self,
        argv,
        *,
        command_id: str = "TEST_COMMAND",
        working_directory: str = ".",
        timeout_seconds: int = 5,
        network: str = "DENIED",
    ):
        return {
            "command_id": command_id,
            "argv": list(argv),
            "working_directory": working_directory,
            "timeout_seconds": timeout_seconds,
            "network": network,
        }

    def executor(self, **kwargs) -> ProjectTestExecutor:
        return ProjectTestExecutor(
            network_boundary=TestFixtureNetworkBoundary(),
            **kwargs,
        )

    def run_executor(self, executor: ProjectTestExecutor):
        return executor.run_all(
            adapter_path=self.adapter_path,
            worktree_path=self.repo,
            expected_project_id="TEST_GAME",
            expected_main_sha=self.sha,
        )

    def test_default_executor_fails_closed_when_network_policy_is_unenforced(self) -> None:
        marker = self.repo / "should-not-exist.txt"
        self.write_adapter(
            [
                self.command(
                    [
                        sys.executable,
                        "-c",
                        f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')",
                    ]
                )
            ]
        )
        result = self.run_executor(ProjectTestExecutor())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "NETWORK_POLICY_UNENFORCED")
        self.assertFalse(marker.exists())

    def test_read_only_approved_network_also_requires_real_enforcement(self) -> None:
        self.write_adapter(
            [self.command([sys.executable, "-c", "pass"], network="READ_ONLY_APPROVED")]
        )
        result = self.run_executor(ProjectTestExecutor())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "NETWORK_POLICY_UNENFORCED")

    def test_success_records_digest_only_evidence_without_raw_output(self) -> None:
        self.write_adapter(
            [self.command([sys.executable, "-c", "print('bounded output')"])]
        )
        result = self.run_executor(self.executor())
        self.assertEqual(result.status, "PASS")
        command = result.commands[0]
        self.assertEqual(command.status, "PASS")
        self.assertRegex(command.stdout_sha256, r"^[0-9a-f]{64}$")
        payload = result.to_dict()
        self.assertNotIn("stdout", payload["commands"][0])
        self.assertNotIn("stderr", payload["commands"][0])
        self.assertRegex(payload["receipt_digest"], r"^[0-9a-f]{64}$")

    def test_nonzero_exit_is_verification_failure(self) -> None:
        self.write_adapter(
            [self.command([sys.executable, "-c", "raise SystemExit(7)"])]
        )
        result = self.run_executor(self.executor())
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.commands[0].status, "FAIL")
        self.assertEqual(result.commands[0].exit_code, 7)
        self.assertEqual(result.commands[0].error_code, "TEST_EXIT_NONZERO")

    def test_timeout_is_fail_closed(self) -> None:
        self.write_adapter(
            [
                self.command(
                    [sys.executable, "-c", "import time; time.sleep(3)"],
                    timeout_seconds=1,
                )
            ]
        )
        result = self.run_executor(self.executor())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].status, "TIMEOUT")
        self.assertEqual(result.commands[0].error_code, "TEST_TIMEOUT")

    def test_output_limit_blocks_without_persisting_output(self) -> None:
        self.write_adapter(
            [self.command([sys.executable, "-c", "print('x' * 10000)"])]
        )
        result = self.run_executor(self.executor(output_limit_bytes=2048))
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "TEST_OUTPUT_LIMIT")
        self.assertNotIn("x" * 100, json.dumps(result.to_dict()))

    def test_parent_openai_secret_is_not_inherited(self) -> None:
        self.write_adapter(
            [
                self.command(
                    [
                        sys.executable,
                        "-c",
                        "import os,sys; sys.exit(9 if os.environ.get('OPENAI_API_KEY') else 0)",
                    ]
                )
            ]
        )
        previous = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "sentinel-must-not-cross"
        try:
            result = self.run_executor(self.executor())
            self.assertEqual(result.status, "PASS")
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous

    def test_cross_platform_parent_working_directory_is_rejected(self) -> None:
        for unsafe in ("../outside", "..\\outside"):
            with self.subTest(unsafe=unsafe):
                self.write_adapter(
                    [self.command([sys.executable, "-c", "pass"], working_directory=unsafe)]
                )
                result = self.run_executor(self.executor())
                self.assertEqual(result.status, "BLOCKED")
                self.assertEqual(result.commands[0].error_code, "TEST_WORKING_DIRECTORY_UNSAFE")

    def test_symlink_working_directory_escape_is_rejected(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        link = self.repo / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink unavailable")
        self.write_adapter(
            [self.command([sys.executable, "-c", "pass"], working_directory="linked")]
        )
        result = self.run_executor(self.executor())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "TEST_WORKING_DIRECTORY_UNSAFE")

    def test_workspace_mutation_by_test_command_is_blocked(self) -> None:
        self.write_adapter(
            [
                self.command(
                    [
                        sys.executable,
                        "-c",
                        "from pathlib import Path; Path('tests/mutated.txt').write_text('bad')",
                    ]
                )
            ]
        )
        result = self.run_executor(self.executor())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "TEST_MUTATED_WORKSPACE")

    def test_stale_or_wrong_project_blocks_before_command_execution(self) -> None:
        self.write_adapter([self.command([sys.executable, "-c", "pass"])])
        executor = self.executor()
        stale = executor.run_all(
            adapter_path=self.adapter_path,
            worktree_path=self.repo,
            expected_project_id="TEST_GAME",
            expected_main_sha="f" * 40,
        )
        self.assertEqual(stale.status, "BLOCKED")
        self.assertEqual(stale.commands[0].error_code, "TEST_WORKTREE_SHA_MISMATCH")

        wrong = executor.run_all(
            adapter_path=self.adapter_path,
            worktree_path=self.repo,
            expected_project_id="OTHER_GAME",
            expected_main_sha=self.sha,
        )
        self.assertEqual(wrong.status, "BLOCKED")
        self.assertEqual(wrong.commands[0].error_code, "TEST_ADAPTER_PROJECT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
