from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools/godot_multi_project_pilot.py"
WORKSPACE = ROOT / "tools/godot_project_pilot_workspace.py"
PILOT = ROOT / "templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd"


class GodotPilotWorkspaceBehaviorOrderTests(unittest.TestCase):
    def test_runtime_behavior_checks_never_execute_in_source_checkout(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("run_behavior_check(check, source, godot_bin)", text)
        self.assertIn("run_behavior_check(check, workspace, godot_bin)", text)

    def test_plugin_files_are_staged_before_import_but_activated_after_behavior(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        prepare = text.index("prepared = prepare_runtime_workspace(")
        stage = text.index("staged = stage_runtime_workspace(")
        import_marker = text.index("GODOT_PROJECT_IMPORT_FAILED")
        behavior = text.index("run_behavior_check(check, workspace, godot_bin)")
        activate = text.index("materialized = activate_staged_runtime_workspace(")
        pilot = text.index("GODOT_PROJECT_PILOT_FAILED")
        self.assertLess(prepare, stage)
        self.assertLess(stage, import_marker)
        self.assertLess(import_marker, behavior)
        self.assertLess(behavior, activate)
        self.assertLess(activate, pilot)
        self.assertIn("transform_report=prepared", text)

    def test_import_is_bounded_editor_parse_in_disposable_workspace(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        for marker in (
            '"--editor"',
            '"--headless"',
            '"--path"',
            "str(workspace)",
            '"--quit"',
            "timeout_seconds=180",
        ):
            self.assertIn(marker, text)

    def test_workspace_module_separates_staging_from_activation(self) -> None:
        text = WORKSPACE.read_text(encoding="utf-8")
        self.assertIn("def prepare_runtime_workspace(", text)
        self.assertIn("def stage_runtime_workspace(", text)
        self.assertIn("def activate_staged_runtime_workspace(", text)
        self.assertIn("transform_report: ProjectTransformReport | None = None", text)

        prepare_body = text[
            text.index("def prepare_runtime_workspace(") :
            text.index("def stage_runtime_workspace(")
        ]
        stage_body = text[
            text.index("def stage_runtime_workspace(") :
            text.index("def activate_staged_runtime_workspace(")
        ]
        activate_body = text[
            text.index("def activate_staged_runtime_workspace(") :
            text.index("def materialize_runtime_workspace(")
        ]
        self.assertNotIn("copy_canonical_addon", prepare_body)
        self.assertIn("copy_canonical_addon", stage_body)
        self.assertNotIn("_activate_pilot_plugin", stage_body)
        self.assertNotIn("build_configured_manifest", stage_body)
        self.assertIn("_activate_pilot_plugin", activate_body)
        self.assertIn("build_configured_manifest", activate_body)

    def test_behavior_failure_records_workspace_legacy_state(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn('legacy_mutation_authority="NOT_RUN"', text)
        self.assertIn("legacy_mutation_authority=legacy_state", text)
        self.assertIn("preserved_autoloads=preserved_autoloads", text)

    def test_pilot_failure_code_is_bound_to_first_failed_operation(self) -> None:
        text = PILOT.read_text(encoding="utf-8")
        self.assertIn("func _first_failure_code(", text)
        for marker in (
            'return str(inspect_result.get("code", "MAIN_SCENE_INSPECT_FAILED"))',
            'return str(dirty_result.get("code", "SCRATCH_RENAME_DIRTY_FAILED"))',
            'return "EDITOR_UNDO_FAILED"',
            'return str(save_result.get("code", "SCRATCH_RENAME_SAVE_FAILED"))',
            '"code": "PASS" if passed else _first_failure_code(',
        ):
            self.assertIn(marker, text)

    def test_pilot_waits_for_stable_scene_identity_before_operations(self) -> None:
        text = PILOT.read_text(encoding="utf-8")
        for marker in (
            "const REQUIRED_STABLE_SCENE_FRAMES := 3",
            "func _wait_for_stable_scene(",
            "main_wait = await _wait_for_stable_scene(main_scene, NodePath(\".\"))",
            "scratch_wait = await _wait_for_stable_scene(scratch_scene, NodePath(\"Target\"))",
            "stable_frames += 1",
            "if stable_frames >= REQUIRED_STABLE_SCENE_FRAMES:",
        ):
            self.assertIn(marker, text)
        self.assertNotIn(
            'EditorInterface.open_scene_from_path(scratch_scene)\n    await get_tree().process_frame\n    await get_tree().process_frame',
            text,
        )

    def test_scene_wait_failure_codes_distinguish_editor_states(self) -> None:
        text = PILOT.read_text(encoding="utf-8")
        for marker in (
            "var open_scenes := EditorInterface.get_open_scenes()",
            'last_code = "SCENE_NOT_OPEN"',
            'last_code = "NO_EDITED_SCENE"',
            'last_code = "EDITED_SCENE_PATH_EMPTY"',
            'last_code = "EDITED_SCENE_NOT_ACTIVE"',
            'last_code = "TARGET_NODE_NOT_FOUND"',
            'return {"root": root, "code": "PASS"}',
            'return {"root": null, "code": last_code}',
            '"code": main_wait.get("code", "MAIN_SCENE_OPEN_FAILED")',
            '"code": scratch_wait.get("code", "SCRATCH_SCENE_OPEN_FAILED")',
        ):
            self.assertIn(marker, text)

    def test_main_scene_is_closed_before_scratch_scene_is_opened(self) -> None:
        text = PILOT.read_text(encoding="utf-8")
        for marker in (
            "var close_main_result := EditorInterface.close_scene()",
            "if close_main_result != OK:",
            '"code": "MAIN_SCENE_CLOSE_FAILED"',
            "var main_close_wait = await _wait_for_scene_closed(main_scene)",
            "func _wait_for_scene_closed(",
            "if scene_path not in EditorInterface.get_open_scenes():",
            'return {"closed": true, "code": "PASS"}',
            'return {"closed": false, "code": "SCENE_CLOSE_TIMEOUT"}',
        ):
            self.assertIn(marker, text)

        close_call = text.index("var close_main_result := EditorInterface.close_scene()")
        close_wait = text.index("var main_close_wait = await _wait_for_scene_closed(main_scene)")
        scratch_open = text.index("EditorInterface.open_scene_from_path(scratch_scene)")
        self.assertLess(close_call, close_wait)
        self.assertLess(close_wait, scratch_open)
        self.assertNotIn("EditorInterface.edit_node(", text)
        self.assertNotIn("func _find_open_scene_root(", text)


if __name__ == "__main__":
    unittest.main()
