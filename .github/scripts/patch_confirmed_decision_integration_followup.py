from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEWED_COMMIT = os.environ.get("GITHUB_SHA", "UNVERIFIED")


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: old text missing")
    return text.replace(old, new, 1)


# 1. Project cold-start read order.
map_path = ROOT / "docs/DOCUMENTATION_MAP.md"
text = map_path.read_text(encoding="utf-8")
text = replace_required(
    text,
    "→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md\n→ DESIGN_DOCUMENT_REGISTRY.json",
    "→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md\n→ CURRENT_CONFIRMED_DECISIONS.md\n→ DESIGN_DOCUMENT_REGISTRY.json",
    "project read order",
)
text = replace_required(
    text,
    "| 운영체계 신규 설치·기존 감사·마이그레이션·Health Review | `managing-game-project-operating-system` | `install` / `audit` / `migrate` / `verify` |",
    "| 운영체계 신규 설치·기존 감사·마이그레이션·Health Review | `managing-game-project-operating-system` | `install` / `audit` / `migrate` / `verify`; CURRENT_CONFIRMED_DECISIONS·관련 PR·프로젝트 Sheets 포함 |",
    "operating system routing row",
)
map_path.write_text(text, encoding="utf-8")

# 2. Intake must restore current decisions before asking.
intake_path = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
text = intake_path.read_text(encoding="utf-8")
text = replace_required(
    text,
    "상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`",
    "상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`\n\n승인 결정 복원·중복 질문 방지·GitHub·Google Sheets 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`",
    "intake policy link",
)
text = replace_required(
    text,
    "active_context:\ndocumentation_map:\ndesign_document_registry:",
    "active_context:\ncurrent_confirmed_decisions:\nproject_google_sheet:\nrelated_open_and_recent_prs:\ndocumentation_map:\ndesign_document_registry:",
    "intake required inputs",
)
text = replace_required(
    text,
    "2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map\n3. `docs/WORK_MODE_AND_SKILL_ROUTING.md`\n4. 현재 Issue·Plan·책임 원본과 실제 파일",
    "2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map\n3. `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, 프로젝트 Google Sheets\n4. `docs/WORK_MODE_AND_SKILL_ROUTING.md`\n5. 현재 Issue·Plan·책임 원본과 실제 파일",
    "intake read order",
)
for old, new in (
    ("5. `SKILL_REGISTRY.json`", "6. `SKILL_REGISTRY.json`"),
    ("6. 필요한 경우 `references/question-and-source-model.md`", "7. 필요한 경우 `references/question-and-source-model.md`"),
    ("7. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`", "8. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`"),
    ("8. Grill Me 핵심 결정 인터뷰가 필요한 경우 `references/grill-me-protocol.md`", "9. Grill Me 핵심 결정 인터뷰가 필요한 경우 `references/grill-me-protocol.md`"),
    ("9. 작업 분해·순서화가 필요한 경우 `references/work-decomposition-and-sequencing.md`", "10. 작업 분해·순서화가 필요한 경우 `references/work-decomposition-and-sequencing.md`"),
):
    text = text.replace(old, new, 1)
text = replace_required(
    text,
    "현재 파일·경로·호출·데이터·테스트에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다.",
    "최신 `main`, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 실제 파일과 프로젝트 Google Sheets에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다.",
    "intake repository facts",
)
text = replace_required(
    text,
    "결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다. 상세 요청은 처음부터 다시 인터뷰하지 않고 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.",
    "결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다. 기존 Decision이 유효하면 다시 묻지 않는다. 프로젝트 방향을 바꾸지 않는 기술 세부·초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다. 상세 요청은 처음부터 다시 인터뷰하지 않고 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.",
    "intake material decisions",
)
intake_path.write_text(text, encoding="utf-8")

