from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "evolving-project-discipline-skills" / "SKILL.md"
LEARNING_LOG = ROOT / "skills" / "evolving-project-discipline-skills" / "LEARNING_LOG.md"
REFERENCE = (
    ROOT
    / "skills"
    / "evolving-project-discipline-skills"
    / "references"
    / "verified-failure-learning-and-promotion.md"
)


class VerifiedFailureLearningContractTests(unittest.TestCase):
    def reference_text(self) -> str:
        self.assertTrue(REFERENCE.is_file(), "verified failure learning reference is missing")
        return REFERENCE.read_text(encoding="utf-8")

    def test_existing_learn_mode_routes_failure_evidence_without_new_skill(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        learning = LEARNING_LOG.read_text(encoding="utf-8")
        self.assertIn("→ learn`", skill)
        self.assertIn("learning_and_failure_evidence:", skill)
        self.assertIn("verified-failure-learning-and-promotion.md", learning)
        self.assertIn("VERIFIED_FAILURE_LEARNING", learning)

    def test_failure_learning_requires_verified_fix_before_reuse(self) -> None:
        text = self.reference_text()
        for marker in (
            "OBSERVED_FAILURE",
            "VERIFIED_FIX",
            "RECURRENCE_CANDIDATE",
            "PROACTIVE_CHECK_CANDIDATE",
            "PROMOTED_RULE",
            "FIX_VERIFICATION_REQUIRED_BEFORE_LEARNING",
            "SAME_RUN_RETRY_DOES_NOT_COUNT_AS_INDEPENDENT_EVIDENCE",
            "AUTOMATIC_SEMANTIC_PROMOTION_FORBIDDEN",
        ):
            self.assertIn(marker, text)

    def test_learning_entry_preserves_failure_context_and_counterevidence(self) -> None:
        text = self.reference_text()
        for field in (
            "failure_signature:",
            "exact_context:",
            "failing_evidence:",
            "root_cause:",
            "verified_fix:",
            "verification_after_fix:",
            "independent_occurrences:",
            "distinct_projects_or_contexts:",
            "false_positive_risk:",
            "counterexample_or_non_applicability:",
            "proactive_check_candidate:",
        ):
            self.assertIn(field, text)

    def test_base_rule_promotion_requires_recurrence_and_negative_validation(self) -> None:
        text = self.reference_text()
        for marker in (
            "CROSS_PROJECT_OR_INDEPENDENT_RECURRENCE_REQUIRED",
            "NEGATIVE_CASE_REQUIRED_BEFORE_PROACTIVE_PROMOTION",
            "EXISTING_OWNER_FIRST",
            "PREVENTED_OCCURRENCE_EVIDENCE",
            "PROJECT_LOCAL_FIRST_WHEN_SCOPE_IS_NARROW",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
