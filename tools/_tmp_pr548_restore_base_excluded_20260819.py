from pathlib import Path

p = Path('docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md')
text = p.read_text(encoding='utf-8')
old = "Google Sheets\n→ `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`"
new = "Google Sheets\n→ `BASE_EXCLUDED` (Base repository)\n→ `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` (legacy project sources only)"
if old not in text:
    raise SystemExit('planning Sheet anchor missing')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8', newline='\n')
print('PR548_BASE_EXCLUDED_RESTORED')
