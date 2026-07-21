from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def insert_after(text: str, needle: str, addition: str, label: str) -> str:
    if addition.strip() in text:
        return text
    if needle not in text:
        raise RuntimeError(f"Missing insertion point for {label}: {needle}")
    return text.replace(needle, needle + addition, 1)


def insert_before(text: str, needle: str, addition: str, label: str) -> str:
    if addition.strip() in text:
        return text
    if needle not in text:
        raise RuntimeError(f"Missing insertion point for {label}: {needle}")
    return text.replace(needle, addition + needle, 1)


NEW_SKILLS = [
    {
        "skill_id": "identifying-project-core",
        "layer": "foundation",
        "discipline": "project-core-governance",
        "path": "skills/identifying-project-core/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": [
            "project-core",
            "core-identification",
            "core-classification",
            "core-loop-boundary",
            "core-vs-mvp",
            "identity-defining-system",
            "technical-core",
            "removal-test",
            "change-impact",
        ],
        "use_when": [
            "기존 프로젝트에서 무엇이 정체성·핵심 경험·중심 시스템·기술 기반의 프로젝트 코어인지 근거와 제거·대체 테스트로 판정하고 코어·MVP 지원·콘텐츠·외피를 구분한다."
        ],
        "do_not_use_when": [
            "새 프로젝트의 코어를 승인·확정하는 기획 작업, 단순 핵심 컨셉 브레인스토밍, 실제 diff의 통합 검증만 필요한 경우다."
        ],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": [
            "중요 기능을 전부 코어로 판정",
            "코어와 MVP 혼동",
            "기술 의존성과 제품 정체성 혼동",
            "근거 없는 확정",
            "문서·구현 충돌 누락",
        ],
        "last_reviewed_at": "2026-07-21",
        "last_reviewed_commit": "ee265576da7f67d3278f8099dd97d4e714ef0651",
        "knowledge_state": "OBSERVATION",
    },
    {
        "skill_id": "establishing-project-core",
        "layer": "specialist",
        "discipline": "game-design-strategy",
        "path": "skills/establishing-project-core/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": [
            "establish-project-core",
            "confirm-project-core",
            "planning-core-contract",
            "core-invariants",
            "core-approval",
            "core-protection-boundary",
            "core-reopen",
        ],
        "use_when": [
            "PLAN Work Mode에서 새 프로젝트 또는 방향 재정의 프로젝트의 정체성·핵심 경험·코어 루프·중심 시스템·불변 조건·변경 가능 외피를 제안하고 스트레스 테스트한 뒤 사용자 승인으로 확정한다."
        ],
        "do_not_use_when": [
            "기존 프로젝트의 코어 사실만 읽기 전용으로 판정하거나, 사용자 승인 없이 코어를 확정하거나, 확정된 코어와 무관한 단일 기능을 구현하는 경우다."
        ],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": [
            "승인 없는 CORE_CONFIRMED",
            "과도한 코어 범위",
            "기능 목록을 코어로 고정",
            "코어와 MVP 혼동",
            "PoC 반증 무시",
            "일반 변경으로 코어 암묵 변경",
        ],
        "last_reviewed_at": "2026-07-21",
        "last_reviewed_commit": "ee265576da7f67d3278f8099dd97d4e714ef0651",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "running-adversarial-review-and-refinement",
        "layer": "foundation",
        "discipline": "integrated-review",
        "path": "skills/running-adversarial-review-and-refinement/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": [
            "adversarial-review",
            "red-team-review",
            "critique-refine",
            "self-refine",
            "failure-assumption",
            "critique-validation",
            "approved-refinement",
            "regression-recheck",
            "negative-review",
        ],
        "use_when": [
            "기획·계획·문서·코드 제안·데이터·UX 등 작업물이 실패했다고 가정해 결함을 공격적으로 찾고, 비판 자체를 검증한 뒤 유효한 문제만 최소 개선하고 회귀 재검토한다."
        ],
        "do_not_use_when": [
            "칭찬·균형 평가만 요청됐거나, 같은 입력의 단순 검사 재실행이거나, 실제 변경의 정적·런타임 증거 검증만 필요한 경우다."
        ],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": [
            "레드팀 지적 전부 수용",
            "취향을 결함으로 판정",
            "프로젝트 코어 훼손",
            "기능 팽창",
            "보류·기각 항목 몰래 반영",
            "회귀 검토 누락",
        ],
        "last_reviewed_at": "2026-07-21",
        "last_reviewed_commit": "ee265576da7f67d3278f8099dd97d4e714ef0651",
        "knowledge_state": "HYPOTHESIS",
    },
]


