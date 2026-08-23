from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillEvalIntegrityContractTests(unittest.TestCase):
    def test_functional_eval_integrity_stays_in_existing_adoption_owner(self) -> None:
        guide = (ROOT / "docs/AI_SKILL_ADOPTION_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("### EVAL_BEFORE_PROMOTION", guide)
        self.assertIn("#### Functional eval integrity", guide)
        self.assertNotIn("behavior-eval-integrity.md", guide)

    def test_oracle_pair_and_claim_ceiling_are_explicit(self) -> None:
        guide = (ROOT / "docs/AI_SKILL_ADOPTION_GUIDE.md").read_text(encoding="utf-8")
        for token in (
            "BROKEN_BASELINE",
            "REFERENCE_SOLUTION",
            "UNCHANGED_ORACLE_REQUIRED",
            "BLOCKED_INVALID_ORACLE",
            "FIXTURE_VALIDITY_NOT_SKILL_EFFICACY",
            "HIDDEN_GRADER_WHEN_CAUSAL_LEAKAGE",
            "GRADER_VISIBLE_CEILING",
            "SAME_HARNESS_AB",
            "EFFICIENCY_METRICS_SEPARATE_FROM_CORRECTNESS",
            "VALID_ORACLE_MODEL_RUN_NOT_RUN",
        ):
            self.assertIn(token, guide)

        self.assertIn("assertion·threshold·fixture·expected output을 약화하지 않는다", guide)
        self.assertIn("correctness uplift를 주장하지 않는다", guide)
        self.assertIn("자동 activation", guide)
        self.assertIn("실제 모델 행동 PASS로 승격하지 않는다", guide)

    def test_dedicated_skill_behavior_workflow_consumes_integrity_owner_and_regression(self) -> None:
        workflow = (ROOT / ".github/workflows/validate-skill-behavior-evidence.yml").read_text(encoding="utf-8")
        self.assertIn('- "docs/AI_SKILL_ADOPTION_GUIDE.md"', workflow)
        self.assertIn('- "tests/test_skill_eval_integrity_contract.py"', workflow)
        self.assertGreaterEqual(workflow.count("tests/test_skill_eval_integrity_contract.py"), 2)


if __name__ == "__main__":
    unittest.main()
