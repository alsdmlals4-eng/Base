from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-project-pilot-v1.schema.json"


def _load(relative: str):
    path = ROOT / relative
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime_descriptor() -> dict[str, object]:
    return {
        "schema_version": "1",
        "project_identity": {
            "repository": "owner/game",
            "project_id": "game",
        },
        "base_pilot_commit": "a" * 40,
        "project_state": "EXISTING_GODOT_PROJECT",
        "godot": {
            "version": "4.7.1-stable",
            "archive_sha256": "b" * 64,
        },
        "project_file": "project.godot",
        "main_scene_source": "application/run/main_scene",
        "legacy_editor_plugins": [],
        "legacy_autoloads": [],
        "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
        "source_mutation_policy": "FORBIDDEN",
        "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
        "behavior_checks": [],
        "expected_platform": "PC",
    }


class GodotMultiProjectPilotAdversarialTests(unittest.TestCase):
    def test_descriptor_rejects_shell_and_traversal_surfaces(self) -> None:
        module = _load("tools/godot_project_pilot_descriptor.py")
        self.assertIsNotNone(module)
        attacks = (
            ("command", "rm -rf /"),
            ("shell", True),
            ("project_file", "../project.godot"),
            ("scratch_scene_path", "res://../escape.tscn"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "descriptor.json"
            for key, value in attacks:
                with self.subTest(key=key):
                    payload = _runtime_descriptor()
                    payload[key] = value
                    path.write_text(json.dumps(payload), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "DESCRIPTOR_SCHEMA_INVALID"):
                        module.load_descriptor(path, SCHEMA)

    def test_descriptor_rejects_arbitrary_behavior_commands(self) -> None:
        module = _load("tools/godot_project_pilot_descriptor.py")
        self.assertIsNotNone(module)
        payload = _runtime_descriptor()
        payload["behavior_checks"] = [
            {
                "kind": "GODOT_SCRIPT",
                "target": "res://tests/run.gd; touch /tmp/pwned",
                "timeout_seconds": 30,
            }
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "descriptor.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "DESCRIPTOR_SCHEMA_INVALID"):
                module.load_descriptor(path, SCHEMA)

    def test_workspace_rejects_overlap_and_symlink_escape(self) -> None:
        module = _load("tools/godot_project_pilot_workspace.py")
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=source, check=True)
            (source / "project.godot").write_text("config_version=5\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=source, check=True)
            with self.assertRaisesRegex(ValueError, "WORKSPACE_OVERLAP"):
                module.copy_to_workspace(source, source / "copy")
            if os.name != "nt":
                outside = root / "outside"
                outside.mkdir()
                (source / "escape").symlink_to(outside, target_is_directory=True)
                subprocess.run(["git", "add", "escape"], cwd=source, check=True)
                with self.assertRaisesRegex(ValueError, "SYMLINK_ESCAPE"):
                    module.inventory_tracked_files(source)

    def test_transform_fails_when_declared_legacy_authority_is_missing(self) -> None:
        descriptor_module = _load("tools/godot_project_pilot_descriptor.py")
        workspace_module = _load("tools/godot_project_pilot_workspace.py")
        self.assertIsNotNone(descriptor_module)
        self.assertIsNotNone(workspace_module)
        descriptor = descriptor_module.ProjectPilotDescriptor(
            repository="owner/game",
            project_id="game",
            base_pilot_commit="a" * 40,
            project_state="EXISTING_GODOT_PROJECT",
            godot_version="4.7.1-stable",
            godot_archive_sha256="b" * 64,
            project_file="project.godot",
            main_scene_source="application/run/main_scene",
            legacy_editor_plugins=("res://addons/godot_ai/plugin.cfg",),
            legacy_autoloads=("_mcp_game_helper",),
            scratch_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
            behavior_checks=(),
            expected_platform="PC",
        )
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project.godot"
            project.write_text(
                'config_version=5\n[application]\nrun/main_scene="res://main.tscn"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError,
                "DECLARED_LEGACY_PLUGIN_NOT_FOUND|DECLARED_LEGACY_AUTOLOAD_NOT_FOUND",
            ):
                workspace_module.transform_project_godot(project, descriptor)

    def test_evidence_rejects_path_escape_and_identity_mismatch(self) -> None:
        module = _load("tools/godot_project_pilot_evidence.py")
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            outside = workspace.parent / "outside.tscn"
            outside.write_text("outside", encoding="utf-8")
            result = {
                "status": "PASS",
                "repository": "wrong/repo",
                "source_commit": "a" * 40,
                "base_pilot_commit": "b" * 40,
                "saved_scene_path": "../outside.tscn",
                "saved_scene_sha256": "0" * 64,
                "ledger_states": ["COMPLETED", "COMPLETED"],
                "main_scene_inspect": "PASS",
                "scratch_scene_rename": "PASS",
                "editor_undo": "PASS",
                "scratch_scene_save": "PASS",
                "base_network_listener": False,
            }
            path = workspace / "runtime-result.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "EVIDENCE_PATH_ESCAPE"):
                module.verify_runtime_evidence(workspace, path)

    def test_runner_uses_closed_argv_and_never_shell(self) -> None:
        module = _load("tools/godot_multi_project_pilot.py")
        descriptor_module = _load("tools/godot_project_pilot_descriptor.py")
        self.assertIsNotNone(module)
        self.assertIsNotNone(descriptor_module)
        check = descriptor_module.BehaviorCheck(
            kind="PYTHON_UNITTEST_MODULE",
            target="tests.test_safe",
            timeout_seconds=30,
        )
        argv = module.argv_for_check(check, Path("/godot"))
        self.assertEqual(
            [module.sys.executable, "-m", "unittest", "tests.test_safe", "-v"],
            argv,
        )
        source = (ROOT / "tools/godot_multi_project_pilot.py").read_text(encoding="utf-8")
        self.assertIn("shell=False", source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("os.system(", source)
        self.assertNotIn("eval(", source)
        self.assertNotIn("exec(", source)

    def test_not_created_path_never_starts_godot(self) -> None:
        runner = _load("tools/godot_multi_project_pilot.py")
        descriptor_module = _load("tools/godot_project_pilot_descriptor.py")
        self.assertIsNotNone(runner)
        self.assertIsNotNone(descriptor_module)
        static = json.loads(
            (
                ROOT
                / "templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json"
            ).read_text(encoding="utf-8")
        )
        static["base_pilot_commit"] = "a" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            descriptor_path = root / "descriptor.json"
            descriptor_path.write_text(json.dumps(static), encoding="utf-8")
            descriptor = descriptor_module.load_descriptor(descriptor_path, SCHEMA)
            self.assertFalse(descriptor.is_runtime_project)
            self.assertEqual([], runner.processes_for_descriptor(descriptor, Path("/godot")))


if __name__ == "__main__":
    unittest.main()
