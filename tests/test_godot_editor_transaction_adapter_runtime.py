from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/godot-live-editor-v2-editor-pilot"
ADDON = ROOT / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"
MATERIALIZER = ROOT / "tools/materialize_godot_editor_adapter_pilot.py"
PILOT_PLUGIN = FIXTURE / "addons/base_live_editor_adapter_pilot/plugin.gd"


def _load_materializer():
    if not MATERIALIZER.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "materialize_godot_editor_adapter_pilot",
        MATERIALIZER,
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GodotEditorTransactionAdapterRuntimeTests(unittest.TestCase):
    maxDiff = None

    def test_pilot_fixture_and_materializer_are_complete(self) -> None:
        for path in (
            FIXTURE / "project.godot",
            FIXTURE / "main.tscn",
            FIXTURE / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json",
            FIXTURE / "addons/base_live_editor_adapter_pilot/plugin.cfg",
            PILOT_PLUGIN,
            FIXTURE / ".gitignore",
            MATERIALIZER,
        ):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")

    def test_pilot_materializer_copies_canonical_addon(self) -> None:
        module = _load_materializer()
        self.assertIsNotNone(module, "missing or unloadable Pilot materializer")
        with tempfile.TemporaryDirectory() as temporary:
            project = module.materialize(ROOT, Path(temporary) / "pilot")
            copied = project / "addons/base_live_editor_adapter"
            self.assertEqual((ADDON / "plugin.gd").read_bytes(), (copied / "plugin.gd").read_bytes())
            self.assertFalse(list(project.rglob("*.uid")))
            manifest = json.loads(
                (project / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual("CONFIGURED", manifest["configuration_state"])
            transport = manifest["transport"]
            self.assertEqual("PROJECT_DEFINED", transport["kind"])
            self.assertTrue(transport["enabled"])
            self.assertIsNone(transport["bind_host"])
            self.assertEqual("in-process-editor-plugin", transport["endpoint_identity"])
            self.assertEqual(
                "CURRENT_USER_ONLY",
                transport["access_control"]["os_access_control"],
            )
            self.assertEqual(
                {"scene.inspect", "node.rename"},
                {item["capability_id"] for item in manifest["capabilities"]},
            )

    def test_runtime_pilot_uses_canonical_request_hashes(self) -> None:
        guard = (ADDON / "runtime_contract_guard.gd").read_text(encoding="utf-8")
        pilot = PILOT_PLUGIN.read_text(encoding="utf-8")
        for marker in (
            "REQUEST_HASH_MISMATCH",
            "operation_request_material",
            "canonical_json_sha256",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, guard)
        self.assertNotIn('"a".repeat(64)', pilot)
        self.assertIn("_guard.operation_request_material", pilot)
        self.assertIn("_guard.canonical_json_sha256", pilot)

    @unittest.skipUnless(
        os.environ.get("GODOT_BIN"),
        "SKIPPED_NOT_CONFIGURED: set GODOT_BIN to exact Godot 4.7.x executable",
    )
    def test_actual_godot_editor_transaction_pilot(self) -> None:
        module = _load_materializer()
        self.assertIsNotNone(module, "missing or unloadable Pilot materializer")
        godot = Path(os.environ["GODOT_BIN"]).resolve()
        self.assertTrue(godot.is_file(), f"missing GODOT_BIN: {godot}")
        version = subprocess.run(
            [str(godot), "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(0, version.returncode, version.stderr)
        self.assertIn("4.7.", version.stdout)
        executable_sha256 = hashlib.sha256(godot.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as temporary:
            project = module.materialize(ROOT, Path(temporary) / "pilot")
            environment = os.environ.copy()
            environment.update(
                {
                    "HOME": str(Path(temporary) / "home"),
                    "TMPDIR": str(Path(temporary) / "tmp"),
                    "TMP": str(Path(temporary) / "tmp"),
                    "TEMP": str(Path(temporary) / "tmp"),
                }
            )
            Path(environment["HOME"]).mkdir(parents=True)
            Path(environment["TMPDIR"]).mkdir(parents=True)
            completed = subprocess.run(
                [
                    str(godot),
                    "--editor",
                    "--headless",
                    "--path",
                    str(project),
                    "--quit-after",
                    "600",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
                env=environment,
            )
            result_path = project / "artifacts/godot-live-editor/editor_transaction_pilot_result.json"
            self.assertEqual(
                0,
                completed.returncode,
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertTrue(
                result_path.is_file(),
                f"missing runtime result\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "PASS",
                result["status"],
                f"result={result}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            for key in (
                "inspect_pass",
                "rename_keep_dirty_pass",
                "undo_pass",
                "rename_save_pass",
            ):
                with self.subTest(key=key):
                    self.assertTrue(result[key])
            self.assertFalse(result["network_listener_enabled"])
            self.assertEqual(["COMPLETED", "COMPLETED"], result["ledger_states"])
            self.assertEqual(
                hashlib.sha256((project / "main.tscn").read_bytes()).hexdigest(),
                result["saved_scene_sha256"],
            )
            self.assertEqual(64, len(executable_sha256))


if __name__ == "__main__":
    unittest.main()
