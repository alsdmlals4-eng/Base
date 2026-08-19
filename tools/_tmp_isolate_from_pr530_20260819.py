from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def restore_from_main(path: str) -> None:
    proc = subprocess.run(
        ["git", "show", f"origin/main:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    (ROOT / path).write_bytes(proc.stdout)


# Exact paths already owned by active independent PR #530: keep #544 out.
for path in (
    ".github/reference-freshness.json",
    "AGENTS.md",
    "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
    "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",
    "skills/managing-game-project-operating-system/SKILL.md",
):
    restore_from_main(path)

# Semantic Sheet-policy/test work is also active in #530; preserve it rather than
# forcing a new policy/test interpretation from the coordinator PR.
restore_from_main("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")

# The P02 strict-alias parser improvement needs reference-freshness config semantics
# that #530 currently edits. Defer it instead of manufacturing a conflict.
for path in (
    "skills/LEGACY_SKILL_ALIASES.md",
    "tools/check_canonical_reference_freshness.py",
    "tests/test_reference_freshness.py",
    "tests/test_consolidated_skill_references.py",
):
    restore_from_main(path)

# Dedicated conflict-free global policy for the corrected adversarial-loop meaning.
full_loop = ROOT / "docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"
full_loop.write_text(
    '''# Full Adversarial Review Loop Policy\n\n'
    '`FULL_LOOP_IS_NOT_A_REVIEW_LENS`\n\n'
    'Base의 `FULL_LOOP_COUNT_MINIMUM: 5`는 서로 다른 관점 다섯 개를 한 번씩 보는 뜻이 아니다. **한 counted loop가 아래 전체 lifecycle을 모두 수행**하고, 개선된 결과에 대해 이 lifecycle을 최소 5번 반복한다.\n\n'
    '```text\n'
    'CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK\n'
    '→ MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK\n'
    '→ FULL-SCOPE ATTACK\n'
    '→ VALIDATE CRITIQUE\n'
    '→ FIX / REFINE VERIFIED FINDINGS\n'
    '→ EXECUTION / REGRESSION / REFERENCE VERIFICATION\n'
    '→ BETTER_ALTERNATIVE_SEARCH\n'
    '→ LONG_TERM_PLAN_FIT_RECHECK\n'
    '→ RE-ATTACK THE WHOLE RESULTING STATE\n'
    '```\n\n'
    '`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`, `Loop 4=long-term`, `Loop 5=review`처럼 **관점 하나를 loop 하나로 계수하지 않는다**. Scope, UX, CI, security, cost, consumer, rollback 등은 각 full loop 내부의 attack coverage다.\n\n'
    '회차 보고에 대표 finding을 적는 것은 허용하지만, 대표 finding이 회차의 전체 범위를 뜻하지 않는다. 최소 5회 후에도 유효 오류·충돌·누락·blocking finding·회귀·acceptance failure가 있으면 6..N회를 계속한다.\n'''.replace("'''#", "#").replace("\\n'\n    '", "\n").replace("\\n'\n", "\n").replace("'", ""),
    encoding="utf-8",
    newline="\n",
)

# Dedicated conflict-free policy for human-facing Home requirements. #530 may later
# absorb it into its Project OS schema, but #544 does not edit #530-owned files.
home = ROOT / "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md"
home.write_text(
    """# Human Home Self-Contained Policy\n\n"
    "`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`\n\n"
    "Notion의 Base Home과 Project Home은 링크 허브가 아니라 사람이 **추가 이동 없이 핵심을 이해하는 첫 화면**이다. GitHub/Repository의 structured/runtime truth를 복제해 새 정본을 만드는 것이 아니라, latest merged facts와 사용자 확정 방향을 사람이 읽기 쉬운 형태로 투영한다.\n\n"
    "## Base Home 필수 내용\n\n"
    "- Base 목적과 Notion/GitHub authority split\n"
    "- 전체 작업 lifecycle과 각 단계의 존재 이유\n"
    "- 중요 규칙과 작동 조건\n"
    "- active Skill별 **Skill 목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / 연결 Module·consumer·Test**\n"
    "- Module별 입력→판단/처리→출력→다음 consumer와 **없으면** 생기는 실패\n"
    "- P01~P09 책임·대표 Skill/Module·진행 흐름·연결·기대효과·위험/revisit\n"
    "- current main, 완료/미완료 workstream, 실제 검증과 `NOT_RUN`\n\n"
    "## Project Home 필수 내용\n\n"
    "1. 프로젝트 한 줄 정의\n"
    "2. 핵심 플레이어/사용자 가치\n"
    "3. 현재 확정 방향과 보호/금지 요소\n"
    "4. Core Loop / 주요 Flow\n"
    "5. 핵심 시스템별 목적·작동·상호작용\n"
    "6. UX/UI/Visual 방향·승인 상태\n"
    "7. 현재 구현상태와 Repository/runtime truth 연결\n"
    "8. 검증상태와 static/runtime/device/human/accessibility/platform/store evidence ceiling\n"
    "9. 현재 blocker / 다음 작업\n"
    "10. 최근 중요한 결정과 이유\n"
    "11. 주요 위험 / revisit condition\n\n"
    "하위 페이지는 `drilldown`이다. 긴 표·전체 asset·reference·로그·세부 수치·evidence를 보관하되 Home의 핵심 설명을 '상세는 링크 참조'로 대체하지 않는다.\n",
    encoding="utf-8",
    newline="\n",
)

# Ensure the conflict-free Notion operating contract points to the dedicated policy.
notion_path = ROOT / "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
notion = notion_path.read_text(encoding="utf-8")
if "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md" not in notion:
    notion = notion.rstrip() + (
        "\n\n## Human Home 상세 정책\n\n"
        "`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`의 Base/Project Home 필수 내용은 "
        "`docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`가 소유한다. 하위 페이지는 drilldown/evidence이며 core understanding을 대신하지 않는다.\n"
    )
notion_path.write_text(notion.rstrip() + "\n", encoding="utf-8", newline="\n")

# Rewrite new tests so they verify conflict-free canonical owners rather than #530 files.
full_test = ROOT / "tests/test_full_adversarial_loop_semantics.py"
full_test.write_text(
    '''from __future__ import annotations\n\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nPOLICY = ROOT / "docs" / "operations" / "FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"\nOPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"\nAGENTS = ROOT / "AGENTS.md"\n\n\nclass FullAdversarialLoopSemanticsTests(unittest.TestCase):\n    def authoritative_text(self) -> str:\n        return POLICY.read_text(encoding="utf-8") + "\\n" + OPERATING_MODEL.read_text(encoding="utf-8")\n\n    def test_base_still_requires_minimum_five_full_loops(self) -> None:\n        agents = AGENTS.read_text(encoding="utf-8")\n        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", agents)\n        self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", agents)\n\n    def test_full_loop_is_not_a_review_lens(self) -> None:\n        text = self.authoritative_text()\n        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)\n        self.assertIn("관점 하나", text)\n        self.assertIn("최소 5", text)\n\n    def test_each_counted_loop_repeats_the_complete_lifecycle(self) -> None:\n        text = self.authoritative_text()\n        for term in (\n            "CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK",\n            "MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK",\n            "FULL-SCOPE ATTACK",\n            "VALIDATE CRITIQUE",\n            "FIX / REFINE VERIFIED FINDINGS",\n            "EXECUTION / REGRESSION / REFERENCE VERIFICATION",\n            "BETTER_ALTERNATIVE_SEARCH",\n            "LONG_TERM_PLAN_FIT_RECHECK",\n            "RE-ATTACK THE WHOLE RESULTING STATE",\n        ):\n            self.assertIn(term, text)\n\n    def test_lens_split_examples_are_explicitly_rejected(self) -> None:\n        text = self.authoritative_text()\n        self.assertIn("Loop 1=scope", text)\n        self.assertIn("Loop 2=UX", text)\n        self.assertIn("Loop 3=CI", text)\n        self.assertIn("계수하지 않는다", text)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''',
    encoding="utf-8",
    newline="\n",
)

home_test = ROOT / "tests/test_human_home_self_contained_contract.py"
home_test.write_text(
    '''from __future__ import annotations\n\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nPOLICY = ROOT / "docs" / "operations" / "HUMAN_HOME_SELF_CONTAINED_POLICY.md"\nNOTION_CONTRACT = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"\nBASE_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"\n\n\nclass HumanHomeSelfContainedContractTests(unittest.TestCase):\n    def test_project_home_is_self_contained_before_drilldown(self) -> None:\n        text = POLICY.read_text(encoding="utf-8")\n        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)\n        for term in (\n            "프로젝트 한 줄 정의", "핵심 플레이어/사용자 가치", "현재 확정 방향",\n            "Core Loop", "핵심 시스템", "UX/UI/Visual", "현재 구현상태", "검증상태",\n            "현재 blocker", "다음 작업", "최근 중요한 결정", "주요 위험", "revisit condition",\n        ):\n            self.assertIn(term, text)\n        self.assertIn("drilldown", text)\n\n    def test_notion_contract_routes_to_self_contained_home_policy(self) -> None:\n        text = NOTION_CONTRACT.read_text(encoding="utf-8")\n        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)\n        self.assertIn("docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md", text)\n\n    def test_base_home_contract_is_self_contained_for_learning(self) -> None:\n        text = POLICY.read_text(encoding="utf-8") + "\\n" + BASE_MODEL.read_text(encoding="utf-8")\n        for term in (\n            "Skill 목적", "호출 조건", "입력", "처리", "출력", "기대효과",\n            "Module", "없으면", "P01~P09",\n        ):\n            self.assertIn(term, text)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''',
    encoding="utf-8",
    newline="\n",
)

# Record protected follow-ups instead of silently losing the valid findings.
followup = ROOT / "docs/operations/PROTECTED_ACTIVE_WORKSTREAM_FOLLOWUPS_2026-08-19.md"
followup.write_text(
    """# Protected active-workstream follow-ups · 2026-08-19\n\n"
    "These findings remain valid but are not rewritten by the sequential coordinator PR because active independent PR #530 owns the same policy/test surface.\n\n"
    "## P01 / Project workspace schema consumer\n"
    "- current completed main has schema v2 while `tests/test_notion_project_workspace_contract.py` still asserts v1.\n"
    "- active PR #530 already changes this consumer and advances the workspace contract toward schema v3.\n"
    "- coordinator disposition: `DUPLICATE_ACTIVE_WORKSTREAM / READ_ONLY`; recheck after #530 completes.\n\n"
    "## P02 / strict multi-alias legacy parser\n"
    "- multi-alias stale-ID parsing remains a valid robustness improvement.\n"
    "- implementing it requires `.github/reference-freshness.json` companion semantics currently edited by #530.\n"
    "- coordinator disposition: `DEFER_PROTECTED_ACTIVE_WORKSTREAM`; do not lose the finding.\n\n"
    "## P04 / legacy Sheet planning inventory\n"
    "- `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md` still contains active-looking Sheet/Figma legacy language on completed main.\n"
    "- its canonical migration policy/tests are actively modified by #530.\n"
    "- coordinator disposition: preserve main file during #530; revalidate and migrate after #530 completes.\n\n"
    "## Human Home absorption into Project OS\n"
    "- the new self-contained Home policy is implemented in a conflict-free canonical document and Notion contract.\n"
    "- `skills/managing-game-project-operating-system/SKILL.md` and `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` are #530-owned active paths, so direct absorption is deferred until #530 completion.\n",
    encoding="utf-8",
    newline="\n",
)

print("PR530_ACTIVE_WORKSTREAM_ISOLATION_APPLIED")
