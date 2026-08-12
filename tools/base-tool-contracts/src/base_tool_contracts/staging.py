"""Race-resistant, Git-local staging directory creation for Base tools."""

from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
from contextlib import contextmanager
from typing import Iterator


class StagingViolation(ValueError):
    """Raised when local-only output cannot be proved confined and ignored."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9_-]+$")


def staging_identity(path: Path) -> tuple[int, int]:
    try:
        stat = path.stat(follow_symlinks=False)
    except OSError as error:
        raise StagingViolation("run output identity is unavailable") from error
    return stat.st_dev, stat.st_ino


@contextmanager
def stable_staging_path(project_root: Path, path: Path, expected_identity: tuple[int, int]) -> Iterator[Path]:
    """Hold a no-follow directory handle across mutable local tool work."""
    assert_verified_staging_path(project_root, path)
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise StagingViolation("run output directory cannot be opened without following links") from error
    try:
        stat = os.fstat(descriptor)
        if (stat.st_dev, stat.st_ino) != expected_identity:
            raise StagingViolation("run output directory identity changed after creation")
        alias = Path(f"/proc/self/fd/{descriptor}")
        if not alias.exists():
            raise StagingViolation("stable staging handles are unavailable on this operating system")
        yield alias
    finally:
        os.close(descriptor)


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
