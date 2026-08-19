from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
test_path = ROOT / "tests/test_base_partition_contract.py"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
paths = p05["owned_write_paths"]
old = "docs/knowledge/game-development/*UI*"
new = "docs/knowledge/game-development/UI_*"
if old not in paths:
    raise SystemExit(f"expected broad P05 UI glob missing: {old}")
paths[paths.index(old)] = new
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

text = test_path.read_text(encoding="utf-8")
if 'SKILL_REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"' not in text:
    text = text.replace(
        'LEARNING_SYSTEM = ROOT / "docs" / "operations" / "BASE_PARTITION_LEARNING_SYSTEM.md"\n',
        'LEARNING_SYSTEM = ROOT / "docs" / "operations" / "BASE_PARTITION_LEARNING_SYSTEM.md"\n'
        'SKILL_REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"\n',
        1,
    )
text, count = re.subn(
    r'\nEXPECTED_SKILLS = \{.*?\n\}\n',
    '\n\ndef active_registry_skill_ids() -> set[str]:\n'
    '    registry = json.loads(SKILL_REGISTRY.read_text(encoding="utf-8"))\n'
    '    excluded = set(registry.get("routing_policy", {}).get("exclude_statuses", []))\n'
    '    return {\n'
    '        row["skill_id"]\n'
    '        for row in registry.get("skills", [])\n'
    '        if row.get("status") not in excluded\n'
    '    }\n',
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"expected one static EXPECTED_SKILLS block, got {count}")
text = text.replace(
    '        self.assertEqual(EXPECTED_SKILLS, set(assignments))\n',
    '        self.assertEqual(active_registry_skill_ids(), set(assignments))\n',
    1,
)
needle = '    def test_each_part_has_a_context_pack_and_operational_contract(self) -> None:\n'
insert = '''    def test_p05_ui_glob_does_not_capture_generic_guide_suffix(self) -> None:\n        manifest = self.load_manifest()\n        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")\n        self.assertNotIn("docs/knowledge/game-development/*UI*", p05["owned_write_paths"])\n        self.assertIn("docs/knowledge/game-development/UI_*", p05["owned_write_paths"])\n\n'''
if insert not in text:
    text = text.replace(needle, insert + needle, 1)
test_path.write_text(text, encoding="utf-8", newline="\n")
print("PARTITION_SEMANTIC_OWNERSHIP_HARDENED")
