"""Bounded, reviewed project discovery and transactional clone onboarding."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import threading
from typing import Callable

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry, ProjectRepositoryPointer
from base_tool_contracts.trusted_files import TrustedFileError, trusted_git_executable

from .projects import ProjectBindingError, ProjectLocator


_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)
_ACTIONS = {
    "REGISTERED": "연결됨",
    "FOUND_UNREGISTERED": "PC에서 찾기",
    "CLONE_AVAILABLE": "자동 설치 및 연결",
    "ONBOARDING": "설치 중",
}


@dataclass(frozen=True)
class OnboardingState:
    project_id: str
    local_state: str
    detail: str = ""

    def public_view(self) -> dict[str, str]:
        return {
            "project_id": self.project_id,
            "local_state": self.local_state,
            "action_label": _ACTIONS.get(self.local_state, "조치 필요"),
        }


CloneRunner = Callable[[str, Path], None]


class ProjectOnboardingService:
    def __init__(
        self,
        locator: ProjectLocator,
        registry: ProjectFigmaRegistry,
        *,
        managed_root: Path | None = None,
        home_root: Path | None = None,
        clone_runner: CloneRunner | None = None,
    ) -> None:
        self.locator = locator
        self.registry = registry
        home = Path(home_root or Path.home()).absolute()
        self.managed_root = Path(managed_root or (home / "Documents" / "GitHub")).absolute()
        self.home_root = home
        self._clone_runner = clone_runner or self._clone
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def _lock_for(self, project_id: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(project_id, threading.Lock())

    def _pointer(self, project_id: str) -> ProjectRepositoryPointer:
        try:
            return self.registry.repository_pointer(project_id)
        except DeliveryBlockedError as error:
            raise ProjectBindingError("PROJECT_CATALOG_ENTRY_REQUIRED") from error

    def _candidates(self, pointer: ProjectRepositoryPointer) -> tuple[Path, ...]:
        return (
            self.managed_root / pointer.repository_name,
            self.home_root / "source" / "repos" / pointer.repository_name,
        )

    @staticmethod
    def _is_link_or_reparse(path: Path) -> bool:
        try:
            metadata = path.lstat()
        except OSError:
            return False
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return stat.S_ISLNK(metadata.st_mode) or bool(
            reparse and getattr(metadata, "st_file_attributes", 0) & reparse
        )

    @staticmethod
    def _git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
        executable = trusted_git_executable()
        return subprocess.run(
            [str(executable), *_GIT_OVERRIDES, "-C", str(repository), *arguments],
            capture_output=True,
            check=False,
            env={
                "PATH": str(executable.parent),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )

    @staticmethod
    def _normalize_repository_url(value: str) -> str:
        return value.rstrip("/").removesuffix(".git").casefold()

    def _origin_matches(self, root: Path, pointer: ProjectRepositoryPointer) -> bool:
        try:
            completed = self._git(
                root,
                "config",
                "--local",
                "--no-includes",
                "--get",
                "remote.origin.url",
            )
        except TrustedFileError:
            return False
        if completed.returncode != 0:
            return False
        origin = completed.stdout.decode("utf-8", errors="replace").strip()
        return self._normalize_repository_url(origin) == self._normalize_repository_url(
            pointer.repository_url
        )

    def _found_candidate(self, pointer: ProjectRepositoryPointer) -> tuple[Path | None, str]:
        for candidate in self._candidates(pointer):
            if not candidate.exists() and not candidate.is_symlink():
                continue
            if self._is_link_or_reparse(candidate) or not candidate.is_dir():
                return None, "PATH_OCCUPIED"
            if not self._origin_matches(candidate, pointer):
                return None, "IDENTITY_MISMATCH"
            try:
                self.locator.inspect(candidate, pointer.project_id)
            except ProjectBindingError as error:
                code = str(error)
                if code == "PROJECT_ASSET_VAULT_MISSING":
                    return candidate, "PROJECT_SETUP_REQUIRED"
                return None, "IDENTITY_MISMATCH"
            return candidate, "FOUND_UNREGISTERED"
        return None, "CLONE_AVAILABLE"

    def status(self, project_id: str) -> OnboardingState:
        pointer = self._pointer(project_id)
        try:
            binding = self.locator.resolve(project_id)
        except ProjectBindingError:
            candidate, state = self._found_candidate(pointer)
            return OnboardingState(project_id, state, "candidate" if candidate else "")
        if not self._origin_matches(binding.root, pointer):
            return OnboardingState(project_id, "IDENTITY_MISMATCH")
        return OnboardingState(project_id, "REGISTERED")

    def _ensure_managed_root(self) -> None:
        self.managed_root.mkdir(parents=True, exist_ok=True)
        if self._is_link_or_reparse(self.managed_root) or not self.managed_root.is_dir():
            raise ProjectBindingError("PATH_OCCUPIED")

    def _ensure_vault(self, root: Path) -> None:
        probe = ".asset-vault/library/.hub-probe"
        ignored = self._git(root, "check-ignore", "-q", "--no-index", "--", probe)
        if ignored.returncode != 0:
            raise ProjectBindingError("PROJECT_SETUP_REQUIRED")
        (root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)

    def _clone(self, repository_url: str, destination: Path) -> None:
        executable = trusted_git_executable()
        environment = {
            "PATH": str(executable.parent),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        }
        for name in ("HOME", "USERPROFILE", "SYSTEMROOT", "COMSPEC", "TEMP", "TMP"):
            if value := os.environ.get(name):
                environment[name] = value
        completed = subprocess.run(
            [str(executable), *_GIT_OVERRIDES, "clone", "--origin", "origin", "--", repository_url, str(destination)],
            capture_output=True,
            check=False,
            shell=False,
            env=environment,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.decode("utf-8", errors="replace").casefold()
            if "authentication" in stderr or "permission denied" in stderr:
                raise ProjectBindingError("AUTHENTICATION_REQUIRED")
            raise ProjectBindingError("CLONE_FAILED")

    def onboard(self, project_id: str) -> OnboardingState:
        with self._lock_for(project_id):
            pointer = self._pointer(project_id)
            current = self.status(project_id)
            if current.local_state == "REGISTERED":
                return current
            candidate, found_state = self._found_candidate(pointer)
            if candidate is not None:
                try:
                    if found_state == "PROJECT_SETUP_REQUIRED":
                        self._ensure_vault(candidate)
                    self.locator.register(candidate, project_id)
                    return OnboardingState(project_id, "REGISTERED")
                except ProjectBindingError as error:
                    return OnboardingState(project_id, str(error))
            if found_state != "CLONE_AVAILABLE":
                return OnboardingState(project_id, found_state)

            staging: Path | None = None
            staging_identity: tuple[int, int] | None = None
            try:
                self.registry.assert_unchanged()
                self._ensure_managed_root()
                final = self.managed_root / pointer.repository_name
                if final.exists() or final.is_symlink():
                    return OnboardingState(project_id, "PATH_OCCUPIED")
                staging = Path(tempfile.mkdtemp(prefix=f".{pointer.repository_name}.onboard-", dir=self.managed_root))
                created = staging.lstat()
                staging_identity = (created.st_dev, created.st_ino)
                self._clone_runner(pointer.repository_url, staging)
                if not self._origin_matches(staging, pointer):
                    raise ProjectBindingError("IDENTITY_MISMATCH")
                self._ensure_vault(staging)
                self.locator.inspect(staging, project_id)
                os.rename(staging, final)
                staging = None
                self.locator.register(final, project_id)
                return OnboardingState(project_id, "REGISTERED")
            except ProjectBindingError as error:
                return OnboardingState(project_id, str(error))
            except (OSError, RuntimeError, TrustedFileError):
                return OnboardingState(project_id, "CLONE_FAILED")
            finally:
                if staging is not None and staging_identity is not None:
                    try:
                        current = staging.lstat()
                    except OSError:
                        current = None
                    if (
                        current is not None
                        and stat.S_ISDIR(current.st_mode)
                        and not self._is_link_or_reparse(staging)
                        and (current.st_dev, current.st_ino) == staging_identity
                    ):
                        shutil.rmtree(staging, ignore_errors=True)
