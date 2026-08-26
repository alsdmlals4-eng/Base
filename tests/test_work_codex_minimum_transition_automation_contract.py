from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"


class WorkCodexMinimumTransitionAutomationContractTests(unittest.TestCase):
    def _profile_text(self) -> str:
        self.assertTrue(PROFILE.exists(), "opt-in minimum-transition profile must exist")
        return PROFILE.read_text(encoding="utf-8")

    def test_profile_is_discoverable_from_the_work_bundle(self) -> None:
        appendix = APPENDIX.read_text(encoding="utf-8")
        self.assertTrue(PROFILE.exists(), "opt-in minimum-transition profile must exist")
        self.assertIn("WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md", appendix)
        self.assertIn("EXPLICIT_USER_DELEGATION_REQUIRED", appendix)

    def test_profile_defines_three_stage_minimum_transition_flow(self) -> None:
        text = self._profile_text()
        for token in (
            "WORK_PREP_COMPLETION_BEFORE_CODEX",
            "WORK_PRODUCTION_INPUT_BATCH",
            "MINIMIZE_WORK_CODEX_TRANSITIONS",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "CONSOLIDATED_RETURN_PACKET",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertLess(text.index("WORK_PREP_COMPLETION_BEFORE_CODEX"), text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"))
        self.assertLess(text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"), text.index("READY_FOR_USER_VERTICAL_SLICE_VALIDATION"))

    def test_routine_approval_is_delegated_but_high_risk_remains_deferred(self) -> None:
        text = self._profile_text()
        for token in (
            "DELEGATED_RECOMMENDED_DEFAULT_APPROVAL",
            "NO_ROUTINE_APPROVAL_STOPS",
            "HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE",
            "HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE",
            "NO_AUTOMATIC_SCOPE_EXPANSION",
        ):
            self.assertIn(token, text)
        for risk in (
            "IRREVERSIBLE_DATA_LOSS",
            "ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION",
            "NEW_PAID_COST",
            "LEGAL_OR_RIGHTS_UNCERTAINTY",
            "PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION",
            "FORCE_DIRECT_MAIN_ADMIN_BYPASS",
        ):
            self.assertIn(risk, text)

    def test_stall_recovery_and_scope_bounded_zero_are_explicit(self) -> None:
        text = self._profile_text()
        for token in (
            "STALL_SIGNAL_ROUTE_SWITCH",
            "BOUNDED_RETRY_THEN_FALLBACK",
            "EVIDENCE_EQUIVALENT_FALLBACK_ONLY",
            "DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK",
            "SCOPE_BOUNDED_REQUIRED_WORK_ZERO",
            "AUTOMATION_PHASE_REMAINING_WORK_ZERO",
            "COMPLETION_CANDIDATE_RESCAN",
        ):
            self.assertIn(token, text)

    def test_machine_qa_is_required_without_claiming_human_or_player_pass(self) -> None:
        text = self._profile_text()
        for token in (
            "MACHINE_QA_FIRST",
            "GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED",
            "HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED",
            "HERA_PERSISTENT_AUTHORING_FORBIDDEN",
            "HERA_PHASE_SOURCE_DELTA_NONE",
            "HUMAN_QA_DEFERRED_BY_CURRENT_USER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "AUTOMATED_VERTICAL_SLICE_READY",
        ):
            self.assertIn(token, text)

    def test_automated_readiness_requires_completed_codex_implementation(self) -> None:
        text = self._profile_text()
        self.assertIn("Codex one-window implementation completed", text)
        self.assertNotIn("Codex one-window implementation attempted", text)

    def test_work_final_review_precedes_user_validation(self) -> None:
        text = self._profile_text()
        self.assertIn("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION", text)
        self.assertLess(
            text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"),
            text.index("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION"),
        )
        self.assertLess(
            text.index("WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION"),
            text.index("READY_FOR_USER_VERTICAL_SLICE_VALIDATION"),
        )

    def test_missing_adopted_qa_tool_requires_evidence_equivalent_machine_qa(self) -> None:
        text = self._profile_text()
        self.assertIn("EVIDENCE_EQUIVALENT_MACHINE_QA_REQUIRED_WHEN_NOT_ADOPTED", text)
        self.assertIn("BLOCKING_HIGH_RISK_PREVENTS_PHASE_ADVANCE", text)

    def test_profile_composes_current_owners_instead_of_becoming_second_canon(self) -> None:
        text = self._profile_text()
        for token in (
            "COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON",
            "continuous-work-execution.md",
            "docs/GPT_CODEX_WORKFLOW_POLICY.md",
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            "IMAGE_CONVERSATION_APPROVAL_GATE.md",
            "skills/designing-vertical-slices/SKILL.md",
            "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
            "skills/synchronizing-local-and-github-state/SKILL.md",
            "safe-sync-protocol.md",
        ):
            self.assertIn(token, text)

    def test_automatic_git_fetch_and_safe_pull_are_explicit(self) -> None:
        text = self._profile_text()
        for token in (
            "AUTOMATIC_GIT_FETCH_AUTHORIZED",
            "AUTOMATIC_SAFE_PULL_AUTHORIZED",
            "FETCH_BEFORE_START_RESUME_WRITE_PR_MERGE",
            "PULL_FAST_FORWARD_ONLY",
            "DIRTY_OR_DIVERGED_NO_BLIND_PULL",
            "NO_AUTOMATIC_STASH_RESET_CLEAN_REBASE_FORCE",
            "GITHUB_CONNECTOR_REFRESH_EQUIVALENT_WHEN_NO_LOCAL_WORKTREE",
            "git fetch --prune <intended-remote>",
            "git pull --ff-only",
        ):
            self.assertIn(token, text)

    def test_automatic_git_sync_preserves_local_and_remote_work(self) -> None:
        text = self._profile_text()
        for token in (
            "EXACT_REPOSITORY_BRANCH_UPSTREAM_IDENTITY_REQUIRED",
            "CLEAN_TRACKING_BRANCH_REQUIRED_FOR_PULL",
            "WRONG_WORKTREE_OR_UPSTREAM_ABORTS_PULL",
            "NO_PR_BRANCH_TAKEOVER_FROM_PULL",
            "POST_SYNC_EXACT_SHA_READBACK",
        ):
            self.assertIn(token, text)

    def test_godot_launch_and_project_scoped_computer_control_are_authorized(self) -> None:
        text = self._profile_text()
        for token in (
            "AUTOMATIC_GODOT_LAUNCH_AUTHORIZED",
            "PROJECT_SCOPED_COMPUTER_CONTROL_AUTHORIZED",
            "CALLABLE_TOOL_ONLY_NO_CAPABILITY_CLAIM",
            "EXACT_PROJECT_WINDOW_PROCESS_IDENTITY_REQUIRED",
            "SEMANTIC_CONTROL_BEFORE_PIXEL_COORDINATE_GUI",
            "UNRELATED_USER_SESSION_AND_PROCESS_PROTECTED",
            "godot --editor --path <project-directory>",
            "godot --path <project-directory>",
        ):
            self.assertIn(token, text)

    def test_computer_control_keeps_sensitive_and_destructive_actions_deferred(self) -> None:
        text = self._profile_text()
        for token in (
            "CREDENTIAL_ACCOUNT_SECURITY_OS_SETTINGS_FORBIDDEN",
            "UNRELATED_FILE_AND_APPLICATION_ACCESS_FORBIDDEN",
            "UNRELATED_PROCESS_TERMINATION_FORBIDDEN",
            "SOFTWARE_INSTALL_OR_UPDATE_REQUIRES_CURRENT_ADOPTION_AUTHORITY",
            "PUBLIC_UPLOAD_RELEASE_PURCHASE_FORBIDDEN_WITHOUT_HIGH_RISK_APPROVAL",
            "ACTIVE_USER_SESSION_CONFLICT_LOCAL_DEFER_OR_NEW_SESSION",
        ):
            self.assertIn(token, text)

    def test_default_approval_and_owner_boundaries_are_preserved(self) -> None:
        text = self._profile_text()
        for token in (
            "OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT",
            "DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION",
            "WORK_NONPRODUCT_OWNER_PRESERVED",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED",
            "CURRENT_SLICE_ONLY",
            "HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
