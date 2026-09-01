from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"
CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
V49 = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
AGENTS = ROOT / "AGENTS.md"
INTAKE_SKILL = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
DECOMPOSITION_OWNER = ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md"
EXECUTION_PLAN = ROOT / "templates/planning/EXECUTION_SEQUENCE_PLAN.md"
RECEIPT_VALIDATOR = ROOT / "tools/validate_work_contract_receipt.py"


class WorkProjectStartCanonChecklistContractTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"required Work contract must exist: {path}")
        return path.read_text(encoding="utf-8")

    def test_starter_routes_startup_canon_checklist_before_new_work(self) -> None:
        text = self._read(STARTER)
        for token in (
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST",
            "PROJECT_START_CANON_CHECKLIST_REQUIRED",
            "NO_NEW_SLICE_WORK_BEFORE_STARTUP_CORRECTION_OR_EXPLICIT_DEFER",
        ):
            self.assertIn(token, text)
        self.assertLess(
            text.index("STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST"),
            text.index("WORK_PRODUCTION_INPUT_PACKET"),
        )

    def test_checklist_surfaces_core_fun_core_systems_remaining_work_and_order(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "PROJECT_START_CANON_CHECKLIST",
            "project_goal:",
            "player_promise:",
            "pointed_fun:",
            "core_loop:",
            "core_systems:",
            "meaningful_choices:",
            "reward_and_failure_learning:",
            "current_stage:",
            "roadmap_or_milestones:",
            "accepted_frontier:",
            "active_playable_slice:",
            "next_playable_slice_candidate:",
            "remaining_required_work:",
            "work_order:",
            "next_safe_action:",
            "STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_swot_is_evidence_based_and_not_a_generic_marketing_fill_in(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "SWOT_IS_CURRENT_EVIDENCE_BASED_NOT_GENERIC_MARKETING",
            "strengths:",
            "weaknesses:",
            "opportunities:",
            "threats:",
            "evidence_and_owner:",
            "NOT_RUN",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
        ):
            self.assertIn(token, text)

    def test_material_project_work_receipt_recovers_genre_world_visual_and_benchmark_context(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "FRESH_READ_BEFORE_PROJECT_WORK_REQUIRED",
            "GENRE_WORLD_VISUAL_BENCHMARK_RECEIPT_REQUIRED",
            "ACTUAL_IMPLEMENTATION_EVIDENCE_NO_SPECULATION",
            "genre_and_subgenre:",
            "world_and_setting_tone:",
            "visual_style_and_composition_anchor:",
            "benchmark_decisions:",
            "ADOPT | ADAPT | REJECT | NOT_APPLICABLE",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, text)

    def test_material_work_requires_benchmark_and_reverse_engineering_preflight_before_execution(self) -> None:
        bundle = "\n".join(
            self._read(path)
            for path in (AGENTS, INTAKE_SKILL, CHECKLIST, DECOMPOSITION_OWNER)
        )
        for token in (
            "MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT",
            "BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED",
            "benchmark_preflight_state:",
            "PASS | REUSED_EVIDENCE | NOT_APPLICABLE | BLOCKED_UNVERIFIED",
            "source_and_evidence:",
            "observed_pattern:",
            "project_fit_and_difference:",
            "ADOPT | ADAPT | REJECT | NOT_APPLICABLE",
        ):
            self.assertIn(token, bundle)

    def test_material_work_hygiene_classifies_legacy_context_and_configuration_before_safe_cleanup(self) -> None:
        bundle = "\n".join(
            self._read(path)
            for path in (AGENTS, INTAKE_SKILL, CHECKLIST, DECOMPOSITION_OWNER)
        )
        for token in (
            "LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED",
            "ACTIVE_OWNER | COMPATIBILITY | ARCHIVE | OBSOLETE_CANDIDATE | UNKNOWN_UNVERIFIED",
            "NO_DELETION_BY_AGE_OR_NAME",
            "REFERENCES_AND_CONSUMERS_ZERO_BEFORE_REMOVAL",
            "GIT_RECOVERABLE_REMOVAL_AND_READBACK",
            "NO_BROAD_SWEEP_WITHOUT_SCOPE",
        ):
            self.assertIn(token, bundle)

    def test_receipt_is_machine_validated_in_the_base_contract_and_project_templates(self) -> None:
        intake = self._read(INTAKE_SKILL)
        checklist = self._read(CHECKLIST)
        decomposition = self._read(DECOMPOSITION_OWNER)
        plan = self._read(EXECUTION_PLAN)
        validator = self._read(RECEIPT_VALIDATOR)

        for source in (intake, checklist):
            for token in (
                "benchmark_preflight_receipt",
                "context_configuration_hygiene",
                "source_and_evidence",
                "observed_pattern",
                "project_fit_and_difference",
                "owner_or_provenance",
                "references_and_consumers",
            ):
                self.assertIn(token, source)
        for source in (intake, checklist, decomposition, plan):
            self.assertIn("validate_work_contract_receipt.py", source)
        for token in (
            "NOT_APPLICABLE is restricted to L0",
            "blocked_sources is required for BLOCKED_UNVERIFIED",
            "references_and_consumers_zero_before_removal is required",
            "git_recoverable_removal_and_readback is required",
        ):
            self.assertIn(token, validator)

    def test_canon_correction_precedes_new_planning_production_or_implementation(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST",
            "CORRECTION_BEFORE_PRODUCTION",
            "CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON",
            "CURRENT / HISTORICAL / SUPERSEDED / CONFLICT / UNKNOWN_UNVERIFIED",
            "REPOSITORY_PRIMARY_CANON",
            "repository_canon_readback:",
            "asset_manifest_readback:",
            "human_pdf_freshness_readback:",
            "legacy_migration:",
            "USER_DECISION_REQUIRED",
            "READY_AFTER_CORRECTION | BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, text)

    def test_previous_v48_v49_capabilities_remain_discoverable_in_current_bundle(self) -> None:
        files = (STARTER, CHECKLIST, V49, APPENDIX, PROFILE)
        bundle = "\n".join(self._read(path) for path in files)
        for token in (
            "REVISION_NON_REGRESSION_GATE",
            "WHOLE_PROJECT_AUDIT_FIRST",
            "REUSE_FIRST_PREFLIGHT_REQUIRED",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "VISUAL_REQUIREMENT_DELETE_TEST_GATE",
            "IMPLEMENTATION_REALITY_GATE",
            "PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY",
            "RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE",
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE",
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "CURRENT_SKILL_REGISTRY_COVERAGE_GATE",
            "DOMAIN_SPLIT_CANON",
            "TEXT_BRIEF_STOP_REQUIRED",
            "VISUAL_ASSET_COVERAGE",
            "ART_STYLE_LOCK",
            "DECISION_SCREEN_COMPREHENSION_GATE",
            "MULTI_PLATFORM_SHARED_CORE_GATE",
            "AUDIO_VISUAL_POC_EVIDENCE",
            "CANONICAL_REFLECTION_AFTER_PLAY",
            "EVIDENCE_EQUIVALENT_FALLBACK_ONLY",
            "INCIDENT_SOLUTION_LESSON_LOOP",
            "REQUIRED_WORK_REMAINING: 0",
            "COMPLETION_CANDIDATE",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "REMOTE_HEAD_READBACK_AFTER_PUSH",
            "NO_DIRECT_MAIN_PUSH",
            "NO_FORCE_PUSH",
            "LOCAL_COMPUTER_CONTROL_DELEGATED",
            "AUTO_LAUNCH_GODOT_WHEN_CALLABLE",
            "REPOSITORY_PRIMARY_CANON",
            "CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA",
            "APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
        ):
            self.assertIn(token, bundle)

    def test_checklist_defines_receipt_format_without_becoming_project_canon(self) -> None:
        text = self._read(CHECKLIST)
        self.assertIn("project-specific 실행 receipt의 형식과 Gate", text)
        self.assertIn("CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON", text)
        self.assertIn(
            "durable 사실과 결정은 project repository의 분야별 structured/runtime canon이 소유",
            text,
        )
        self.assertIn("사람용 PDF와 이 receipt가 그 사실을 덮어쓰지 않는다", text)

    def test_work_order_is_dependency_and_player_value_driven(self) -> None:
        text = self._read(CHECKLIST)
        for token in (
            "priority:",
            "status:",
            "why_now:",
            "dependency:",
            "player_value:",
            "risk_or_blocker:",
            "owner:",
            "acceptance:",
            "verification:",
            "fallback_or_defer:",
        ):
            self.assertIn(token, text)

    def test_legacy_notion_is_migration_only_not_a_startup_requirement(self) -> None:
        checklist = self._read(CHECKLIST)
        starter = self._read(STARTER)
        for token in (
            "NOTION_UNIQUE_CANON_COUNT",
            "CODEX_NOTION_DEPENDENCY_COUNT",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
        ):
            self.assertIn(token, checklist + "\n" + starter)
        self.assertNotIn(
            "→ exact Project Notion Home / active Domain / Visual / Asset / Flow / Production",
            starter,
        )


if __name__ == "__main__":
    unittest.main()
