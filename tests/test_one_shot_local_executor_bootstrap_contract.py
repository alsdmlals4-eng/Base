from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class OneShotLocalExecutorBootstrapContractTests(unittest.TestCase):
    def test_policy_scopes_execution_freshness_to_godot_product_codex(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED",
            "actual game-project Godot product implementation",
            "exact project/repository/worktree identity",
            "stale PID/session",
            "project.godot",
        ):
            self.assertIn(term, policy)
        self.assertIn("GPT→PowerShell→local Codex one-shot launcher", policy)
        self.assertNotIn("ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP", policy)

    def test_godot_template_preserves_project_authoring_and_live_qa_safety(self) -> None:
        godot_template = (
            ROOT
            / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
        ).read_text(encoding="utf-8")
        for term in (
            "matching editor",
            "fresh",
            "HiGodot",
            "Hera",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
        ):
            self.assertIn(term, godot_template)

    def test_base_contract_is_not_generic_local_codex_launcher(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        combined = policy + "\n" + (
            ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Base Python test, CI contract, Registry/generated checker", policy)
        self.assertIn("Base/Notion work not Codex trigger", policy)
        for forbidden_project_literal in (
            "GRIMOIRE-",
            "8001",
            "9501",
            ".codex-grimoire",
            "task8-spell-use-screen-v2",
            "Hera 1.0.0",
        ):
            self.assertNotIn(forbidden_project_literal, combined)

    def test_capability_discovery_support_history_remains_available(self) -> None:
        executor_policy = (ROOT / "docs/LOOP_A2_LOCAL_EXECUTOR.md").read_text(encoding="utf-8")
        learning = (
            ROOT / "skills/managing-project-intake-and-work-contract/LEARNING_LOG.md"
        ).read_text(encoding="utf-8")
        for term in (
            "CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION",
            "DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE",
            "PATHEXT",
            "semantic readiness probe",
            "discovery는 넓게, authority와 acceptance는 좁게",
        ):
            self.assertIn(term, executor_policy)
        self.assertIn("codex.exe", learning)
        self.assertIn("codex login status", learning)
        self.assertIn("diagnostic", learning.lower())

    def test_validation_workflow_still_tracks_this_compatibility_contract(self) -> None:
        workflow = (
            ROOT / ".github/workflows/validate-one-shot-local-executor-bootstrap.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("tests/test_one_shot_local_executor_bootstrap_contract.py", workflow)
        self.assertIn("docs/GPT_CODEX_WORKFLOW_POLICY.md", workflow)


if __name__ == "__main__":
    unittest.main()