# 3. Operating-system install/audit/verify must include recovery canon and Sheet.
os_path = ROOT / "skills/managing-game-project-operating-system/SKILL.md"
text = os_path.read_text(encoding="utf-8")
text = replace_required(
    text,
    "active_context:\ndevelopment_gates:",
    "active_context:\ncurrent_confirmed_decisions:\nproject_google_sheet:\nrelated_open_and_recent_prs:\ndevelopment_gates:",
    "operating required inputs",
)
text = replace_required(
    text,
    "→ Active Context·Documentation Map·Roadmap·Development Gates\n→ Design Document Registry·Skill Registry",
    "→ Active Context·Documentation Map·Roadmap·Development Gates\n→ CURRENT_CONFIRMED_DECISIONS.md·동일 Goal의 열린·최근 병합 PR·프로젝트 Google Sheets\n→ Design Document Registry·Skill Registry",
    "operating shared read order",
)
text = replace_required(
    text,
    "- 새 AI가 과거 대화 없이 현재 상태와 다음 작업을 찾을 수 있어야 한다.",
    "- 새 AI가 과거 대화 없이 `CURRENT_CONFIRMED_DECISIONS.md`에서 현재 승인 상태와 다음 작업을 찾을 수 있어야 한다.\n- 질문 전에 최신 `main`, 기존 Decision, 분야 정본, 동일 Goal의 PR과 Google Sheets를 비교하고 이미 답한 질문은 반복하지 않는다.\n- 승인된 Decision은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`에 따라 GitHub 정본·허용된 `main` 문서 Commit·Google Sheets에 즉시 동기화한다.",
    "operating shared contract",
)
old_install = """1. 신규·빈 프로젝트인지 확인한다. 고유 문서·자산·이력이 있으면 `audit`로 전환한다.
2. 루트 `[기획서]/00_프로젝트_허브/`와 시작 문서·Registry·게이트를 설치한다.
3. 프로젝트가 실제 선택한 책임 분야만 등록한다.
4. 서술은 Markdown, 구조·상태·게임 데이터는 JSON을 선택한다.
5. 발행 생성기·Manifest·선택 파생본 정책을 설치한다.
6. Foundation·분야 Skill Registry와 Learning Log를 설치한다.
7. Visual Source·Asset Manifest와 승인 상태를 연결한다.
8. Governance 검사·Actions·Required Check 준비 상태를 구분한다.
9. `verify`로 콜드 스타트와 파이프라인을 확인한다."""
new_install = """1. 신규·빈 프로젝트인지 확인한다. 고유 문서·자산·이력이 있으면 `audit`로 전환한다.
2. 루트 `[기획서]/00_프로젝트_허브/`와 시작 문서·`CURRENT_CONFIRMED_DECISIONS.md`·Registry·게이트를 설치한다.
3. 제공된 프로젝트 Google Sheets URL·확정 결정 탭·마지막 Decision ID를 연결하고, 없으면 `NOT_CONFIGURED`로 명시한다.
4. 프로젝트가 실제 선택한 책임 분야만 등록한다.
5. 서술은 Markdown, 구조·상태·게임 데이터는 JSON을 선택한다.
6. 발행 생성기·Manifest·선택 파생본 정책을 설치한다.
7. Foundation·분야 Skill Registry와 Learning Log를 설치한다.
8. Visual Source·Asset Manifest와 승인 상태를 연결한다.
9. Governance 검사·Actions·Required Check 준비 상태를 구분한다.
10. `verify`로 콜드 스타트와 결정 복원·동기화 파이프라인을 확인한다."""
text = replace_required(text, old_install, new_install, "operating install sequence")
text = replace_required(
    text,
    "- 현재 책임 문서·Skill·자산·파생본 지도",
    "- 현재 책임 문서·Skill·자산·파생본 지도\n- `CURRENT_CONFIRMED_DECISIONS.md`·분야 정본·GitHub `main`·프로젝트 Google Sheets의 Decision·Commit·대체 관계 대조",
    "operating audit outputs",
)
old_verify = """1. 루트와 시작 문서
2. Work Mode·Skill 자동 라우팅과 실행 보고
3. Design Document Registry와 단일 책임 원본
4. 구형본 처리표·Legacy Alias·활성 stale reference 부재
5. PDF·선택 DOCX·다이어그램·승인 이미지·Manifest
6. Skill Registry·최소 라우팅·Learning Log
7. Development Gates·Roadmap·결정 추적성
8. Visual Source·Asset Manifest
9. Governance checker·회귀 테스트·GitHub Actions·브랜치 보호
10. 콜드 스타트"""
new_verify = """1. 루트와 시작 문서
2. Work Mode·Skill 자동 라우팅과 실행 보고
3. `CURRENT_CONFIRMED_DECISIONS.md`·분야 정본·GitHub `main`·프로젝트 Google Sheets 동기화
4. Design Document Registry와 단일 책임 원본
5. 구형본 처리표·Legacy Alias·활성 stale reference 부재
6. PDF·선택 DOCX·다이어그램·승인 이미지·Manifest
7. Skill Registry·최소 라우팅·Learning Log
8. Development Gates·Roadmap·결정 추적성
9. Visual Source·Asset Manifest
10. Governance checker·회귀 테스트·GitHub Actions·브랜치 보호
11. 과거 대화 없이 현재 Decision을 복원하는 콜드 스타트"""
text = replace_required(text, old_verify, new_verify, "operating verify sequence")
text = replace_required(
    text,
    "## Registry·책임 원본·발행본",
    "## CURRENT_CONFIRMED_DECISIONS·GitHub·Google Sheets 동기화\n## Registry·책임 원본·발행본",
    "operating output contract",
)
os_path.write_text(text, encoding="utf-8")

