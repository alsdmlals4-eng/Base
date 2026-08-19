from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "build_base_v9_artifacts.py"
DECISIONS = ROOT / "docs" / "operations" / "BASE_V9_DECISION_REGISTRY.json"
SHEET = ROOT / "docs" / "operations" / "SHEET_CONTROL_CONTRACT.json"

# Preserve BASE-V9-002 as released history, but make its supersession explicit and
# add a current migration-only decision for any future non-frozen reconstruction.
text = GENERATOR.read_text(encoding="utf-8")
old = '''            {"id": "BASE-V9-002", "status": "CONFIRMED", "decision": "Google Sheets remain USER_FACING_GDD_WORKSPACE for projects; Base is BASE_EXCLUDED."},
            {"id": "BASE-V9-003", "status": "CONFIRMED", "decision": "Project adoption is a post-release wave and must not block the Base v9.0.0 release."},
'''
new = '''            {"id": "BASE-V9-002", "status": "SUPERSEDED", "decision": "Google Sheets remain USER_FACING_GDD_WORKSPACE for projects; Base is BASE_EXCLUDED.", "superseded_by": "BASE-V9-004"},
            {"id": "BASE-V9-003", "status": "CONFIRMED", "decision": "Project adoption is a post-release wave and must not block the Base v9.0.0 release."},
            {"id": "BASE-V9-004", "status": "CONFIRMED", "decision": "Google Sheets are migration-only legacy sources; Notion is the human-facing project canon and repository structured/runtime truth remains authoritative."},
'''
if old in text:
    text = text.replace(old, new, 1)
elif '"id": "BASE-V9-004"' not in text:
    raise SystemExit("BASE-V9 decision generator anchor missing")
GENERATOR.write_text(text, encoding="utf-8", newline="\n")

# Released decision metadata keeps the old decision as history but marks it superseded.
data = json.loads(DECISIONS.read_text(encoding="utf-8"))
rows = data["decisions"]
old_row = next(row for row in rows if row["id"] == "BASE-V9-002")
old_row["status"] = "SUPERSEDED"
old_row["superseded_by"] = "BASE-V9-004"
if not any(row["id"] == "BASE-V9-004" for row in rows):
    rows.append({
        "id": "BASE-V9-004",
        "status": "CONFIRMED",
        "decision": "Google Sheets are migration-only legacy sources; Notion is the human-facing project canon and repository structured/runtime truth remains authoritative.",
    })
DECISIONS.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

# Current Sheet control is not an active GDD workspace.
sheet = json.loads(SHEET.read_text(encoding="utf-8"))
sheet.update({
    "active_project_workspace": False,
    "project_sheet_role": "MIGRATION_ONLY_LEGACY_SOURCE",
    "sheet_only_change_status": "MIGRATION_PROPOSAL_ONLY",
    "migration_policy": "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
    "human_facing_destination": "NOTION_HUMAN_FACING_CANON",
    "structured_destination": "REPOSITORY_STRUCTURED_CANON",
    "external_sheet_writes_authorized": False,
})
SHEET.write_text(json.dumps(sheet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print("PR530_SHEET_SUPERSESSION_FIXED")
