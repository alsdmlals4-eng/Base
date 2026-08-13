"""Race-resistant, Git-local staging directory creation for Base tools."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import stat
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterator


class StagingViolation(ValueError):
    """Raised when local-only output cannot be proved confined and ignored."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9_-]+$")
_FILENAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def _open_staging_directory(directory: Path) -> int:
    parts = directory.parts
    if len(parts) == 5 and parts[:4] == ("/", "proc", "self", "fd") and parts[4].isdigit():
        descriptor = os.dup(int(parts[4]))
        if not os.path.isdir(f"/proc/self/fd/{descriptor}"):
            os.close(descriptor)
            raise OSError("descriptor is not a directory")
        return descriptor
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    return os.open(directory, flags)


def staging_read_bytes(directory: Path, filename: str, *, expected_sha256: str | None = None) -> bytes:
    """Read one regular output through a fixed directory fd without following its final symlink."""
    if not _FILENAME.fullmatch(filename) or filename in {".", ".."}:
        raise StagingViolation("staging input filename is invalid")
    directory_descriptor = -1
    descriptor = -1
    try:
        directory_descriptor = _open_staging_directory(directory)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(filename, flags, dir_fd=directory_descriptor)
        attributes = os.fstat(descriptor)
        if not stat.S_ISREG(attributes.st_mode):
            raise StagingViolation("staging input must be a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        data = b"".join(chunks)
        if expected_sha256 is not None and hashlib.sha256(data).hexdigest() != expected_sha256:
            raise StagingViolation("staging input SHA-256 does not match the generated evidence")
        return data
    except OSError as error:
        raise StagingViolation("staging input must be a readable regular file") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if directory_descriptor >= 0:
            os.close(directory_descriptor)


def safe_staging_write_bytes(directory: Path, filename: str, data: bytes) -> Path:
    """Publish a fresh regular-file inode and never write through an existing entry."""
    if not _FILENAME.fullmatch(filename) or filename in {".", ".."}:
        raise StagingViolation("staging output filename is invalid")
    try:
        directory_descriptor = _open_staging_directory(directory)
    except OSError as error:
        raise StagingViolation("staging output directory is unavailable") from error
    descriptor = -1
    try:
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        try:
            existing = os.stat(filename, dir_fd=directory_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if not stat.S_ISREG(existing.st_mode):
                raise StagingViolation("staging output must be a regular file")
            os.unlink(filename, dir_fd=directory_descriptor)
        descriptor = os.open(
            filename,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
            0o600,
            dir_fd=directory_descriptor,
        )
        opened_attributes = os.fstat(descriptor)
        if not stat.S_ISREG(opened_attributes.st_mode):
            raise StagingViolation("staging output must be a regular file")
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise StagingViolation("staging output write did not make progress")
            view = view[written:]
        os.fsync(descriptor)
        named_attributes = os.stat(filename, dir_fd=directory_descriptor, follow_symlinks=False)
        if not stat.S_ISREG(named_attributes.st_mode) or (
            opened_attributes.st_dev,
            opened_attributes.st_ino,
        ) != (named_attributes.st_dev, named_attributes.st_ino):
            raise StagingViolation("staging output identity changed during write")
        os.close(descriptor)
        descriptor = -1
        return directory / filename
    except OSError as error:
        raise StagingViolation("staging output could not be written safely") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(directory_descriptor)


def safe_staging_write_text(directory: Path, filename: str, text: str) -> Path:
    return safe_staging_write_bytes(directory, filename, text.encode("utf-8"))


def staging_identity(path: Path) -> tuple[int, int]:
    try:
        stat = path.stat(follow_symlinks=False)
    except OSError as error:
        raise StagingViolation("run output identity is unavailable") from error
    return stat.st_dev, stat.st_ino


def _descriptor_alias(descriptor: int) -> Path:
    alias = Path(f"/proc/self/fd/{descriptor}")
    if not alias.exists():
        raise StagingViolation("stable staging handles are unavailable on this operating system")
    return alias


@dataclass
class StableStagingTree:
    """Directory-handle-backed view of one run and its mutable descendants."""

    _run_descriptor: int
    _descriptors: list[int] = field(default_factory=list)

    @property
    def run_dir(self) -> Path:
        return _descriptor_alias(self._run_descriptor)

    def open_directory(
        self,
        relative_path: str,
        *,
        create: bool = False,
        expected_identity: tuple[int, int] | None = None,
    ) -> Path:
        """Open each component without following links and hold the final handle."""
        relative = Path(relative_path)
        if relative.is_absolute() or not relative.parts or any(
            part in {"", ".", ".."} or not _IDENTIFIER.fullmatch(part)
            for part in relative.parts
        ):
            raise StagingViolation("stable staging subdirectory is invalid")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.dup(self._run_descriptor)
        try:
            for component in relative.parts:
                if create:
                    try:
                        os.mkdir(component, dir_fd=descriptor)
                    except FileExistsError:
                        pass
                try:
                    next_descriptor = os.open(component, flags, dir_fd=descriptor)
                except OSError as error:
                    raise StagingViolation("stable staging path contains a link or non-directory") from error
                os.close(descriptor)
                descriptor = next_descriptor
            stat = os.fstat(descriptor)
            if expected_identity is not None and (stat.st_dev, stat.st_ino) != expected_identity:
                raise StagingViolation("stable staging subdirectory identity changed after creation")
            alias = _descriptor_alias(descriptor)
            self._descriptors.append(descriptor)
            descriptor = -1
            return alias
        finally:
            if descriptor >= 0:
                os.close(descriptor)

    def close(self) -> None:
        while self._descriptors:
            os.close(self._descriptors.pop())


@contextmanager
def stable_staging_tree(
    project_root: Path,
    path: Path,
    expected_identity: tuple[int, int],
) -> Iterator[StableStagingTree]:
    """Hold a run handle and any explicitly opened child handles during mutable work."""
    assert_verified_staging_path(project_root, path)
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise StagingViolation("run output directory cannot be opened without following links") from error
    tree = StableStagingTree(descriptor)
    try:
        stat = os.fstat(descriptor)
        if (stat.st_dev, stat.st_ino) != expected_identity:
            raise StagingViolation("run output directory identity changed after creation")
        _descriptor_alias(descriptor)
        yield tree
    finally:
        tree.close()
        os.close(descriptor)


@contextmanager
def stable_staging_path(project_root: Path, path: Path, expected_identity: tuple[int, int]) -> Iterator[Path]:
    """Hold a no-follow directory handle across mutable local tool work."""
    with stable_staging_tree(project_root, path, expected_identity) as tree:
        yield tree.run_dir


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)


def _verify_project_gitignore(root: Path, relative_probe: Path) -> None:
    tracked = _git(root, "ls-files", "--", ".asset-vault")
    if tracked.returncode != 0:
        raise StagingViolation("project asset vault requires a readable Git worktree")
    if tracked.stdout.strip():
        raise StagingViolation("project asset vault must not contain tracked files")
    ignored = _git(root, "check-ignore", "-v", "--no-index", "--", relative_probe.as_posix())
    if ignored.returncode != 0:
        raise StagingViolation("project asset vault output must be effectively gitignored")
    source = ignored.stdout.split("\t", 1)[0]
    if not (source.startswith(".gitignore:") or source.startswith(str(root / ".gitignore") + ":")):
        raise StagingViolation("project asset vault ignore rule must come from the project .gitignore")


def _verify_not_protected(root: Path, relative: Path) -> None:
    adapter = root / "skills" / "PROJECT_BASE_ADAPTER.json"
    if not adapter.is_file():
        return
    try:
        payload = json.loads(adapter.read_text(encoding="utf-8"))
        patterns = payload["protected_paths"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise StagingViolation("canonical project adapter protected paths are unreadable") from error
    if not isinstance(patterns, list) or any(not isinstance(item, str) for item in patterns):
        raise StagingViolation("canonical project adapter protected paths are invalid")
    candidate = relative.as_posix()
    if any(fnmatch.fnmatchcase(candidate, pattern) for pattern in patterns):
        raise StagingViolation("project asset vault output collides with a protected path")


def _mkdir_chain_nofollow(base: Path, components: tuple[str, ...], *, final_must_be_new: bool) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(base, flags)
    except OSError as error:
        raise StagingViolation("project asset vault library must exist and must not be a symlink") from error
    try:
        for index, component in enumerate(components):
            try:
                os.mkdir(component, dir_fd=descriptor)
            except FileExistsError:
                if final_must_be_new and index == len(components) - 1:
                    raise StagingViolation("run output directory already exists")
            try:
                next_descriptor = os.open(component, flags, dir_fd=descriptor)
            except OSError as error:
                raise StagingViolation("project asset vault path contains a symlink or non-directory") from error
            os.close(descriptor)
            descriptor = next_descriptor
    finally:
        os.close(descriptor)


def create_verified_run_directories(project_root: Path, *, dynamic_components: tuple[str, ...], leaf_directories: tuple[str, ...]) -> tuple[Path, tuple[Path, ...]]:
    """Create one run without following any attacker-controlled directory symlink."""
    if any(not _IDENTIFIER.fullmatch(value) for value in dynamic_components + leaf_directories):
        raise StagingViolation("run identifiers must contain only letters, numbers, hyphens, or underscores")
    root = project_root.resolve()
    library = root / ".asset-vault" / "library"
    if not library.is_dir() or library.is_symlink():
        raise StagingViolation("project asset vault library must exist and must not be a symlink")
    repository = _git(root, "rev-parse", "--show-toplevel")
    if repository.returncode != 0 or Path(repository.stdout.strip()).resolve() != root:
        raise StagingViolation("project asset vault requires project_root to be the Git worktree root")
    run_relative = Path(".asset-vault", "library", *dynamic_components)
    probe = run_relative / ".staging-ignore-probe"
    _verify_project_gitignore(root, probe)
    _verify_not_protected(root, run_relative)
    _mkdir_chain_nofollow(library, dynamic_components, final_must_be_new=True)
    run_dir = library / Path(*dynamic_components)
    for leaf in leaf_directories:
        _mkdir_chain_nofollow(run_dir, (leaf,), final_must_be_new=True)
    resolved = run_dir.resolve()
    if library.resolve() not in resolved.parents:
        raise StagingViolation("project asset vault output escaped the verified library")
    _verify_project_gitignore(root, probe)
    _verify_not_protected(root, run_relative)
    return run_dir, tuple(run_dir / leaf for leaf in leaf_directories)


def assert_verified_staging_path(project_root: Path, path: Path) -> None:
    """Revalidate an existing vault path before and after mutable engine/export work."""
    root = project_root.resolve()
    library = root / ".asset-vault" / "library"
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise StagingViolation("run output escaped the project workspace") from error
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise StagingViolation("run output path contains a symlink")
        if current.exists():
            attributes = getattr(current.stat(follow_symlinks=False), "st_file_attributes", 0)
            if attributes & 0x400:
                raise StagingViolation("run output path contains a reparse point")
    resolved = path.resolve()
    if library.resolve() not in resolved.parents or not resolved.is_dir():
        raise StagingViolation("run output is not a directory inside the verified asset vault")
    _verify_project_gitignore(root, relative / ".staging-ignore-probe")
    _verify_not_protected(root, relative)
