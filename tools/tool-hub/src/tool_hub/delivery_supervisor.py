"""Delivery-aware wrapper around the reviewed Tool Hub process supervisor."""

from __future__ import annotations

from dataclasses import replace
import hmac
import os
from pathlib import Path
import secrets
from typing import Iterable
from urllib.parse import urlsplit

from .adapters import LaunchSpec, build_launch_spec
from .environment import LaunchContext
from .launcher import LaunchError
from .projects import ProjectBinding, ProjectLocator
from .supervisor import ProcessSupervisor as _BaseProcessSupervisor
from .windows_process_owner import WindowsOwnershipError


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

    def _read_startup(self, child: object, expected: dict[str, object]) -> dict[str, object]:
        """Accept a Windows venv runtime PID only after exact Job Object ownership proof."""
        if os.name != "nt":
            return super()._read_startup(child, expected)  # type: ignore[arg-type,return-value]

        startup_expected = {name: value for name, value in expected.items() if name != "process_id"}
        payload = super()._read_startup(child, startup_expected)  # type: ignore[arg-type]
        reported_pid = payload.get("process_id")
        windows_owner = getattr(child, "windows_owner", None)
        if type(reported_pid) is not int or reported_pid <= 0 or windows_owner is None:
            raise LaunchError("child startup identity did not match the requested binding")
        try:
            owned = windows_owner.contains_process(reported_pid)
        except WindowsOwnershipError as error:
            raise LaunchError("child startup ownership proof failed") from error
        if not owned:
            raise LaunchError("child startup identity did not match the requested binding")
        expected["process_id"] = reported_pid
        setattr(child, "_runtime_process_id", reported_pid)
        return payload

    def _health_expected(self, child: object, expected: dict[str, object]) -> dict[str, object]:
        """Keep health authentication bound to the verified runtime PID on Windows."""
        if os.name == "nt":
            runtime_pid = getattr(child, "_runtime_process_id", None)
            if type(runtime_pid) is int and runtime_pid > 0:
                return {**expected, "process_id": runtime_pid}
        return super()._health_expected(child, expected)  # type: ignore[arg-type]

    def _start(self, tool_id: str, project_id: str):
        identity = super()._start(tool_id, project_id)
        if os.name != "nt":
            return identity
        child = self._children.get((tool_id, project_id))
        runtime_pid = getattr(child, "_runtime_process_id", None) if child is not None else None
        if type(runtime_pid) is int and runtime_pid > 0 and identity.process_id != runtime_pid:
            identity = replace(identity, process_id=runtime_pid)
            child.identity = identity
        return identity

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
