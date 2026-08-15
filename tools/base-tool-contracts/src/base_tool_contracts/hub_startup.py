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


def _startup_bytes(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _assert_portable_plain_parent(path: Path) -> Path:
    """Validate a Windows-style directory chain without following reparse points."""
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
                raise HubStartupError("startup report parent is unavailable or crosses a symlink")
    except OSError as error:
        raise HubStartupError("startup report parent is unavailable or crosses a symlink") from error
    return absolute


def _write_startup_report_portable(target: Path, payload: dict[str, object]) -> None:
    """Publish a complete startup report on Windows without descriptor-relative APIs."""
    parent = _assert_portable_plain_parent(target.parent)
    if os.path.lexists(target):
        raise HubStartupError("startup report already exists")
    temporary = parent / f".{target.name}.{secrets.token_hex(16)}.tmp"
    descriptor = -1
    published = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        descriptor = os.open(temporary, flags, 0o600)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise HubStartupError("startup report temporary file is not regular")
        raw = _startup_bytes(payload)
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise OSError("startup report write made no progress")
            offset += written
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1

        # Creating a hard link is no-overwrite publication: if another file
        # appears at the final name, the operation fails instead of replacing it.
        try:
            os.link(temporary, target, follow_symlinks=False)
        except FileExistsError as error:
            raise HubStartupError("startup report already exists") from error
        published = True
        final = target.lstat()
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if (
            stat.S_ISLNK(final.st_mode)
            or not stat.S_ISREG(final.st_mode)
            or (reparse and getattr(final, "st_file_attributes", 0) & reparse)
            or (final.st_dev, final.st_ino) != (opened.st_dev, opened.st_ino)
        ):
            raise HubStartupError("startup report publication identity changed")
        temporary.unlink()
    except HubStartupError:
        raise
    except OSError as error:
        raise HubStartupError("startup report could not be written safely") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        if published:
            # Never remove the final report during ordinary cleanup; the Hub
            # owns it after successful no-overwrite publication.
            pass


def _write_startup_report_descriptor_bound(target: Path, payload: dict[str, object]) -> None:
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
        raw = _startup_bytes(payload)
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise OSError("startup report write made no progress")
            offset += written
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


def write_startup_report(path: Path, payload: dict[str, object]) -> None:
    target = Path(os.path.abspath(path))
    if os.name == "nt":
        _write_startup_report_portable(target, payload)
        return
    _write_startup_report_descriptor_bound(target, payload)
