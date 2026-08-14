"""Authenticated ephemeral-port startup contract for Tool Hub children."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import secrets
import socket
import stat
from typing import Mapping

from .trusted_files import TrustedFileError, open_directory_nofollow


class HubStartupError(ValueError):
    pass


@dataclass(frozen=True)
class HubLaunchIdentity:
    launch_nonce: str
    adapter_sha256: str
    root_fingerprint: str


def hub_identity_from_environment(environ: Mapping[str, str] | None = None) -> HubLaunchIdentity:
    values = os.environ if environ is None else environ
    nonce = values.get("BASE_TOOL_HUB_LAUNCH_NONCE", "")
    adapter = values.get("BASE_TOOL_HUB_ADAPTER_SHA256", "")
    root = values.get("BASE_TOOL_HUB_ROOT_FINGERPRINT", "")
    if len(nonce) < 32 or not re.fullmatch(r"[0-9a-f]{64}", adapter) or not re.fullmatch(r"[0-9a-f]{64}", root):
        raise HubStartupError("Tool Hub child identity environment is missing or invalid")
    return HubLaunchIdentity(nonce, adapter, root)


def open_loopback_listener(port: int) -> socket.socket:
    if not 0 <= port <= 65535:
        raise HubStartupError("port must be between 0 and 65535")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", port))
        listener.listen(128)
        return listener
    except Exception:
        listener.close()
        raise


def write_startup_report(path: Path, payload: dict[str, object]) -> None:
    target = Path(os.path.abspath(path))
    try:
        parent_fd = open_directory_nofollow(target.parent)
    except TrustedFileError as error:
        raise HubStartupError("startup report parent is unavailable or crosses a symlink") from error
    descriptor = -1
    temporary_name = f".{target.name}.{secrets.token_hex(16)}.tmp"
    try:
        metadata = os.fstat(parent_fd)
        if metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) & 0o077:
            raise HubStartupError("startup report parent must be private to the current user")
        try:
            descriptor = os.open(
                temporary_name,
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0),
                0o600,
                dir_fd=parent_fd,
            )
        except FileExistsError as error:
            raise HubStartupError("startup report temporary file already exists") from error
        raw = (json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode()
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
        try:
            os.link(
                temporary_name,
                target.name,
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise HubStartupError("startup report already exists") from error
        os.unlink(temporary_name, dir_fd=parent_fd)
        temporary_name = ""
        try:
            os.fsync(parent_fd)
        except OSError:
            pass
    except OSError as error:
        raise HubStartupError("startup report could not be written safely") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary_name:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except OSError:
                pass
        os.close(parent_fd)
