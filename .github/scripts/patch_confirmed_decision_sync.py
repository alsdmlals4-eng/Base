from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEWED_COMMIT = os.environ.get("GITHUB_SHA", "UNVERIFIED")


def insert_once(text: str, anchor: str, addition: str, label: str) -> str:
    if addition in text:
        return text
    if anchor not in text:
        raise SystemExit(f"{label} anchor missing")
    return text.replace(anchor, anchor + addition, 1)


def patch_registry() -> None:
    path = ROOT / "skills/SKILL_REGISTRY.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    by_id = {item["skill_id"]: item for item in registry["skills"]}

    design = by_id["managing-design-documents"]
    for tag in (
        "confirmed-decision-sync",
        "duplicate-question-prevention",
        "google-sheets-sync",
        "immediate-canonical-promotion",
    ):
        if tag not in design["trigger_tags"]:
            design["trigger_tags"].append(tag)
    design["use_when"] = [
        "등록된 기획 책임 원본을 작성·갱신·재구조화하고 발행 정책에 따라 파생본을 생성·검수하며, 질문 전 기존 Decision·PR·Google Sheets를 대조하고 승인 결정을 GitHub 추적 근거·CURRENT_CONFIRMED_DECISIONS·분야 정본·허용된 main 문서 Commit·Google Sheets에 즉시 동기화한다."
    ]
    for trigger in (
        "중복 질문",
        "승인 결정 즉시 정본화 누락",
        "GitHub·Google Sheets 동기화 누락",
        "SYNCED 오판",
        "checkpoint까지 승인 승격 지연",
    ):
        if trigger not in design["review_triggers"]:
            design["review_triggers"].append(trigger)
    design["last_reviewed_at"] = "2026-07-28"
    design["last_reviewed_commit"] = REVIEWED_COMMIT
    design["knowledge_state"] = "PATTERN"

    adversarial = by_id["running-adversarial-review-and-refinement"]
    for tag in (
        "post-merge-review",
        "canonical-conflict",
        "decision-omission",
        "google-sheets-drift",
        "merged-pr-regression",
    ):
        if tag not in adversarial["trigger_tags"]:
            adversarial["trigger_tags"].append(tag)
    adversarial["use_when"] = [
        "기획·계획·문서·코드·데이터·UX와 병합된 PR 또는 직접 main 결정 Commit이 실패했다고 가정해 공격하고, 비판을 검증한 뒤 승인된 finding만 최소 개선하며, 새 main·현재 확정 Decision·분야 정본·실제 diff·Google Sheets·회귀 증거를 재검사한다."
    ]
    for trigger in (
        "병합 후 적대적 검토 누락",
        "최근 승인 Decision 누락",
        "이전 Decision 부활",
        "GitHub·Google Sheets 불일치",
        "중복 PR·구현 잔존",
    ):
        if trigger not in adversarial["review_triggers"]:
            adversarial["review_triggers"].append(trigger)
    adversarial["last_reviewed_at"] = "2026-07-28"
    adversarial["last_reviewed_commit"] = REVIEWED_COMMIT
    adversarial["knowledge_state"] = "PATTERN"

    path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def patch_learning_log() -> None:
    path = ROOT / "skills/SKILL_LEARNING_LOG.md"
    text = path.read_text(encoding="utf-8")
    entry = """## 2026-07-28 승인 즉시 정본화·중복 질문 방지·병합 후 검토 교훈

- 장시간 기획·Grill Me에서 사용자 승인을 댓글이나 하위 시스템 checkpoint까지 누적하면 최근 결정이 분야 정본·현재 상태·Google Sheets에 승격되지 않는 운영 실패가 발생한다.
- 질문 전에 최신 main, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 실제 구현과 Google Sheets를 대조하고 이미 답한 질문은 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리하고, 코어·중요 기획·방향성·정본 충돌만 `USER_DECISION_REQUIRED`로 올린다.
- 승인 답변은 GitHub 추적 근거 → 현재 확정 결정 → 분야 정본 → 허용된 main 문서 Commit → Google Sheets → 양쪽 재조회까지 같은 승인 단위에서 완료하고 `SYNCED`를 증명한다.
- 모든 병합 뒤 새 main과 실제 diff를 다시 읽어 최근 승인 누락, 이전 Decision 부활, 정본·Sheets 불일치, 중복 PR과 회귀를 적대적으로 검토한다.
- 현재 지식 상태: 사용자 승인과 Base 정책 통합은 `PATTERN`, 여러 프로젝트에서의 실제 누락 감소 효과는 후속 관찰 전까지 `OBSERVATION`.

"""
    if "## 2026-07-28 승인 즉시 정본화" not in text:
        text = text.replace("# Base Skill Learning Log\n\n", "# Base Skill Learning Log\n\n" + entry, 1)
        path.write_text(text, encoding="utf-8")


