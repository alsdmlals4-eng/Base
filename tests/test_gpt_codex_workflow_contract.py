from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GptCodexWorkflowContractTests(unittest.TestCase):
    def test_work_sequence_reserves_review_for_implementation_before_merge(self) -> None:
        text = (ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md").read_text(encoding="utf-8")
        sequence = text.split("## 25. 자동 실행 순서", 1)[1].split("## 26.", 1)[0]
        self.assertIn("실제 구현 결과 검토에 최소 1회를 남긴다", sequence)
        implementation = sequence.index("16. 현재 승인된 Work capability")
        final_review = sequence.index("23. 남은 필수 작업이 0이면 실제 구현된 Completion Candidate")
        merge = sequence.index("24. required finding 0과 exact-head CI")
        self.assertLess(implementation, final_review)
        self.assertLess(final_review, merge)
        self.assertIn("이미 2회가 끝났다면 결함별 교정·표적 검증만", sequence)
        self.assertNotIn("14. 전체 결과를 정확히 2회", sequence)

    def test_active_research_and_combat_consumers_follow_same_capability_owner(self) -> None:
        for relative in (
            "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md",
            "skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md",
        ):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("docs/GPT_CODEX_WORKFLOW_POLICY.md", text)
                self.assertIn("현재 Work", text)
                self.assertIn("조건부 인계", text)
                self.assertNotIn("Codex 구현 패키지로 넘긴다", text)
                self.assertNotIn("Codex가 exact repository revision", text)

    def test_canonical_policy_uses_capability_not_application_name(self) -> None:
        text = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "UNIFIED_WORK_EXECUTION",
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "CAPABILITY_IS_NOT_AUTHORIZATION",
            "HANDOFF_ONLY_FOR_CAPABILITY_GAP_OR_EXPLICIT_REQUEST",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
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
            "PLANNING_CANON_BEFORE_HANDOFF",
            "PRE_HANDOFF_GPT_STOP",
            "FIX | TUNE | REDESIGN",
            "IMPACT_BOUNDED_REVALIDATION",
            "CANON_SYNC_AFTER_VALIDATION",
            "DIRECT_RUN_OR_VERIFIED_EVIDENCE",
            "플레이어 행동",
            "의미 있는 선택",
            "제외 범위",
            "필요한 데이터",
            "필요한 이미지·사운드",
        ):
            self.assertIn(term, policy)

    def test_planning_sequence_consumes_current_gpt_codex_slice_boundary(self) -> None:
        text = (ROOT / "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "PLAY_MEANINGFUL_WORK_SLICE",
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "docs/GPT_CODEX_WORKFLOW_POLICY.md",
            "UNIFIED_WORK_EXECUTION",
        ):
            self.assertIn(term, text)
        self.assertNotIn("OPTIONAL_CODEX_EXECUTOR", text)
        self.assertNotIn("GPT-first / Codex optional", text)

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
            "MISSING_CAPABILITY",
        ):
            self.assertIn(term, text)
        self.assertIn("구현 방향·기술 방법 결정", text)

    def test_handoff_reference_consumes_bounded_slice_contract(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md").read_text(encoding="utf-8")
        for term in (
            "PLAY_MEANINGFUL_WORK_SLICE",
            "work_slice_id",
            "explicit_non_scope",
            "CAPABILITY_GAP",
            "PLANNING_CANON_BEFORE_HANDOFF",
        ):
            self.assertIn(term, text)

    def test_active_handoff_skill_consumes_bounded_slice_contract(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "PLAY_MEANINGFUL_WORK_SLICE",
            "PLANNING_CANON_BEFORE_HANDOFF",
            "PRE_HANDOFF_GPT_STOP",
            "work_slice_id",
            "explicit_non_scope",
            "gpt-codex-implementation-handoff.md",
        ):
            self.assertIn(term, text)

    def test_recovery_pilot_is_owned_without_claiming_live_handoff_success(self) -> None:
        owner = ROOT / "skills/maintaining-project-context-and-handoff"
        skill = (owner / "SKILL.md").read_text(encoding="utf-8")
        for suffix in ("md", "json"):
            relative = f"references/long-horizon-failure-recovery-pilot.{suffix}"
            self.assertIn(relative, skill)
            self.assertTrue((owner / relative).is_file())
        pilot = json.loads((owner / "references/long-horizon-failure-recovery-pilot.json").read_text(encoding="utf-8"))
        self.assertEqual("PILOT_SPECIFICATION_NOT_RESULT", pilot["artifact_role"])
        self.assertEqual("NOT_RUN", pilot["live_model_run_status"])
        self.assertEqual(
            (owner / "references/fresh-read-project-bootstrap.md").relative_to(ROOT).as_posix(),
            pilot["owner"],
        )
        guide = (owner / "references/long-horizon-failure-recovery-pilot.md").read_text(encoding="utf-8")
        for marker in ("UNIT_GUARD_ONLY", "NO_PRODUCTION_AUTHORIZATION_GATE", "TRANSFER_ACCEPTED_NOT_CLAIMED"):
            self.assertIn(marker, guide)

    def test_work_mode_preserves_modes_without_forcing_executor_change(self) -> None:
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        for term in (
            "UNIFIED_WORK_EXECUTION",
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "CAPABILITY_IS_NOT_AUTHORIZATION",
            "NONCODING_BUILD",
            "GODOT_PRODUCT_BUILD",
            "REVIEW",
        ):
            self.assertIn(term, routing)

    def test_registry_does_not_route_code_or_runtime_alone_to_handoff(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        entry = next(
            item for item in registry["skills"]
            if item["skill_id"] == "maintaining-project-context-and-handoff"
        )
        for term in (
            "godot-product-implementation-handoff",
            "godot-work-instruction",
            "actual-capability-gap",
            "explicit-executor-handoff",
        ):
            self.assertIn(term, entry["trigger_tags"])
        for tag in ("gdscripting", "godot-scene-resource-implementation", "godot-runtime-test"):
            self.assertNotIn(tag, entry["trigger_tags"])
        self.assertFalse(entry["load_by_default"])
        self.assertTrue((ROOT / entry["path"]).is_file())
        self.assertEqual(
            entry["learning_log"],
            "skills/maintaining-project-context-and-handoff/LEARNING_LOG.md",
        )
        generated = (ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md").read_text(encoding="utf-8")
        self.assertIn("godot-product-implementation-handoff", generated)

    def test_handoff_skill_is_conditional_and_requires_project_rehydration(self) -> None:
        text = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "codex-godot-implementation-handoff",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF",
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "AGENTS.md",
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
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF",
            "구현 방향·기술 방법 결정",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "GPT_VISUAL_REQUEST",
            "CHANGE_PROPOSAL",
            "READY_FOR_GPT_REVIEW",
        ):
            self.assertIn(term, text)

    def test_historical_v3_contract_is_preserved_for_explicit_compatibility(self) -> None:
        data = json.loads((ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json").read_text(encoding="utf-8"))
        self.assertEqual(3, data["schema_version"])
        self.assertEqual("GPT_BASE_NOTION_GOVERNANCE_OWNER", data["base_governance_owner"])
        self.assertEqual("CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER", data["implementation_owner"])
        self.assertTrue(data["codex_not_general_repository_executor"])
        self.assertIn("BASE_VALIDATION_CONTRACT", data["gpt_repository_domains"])
        self.assertIn("GODOT_SCENE", data["codex_product_domains"])
        self.assertIn("GODOT_IMPLEMENTATION_TEST", data["codex_product_domains"])

    def test_current_v4_has_one_execution_owner_and_conditional_handoff(self) -> None:
        """Validate parsed routing edges; this does not attest live agent execution."""
        data = json.loads((ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json").read_text(encoding="utf-8"))
        self.assertEqual("ACTIVE_DEFAULT", data["status"])
        self.assertEqual("UNIFIED_WORK_EXECUTION", data["execution_model"])
        self.assertEqual("CAPABILITY_BASED_EXECUTOR_SELECTION", data["executor_selection"])
        self.assertIs(True, data["capability_is_not_authorization"])
        owner = (ROOT / data["execution_policy"]).resolve()
        self.assertTrue(owner.is_relative_to(ROOT.resolve()))
        self.assertTrue(owner.is_file())
        conditional = data["conditional_project_entrypoints"]
        self.assertEqual({"docs/handoffs/CURRENT_CODEX_HANDOFF.md": "ONLY_WHEN_ACTUAL_HANDOFF_IS_NEEDED"}, conditional)
        self.assertFalse(set(conditional).intersection(data["required_project_entrypoints"]))
        self.assertIn("AGENTS.md", data["required_project_entrypoints"])
        self.assertIn("assets/ASSET_MANIFEST.json", data["required_project_entrypoints"])
        self.assertFalse(data["legacy_contract"]["active_route_for_new_work"])
        self.assertTrue((ROOT / data["legacy_contract"]["path"]).is_file())

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
            "UNIFIED_WORK_EXECUTION",
            "CAPABILITY_BASED_EXECUTOR_SELECTION",
            "AGENTS.md",
            "Active Context",
            "REPOSITORY_PRIMARY_CANON",
            "project.godot",
            "actual evidence",
        ):
            self.assertIn(term, text)

    def test_base_partition_uses_capability_even_when_tests_or_ci_are_code(self) -> None:
        model = (ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md").read_text(encoding="utf-8")
        prompt = (ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md").read_text(encoding="utf-8")
        for text in (model, prompt):
            self.assertIn("Base", text)
            self.assertIn("CAPABILITY_BASED_EXECUTOR_SELECTION", text)
            self.assertIn("docs/GPT_CODEX_WORKFLOW_POLICY.md", text)
        self.assertIn("CAPABILITY_IS_NOT_AUTHORIZATION", prompt)

    def test_historical_role_records_can_remain_but_are_explicitly_superseded(self) -> None:
        review = (ROOT / "docs/reviews/2026-08-25-gpt-codex-role-split-adversarial-review.md").read_text(encoding="utf-8")
        followup = (ROOT / "docs/reviews/2026-08-25-gpt-codex-role-split-non-regression-followup.md").read_text(encoding="utf-8")
        learning = (ROOT / "skills/maintaining-project-context-and-handoff/LEARNING_LOG.md").read_text(encoding="utf-8")
        for text in (review, followup):
            self.assertIn("SUPERSEDED_BY_GODOT_PRODUCT_SCOPE_CORRECTION", text)
        self.assertIn("product responsibility, not code shape", learning)
        self.assertIn("SUPERSEDED INTERIM", learning)

    def test_repository_first_workspace_routes_fresh_read_and_codex_inputs(self) -> None:
        policy = (ROOT / "docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md").read_text(encoding="utf-8")
        combined = policy + "\n" + skill
        for term in (
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "REPOSITORY_PRIMARY_CANON",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "FRESH_READ_PROJECT_BOOTSTRAP",
        ):
            self.assertIn(term, combined)


if __name__ == "__main__":
    unittest.main()
