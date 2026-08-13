"""Exact-loopback browser mutation boundary for Tool Hub."""

from __future__ import annotations

import secrets
from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.trustedhost import TrustedHostMiddleware


class HubSecurity:
    def __init__(self, expected_origin: str, *, test_mode: bool = False) -> None:
        self.expected_origin = expected_origin.rstrip("/")
        self.allowed_hosts = ["127.0.0.1", "localhost", "[::1]"] + (["testserver"] if test_mode else [])
        self.csrf_token = secrets.token_urlsafe(32)
        self.session_id = secrets.token_urlsafe(32)


def install_security(app: FastAPI, security: HubSecurity) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=security.allowed_hosts)

    @app.middleware("http")
    async def enforce_local_mutation(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if request.headers.get("origin", "").rstrip("/") != security.expected_origin:
                return JSONResponse(status_code=403, content={"detail": "mutation Origin must match Tool Hub"})
            if request.cookies.get("hub_session") != security.session_id:
                return JSONResponse(status_code=403, content={"detail": "Tool Hub session is required"})
            if request.headers.get("x-hub-csrf") != security.csrf_token:
                return JSONResponse(status_code=403, content={"detail": "valid X-Hub-CSRF token is required"})
        return await call_next(request)