def patch_tests() -> None:
    path = ROOT / "tests/test_consolidated_skill_references.py"
    text = path.read_text(encoding="utf-8")
    if "test_confirmed_decision_sync_and_post_merge_review_contract" in text:
        return
    block = '''    def test_confirmed_decision_sync_and_post_merge_review_contract(self) -> None:
        policy = (ROOT / "docs/CONFIRMED_DECISION_SYNC_POLICY.md").read_text(encoding="utf-8")
        grill = skill_package_text("managing-project-intake-and-work-contract")
        design = (ROOT / "skills/managing-design-documents/SKILL.md").read_text(encoding="utf-8")
        adversarial = skill_package_text("running-adversarial-review-and-refinement")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        for term in (
            "DUPLICATE_QUESTION",
            "RECOMMENDED_DEFAULT",
            "USER_DECISION_REQUIRED",
            "APPROVED_PENDING_CANON",
            "SHEET_UPDATED",
            "SYNCED",
            "NO_CONFLICT",
            "CONFLICT_FIXED",
        ):
            self.assertIn(term, policy)
        for file_path in (
            "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md",
            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md",
        ):
            self.assertTrue((ROOT / file_path).is_file(), file_path)
        for term in ("질문 전 필수 대조", "중복 질문 판정", "답변 처리와 즉시 동기화"):
            self.assertIn(term, grill)
        self.assertIn("Preserve approved decisions immediately", design)
        self.assertIn("Post-merge attack lenses", adversarial)
        for tag in (
            "confirmed-decision-sync",
            "google-sheets-sync",
            "post-merge-review",
            "canonical-conflict",
        ):
            self.assertIn(tag, registry)

'''
    marker = '\n\nif __name__ == "__main__":\n'
    if marker not in text:
        raise SystemExit("test insertion marker missing")
    path.write_text(text.replace(marker, "\n\n" + block + 'if __name__ == "__main__":\n', 1), encoding="utf-8")


def patch_documentation_map() -> None:
    path = ROOT / "docs/DOCUMENTATION_MAP.md"
    text = path.read_text(encoding="utf-8")
    row_anchor = "| GitHub 작업 항목 생명주기 | `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | Issue·Goal·Branch·PR·Run·Artifact·Release 책임, PR WIP·재사용·종료·보존·무손실 정리 |\n"
    row = "| 승인 결정 즉시 동기화 | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | 질문 전 정본·PR·Sheets 대조, 중복 질문 방지, 승인 즉시 정본·main·Sheets 동기화, 병합 후 적대적 검토 |\n"
    text = insert_once(text, row_anchor, row, "documentation map row")
    project_anchor = "Grill Me 결정 → GRILL_ME_DECISION_RECORD와 해당 기획 책임 원본\n"
    project_lines = "현재 승인 결정 복원 → CURRENT_CONFIRMED_DECISIONS.md\n승인 결정 동기화 → GitHub 추적 surface·분야 정본·main Commit·프로젝트 Google Sheets\n"
    text = insert_once(text, project_anchor, project_lines, "documentation map project")
    text = text.replace(
        "저장소 우선 조사 → 질문 하나 → 권장안 → 결정 원장 반영",
        "main·PR·정본·Sheets 대조 → 중복 제거 → 중요 질문 하나 → 권장안 → 승인 즉시 정본·main·Sheets 동기화",
    )
    text = text.replace(
        "`attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report`",
        "`attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report`; 병합 후 새 main·Decision·정본·Sheets 재검사",
    )
    path.write_text(text, encoding="utf-8")


def patch_template_readme() -> None:
    path = ROOT / "templates/project-operations/README.md"
    text = path.read_text(encoding="utf-8")
    decision_anchor = "| `DECISION_LOG.md` | 결정·근거·재검토 조건 |\n"
    current_row = "| `CURRENT_CONFIRMED_DECISIONS.md` | 현재 승인 Decision·대체 관계·main Commit·Google Sheets 동기화 복원 정본 |\n"
    if current_row not in text:
        if decision_anchor not in text:
            raise SystemExit("template decision anchor missing")
        text = text.replace(decision_anchor, current_row + decision_anchor, 1)
    tree_anchor = "│  ├─ DECISION_LOG.md\n"
    tree_line = "│  ├─ CURRENT_CONFIRMED_DECISIONS.md\n"
    if tree_line not in text:
        if tree_anchor not in text:
            raise SystemExit("template tree anchor missing")
        text = text.replace(tree_anchor, tree_line + tree_anchor, 1)
    check_anchor = "- [ ] Active Context가 실제 상태와 일치한다.\n"
    check_line = "- [ ] 승인 Decision이 GitHub 정본·main·Google Sheets에 반영되고 재조회 결과가 일치한다.\n"
    text = insert_once(text, check_anchor, check_line, "template check")
    path.write_text(text, encoding="utf-8")


def patch_changelog() -> None:
    path = ROOT / "docs/CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    anchor = "## Unreleased - Base audit and operating-contract consistency\n\n"
    line = "- 질문 전 최신 main·PR·정본·Google Sheets를 비교해 중복 질문을 막고, 기술 기본값과 사용자 기획 결정을 분리하며, 승인 즉시 정본·main·Sheets 동기화와 병합 후 적대적 검토를 수행하는 공용 계약·템플릿·회귀 테스트를 추가했다.\n"
    text = insert_once(text, anchor, line, "changelog")
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    patch_registry()
    patch_learning_log()
    patch_tests()
    patch_documentation_map()
    patch_template_readme()
    patch_changelog()
