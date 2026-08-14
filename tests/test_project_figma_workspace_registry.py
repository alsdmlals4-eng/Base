from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json"
TARGET_REGISTRY_PATH = ROOT / "docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json"


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
        self.assertEqual(len(projects), 8)
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

    def test_target_registry_binds_each_project_to_the_reviewed_github_repository(self):
        entries = json.loads(TARGET_REGISTRY_PATH.read_text(encoding="utf-8"))["entries"]
        expected = {
            "coc-fiction": "https://github.com/alsdmlals4-eng/Coc-Fiction.git",
            "ten-paces-hidden-moves": "https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves.git",
            "ninja-survival": "https://github.com/alsdmlals4-eng/ninja-survival-godot.git",
            "switchy-express-cargo-puzzle": "https://github.com/alsdmlals4-eng/Switchy-Express-Cargo-Puzzle.git",
            "urban-legend": "https://github.com/alsdmlals4-eng/urban-legend.git",
            "grimoire-how-to-rewrite-the-world": "https://github.com/alsdmlals4-eng/GRIMOIRE-.git",
            "blacksmith": "https://github.com/alsdmlals4-eng/Blacksmith.git",
            "omenward": "https://github.com/alsdmlals4-eng/omenward.git",
        }
        self.assertEqual(
            {entry["project_id"]: entry["repository_url"] for entry in entries},
            expected,
        )

    def test_professional_single_file_profiles_preserve_visual_lifecycle(self):
        profiles = self.data["workspace_profiles"]
        game = profiles["PROFESSIONAL_SINGLE_FILE_GAME"]
        fiction = profiles["PROFESSIONAL_SINGLE_FILE_FICTION"]

        self.assertEqual(
            game["pages"],
            [
                "00_START_HERE",
                "01_DIRECTION",
                "02_APPROVED_REFERENCE",
                "10_ART_SOURCE",
                "11_ART_WORKBENCH",
                "12_ART_LIBRARY",
                "13_EXPORT_READY",
                "20_UI_FOUNDATIONS",
                "21_UI_COMPONENTS",
                "22_UI_SCREENS",
                "23_UI_FLOWS",
                "24_PROTOTYPES",
                "30_GPT_INTERPRETATION",
                "31_REVIEW",
                "32_REJECTED",
                "40_IMPLEMENTATION_COMPARE",
                "90_DEV_HANDOFF",
                "99_ARCHIVE",
            ],
        )
        for token in (
            "02_APPROVED_REFERENCE",
            "30_GPT_INTERPRETATION",
            "31_REVIEW",
            "32_REJECTED",
            "40_IMPLEMENTATION_COMPARE",
            "90_DEV_HANDOFF",
            "99_ARCHIVE",
        ):
            self.assertIn(token, game["pages"])

        self.assertEqual(len(fiction["pages"]), 14)
        for token in (
            "30_AI_WORKBENCH",
            "31_GPT_INTERPRETATION",
            "32_REVIEW",
            "33_REJECTED",
            "90_HANDOFF",
            "99_ARCHIVE",
        ):
            self.assertIn(token, fiction["pages"])

    def test_live_setup_is_recorded_as_verified_and_duplicate_free(self):
        self.assertEqual(self.data["figma_setup_run"]["status"], "STANDARDIZED_PRO_FULL")
        for item in self.data["projects"]:
            self.assertEqual(item["access_status"], "READ_WRITE_CONFIRMED")
            self.assertEqual(item["visual_bible_setup_status"], "STANDARDIZED")
            self.assertEqual(item["duplicate_page_name_count"], 0)
            if item["workspace_profile"] == "PROFESSIONAL_SINGLE_FILE_FICTION":
                self.assertEqual(item["page_count"], 14)
            else:
                self.assertEqual(item["workspace_profile"], "PROFESSIONAL_SINGLE_FILE_GAME")
                self.assertEqual(item["page_count"], 18)


if __name__ == "__main__":
    unittest.main()
