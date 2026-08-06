from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .profile_store import ClientProfile
from .project_identity import ProjectIdentity


_PROTOCOL = "BASE_GODOT_BRIDGE_V1"
_DESCRIPTOR_KEYS = frozenset(
    {
        "schema_version",
        "protocol",
        "host",
        "port",
        "bridge_instance_id",
        "descriptor_nonce",
        "profile_id",
        "project_fingerprint",
        "expires_at",
    }
)
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{32,256}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class BridgeDescriptorError(ValueError):
    """Fail-closed Bridge descriptor error with a stable code."""


@dataclass(frozen=True, slots=True)
class BridgeDescriptor:
    protocol: str
    host: str
    port: int
    bridge_instance_id: str
    descriptor_nonce: str
    profile_id: str
    project_fingerprint: str
    expires_at: datetime


def _fail(code: str, exc: BaseException | None = None) -> BridgeDescriptorError:
    error = BridgeDescriptorError(code)
    if exc is not None:
        error.__cause__ = exc
    return error


def _parse_expiry(value: Any) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as exc:
        raise _fail("BRIDGE_DESCRIPTOR_INVALID", exc)
    return parsed.astimezone(timezone.utc)


def load_bridge_descriptor(
    path: str | Path,
    *,
    profile: ClientProfile,
    project: ProjectIdentity,
    now: datetime | None = None,
) -> BridgeDescriptor:
    descriptor_path = Path(path).expanduser()
    if descriptor_path.is_symlink() or not descriptor_path.is_file():
        raise _fail("BRIDGE_DESCRIPTOR_REQUIRED")
    if os.name == "posix" and descriptor_path.stat().st_mode & 0o077:
        raise _fail("BRIDGE_DESCRIPTOR_PERMISSION_INVALID")
    try:
        payload = json.loads(descriptor_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _fail("BRIDGE_DESCRIPTOR_INVALID", exc)
    if not isinstance(payload, dict) or frozenset(payload) != _DESCRIPTOR_KEYS:
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")
    if payload.get("schema_version") != 1 or payload.get("protocol") != _PROTOCOL:
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")

    host = payload.get("host")
    if host not in {"127.0.0.1", "::1"}:
        raise _fail("BRIDGE_DESCRIPTOR_LOOPBACK_REQUIRED")
    port = payload.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1024 <= port <= 65535:
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")
    bridge_instance_id = payload.get("bridge_instance_id")
    if not isinstance(bridge_instance_id, str) or not _ID_RE.fullmatch(bridge_instance_id):
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")
    descriptor_nonce = payload.get("descriptor_nonce")
    if not isinstance(descriptor_nonce, str) or not _NONCE_RE.fullmatch(descriptor_nonce):
        raise _fail("BRIDGE_DESCRIPTOR_INVALID")
    profile_id = payload.get("profile_id")
    if profile_id != profile.profile_id:
        raise _fail("BRIDGE_DESCRIPTOR_PROFILE_MISMATCH")
    project_fingerprint = payload.get("project_fingerprint")
    if (
        not isinstance(project_fingerprint, str)
        or not _SHA256_RE.fullmatch(project_fingerprint)
        or project_fingerprint != project.fingerprint
    ):
        raise _fail("BRIDGE_DESCRIPTOR_PROJECT_MISMATCH")
    expires_at = _parse_expiry(payload.get("expires_at"))
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if expires_at <= current:
        raise _fail("BRIDGE_DESCRIPTOR_EXPIRED")

    return BridgeDescriptor(
        protocol=_PROTOCOL,
        host=host,
        port=port,
        bridge_instance_id=bridge_instance_id,
        descriptor_nonce=descriptor_nonce,
        profile_id=profile_id,
        project_fingerprint=project_fingerprint,
        expires_at=expires_at,
    )
