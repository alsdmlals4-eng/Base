from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tools.loop_a2_runtime.authority_snapshot import capture_authority_snapshot
from tools.loop_a2_runtime.contract_bridge import build_request_from_capsule
from tools.loop_a2_runtime.openai_transport import OpenAIWorkspaceBuilder
from tools.loop_a2_runtime.protocol import Budgets


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates" / "project-operations" / "loop"
CAPSULE = "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json"


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=check
    )


def _rewrite_source_fields(value: object, source_sha: str) -> object:
    if isinstance(value, dict):
        return {
            key: source_sha
            if key in {"source_main_sha", "source_commit"}
            else _rewrite_source_fields(item, source_sha)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_rewrite_source_fields(item, source_sha) for item in value]
    return value


class _Response:
    def __init__(self, payload: dict[str, object]) -> None:
        self.output_text = json.dumps(payload)
        self.usage = None


class _Responses:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response(self.payload)


class _Client:
    def __init__(self, payload: dict[str, object]) -> None:
        self.responses = _Responses(payload)


class AuthorityContextTests(unittest.TestCase):
    def _fixture(self, *, allow_capsule_write: bool = False):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        repo = root / "project"
        repo.mkdir()
        _git(repo, "init", "-b", "main")
        _git(repo, "config", "user.name", "Loop Test")
        _git(repo, "config", "user.email", "loop@example.invalid")
        (repo / "scripts").mkdir()
        (repo / "scripts/example.gd").write_text("extends Node\n", encoding="utf-8")
        _git(repo, "add", ".")
        _git(repo, "commit", "-m", "implementation baseline")
        baseline = _git(repo, "rev-parse", "HEAD").stdout.strip()

        loop = repo / "docs/operations/loop"
        shutil.copytree(TEMPLATE_ROOT, loop)
        for path in sorted(loop.rglob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            value = _rewrite_source_fields(value, baseline)
            if allow_capsule_write and path.name == "IMPLEMENTATION_PACKAGE.json":
                value["allowed_paths"].append(CAPSULE)
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

        request = build_request_from_capsule(
            project_root=repo,
            capsule_relative=CAPSULE,
            run_id="RUN_CONTEXT_001",
            provider_mode="REAL",
            budgets=Budgets(12, 2, 600),
        )
        snapshot = capture_authority_snapshot(
            project_root=repo,
            capsule_relative=CAPSULE,
            request=request,
        )
        worktree = root / "baseline-worktree"
        _git(repo, "worktree", "add", "--detach", str(worktree), baseline)
        self.assertFalse((worktree / CAPSULE).exists())
        return temp, repo, worktree, request, snapshot

    def test_builder_uses_snapshot_authority_while_writing_only_detached_baseline(self) -> None:
        temp, repo, worktree, request, snapshot = self._fixture()
        try:
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "bounded baseline edit",
                    "writes": [
                        {
                            "path": "scripts/example.gd",
                            "content": "extends Node\n# changed by bounded builder\n",
                        }
                    ],
                    "blocked_reason": "",
                }
            )
            builder = OpenAIWorkspaceBuilder(
                client=client,
                model="fixture-model",
                authority_snapshot=snapshot,
            )
            result = builder.invoke(request, worktree_path=worktree, repair_cycle=0)

            self.assertEqual(result.status, "COMPLETED")
            self.assertEqual(result.changed_paths, ("scripts/example.gd",))
            self.assertEqual(len(client.responses.calls), 1)
            prompt = str(client.responses.calls[0]["input"])
            self.assertIn("LOOP_PROJECT_EXECUTION_CAPSULE", prompt)
            self.assertFalse((worktree / CAPSULE).exists())
            self.assertEqual(_git(repo, "status", "--porcelain").stdout.strip(), "?? docs/")
        finally:
            _git(repo, "worktree", "remove", "--force", str(worktree), check=False)
            temp.cleanup()

    def test_snapshot_authority_path_is_immutable_even_when_package_allowlist_is_overbroad(self) -> None:
        temp, repo, worktree, request, snapshot = self._fixture(allow_capsule_write=True)
        try:
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "attempt authority rewrite",
                    "writes": [{"path": CAPSULE, "content": "{}\n"}],
                    "blocked_reason": "",
                }
            )
            builder = OpenAIWorkspaceBuilder(
                client=client,
                model="fixture-model",
                authority_snapshot=snapshot,
            )
            result = builder.invoke(request, worktree_path=worktree, repair_cycle=0)

            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.errors[0].code, "BUILDER_AUTHORITY_WRITE_FORBIDDEN")
            self.assertFalse((worktree / CAPSULE).exists())
        finally:
            _git(repo, "worktree", "remove", "--force", str(worktree), check=False)
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
