from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools/check_external_ai_worktree_contract.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_external_ai_worktree_contract", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class ExternalAIWorktreeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_checker()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        run_git(self.root, "init", "-b", "main")
        run_git(self.root, "config", "user.email", "test@example.com")
        run_git(self.root, "config", "user.name", "Test User")
        (self.root / "docs").mkdir()
        (self.root / "docs/canon.md").write_text("canon\n", encoding="utf-8")
        (self.root / "project.godot").write_text("[application]\n", encoding="utf-8")
        (self.root / ".gitignore").write_text(".worktrees/\n", encoding="utf-8")
        schema_target = self.root / "schemas/external-ai-worktree-contract-v1.schema.json"
        schema_target.parent.mkdir(parents=True)
        schema_target.write_text(
            (ROOT / "schemas/external-ai-worktree-contract-v1.schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        run_git(self.root, "add", ".")
        run_git(self.root, "commit", "-m", "base")
        self.start_commit = run_git(self.root, "rev-parse", "HEAD").stdout.strip()
        self.worktree = self.root / ".worktrees/deepseek-test"
        self.worktree.parent.mkdir()
        run_git(
            self.root,
            "worktree",
            "add",
            str(self.worktree),
            "-b",
            "ai/deepseek-test",
        )
        self.contract_path = self.worktree / "drafts/external-ai/test/worktree-contract.json"
        self.contract_path.parent.mkdir(parents=True)

    def contract(self, **overrides: object) -> dict:
        value = {
            "schema_version": 1,
            "artifact_role": "EXTERNAL_AI_WORKTREE_CONTRACT",
            "repository": "owner/project",
            "base_branch": "main",
            "start_commit": self.start_commit,
            "worktree_path": ".worktrees/deepseek-test",
            "task_branch": "ai/deepseek-test",
            "allowlist": {
                "read": ["docs/**", "skills/**"],
                "write": ["drafts/external-ai/test/**"],
            },
            "protected_paths": ["project.godot", "docs/canon.md"],
            "result_state": "REVIEW_PENDING",
            "integration_state": "NOT_INTEGRATED",
            "cleanup_requested": False,
        }
        value.update(overrides)
        return value

    def write_contract(self, value: dict) -> None:
        self.contract_path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_allows_isolated_review_pending_draft_inside_write_allowlist(self) -> None:
        self.write_contract(self.contract())
        (self.worktree / "drafts/external-ai/test/result.md").write_text(
            "# Draft\n",
            encoding="utf-8",
        )

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertEqual([], errors)

    def test_rejects_protected_or_outside_allowlist_changes(self) -> None:
        self.write_contract(self.contract())
        (self.worktree / "docs/canon.md").write_text("changed\n", encoding="utf-8")

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertIn("protected path changed: docs/canon.md", errors)
        self.assertIn("changed path is outside write allowlist: docs/canon.md", errors)

    def test_rejects_unignored_worktree_parent(self) -> None:
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        self.write_contract(self.contract())

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertIn(".worktrees/ is not ignored by git", errors)

    def test_rejects_main_or_active_branch_as_external_task_branch(self) -> None:
        self.write_contract(self.contract(task_branch="main"))

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertTrue(any("task_branch" in error for error in errors), errors)

    def test_blocks_cleanup_when_result_is_dirty_or_not_integrated(self) -> None:
        self.write_contract(self.contract(cleanup_requested=True))
        (self.worktree / "drafts/external-ai/test/result.md").write_text(
            "dirty\n",
            encoding="utf-8",
        )

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertIn("cleanup requires integration_state APPROVED_INTEGRATED", errors)
        self.assertTrue(any("cleanup is blocked" in error for error in errors), errors)

    def test_allows_cleanup_only_after_approved_integration_and_clean_status(self) -> None:
        self.write_contract(
            self.contract(
                cleanup_requested=True,
                integration_state="APPROVED_INTEGRATED",
            )
        )
        (self.worktree / "drafts/external-ai/test/result.md").write_text(
            "reviewed\n",
            encoding="utf-8",
        )
        run_git(self.worktree, "add", ".")
        run_git(self.worktree, "commit", "-m", "external draft")

        errors = self.checker.validate_contract(self.root, self.contract_path)

        self.assertEqual([], errors)

    def test_skill_package_routes_to_machine_contract_and_evidence(self) -> None:
        package = (ROOT / "templates/ai/DEEPSEEK_WORK_PACKAGE.md").read_text(encoding="utf-8")
        evidence_index = json.loads(
            (ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json").read_text(encoding="utf-8")
        )
        entry = next(
            item
            for item in evidence_index["entries"]
            if item["skill_id"] == "orchestrating-deepseek-worktrees"
        )
        evidence_paths = {item["path"] for item in entry["evidence"]}
        generated = (ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("EXTERNAL_AI_WORKTREE_CONTRACT.json", package)
        self.assertIn("tools/check_external_ai_worktree_contract.py", package)
        self.assertIn("tools/check_external_ai_worktree_contract.py", evidence_paths)
        self.assertIn("tests/test_external_ai_worktree_contract.py", evidence_paths)
        row = next(
            line
            for line in generated.splitlines()
            if "`orchestrating-deepseek-worktrees`" in line
        )
        self.assertIn("EXECUTABLE_EVIDENCE", row)


if __name__ == "__main__":
    unittest.main()
