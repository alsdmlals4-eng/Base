from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/BASE_SHARED_SKILL_PROJECT_ROUTING_POLICY.md"
ROUTES = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"


class BaseSharedSkillProjectRoutingPolicyTests(unittest.TestCase):
    def test_policy_defines_main_and_extension_routes(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "Base 메인 Registry route",
            "전문 extension route",
            '"source_registry": "skills/SKILL_REGISTRY.json"',
            '"adapter": "skills/PROJECT_BASE_ADAPTER.json"',
            "HISTORY_ONLY",
            '"copy_skill_bodies_to_project": false',
            "전체 운영체계 채택 기준",
            "공용 Skill route 기준",
        ):
            self.assertIn(required, text)

    def test_extension_registry_keeps_common_skills_in_base(self) -> None:
        registry = json.loads(ROUTES.read_text(encoding="utf-8"))
        policy = registry["project_skill_policy"]
        self.assertEqual(policy["base_shared_skills"], "route-through-project-adapter")
        self.assertEqual(policy["project_specific_skills"], "create-and-maintain-in-project")
        self.assertEqual(policy["duplicate_base_skill_bodies"], "forbidden")

        by_id = {item["skill_id"]: item for item in registry["shared_skills"]}
        self.assertEqual(
            set(by_id),
            {
                "governing-legacy-retention-and-archives",
                "evaluating-godot-assets-and-plugins-before-creation",
            },
        )
        for item in by_id.values():
            self.assertFalse(item["load_by_default"])
            self.assertTrue(item["project_adapter_roles"])


if __name__ == "__main__":
    unittest.main()
