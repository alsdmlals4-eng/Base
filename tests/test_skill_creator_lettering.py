"""Routing and progressive-load regressions, not model/art-quality proof."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from tools.skill_context import load_skill_context

ROOT = Path(__file__).resolve().parents[1]
NEW = "designing-game-lettering"
EVOLVE = "evolving-project-discipline-skills"


class SkillCreatorLetteringTests(unittest.TestCase):
    def registry(self):
        data = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        return {entry["skill_id"]: entry for entry in data["skills"]}

    def test_lettering_is_registered_selectively_with_a_real_package(self):
        registry = self.registry()
        self.assertTrue(NEW in registry, "lettering registration missing")
        entry = registry[NEW]
        self.assertFalse(entry["load_by_default"])
        self.assertTrue((ROOT / entry["path"]).is_file())
        self.assertTrue({"lettering", "game-logo", "display-typography"} <= set(entry["trigger_tags"]))
        self.assertNotIn("runtime-ui-audit", entry["trigger_tags"])

    def test_creator_bridge_is_linked_but_not_eagerly_loaded(self):
        path = ROOT / self.registry()[EVOLVE]["path"]
        self.assertEqual(len(load_skill_context(path)), 1)
        self.assertTrue("(references/repeated-work-and-skill-creator.md)" in path.read_text(encoding="utf-8"), "creator reference link missing")
        pack = load_skill_context(path, ["references/repeated-work-and-skill-creator.md"])
        self.assertEqual(len(pack), 2)

    def test_lettering_recipe_is_conditional_and_complete(self):
        path = ROOT / f"skills/{NEW}/SKILL.md"
        self.assertTrue(path.is_file(), "new lettering package is missing")
        self.assertEqual(len(load_skill_context(path)), 1)
        pack = load_skill_context(path, ["references/lettering-production.md"])
        self.assertEqual(len(pack), 2)
        self.assertTrue(all(text.strip() for text in pack.values()))

    def test_repeated_work_and_existing_creator_can_find_evolution(self):
        tags = set(self.registry()[EVOLVE]["trigger_tags"])
        self.assertTrue({"repeated-work", "skill-creator", "reusable-automation"} <= tags)
        self.assertNotIn("skill-creator", self.registry(), "do not duplicate the system skill in Base")

    def test_entrypoints_reach_lettering_and_reuse_owner(self):
        for path in ("START_HERE.md", "docs/DOCUMENTATION_MAP.md"):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertTrue(f"skills/{NEW}/SKILL.md" in text, f"lettering route missing: {path}")
                self.assertTrue(f"skills/{EVOLVE}/SKILL.md" in text, f"evolution route missing: {path}")

    def test_behavior_cases_cover_primary_and_nonselection(self):
        data = json.loads((ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8"))
        self.assertTrue(any(c["expected_primary_skill"] == NEW for c in data["cases"]))
        self.assertTrue(any(NEW in c["forbidden_skills"] for c in data["cases"]))

    def test_implementation_evidence_points_to_executable_test(self):
        data = json.loads((ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json").read_text(encoding="utf-8"))
        entries = {entry["skill_id"]: entry for entry in data["entries"]}
        self.assertTrue(NEW in entries, "lettering evidence missing")
        self.assertIn({"kind": "TEST", "path": "tests/test_skill_creator_lettering.py"}, entries[NEW]["evidence"])


if __name__ == "__main__":
    unittest.main()
