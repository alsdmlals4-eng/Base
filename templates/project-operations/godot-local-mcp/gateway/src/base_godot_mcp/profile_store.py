from __future__ import annotations

from dataclasses import dataclass


AUTHORIZED_PROFILE_IDS = frozenset({"codex", "gpt-vscode"})
DENIED_PROFILE_IDS = frozenset({"deepseek"})


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