def update_registry() -> None:
    path = "skills/SKILL_REGISTRY.json"
    text = read(path)
    current = json.loads(text)
    existing = {item["skill_id"] for item in current["skills"]}
    missing = [item for item in NEW_SKILLS if item["skill_id"] not in existing]
    if not missing:
        return
    closing = "\n  ]\n}\n"
    if not text.endswith(closing):
        raise RuntimeError("Unexpected Skill Registry closing structure")
    rendered = ",\n".join(
        textwrap.indent(json.dumps(item, ensure_ascii=False, indent=2), "    ")
        for item in missing
    )
    text = text[: -len(closing)] + ",\n" + rendered + closing
    parsed = json.loads(text)
    if len(parsed["skills"]) != 16:
        raise RuntimeError(f"Expected 16 skills, found {len(parsed['skills'])}")
    write(path, text)


def update_learning_log() -> None:
    path = "skills/SKILL_LEARNING_LOG.md"
    text = read(path)
    summary = """

## 2026-07-21 프로젝트 코어·적대적 검토 Skill 분리 교훈

- 프로젝트 코어 판정은 기존 프로젝트의 승인 원본·실제 구현·의존 관계를 읽기 전용으로 대조하는 작업이며, 새 프로젝트의 코어를 제안·확정하는 기획 권한과 분리한다.
- `identifying-project-core`는 기획·시스템·코드 코어와 코어 기능·MVP 지원 기능을 제거·대체 테스트로 구분한다.
- `establishing-project-core`는 PLAN Work Mode에서 불변 조건과 변경 가능한 외피를 제안하고, 반례 검토 뒤 사용자의 명시적 승인만 `CORE_CONFIRMED`로 인정한다.
- 적대적 검토는 레드팀 공격, 비판 검증, 승인된 finding의 최소 개선, 회귀 재검토를 분리한다. 비판도 취향·과잉 요구·잘못된 전제일 수 있으므로 그대로 반영하지 않는다.
- 세 Skill은 읽기 권한, 승인 경계, 산출물이 달라 독립 Skill로 유지하되 실제 여러 프로젝트에서 오라우팅·코어 과대 판정·비판 과수용을 검증하기 전까지 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 둔다.
"""
    text = insert_after(text, "# Base Skill Learning Log", summary, "learning summary")
    record = """
### 2026-07-21 project core and adversarial review skills

- 프로젝트·작업: 프로젝트 코어 판정, PLAN 단계 코어 확정, 적대적 검토·개선 루프를 독립 Skill로 추가
- 호출 트리거: 사용자가 사람도 이해하기 쉬운 컨텍스트를 Base Skill로 분리하고 기획 모드의 코어 확정 Skill을 추가하도록 요청
- 실제 산출물: `identifying-project-core`, `establishing-project-core`, `running-adversarial-review-and-refinement`, Registry·라우팅·회귀 동기화
- 실행한 검증: Registry Schema, Skill 패키지 1:1, 진입점 발견성, 구조 회귀, 정본 최신성 검사
- 결과: 부분 성공 — 공용 계약 추가, 실제 여러 프로젝트 적용은 미검증
- 성공 조건: 코어와 MVP를 구분하고, 사용자 승인 없이 코어를 확정하지 않으며, 레드팀 비판을 검증한 뒤 유효한 문제만 수정하고 회귀를 재검사함
- 실패·예외: 모든 중요 기능을 코어로 판정, 기술 부채를 불변 코어로 고정, 비판 전부 수용, 기능 팽창, 회귀 누락
- 지식 상태: 코어 판정은 관찰, 코어 확정과 적대적 개선 루프는 가설
- 다음 검토 트리거: 서로 다른 프로젝트 적용, 승인 없는 확정, 코어 과대 판정, 비판 과수용·기각 오류

"""
    text = insert_after(text, "## 기록\n", record, "learning execution record")
    write(path, text)


