"""Exact-loopback browser and child identity boundary."""

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


class QaSecurity:
    def __init__(
        self,
        project_root: Path,
        project_id: str,
        expected_origin: str,
        *,
        launch_nonce: str | None = None,
        test_mode: bool = False,
    ) -> None:
        self.project_id = project_id
        self.expected_origin = expected_origin.rstrip("/")
        self.allowed_hosts = ["127.0.0.1", "localhost", "[::1]"] + (["testserver"] if test_mode else [])
        self.launch_nonce = launch_nonce or secrets.token_urlsafe(32)
        self.csrf_token = secrets.token_urlsafe(32)
        self.session_id = secrets.token_urlsafe(32)
        root = project_root.resolve()
        stat = root.stat()
        self.root_fingerprint = hashlib.sha256(f"{root}:{stat.st_dev}:{stat.st_ino}".encode()).hexdigest()

    def status(self) -> dict[str, object]:
        identity = {
            "tool_id": "qa-evidence-studio",
            "project_id": self.project_id,
            "root_fingerprint": self.root_fingerprint,
            "reviewer_role": "DEVELOPER_OWNER",
            "android_status": "DEFERRED_NOT_CONNECTED",
        }
        encoded = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
        return {
            **identity,
            "status": "ready",
            "launch_nonce": self.launch_nonce,
            "process_id": os.getpid(),
            "config_hash": hashlib.sha256(encoded).hexdigest(),
        }


def install_security(app: FastAPI, security: QaSecurity) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=security.allowed_hosts)

    @app.middleware("http")
    async def enforce_local_mutation(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if request.headers.get("origin", "").rstrip("/") != security.expected_origin:
                return JSONResponse(status_code=403, content={"detail": "mutation Origin must match QA Evidence Studio"})
            if request.cookies.get("qa_session") != security.session_id:
                return JSONResponse(status_code=403, content={"detail": "QA browser session is required"})
            if request.headers.get("x-qa-csrf") != security.csrf_token:
                return JSONResponse(status_code=403, content={"detail": "valid X-QA-CSRF token is required"})
        return await call_next(request)
