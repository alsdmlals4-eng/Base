from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"


class EvidenceKnowledgeWorkflowContractTests(unittest.TestCase):
    def test_dedicated_workflow_runs_all_contract_tests(self) -> None:
        self.assertTrue(WORKFLOW.is_file())
        content = WORKFLOW.read_text(encoding="utf-8")

        for required_path in (
            "tests/test_evidence_based_game_development_knowledge.py",
            "tests/test_evidence_knowledge_workflow_contract.py",
            "tests/test_human_validation_artifact_governance.py",
            "tests/test_synthetic_tester_simulation_governance.py",
            "tests/test_prompt_recipe_reference_contract.py",
            "skills/SKILL_LEARNING_LOG.md",
            "skills/governing-game-user-research-coverage/references/**",
            "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            "docs/knowledge/game-development/**",
            "docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md",
            "templates/research/**",
        ):
            self.assertIn(required_path, content)

        self.assertIn("python -m py_compile", content)
        self.assertIn("python -m unittest", content)
        self.assertIn("contents: read", content)
        self.assertNotIn("contents: write", content)
        self.assertNotIn("git push", content)
        self.assertNotIn("prepend-learning-entry", content)


if __name__ == "__main__":
    unittest.main()
