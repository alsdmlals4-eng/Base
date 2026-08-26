from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md"
CASE = ROOT / "docs/knowledge/cases/WORK_CODEX_STARTER_LOCAL_EXECUTION_SYNC_CASE.md"


class WorkCodexStarterLocalExecutionContractTests(unittest.TestCase):
    def _starter(self) -> str:
        self.assertTrue(STARTER.exists(), "copy-paste Work starter prompt must exist")
        return STARTER.read_text(encoding="utf-8")

    def test_starter_routes_current_base_profile_instead_of_copying_a_second_canon(self) -> None:
        text = self._starter()
        for token in (
            "USE_CURRENT_BASE_PROFILE_NOT_INLINE_DUPLICATE",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "EXPLICIT_USER_DELEGATION_REQUIRED",
            "CURRENT_BASE_OWNER_WINS_ON_DRIFT",
        ):
            self.assertIn(token, text)

    def test_git_fetch_pull_push_are_automatic_but_safe(self) -> None:
        text = self._starter()
        for token in (
            "AUTO_GIT_FETCH_AND_SAFE_PULL",
            "git fetch --prune origin",
            "git pull --ff-only",
            "DIRTY_OR_DIVERGED_STATE_RECONCILE_NO_FORCE",
            "AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "CURRENT_TASK_BRANCH_IDENTITY_REQUIRED",
            "NO_DIRECT_MAIN_PUSH",
            "POST_MERGE_MAIN_READBACK_AND_SAFE_LOCAL_MAIN_REFRESH",
            "git pull --ff-only origin main",
        ):
            self.assertIn(token, text)

    def test_project_scoped_local_computer_and_godot_control_are_delegated(self) -> None:
        text = self._starter()
        for token in (
            "LOCAL_COMPUTER_CONTROL_DELEGATED",
            "AUTO_LAUNCH_GODOT_WHEN_CALLABLE",
            "EXACT_PROJECT_EDITOR_SESSION_REQUIRED",
            "PROJECT_SCOPED_OS_AUTOMATION_ONLY",
            "PROJECT_PROCESS_ONLY_CLOSE",
            "TOOL_NOT_CALLABLE_DO_NOT_CLAIM",
            "STABLE_ENGINE_BASELINE_NO_AUTO_UPDATE",
            "NO_NEW_TOOL_INSTALL_OR_UPDATE_WITHOUT_CURRENT_OWNER_GATE",
            "PROJECT_SCOPED_BROWSER_AND_FILE_DIALOG_AUTOMATION_ALLOWED",
        ):
            self.assertIn(token, text)

    def test_local_control_keeps_security_and_scope_boundaries(self) -> None:
        text = self._starter()
        for token in (
            "NO_UNRELATED_APPLICATION_OR_FILE_ACCESS",
            "NO_CREDENTIAL_OR_SECRET_CAPTURE",
            "NO_OS_SECURITY_SETTINGS_OR_DESTRUCTIVE_SYSTEM_CHANGE",
            "NO_REMOTE_TUNNEL_OR_PUBLIC_PORT",
            "HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE",
            "NO_NEW_LOGIN_PERMISSION_OR_CONSENT_GRANT",
        ):
            self.assertIn(token, text)

    def test_downloadable_user_build_is_an_explicit_delivery_gate(self) -> None:
        text = self._starter()
        for token in (
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE",
            "BUILD_SHA256_AND_DURABLE_LOCATOR_REQUIRED",
            "CLEAN_EXTRACT_AND_LAUNCH_SMOKE_REQUIRED",
            "NO_PUBLIC_RELEASE_WITHOUT_HIGH_RISK_APPROVAL",
            "ARTIFACT_SECRET_AND_DEBUG_RESIDUE_SCAN_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_notion_audit_and_incident_learning_are_not_omitted(self) -> None:
        text = self._starter()
        for token in (
            "ONE_TIME_ACTIVE_PROJECT_NOTION_AUDIT_IF_NOT_EVIDENCED",
            "TARGETED_NOTION_AUDIT_AFTER_BASELINE",
            "INCIDENT_SOLUTION_LESSON_LOOP",
            "BASE_PROMOTION_DISPOSITION_REQUIRED",
            "destination readback",
            "NON_SLICE_NOTION_DEBT_DOES_NOT_BLOCK_CURRENT_SLICE",
        ):
            self.assertIn(token, text)

    def test_uncallable_codex_executor_cannot_be_promoted_to_implementation(self) -> None:
        text = self._starter()
        for token in (
            "CODEX_EXECUTOR_NOT_CALLABLE_DO_NOT_CLAIM_IMPLEMENTED",
            "DEFER_PRODUCT_IMPLEMENTATION_CONTINUE_WORK_READY_TASKS",
            "DURABLE_CODEX_HANDOFF_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_machine_qa_and_human_evidence_ceiling_remain_separate(self) -> None:
        text = self._starter()
        for token in (
            "MACHINE_QA_FIRST",
            "HUMAN_QA_DEFERRED_BY_CURRENT_USER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
            "DO_NOT_AUTO_ADVANCE_TO_NEXT_SLICE_BEFORE_USER_VALIDATION",
        ):
            self.assertIn(token, text)

    def test_problem_lesson_case_is_linked_and_project_neutral(self) -> None:
        text = self._starter()
        self.assertTrue(CASE.exists(), "starter correction learning case must exist")
        case = CASE.read_text(encoding="utf-8")
        self.assertIn("WORK_CODEX_STARTER_LOCAL_EXECUTION_SYNC_CASE.md", text)
        for token in (
            "STARTER_PROMPT_SHOULD_ROUTE_CURRENT_OWNER",
            "SAFE_PULL_IS_NOT_BLIND_PULL",
            "LOCAL_CONTROL_IS_CAPABILITY_BOUNDED",
            "DOWNLOADABLE_BUILD_IS_SEPARATE_FROM_PUBLIC_RELEASE",
        ):
            self.assertIn(token, case)
        for project_only in ("오멘워드", "십보강호", "Switchy Express"):
            self.assertNotIn(project_only, case)


if __name__ == "__main__":
    unittest.main()
