from __future__ import annotations

import json
from pathlib import Path

path = Path('.github/reference-freshness.json')
data = json.loads(path.read_text(encoding='utf-8'))
rule = next(
    item for item in data['coupled_change_rules']
    if item['name'] == 'skill-description-learning-test-sync'
)
companions = rule['require_any_changed']
for item in ('tests/test_bca_visual_sheet_workflow.py', 'tests/test_p0[1-9]_*.py'):
    if item not in companions:
        companions.append(item)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('PR548_FRESHNESS_COMPANIONS_UPDATED')
