from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
AGENTS_FRAGMENT = ROOT / "templates/project-operations/godot-live-editor/AGENTS_FRAGMENT.md"


class GodotAdapterResolutionTests(unittest.TestCase):
    def test_project_adapter_resolves_base_contract_through_validated_adapter(self) -> None:
        combined = ADAPTER.read_text(encoding="utf-8") + AGENTS_FRAGMENT.read_text(encoding="utf-8")

        for term in (
            "PROJECT_BASE_ADAPTER.json",
            "validated Base adapter",
            "Base canonical contract",
        ):
            self.assertIn(term, combined)


if __name__ == "__main__":
    unittest.main()
