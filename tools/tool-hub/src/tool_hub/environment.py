"""Clean, bounded environments for reviewed Tool Hub children."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import stat
from typing import Mapping
from types import MappingProxyType

from base_tool_contracts.trusted_files import TrustedFileError, open_directory_nofollow


class EnvironmentError(ValueError):
    pass


@dataclass(frozen=True)
class LaunchContext:
    """Hub-owned launch inputs; none are accepted from a browser request."""

    base_root: Path
    runtime_root: Path
    python_executable: Path
    launch_nonce: str


def ensure_runtime_directory(path: Path) -> Path:
    """Create then reopen the Hub-owned runtime path without link traversal."""
    path = Path(path).absolute()
    try:
        path.mkdir(parents=True, mode=0o700, exist_ok=True)
        descriptor = open_directory_nofollow(path)
        try:
            os.fchmod(descriptor, 0o700)
            metadata = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except (OSError, TrustedFileError) as error:
        raise EnvironmentError("private runtime directory is unavailable or replaced") from error
    if metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) != 0o700:
        raise EnvironmentError("private runtime directory is unsafe")
    return path


def _private_empty_directory(path: Path) -> Path:
    path = ensure_runtime_directory(path.parent) / path.name
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        pass
    try:
        metadata = os.lstat(path)
    except OSError as error:
        raise EnvironmentError("private Python cache is unavailable") from error
    if (
        not stat.S_ISDIR(metadata.st_mode)
        or stat.S_ISLNK(metadata.st_mode)
        or metadata.st_uid != os.geteuid()
        or stat.S_IMODE(metadata.st_mode) != 0o700
    ):
        raise EnvironmentError("private Python cache is unsafe")
    try:
        if any(path.iterdir()):
            raise EnvironmentError("private Python cache must start empty")
    except OSError as error:
        raise EnvironmentError("private Python cache is unavailable") from error
    return path


def child_environment(context: LaunchContext, adapter_sha256: str, root_fingerprint: str) -> Mapping[str, str]:
    """Build an import-only child environment without inheriting caller secrets."""
    if len(context.launch_nonce) < 32:
        raise EnvironmentError("Hub launch nonce is invalid")
    if re.fullmatch(r"[0-9a-f]{64}", adapter_sha256) is None:
        raise EnvironmentError("project adapter identity is invalid")
    if re.fullmatch(r"[0-9a-f]{64}", root_fingerprint) is None:
        raise EnvironmentError("project root fingerprint is invalid")
    runtime = ensure_runtime_directory(context.runtime_root)
    cache = _private_empty_directory(runtime / "pycache")
    environment = {
        "PATH": os.defpath,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": str(cache),
        "BASE_TOOL_HUB_LAUNCH_NONCE": context.launch_nonce,
        "BASE_TOOL_HUB_ADAPTER_SHA256": adapter_sha256,
        "BASE_TOOL_HUB_ROOT_FINGERPRINT": root_fingerprint,
    }
    return MappingProxyType(environment)
