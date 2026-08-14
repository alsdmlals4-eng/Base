from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.loop_a2_runtime.test_executor import NetworkExecutionPlan, ProjectTestExecutor


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    ).stdout.strip()


class _Boundary:
    boundary_id = "VALUE_TEST_BOUNDARY"

    def prepare(self, *, policy, argv, cwd, environment):
        return NetworkExecutionPlan(
            argv=tuple(argv),
            environment=dict(environment),
            boundary_id=self.boundary_id,
        )


class ProjectTestExecutorValueTests(unittest.TestCase):
    def test_value_entry_matches_file_entry_without_requiring_authority_file_in_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()
            _git(repo, "init", "-b", "main")
            _git(repo, "config", "user.name", "Loop Test")
            _git(repo, "config", "user.email", "loop@example.invalid")
            (repo / "tests").mkdir()
            (repo / "tests/marker.txt").write_text("base\n", encoding="utf-8")
            _git(repo, "add", ".")
            _git(repo, "commit", "-m", "baseline")
            sha = _git(repo, "rev-parse", "HEAD")

            adapter = {
                "schema_version": 1,
                "contract_role": "LOOP_RUNTIME_ADAPTER",
                "project_id": "TEST_GAME",
                "status": "PROJECT_ADAPTER_VALIDATED",
                "engine": {"name": "Fixture", "version": "1"},
                "languages": ["Python"],
                "source_roots": ["tests/"],
                "test_commands": [
                    {
                        "command_id": "VALUE_PASS",
                        "argv": [sys.executable, "-c", "raise SystemExit(0)"],
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
            adapter_path = root / "RUNTIME_ADAPTER.json"
            adapter_path.write_text(json.dumps(adapter), encoding="utf-8")
            executor = ProjectTestExecutor(network_boundary=_Boundary())

            file_result = executor.run_all(
                adapter_path=adapter_path,
                worktree_path=repo,
                expected_project_id="TEST_GAME",
                expected_main_sha=sha,
            )
            value_result = executor.run_all_from_value(
                adapter_value=adapter,
                worktree_path=repo,
                expected_project_id="TEST_GAME",
                expected_main_sha=sha,
            )

            self.assertEqual(file_result.status, "PASS")
            self.assertEqual(value_result.status, "PASS")
            self.assertEqual(
                [item.to_dict() for item in value_result.commands],
                [item.to_dict() for item in file_result.commands],
            )
            self.assertFalse((repo / "RUNTIME_ADAPTER.json").exists())


if __name__ == "__main__":
    unittest.main()
