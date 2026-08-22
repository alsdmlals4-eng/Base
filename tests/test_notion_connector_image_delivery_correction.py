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

    def test_connector_only_page_image_path_is_primary(self) -> None:
        ordered = [
            "temporary Google Sheets image_uris transport",
            "Notion create-attachment(source_url)",
            "suggested_markdown / file-upload:// source",
            "prod-files-secure readback",
            "delete temporary Sheet",
        ]
        positions = [self.text.index(marker) for marker in ordered]
        self.assertEqual(positions, sorted(positions))

    def test_local_ntn_bridge_is_fallback_not_mandatory(self) -> None:
        self.assertIn("Notion Native File Bridge (`ntn`) fallback", self.text)
        self.assertIn("Do not require PowerShell/`ntn`", self.text)

    def test_android_success_requires_actual_pixel_observation(self) -> None:
        self.assertIn("HUMAN_VISIBLE_PASS", self.text)
        self.assertIn("actual Android/iOS/browser pixel observation", self.text)
        self.assertIn("READBACK_PASS != HUMAN_VISIBLE_PASS", self.text)

    def test_preview_is_optional_and_not_a_human_image_completion_gate(self) -> None:
        self.assertIn("OPTIONAL / NON-AUTHORITY", self.text)
        self.assertIn(
            "Do not make Asset Library `Preview` a completion gate",
            self.text,
        )
        self.assertIn("direct Notion-owned image block", self.text)

    def test_preview_wrapper_failures_are_documented_without_private_id_hack(self) -> None:
        self.assertIn('Preview=["file-upload://<id>"]', self.text)
        self.assertIn('Preview=["<raw-upload-id>"]', self.text)
        self.assertIn("User cannot access file id", self.text)
        self.assertIn(
            "does **not** spend additional complexity on reverse-engineering private Notion file IDs",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
