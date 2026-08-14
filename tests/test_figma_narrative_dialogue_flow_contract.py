from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md"
GODOT_ROOT = ROOT / "examples/godot-narrative-dialogue-flow"
MAKE_ROOT = ROOT / "examples/figma-make-narrative-dialogue-flow"
EVIDENCE = ROOT / "docs/knowledge/godot/evidence/2026-08-14-narrative-dialogue-runtime-sample.md"


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

        self.assertIn("같은 `scene_id`", text)
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

    def test_base_reference_has_make_edit_mode_and_godot_runtime(self):
        required = (
            MAKE_ROOT / "package.json",
            MAKE_ROOT / "src/App.tsx",
            MAKE_ROOT / "src/sample_dialogue.json",
            GODOT_ROOT / "project.godot",
            GODOT_ROOT / "main.tscn",
            GODOT_ROOT / "src/dialogue_flow_model.gd",
            GODOT_ROOT / "src/dialogue_flow_session.gd",
            GODOT_ROOT / "tests/test_dialogue_flow_runtime.gd",
            EVIDENCE,
        )
        for path in required:
            self.assertTrue(path.is_file(), path.as_posix())

        make_text = (MAKE_ROOT / "src/App.tsx").read_text(encoding="utf-8")
        for token in (
            "Preview",
            "Edit",
            "SCENE INSPECTOR",
            "BEAT INSPECTOR",
            "DIALOGUE INSPECTOR",
            "CHOICE INSPECTOR",
            "DERIVED FLOW MAP",
            "STAY_IN_SCENE",
            "MOVE_SCENE",
            "dialogue_id",
            "choice_id",
        ):
            self.assertIn(token, make_text)
        self.assertNotIn("MNODES", make_text)
        self.assertNotIn("MEDGES", make_text)

    def test_make_and_godot_reference_use_identical_sample_fixture(self):
        make_fixture = (MAKE_ROOT / "src/sample_dialogue.json").read_bytes()
        godot_fixture = (GODOT_ROOT / "data/sample_dialogue.json").read_bytes()
        self.assertEqual(make_fixture, godot_fixture)

    def test_evidence_keeps_implementation_reality_gate_bounded(self):
        text = EVIDENCE.read_text(encoding="utf-8")
        for token in (
            "NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS",
            "NARRATIVE_DIALOGUE_SAMPLE_READY",
            "RUNTIME_PASS",
            "supplied_figma_make_url_mutation: BLOCKED_TOOL_SURFACE",
            "higodot_project_authoring: NOT_RUN",
            "real_project_adoption: NOT_RUN",
            "production_ready: NO",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
