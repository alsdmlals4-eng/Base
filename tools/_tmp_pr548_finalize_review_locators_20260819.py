from __future__ import annotations

import json
from pathlib import Path

REVIEWED_HEAD = "e8730f8f1804fa951260713f0e6d7f9220c62f4b"
TARGETS = {
    "managing-project-intake-and-work-contract",
    "managing-game-project-operating-system",
    "managing-design-documents",
    "building-project-visual-dashboards",
}

path = Path("skills/SKILL_REGISTRY.json")
data = json.loads(path.read_text(encoding="utf-8"))
seen = set()
for row in data["skills"]:
    if row["skill_id"] in TARGETS:
        if row.get("last_reviewed_commit") != "PENDING_PR530_SELECTIVE_INTEGRATION":
            raise SystemExit(f"unexpected review locator for {row['skill_id']}: {row.get('last_reviewed_commit')}")
        row["last_reviewed_commit"] = REVIEWED_HEAD
        seen.add(row["skill_id"])
if seen != TARGETS:
    raise SystemExit(f"missing target rows: {sorted(TARGETS - seen)}")
path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
print("PR548_REVIEW_LOCATORS_FINALIZED")
