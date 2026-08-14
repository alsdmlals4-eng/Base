"""Descriptor-bound reads for local contract files."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import stat
import subprocess


class TrustedFileError(ValueError):
    pass


@dataclass(frozen=True)
class FileIdentity:
    device: int
    inode: int
    mode: int


_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=/dev/null",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)


def _parts(path: Path) -> tuple[str, ...]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    if not absolute.is_absolute():
        raise TrustedFileError("path must be absolute")
    return absolute.parts[1:]


def open_directory_nofollow(path: Path) -> int:
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    if not nofollow:
        raise TrustedFileError("component-safe reads are unavailable")
    descriptor = os.open(
        os.path.sep,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        for part in _parts(path):
            next_descriptor = os.open(
                part,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_CLOEXEC", 0)
                | nofollow,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
        metadata = os.fstat(descriptor)
        if not stat.S_ISDIR(metadata.st_mode):
            raise TrustedFileError("path is not a directory")
        return descriptor
    except (OSError, TrustedFileError) as error:
        os.close(descriptor)
        if isinstance(error, TrustedFileError):
            raise
        raise TrustedFileError("directory is unavailable or crosses a symlink") from error


def open_directory_at_nofollow(root_descriptor: int, relative: Path) -> int:
    """Open a relative directory chain without following any component links."""
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise TrustedFileError("relative directory path is invalid")
    descriptor = os.dup(root_descriptor)
    try:
        for part in relative.parts:
            next_descriptor = os.open(
                part,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
        metadata = os.fstat(descriptor)
        if not stat.S_ISDIR(metadata.st_mode):
            raise TrustedFileError("path is not a directory")
        return descriptor
    except (OSError, TrustedFileError) as error:
        os.close(descriptor)
        if isinstance(error, TrustedFileError):
            raise
        raise TrustedFileError("directory is unavailable or crosses a symlink") from error


def read_regular_at(
    root_descriptor: int,
    relative: Path,
    *,
    max_bytes: int = 4 * 1024 * 1024,
) -> tuple[bytes, FileIdentity]:
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise TrustedFileError("relative contract path is invalid")
    descriptor = os.dup(root_descriptor)
    try:
        for part in relative.parts[:-1]:
            next_descriptor = os.open(
                part,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
        file_descriptor = os.open(
            relative.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=descriptor,
        )
        try:
            metadata = os.fstat(file_descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_bytes:
                raise TrustedFileError("contract file is not a bounded regular file")
            chunks: list[bytes] = []
            remaining = max_bytes + 1
            while remaining:
                chunk = os.read(file_descriptor, min(1024 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            if len(raw) > max_bytes:
                raise TrustedFileError("contract file exceeds its size limit")
            return raw, FileIdentity(metadata.st_dev, metadata.st_ino, metadata.st_mode)
        finally:
            os.close(file_descriptor)
    except OSError as error:
        raise TrustedFileError("contract file is unavailable or crosses a symlink") from error
    finally:
        os.close(descriptor)


def read_regular_nofollow(path: Path, *, max_bytes: int = 4 * 1024 * 1024) -> tuple[bytes, FileIdentity]:
    parent = open_directory_nofollow(Path(path).absolute().parent)
    try:
        return read_regular_at(parent, Path(Path(path).name), max_bytes=max_bytes)
    finally:
        os.close(parent)


def read_regular_portable_nofollow(
    path: Path,
    *,
    max_bytes: int = 4 * 1024 * 1024,
) -> tuple[bytes, FileIdentity]:
    """Bounded fallback for platforms without descriptor-relative no-follow opens.

    The local OS account remains trusted, but every component must be a normal
    path, Windows reparse points are rejected, and the final file identity must
    remain stable across the one read.
    """
    absolute = Path(os.path.abspath(os.fspath(path)))
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    current = Path(absolute.anchor)
    try:
        for index, part in enumerate(absolute.parts[1:]):
            current = current / part
            metadata = current.lstat()
            if stat.S_ISLNK(metadata.st_mode) or (
                reparse_flag and getattr(metadata, "st_file_attributes", 0) & reparse_flag
            ):
                raise TrustedFileError("contract path crosses a link or reparse point")
            if index < len(absolute.parts[1:]) - 1 and not stat.S_ISDIR(metadata.st_mode):
                raise TrustedFileError("contract parent is not a directory")
        before = current.lstat()
        if not stat.S_ISREG(before.st_mode) or before.st_size > max_bytes:
            raise TrustedFileError("contract file is not a bounded regular file")
        descriptor = os.open(current, os.O_RDONLY | getattr(os, "O_BINARY", 0))
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                raise TrustedFileError("contract file changed before it was opened")
            chunks: list[bytes] = []
            remaining = max_bytes + 1
            while remaining:
                chunk = os.read(descriptor, min(1024 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
        finally:
            os.close(descriptor)
        after = current.lstat()
    except OSError as error:
        raise TrustedFileError("contract file is unavailable or crosses a link") from error
    if (
        len(raw) > max_bytes
        or (before.st_dev, before.st_ino, before.st_size)
        != (after.st_dev, after.st_ino, after.st_size)
    ):
        raise TrustedFileError("contract file changed while it was read")
    return raw, FileIdentity(opened.st_dev, opened.st_ino, opened.st_mode)


def run_portable_git(root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    """Run fixed Git arguments for catalog proof on non-POSIX platforms."""
    candidate = shutil.which("git")
    if not candidate:
        raise TrustedFileError("trusted Git executable is unavailable")
    executable = Path(candidate).absolute()
    metadata = executable.lstat()
    if executable.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise TrustedFileError("trusted Git executable must be a regular non-symlink file")
    overrides = (
        "-c", "core.fsmonitor=false",
        "-c", "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
        "-c", "filter.lfs.required=false",
        "-c", "filter.lfs.smudge=cat",
        "-c", "filter.lfs.clean=cat",
    )
    return subprocess.run(
        [str(executable), *overrides, "-C", str(root), *arguments],
        capture_output=True,
        check=False,
        env={
            "PATH": str(executable.parent),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )


def trusted_git_executable() -> Path:
    candidate = shutil.which("git", path=os.defpath)
    if not candidate:
        raise TrustedFileError("trusted Git executable is unavailable")
    path = Path(candidate).absolute()
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise TrustedFileError("trusted Git executable must be a regular non-symlink file")
    return path


def normalized_line_endings(raw: bytes) -> bytes:
    """Normalize checkout-only CRLF differences without hiding other edits."""
    return raw.replace(b"\r\n", b"\n")


def run_trusted_git(root_descriptor: int, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    """Run fixed Git against the exact open repository directory."""
    if not Path("/proc/self/fd").is_dir():
        raise TrustedFileError("descriptor-bound Git is unavailable")
    executable = trusted_git_executable()
    root_alias = Path(f"/proc/self/fd/{root_descriptor}")
    return subprocess.run(
        [str(executable), *_GIT_OVERRIDES, "-C", str(root_alias), *arguments],
        capture_output=True,
        check=False,
        pass_fds=(root_descriptor,),
        env={
            "PATH": os.defpath,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C.UTF-8",
        },
    )
