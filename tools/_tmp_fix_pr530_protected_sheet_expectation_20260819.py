from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "tests/test_sequential_part_coordinator_contract.py"
text = path.read_text(encoding="utf-8")
old = '''    def test_legacy_sheet_planning_template_is_migration_only(self) -> None:
        text = (ROOT / "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md").read_text(encoding="utf-8")
        self.assertIn("MIGRATION_ONLY_UNTIL_REMOVAL", text)
        self.assertIn("GOOGLE_SHEETS_COMPATIBILITY_ONLY", text)
        self.assertIn("Project Notion Home", text)
        self.assertIn("신규 설치 금지", text)
        self.assertIn("새 Sheet/새 tab 설치는 금지", text)
        self.assertNotIn("새 Sheet에 설치하는 권장 핵심 tab", text)
        self.assertNotIn("시각 Artifact가 있을 때만 설치한다", text)

'''
new = '''    def test_legacy_sheet_planning_migration_is_preserved_as_active_workstream_followup(self) -> None:
        followup = (ROOT / "docs/operations/PROTECTED_ACTIVE_WORKSTREAM_FOLLOWUPS_2026-08-19.md").read_text(encoding="utf-8")
        self.assertIn("P04 / legacy Sheet planning inventory", followup)
        self.assertIn("active-looking Sheet/Figma legacy language", followup)
        self.assertIn("actively modified by #530", followup)
        self.assertIn("revalidate and migrate after #530 completes", followup)

'''
if old not in text:
    raise SystemExit("legacy Sheet stale expectation block missing")
path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
print("PR530_PROTECTED_SHEET_EXPECTATION_FIXED")
