"""Exact-loopback request and authenticated child identity boundary."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import secrets
from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.trustedhost import TrustedHostMiddleware


class StudioSecurity:
    def __init__(self, tool_id: str, *, project_root: Path, expected_origin: str, engine_config_sha256: str, figma_registry_sha256: str, anchor_registry_sha256: str, launch_nonce: str | None = None, test_mode: bool = False) -> None:
        self.tool_id = tool_id
        self.expected_origin = expected_origin.rstrip("/")
        self.allowed_hosts = ["127.0.0.1", "localhost", "[::1]"] + (["testserver"] if test_mode else [])
        self.launch_nonce = launch_nonce or secrets.token_urlsafe(32)
        self.csrf_token = secrets.token_urlsafe(32)
        self.session_id = secrets.token_urlsafe(32)
        stat = project_root.resolve().stat()
        self.root_fingerprint = hashlib.sha256(f"{project_root.resolve()}:{stat.st_dev}:{stat.st_ino}".encode()).hexdigest()
        self.engine_config_sha256 = engine_config_sha256
        self.figma_registry_sha256 = figma_registry_sha256
        self.anchor_registry_sha256 = anchor_registry_sha256

    def status_payload(self, config: dict[str, object]) -> dict[str, object]:
        identity = {
            "tool_id": self.tool_id,
            "project_id": config.get("project_id"),
            "engine_provenance": config.get("engine_provenance"),
            "delivery_eligible": config.get("delivery_eligible"),
            "routing_state": config.get("routing_state"),
            "root_fingerprint": self.root_fingerprint,
            "engine_config_sha256": self.engine_config_sha256,
            "figma_registry_sha256": self.figma_registry_sha256,
            "anchor_registry_sha256": self.anchor_registry_sha256,
        }
        encoded = json.dumps(identity, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
        return {**identity, "status": "ready", "launch_nonce": self.launch_nonce, "process_id": os.getpid(), "config_hash": hashlib.sha256(encoded).hexdigest()}


def install_security(app: FastAPI, security: StudioSecurity) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=security.allowed_hosts)

    @app.middleware("http")
    async def enforce_local_mutation(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.url.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if request.headers.get("origin", "").rstrip("/") != security.expected_origin:
                return JSONResponse(status_code=403, content={"detail": "mutation Origin must exactly match the bound Studio origin"})
            if request.cookies.get("studio_session") != security.session_id:
                return JSONResponse(status_code=403, content={"detail": "studio session is required"})
            if request.headers.get("x-studio-csrf") != security.csrf_token:
                return JSONResponse(status_code=403, content={"detail": "valid X-Studio-CSRF token is required"})
        return await call_next(request)
