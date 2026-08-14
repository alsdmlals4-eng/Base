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
