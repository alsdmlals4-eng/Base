from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "check_skill_system_coverage",
    ROOT / "tools/check_skill_system_coverage.py",
)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


class SkillSystemCoverageTests(unittest.TestCase):
    def test_source_responsibilities_are_mapped_to_active_skills(self) -> None:
        self.assertEqual(checker.validate(), [])

    def test_requested_independent_skills_remain_distinct(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        ids = {item["skill_id"] for item in registry["skills"]}
        required = {
            "refactoring-with-contract-preservation",
            "simplifying-skill-bodies",
            "pruning-stale-and-nonfunctional-material",
            "synchronizing-local-and-github-state",
            "maintaining-long-running-task-continuity",
            "governing-game-user-research-coverage",
            "creating-user-learning-notes",
            "building-project-visual-dashboards",
            "diagnosing-game-engine-runtime-failures",
        }
        self.assertTrue(required.issubset(ids))

    def test_games_user_research_contract_has_exactly_eleven_domains(self) -> None:
        text = (ROOT / "skills/governing-game-user-research-coverage/SKILL.md").read_text(encoding="utf-8")
        numbered = [line for line in text.splitlines() if line[:1].isdigit() and ". " in line]
        self.assertEqual(len(numbered), 11)

    def test_optimization_report_and_machine_coverage_exist(self) -> None:
        self.assertTrue((ROOT / "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md").is_file())
        self.assertTrue((ROOT / "docs/SKILL_COVERAGE_MAP.md").is_file())
        self.assertTrue((ROOT / "skills/SKILL_COVERAGE.json").is_file())


if __name__ == "__main__":
    unittest.main()
