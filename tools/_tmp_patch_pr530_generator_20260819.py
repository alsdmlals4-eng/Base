from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "tools" / "build_base_v9_artifacts.py"
text = path.read_text(encoding="utf-8")
old = '''        "project_sheet_role": "USER_FACING_GDD_WORKSPACE",
        "sheet_only_change_status": "PROPOSED_SHEET_CHANGE",
'''
new = '''        "project_sheet_role": "MIGRATION_ONLY_LEGACY_SOURCE",
        "sheet_only_change_status": "MIGRATION_PROPOSAL_ONLY",
'''
if old not in text:
    raise SystemExit("sheet generator anchor missing")
path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
print("PR530_GENERATOR_PATCH_APPLIED")
