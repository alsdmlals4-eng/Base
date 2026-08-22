from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from notion_native_file_bridge.ntn import BridgeError, NOTION_VERSION, NtnClient


class QueueRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[bytes]]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def __call__(self, args: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        self.calls.append({"args": list(args), **kwargs})
        if not self.responses:
            raise AssertionError(f"unexpected subprocess call: {args}")
        return self.responses.pop(0)


def completed(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess(
        args=["ntn"],
        returncode=returncode,
        stdout=stdout.encode("utf-8"),
        stderr=stderr.encode("utf-8"),
    )


class NtnClientTests(unittest.TestCase):
    def test_preflight_requires_version_and_authenticated_api_probe(self) -> None:
        runner = QueueRunner(
            [
                completed("ntn 0.9.0\n"),
                completed('{"object":"user","id":"user-1"}\n'),
            ]
        )
        client = NtnClient(executable="C:/Tools/ntn.cmd", runner=runner)

        receipt = client.preflight()

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["operation"], "preflight")
        self.assertEqual(receipt["api_version"], NOTION_VERSION)
        self.assertEqual(
            runner.calls[0]["args"],
            ["C:/Tools/ntn.cmd", "--version"],
        )
        self.assertEqual(
            runner.calls[1]["args"],
            [
                "C:/Tools/ntn.cmd",
                "api",
                "v1/users/me",
                "--notion-version",
                NOTION_VERSION,
            ],
        )

    def test_upload_sends_local_bytes_and_returns_identity_receipt_after_readback(self) -> None:
        payload = b"approved-dark-dashboard-bytes"
        upload_id = "43833259-72ae-404e-8441-b6577f3159b4"
        runner = QueueRunner(
            [
                completed(f"{upload_id}\tapproved.jpg\tuploaded\timage/jpeg\t29\n"),
                completed(
                    '{"object":"file_upload","id":"43833259-72ae-404e-8441-b6577f3159b4",'
                    '"status":"uploaded","filename":"approved.jpg","content_type":"image/jpeg"}'
                ),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approved.jpg"
            path.write_bytes(payload)
            receipt = client.upload(path)

        self.assertEqual(receipt.status, "PASS")
        self.assertEqual(receipt.operation, "upload")
        self.assertEqual(receipt.upload_id, upload_id)
        self.assertEqual(receipt.filename, "approved.jpg")
        self.assertEqual(receipt.content_type, "image/jpeg")
        self.assertEqual(receipt.content_length, len(payload))
        self.assertEqual(receipt.source_sha256, hashlib.sha256(payload).hexdigest())
        self.assertEqual(
            runner.calls[0]["args"],
            [
                "ntn",
                "files",
                "create",
                "--plain",
                "--filename",
                "approved.jpg",
                "--content-type",
                "image/jpeg",
            ],
        )
        self.assertEqual(runner.calls[0]["input"], payload)
        self.assertEqual(
            runner.calls[1]["args"],
            ["ntn", "files", "get", upload_id, "--json"],
        )

    def test_upload_fails_closed_when_readback_id_or_status_disagrees(self) -> None:
        upload_id = "43833259-72ae-404e-8441-b6577f3159b4"
        runner = QueueRunner(
            [
                completed(f"{upload_id}\tapproved.png\tuploaded\timage/png\t3\n"),
                completed('{"object":"file_upload","id":"different","status":"uploaded"}'),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approved.png"
            path.write_bytes(b"png")
            with self.assertRaises(BridgeError) as ctx:
                client.upload(path)

        self.assertEqual(ctx.exception.code, "UPLOAD_READBACK_MISMATCH")

    def test_append_image_uses_typed_file_upload_and_independent_block_readback(self) -> None:
        upload_id = "upload-1"
        block_id = "block-1"
        runner = QueueRunner(
            [
                completed('{"object":"list","results":[{"id":"block-1","type":"image"}]}'),
                completed('{"object":"block","id":"block-1","type":"image","image":{"type":"file"}}'),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        receipt = client.append_image("page-1", upload_id)

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["block_id"], block_id)
        args = runner.calls[0]["args"]
        self.assertIn("children[0][type]=image", args)
        self.assertIn("children[0][image][type]=file_upload", args)
        self.assertIn(f"children[0][image][file_upload][id]={upload_id}", args)
        self.assertEqual(
            runner.calls[1]["args"],
            ["ntn", "api", f"v1/blocks/{block_id}", "--notion-version", NOTION_VERSION],
        )

    def test_set_cover_uses_typed_file_upload_and_page_readback(self) -> None:
        runner = QueueRunner(
            [
                completed('{"object":"page","id":"page-1"}'),
                completed('{"object":"page","id":"page-1","cover":{"type":"file","file":{"url":"https://signed"}}}'),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        receipt = client.set_cover("page-1", "upload-1")

        self.assertEqual(receipt["status"], "PASS")
        args = runner.calls[0]["args"]
        self.assertIn("cover[type]=file_upload", args)
        self.assertIn("cover[file_upload][id]=upload-1", args)
        self.assertEqual(
            runner.calls[1]["args"],
            ["ntn", "api", "v1/pages/page-1", "--notion-version", NOTION_VERSION],
        )

    def test_set_files_property_uses_typed_upload_and_requires_nonempty_readback(self) -> None:
        runner = QueueRunner(
            [
                completed('{"object":"page","id":"page-1"}'),
                completed(
                    '{"object":"page","id":"page-1","properties":{'
                    '"Preview":{"id":"abc","type":"files","files":[{"name":"approved.jpg","type":"file"}]}}}'
                ),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        receipt = client.set_files_property("page-1", "Preview", "upload-1", "approved.jpg")

        self.assertEqual(receipt["status"], "PASS")
        args = runner.calls[0]["args"]
        self.assertIn("properties[Preview][files][0][type]=file_upload", args)
        self.assertIn("properties[Preview][files][0][file_upload][id]=upload-1", args)
        self.assertIn("properties[Preview][files][0][name]=approved.jpg", args)

    def test_subprocess_error_redacts_notion_api_token(self) -> None:
        secret = "ntn_super_secret_value"
        runner = QueueRunner(
            [completed(stderr=f"authorization failed for {secret}", returncode=1)]
        )
        client = NtnClient(executable="ntn", runner=runner)

        with patch.dict(os.environ, {"NOTION_API_TOKEN": secret}, clear=False):
            with self.assertRaises(BridgeError) as ctx:
                client.preflight()

        self.assertNotIn(secret, str(ctx.exception))
        self.assertIn("<REDACTED>", str(ctx.exception))

    def test_missing_local_file_fails_before_subprocess(self) -> None:
        runner = QueueRunner([])
        client = NtnClient(executable="ntn", runner=runner)

        with self.assertRaises(BridgeError) as ctx:
            client.upload(Path("definitely-missing.png"))

        self.assertEqual(ctx.exception.code, "FILE_NOT_FOUND")
        self.assertEqual(runner.calls, [])


if __name__ == "__main__":
    unittest.main()
