from pathlib import Path

root = Path(__file__).resolve().parents[1]
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
print("PR548_CANONICAL_TOKENS_NORMALIZED")
