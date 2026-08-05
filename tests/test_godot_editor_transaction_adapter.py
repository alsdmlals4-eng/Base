from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADDON = (
    ROOT
    / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"
)

REQUIRED = {
    "plugin.cfg",
    "plugin.gd",
    "request_queue.gd",
    "runtime_contract_guard.gd",
    "editor_state_probe.gd",
    "capability_registry.gd",
    "operation_ledger.gd",
    "evidence_writer.gd",
    "editor_transaction_executor.gd",
    "README.md",
}


class GodotEditorTransactionAdapterTests(unittest.TestCase):
    def test_editor_transaction_adapter_files_exist(self) -> None:
        self.assertTrue(ADDON.is_dir(), "missing canonical editor adapter directory")
        self.assertEqual(
            REQUIRED,
            {path.name for path in ADDON.iterdir() if path.is_file()},
        )

    def test_adapter_has_required_editor_transaction_markers(self) -> None:
        self.assertTrue(ADDON.is_dir(), "missing canonical editor adapter directory")
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in ADDON.glob("*.gd")
        )
        for required in (
            "EditorPlugin",
            "get_undo_redo()",
            "EditorInterface.get_unsaved_scenes()",
            "EditorInterface.save_scene()",
            "get_resource_filesystem().update_file",
            "TARGET_STATE_CONFLICT",
            "STARTED",
            "COMPLETED",
            "FAILED",
            "MAX_PENDING",
        ):
            with self.subTest(required=required):
                self.assertIn(required, source)

        for forbidden in (
            "TCPServer",
            "WebSocketPeer",
            "HTTPServer",
            "PacketPeerUDP",
            "Thread.new",
            "OS.execute",
            "GDScript.new",
            "Expression.new",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_queue_is_bounded_and_rejects_duplicates(self) -> None:
        path = ADDON / "request_queue.gd"
        self.assertTrue(path.is_file(), "missing request_queue.gd")
        source = path.read_text(encoding="utf-8")
        self.assertIn("const MAX_PENDING := 64", source)
        self.assertIn("QUEUE_FULL", source)
        self.assertIn("DUPLICATE_OPERATION_ID", source)
        self.assertIn("OPERATION_ID_REQUIRED", source)
        self.assertIn("envelope.duplicate(true)", source)

    def test_guard_rechecks_exact_v2_bindings(self) -> None:
        path = ADDON / "runtime_contract_guard.gd"
        self.assertTrue(path.is_file(), "missing runtime_contract_guard.gd")
        source = path.read_text(encoding="utf-8")
        for marker in (
            "schema_version",
            "project_fingerprint",
            "automation_service_instance_id",
            "editor_instance_id",
            "contract_snapshot",
            "capability_id",
            "approval",
            "request_hash",
            "TARGET_STATE_CONFLICT",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)
        self.assertIn("validate_for_enqueue", source)
        self.assertIn("validate_before_execute", source)

    def test_state_probe_uses_editor_owned_state(self) -> None:
        path = ADDON / "editor_state_probe.gd"
        self.assertTrue(path.is_file(), "missing editor_state_probe.gd")
        source = path.read_text(encoding="utf-8")
        for marker in (
            "EditorInterface.get_unsaved_scenes()",
            "get_object_history_id",
            "get_history_undo_redo",
            "get_version()",
            "HashingContext.HASH_SHA256",
            "ProjectSettings.globalize_path",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)

    def test_registry_allows_only_inspect_and_rename(self) -> None:
        path = ADDON / "capability_registry.gd"
        self.assertTrue(path.is_file(), "missing capability_registry.gd")
        source = path.read_text(encoding="utf-8")
        self.assertIn('"scene.inspect"', source)
        self.assertIn('"node.rename"', source)
        self.assertIn("UNKNOWN_CAPABILITY", source)
        self.assertIn("ABSOLUTE_NODE_PATH_FORBIDDEN", source)
        self.assertIn("NODE_OUTSIDE_EDITED_SCENE", source)
        self.assertIn("INVALID_NODE_NAME", source)
        self.assertNotIn("set_indexed", source)

    def test_ledger_and_evidence_are_atomic_and_confined(self) -> None:
        ledger_path = ADDON / "operation_ledger.gd"
        evidence_path = ADDON / "evidence_writer.gd"
        self.assertTrue(ledger_path.is_file(), "missing operation_ledger.gd")
        self.assertTrue(evidence_path.is_file(), "missing evidence_writer.gd")
        ledger = ledger_path.read_text(encoding="utf-8")
        evidence = evidence_path.read_text(encoding="utf-8")
        for source in (ledger, evidence):
            self.assertIn("ProjectSettings.globalize_path", source)
            self.assertIn(".tmp", source)
            self.assertIn("rename_absolute", source)
        self.assertIn("HashingContext.HASH_SHA256", evidence)
        self.assertIn("LEDGER_STATE_INVALID", ledger)
        self.assertIn("STARTED", ledger)
        self.assertIn("COMPLETED", ledger)
        self.assertIn("FAILED", ledger)


if __name__ == "__main__":
    unittest.main()
