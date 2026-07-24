from __future__ import annotations

import json
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
            "파일 생성·수정·삭제·이동",
            "Commit·Push·PR·Issue 변경",
            "CHANGE_PROPOSAL",
            "PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES",
            "USER_REVIEW_REQUIRED",
            "AUTO_MERGE_AFTER_REQUIRED_CHECKS",
            "AUTO_MERGE_ELIGIBLE",
            "AUTO_MERGE_ENABLED",
            "AUTO_MERGE_BLOCKED",
            "UNVERIFIED_REPOSITORY_SETTING",
        ):
            self.assertIn(term, text)
        self.assertNotIn("사용자의 명시적 승인 전에는 PR을 병합하지 않는다", text)

    def test_handoff_skill_has_implementation_package_mode(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "implementation-package-handoff",
            "PLAN_REVIEW_ONLY",
            "godot_runtime_files_only",
            "ALLOWED_BRANCH_ONLY",
            "PACKAGE_APPROVED",
            "CHANGE_PROPOSAL",
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
            "AUTO_MERGE_AFTER_REQUIRED_CHECKS",
            "AUTO_MERGE_ELIGIBLE",
        ):
            self.assertIn(term, text)
        self.assertNotIn("PR 병합은 별도로 사용자 승인이 필요하다", text)

    def test_master_plan_template_has_package_and_merge_contract(self) -> None:
        text = (ROOT / "templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
        for term in (
            "구현 패키지 지도",
            "데이터·저장·ID·Schema 보호 조건",
            "CHANGE_PROPOSAL",
            "PACKAGE_APPROVED",
            "USER_REVIEW_REQUIRED",
            "기본 병합 정책: `AUTO_MERGE_AFTER_REQUIRED_CHECKS`",
            "Required Check: `ci-gate`",
            "수동 사용자 병합 승인: `OPTIONAL_EXCEPTION`",
        ):
            self.assertIn(term, text)
        self.assertNotIn("사용자 병합 승인: `REQUIRED`", text)

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

    def test_package_contract_limits_codex_git_authority_and_gates_merge(self) -> None:
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
            "merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS | MANUAL_USER_APPROVAL",
            "required_check: ci-gate",
            "AUTO_MERGE_ELIGIBLE",
            "UNVERIFIED_REPOSITORY_SETTING",
        ):
            self.assertIn(term, text)

    def test_github_pro_policy_declares_safe_rollout_and_blocking_states(self) -> None:
        text = (ROOT / "docs/GITHUB_PRO_OPERATING_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "Base → 비공개 `omenward` → 다른 활성 프로젝트",
            "AUTO_MERGE_AFTER_REQUIRED_CHECKS",
            "required_approving_review_count: 0",
            "AUTO_MERGE_BLOCKED",
            "UNVERIFIED_REPOSITORY_SETTING",
            "USER_REVIEW_REQUIRED",
            "CHANGE_PROPOSAL",
            "비공개 Push ruleset",
        ):
            self.assertIn(term, text)

    def test_solo_main_ruleset_is_importable_and_requires_ci_gate(self) -> None:
        path = ROOT / "templates/project-operations/github/rulesets/solo-main-safety.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "solo-main-safety")
        self.assertEqual(data["target"], "branch")
        self.assertEqual(data["enforcement"], "active")
        self.assertEqual(data["conditions"]["ref_name"]["include"], ["~DEFAULT_BRANCH"])

        rules = {rule["type"]: rule for rule in data["rules"]}
        self.assertIn("deletion", rules)
        self.assertIn("non_fast_forward", rules)
        self.assertIn("required_linear_history", rules)
        self.assertEqual(
            rules["pull_request"]["parameters"]["required_approving_review_count"],
            0,
        )
        self.assertTrue(
            rules["pull_request"]["parameters"]["required_review_thread_resolution"]
        )
        self.assertEqual(
            rules["required_status_checks"]["parameters"]["required_status_checks"],
            [{"context": "ci-gate"}],
        )
        self.assertTrue(
            rules["required_status_checks"]["parameters"]
            ["strict_required_status_checks_policy"]
        )

    def test_documentation_map_routes_without_new_duplicate_skill(self) -> None:
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("Grill Me 핵심 의사결정 인터뷰", text)
        self.assertIn("`clarify` + `references/grill-me-protocol.md`", text)
        self.assertIn("GPT→Codex 단계별 Godot 구현 인계", text)
        self.assertIn("`implementation-package-handoff`", text)


if __name__ == "__main__":
    unittest.main()
