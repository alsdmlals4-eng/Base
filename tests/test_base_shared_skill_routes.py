from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"
FRONT_NAME = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)


class BaseSharedSkillRouteTests(unittest.TestCase):
    def test_shared_skill_routes_are_registered_and_adapter_only(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

        self.assertEqual(registry["registry_role"], "base-shared-skill-extension-router")
        self.assertFalse(registry["routing_policy"]["load_all_skills"])
        self.assertTrue(registry["routing_policy"]["project_adapter_required"])
        self.assertFalse(registry["routing_policy"]["copy_shared_skill_bodies_to_projects"])

        by_id = {item["skill_id"]: item for item in registry["shared_skills"]}
        required = {
            "governing-legacy-retention-and-archives",
            "evaluating-godot-assets-and-plugins-before-creation",
        }
        self.assertEqual(set(by_id), required)

        for skill_id, item in by_id.items():
            self.assertEqual(item["status"], "ACTIVE")
            self.assertFalse(item["load_by_default"])
            self.assertTrue(item["trigger_tags"])
            self.assertTrue(item["use_when"])
            self.assertTrue(item["do_not_use_when"])
            self.assertTrue(item["project_adapter_roles"])

            skill_path = ROOT / item["path"]
            self.assertTrue(skill_path.is_file(), item["path"])
            text = skill_path.read_text(encoding="utf-8")
            match = FRONT_NAME.search(text)
            self.assertIsNotNone(match, skill_id)
            self.assertEqual(match.group(1).strip(), skill_id)

    def test_project_specific_skills_remain_local_only(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        policy = registry["project_skill_policy"]
        self.assertEqual(policy["base_shared_skills"], "route-through-project-adapter")
        self.assertEqual(policy["project_specific_skills"], "create-and-maintain-in-project")
        self.assertEqual(policy["duplicate_base_skill_bodies"], "forbidden")


if __name__ == "__main__":
    unittest.main()