# 4. Registry routing companions.
registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
by_id = {item["skill_id"]: item for item in registry["skills"]}

intake = by_id["managing-project-intake-and-work-contract"]
for tag in (
    "current-confirmed-decisions",
    "duplicate-question-prevention",
    "recommended-default",
    "google-sheets-sync",
    "pr-preflight",
):
    if tag not in intake["trigger_tags"]:
        intake["trigger_tags"].append(tag)
intake["use_when"] = [
    "새 요청과 중요 기획 질문을 라우팅할 때 최신 main·CURRENT_CONFIRMED_DECISIONS·분야 정본·동일 Goal의 열린·최근 병합 PR·프로젝트 Google Sheets를 먼저 비교하고, 기술 기본값과 사용자 결정 사항을 분리해 실행 계약으로 만든다."
]
for trigger in (
    "기존 Decision을 다시 질문함",
    "main·PR·Google Sheets 사전 대조 누락",
    "기술 기본값을 사용자에게 전가함",
):
    if trigger not in intake["review_triggers"]:
        intake["review_triggers"].append(trigger)
intake["last_reviewed_at"] = "2026-07-28"
intake["last_reviewed_commit"] = REVIEWED_COMMIT
intake["knowledge_state"] = "PATTERN"

operating = by_id["managing-game-project-operating-system"]
for tag in (
    "current-confirmed-decisions",
    "decision-recovery",
    "google-sheets-sync",
    "project-cold-start",
):
    if tag not in operating["trigger_tags"]:
        operating["trigger_tags"].append(tag)
operating["use_when"] = [
    "프로젝트 운영체계를 설치·감사·마이그레이션·검증하면서 CURRENT_CONFIRMED_DECISIONS, 동일 Goal의 PR, 분야 정본, GitHub main과 프로젝트 Google Sheets의 결정 복원·동기화 상태를 포함한다."
]
for trigger in (
    "CURRENT_CONFIRMED_DECISIONS 설치 누락",
    "프로젝트 Google Sheets 연결·재조회 누락",
    "콜드 스타트에서 승인 Decision 복원 실패",
):
    if trigger not in operating["review_triggers"]:
        operating["review_triggers"].append(trigger)
operating["last_reviewed_at"] = "2026-07-28"
operating["last_reviewed_commit"] = REVIEWED_COMMIT
operating["knowledge_state"] = "PATTERN"

registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

