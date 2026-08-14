from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class OneShotLocalExecutorBootstrapContractTests(unittest.TestCase):
    def test_shared_policy_and_godot_template_require_one_shot_bootstrap(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        godot_template = (
            ROOT
            / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
        ).read_text(encoding="utf-8")

        for text in (policy, godot_template):
            self.assertIn("ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP", text)
            self.assertIn("BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY", text)

        self.assertIn("one copy/paste", policy)
        self.assertIn("exact project/worktree", policy)
        self.assertIn("matching editor", godot_template)
        self.assertIn("fresh", godot_template)
        self.assertIn("HiGodot", godot_template)

    def test_project_dedicated_local_environment_is_required_before_local_work(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        godot_template = (
            ROOT
            / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
        ).read_text(encoding="utf-8")
        combined = policy + "\n" + godot_template

        for token in (
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "ASSUME_PREVIOUS_POWERSHELL_CLOSED",
            "CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST",
        ):
            self.assertIn(token, combined)

        self.assertIn("live-QA", combined)
        self.assertIn("non-authoring", combined)
        self.assertIn("adversarial", combined.lower())
        self.assertIn("Hera", godot_template)
        self.assertIn("LIVE_QA_AND_OBSERVABILITY_ONLY", godot_template)

    def test_base_contract_stays_project_neutral_and_fail_closed(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        godot_template = (
            ROOT
            / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
        ).read_text(encoding="utf-8")
        combined = policy + "\n" + godot_template

        for term in ("reset", "restore", "clean"):
            self.assertIn(term, combined)

        for forbidden_project_literal in (
            "GRIMOIRE-",
            "8001",
            "9501",
            ".codex-grimoire",
            "task8-spell-use-screen-v2",
            "Hera 1.0.0",
        ):
            self.assertNotIn(forbidden_project_literal, combined)

    def test_bootstrap_discovers_capability_before_rejecting_one_executable_literal(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
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
            self.assertIn(term, policy)

        self.assertIn("codex.exe", learning)
        self.assertIn("codex login status", learning)
        self.assertIn("diagnostic", learning.lower())
        self.assertIn("trusted", policy.lower())


if __name__ == "__main__":
    unittest.main()
