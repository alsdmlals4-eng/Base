from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class SyntheticTesterSimulationGovernanceTests(unittest.TestCase):
    def test_governance_and_template_exist(self) -> None:
        governance = (
            ROOT
            / "docs"
            / "knowledge"
            / "game-development"
            / "SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md"
        )
        template = ROOT / "templates" / "research" / "SYNTHETIC_TESTER_SIMULATION_PACKET.md"

        self.assertTrue(governance.is_file())
        self.assertTrue(template.is_file())

    def test_governance_preserves_evidence_and_authority_boundaries(self) -> None:
        governance = read(
            "docs/knowledge/game-development/"
            "SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md"
        )

        for term in (
            "SYNTHETIC_TESTER_SIMULATION",
            "T6_AI_INFERENCE",
            "human_validation: NOT_RUN",
            "ai_simulation: COMPLETED",
            "implementation_authority: NONE",
            "assumption_not_observation",
            "actual_player_behavior",
            "actual_fun",
            "actual_preference",
            "actual_usability",
            "actual_performance",
            "ADOPT",
            "VALIDATED",
            "HUMAN_TEST_PASSED",
            "PROMISING_DIRECTION",
            "ADAPT",
            "REWORK",
            "REJECT",
            "TEST",
            "STOP",
        ):
            self.assertIn(term, governance)

    def test_governance_requires_project_structure_analysis_first(self) -> None:
        governance = read(
            "docs/knowledge/game-development/"
            "SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md"
        )

        for term in (
            "current_skill_registry",
            "selected_project_skills",
            "selected_base_skills",
            "work_mode",
            "canonical_sources",
            "protected_paths",
            "validation_routes",
            "current_status_sources",
            "structure_analysis",
            "simulation_report",
        ):
            self.assertIn(term, governance)

    def test_template_separates_assumptions_reasoning_and_counterexamples(self) -> None:
        template = read("templates/research/SYNTHETIC_TESTER_SIMULATION_PACKET.md")

        for term in (
            "simulation_id",
            "validation_method: SYNTHETIC_TESTER_SIMULATION",
            "evidence_tier: T6_AI_INFERENCE",
            "human_validation: NOT_RUN",
            "current_skill_registry",
            "selected_project_skills",
            "selected_base_skills",
            "canonical_sources",
            "protected_paths",
            "persona_id",
            "assumed_first_attempt",
            "reasoning_basis",
            "confidence: LOW | MEDIUM | HIGH",
            "counterexample",
            "adversarial_question",
            "assumption_not_observation: true",
            "claims_not_allowed",
            "PROMISING_DIRECTION | ADAPT | REWORK | REJECT | TEST | STOP",
            "human_followup_status: NOT_RUN",
        ):
            self.assertIn(term, template)

    def test_human_validation_governance_and_knowledge_hub_route_synthetic_method(self) -> None:
        human_governance = read(
            "docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md"
        )
        knowledge_hub = read("docs/knowledge/game-development/README.md")
        synthetic_path = (
            "docs/knowledge/game-development/"
            "SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md"
        )
        synthetic_template = "templates/research/SYNTHETIC_TESTER_SIMULATION_PACKET.md"

        self.assertIn(synthetic_path, human_governance)
        self.assertIn(synthetic_path, knowledge_hub)
        self.assertIn(synthetic_template, knowledge_hub)

    def test_no_duplicate_synthetic_tester_skill_is_added(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")

        self.assertNotIn('"skill_id":"synthetic-tester-simulation"', registry)
        self.assertNotIn('"skill_id":"running-synthetic-testers"', registry)


if __name__ == "__main__":
    unittest.main()
