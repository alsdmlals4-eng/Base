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
            "AGENT_MERGE_REQUIRED",
        ):
            self.assertIn(term, text)
        self.assertNotIn("사용자의 명시적 승인 전에는 PR을 병합하지 않는다", text)

    def test_on_demand_handoff_allows_gpt_preproduction_and_optional_codex_preflight(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for text in (policy, routing, handoff):
            self.assertIn("ON_DEMAND_CODEX_HANDOFF", text)
            self.assertIn("USER_REQUESTED_CODEX_HANDOFF", text)
            self.assertIn("CODEX_PREFLIGHT_OPTIONAL", text)
        self.assertIn("GPT_GODOT_PREPRODUCTION_ALLOWED", policy)
        self.assertIn("기획·구현·POC 누적", routing)
        self.assertIn("실제 저장소·프로젝트·Godot 상태", handoff)

    def test_continuous_work_can_handoff_same_approved_scope_without_reapproval(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        reference = (ROOT / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md").read_text(encoding="utf-8")
        for text in (policy, routing, reference):
            self.assertIn("CONTINUOUS_WORK_EXECUTOR_HANDOFF", text)
            self.assertIn("DEFERRED_EXTERNAL_EXECUTOR", text)
        for term in (
            "Codex로 넘길까요?",
            "현재 세션",
            "HiGodot",
            "실제로",
        ):
            self.assertIn(term, policy)
        self.assertIn("현재 세션 부재와 전체 실행 경로 부재", routing)
        self.assertIn("alternate executor", reference)
        self.assertIn("우회", reference)

    def test_explicit_approval_inherits_merge_authority_without_reapproval(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for text in (policy, routing, handoff):
            self.assertIn("APPROVED_ITEM_INHERITS_MERGE_AUTHORITY", text)
            self.assertIn("추가 확인·재승인·병합 승인 요청 없이", text)
        self.assertIn("명시적 승인이 완료된 항목", policy)

    def test_machine_registry_routes_on_demand_codex_handoff(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "maintaining-project-context-and-handoff"
        )
        for term in (
            "on-demand-codex-handoff",
            "codex-handoff",
            "codex-work-spec",
        ):
            self.assertIn(term, entry["trigger_tags"])
        joined_use = "\n".join(entry["use_when"])
        joined_review = "\n".join(entry["review_triggers"])
        self.assertIn("USER_REQUESTED_CODEX_HANDOFF", joined_use)
        self.assertIn("실제 저장소·프로젝트·Godot 상태", joined_use)
        self.assertIn("불필요한 Codex Plan 강제", joined_review)
        self.assertIn("승인 완료 항목 재승인 요구", joined_review)
        self.assertEqual(
            entry["learning_log"],
            "skills/maintaining-project-context-and-handoff/LEARNING_LOG.md",
        )

        generated = (ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md").read_text(encoding="utf-8")
        self.assertIn("on-demand-codex-handoff", generated)

    def test_handoff_skill_has_implementation_package_mode(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "implementation-package-handoff",
            "PLAN_REVIEW_ONLY",
            "godot_runtime_files_only",
            "ALLOWED_BRANCH_ONLY",
            "PACKAGE_APPROVED",
            "CHANGE_PROPOSAL",
            "AGENT_MERGE_REQUIRED",
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
            "병합 실행: `AGENT_MERGE_REQUIRED`",
            "Required Check: `ci-gate`",
            "별도 사용자 병합 승인: `NOT_REQUIRED`",
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
            "merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS",
            "agent_merge_execution: REQUIRED",
            "required_check: ci-gate",
            "AUTO_MERGE_ELIGIBLE",
            "UNVERIFIED_REPOSITORY_SETTING",
        ):
            self.assertIn(term, text)
        self.assertNotIn("MANUAL_USER_APPROVAL", text)

    def test_base_rules_require_agent_merge_after_all_gates(self) -> None:
        rules = (ROOT / "docs/BASE_RULES_VERSION.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for text in (rules, routing, handoff):
            self.assertIn("AGENT_MERGE_REQUIRED", text)
        self.assertIn("A separate user merge", rules)
        self.assertIn("별도 사용자 병합 승인", routing)
        self.assertIn("별도 사용자 병합 승인", handoff)
        self.assertNotIn("사용자의 명시적 승인 전에는 PR을 병합하지 않는다", routing)
        self.assertNotIn("사용자의 명시적 승인 전에는 PR을 병합하지 않는다", handoff)

    def test_github_pro_policy_declares_safe_rollout_and_blocking_states(self) -> None:
        text = (ROOT / "docs/GITHUB_PRO_OPERATING_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "Public project pilot",
            "standard GitHub-hosted",
            "REMOTE_CI",
            "LOCAL_FALLBACK",
            "AUTO_MERGE_AFTER_REQUIRED_CHECKS",
            "승인 리뷰 수 `0`",
            "AUTO_MERGE_BLOCKED",
            "UNVERIFIED_REPOSITORY_SETTING",
            "USER_REVIEW_REQUIRED",
            "CHANGE_PROPOSAL",
            "비공개 Push ruleset",
        ):
            self.assertIn(term, text)
        self.assertNotIn("Base → 비공개 `omenward` → 다른 활성 프로젝트", text)

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

    def test_cold_start_docs_match_on_demand_handoff_and_skill_growth_policy(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        docs_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")

        self.assertIn("Codex 작업 명세·전환", start)
        self.assertIn("on-demand-codex-handoff", start)
        self.assertIn("USER_REQUESTED_CODEX_HANDOFF", docs_map)
        self.assertIn("CODEX_PREFLIGHT_OPTIONAL", docs_map)
        self.assertIn("독립 입력·산출물·권한·검증 경계", operating)
        self.assertIn("새 Skill을 만들 수 있다", operating)
        self.assertNotIn("새 광역 Skill을 만들지 않는다.", operating)

    def test_documentation_map_routes_without_new_duplicate_skill(self) -> None:
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        for term in (
            "Grill Me 핵심 의사결정 인터뷰",
            "`clarify` + `references/grill-me-protocol.md`",
            "GPT→Codex 단계별 Godot 구현 인계",
            "`implementation-package-handoff`",
            "GitHub Pro 저장소 운영",
            "GitHub Pro 보호·Ruleset·자동 병합",
            "GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md",
            "GITHUB_USAGE_BUDGET.md",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
