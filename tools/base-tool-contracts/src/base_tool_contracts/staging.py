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

from .trusted_files import TrustedFileError, read_regular_portable_nofollow, run_portable_git


class StagingViolation(ValueError):
    """Raised when local-only output cannot be proved confined and ignored."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9_-]+$")
_FILENAME = re.compile(r"^[A-Za-z0-9_.-]+$")
_MAX_PORTABLE_STAGING_READ_BYTES = 512 * 1024 * 1024
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400 if os.name == "nt" else 0)


def _is_reparse(metadata: os.stat_result) -> bool:
    return bool(_REPARSE_POINT and getattr(metadata, "st_file_attributes", 0) & _REPARSE_POINT)


def _portable_directory_identity(path: Path) -> tuple[int, int]:
    """Validate a normal directory chain on platforms without dir-fd no-follow operations."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    try:
        for part in absolute.parts[1:]:
            current = current / part
            metadata = current.lstat()
            if stat.S_ISLNK(metadata.st_mode) or _is_reparse(metadata):
                raise StagingViolation("staging directory path contains a link or reparse point")
            if not stat.S_ISDIR(metadata.st_mode):
                raise StagingViolation("staging directory path contains a non-directory")
    except OSError as error:
        raise StagingViolation("staging directory is unavailable") from error
    metadata = absolute.lstat()
    return metadata.st_dev, metadata.st_ino


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
    """Read one regular output without following its final link."""
    if not _FILENAME.fullmatch(filename) or filename in {".", ".."}:
        raise StagingViolation("staging input filename is invalid")
    if os.name == "nt":
        try:
            data, _ = read_regular_portable_nofollow(
                directory / filename,
                max_bytes=_MAX_PORTABLE_STAGING_READ_BYTES,
            )
        except TrustedFileError as error:
            raise StagingViolation("staging input must be a readable regular file") from error
        if expected_sha256 is not None and hashlib.sha256(data).hexdigest() != expected_sha256:
            raise StagingViolation("staging input SHA-256 does not match the generated evidence")
        return data

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


def confined_staging_read_bytes(project_root: Path, path: Path, *, expected_sha256: str | None = None) -> bytes:
    """Read one project-staged regular file through a no-follow component chain."""
    try:
        relative = path.relative_to(project_root)
    except ValueError as error:
        raise StagingViolation("staging input must remain under the project root") from error
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise StagingViolation("staging input path is invalid")

    if os.name == "nt":
        try:
            data, _ = read_regular_portable_nofollow(
                path,
                max_bytes=_MAX_PORTABLE_STAGING_READ_BYTES,
            )
        except TrustedFileError as error:
            raise StagingViolation("staging input path contains a link or unreadable component") from error
        if expected_sha256 is not None and hashlib.sha256(data).hexdigest() != expected_sha256:
            raise StagingViolation("staging input SHA-256 does not match the generated evidence")
        return data

    directory_descriptor = -1
    descriptor = -1
    try:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        directory_descriptor = os.open(project_root, directory_flags)
        for component in relative.parts[:-1]:
            next_descriptor = os.open(component, directory_flags, dir_fd=directory_descriptor)
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        descriptor = os.open(
            relative.parts[-1],
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=directory_descriptor,
        )
        attributes = os.fstat(descriptor)
        if not stat.S_ISREG(attributes.st_mode):
            raise StagingViolation("staging input must be a regular file without links")
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
        raise StagingViolation("staging input path contains a link or unreadable component") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if directory_descriptor >= 0:
            os.close(directory_descriptor)


