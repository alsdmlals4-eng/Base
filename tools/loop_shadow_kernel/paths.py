from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:/")


class UnsafePath(ValueError):
    pass


class UnsafeSymlink(UnsafePath):
    pass


@dataclass(frozen=True, slots=True)
class ConfinedPath:
    normalized: str
    physical: Path


def normalize_repo_path(value: str) -> str:
    if not isinstance(value, str):
        raise UnsafePath("path must be a string")
    if "\x00" in value:
        raise UnsafePath("path contains NUL")
    normalized = unicodedata.normalize("NFC", value).replace("\\", "/")
    if not normalized or normalized.startswith("/") or normalized.startswith("//"):
        raise UnsafePath("path must be project-relative")
    if _WINDOWS_DRIVE.match(normalized):
        raise UnsafePath("Windows drive paths are forbidden")
    parts = PurePosixPath(normalized).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise UnsafePath("path traversal or ambiguous component is forbidden")
    return "/".join(parts)


def normalized_path_key(value: str) -> str:
    return normalize_repo_path(value).casefold()


def duplicate_normalized_paths(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for value in values:
        key = normalized_path_key(value)
        if key in seen:
            duplicates.append(value)
        else:
            seen[key] = value
    return tuple(duplicates)


def _assert_no_symlink_components(root: Path, normalized: str) -> None:
    current = root
    for part in PurePosixPath(normalized).parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink():
                raise UnsafeSymlink(f"symlink component is forbidden: {normalized}")


def resolve_project_path(project_root: Path, value: str) -> ConfinedPath:
    normalized = normalize_repo_path(value)
    root = project_root.resolve(strict=True)
    _assert_no_symlink_components(root, normalized)
    candidate = root.joinpath(*PurePosixPath(normalized).parts).resolve(strict=False)
    if candidate != root and root not in candidate.parents:
        raise UnsafePath(f"path escapes project root: {value}")
    return ConfinedPath(normalized=normalized, physical=candidate)


def validate_state_root(project_root: Path, state_root: Path) -> Path:
    root = project_root.resolve(strict=True)
    candidate = state_root.resolve(strict=False)
    reserved = root / ".loop-engineering"
    if candidate != reserved:
        raise UnsafePath("state root must equal project-local .loop-engineering")

    relative = candidate.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink():
                raise UnsafeSymlink("state root traverses a symlink")
    projects = candidate / "projects"
    if projects.is_symlink():
        raise UnsafeSymlink("state root projects directory is a symlink")
    return candidate
