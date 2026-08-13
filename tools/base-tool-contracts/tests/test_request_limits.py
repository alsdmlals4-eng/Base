import asyncio
import json

from base_tool_contracts import BoundedRequestBodyMiddleware


async def _call(body_messages: list[dict[str, object]], *, content_length: int | None = None) -> tuple[int, bytes, bool]:
    called = False

    async def app(scope: dict[str, object], receive: object, send: object) -> None:
        nonlocal called
        while True:
            message = await receive()
            if not message.get("more_body", False):
                break
        called = True
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    headers = [] if content_length is None else [(b"content-length", str(content_length).encode())]
    scope = {"type": "http", "headers": headers}
    queued = list(body_messages)

    async def receive() -> dict[str, object]:
        return queued.pop(0)

    sent: list[dict[str, object]] = []

    async def send(message: dict[str, object]) -> None:
        sent.append(message)

    await BoundedRequestBodyMiddleware(app, max_body_bytes=10)(scope, receive, send)
    status = next(message["status"] for message in sent if message["type"] == "http.response.start")
    body = b"".join(message.get("body", b"") for message in sent if message["type"] == "http.response.body")
    return int(status), body, called


def test_request_limit_rejects_declared_oversize_before_downstream_parsing() -> None:
    status, body, called = asyncio.run(
        _call([{"type": "http.request", "body": b"small", "more_body": False}], content_length=11)
    )

    assert status == 413
    assert json.loads(body)["detail"] == "request body exceeds the configured safety limit"
    assert called is False


def test_request_limit_rejects_chunked_oversize_before_downstream_parsing() -> None:
    status, _, called = asyncio.run(
        _call(
            [
                {"type": "http.request", "body": b"123456", "more_body": True},
                {"type": "http.request", "body": b"78901", "more_body": False},
            ]
        )
    )

    assert status == 413
    assert called is False


def test_request_limit_replays_a_bounded_body_to_the_downstream_app() -> None:
    status, body, called = asyncio.run(
        _call([{"type": "http.request", "body": b"bounded", "more_body": False}])
    )

    assert status == 204
    assert body == b""
    assert called is True


def test_request_limit_can_be_scoped_to_only_the_import_endpoint() -> None:
    async def call_other_path() -> tuple[int, bool]:
        called = False

        async def app(scope: dict[str, object], receive: object, send: object) -> None:
            nonlocal called
            called = True
            await send({"type": "http.response.start", "status": 204, "headers": []})
            await send({"type": "http.response.body", "body": b""})

        async def receive() -> dict[str, object]:
            return {"type": "http.request", "body": b"", "more_body": False}

        sent: list[dict[str, object]] = []

        async def send(message: dict[str, object]) -> None:
            sent.append(message)

        scope = {"type": "http", "path": "/api/config", "headers": [(b"content-length", b"999")]}
        await BoundedRequestBodyMiddleware(app, max_body_bytes=10, path="/api/import-runs")(scope, receive, send)
        return int(sent[0]["status"]), called

    assert asyncio.run(call_other_path()) == (204, True)
