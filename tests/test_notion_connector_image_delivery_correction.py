from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "NOTION_CONNECTOR_IMAGE_DELIVERY_CORRECTION_2026-08-22.md"
)


class NotionConnectorImageDeliveryCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CORRECTION.read_text(encoding="utf-8")

    def test_correction_explicitly_supersedes_old_binary_routing(self) -> None:
        self.assertIn("supersedes the `Binary media delivery routing` subsection", self.text)
        self.assertIn("NO_SHEETS_NO_LOCAL_BRIDGE_IMAGE_TRANSPORT", self.text)

    def test_google_sheets_and_local_bridge_are_not_active_image_transport(self) -> None:
        for stale_route in (
            "temporary Google Sheets image_uris transport",
            "temporary Sheets transport: PASS",
            "connector-only temporary Sheets transport",
            "Notion Native File Bridge (`ntn`) fallback",
            "tools/notion-native-file-bridge` remains valid and maintained as a **fallback capability",
        ):
            self.assertNotIn(stale_route, self.text)
        self.assertIn("Google Sheets: FORBIDDEN_AS_NEW_IMAGE_TRANSPORT", self.text)
        self.assertIn("LOCAL_NOTION_FILE_BRIDGE: RETIRED_FROM_ACTIVE_ROUTE", self.text)

    def test_direct_notion_attachment_is_primary_and_missing_transport_fails_closed(self) -> None:
        ordered = [
            "trusted direct HTTPS source or connector-native attachment source",
            "Notion create-attachment(source_url)",
            "suggested_markdown / file-upload:// source",
            "prod-files-secure readback",
        ]
        positions = [self.text.index(marker) for marker in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT", self.text)
        self.assertIn("do not substitute Google Sheets or a local bridge", self.text)

    def test_android_success_requires_actual_pixel_observation(self) -> None:
        self.assertIn("HUMAN_VISIBLE_PASS", self.text)
        self.assertIn("actual Android/iOS/browser pixel observation", self.text)
        self.assertIn("READBACK_PASS != HUMAN_VISIBLE_PASS", self.text)

    def test_page_images_do_not_imply_gallery_preview_success(self) -> None:
        self.assertIn("Page/Home/Visual image success does not prove database Files-property", self.text)
        self.assertIn("Gallery Preview", self.text)


if __name__ == "__main__":
    unittest.main()
