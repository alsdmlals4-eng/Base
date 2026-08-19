from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
MANAGING = ROOT / "skills" / "managing-design-documents" / "SKILL.md"
MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"


class NotionProjectIsolationCoreSystemContractTests(unittest.TestCase):
    def test_workspace_authority_declares_project_isolation_and_core_system_master(self) -> None:
        contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))

        self.assertEqual("PROJECT_NAMESPACE_ISOLATION", contract["parallel_project_write_model"])
        self.assertEqual("CORE_SYSTEM_MASTER", contract["core_system_master"])
        self.assertEqual("OPTIMISTIC_CONFLICT_DETECTION", contract["same_record_concurrency"])
        self.assertEqual("BOUNDED_RECORD_WRITE", contract["notion_write_mode"])
        self.assertIn("SYSTEM", contract["required_project_record_types"])
        self.assertIn("Record Key", contract["core_system_identity_fields"])
        self.assertIn("Revision", contract["core_system_identity_fields"])
        self.assertIn("Last Edited", contract["core_system_identity_fields"])
        self.assertIn("CONFLICT_STALE_READ", contract["conflict_states"])
        self.assertIn("CONFLICT_DUPLICATE_KEY", contract["conflict_states"])

        invariants = "\n".join(contract["invariants"])
        for required in (
            "exactly one Project relation",
            "deterministic Record Key",
            "Revision and Last Edited",
            "bounded record-level update",
            "stale read",
            "destination readback",
        ):
            self.assertIn(required, invariants)

    def test_managing_design_documents_has_fail_closed_parallel_write_protocol(self) -> None:
        text = MANAGING.read_text(encoding="utf-8")
        for required in (
            "PROJECT_NAMESPACE_ISOLATION",
            "CORE SYSTEM · Master",
            "<ProjectKey>::<RecordType>::<LocalId>",
            "Revision",
            "Last Edited",
            "CONFLICT_STALE_READ",
            "CONFLICT_DUPLICATE_KEY",
            "bounded field-level update",
            "destination readback",
        ):
            self.assertIn(required, text)

        self.assertIn("다른 Project relation", text)
        self.assertIn("전체 `replace_content`", text)

    def test_documentation_map_routes_core_system_human_surface(self) -> None:
        text = MAP.read_text(encoding="utf-8")
        for required in (
            "CORE SYSTEM · Master",
            "08 · 핵심 시스템 · 상세",
            "Project namespace",
            "Record Key",
            "optimistic conflict",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
