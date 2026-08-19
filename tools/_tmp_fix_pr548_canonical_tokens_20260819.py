import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]

# 1. Normalize planning-policy tokens to current Base canon.
path = root / "docs" / "PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md"
text = path.read_text(encoding="utf-8")
replacements = {
    "GPT_PRIMARY_PLANNING_REVIEW": "GPT_FIRST_PLANNING_AND_REVIEW",
    "GPT_FINAL_REVIEW_AUTHORITY": "GPT_PRIMARY_REVIEWER",
    "CODEX_OPTIONAL_SUB_EXECUTOR": "OPTIONAL_CODEX_EXECUTOR",
    "NOTION_VISUAL_CHECKPOINT_BEFORE_POC": "VISUALIZED_POC_BEFORE_DEMO_TEST",
    "UX_UI_REPRESENTATIVE_STATE_REQUIRED": "REPRESENTATIVE_UX_UI_STATE_REQUIRED_WHEN_VISUALS_MATTER",
    "APPROVED_VISUALS_FEED_POC": "APPROVED_VISUAL_INPUTS_FEED_POC",
}
for old, new in replacements.items():
    text = text.replace(old, new)
path.write_text(text, encoding="utf-8", newline="\n")

# 2. Preserve BASE-V9-002 as superseded history and add the current migration-only decision.
generator_path = root / "tools" / "build_base_v9_artifacts.py"
generator = generator_path.read_text(encoding="utf-8")
old_decision = '{"id": "BASE-V9-002", "status": "CONFIRMED", "decision": "Google Sheets remain USER_FACING_GDD_WORKSPACE for projects; Base is BASE_EXCLUDED."},'
new_decisions = '{"id": "BASE-V9-002", "status": "SUPERSEDED", "superseded_by": "BASE-V9-004", "decision": "Historical project Google Sheets workspace authority; no longer current."},\n            {"id": "BASE-V9-004", "status": "CONFIRMED", "decision": "Google Sheets are migration-only legacy sources until unique material is absorbed and active references are removed."},'
if old_decision not in generator and '"id": "BASE-V9-004"' not in generator:
    raise SystemExit("BASE-V9-002 generator anchor missing")
if old_decision in generator:
    generator = generator.replace(old_decision, new_decisions, 1)
generator_path.write_text(generator, encoding="utf-8", newline="\n")

# 3. Released Base v9 artifacts are intentionally frozen by the generator, so migrate the decision registry explicitly.
decisions_path = root / "docs" / "operations" / "BASE_V9_DECISION_REGISTRY.json"
data = json.loads(decisions_path.read_text(encoding="utf-8"))
rows = data["decisions"]
old = next(row for row in rows if row["id"] == "BASE-V9-002")
old["status"] = "SUPERSEDED"
old["superseded_by"] = "BASE-V9-004"
old["decision"] = "Historical project Google Sheets workspace authority; no longer current."
if not any(row["id"] == "BASE-V9-004" for row in rows):
    rows.append({
        "id": "BASE-V9-004",
        "status": "CONFIRMED",
        "decision": "Google Sheets are migration-only legacy sources until unique material is absorbed and active references are removed.",
    })
decisions_path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print("PR548_CANONICAL_TOKENS_AND_DECISION_HISTORY_NORMALIZED")
