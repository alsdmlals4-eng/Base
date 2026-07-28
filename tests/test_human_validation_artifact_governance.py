from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class HumanValidationArtifactGovernanceTests(unittest.TestCase):
    def test_reference_and_template_exist(self) -> None:
        reference_path = (
            ROOT
            / "skills"
            / "governing-game-user-research-coverage"
            / "references"
            / "human-validation-artifact-governance.md"
        )
        template_path = ROOT / "templates" / "research" / "HUMAN_VALIDATION_SESSION_PACKET.md"

        self.assertTrue(reference_path.is_file())
        self.assertTrue(template_path.is_file())

    def test_reference_claim_ceiling_and_small_sample_contract(self) -> None:
        reference = read(
            "skills/governing-game-user-research-coverage/references/"
            "human-validation-artifact-governance.md"
        )

        for term in (
            "artifact_fidelity",
            "claim_ceiling",
            "SIMULATED_COMPONENT",
            "SCRIPTED_OUTCOME",
            "FIXED_STIMULUS",
            "ALGORITHM_ACCURACY",
            "first_attempt",
            "post_feedback_attempt",
            "behavior_observation",
            "player_self_report",
            "facilitator_intervention",
            "PROMISING_DIRECTION",
            "ADAPT",
            "REWORK",
            "REJECT",
            "STOP",
            "작은 표본 비율만으로 제품 방향을 `ADOPT`",
            "NOT_RUN",
        ):
            self.assertIn(term, reference)

    def test_session_packet_separates_evidence_sources(self) -> None:
        template = read("templates/research/HUMAN_VALIDATION_SESSION_PACKET.md")

        for term in (
            "artifact_fidelity",
            "simulated_components",
            "scripted_components",
            "fixed_outcomes",
            "claim_ceiling",
            "first_attempt",
            "post_feedback_attempt",
            "behavior_observation",
            "player_self_report",
            "facilitator_intervention",
            "system_or_artifact_log",
            "critical_incident",
            "PROMISING_DIRECTION | ADAPT | REWORK | REJECT | STOP",
            "claims_not_allowed",
            "next_fidelity_gate",
            "NOT_RUN",
        ):
            self.assertIn(term, template)

    def test_skill_and_documentation_map_route_governance(self) -> None:
        skill = read("skills/governing-game-user-research-coverage/SKILL.md")
        doc_map = read("docs/DOCUMENTATION_MAP.md")

        reference_path = (
            "skills/governing-game-user-research-coverage/references/"
            "human-validation-artifact-governance.md"
        )
        template_path = "templates/research/HUMAN_VALIDATION_SESSION_PACKET.md"

        for text in (skill, doc_map):
            self.assertIn(reference_path, text)
            self.assertIn(template_path, text)

        for term in (
            "simulated",
            "작은 표본",
            "행동",
            "자기보고",
            "진행자",
        ):
            self.assertIn(term, skill)

    def test_learning_and_changelog_record_pilot_findings(self) -> None:
        learning = read("skills/SKILL_LEARNING_LOG.md")
        changelog = read("docs/CHANGELOG.md")

        for term in (
            "사람 검증 Artifact",
            "작은 표본",
            "simulated",
            "PROMISING_DIRECTION",
        ):
            self.assertIn(term, learning)
            self.assertIn(term, changelog)

    def test_no_duplicate_human_validation_skill(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")

        self.assertNotIn('"skill_id":"human-validation-artifact-governance"', registry)
        self.assertNotIn('"skill_id":"running-human-validation-sessions"', registry)
        self.assertEqual(
            registry.count('"skill_id":"governing-game-user-research-coverage"'),
            1,
        )


if __name__ == "__main__":
    unittest.main()
