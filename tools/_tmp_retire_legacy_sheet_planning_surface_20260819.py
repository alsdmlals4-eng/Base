from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md"
text = path.read_text(encoding="utf-8")

text = text.replace(
    "# 프로젝트 기획 작업순서·Google Sheets GDD tab Template",
    "# 프로젝트 기획 작업순서 · Legacy Google Sheets migration inventory",
    1,
)
old_intro = "이 Template은 Base 자체가 아니라 Base를 적용한 개별 프로젝트에서 사용한다. 프로젝트 Google Sheets가 없거나 정확한 URL을 확인하지 못하면 `NOT_CONFIGURED`로 기록하고 새 Sheet나 임의 후보를 추정하지 않는다.\n\n공용 정책: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`"
new_intro = """`MIGRATION_ONLY_UNTIL_REMOVAL` · `GOOGLE_SHEETS_COMPATIBILITY_ONLY`

이 파일은 **기존 프로젝트의 Google Sheets에만 남아 있는 UNIQUE 정보를 해석·이관하기 위한 legacy inventory**다. 신규 프로젝트에 Sheet를 만들거나 tab을 설치하는 작업지시문이 아니며 active 계획·승인·동기화 정본도 아니다.

현재 active 사람용 계획/학습/시각 면은 **Project Notion Home + 필요한 drilldown pages**, 구조화·runtime truth는 **Project Repository**가 소유한다. 기존 Sheet가 실제 존재할 때만 `UNIQUE / DUPLICATE / OBSOLETE`를 판정하고 UNIQUE 자료를 현재 owner로 이관한 뒤 destination readback·consumer/reference 확인을 거쳐 retirement한다.

공용 정책: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

## 현재 active replacement

```text
Project Notion Home
→ 한 줄 정의 / 플레이어 가치 / 확정 방향 / Core Loop / 핵심 시스템
→ UX/UI/Visual / 구현상태 / 검증 evidence ceiling
→ blocker / 다음 작업 / 중요 결정 / 위험·revisit
→ 필요한 경우 하위 Notion page로 drilldown

Project Repository
→ 구조화 상태 / Markdown·JSON / code·Scene·Resource·asset / Test / runtime evidence
```

아래 tab 이름과 열 구조는 **legacy Sheet에서 UNIQUE 정보를 찾기 위한 migration mapping**으로만 유지한다."""
if old_intro not in text:
    raise SystemExit("legacy template intro anchor missing")
text = text.replace(old_intro, new_intro, 1)
text = text.replace("## 1. 설치할 tab", "## 1. Legacy tab inventory — 신규 설치 금지", 1)
text = text.replace(
    "위 11개는 **새 Sheet에 설치하는 권장 핵심 tab**이다. 다음은 기존 Sheet에만 남을 수 있는 호환 상세 tab의 참조 목록이며, 새 Sheet에 자동 생성하거나 사용자 승인 없이 이름을 바꾸지 않는다.",
    "위 11개는 과거 핵심 tab 이름을 보존한 **migration inventory**다. **새 Sheet/새 tab 설치는 금지**하며, 아래 상세 tab도 기존 Sheet의 UNIQUE 미이관 정보를 찾는 경우에만 읽는다. 기존 자료는 사용자 승인 없이 이름을 바꾸거나 삭제하지 않는다.",
    1,
)
text = text.replace(
    "## 4A. `06_시각_작업면` — 선택적 GDD·외부 협업 Artifact 색인\n\n실제 Figma·Whimsical·기타 시각 Artifact가 있을 때만 설치한다. 이 tab은 GDD 전용이 아니며 GDD 안·밖의 시각 작업면을 같은 계약으로 연결한다.",
    "## 4A. `06_시각_작업면` — legacy 시각 Artifact migration 색인\n\n기존 Sheet에 Figma·Whimsical·기타 폐기 surface 링크가 남아 있을 때만 **provenance/migration input**으로 읽는다. 새 Figma/Whimsical workspace 또는 tab을 만들지 않는다. 고유 시각 정보는 정확한 Project Notion/Repository owner로 이관하고 readback한 뒤 legacy reference 수명주기를 판정한다.",
    1,
)
path.write_text(text, encoding="utf-8", newline="\n")

# The new coordinator contract test is the semantic consumer for this migration-only assertion.
test_path = ROOT / "tests/test_sequential_part_coordinator_contract.py"
test = test_path.read_text(encoding="utf-8")
needle = "    def test_cross_part_request_is_only_for_real_coordination_blockers(self) -> None:\n"
insert = '''    def test_legacy_sheet_planning_template_is_migration_only(self) -> None:\n        text = (ROOT / "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md").read_text(encoding="utf-8")\n        self.assertIn("MIGRATION_ONLY_UNTIL_REMOVAL", text)\n        self.assertIn("GOOGLE_SHEETS_COMPATIBILITY_ONLY", text)\n        self.assertIn("Project Notion Home", text)\n        self.assertIn("신규 설치 금지", text)\n        self.assertIn("새 Sheet/새 tab 설치는 금지", text)\n        self.assertNotIn("새 Sheet에 설치하는 권장 핵심 tab", text)\n        self.assertNotIn("시각 Artifact가 있을 때만 설치한다", text)\n\n'''
if "test_legacy_sheet_planning_template_is_migration_only" not in test:
    if needle not in test:
        raise SystemExit("sequential test insertion anchor missing")
    test = test.replace(needle, insert + needle, 1)
test_path.write_text(test, encoding="utf-8", newline="\n")

config_path = ROOT / ".github/reference-freshness.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
for rule in config.get("coupled_change_rules", []):
    if rule.get("name") == "bca-visual-sheet-policy-sync":
        allowed = rule.setdefault("require_any_changed", [])
        companion = "tests/test_sequential_part_coordinator_contract.py"
        if companion not in allowed:
            allowed.append(companion)
        rule["semantic_note"] = "Legacy planning-Sheet migration-only semantics may be verified by the sequential coordinator contract; existing BCA/Sheet tests remain valid companions for their own owned policies."
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("LEGACY_SHEET_PLANNING_SURFACE_MIGRATED")
