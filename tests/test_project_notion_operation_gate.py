from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS_TEMPLATE = ROOT / "templates" / "AGENTS.project.md"
PROJECT_OPERATIONS = ROOT / "templates" / "project-operations" / "README.md"


class ProjectNotionOperationGateTests(unittest.TestCase):
    def test_project_agents_routes_notion_mutations_through_safe_bounded_gate(self) -> None:
        text = AGENTS_TEMPLATE.read_text(encoding="utf-8")
        for required in (
            "NOTION_OPERATION_GATE",
            "PAGE_BLOCK",
            "DATABASE_RECORD",
            "VIEW_PRESENTATION",
            "DATA_SOURCE_SCHEMA_OR_RECORD",
            "fetch/read",
            "smallest bounded edit",
            "destination readback",
            "allow_deleting_content",
            "사용자 확인",
        ):
            self.assertIn(required, text)

    def test_project_operations_distinguishes_notion_automation_and_webhook_roles(self) -> None:
        text = PROJECT_OPERATIONS.read_text(encoding="utf-8")
        for required in (
            "NOTION_OPERATION_GATE",
            "Webhook action",
            "Integration webhook",
            "Database automation",
            "자동 연쇄 실행을 전제로 설계하지 않는다",
            "secret",
            "destination readback",
        ):
            self.assertIn(required, text)

    def test_project_operations_preserves_human_home_and_runtime_authority_boundaries(self) -> None:
        text = PROJECT_OPERATIONS.read_text(encoding="utf-8")
        self.assertIn("NOTION_HUMAN_FACING_CANON", text)
        self.assertIn("REPOSITORY_STRUCTURED_CANON", text)
        self.assertIn("사람용 Home", text)
        self.assertIn("AI/System", text)
        self.assertIn("runtime truth", text)


if __name__ == "__main__":
    unittest.main()
