from __future__ import annotations

import json
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


for path in (
    ".github/reference-freshness.json",
    "AGENTS.md",
    "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
    "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",
    "skills/managing-game-project-operating-system/SKILL.md",
):
    restore_from_main(path)

restore_from_main("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")

for path in (
    "skills/LEGACY_SKILL_ALIASES.md",
    "tools/check_canonical_reference_freshness.py",
    "tests/test_reference_freshness.py",
    "tests/test_consolidated_skill_references.py",
):
    restore_from_main(path)

manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
p01 = next(p for p in manifest["parts"] if p["part_id"] == "P01")
contract_path = "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
if contract_path not in p01["owned_write_paths"]:
    p01["owned_write_paths"].append(contract_path)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

full_loop = ROOT / "docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"
full_loop.write_text(
    """# Full Adversarial Review Loop Policy

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

Base의 `FULL_LOOP_COUNT_MINIMUM: 5`는 서로 다른 관점 다섯 개를 한 번씩 보는 뜻이 아니다. **한 counted loop가 아래 전체 lifecycle을 모두 수행**하고, 개선된 결과에 대해 이 lifecycle을 최소 5번 반복한다.

```text
CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK
→ MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK
→ FULL-SCOPE ATTACK
→ VALIDATE CRITIQUE
→ FIX / REFINE VERIFIED FINDINGS
→ EXECUTION / REGRESSION / REFERENCE VERIFICATION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK THE WHOLE RESULTING STATE
```

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`, `Loop 4=long-term`, `Loop 5=review`처럼 **관점 하나를 loop 하나로 계수하지 않는다**. Scope, UX, CI, security, cost, consumer, rollback 등은 각 full loop 내부의 attack coverage다.

회차 보고에 대표 finding을 적는 것은 허용하지만, 대표 finding이 회차의 전체 범위를 뜻하지 않는다. 최소 5회 후에도 유효 오류·충돌·누락·blocking finding·회귀·acceptance failure가 있으면 6..N회를 계속한다.
""",
    encoding="utf-8",
    newline="\n",
)

home = ROOT / "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md"
home.write_text(
    """# Human Home Self-Contained Policy

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Notion의 Base Home과 Project Home은 링크 허브가 아니라 사람이 **추가 이동 없이 핵심을 이해하는 첫 화면**이다. GitHub/Repository의 structured/runtime truth를 복제해 새 정본을 만드는 것이 아니라, latest merged facts와 사용자 확정 방향을 사람이 읽기 쉬운 형태로 투영한다.

## Base Home 필수 내용

- Base 목적과 Notion/GitHub authority split
- 전체 작업 lifecycle과 각 단계의 존재 이유
- 중요 규칙과 작동 조건
- active Skill별 **Skill 목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / 연결 Module·consumer·Test**
- Module별 입력→판단/처리→출력→다음 consumer와 **없으면** 생기는 실패
- P01~P09 책임·대표 Skill/Module·진행 흐름·연결·기대효과·위험/revisit
- current main, 완료/미완료 workstream, 실제 검증과 `NOT_RUN`

## Project Home 필수 내용

1. 프로젝트 한 줄 정의
2. 핵심 플레이어/사용자 가치
3. 현재 확정 방향과 보호/금지 요소
4. Core Loop / 주요 Flow
5. 핵심 시스템별 목적·작동·상호작용
6. UX/UI/Visual 방향·승인 상태
7. 현재 구현상태와 Repository/runtime truth 연결
8. 검증상태와 static/runtime/device/human/accessibility/platform/store evidence ceiling
9. 현재 blocker / 다음 작업
10. 최근 중요한 결정과 이유
11. 주요 위험 / revisit condition

하위 페이지는 `drilldown`이다. 긴 표·전체 asset·reference·로그·세부 수치·evidence를 보관하되 Home의 핵심 설명을 '상세는 링크 참조'로 대체하지 않는다.
""",
    encoding="utf-8",
    newline="\n",
)

notion_path = ROOT / "docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
notion = notion_path.read_text(encoding="utf-8")
if "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md" not in notion:
    notion = notion.rstrip() + (
        "\n\n## Human Home 상세 정책\n\n"
        "`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`의 Base/Project Home 필수 내용은 "
        "`docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`가 소유한다. 하위 페이지는 drilldown/evidence이며 core understanding을 대신하지 않는다.\n"
    )
notion_path.write_text(notion.rstrip() + "\n", encoding="utf-8", newline="\n")