def _portable_staging_write_bytes(directory: Path, filename: str, data: bytes) -> Path:
    directory_identity = _portable_directory_identity(directory)
    target = directory / filename
    try:
        existing = target.lstat()
    except FileNotFoundError:
        pass
    except OSError as error:
        raise StagingViolation("staging output could not be inspected safely") from error
    else:
        if stat.S_ISLNK(existing.st_mode) or _is_reparse(existing) or not stat.S_ISREG(existing.st_mode):
            raise StagingViolation("staging output must be a regular file")
        try:
            target.unlink()
        except OSError as error:
            raise StagingViolation("staging output could not be replaced safely") from error
        if _portable_directory_identity(directory) != directory_identity:
            raise StagingViolation("staging output directory identity changed before write")

    descriptor = -1
    try:
        descriptor = os.open(
            target,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_BINARY", 0),
            0o600,
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
        named_attributes = target.lstat()
        if (
            stat.S_ISLNK(named_attributes.st_mode)
            or _is_reparse(named_attributes)
            or not stat.S_ISREG(named_attributes.st_mode)
            or (opened_attributes.st_dev, opened_attributes.st_ino)
            != (named_attributes.st_dev, named_attributes.st_ino)
        ):
            raise StagingViolation("staging output identity changed during write")
        if _portable_directory_identity(directory) != directory_identity:
            raise StagingViolation("staging output directory identity changed during write")
        return target
    except OSError as error:
        raise StagingViolation("staging output could not be written safely") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def safe_staging_write_bytes(directory: Path, filename: str, data: bytes) -> Path:
    """Publish a fresh regular-file inode and never write through an existing entry."""
    if not _FILENAME.fullmatch(filename) or filename in {".", ".."}:
        raise StagingViolation("staging output filename is invalid")
    if os.name == "nt":
        return _portable_staging_write_bytes(directory, filename, data)

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
        attributes = path.stat(follow_symlinks=False)
    except OSError as error:
        raise StagingViolation("run output identity is unavailable") from error
    return attributes.st_dev, attributes.st_ino


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
            attributes = os.fstat(descriptor)
            if expected_identity is not None and (attributes.st_dev, attributes.st_ino) != expected_identity:
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


@dataclass
class PortableStableStagingTree:
    """Path-identity-backed Windows view for a developer-owned local workspace."""

    _run_path: Path
    _run_identity: tuple[int, int]

    @property
    def run_dir(self) -> Path:
        if _portable_directory_identity(self._run_path) != self._run_identity:
            raise StagingViolation("run output directory identity changed after creation")
        return self._run_path

    def open_directory(
        self,
        relative_path: str,
        *,
        create: bool = False,
        expected_identity: tuple[int, int] | None = None,
    ) -> Path:
        relative = Path(relative_path)
        if relative.is_absolute() or not relative.parts or any(
            part in {"", ".", ".."} or not _IDENTIFIER.fullmatch(part)
            for part in relative.parts
        ):
            raise StagingViolation("stable staging subdirectory is invalid")
        current = self.run_dir
        for component in relative.parts:
            current = current / component
            if create:
                try:
                    current.mkdir()
                except FileExistsError:
                    pass
            identity = _portable_directory_identity(current)
        if expected_identity is not None and identity != expected_identity:
            raise StagingViolation("stable staging subdirectory identity changed after creation")
        return current

    def close(self) -> None:
        return None


@contextmanager
def stable_staging_tree(
    project_root: Path,
    path: Path,
    expected_identity: tuple[int, int],
) -> Iterator[StableStagingTree | PortableStableStagingTree]:
    """Hold or revalidate one run and its mutable descendants during local tool work."""
    assert_verified_staging_path(project_root, path)
    if os.name == "nt":
        tree = PortableStableStagingTree(path, expected_identity)
        if _portable_directory_identity(path) != expected_identity:
            raise StagingViolation("run output directory identity changed after creation")
        try:
            yield tree
        finally:
            tree.close()
        return

    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise StagingViolation("run output directory cannot be opened without following links") from error
    tree = StableStagingTree(descriptor)
    try:
        attributes = os.fstat(descriptor)
        if (attributes.st_dev, attributes.st_ino) != expected_identity:
            raise StagingViolation("run output directory identity changed after creation")
        _descriptor_alias(descriptor)
        yield tree
    finally:
        tree.close()
        os.close(descriptor)


@contextmanager
def stable_staging_path(project_root: Path, path: Path, expected_identity: tuple[int, int]) -> Iterator[Path]:
    """Hold a no-follow directory handle across mutable local tool work where supported."""
    with stable_staging_tree(project_root, path, expected_identity) as tree:
        yield tree.run_dir


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        try:
            completed = run_portable_git(root, *arguments)
        except TrustedFileError as error:
            raise StagingViolation("project asset vault requires trusted Git") from error
        return subprocess.CompletedProcess(
            completed.args,
            completed.returncode,
            completed.stdout.decode("utf-8", errors="replace"),
            completed.stderr.decode("utf-8", errors="replace"),
        )
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
    if os.name == "nt":
        base_identity = _portable_directory_identity(base)
        current = base
        for index, component in enumerate(components):
            current = current / component
            try:
                current.mkdir()
            except FileExistsError:
                if final_must_be_new and index == len(components) - 1:
                    raise StagingViolation("run output directory already exists")
            _portable_directory_identity(current)
        if _portable_directory_identity(base) != base_identity:
            raise StagingViolation("project asset vault library identity changed during directory creation")
        return

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
    if os.name == "nt":
        _portable_directory_identity(library)
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
            attributes = current.stat(follow_symlinks=False)
            if _is_reparse(attributes):
                raise StagingViolation("run output path contains a reparse point")
    resolved = path.resolve()
    if library.resolve() not in resolved.parents or not resolved.is_dir():
        raise StagingViolation("run output is not a directory inside the verified asset vault")
    _verify_project_gitignore(root, relative / ".staging-ignore-probe")
    _verify_not_protected(root, relative)