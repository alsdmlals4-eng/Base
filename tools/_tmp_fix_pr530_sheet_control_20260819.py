from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs" / "operations" / "SHEET_CONTROL_CONTRACT.json"

data = json.loads(PATH.read_text(encoding="utf-8"))
data["project_sheet_role"] = "MIGRATION_ONLY_LEGACY_SOURCE"
data["sheet_only_change_status"] = "MIGRATION_PROPOSAL_ONLY"
data["external_sheet_writes_authorized"] = False
data["active_project_workspace"] = False
data["migration_policy"] = "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL"
data["human_facing_destination"] = "NOTION_HUMAN_FACING_CANON"
data["structured_destination"] = "REPOSITORY_STRUCTURED_CANON"
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("PR530_SHEET_CONTROL_MIGRATION_APPLIED")
