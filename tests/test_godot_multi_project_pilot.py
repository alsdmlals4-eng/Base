from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools import godot_editor_adapter_materialization as materialization
from tools import godot_project_pilot_evidence as evidence
from tools import godot_project_pilot_workspace as workspace
from tools.godot_project_pilot_descriptor import (
    ProjectPilotDescriptor,
    load_descriptor,
)
from tools import materialize_godot_editor_adapter_pilot as existing_materializer


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-project-pilot-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json"
WORKFLOW = ROOT / ".github/workflows/reusable-godot-project-pilot.yml"
GUIDE = ROOT / "docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md"
GODOT_ARCHIVE_SHA256 = "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"

REQUIRED_PATHS = (
    SCHEMA,
    TEMPLATE,
    WORKFLOW,
    GUIDE,
    ROOT / "tools/godot_editor_adapter_materialization.py",
    ROOT / "tools/godot_project_pilot_descriptor.py",
    ROOT / "tools/godot_project_pilot_workspace.py",
    ROOT / "tools/godot_project_pilot_evidence.py",
    ROOT / "tools/godot_multi_project_pilot.py",
    ROOT / "templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd",
    ROOT / "templates/project-operations/godot-live-editor/pilot/scratch.tscn",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_closed(test: unittest.TestCase, node: object) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            test.assertFalse(node.get("additionalProperties", True), node)
        for value in node.values():
            _assert_closed(test, value)
    elif isinstance(node, list):
        for value in node:
            _assert_closed(test, value)


class GodotMultiProjectPilotTests(unittest.TestCase):
    maxDiff = None

    def test_required_c0_artifacts_exist(self) -> None:
        for path in REQUIRED_PATHS:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")

    def test_transaction_hardening_prerequisite_is_present(self) -> None:
        addon = ROOT / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"
        ledger = (addon / "operation_ledger.gd").read_text(encoding="utf-8")
        guard = (addon / "runtime_contract_guard.gd").read_text(encoding="utf-8")
        registry = (addon / "capability_registry.gd").read_text(encoding="utf-8")

        self.assertNotIn("DirAccess.remove_absolute(target)", ledger)
        for marker in (
            "APPROVAL_EXPIRED",
            "APPROVAL_BINDING_MISMATCH",
            "request_hash",
            "expires_at",
        ):
            self.assertIn(marker, guard)
        for marker in (
            "saved_scene_sha256",
            "SAVE_CURRENT_SCENE",
            "KEEP_DIRTY",
            "typeof(",
            "OUTPUT_SCHEMA_INVALID",
        ):
            self.assertIn(marker, registry)

    def test_descriptor_schema_is_closed_and_template_is_non_authorizing(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        _assert_closed(self, schema)
        self.assertEqual(
            "^[0-9a-f]{40}$",
            schema["properties"]["base_pilot_commit"]["pattern"],
        )
        self.assertEqual(
            GODOT_ARCHIVE_SHA256,
            schema["properties"]["godot"]["properties"]["archive_sha256"]["const"],
        )
        serialized = json.dumps(schema)
        self.assertNotIn('"command"', serialized)
        self.assertNotIn('"shell"', serialized)

        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual("NOT_CREATED", template["project_state"])
        self.assertEqual("0" * 40, template["base_pilot_commit"])
        self.assertEqual(GODOT_ARCHIVE_SHA256, template["godot"]["archive_sha256"])
        self.assertIsNone(template["project_file"])
        self.assertEqual([], template["behavior_checks"])

    def test_descriptor_loader_accepts_runtime_and_static_descriptors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "descriptor.json"
            runtime = {
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
                "behavior_checks": [
                    {
                        "kind": "GODOT_SCRIPT",
                        "target": "res://tests/run_tests.gd",
                        "timeout_seconds": 30,
                    }
                ],
                "expected_platform": "PC",
            }
            path.write_text(json.dumps(runtime), encoding="utf-8")
            self.assertTrue(load_descriptor(path, SCHEMA).is_runtime_project)

            static = json.loads(TEMPLATE.read_text(encoding="utf-8"))
            static["base_pilot_commit"] = "c" * 40
            path.write_text(json.dumps(static), encoding="utf-8")
            self.assertFalse(load_descriptor(path, SCHEMA).is_runtime_project)

    def test_shared_materializer_preserves_existing_pilot_contract(self) -> None:
        capabilities = materialization.build_capabilities()
        self.assertEqual(
            {"scene.inspect", "node.rename"},
            {item["capability_id"] for item in capabilities},
        )
        with tempfile.TemporaryDirectory() as temporary:
            project = existing_materializer.materialize(ROOT, Path(temporary) / "pilot")
            manifest = json.loads(
                (project / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(capabilities, manifest["capabilities"])

    def test_tracked_inventory_detects_source_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "project.godot").write_text("[application]\n", encoding="utf-8")
            (root / "main.tscn").write_text("[gd_scene format=3]\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            before = workspace.inventory_tracked_files(root)
            (root / "main.tscn").write_text(
                "[gd_scene format=3]\n[node]\n", encoding="utf-8"
            )
            after = workspace.inventory_tracked_files(root)
            self.assertEqual(("main.tscn",), workspace.compare_inventories(before, after))
            self.assertNotEqual(
                workspace.inventory_digest(before), workspace.inventory_digest(after)
            )

    def test_project_transform_removes_only_declared_legacy_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project.godot"
            project.write_text(
                'config_version=5\n\n[application]\nrun/main_scene="res://main.tscn"\n\n'
                '[autoload]\nGameState="*res://scripts/game_state.gd"\n'
                '_mcp_game_helper="*res://addons/godot_ai/runtime/game_helper.gd"\n\n'
                '[editor_plugins]\nenabled=PackedStringArray("res://addons/godot_ai/plugin.cfg")\n',
                encoding="utf-8",
            )
            descriptor = ProjectPilotDescriptor(
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
            report = workspace.transform_project_godot(project, descriptor)
            transformed = project.read_text(encoding="utf-8")
            self.assertNotIn("godot_ai", transformed)
            self.assertNotIn("_mcp_game_helper", transformed)
            self.assertIn("GameState", transformed)
            self.assertEqual(("GameState",), report.preserved_autoloads)

    def test_evidence_verifier_recomputes_physical_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scene = root / ".godot-live-editor-pilot/scratch.tscn"
            scene.parent.mkdir()
            scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
            result = {
                "status": "PASS",
                "repository": "owner/game",
                "source_commit": "a" * 40,
                "base_pilot_commit": "b" * 40,
                "saved_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
                "saved_scene_sha256": _sha256(scene),
                "ledger_states": ["COMPLETED", "COMPLETED"],
                "main_scene_inspect": "PASS",
                "scratch_scene_rename": "PASS",
                "editor_undo": "PASS",
                "scratch_scene_save": "PASS",
                "base_network_listener": False,
            }
            result_path = root / "runtime-result.json"
            result_path.write_text(json.dumps(result), encoding="utf-8")
            verified = evidence.verify_runtime_evidence(root, result_path)
            self.assertEqual(_sha256(scene), verified.saved_scene_sha256)

            result["saved_scene_sha256"] = "0" * 64
            result_path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ARTIFACT_BYTE_HASH_MISMATCH"):
                evidence.verify_runtime_evidence(root, result_path)

    def test_reusable_workflow_is_immutable_and_listener_free(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for marker in (
            "workflow_call:",
            "base_pilot_commit:",
            "repository: alsdmlals4-eng/Base",
            "ref: ${{ inputs.base_pilot_commit }}",
            "persist-credentials: false",
            "permissions:\n  contents: read",
            "Godot_v4.7.1-stable_linux.x86_64.zip",
            GODOT_ARCHIVE_SHA256,
            "PYTHONPATH: ${{ github.workspace }}/_base_c0",
            "python -m tools.godot_multi_project_pilot",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("github.action_path", text)
        self.assertNotIn("TCPServer", text)
        self.assertNotIn("WebSocket", text)
        self.assertNotIn("python _base_c0/tools/godot_multi_project_pilot.py", text)

    def test_readiness_docs_remain_truthful(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        readiness = (
            ROOT / "docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md"
        ).read_text(encoding="utf-8")
        for marker in (
            "disposable workspace",
            "main Scene",
            "scratch",
            "BASE_C0_SHA",
            "Program B",
            "Program C",
        ):
            self.assertIn(marker, guide)
        self.assertIn("multi_project_pilot_runner: STATIC_PASS", readiness)
        self.assertIn("real_project_pilots: NOT_RUN", readiness)
        self.assertIn("production_adapter_ready: NOT_READY", readiness)


if __name__ == "__main__":
    unittest.main()
