"""ASGI request-body limits applied before multipart parsing."""

import json
from typing import Any, Awaitable, Callable


ASGIMessage = dict[str, Any]
ASGIReceive = Callable[[], Awaitable[ASGIMessage]]
ASGISend = Callable[[ASGIMessage], Awaitable[None]]
ASGIApp = Callable[[dict[str, Any], ASGIReceive, ASGISend], Awaitable[None]]


class _RequestBodyTooLarge(Exception):
    pass


class BoundedRequestBodyMiddleware:
    """Count the original receive stream and fail closed before unbounded multipart spooling."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        max_body_bytes: int,
        path: str | None = None,
        path_prefix: str | None = None,
    ) -> None:
        if max_body_bytes < 1:
            raise ValueError("request body limit must be positive")
        if path is not None and path_prefix is not None:
            raise ValueError("request body limit may use an exact path or a path prefix, not both")
        if path_prefix is not None and not path_prefix.startswith("/"):
            raise ValueError("request body path prefix must be absolute")
        self._app = app
        self._max_body_bytes = max_body_bytes
        self._path = path
        self._path_prefix = path_prefix

    async def __call__(self, scope: dict[str, Any], receive: ASGIReceive, send: ASGISend) -> None:
        if scope.get("type") != "http":
            await self._app(scope, receive, send)
            return
        request_path = scope.get("path")
        if self._path is not None and request_path != self._path:
            await self._app(scope, receive, send)
            return
        if self._path_prefix is not None and (
            not isinstance(request_path, str) or not request_path.startswith(self._path_prefix)
        ):
            await self._app(scope, receive, send)
            return
        content_lengths = [value for name, value in scope.get("headers", []) if name.lower() == b"content-length"]
        try:
            declared_length = int(content_lengths[-1]) if content_lengths else None
        except (TypeError, ValueError):
            await self._reject(send, status=400, detail="invalid Content-Length header")
            return
        if declared_length is not None and (declared_length < 0 or declared_length > self._max_body_bytes):
            await self._reject(send, status=413, detail="request body exceeds the configured safety limit")
            return

        total = 0
        exceeded = False
        buffered_response: list[ASGIMessage] = []

        async def capped_receive() -> ASGIMessage:
            nonlocal total, exceeded
            message = await receive()
            if message.get("type") == "http.request":
                total += len(message.get("body", b""))
                if total > self._max_body_bytes:
                    exceeded = True
                    raise _RequestBodyTooLarge
            return message

        async def buffer_send(message: ASGIMessage) -> None:
            buffered_response.append(message)

        try:
            await self._app(scope, capped_receive, buffer_send)
        except _RequestBodyTooLarge:
            exceeded = True
        if exceeded:
            await self._reject(send, status=413, detail="request body exceeds the configured safety limit")
            return
        for message in buffered_response:
            await send(message)

    @staticmethod
    async def _reject(send: ASGISend, *, status: int, detail: str) -> None:
        payload = json.dumps({"detail": detail}, separators=(",", ":")).encode()
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(payload)).encode())],
            }
        )
        await send({"type": "http.response.body", "body": payload})