# 5. Learning log and regression test.
learning_path = ROOT / "skills/SKILL_LEARNING_LOG.md"
text = learning_path.read_text(encoding="utf-8")
entry = """## 2026-07-28 병합 후 결정 복원 진입점 누락 교훈

- 승인 결정 동기화 정책과 템플릿만 추가해도 프로젝트 기본 읽기 순서와 운영체계 `install/audit/verify`가 이를 명시적으로 소비하지 않으면 새 채팅·신규 설치에서 복원 정본을 건너뛸 수 있다.
- `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, 분야 정본, GitHub `main`, 프로젝트 Google Sheets를 Intake와 운영체계 Skill의 Required inputs·Read order·설치·감사·검증 계약에 모두 연결한다.
- 병합 후 적대적 검토는 새 파일의 존재가 아니라 실제 소비 진입점과 콜드 스타트 경로까지 검사해야 한다.
- 현재 지식 상태: Base 회귀 검사와 병합 후 정본 대조로 확인한 `PATTERN`.

"""
if "## 2026-07-28 병합 후 결정 복원 진입점 누락 교훈" not in text:
    text = text.replace("# Base Skill Learning Log\n\n", "# Base Skill Learning Log\n\n" + entry, 1)
    learning_path.write_text(text, encoding="utf-8")

test_path = ROOT / "tests/test_consolidated_skill_references.py"
text = test_path.read_text(encoding="utf-8")
if "test_confirmed_decisions_are_consumed_by_intake_and_project_os" not in text:
    block = '''    def test_confirmed_decisions_are_consumed_by_intake_and_project_os(self) -> None:
        doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        operating = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        self.assertIn("→ CURRENT_CONFIRMED_DECISIONS.md", doc_map)
        for term in ("current_confirmed_decisions", "project_google_sheet", "related_open_and_recent_prs"):
            self.assertIn(term, intake)
            self.assertIn(term, operating)
        for term in ("RECOMMENDED_DEFAULT", "USER_DECISION_REQUIRED"):
            self.assertIn(term, intake)
        for term in ("install", "audit", "verify", "콜드 스타트"):
            self.assertIn(term, operating)
        for tag in ("decision-recovery", "pr-preflight", "project-cold-start"):
            self.assertIn(tag, registry)

'''
    marker = '\n\nif __name__ == "__main__":\n'
    if marker not in text:
        raise SystemExit("test insertion marker missing")
    text = text.replace(marker, "\n\n" + block + 'if __name__ == "__main__":\n', 1)
    test_path.write_text(text, encoding="utf-8")

# 6. Close the original implementation plan with the post-merge finding.
plan_path = ROOT / "docs/superpowers/plans/2026-07-28-confirmed-decision-sync.md"
text = plan_path.read_text(encoding="utf-8")
for old, new in (
    ("- [ ] **Step 2:** PR을 생성하고 `Validate Game Project Operating System` 결과를 확인한다.", "- [x] **Step 2:** PR을 생성하고 `Validate Game Project Operating System` 결과를 확인한다."),
    ("- [ ] **Step 3:** Squash merge한다.", "- [x] **Step 3:** Squash merge한다."),
    ("- [ ] **Step 4:** 새 main을 기준으로 정본·PR·템플릿·Skill·Sheets 계약을 적대적으로 재검사한다.", "- [x] **Step 4:** 새 main을 기준으로 정본·PR·템플릿·Skill·Sheets 계약을 적대적으로 재검사한다."),
    ("- [ ] **Step 5:** branch 자동 삭제 여부를 확인하고 확인하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 보고한다.", "- [x] **Step 5:** 병합 뒤 작업 branch가 존재하지 않음을 확인했다. 삭제 방식 자체는 별도 설정으로 추정하지 않는다."),
):
    if old in text:
        text = text.replace(old, new, 1)
followup = """
## Post-merge follow-up

- `MUST_FIX`: 최초 병합 뒤 프로젝트 기본 읽기 순서와 `managing-game-project-operating-system`의 `install/audit/verify`가 `CURRENT_CONFIRMED_DECISIONS.md`와 프로젝트 Google Sheets를 명시적으로 소비하지 않는 누락을 발견했다.
- 처리: Intake·운영체계 Skill의 Required inputs·Read order·설치·감사·검증, Documentation Map, Registry, Learning Log와 회귀 테스트에 연결했다.
- 검증 기준: 새 채팅·신규 설치·기존 프로젝트 감사에서 과거 대화 없이 현재 Decision·main Commit·Sheet 동기화 상태를 복원할 수 있어야 한다.
"""
if "## Post-merge follow-up" not in text:
    text = text.rstrip() + "\n" + followup
plan_path.write_text(text, encoding="utf-8")
