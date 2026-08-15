"""Delivery-aware wrapper around the reviewed Tool Hub process supervisor."""

from __future__ import annotations

from dataclasses import replace
import hmac
from pathlib import Path
import secrets
from typing import Iterable
from urllib.parse import urlsplit

from .adapters import LaunchSpec, build_launch_spec
from .environment import LaunchContext
from .launcher import LaunchError
from .projects import ProjectBinding, ProjectLocator
from .supervisor import ProcessSupervisor as _BaseProcessSupervisor


_DELIVERY_TOKEN_ENV = "BASE_TOOL_HUB_DELIVERY_TOKEN"


def _validated_origin(value: str) -> str:
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
        raise ValueError("Tool Hub delivery origin must be an exact 127.0.0.1 HTTP origin")
    return f"http://127.0.0.1:{parsed.port}"


class ProcessSupervisor(_BaseProcessSupervisor):
    """Inject one private delivery credential into each reviewed Studio child."""

    def __init__(
        self,
        runtime_root: Path,
        base_root: Path,
        locator: ProjectLocator,
        tools: Iterable[dict[str, object]],
        *,
        hub_origin: str = "http://127.0.0.1:8764",
        spec_builder=build_launch_spec,
        **kwargs: object,
    ) -> None:
        self.hub_origin = _validated_origin(hub_origin)

        def delivery_spec_builder(
            tool: dict[str, object],
            binding: ProjectBinding,
            context: LaunchContext,
        ) -> LaunchSpec:
            enriched = replace(
                context,
                hub_origin=self.hub_origin,
                delivery_token=secrets.token_urlsafe(32),
            )
            return spec_builder(tool, binding, enriched)

        super().__init__(
            runtime_root,
            base_root,
            locator,
            tools,
            spec_builder=delivery_spec_builder,
            **kwargs,
        )

    def authorize_delivery_token(self, token: str) -> tuple[str, str]:
        """Resolve one credential only while its exact child is in the public RUNNING state."""
        if not isinstance(token, str) or len(token) < 32:
            raise LaunchError("studio delivery credential is invalid")
        matches: list[tuple[str, str]] = []
        for key, child in tuple(self._children.items()):
            state = self._states.get(key)
            if state is None or state.status != "RUNNING" or child.process.poll() is not None:
                continue
            candidate = str(child.spec.env.get(_DELIVERY_TOKEN_ENV, ""))
            if candidate and hmac.compare_digest(candidate, token):
                matches.append(key)
        if len(matches) != 1:
            raise LaunchError("studio delivery credential is invalid")
        return matches[0]

    def _sanitized_log_tail(self, child: object) -> str:
        """Preserve base log sanitization and additionally remove the child-only delivery secret."""
        public = super()._sanitized_log_tail(child)  # type: ignore[arg-type]
        try:
            token = str(child.spec.env.get(_DELIVERY_TOKEN_ENV, ""))  # type: ignore[attr-defined]
        except (AttributeError, TypeError):
            token = ""
        if token:
            public = public.replace(token, "<redacted>")
        return public
