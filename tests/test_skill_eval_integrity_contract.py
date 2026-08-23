from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillEvalIntegrityContractTests(unittest.TestCase):
    def test_functional_eval_integrity_is_owned_by_existing_skill(self) -> None:
        skill = (
            ROOT / "skills/evolving-project-discipline-skills/SKILL.md"
        ).read_text(encoding="utf-8")
        reference_path = (
            ROOT
            / "skills/evolving-project-discipline-skills/references/behavior-eval-integrity.md"
        )
        self.assertTrue(reference_path.is_file())
        self.assertIn("references/behavior-eval-integrity.md", skill)
        self.assertIn("BLOCKED_INVALID_ORACLE", skill)
        self.assertIn("VALID_ORACLE_MODEL_RUN_NOT_RUN", skill)
        self.assertIn("behavioral grader", skill)

    def test_oracle_pair_and_claim_ceiling_are_explicit(self) -> None:
        reference = (
            ROOT
            / "skills/evolving-project-discipline-skills/references/behavior-eval-integrity.md"
        ).read_text(encoding="utf-8")
        for token in (
            "BROKEN_BASELINE",
            "REFERENCE_SOLUTION",
            "UNCHANGED_ORACLE_REQUIRED",
            "FIXTURE_VALIDITY_NOT_SKILL_EFFICACY",
            "HIDDEN_GRADER_WHEN_CAUSAL_LEAKAGE",
            "GRADER_VISIBLE_CEILING",
            "SAME_HARNESS_AB",
            "EFFICIENCY_METRICS_SEPARATE_FROM_CORRECTNESS",
            "COMPARATIVE_EVAL_COMPLETE",
        ):
            self.assertIn(token, reference)

        self.assertIn("oracle을 약화해 green으로 만들지 않는다", reference)
        self.assertIn("correctness uplift를 주장하지 않는다", reference)
        self.assertIn("자동 activation", reference)


if __name__ == "__main__":
    unittest.main()
