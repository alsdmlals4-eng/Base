from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
README = ROOT / "skills" / "README.md"
GUIDE = ROOT / "docs" / "knowledge" / "ai" / "SKILL_ROUTING_PRECISION_GUIDE.md"


class SkillRoutingPrecisionPolicyTests(unittest.TestCase):
    def test_registry_keeps_sparse_hard_boundaries(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        policy = registry["routing_policy"]
        self.assertFalse(policy["load_all_skills"])
        self.assertTrue(policy["require_trigger_match"])
        self.assertEqual(1, policy["max_primary_discipline_skills"])
        self.assertLessEqual(policy["max_foundation_skills"], 3)

    def test_operational_policy_uses_a_smaller_default_shortlist_than_the_hard_ceiling(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        for contract in (
            "DEFAULT_SUPPORTING_SKILL_BUDGET: 1",
            "SECOND_SUPPORTING_SKILL: EXCEPTION_ONLY",
            "FULL_SKILL_BODY_TIE_BREAK: REQUIRED",
            "DO_NOT_FILL_BUDGET: REQUIRED",
            "FUNCTIONAL_OVERLAP: REUSE_ABSORB_MERGE_FIRST",
        ):
            self.assertIn(contract, guide)

    def test_skill_router_readme_exposes_precision_guide(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn("SKILL_ROUTING_PRECISION_GUIDE.md", readme)
        self.assertIn("기본 supporting Skill budget은 1", readme)
        self.assertIn("Skill 본문", readme)


if __name__ == "__main__":
    unittest.main()
