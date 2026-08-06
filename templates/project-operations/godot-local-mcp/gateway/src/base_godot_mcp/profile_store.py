from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AUTHORIZED_PROFILE_IDS = frozenset({"codex", "gpt-vscode"})
DENIED_PROFILE_IDS = frozenset({"deepseek"})
_ALLOWED_CAPABILITIES = frozenset(
    {
        "editor.status",
        "capabilities.list",
        "scene.inspect",
        "node.rename",
        "task.status",
    }
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PROFILE_KEYS = frozenset(
    {
        "schema_version",
        "profile_id",
        "enabled",
        "credential_secret",
        "allowed_project_fingerprints",
        "allowed_capabilities",
        "expires_at",
    }
)


class ProfileError(ValueError):
    """Fail-closed profile authorization error with a stable code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ClientProfile:
    profile_id: str
    enabled: bool
    allowed_project_fingerprints: tuple[str, ...]
    allowed_capabilities: tuple[str, ...]
    credential_secret: str = field(default="", repr=False, compare=False)
    expires_at: datetime | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.profile_id not in AUTHORIZED_PROFILE_IDS:
            raise ProfileError("MCP_CLIENT_PROFILE_DENIED")
        if not self.enabled:
            raise ProfileError("MCP_CLIENT_PROFILE_DISABLED")

    def require_project(self, fingerprint: str) -> None:
        if fingerprint not in self.allowed_project_fingerprints:
            raise ProfileError("MCP_PROJECT_NOT_AUTHORIZED")

    def require_capability(self, capability: str) -> None:
        if capability not in self.allowed_capabilities:
            raise ProfileError("MCP_CAPABILITY_NOT_AUTHORIZED")


def _parse_expiry(value: Any) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as exc:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID") from exc
    if parsed.tzinfo is None:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")
    return parsed.astimezone(timezone.utc)


def _require_private_file(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise ProfileError("MCP_CLIENT_PROFILE_REQUIRED")
    if os.name == "posix" and path.stat().st_mode & 0o077:
        raise ProfileError("MCP_CLIENT_PROFILE_PERMISSION_INVALID")


def _require_string_tuple(value: Any, *, code: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ProfileError(code)
    if any(not isinstance(item, str) or not item for item in value):
        raise ProfileError(code)
    if len(set(value)) != len(value):
        raise ProfileError(code)
    return tuple(value)


def load_profile(
    profile_id: str,
    *,
    config_dir: str | Path,
    now: datetime | None = None,
) -> ClientProfile:
    """Load one owner-private authorized profile without probing denied IDs."""

    if profile_id not in AUTHORIZED_PROFILE_IDS:
        raise ProfileError("MCP_CLIENT_PROFILE_DENIED")

    path = Path(config_dir).expanduser() / f"{profile_id}.json"
    _require_private_file(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID") from exc

    if not isinstance(payload, dict) or frozenset(payload) != _PROFILE_KEYS:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")
    if payload.get("schema_version") != 1 or payload.get("profile_id") != profile_id:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")
    if not isinstance(payload.get("enabled"), bool):
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")

    secret = payload.get("credential_secret")
    if not isinstance(secret, str) or len(secret) < 32 or len(secret) > 512:
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")

    fingerprints = _require_string_tuple(
        payload.get("allowed_project_fingerprints"),
        code="MCP_CLIENT_PROFILE_INVALID",
    )
    if any(not _SHA256_RE.fullmatch(value) for value in fingerprints):
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")

    capabilities = _require_string_tuple(
        payload.get("allowed_capabilities"),
        code="MCP_CLIENT_PROFILE_INVALID",
    )
    if not set(capabilities).issubset(_ALLOWED_CAPABILITIES):
        raise ProfileError("MCP_CLIENT_PROFILE_INVALID")

    expires_at = _parse_expiry(payload.get("expires_at"))
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if expires_at is not None and expires_at <= current:
        raise ProfileError("MCP_CLIENT_PROFILE_EXPIRED")

    return ClientProfile(
        profile_id=profile_id,
        enabled=payload["enabled"],
        allowed_project_fingerprints=fingerprints,
        allowed_capabilities=capabilities,
        credential_secret=secret,
        expires_at=expires_at,
    )
