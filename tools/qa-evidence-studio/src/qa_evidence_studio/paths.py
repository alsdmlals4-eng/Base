"""Cross-platform local-only session paths and atomic file publication."""

from __future__ import annotations

import os
from pathlib import Path
import secrets
import stat
import subprocess


class QaPathError(ValueError):
    pass


_REPARSE_POINT = 0x400


def _is_link_or_reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as error:
        raise QaPathError("QA storage path is unreadable") from error
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & _REPARSE_POINT)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def prepare_session_directory(project_root: Path, session_id: str) -> Path:
    root = project_root.resolve()
    top = _git(root, "rev-parse", "--show-toplevel")
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root:
        raise QaPathError("project_root must be the exact Git worktree root")
    if _git(root, "ls-files", "--", ".asset-vault").stdout.strip():
        raise QaPathError("project Asset Vault must not contain tracked files")
    relative = Path(".asset-vault", "library", "generated", "qa-evidence-studio", session_id)
    ignored = _git(root, "check-ignore", "-q", "--no-index", "--", (relative / ".probe").as_posix())
    if ignored.returncode != 0:
        raise QaPathError("QA evidence output must be gitignored by the project")
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists():
            if not current.is_dir() or _is_link_or_reparse(current):
                raise QaPathError("QA storage path contains a link, reparse point, or non-directory")
        else:
            current.mkdir()
            if _is_link_or_reparse(current):
                raise QaPathError("QA storage directory identity is unsafe")
    evidence = current / "evidence"
    evidence.mkdir()
    if _is_link_or_reparse(evidence):
        raise QaPathError("QA evidence directory identity is unsafe")
    return current


def assert_session_directory(project_root: Path, session_dir: Path) -> None:
    root = project_root.resolve()
    resolved = session_dir.resolve()
    if root not in resolved.parents:
        raise QaPathError("QA session escaped the project root")
    current = root
    for part in session_dir.relative_to(root).parts:
        current = current / part
        if not current.is_dir() or _is_link_or_reparse(current):
            raise QaPathError("QA session path identity changed")


def atomic_write_bytes(directory: Path, filename: str, data: bytes) -> Path:
    if not filename or filename in {".", ".."} or Path(filename).name != filename:
        raise QaPathError("QA output filename is invalid")
    if not directory.exists() or not directory.is_dir() or _is_link_or_reparse(directory):
        raise QaPathError("QA output directory is a link, reparse point, or non-directory")
    temporary = directory / f".{filename}.{secrets.token_hex(8)}.tmp"
    target = directory / filename
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if target.exists() and _is_link_or_reparse(target):
            raise QaPathError("QA output target is a link or reparse point")
        os.replace(temporary, target)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return target
