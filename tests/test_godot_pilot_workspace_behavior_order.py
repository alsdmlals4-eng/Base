from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools/godot_multi_project_pilot.py"
WORKSPACE = ROOT / "tools/godot_project_pilot_workspace.py"


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


if __name__ == "__main__":
    unittest.main()
