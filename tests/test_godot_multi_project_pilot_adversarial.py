from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import godot_multi_project_pilot as runner
from tools import godot_project_pilot_evidence as evidence
from tools import godot_project_pilot_workspace as workspace
from tools.godot_project_pilot_descriptor import (
    BehaviorCheck,
    ProjectPilotDescriptor,
    load_descriptor,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-project-pilot-v1.schema.json"
GODOT_ARCHIVE_SHA256 = "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"


def _runtime_descriptor() -> dict[str, object]:
    return {
        "schema_version": "1",
        "project_identity": {"repository": "owner/game", "project_id": "game"},
        "base_pilot_commit": "a" * 40,
        "project_state": "EXISTING_GODOT_PROJECT",
        "godot": {
            "version": "4.7.1-stable",
            "archive_sha256": GODOT_ARCHIVE_SHA256,
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


def _descriptor_with_legacy() -> ProjectPilotDescriptor:
    return ProjectPilotDescriptor(
        repository="owner/game",
        project_id="game",
        base_pilot_commit="a" * 40,
        project_state="EXISTING_GODOT_PROJECT",
        godot_version="4.7.1-stable",
        godot_archive_sha256=GODOT_ARCHIVE_SHA256,
        project_file="project.godot",
        main_scene_source="application/run/main_scene",
        legacy_editor_plugins=("res://addons/godot_ai/plugin.cfg",),
        legacy_autoloads=("_mcp_game_helper",),
        scratch_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
        behavior_checks=(),
        expected_platform="PC",
    )


class GodotMultiProjectPilotAdversarialTests(unittest.TestCase):
    def test_descriptor_rejects_shell_and_traversal_surfaces(self) -> None:
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
                        load_descriptor(path, SCHEMA)

    def test_descriptor_rejects_wrong_godot_archive(self) -> None:
        payload = _runtime_descriptor()
        payload["godot"]["archive_sha256"] = "b" * 64
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "descriptor.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "DESCRIPTOR_SCHEMA_INVALID"):
                load_descriptor(path, SCHEMA)

    def test_descriptor_rejects_arbitrary_behavior_commands(self) -> None:
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
                load_descriptor(path, SCHEMA)

    def test_workspace_rejects_overlap_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=source, check=True)
            (source / "project.godot").write_text("config_version=5\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=source, check=True)
            with self.assertRaisesRegex(ValueError, "WORKSPACE_OVERLAP"):
                workspace.copy_to_workspace(source, source / "copy")

            if os.name != "nt":
                outside = root / "outside"
                outside.mkdir()
                (source / "escape").symlink_to(outside, target_is_directory=True)
                subprocess.run(["git", "add", "escape"], cwd=source, check=True)
                with self.assertRaisesRegex(ValueError, "SYMLINK_ESCAPE"):
                    workspace.inventory_tracked_files(source)

    def test_transform_fails_when_declared_legacy_authority_is_missing(self) -> None:
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
                workspace.transform_project_godot(project, _descriptor_with_legacy())

    def test_evidence_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload = {
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
            path = root / "runtime-result.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "EVIDENCE_PATH_ESCAPE"):
                evidence.verify_runtime_evidence(root, path)

    def test_unicode_inventory_hash_matches_final_evidence(self) -> None:
        inventory = {"괴이/기록.txt": "a" * 64}
        with tempfile.TemporaryDirectory() as temporary:
            path = evidence.write_final_evidence(
                Path(temporary),
                repository="owner/game",
                source_commit="a" * 40,
                base_pilot_commit="b" * 40,
                project_state="NOT_CREATED",
                result="NOT_APPLICABLE",
                source_before=inventory,
                source_after=inventory,
                changed_paths=(),
                runtime=None,
                legacy_mutation_authority="NOT_APPLICABLE",
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                workspace.inventory_digest(inventory),
                payload["source_before_sha256"],
            )
            self.assertEqual(
                workspace.inventory_digest(inventory),
                payload["source_after_sha256"],
            )

    def test_runner_uses_closed_argv_and_never_shell(self) -> None:
        check = BehaviorCheck(
            kind="PYTHON_UNITTEST_MODULE",
            target="tests.test_safe",
            timeout_seconds=30,
        )
        self.assertEqual(
            [sys.executable, "-m", "unittest", "tests.test_safe", "-v"],
            runner.argv_for_check(check, Path("/godot")),
        )
        source = (ROOT / "tools/godot_multi_project_pilot.py").read_text(encoding="utf-8")
        self.assertIn("shell=False", source)
        self.assertIn('TemporaryDirectory(prefix="base-c0-process-")', source)
        self.assertNotIn(".godot-live-editor-pilot-home", source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("os.system(", source)
        self.assertNotIn("eval(", source)
        self.assertNotIn("exec(", source)

    def test_process_timeout_is_bounded_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            record = runner._run_process(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                cwd=Path(temporary),
                timeout_seconds=1,
            )
            self.assertEqual(124, record.returncode)
            self.assertIn("PROCESS_TIMEOUT", record.stderr_excerpt)

    def test_behavior_process_does_not_leave_home_in_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests = root / "tests"
            tests.mkdir()
            (tests / "__init__.py").write_text("", encoding="utf-8")
            (tests / "test_safe.py").write_text(
                "import unittest\n"
                "class SafeTest(unittest.TestCase):\n"
                "    def test_ok(self):\n"
                "        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            record = runner.run_behavior_check(
                BehaviorCheck(
                    kind="PYTHON_UNITTEST_MODULE",
                    target="tests.test_safe",
                    timeout_seconds=30,
                ),
                root,
                Path("/godot"),
            )
            self.assertEqual(0, record.returncode, record.stderr_excerpt)
            self.assertFalse((root / ".godot-live-editor-pilot-home").exists())

    def test_not_created_path_never_starts_godot(self) -> None:
        static = json.loads(
            (
                ROOT
                / "templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json"
            ).read_text(encoding="utf-8")
        )
        static["base_pilot_commit"] = "a" * 40
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "descriptor.json"
            path.write_text(json.dumps(static), encoding="utf-8")
            descriptor = load_descriptor(path, SCHEMA)
            self.assertFalse(descriptor.is_runtime_project)
            self.assertEqual([], runner.processes_for_descriptor(descriptor, Path("/godot")))


if __name__ == "__main__":
    unittest.main()