def update_tests() -> None:
    path = "tests/test_game_project_operating_system_structure.py"
    text = read(path)
    required = (
        '            "skills/identifying-project-core/SKILL.md",\n'
        '            "skills/establishing-project-core/SKILL.md",\n'
        '            "skills/running-adversarial-review-and-refinement/SKILL.md",\n'
    )
    text = insert_after(
        text,
        '            "skills/analyzing-and-refining-game-concepts/SKILL.md",\n',
        required,
        "required skill paths",
    )
    if 'self.assertEqual(len(registry["skills"]), 13)' not in text:
        raise RuntimeError("Expected 13-skill assertion was not found")
    text = text.replace(
        'self.assertEqual(len(registry["skills"]), 13)',
        'self.assertEqual(len(registry["skills"]), 16)',
        1,
    )
    route_ids = (
        '            "identifying-project-core",\n'
        '            "establishing-project-core",\n'
        '            "running-adversarial-review-and-refinement",\n'
    )
    text = insert_after(
        text,
        '            "analyzing-and-refining-game-concepts",\n',
        route_ids,
        "minimum routing IDs",
    )
    dedicated = '''    def test_project_core_and_adversarial_skills_have_distinct_contracts(self) -> None:
        identify = (ROOT / "skills/identifying-project-core/SKILL.md").read_text(encoding="utf-8")
        establish = (ROOT / "skills/establishing-project-core/SKILL.md").read_text(encoding="utf-8")
        adversarial = (ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md").read_text(encoding="utf-8")
        for term in ("PROJECT_CORE", "MVP_SUPPORT", "removal-and-change-test", "UNVERIFIED"):
            self.assertIn(term, identify)
        for term in ("CORE_PROPOSED", "CORE_STRESS_TESTED", "CORE_CONFIRMED", "사용자 승인", "REQUIRES_REAPPROVAL"):
            self.assertIn(term, establish)
        for term in ("attack", "validate-critique", "refine-approved-findings", "regression-recheck", "MUST_FIX", "REJECT"):
            self.assertIn(term, adversarial)
        self.assertIn("읽기 전용", identify)
        self.assertIn("사용자 승인 없이", establish)
        self.assertIn("비판도 오류·취향·과잉 요구", adversarial)

'''
    text = insert_before(
        text,
        "    def test_work_mode_skill_and_skill_mode_are_distinct_and_automatic(self) -> None:\n",
        dedicated,
        "project core regression",
    )
    write(path, text)


