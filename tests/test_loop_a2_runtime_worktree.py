from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.providers import FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tools.loop_a2_runtime.worktree_adapter import (
    GitWorktreeBuilderAdapter,
    SubprocessWorkspaceWorker,
)
from tests.test_loop_a2_protocol import valid_request


def run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


class WorktreeAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.runtime = self.root / "runtime"
        self.repo.mkdir()
        run_git(self.repo, "init", "-b", "main")
        run_git(self.repo, "config", "user.name", "Loop Test")
        run_git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "scripts/feature").mkdir(parents=True)
        (self.repo / "scripts/feature/a.gd").write_text("before\n", encoding="utf-8")
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        run_git(self.repo, "add", ".")
        run_git(self.repo, "commit", "-m", "base")
        self.sha = run_git(self.repo, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def request(self, *, timeout_seconds: int = 10) -> RunRequest:
        value = valid_request()
        value["expected_main_sha"] = self.sha
        value["allowed_paths"] = ["scripts/feature/a.gd"]
        value["forbidden_paths"] = ["project.godot", ".github/**"]
        value["budgets"]["timeout_seconds"] = timeout_seconds
        return RunRequest.from_dict(value)

    def worker_script(
        self,
        *,
        changed_path: str = "scripts/feature/a.gd",
        declared_path: str | None = None,
        sleep_seconds: float = 0,
        report_environment_key: str | None = None,
    ) -> Path:
        script = self.root / f"worker_{len(list(self.root.glob('worker_*.py')))}.py"
        declared = declared_path or changed_path
        source = f'''from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import time
payload = json.load(sys.stdin)
time.sleep({sleep_seconds!r})
path = Path({changed_path!r})
path.parent.mkdir(parents=True, exist_ok=True)
content = "changed\\n"
key = {report_environment_key!r}
if key:
    content = "KEY_PRESENT\\n" if os.environ.get(key) else "NO_KEY\\n"
path.write_text(content, encoding="utf-8")
request = payload["request"]
print(json.dumps({{
    "schema_version": 1,
    "contract_role": "LOOP_A2_WORKER_RESULT",
    "project_id": request["project_id"],
    "run_id": request["run_id"],
    "package_id": request["package_id"],
    "expected_main_sha": request["expected_main_sha"],
    "role": "BUILDER",
    "status": "COMPLETED",
    "changed_paths": [{declared!r}],
    "summary": "workspace fixture",
    "usage": {{"turns": 1}},
    "errors": []
}}))
'''
        script.write_text(source, encoding="utf-8")
        return script

    def adapter(self, script: Path) -> GitWorktreeBuilderAdapter:
        worker = SubprocessWorkspaceWorker((sys.executable, str(script)))
        return GitWorktreeBuilderAdapter(
            repo_root=self.repo,
            runtime_root=self.runtime,
            worker=worker,
        )

    def test_real_git_diff_replaces_worker_claim(self) -> None:
        request = self.request()
        adapter = self.adapter(self.worker_script())
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "COMPLETED")
            self.assertEqual(result.changed_paths, ("scripts/feature/a.gd",))
            self.assertEqual(run_git(self.repo, "status", "--porcelain"), "")
            self.assertTrue(adapter.workspace_path(request).is_dir())
        finally:
            adapter.close(request)

    def test_declared_diff_mismatch_is_blocked_with_actual_paths(self) -> None:
        request = self.request()
        adapter = self.adapter(
            self.worker_script(declared_path="scripts/feature/not-actually-written.gd")
        )
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.changed_paths, ("scripts/feature/a.gd",))
            self.assertEqual(result.errors[0].code, "DECLARED_DIFF_MISMATCH")
        finally:
            adapter.close(request)

    def test_subprocess_timeout_is_a_hard_stop(self) -> None:
        request = self.request(timeout_seconds=1)
        adapter = self.adapter(self.worker_script(sleep_seconds=3))
        started = time.monotonic()
        try:
            result = adapter.invoke(request, repair_cycle=0)
            elapsed = time.monotonic() - started
            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.errors[0].code, "WORKER_TIMEOUT")
            self.assertLess(elapsed, 2.8)
        finally:
            adapter.close(request)

    def test_parent_secret_is_not_inherited_by_worker(self) -> None:
        request = self.request()
        adapter = self.adapter(
            self.worker_script(report_environment_key="OPENAI_API_KEY")
        )
        previous = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "sentinel-secret-must-not-cross"
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "COMPLETED")
            content = (adapter.workspace_path(request) / "scripts/feature/a.gd").read_text(
                encoding="utf-8"
            )
            self.assertEqual(content, "NO_KEY\n")
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous
            adapter.close(request)

    def test_actual_out_of_scope_diff_is_quarantined_by_runtime(self) -> None:
        request = self.request()
        adapter = self.adapter(self.worker_script(changed_path="README.md"))
        critic = FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",))
        try:
            outcome = A2Runtime(builder=adapter, critic=critic).run(
                request,
                observed_main_sha=request.expected_main_sha,
            )
            self.assertEqual(outcome.state, "QUARANTINED")
            self.assertIn("OUT_OF_SCOPE_WRITE", outcome.finding_codes)
            self.assertEqual(critic.calls, 0)
        finally:
            adapter.close(request)

    def test_unknown_expected_sha_blocks_before_worker(self) -> None:
        value = valid_request()
        value["expected_main_sha"] = "f" * 40
        value["allowed_paths"] = ["scripts/feature/a.gd"]
        request = RunRequest.from_dict(value)
        adapter = self.adapter(self.worker_script())
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.errors[0].code, "EXPECTED_SHA_UNAVAILABLE")
            self.assertFalse(adapter.workspace_path(request).exists())
        finally:
            adapter.close(request)

    def test_close_removes_external_worktree(self) -> None:
        request = self.request()
        adapter = self.adapter(self.worker_script())
        adapter.invoke(request, repair_cycle=0)
        workspace = adapter.workspace_path(request)
        self.assertTrue(workspace.exists())
        adapter.close(request)
        self.assertFalse(workspace.exists())
        listed = run_git(self.repo, "worktree", "list", "--porcelain")
        self.assertNotIn(str(workspace), listed)

    def test_runtime_root_inside_repository_is_rejected(self) -> None:
        worker = SubprocessWorkspaceWorker((sys.executable, str(self.worker_script())))
        with self.assertRaisesRegex(ValueError, "outside"):
            GitWorktreeBuilderAdapter(
                repo_root=self.repo,
                runtime_root=self.repo / ".loop-runtime",
                worker=worker,
            )


if __name__ == "__main__":
    unittest.main()
