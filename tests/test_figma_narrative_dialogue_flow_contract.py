from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md"


class FigmaNarrativeDialogueFlowContractTests(unittest.TestCase):
    def test_profile_models_editable_scene_dialogue_and_choice_identity(self):
        text = PROFILE.read_text(encoding="utf-8")

        for token in (
            "SCENE_GROUP",
            "DIALOGUE_BEAT",
            "DIALOGUE_LINE",
            "CHOICE",
            "scene_id",
            "beat_id",
            "dialogue_id",
            "choice_id",
            "STAY_IN_SCENE",
            "MOVE_SCENE",
            "END",
        ):
            self.assertIn(token, text)

        self.assertIn("array index", text)
        self.assertIn("runtime proof", text)
        self.assertIn("Figma", text)

    def test_same_scene_branch_preserves_background_continuity(self):
        text = PROFILE.read_text(encoding="utf-8")

        self.assertIn("same `scene_id`", text)
        self.assertIn("background_ref", text)
        self.assertIn("STAY_IN_SCENE", text)
        self.assertIn("MOVE_SCENE", text)
        self.assertIn("Scene section boundary", text)

    def test_edit_mode_has_independent_selection_targets(self):
        text = PROFILE.read_text(encoding="utf-8")

        for heading in (
            "### Scene selection",
            "### Beat selection",
            "### Dialogue Line selection",
            "### Choice selection",
        ):
            self.assertIn(heading, text)

        self.assertIn("individually selectable", text)
        self.assertIn("dialogue_id", text)
        self.assertIn("transition_kind", text)

    def test_profile_keeps_visual_authority_bounded_and_avoids_duplicate_graph_canon(self):
        text = PROFILE.read_text(encoding="utf-8")

        for token in (
            "VISUAL_WORKSPACE",
            "DRAFT_VISUAL",
            "IMPLEMENTATION_PINNED",
            "canonical",
            "derived",
            "single relationship model",
            "Godot",
        ):
            self.assertIn(token, text)

        self.assertIn("Do not maintain", text)
        self.assertIn("prototype", text.lower())


if __name__ == "__main__":
    unittest.main()
