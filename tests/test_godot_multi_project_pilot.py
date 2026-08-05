from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-project-pilot-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json"
WORKFLOW = ROOT / ".github/workflows/reusable-godot-project-pilot.yml"
GUIDE = ROOT / "docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md"

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
            "TYPE_MISMATCH",
        ):
            self.assertIn(marker, registry)

    def test_descriptor_schema_is_closed_and_template_is_non_authorizing(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        _assert_closed(self, schema)
        self.assertEqual(
            "^[0-9a-f]{40}$",
            schema["properties"]["base_pilot_commit"]["pattern"],
        )
        self.assertNotIn("command", json.dumps(schema))
        self.assertNotIn("shell", json.dumps(schema))
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual("NOT_CREATED", template["project_state"])
        self.assertEqual("0" * 40, template["base_pilot_commit"])
        self.assertIsNone(template["project_file"])
        self.assertEqual([], template["behavior_checks"])

    def test_descriptor_loader_accepts_valid_runtime_and_static_descriptors(self) -> None:
        module = _load("tools/godot_project_pilot_descriptor.py")
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = {
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
                "behavior_checks": [
                    {
                        "kind": "GODOT_SCRIPT",
                        "target": "res://tests/run_tests.gd",
                        "timeout_seconds": 30,
                    }
                ],
                "expected_platform": "PC",
            }
            path = root / "runtime.json"
            path.write_text(json.dumps(runtime), encoding="utf-8")
            loaded = module.load_descriptor(path, SCHEMA)
            self.assertTrue(loaded.is_runtime_project)
            static = json.loads(TEMPLATE.read_text(encoding="utf-8"))
            static["base_pilot_commit"] = "c" * 40
            path.write_text(json.dumps(static), encoding="utf-8")
            loaded = module.load_descriptor(path, SCHEMA)
            self.assertFalse(loaded.is_runtime_project)

    def test_shared_materializer_preserves_existing_pilot_contract(self) -> None:
        shared = _load("tools/godot_editor_adapter_materialization.py")
        existing = _load("tools/materialize_godot_editor_adapter_pilot.py")
        self.assertIsNotNone(shared)
        self.assertIsNotNone(existing)
        capabilities = shared.build_capabilities()
        self.assertEqual(
            {"scene.inspect", "node.rename"},
            {item["capability_id"] for item in capabilities},
        )
        with tempfile.TemporaryDirectory() as temporary:
            project = existing.materialize(ROOT, Path(temporary) / "pilot")
            manifest = json.loads(
                (project / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(capabilities, manifest["capabilities"])

    def test_tracked_inventory_detects_source_mutation(self) -> None:
        module = _load("tools/godot_project_pilot_workspace.py")
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "project.godot").write_text("[application]\n", encoding="utf-8")
            (root / "main.tscn").write_text("[gd_scene format=3]\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            before = module.inventory_tracked_files(root)
            (root / "main.tscn").write_text("[gd_scene format=3]\n[node]\n", encoding="utf-8")
            after = module.inventory_tracked_files(root)
            self.assertEqual(("main.tscn",), module.compare_inventories(before, after))
            self.assertNotEqual(
                module.inventory_digest(before),
                module.inventory_digest(after),
            )

    def test_project_transform_removes_only_declared_legacy_authority(self) -> None:
        descriptor_module = _load("tools/godot_project_pilot_descriptor.py")
        workspace_module = _load("tools/godot_project_pilot_workspace.py")
        self.assertIsNotNone(descriptor_module)
        self.assertIsNotNone(workspace_module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "project.godot"
            project.write_text(
                'config_version=5\n\n[application]\nrun/main_scene="res://main.tscn"\n\n'
                '[autoload]\nGameState="*res://scripts/game_state.gd"\n'
                '_mcp_game_helper="*res://addons/godot_ai/runtime/game_helper.gd"\n\n'
                '[editor_plugins]\nenabled=PackedStringArray("res://addons/godot_ai/plugin.cfg")\n',
                encoding="utf-8",
            )
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
            report = workspace_module.transform_project_godot(project, descriptor)
            transformed = project.read_text(encoding="utf-8")
            self.assertNotIn("godot_ai", transformed)
            self.assertNotIn("_mcp_game_helper", transformed)
            self.assertIn("GameState", transformed)
            self.assertEqual(("GameState",), report.preserved_autoloads)

    def test_evidence_verifier_recomputes_physical_bytes(self) -> None:
        module = _load("tools/godot_project_pilot_evidence.py")
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            scene = workspace / ".godot-live-editor-pilot/scratch.tscn"
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
            result_path = workspace / "runtime-result.json"
            result_path.write_text(json.dumps(result), encoding="utf-8")
            verified = module.verify_runtime_evidence(workspace, result_path)
            self.assertEqual(_sha256(scene), verified.saved_scene_sha256)
            result["saved_scene_sha256"] = "0" * 64
            result_path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ARTIFACT_BYTE_HASH_MISMATCH"):
                module.verify_runtime_evidence(workspace, result_path)

    def test_reusable_workflow_is_immutable_and_listener_free(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_call:", text)
        self.assertIn("base_pilot_commit:", text)
        self.assertIn("repository: alsdmlals4-eng/Base", text)
        self.assertIn("ref: ${{ inputs.base_pilot_commit }}", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("Godot_v4.7.1-stable_linux.x86_64.zip", text)
        self.assertIn(
            "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
            text,
        )
        self.assertNotIn("github.action_path", text)
        self.assertNotIn("TCPServer", text)
        self.assertNotIn("WebSocket", text)

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
