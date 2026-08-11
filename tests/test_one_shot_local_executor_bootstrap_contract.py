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
        ):
            self.assertNotIn(forbidden_project_literal, combined)


if __name__ == "__main__":
    unittest.main()
