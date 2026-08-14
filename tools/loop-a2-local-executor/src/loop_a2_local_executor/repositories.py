from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import subprocess
from typing import Iterator, Mapping
import uuid


_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", f"core.hooksPath={os.devnull}",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)


class ManagedRepositoryError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


def _git_environment() -> dict[str, str]:
    result = {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }
    for key in ("PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "HOME", "USERPROFILE"):
        value = os.environ.get(key)
        if value:
            result[key] = value
    return result


class ManagedRepositoryStore:
    def __init__(
        self,
        *,
        state_root: Path,
        repository_sources: Mapping[str, str],
        git_executable: str = "git",
    ) -> None:
        self.state_root = Path(state_root).resolve(strict=False)
        self.repositories_root = self.state_root / "repositories"
        self.worktrees_root = self.state_root / "worktrees"
        self.runtime_root = self.state_root / "a2-runtime"
        self.sources = dict(repository_sources)
        self.git_executable = git_executable

    def _source(self, repository: str) -> str:
        source = self.sources.get(repository)
        if not isinstance(source, str) or not source:
            raise ManagedRepositoryError("MANAGED_REPOSITORY_UNTRUSTED", "repository has no configured trusted source")
        return source

    def _repo_path(self, repository: str) -> Path:
        if repository.count("/") != 1:
            raise ManagedRepositoryError("MANAGED_REPOSITORY_UNTRUSTED", "repository identity is invalid")
        owner, name = repository.split("/", 1)
        if any(value in {"", ".", ".."} for value in (owner, name)):
            raise ManagedRepositoryError("MANAGED_REPOSITORY_UNTRUSTED", "repository identity is invalid")
        return self.repositories_root / owner / name

    def _git(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                [self.git_executable, *_GIT_OVERRIDES, *args],
                cwd=cwd,
                text=True,
                capture_output=True,
                env=_git_environment(),
                shell=False,
                check=False,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ManagedRepositoryError("MANAGED_GIT_EXECUTION_FAILED", "Git operation could not complete") from exc

    def _origin(self, repo: Path) -> str | None:
        completed = self._git(repo, "config", "--local", "--no-includes", "--get", "remote.origin.url")
        return completed.stdout.strip() if completed.returncode == 0 else None

    def ensure_repo(self, repository: str) -> Path:
        source = self._source(repository)
        destination = self._repo_path(repository)
        if destination.exists():
            if not destination.is_dir() or self._origin(destination) != source:
                raise ManagedRepositoryError("MANAGED_REPOSITORY_ORIGIN_MISMATCH", "managed repository origin differs")
            return destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        completed = self._git(
            destination.parent,
            "clone", "--no-checkout", "--origin", "origin", "--", source, str(destination),
        )
        if completed.returncode != 0:
            if destination.exists():
                shutil.rmtree(destination, ignore_errors=True)
            raise ManagedRepositoryError("MANAGED_REPOSITORY_CLONE_FAILED", "managed repository clone failed")
        if self._origin(destination) != source:
            shutil.rmtree(destination, ignore_errors=True)
            raise ManagedRepositoryError("MANAGED_REPOSITORY_ORIGIN_MISMATCH", "cloned repository origin differs")
        return destination

    def _refresh(self, repo: Path) -> None:
        completed = self._git(
            repo,
            "fetch", "--prune", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main",
        )
        if completed.returncode != 0:
            raise ManagedRepositoryError("MANAGED_REPOSITORY_FETCH_FAILED", "managed repository main refresh failed")

    def _has_sha(self, repo: Path, sha: str) -> bool:
        completed = self._git(repo, "cat-file", "-e", f"{sha}^{{commit}}")
        return completed.returncode == 0

    @contextmanager
    def exact_worktree(self, repository: str, sha: str, role: str) -> Iterator[Path]:
        if len(sha) != 40 or any(character not in "0123456789abcdef" for character in sha):
            raise ManagedRepositoryError("MANAGED_REPOSITORY_SHA_INVALID", "exact SHA must be lowercase 40-hex")
        if not role or any(character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" for character in role):
            raise ManagedRepositoryError("MANAGED_WORKTREE_ROLE_INVALID", "worktree role is invalid")
        repo = self.ensure_repo(repository)
        self._refresh(repo)
        if not self._has_sha(repo, sha):
            raise ManagedRepositoryError("MANAGED_REPOSITORY_SHA_UNAVAILABLE", "requested exact SHA is unavailable")
        owner, name = repository.split("/", 1)
        worktree = self.worktrees_root / role / owner / name / f"{sha[:12]}-{uuid.uuid4().hex[:12]}"
        worktree.parent.mkdir(parents=True, exist_ok=True)
        created = False
        try:
            completed = self._git(repo, "worktree", "add", "--detach", str(worktree), sha)
            if completed.returncode != 0:
                raise ManagedRepositoryError("MANAGED_WORKTREE_CREATE_FAILED", "exact detached worktree creation failed")
            created = True
            resolved = worktree.resolve(strict=True)
            if self.worktrees_root.resolve(strict=False) not in resolved.parents:
                raise ManagedRepositoryError("MANAGED_WORKTREE_PATH_UNSAFE", "worktree escaped executor state root")
            head = self._git(resolved, "rev-parse", "HEAD")
            if head.returncode != 0 or head.stdout.strip() != sha:
                raise ManagedRepositoryError("MANAGED_WORKTREE_SHA_MISMATCH", "created worktree head differs")
            yield resolved
        finally:
            if created:
                self._git(repo, "worktree", "remove", "--force", str(worktree))
                self._git(repo, "worktree", "prune")
            if worktree.exists():
                shutil.rmtree(worktree, ignore_errors=True)
