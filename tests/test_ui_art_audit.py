from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "auditing-and-refining-ui-art" / "scripts" / "scan_ui_art_signals.py"
SCHEMA = ROOT / "schemas" / "ui-art-findings-v1.schema.json"
FIXTURES = ROOT / "tests" / "fixtures" / "ui-art"
INVENTORY = ROOT / "docs" / "knowledge" / "research" / "inventories" / "slopslap-6b5dae1e.json"

SPEC = importlib.util.spec_from_file_location("scan_ui_art_signals", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


class UiArtAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))

    def test_web_fixture_reports_all_five_areas(self) -> None:
        report = MODULE.scan(FIXTURES / "web" / "risky", "web")
        self.validator.validate(report)
        self.assertEqual({"A", "B", "C", "D", "E"}, {item["area"] for item in report["findings"]})
        self.assertTrue(all(item["status"] == "CANDIDATE" for item in report["findings"]))

    def test_slopslap_source_inventory_is_complete_and_classified(self) -> None:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual("6b5dae1efaa319d7bb015ee5c2d593933b92911b", inventory["commit"])
        self.assertEqual(51, inventory["tracked_file_count"])
        self.assertEqual(51, len(inventory["files"]))
        self.assertNotIn("unclassified", inventory["role_counts"])
        self.assertEqual(27, inventory["role_counts"]["asset"])
        self.assertTrue(all(item["role"] != "unclassified" for item in inventory["files"]))

    def test_godot_fixture_reports_all_five_areas(self) -> None:
        report = MODULE.scan(FIXTURES / "godot" / "risky", "godot")
        self.validator.validate(report)
        self.assertEqual({"A", "B", "C", "D", "E"}, {item["area"] for item in report["findings"]})

    def test_intentional_design_directives_preserve_effects(self) -> None:
        web = MODULE.scan(FIXTURES / "web" / "intentional", "web")
        godot = MODULE.scan(FIXTURES / "godot" / "intentional", "godot")
        self.assertNotIn("A", {item["area"] for item in web["findings"]})
        self.assertNotIn("E", {item["area"] for item in godot["findings"]})
        self.assertEqual("W-A-DECORATIVE-EFFECT", web["suppressions"][0]["rule_id"])
        self.assertEqual("G-E-COLOR-LITERAL", godot["suppressions"][0]["rule_id"])
        with tempfile.TemporaryDirectory() as tmp:
            unapproved = Path(tmp) / "accent.gd"
            source = (FIXTURES / "godot" / "intentional" / "accent.gd").read_text(encoding="utf-8")
            unapproved.write_text("\n".join(line for line in source.splitlines() if "base-ui-audit: allow" not in line), encoding="utf-8")
            self.assertIn("E", {item["area"] for item in MODULE.scan(unapproved, "godot")["findings"]})

    def test_scanner_does_not_modify_target_before_approval(self) -> None:
        before = tree_hash(FIXTURES)
        MODULE.scan(FIXTURES, "auto")
        self.assertEqual(before, tree_hash(FIXTURES))

    def test_approved_change_is_visible_to_fresh_reaudit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "ui"
            shutil.copytree(FIXTURES / "web" / "risky", work)
            before = MODULE.scan(work, "web")
            css = work / "style.css"
            css.write_text(
                ".panel {\n  max-width: 58rem;\n  padding: 1rem;\n  background: var(--surface);\n  color: var(--text);\n  font-size: 1rem;\n}\n",
                encoding="utf-8",
            )
            after = MODULE.scan(work, "web")
            self.assertGreater(len(before["findings"]), len(after["findings"]))
            self.assertEqual([], after["findings"])

    def test_markdown_calls_results_candidates_not_confirmed_defects(self) -> None:
        report = MODULE.scan(FIXTURES / "web" / "risky", "web")
        markdown = MODULE.render_markdown(report)
        self.assertIn("정적 패턴 후보", markdown)
        self.assertIn("결함 확정이나 자동 수정 지시가 아닙니다", markdown)


if __name__ == "__main__":
    unittest.main()
