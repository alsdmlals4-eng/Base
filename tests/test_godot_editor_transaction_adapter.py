from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "templates/project-operations/godot-live-editor/addons/base_live_editor_adapter"

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
        self.assertEqual(REQUIRED, {path.name for path in ADDON.iterdir() if path.is_file()})

    def test_adapter_has_required_editor_transaction_markers(self) -> None:
        self.assertTrue(ADDON.is_dir(), "missing canonical editor adapter directory")
        source = "\n".join(path.read_text(encoding="utf-8") for path in ADDON.glob("*.gd"))
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

    def test_guard_rechecks_full_approval_binding_and_expiry(self) -> None:
        source = (ADDON / "runtime_contract_guard.gd").read_text(encoding="utf-8")
        for marker in (
            "token_binding",
            "_approval_binding",
            "APPROVAL_BINDING_MISMATCH",
            "APPROVAL_EXPIRED",
            "get_unix_time_from_datetime_string",
            "_unix_time_from_rfc3339",
            'ends_with("Z")',
            "offset_seconds",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)

    def test_state_probe_uses_editor_owned_state(self) -> None:
        source = (ADDON / "editor_state_probe.gd").read_text(encoding="utf-8")
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
        source = (ADDON / "capability_registry.gd").read_text(encoding="utf-8")
        self.assertIn('"scene.inspect"', source)
        self.assertIn('"node.rename"', source)
        self.assertIn("UNKNOWN_CAPABILITY", source)
        self.assertIn("ABSOLUTE_NODE_PATH_FORBIDDEN", source)
        self.assertIn("NODE_OUTSIDE_EDITED_SCENE", source)
        self.assertIn("INVALID_NODE_NAME", source)
        self.assertNotIn("set_indexed", source)

    def test_registry_validates_output_types_and_cross_field_semantics(self) -> None:
        source = (ADDON / "capability_registry.gd").read_text(encoding="utf-8")
        for marker in (
            "_validate_inspect_output",
            "_validate_rename_output",
            "TYPE_INT",
            "SAVE_CURRENT_SCENE",
            "saved_scene_sha256",
            "OUTPUT_SCHEMA_INVALID",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)

    def test_ledger_and_evidence_are_atomic_and_confined(self) -> None:
        ledger = (ADDON / "operation_ledger.gd").read_text(encoding="utf-8")
        evidence = (ADDON / "evidence_writer.gd").read_text(encoding="utf-8")
        for source in (ledger, evidence):
            self.assertIn("ProjectSettings.globalize_path", source)
            self.assertIn(".tmp", source)
            self.assertIn("rename_absolute", source)
        self.assertIn("HashingContext.HASH_SHA256", evidence)
        self.assertIn("LEDGER_STATE_INVALID", ledger)
        self.assertIn("STARTED", ledger)
        self.assertIn("COMPLETED", ledger)
        self.assertIn("FAILED", ledger)

    def test_operation_ids_with_digits_are_safe_and_replace_is_atomic(self) -> None:
        ledger = (ADDON / "operation_ledger.gd").read_text(encoding="utf-8")
        evidence = (ADDON / "evidence_writer.gd").read_text(encoding="utf-8")
        self.assertNotIn("character.is_valid_identifier()", ledger)
        for source in (ledger, evidence):
            self.assertIn("SAFE_NAME_CHARACTERS", source)
            self.assertNotIn("DirAccess.remove_absolute(target_path)", source)
            self.assertIn("JSON.stringify(payload) +", source)

    def test_executor_orders_precondition_ledger_undo_save_and_terminal_state(self) -> None:
        source = (ADDON / "editor_transaction_executor.gd").read_text(encoding="utf-8")
        markers = [
            "validate_before_execute",
            "record_started",
            "create_action",
            "add_do_property",
            "add_undo_property",
            "commit_action",
            "mark_scene_as_unsaved",
            "save_scene",
            "update_file",
            "sha256_file",
            "record_terminal",
        ]
        positions = [source.index(marker) for marker in markers]
        self.assertEqual(sorted(positions), positions)

    def test_executor_has_stable_failure_codes(self) -> None:
        source = (ADDON / "editor_transaction_executor.gd").read_text(encoding="utf-8")
        for code in (
            "TARGET_STATE_CONFLICT",
            "LEDGER_START_FAILED",
            "UNDO_REDO_BUSY",
            "SAVE_FAILED",
            "OUTPUT_SCHEMA_INVALID",
            "EVIDENCE_WRITE_FAILED",
        ):
            with self.subTest(code=code):
                self.assertIn(code, source)

    def test_adapter_work_is_bounded_and_streamed(self) -> None:
        queue = (ADDON / "request_queue.gd").read_text(encoding="utf-8")
        plugin = (ADDON / "plugin.gd").read_text(encoding="utf-8")
        probe = (ADDON / "editor_state_probe.gd").read_text(encoding="utf-8")
        evidence = (ADDON / "evidence_writer.gd").read_text(encoding="utf-8")
        self.assertIn("const MAX_PENDING := 64", queue)
        self.assertIn("const MAX_COMPLETED_RESULTS := 64", plugin)
        self.assertEqual(1, plugin.count("_queue.pop_next()"))
        self.assertIn("65536", probe)
        self.assertIn("65536", evidence)

    def test_plugin_is_composition_only_and_network_disabled(self) -> None:
        source = (ADDON / "plugin.gd").read_text(encoding="utf-8")
        self.assertIn("extends EditorPlugin", source)
        self.assertIn("func submit_validated_operation(envelope: Dictionary) -> Dictionary:", source)
        self.assertIn("func _process(_delta: float) -> void:", source)
        self.assertIn("execute(envelope)", source)
        self.assertIn("_queue.clear()", source)
        self.assertIn("network_listener_enabled", source)
        self.assertIn("ADAPTER_NOT_CONFIGURED", source)
        self.assertIn('transport.get("kind") != "PROJECT_DEFINED"', source)
        self.assertIn('const IN_PROCESS_ENDPOINT := "in-process-editor-plugin"', source)
        self.assertIn('transport.get("endpoint_identity") != IN_PROCESS_ENDPOINT', source)
        self.assertIn('transport.get("bind_host") != null', source)


if __name__ == "__main__":
    unittest.main()
