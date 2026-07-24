from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GptCodexWorkflowContractTests(unittest.TestCase):
    def test_canonical_policy_separates_gpt_codex_plan_and_build(self) -> None:
        text = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "GPT 책임",
            "Codex Plan 책임",
            "Codex Build 책임",
            "file_write",
            "FORBIDDEN",
            "CHANGE_PROPOSAL",
            "PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES",
            "USER_REVIEW_REQUIRED",
            "사용자의 명시적 승인 전에는 PR을 병합하지 않는다",
        ):
            self.assertIn(term, text)

    def test_handoff_skill_has_implementation_package_mode(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "implementation-package-handoff",
            "PLAN_REVIEW_ONLY",
            "godot_runtime_files_only",
            "ALLOWED_BRANCH_ONLY",
            "PACKAGE_APPROVED",
            "CHANGE_PROPOSAL",
            "사용자의 명시적 승인 전에는 PR을 병합하지 않는다",
        ):
            self.assertIn(term, text)

    def test_handoff_reference_requires_latest_main_and_read_only_plan(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md").read_text(encoding="utf-8")
        for term in (
            "최신 `main`",
            "읽기 전용",
            "file_write: FORBIDDEN",
            "commit_push_pr_issue: FORBIDDEN",
            "SEQUENTIAL",
            "원격 HEAD",
        ):
            self.assertIn(term, text)

    def test_master_plan_template_has_package_and_approval_contract(self) -> None:
        text = (ROOT / "templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
        for term in (
            "구현 패키지 지도",
            "데이터·저장·ID·Schema 보호 조건",
            "CHANGE_PROPOSAL",
            "PACKAGE_APPROVED",
            "USER_REVIEW_REQUIRED",
            "사용자 병합 승인: `REQUIRED`",
        ):
            self.assertIn(term, text)

    def test_codex_plan_report_is_read_only_and_evidence_driven(self) -> None:
        text = (ROOT / "templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md").read_text(encoding="utf-8")
        for term in (
            "mode: PLAN_REVIEW_ONLY",
            "file_write: FORBIDDEN",
            "최신 저장소 조사",
            "예상 파일과 실제 파일 대조",
            "Red → Green → Refactor",
            "CHANGE_PROPOSAL",
            "tests_not_run",
        ):
            self.assertIn(term, text)

    def test_package_contract_limits_codex_git_authority(self) -> None:
        text = (ROOT / "templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md").read_text(encoding="utf-8")
        for term in (
            "create_or_switch: FORBIDDEN",
            "push_target: ALLOWED_BRANCH_ONLY",
            "godot_runtime_files_only: true",
            "force_push: FORBIDDEN",
            "amend: FORBIDDEN",
            "create_or_update: FORBIDDEN",
            "merge: FORBIDDEN",
            "비-Godot 변경 반환 계약",
        ):
            self.assertIn(term, text)

    def test_documentation_map_routes_without_new_duplicate_skill(self) -> None:
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("Grill Me 핵심 의사결정 인터뷰", text)
        self.assertIn("`clarify` + `references/grill-me-protocol.md`", text)
        self.assertIn("GPT→Codex 단계별 Godot 구현 인계", text)
        self.assertIn("`implementation-package-handoff`", text)


if __name__ == "__main__":
    unittest.main()
