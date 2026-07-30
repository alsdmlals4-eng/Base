from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BaseV91SkillPressureContractTests(unittest.TestCase):
    def test_baseline_pressure_scenarios_record_failures_before_guidance(self) -> None:
        evidence = (ROOT / "docs/operations/BASE_V9_1_SKILL_PRESSURE_TESTS.md").read_text(encoding="utf-8")
        for scenario in (
            "BODY-COPY",
            "STALE-PIN-EXECUTION",
            "LOCAL-SHARED-PRECEDENCE",
            "MISMATCH-IGNORE",
        ):
            self.assertIn(scenario, evidence)
        self.assertGreaterEqual(evidence.count("BASELINE_FAIL"), 4)
        self.assertGreaterEqual(evidence.count("GUIDED_PASS"), 4)
        self.assertIn("deadline", evidence)
        self.assertIn("sunk cost", evidence)
        self.assertIn("authority pressure", evidence)

    def test_operating_skill_routes_to_focused_adapter_reference(self) -> None:
        skill = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        reference = (
            ROOT
            / "skills/managing-game-project-operating-system/references/project-adapter-and-routing-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("project-adapter-and-routing-contract.md", skill)
        for required in (
            "Do not copy a Base shared Skill body",
            "Refuse execution",
            "PROJECT_LOCAL_THEN_BASE_SHARED",
            "mismatched pin",
            "PROJECT_BASE_ADAPTER.json",
            "PROJECT_SKILL_SNAPSHOT.json",
        ):
            self.assertIn(required, reference)

    def test_review_skill_requires_fail_closed_operating_integrity(self) -> None:
        skill = (ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md").read_text(encoding="utf-8")
        for required in (
            "PROJECT_OPERATING_INTEGRITY",
            "stale pin",
            "generated-view drift",
            "protected-path",
            "NOT_RUN",
        ):
            self.assertIn(required, skill)


if __name__ == "__main__":
    unittest.main()
