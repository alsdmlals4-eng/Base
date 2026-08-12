from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json"


class ProjectFigmaWorkspaceRegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_is_pointer_only_and_explicitly_authorized(self):
        self.assertEqual(self.data["authority"], "POINTER_ONLY_NOT_CANON")
        self.assertEqual(self.data["authorization"]["source"], "explicit_user_instruction")
        forbidden = set(self.data["security_boundary"]["forbidden"])
        self.assertIn("access_token", forbidden)
        self.assertIn("private_credentials", forbidden)
        self.assertIn("project_canon_content", forbidden)

    def test_projects_have_unique_ids_and_file_keys(self):
        projects = self.data["projects"]
        self.assertGreater(len(projects), 0)
        ids = [item["project_id"] for item in projects]
        keys = [item["figma_file_key"] for item in projects]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(keys), len(set(keys)))

    def test_each_pointer_is_a_figma_design_url_for_its_file_key(self):
        for item in self.data["projects"]:
            self.assertIn(item["figma_file_key"], item["figma_url"])
            self.assertTrue(item["figma_url"].startswith("https://www.figma.com/design/"))
            self.assertNotIn("access_token", item)
            self.assertNotIn("token", item)

    def test_standard_visual_bible_structure_is_registered(self):
        self.assertEqual(
            self.data["standard_visual_bible_pages"],
            [
                "00_DIRECTION",
                "01_APPROVED_REFERENCE",
                "02_WIP",
                "03_REJECTED",
                "04_FINAL",
            ],
        )
        for section in (
            "00.8_VISUAL_FLOW_HUB",
            "02.5_FLOW_PROTOTYPE",
            "02.6_GPT_INTERPRETATION",
            "04.2_IMPLEMENTATION_COMPARE",
        ):
            self.assertIn(section, self.data["standard_optional_sections"])


if __name__ == "__main__":
    unittest.main()
