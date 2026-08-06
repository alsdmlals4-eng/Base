from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
AGENTS_FRAGMENT = ROOT / "templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md"
POLICY = ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"


class GodotAdapterResolutionTests(unittest.TestCase):
    def test_project_skill_routes_higodot_while_base_adapter_remains_auditable(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        fragment = AGENTS_FRAGMENT.read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")

        self.assertIn("hi-godot/godot-ai", adapter)
        self.assertIn("SOLE_GODOT_EXECUTION_AUTHORITY", adapter)
        self.assertIn(str(POLICY.relative_to(ROOT)).replace("\\", "/"), adapter)
        self.assertNotIn("base_live_editor_adapter/", adapter)

        for term in ("PROJECT_BASE_ADAPTER.json", "validated Base adapter"):
            self.assertIn(term, fragment)
        self.assertIn("과거 Base", adapter)
        self.assertIn("감사", adapter)
        self.assertIn("ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION", policy)


if __name__ == "__main__":
    unittest.main()
