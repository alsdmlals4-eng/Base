from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-capability-manifest-v2.schema.json"
OPERATION_SCHEMA_V2 = ROOT / "schemas/godot-live-editor-operation-envelope-v2.schema.json"
SEMANTIC_VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract_v2.py"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md"
V2_TEMPLATE = ROOT / "templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
V1_PILOT_MANIFEST = ROOT / "examples/godot-live-editor-pilot/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


class GodotLiveEditorContractV2Tests(unittest.TestCase):
    maxDiff = None

    def test_v2_contract_artifacts_exist(self) -> None:
        required = (
            CAPABILITY_SCHEMA_V2,
            OPERATION_SCHEMA_V2,
            SEMANTIC_VALIDATOR,
            DESIGN,
        )
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
