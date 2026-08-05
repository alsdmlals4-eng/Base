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
        source = (ADDON / "request_queue.gd").read_text(encoding="utf-8")
        self.assertIn("const MAX_PENDING := 64", source)
        self.assertIn("QUEUE_FULL", source)
        self.assertIn("DUPLICATE_OPERATION_ID", source)
        self.assertIn("OPERATION_ID_REQUIRED", source)
        self.assertIn("envelope.duplicate(true)", source)

    def test_guard_rechecks_exact_v2_bindings(self) -> None:
        source = (ADDON / "runtime_contract_guard.gd").read_text(encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