def update_entrypoints() -> None:
    readme = read("README.md")
    readme = readme.replace(
        "활성 Registry 스킬은 중복 통합 뒤 **13개**입니다.",
        "활성 Registry 스킬은 중복 통합 뒤 **16개**입니다.",
        1,
    )
    rows = (
        "| `identifying-project-core` | 기존 프로젝트의 기획·시스템·코드 코어와 코어·MVP 경계를 근거로 판정 |\n"
        "| `establishing-project-core` | PLAN 단계에서 프로젝트 코어를 제안·반례 검토하고 사용자 승인으로 확정 |\n"
        "| `running-adversarial-review-and-refinement` | 실패 가정 공격·비판 검증·승인된 개선·회귀 재검토 |\n"
    )
    readme = insert_after(
        readme,
        "| `analyzing-and-refining-game-concepts` | 핵심 컨셉·DDD·벤치마크·플레이어 반응·플레이테스트·PoC·기획 재조정 |\n",
        rows,
        "README skill rows",
    )
    write("README.md", readme)

    start = read("START_HERE.md")
    section = """### 프로젝트 코어 판정

`skills/identifying-project-core/SKILL.md`

기존 프로젝트의 기획·시스템·코드 코어와 코어 기능·MVP 지원 기능의 경계를 승인 원본·실제 구현·제거·대체 테스트로 판정한다. 기본 권한은 읽기 전용이다.

### 기획 단계 프로젝트 코어 확정

`skills/establishing-project-core/SKILL.md`

PLAN Work Mode에서 프로젝트 정체성·핵심 경험·코어 루프·불변 조건·변경 가능한 외피를 제안하고 반례 검토 뒤 사용자의 명시적 승인으로 확정한다.

### 적대적 검토·개선 루프

`skills/running-adversarial-review-and-refinement/SKILL.md`

```text
attack
→ validate-critique
→ MUST_FIX·SHOULD_FIX만 refine-approved-findings
→ regression-recheck
→ decision-report
```

레드팀 지적을 그대로 수용하지 않고 취향·범위 밖 요구·잘못된 전제를 다시 검증한다.

"""
    start = insert_before(
        start,
        "### 기획 책임 원본 작성·발행\n",
        section,
        "START_HERE routing",
    )
    write("START_HERE.md", start)

    docs = read("docs/DOCUMENTATION_MAP.md")
    docs_rows = (
        "| 프로젝트 코어 식별·코어/MVP 경계 | `identifying-project-core` | `inventory` / `extract-candidates` / `dependency-map` / `removal-and-change-test` / `classify` / `core-report` |\n"
        "| PLAN 단계 프로젝트 코어 확정 | `establishing-project-core` | `propose` / `stress-test` / `confirm` / `lock` / `reopen` |\n"
        "| 적대적 검토·비판 검증·개선·회귀 | `running-adversarial-review-and-refinement` | `attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report` |\n"
    )
    docs = insert_after(
        docs,
        "| 핵심 컨셉·뾰족한 재미·DDD·기획 정렬 | `analyzing-and-refining-game-concepts` | `frame` / `constrain` / `sharpen` / `structure` / `analyze` |\n",
        docs_rows,
        "Documentation Map rows",
    )
    write("docs/DOCUMENTATION_MAP.md", docs)

    workflow = read("templates/project-operations/AI_WORKFLOW.md")
    workflow_rows = (
        "| 기존 프로젝트 코어 판정 | `identifying-project-core` |\n"
        "| PLAN 단계 프로젝트 코어 확정 | `establishing-project-core` |\n"
        "| 적대적 검토·개선·회귀 | `running-adversarial-review-and-refinement` |\n"
    )
    workflow = insert_after(
        workflow,
        "| 핵심 컨셉·DDD·SWOT·PoC·재조정 | `analyzing-and-refining-game-concepts` |\n",
        workflow_rows,
        "AI Workflow rows",
    )
    write("templates/project-operations/AI_WORKFLOW.md", workflow)

    changelog = read("docs/CHANGELOG.md")
    changes = (
        "- 기존 프로젝트의 기획·시스템·코드 코어와 코어·MVP 경계를 판정하는 `identifying-project-core`를 추가했다.\n"
        "- PLAN 단계에서 코어 제안·반례 검토·사용자 승인·책임 원본 연결을 수행하는 `establishing-project-core`를 추가했다.\n"
        "- 레드팀 공격·비판 검증·승인된 finding만 개선·회귀 재검토하는 `running-adversarial-review-and-refinement`를 추가했다.\n"
    )
    changelog = insert_after(
        changelog,
        "## Unreleased - Base audit and operating-contract consistency\n\n",
        changes,
        "CHANGELOG rows",
    )
    write("docs/CHANGELOG.md", changelog)


def remove_temporary_files() -> None:
    for relative in (
        ".github/workflows/agent-sync-project-core-pr.yml",
        "tools/apply_project_core_skills.py",
    ):
        path = ROOT / relative
        if path.exists():
            path.unlink()


def main() -> None:
    update_registry()
    update_learning_log()
    update_tests()
    update_entrypoints()
    remove_temporary_files()


if __name__ == "__main__":
    main()
