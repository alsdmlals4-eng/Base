"""Clean, bounded environments for reviewed Tool Hub children."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import stat
from typing import Mapping
from types import MappingProxyType
from urllib.parse import urlsplit

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
    hub_origin: str | None = None
    delivery_token: str | None = None


def _assert_windows_plain_directory(path: Path) -> None:
    """Reject symlink/reparse traversal for a local Windows runtime directory."""
    absolute = Path(os.path.abspath(path))
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    current = Path(absolute.anchor)
    try:
        for part in absolute.parts[1:]:
            current = current / part
            metadata = current.lstat()
            if (
                stat.S_ISLNK(metadata.st_mode)
                or not stat.S_ISDIR(metadata.st_mode)
                or (reparse and getattr(metadata, "st_file_attributes", 0) & reparse)
            ):
                raise EnvironmentError("private runtime directory is unavailable or replaced")
    except OSError as error:
        raise EnvironmentError("private runtime directory is unavailable or replaced") from error


def ensure_runtime_directory(path: Path) -> Path:
    """Create then verify the Hub-owned runtime path for the active platform."""
    path = Path(path).absolute()
    try:
        path.mkdir(parents=True, mode=0o700, exist_ok=True)
        if os.name == "nt":
            _assert_windows_plain_directory(path)
            return path
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
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    common_invalid = (
        not stat.S_ISDIR(metadata.st_mode)
        or stat.S_ISLNK(metadata.st_mode)
        or (reparse and getattr(metadata, "st_file_attributes", 0) & reparse)
    )
    if os.name == "nt":
        if common_invalid:
            raise EnvironmentError("private Python cache is unsafe")
    elif (
        common_invalid
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


def _validated_hub_origin(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
        or parsed.port is None
        or not 0 < parsed.port < 65536
    ):
        raise EnvironmentError("Hub delivery origin must be an exact 127.0.0.1 HTTP origin")
    return f"http://127.0.0.1:{parsed.port}"


def child_environment(context: LaunchContext, adapter_sha256: str, root_fingerprint: str) -> Mapping[str, str]:
    """Build an import-only child environment without inheriting caller secrets."""
    if len(context.launch_nonce) < 32:
        raise EnvironmentError("Hub launch nonce is invalid")
    if re.fullmatch(r"[0-9a-f]{64}", adapter_sha256) is None:
        raise EnvironmentError("project adapter identity is invalid")
    if re.fullmatch(r"[0-9a-f]{64}", root_fingerprint) is None:
        raise EnvironmentError("project root fingerprint is invalid")
    if (context.hub_origin is None) != (context.delivery_token is None):
        raise EnvironmentError("Hub delivery identity must be configured as one complete pair")
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
    if context.hub_origin is not None and context.delivery_token is not None:
        if len(context.delivery_token) < 32:
            raise EnvironmentError("Hub delivery credential is invalid")
        environment["BASE_TOOL_HUB_DELIVERY_ORIGIN"] = _validated_hub_origin(context.hub_origin)
        environment["BASE_TOOL_HUB_DELIVERY_TOKEN"] = context.delivery_token
    if os.name == "nt":
        # Keep PATH isolated. These fixed Windows locator variables are the only
        # additional inputs used by the reviewed Git resolver to find standard
        # Git for Windows installations.
        for name in ("SystemRoot", "WINDIR", "ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            if value := os.environ.get(name):
                environment[name] = value
    return MappingProxyType(environment)
