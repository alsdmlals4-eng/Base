from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = (
    ROOT
    / "docs"
    / "knowledge"
    / "methods"
    / "NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md"
)
P01 = (
    ROOT
    / "docs"
    / "operations"
    / "base-partitions"
    / "P01_PROJECT_PLANNING_OPERATIONS_NOTION.md"
)
VISUAL_LAYOUT = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md"
)


class NotionOfficialProductOperatingReferenceTests(unittest.TestCase):
    def test_reference_covers_object_scope_layout_media_permissions_and_agents(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        for contract in (
            "NOTION_OBJECT_SCOPE_BEFORE_WRITE",
            "VIEW_PRESENTATION != SOURCE_MUTATION",
            "NOTION_DATABASE_GLOBAL_LAYOUT_IMPACT_GATE",
            "NOTION_MOBILE_STACK_SEMANTIC_ORDER_REQUIRED",
            "NOTION_GALLERY_EXPLICIT_MEDIA_PREVIEW",
            "NOTION_FILE_LIMIT_CLAIM_CONFLICT_GUARD",
            "NOTION_PREVIEW_MASTER_SEPARATION",
            "NOTION_UPLOAD_ATTACH_READBACK_LIFECYCLE",
            "NOTION_SYNCED_CONTENT_SHARED_IDENTITY_ONLY",
            "NOTION_PERMISSION_TRANSITIVE_SOURCE_CHECK",
            "PERSONAL_NOTION_AGENT_USER_PERMISSION_INHERITANCE",
            "CUSTOM_AGENT_EXPLICIT_RESOURCE_ACCESS",
            "NOTION_PAID_SURFACE_NOT_BASE_DEPENDENCY",
        ):
            self.assertIn(contract, text)

        for official_source in (
            "https://www.notion.com/ko/product",
            "https://www.notion.com/help/data-sources-and-linked-databases",
            "https://www.notion.com/help/layouts",
            "https://www.notion.com/help/columns-headings-and-dividers",
            "https://www.notion.com/help/galleries",
            "https://www.notion.com/ko/help/images-files-and-media",
            "https://www.notion.com/help/notion-agent",
            "https://www.notion.com/help/custom-agents",
            "https://developers.notion.com/reference/file-upload",
        ):
            self.assertIn(official_source, text)

    def test_file_limit_conflict_is_preserved_as_a_guard_not_a_universal_cap(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        self.assertIn("5MB", text)
        self.assertIn("5GB", text)
        self.assertIn("INLINE_IMAGE_DISPLAY_SAFE_TARGET", text)
        self.assertIn("SOURCE_MASTER_OR_LARGE_FILE", text)
        self.assertIn("단일 숫자를 모든 upload/render 경로의 hard cap으로 일반화하지 않는다", text)

    def test_p01_progressively_loads_the_official_product_reference(self) -> None:
        text = P01.read_text(encoding="utf-8")

        self.assertIn("NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE_REQUIRED", text)
        self.assertIn("NOTION_OBJECT_SCOPE_BEFORE_WRITE", text)
        self.assertIn("NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md", text)

    def test_visual_layout_consumes_mobile_gallery_layout_and_file_guards(self) -> None:
        text = VISUAL_LAYOUT.read_text(encoding="utf-8")

        for contract in (
            "NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md",
            "NOTION_FILE_LIMIT_CLAIM_CONFLICT_GUARD",
            "NOTION_PREVIEW_MASTER_SEPARATION",
            "NOTION_GALLERY_EXPLICIT_MEDIA_PREVIEW",
            "NOTION_MOBILE_STACK_SEMANTIC_ORDER_REQUIRED",
            "NOTION_DATABASE_GLOBAL_LAYOUT_IMPACT_GATE",
        ):
            self.assertIn(contract, text)

        self.assertIn("phone clients do not preserve desktop multi-column geometry", text)
        self.assertIn("database page layout applies across the database", text)
        self.assertIn("typed attach", text)


if __name__ == "__main__":
    unittest.main()
