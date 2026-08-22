from __future__ import annotations

import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from notion_native_file_bridge.cli import main
from notion_native_file_bridge.ntn import BridgeError, UploadReceipt


class FakeClient:
    def preflight(self) -> dict[str, object]:
        return {
            "status": "PASS",
            "operation": "preflight",
            "api_version": "2026-03-11",
            "ntn_version": "ntn 0.9.0",
        }

    def upload(self, path: Path) -> UploadReceipt:
        return UploadReceipt(
            status="PASS",
            operation="upload",
            upload_id="upload-1",
            filename=path.name,
            content_type="image/jpeg",
            content_length=12,
            source_sha256="abc123",
            notion_status="uploaded",
        )

    def append_image(self, page_id: str, upload_id: str) -> dict[str, object]:
        return {"status": "PASS", "operation": "append-image", "page_id": page_id, "upload_id": upload_id, "block_id": "block-1"}

    def set_cover(self, page_id: str, upload_id: str) -> dict[str, object]:
        return {"status": "PASS", "operation": "set-cover", "page_id": page_id, "upload_id": upload_id}

    def set_files_property(self, page_id: str, property_name: str, upload_id: str, filename: str) -> dict[str, object]:
        return {
            "status": "PASS",
            "operation": "set-files-property",
            "page_id": page_id,
            "property": property_name,
            "upload_id": upload_id,
            "filename": filename,
        }


class BlockedClient(FakeClient):
    def preflight(self) -> dict[str, object]:
        raise BridgeError("NTN_UNAVAILABLE", "ntn was not found")


class CliTests(unittest.TestCase):
    def run_cli(self, argv: list[str], client: object) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with patch("notion_native_file_bridge.cli.NtnClient", return_value=client):
            with patch("sys.stdout", output):
                code = main(argv)
        payload = json.loads(output.getvalue())
        return code, payload

    def test_preflight_emits_single_pass_json_receipt(self) -> None:
        code, payload = self.run_cli(["preflight"], FakeClient())

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["operation"], "preflight")
        self.assertNotEqual(payload.get("status"), "HUMAN_VISIBLE_PASS")

    def test_upload_emits_identity_fields(self) -> None:
        code, payload = self.run_cli(["upload", "--file", "approved.jpg"], FakeClient())

        self.assertEqual(code, 0)
        self.assertEqual(payload["upload_id"], "upload-1")
        self.assertEqual(payload["filename"], "approved.jpg")
        self.assertEqual(payload["source_sha256"], "abc123")
        self.assertEqual(payload["content_length"], 12)

    def test_append_image_routes_arguments(self) -> None:
        code, payload = self.run_cli(
            ["append-image", "--page-id", "page-1", "--upload-id", "upload-1"],
            FakeClient(),
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["operation"], "append-image")
        self.assertEqual(payload["block_id"], "block-1")

    def test_set_cover_routes_arguments(self) -> None:
        code, payload = self.run_cli(
            ["set-cover", "--page-id", "page-1", "--upload-id", "upload-1"],
            FakeClient(),
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["operation"], "set-cover")

    def test_set_files_property_routes_arguments(self) -> None:
        code, payload = self.run_cli(
            [
                "set-files-property",
                "--page-id",
                "page-1",
                "--property",
                "Preview",
                "--upload-id",
                "upload-1",
                "--filename",
                "approved.jpg",
            ],
            FakeClient(),
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["operation"], "set-files-property")
        self.assertEqual(payload["property"], "Preview")

    def test_blocked_error_is_json_and_nonzero(self) -> None:
        code, payload = self.run_cli(["preflight"], BlockedClient())

        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertEqual(payload["code"], "NTN_UNAVAILABLE")
        self.assertNotIn("HUMAN_VISIBLE_PASS", json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
