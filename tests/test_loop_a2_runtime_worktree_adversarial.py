from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.worktree_adapter import (
    GitWorktreeBuilderAdapter,
    SubprocessWorkspaceWorker,
)
from tests.test_loop_a2_protocol import valid_request


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=check,
    )


class WorktreeAdapterAdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.runtime = self.root / "runtime"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Loop Test")
        git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts/a.gd").write_text("base\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text("ignored.tmp\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "base")
        self.sha = git(self.repo, "rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def request(self) -> RunRequest:
        value = valid_request()
        value["expected_main_sha"] = self.sha
        value["allowed_paths"] = ["scripts/a.gd"]
        value["forbidden_paths"] = ["project.godot", ".github/**"]
        return RunRequest.from_dict(value)

    def worker(self, *, path: str) -> SubprocessWorkspaceWorker:
        script = self.root / "worker.py"
        script.write_text(
            """from __future__ import annotations
import json
from pathlib import Path
import sys
payload = json.load(sys.stdin)
request = payload['request']
path = Path(%r)
path.write_text('changed\\n', encoding='utf-8')
print(json.dumps({
  'schema_version': 1,
  'contract_role': 'LOOP_A2_WORKER_RESULT',
  'project_id': request['project_id'],
  'run_id': request['run_id'],
  'package_id': request['package_id'],
  'expected_main_sha': request['expected_main_sha'],
  'role': 'BUILDER',
  'status': 'COMPLETED',
  'changed_paths': [%r],
  'summary': 'adversarial fixture',
  'usage': {'turns': 1},
  'errors': []
}))
""" % (path, path),
            encoding="utf-8",
        )
        return SubprocessWorkspaceWorker((sys.executable, str(script)))

    def test_ignored_untracked_write_is_part_of_actual_git_evidence(self) -> None:
        request = self.request()
        adapter = GitWorktreeBuilderAdapter(
            repo_root=self.repo,
            runtime_root=self.runtime,
            worker=self.worker(path="ignored.tmp"),
        )
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "COMPLETED")
            self.assertEqual(result.changed_paths, ("ignored.tmp",))
        finally:
            adapter.close(request)

    def test_close_does_not_remove_unowned_registered_collision(self) -> None:
        request = self.request()
        workspace = self.runtime / request.project_id / request.run_id
        workspace.parent.mkdir(parents=True, exist_ok=True)
        git(
            self.repo,
            "worktree",
            "add",
            "--detach",
            str(workspace),
            request.expected_main_sha,
        )
        adapter = GitWorktreeBuilderAdapter(
            repo_root=self.repo,
            runtime_root=self.runtime,
            worker=self.worker(path="scripts/a.gd"),
        )
        result = adapter.invoke(request, repair_cycle=0)
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.errors[0].code, "WORKSPACE_COLLISION")
        adapter.close(request)
        self.assertTrue(workspace.exists())
        registered = git(self.repo, "worktree", "list", "--porcelain").stdout
        registered_worktrees = [
            Path(line.removeprefix("worktree ")).resolve()
            for line in registered.splitlines()
            if line.startswith("worktree ")
        ]
        self.assertIn(workspace.resolve(), registered_worktrees)
        git(self.repo, "worktree", "remove", "--force", str(workspace))


if __name__ == "__main__":
    unittest.main()
