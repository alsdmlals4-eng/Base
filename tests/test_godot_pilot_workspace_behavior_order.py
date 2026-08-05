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

    def test_legacy_is_removed_before_import_and_base_activation_is_later(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        prepare = text.index("prepared = prepare_runtime_workspace(")
        import_marker = text.index("GODOT_PROJECT_IMPORT_FAILED")
        behavior = text.index("run_behavior_check(check, workspace, godot_bin)")
        materialize = text.index("materialized = materialize_runtime_workspace(")
        pilot = text.index("GODOT_PROJECT_PILOT_FAILED")
        self.assertLess(prepare, import_marker)
        self.assertLess(import_marker, behavior)
        self.assertLess(behavior, materialize)
        self.assertLess(materialize, pilot)
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

    def test_workspace_module_splits_prepare_from_base_activation(self) -> None:
        text = WORKSPACE.read_text(encoding="utf-8")
        self.assertIn("def prepare_runtime_workspace(", text)
        self.assertIn("transform_report: ProjectTransformReport | None = None", text)
        self.assertIn("report = transform_report or prepare_runtime_workspace(", text)
        prepare_body = text[
            text.index("def prepare_runtime_workspace(") :
            text.index("def materialize_runtime_workspace(")
        ]
        self.assertNotIn("copy_canonical_addon", prepare_body)
        self.assertNotIn("_activate_pilot_plugin", prepare_body)

    def test_behavior_failure_records_workspace_legacy_state(self) -> None:
        text = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn('legacy_mutation_authority="NOT_RUN"', text)
        self.assertIn("legacy_mutation_authority=legacy_state", text)
        self.assertIn("preserved_autoloads=preserved_autoloads", text)


if __name__ == "__main__":
    unittest.main()
