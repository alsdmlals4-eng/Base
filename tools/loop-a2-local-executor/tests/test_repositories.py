from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.repositories import ManagedRepositoryError, ManagedRepositoryStore


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=True)
    return completed.stdout.strip()


class ManagedRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "seed"
        self.user_checkout = self.root / "user-checkout"
        self.state = self.root / "executor-state"
        git(self.root, "init", "--bare", str(self.remote))
        self.seed.mkdir()
        git(self.seed, "init", "-b", "main")
        git(self.seed, "config", "user.name", "Loop Test")
        git(self.seed, "config", "user.email", "loop@example.invalid")
        (self.seed / "README.md").write_text("baseline\n", encoding="utf-8")
        git(self.seed, "add", "README.md")
        git(self.seed, "commit", "-m", "baseline")
        self.sha = git(self.seed, "rev-parse", "HEAD")
        git(self.seed, "remote", "add", "origin", str(self.remote))
        git(self.seed, "push", "-u", "origin", "main")
        git(self.root, "clone", str(self.remote), str(self.user_checkout))
        (self.user_checkout / "user-note.txt").write_text("keep me\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def store(self) -> ManagedRepositoryStore:
        return ManagedRepositoryStore(
            state_root=self.state,
            repository_sources={"example/Project": str(self.remote)},
        )

    def test_clone_and_reuse_verify_exact_origin(self) -> None:
        store = self.store()
        first = store.ensure_repo("example/Project")
        second = store.ensure_repo("example/Project")
        self.assertEqual(first, second)
        self.assertEqual(git(first, "remote", "get-url", "origin"), str(self.remote))

    def test_wrong_origin_reuse_fails_closed(self) -> None:
        store = self.store()
        repo = store.ensure_repo("example/Project")
        git(repo, "remote", "set-url", "origin", str(self.root / "other.git"))
        with self.assertRaises(ManagedRepositoryError) as caught:
            store.ensure_repo("example/Project")
        self.assertEqual(caught.exception.code, "MANAGED_REPOSITORY_ORIGIN_MISMATCH")

    def test_exact_sha_worktree_is_detached_and_removed(self) -> None:
        store = self.store()
        repo = store.ensure_repo("example/Project")
        with store.exact_worktree("example/Project", self.sha, "authority") as worktree:
            self.assertTrue(worktree.is_dir())
            self.assertEqual(git(worktree, "rev-parse", "HEAD"), self.sha)
            self.assertEqual(git(worktree, "rev-parse", "--abbrev-ref", "HEAD"), "HEAD")
            self.assertTrue(str(worktree.resolve()).startswith(str((self.state / "worktrees").resolve())))
        self.assertFalse(worktree.exists())
        self.assertTrue(repo.exists())

    def test_unknown_sha_fails_before_worktree_creation(self) -> None:
        store = self.store()
        with self.assertRaises(ManagedRepositoryError) as caught:
            with store.exact_worktree("example/Project", "f" * 40, "authority"):
                pass
        self.assertEqual(caught.exception.code, "MANAGED_REPOSITORY_SHA_UNAVAILABLE")

    def test_executor_never_mutates_separate_user_checkout(self) -> None:
        before = git(self.user_checkout, "status", "--porcelain")
        store = self.store()
        with store.exact_worktree("example/Project", self.sha, "authority") as worktree:
            (worktree / "README.md").write_text("candidate\n", encoding="utf-8")
        after = git(self.user_checkout, "status", "--porcelain")
        self.assertEqual(before, after)
        self.assertTrue((self.user_checkout / "user-note.txt").is_file())

    def test_unconfigured_repository_is_rejected(self) -> None:
        with self.assertRaises(ManagedRepositoryError) as caught:
            self.store().ensure_repo("other/Project")
        self.assertEqual(caught.exception.code, "MANAGED_REPOSITORY_UNTRUSTED")


if __name__ == "__main__":
    unittest.main()
