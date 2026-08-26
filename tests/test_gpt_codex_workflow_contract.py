from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GptCodexWorkflowContractTests(unittest.TestCase):
    def test_canonical_policy_scopes_codex_to_actual_godot_product_work(self) -> None:
        text = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "GPT_NONCODING_PROJECT_OWNER",
            "GPT_BASE_NOTION_GOVERNANCE_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION",
            "CODEX_IMAGE_GENERATION_FORBIDDEN",
            "CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY",
            "GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING",
            "CHANGE_PROPOSAL",
            "Base Python test",
        ):
            self.assertIn(term, text)
        self.assertNotIn("GPT_GODOT_PREPRODUCTION_ALLOWED", text)
        self.assertNotIn("OPTIONAL_CODEX_EXECUTOR", text)

    def test_gpt_project_work_is_bounded_by_play_meaningful_slice(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "PLAY_MEANINGFUL_WORK_SLICE",
            "TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT",
            "GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING",
            "EXISTING_SOLUTION_FIRST",
            "PRE_HANDOFF_GPT_STOP",
            "FIX | TUNE | REDESIGN",
            "IMPACT_BOUNDED_REVALIDATION",
            "CANON_SYNC_AFTER_VALIDATION",
            "플레이어 행동",
            "의미 있는 선택",
            "제외 범위",
            "필요한 데이터",
            "필요한 이미지·사운드",
        ):
            self.assertIn(term, policy)

    def test_codex_work_instruction_carries_slice_scope_without_prescribing_code(self) -> None:
        text = (ROOT / "templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md").read_text(encoding="utf-8")
        for term in (
            "PLAY_MEANINGFUL_WORK_SLICE",
            "work_slice_id",
            "player_action_and_choice",
            "explicit_non_scope",
            "required_data_and_inputs",
            "ui_ux_flow",
            "asset_audio_dependencies",
            "review_evidence_expected",
            "PRE_HANDOFF_GPT_STOP",
        ):
            self.assertIn(term, text)
        self.assertIn("구현 방향·기술 방법 결정", text)

    def test_work_mode_routes_base_notion_to_gpt_and_godot_product_to_codex(self) -> None:
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        for term in (
            "BASE_GOVERNANCE_BUILD_IS_GPT",
            "NOTION_BUILD_IS_GPT",
            "GODOT_PRODUCT_BUILD_IS_CODEX",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "BASE / NOTION / PLANNING / DOC / VISUAL → GPT",
            "ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex",
        ):
            self.assertIn(term, routing)

    def test_registry_routes_only_actual_godot_product_handoff(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        entry = next(
            item for item in registry["skills"]
            if item["skill_id"] == "maintaining-project-context-and-handoff"
        )
        for term in (
            "godot-product-implementation-handoff",
            "godot-work-instruction",
            "gdscripting",
            "godot-scene-resource-implementation",
            "godot-runtime-test",
        ):
            self.assertIn(term, entry["trigger_tags"])
        joined_use = "\n".join(entry["use_when"])
        joined_no = "\n".join(entry["do_not_use_when"])
        joined_review = "\n".join(entry["review_triggers"])
        self.assertIn("실제 게임 프로젝트", joined_use)
        self.assertIn("GDScript", joined_use)
        self.assertIn("Base 정책", joined_no)
        self.assertIn("Notion", joined_no)
        self.assertIn("Base/Notion 작업을 Codex에 넘김", joined_review)
        self.assertIn("코드 파일이라는 이유만으로 Codex owner로 분류", joined_review)
        self.assertEqual(
            entry["learning_log"],
            "skills/maintaining-project-context-and-handoff/LEARNING_LOG.md",
        )
        generated = (ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md").read_text(encoding="utf-8")
        self.assertIn("godot-product-implementation-handoff", generated)

    def test_handoff_skill_excludes_base_notion_and_requires_project_rehydration(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "codex-godot-implementation-handoff",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF",
            "Base/Notion/문서/기획/이미지 작업을 Codex에 넘기지 않는다",
            "Project `AGENTS.md`",
            "Notion Project Home/Domain/AI System",
            "CHANGE_PROPOSAL",
            "GPT_VISUAL_REQUEST",
            "READY_FOR_GPT_REVIEW",
            "fresh-read-project-bootstrap.md",
            "FRESH_READ_PROJECT_BOOTSTRAP",
            "과거 대화",
            "evidence ceiling",
        ):
            self.assertIn(term, text)

    def test_godot_work_instruction_is_intent_contract_not_line_by_line_script(self) -> None:
        text = (ROOT / "templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md").read_text(encoding="utf-8")
        for term in (
            "Codex Godot Product Implementation Work Instruction",
            "실제 게임 프로젝트의 Godot 제품 구현",
            "Base/Notion/문서/기획/이미지/운영 정본 작업에는 사용하지 않는다",
            "구현 방향·기술 방법 결정",
            "CODEX_IMAGE_GENERATION_FORBIDDEN",
            "GPT_VISUAL_REQUEST",
            "CHANGE_PROPOSAL",
            "READY_FOR_GPT_REVIEW",
        ):
            self.assertIn(term, text)

    def test_workspace_contract_separates_base_governance_and_godot_product_domains(self) -> None:
        data = json.loads((ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json").read_text(encoding="utf-8"))
        self.assertEqual(3, data["schema_version"])
        self.assertEqual("GPT_BASE_NOTION_GOVERNANCE_OWNER", data["base_governance_owner"])
        self.assertEqual("CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER", data["implementation_owner"])
        self.assertTrue(data["codex_not_general_repository_executor"])
        self.assertIn("BASE_VALIDATION_CONTRACT", data["gpt_repository_domains"])
        self.assertIn("GODOT_SCENE", data["codex_product_domains"])
        self.assertIn("GODOT_IMPLEMENTATION_TEST", data["codex_product_domains"])

    def test_handoff_resume_preserves_godot_runtime_freshness_and_wrong_target_safety(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        handoff = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        combined = policy + "\n" + handoff
        for term in (
            "CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED",
            "stale PID/session",
            "project.godot",
            "exact project/repository/worktree",
            "force push/history rewrite/destructive reset",
        ):
            self.assertIn(term, combined)

    def test_freshness_skill_still_protects_semantic_contracts(self) -> None:
        text = (ROOT / "skills/auditing-canonical-reference-freshness/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "consumer inventory",
            "CURRENT_MUTABLE",
            "CANONICAL_LOCATOR",
            "HISTORICAL_DISCOVERY",
            "COMPATIBILITY_ANCHOR",
            "SAFE_TO_DROP",
            "semantic contract",
            "literal protocol",
            "exact-head",
            "canonical owner 확인 전 제거·약화 금지",
        ):
            self.assertIn(term, text)

    def test_concurrent_git_sync_still_binds_task_identity_and_exact_heads(self) -> None:
        skill = (ROOT / "skills/synchronizing-local-and-github-state/SKILL.md").read_text(encoding="utf-8")
        protocol = (ROOT / "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md").read_text(encoding="utf-8")
        for term in (
            "CONCURRENT_CHANGE_PREFLIGHT",
            "current_task_or_pr_identity",
            "source_main_sha",
            "current_main_sha",
            "write_parent_sha",
            "same_goal_open_and_recent_prs",
            "STALE_BASE_SHA",
            "WAITING_RESOURCE",
            "DUPLICATE_WORK",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, skill)
        for term in (
            "exclude the current task or PR itself",
            "first persistent write",
            "post-merge main readback",
            "PATH_OVERLAP",
            "SEMANTIC_OVERLAP",
        ):
            self.assertIn(term, protocol)

    def test_codex_bootstrap_is_dynamic_and_project_scoped(self) -> None:
        text = (ROOT / "templates/custom-instructions.codex.md").read_text(encoding="utf-8")
        for term in (
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "AGENTS.md",
            "Active Context",
            "Notion Project Home",
            "project.godot",
            "actual evidence",
        ):
            self.assertIn(term, text)

    def test_base_partition_is_gpt_owned_even_when_tests_or_ci_are_code(self) -> None:
        model = (ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md").read_text(encoding="utf-8")
        prompt = (ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md").read_text(encoding="utf-8")
        for text in (model, prompt):
            self.assertIn("Base", text)
            self.assertIn("GPT", text)
            self.assertIn("CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR", text)
        self.assertIn("Base Python tests, Registry/generated/CI", model)
        self.assertIn("Base Python contract test·Registry/generated·CI policy", prompt)

    def test_historical_role_records_can_remain_but_are_explicitly_superseded(self) -> None:
        review = (ROOT / "docs/reviews/2026-08-25-gpt-codex-role-split-adversarial-review.md").read_text(encoding="utf-8")
        followup = (ROOT / "docs/reviews/2026-08-25-gpt-codex-role-split-non-regression-followup.md").read_text(encoding="utf-8")
        learning = (ROOT / "skills/maintaining-project-context-and-handoff/LEARNING_LOG.md").read_text(encoding="utf-8")
        for text in (review, followup):
            self.assertIn("SUPERSEDED_BY_GODOT_PRODUCT_SCOPE_CORRECTION", text)
        self.assertIn("product responsibility, not code shape", learning)
        self.assertIn("SUPERSEDED INTERIM", learning)


if __name__ == "__main__":
    unittest.main()
