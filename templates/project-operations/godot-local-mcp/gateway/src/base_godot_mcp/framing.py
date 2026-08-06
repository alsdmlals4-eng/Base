from __future__ import annotations

import asyncio
import hashlib
import json
from typing import Any


MAX_FRAME_BYTES = 256 * 1024


class FrameError(ValueError):
    """Stable fail-closed framing error."""


def canonical_json_bytes(payload: Any) -> bytes:
    try:
        return json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise FrameError("FRAME_JSON_INVALID") from exc


def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


async def read_frame(reader: asyncio.StreamReader) -> dict[str, Any]:
    try:
        header = await reader.readexactly(4)
    except (asyncio.IncompleteReadError, ConnectionError) as exc:
        raise FrameError("FRAME_HEADER_INCOMPLETE") from exc
    length = int.from_bytes(header, "big")
    if length <= 0 or length > MAX_FRAME_BYTES:
        raise FrameError("FRAME_LENGTH_INVALID")
    try:
        payload = await reader.readexactly(length)
    except (asyncio.IncompleteReadError, ConnectionError) as exc:
        raise FrameError("FRAME_PAYLOAD_INCOMPLETE") from exc
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise FrameError("FRAME_JSON_INVALID") from exc
    if not isinstance(decoded, dict):
        raise FrameError("FRAME_OBJECT_REQUIRED")
    return decoded


async def write_frame(
    writer: asyncio.StreamWriter,
    payload: dict[str, Any],
) -> None:
    if not isinstance(payload, dict):
        raise FrameError("FRAME_OBJECT_REQUIRED")
    encoded = canonical_json_bytes(payload)
    if not encoded or len(encoded) > MAX_FRAME_BYTES:
        raise FrameError("FRAME_LENGTH_INVALID")
    writer.write(len(encoded).to_bytes(4, "big") + encoded)
    try:
        await writer.drain()
    except ConnectionError as exc:
        raise FrameError("FRAME_WRITE_FAILED") from exc