full_test = ROOT / "tests/test_full_adversarial_loop_semantics.py"
full_test.write_text(
    '''from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
AGENTS = ROOT / "AGENTS.md"


class FullAdversarialLoopSemanticsTests(unittest.TestCase):
    def authoritative_text(self) -> str:
        return POLICY.read_text(encoding="utf-8") + "\n" + OPERATING_MODEL.read_text(encoding="utf-8")

    def test_base_still_requires_minimum_five_full_loops(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", agents)
        self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", agents)

    def test_full_loop_is_not_a_review_lens(self) -> None:
        text = self.authoritative_text()
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("관점 하나", text)
        self.assertIn("최소 5", text)

    def test_each_counted_loop_repeats_the_complete_lifecycle(self) -> None:
        text = self.authoritative_text()
        for term in (
            "CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK",
            "MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK",
            "FULL-SCOPE ATTACK",
            "VALIDATE CRITIQUE",
            "FIX / REFINE VERIFIED FINDINGS",
            "EXECUTION / REGRESSION / REFERENCE VERIFICATION",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "RE-ATTACK THE WHOLE RESULTING STATE",
        ):
            self.assertIn(term, text)

    def test_lens_split_examples_are_explicitly_rejected(self) -> None:
        text = self.authoritative_text()
        self.assertIn("Loop 1=scope", text)
        self.assertIn("Loop 2=UX", text)
        self.assertIn("Loop 3=CI", text)
        self.assertIn("계수하지 않는다", text)


if __name__ == "__main__":
    unittest.main()
''',
    encoding="utf-8",
    newline="\n",
)

home_test = ROOT / "tests/test_human_home_self_contained_contract.py"
home_test.write_text(
    '''from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "HUMAN_HOME_SELF_CONTAINED_POLICY.md"
NOTION_CONTRACT = ROOT / "docs" / "operations" / "NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md"
BASE_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"


class HumanHomeSelfContainedContractTests(unittest.TestCase):
    def test_project_home_is_self_contained_before_drilldown(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        for term in (
            "프로젝트 한 줄 정의", "핵심 플레이어/사용자 가치", "현재 확정 방향",
            "Core Loop", "핵심 시스템", "UX/UI/Visual", "현재 구현상태", "검증상태",
            "현재 blocker", "다음 작업", "최근 중요한 결정", "주요 위험", "revisit condition",
        ):
            self.assertIn(term, text)
        self.assertIn("drilldown", text)

    def test_notion_contract_routes_to_self_contained_home_policy(self) -> None:
        text = NOTION_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", text)
        self.assertIn("docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md", text)

    def test_base_home_contract_is_self_contained_for_learning(self) -> None:
        text = POLICY.read_text(encoding="utf-8") + "\n" + BASE_MODEL.read_text(encoding="utf-8")
        for term in (
            "Skill 목적", "호출 조건", "입력", "처리", "출력", "기대효과",
            "Module", "없으면", "P01~P09",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
''',
    encoding="utf-8",
    newline="\n",
)

followup = ROOT / "docs/operations/PROTECTED_ACTIVE_WORKSTREAM_FOLLOWUPS_2026-08-19.md"
followup.write_text(
    """# Protected active-workstream follow-ups · 2026-08-19

These findings remain valid but are not rewritten by the sequential coordinator PR because active independent PR #530 owns the same policy/test surface.

## P01 / Project workspace schema consumer
- current completed main has schema v2 while `tests/test_notion_project_workspace_contract.py` still asserts v1.
- active PR #530 already changes this consumer and advances the workspace contract toward schema v3.
- coordinator disposition: `DUPLICATE_ACTIVE_WORKSTREAM / READ_ONLY`; recheck after #530 completes.

## P02 / strict multi-alias legacy parser
- multi-alias stale-ID parsing remains a valid robustness improvement.
- implementing it requires `.github/reference-freshness.json` companion semantics currently edited by #530.
- coordinator disposition: `DEFER_PROTECTED_ACTIVE_WORKSTREAM`; do not lose the finding.

## P04 / legacy Sheet planning inventory
- `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md` still contains active-looking Sheet/Figma legacy language on completed main.
- its canonical migration policy/tests are actively modified by #530.
- coordinator disposition: preserve main file during #530; revalidate and migrate after #530 completes.

## Human Home absorption into Project OS
- the new self-contained Home policy is implemented in a conflict-free canonical document and Notion contract.
- `skills/managing-game-project-operating-system/SKILL.md` and `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` are #530-owned active paths, so direct absorption is deferred until #530 completion.
""",
    encoding="utf-8",
    newline="\n",
)

print("PR530_ACTIVE_WORKSTREAM_ISOLATION_APPLIED")
