from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = ROOT / "templates/project-operations/godot-local-mcp/gateway/src"


class GodotLocalMcpFramingTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(GATEWAY_SRC))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(str(GATEWAY_SRC))

    def test_canonical_json_and_sha_are_stable(self) -> None:
        from base_godot_mcp.framing import canonical_json_bytes, canonical_sha256

        self.assertEqual(
            canonical_json_bytes({"z": 1, "a": "한글"}),
            b'{"a":"\xed\x95\x9c\xea\xb8\x80","z":1}',
        )
        self.assertEqual(
            canonical_sha256({"a": 1, "b": 2}),
            canonical_sha256({"b": 2, "a": 1}),
        )

    async def test_round_trip_frame(self) -> None:
        from base_godot_mcp.framing import read_frame, write_frame

        received: asyncio.Future[dict[str, object]] = asyncio.get_running_loop().create_future()

        async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            try:
                received.set_result(await read_frame(reader))
            finally:
                writer.close()
                await writer.wait_closed()

        server = await asyncio.start_server(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            await write_frame(writer, {"type": "TEST", "value": 7})
            writer.close()
            await writer.wait_closed()
            self.assertEqual(
                await asyncio.wait_for(received, 2),
                {"type": "TEST", "value": 7},
            )
        finally:
            server.close()
            await server.wait_closed()

    async def test_zero_oversized_and_non_object_frames_fail_closed(self) -> None:
        from base_godot_mcp.framing import FrameError, MAX_FRAME_BYTES, read_frame

        for payload in (
            (0).to_bytes(4, "big"),
            (MAX_FRAME_BYTES + 1).to_bytes(4, "big"),
            (2).to_bytes(4, "big") + b"[]",
        ):
            reader = asyncio.StreamReader()
            reader.feed_data(payload)
            reader.feed_eof()
            with self.assertRaises(FrameError):
                await read_frame(reader)


if __name__ == "__main__":
    unittest.main()
