@tool
extends "res://addons/base_live_editor_adapter/plugin.gd"

const RESULT_PATH := "res://artifacts/godot-live-editor/editor_transaction_pilot_result.json"
const SCENE_PATH := "res://main.tscn"
const SERVICE_INSTANCE_ID := "pilot-service-001"

var _manifest: Dictionary = {}


func _enter_tree() -> void:
    super._enter_tree()
    call_deferred("_run_pilot")


func _run_pilot() -> void:
    await get_tree().process_frame
    var adapter_state := availability()
    if not adapter_state.get("available", false):
        _finish({"status": "FAIL", "code": adapter_state.get("code")})
        return

    _manifest = _load_json("res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json")
    EditorInterface.open_scene_from_path(SCENE_PATH)
    await get_tree().process_frame
    await get_tree().process_frame

    var root := EditorInterface.get_edited_scene_root()
    if root == null or root.get_node_or_null("Target") == null:
        _finish({"status": "FAIL", "code": "PILOT_SCENE_OPEN_FAILED"})
        return

    var inspect_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("."),
    )
    var inspect_result: Dictionary = await _submit_and_wait(
        _build_envelope(
            "scene.inspect",
            {},
            inspect_observation,
            "op-inspect-001",
        )
    )

    var dirty_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("Target"),
    )
    var dirty_result: Dictionary = await _submit_and_wait(
        _build_envelope(
            "node.rename",
            {
                "node_path": "Target",
                "new_name": "RenamedDirty",
                "save_mode": "KEEP_DIRTY",
            },
            dirty_observation,
            "op-rename-dirty-001",
        )
    )

    root = EditorInterface.get_edited_scene_root()
    var history_id := get_undo_redo().get_object_history_id(root)
    var history := get_undo_redo().get_history_undo_redo(history_id)
    if history != null:
        history.undo()
    await get_tree().process_frame
    var undo_pass := root.get_node_or_null("Target") != null

    var save_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("Target"),
    )
    var save_result: Dictionary = await _submit_and_wait(
        _build_envelope(
            "node.rename",
            {
                "node_path": "Target",
                "new_name": "RenamedSaved",
                "save_mode": "SAVE_CURRENT_SCENE",
            },
            save_observation,
            "op-rename-save-001",
        )
    )

    var saved_hash = null
    if save_result.get("success", false):
        saved_hash = save_result.get("data", {}).get("saved_scene_sha256")
    var ledger_states := [
        _ledger_state("op-rename-dirty-001"),
        _ledger_state("op-rename-save-001"),
    ]
    var passed: bool = (
        inspect_result.get("success", false)
        and dirty_result.get("success", false)
        and undo_pass
        and save_result.get("success", false)
        and ledger_states == ["COMPLETED", "COMPLETED"]
        and saved_hash != null
        and saved_hash == _evidence.sha256_file(SCENE_PATH)
        and network_listener_enabled == false
    )
    _finish({
        "status": "PASS" if passed else "FAIL",
        "engine_version": Engine.get_version_info().get("string", ""),
        "editor_instance_id": editor_instance_id(),
        "inspect_pass": inspect_result.get("success", false),
        "rename_keep_dirty_pass": dirty_result.get("success", false),
        "undo_pass": undo_pass,
        "rename_save_pass": save_result.get("success", false),
        "saved_scene_sha256": saved_hash,
        "ledger_states": ledger_states,
        "network_listener_enabled": network_listener_enabled,
        "inspect_code": inspect_result.get("code"),
        "rename_keep_dirty_code": dirty_result.get("code"),
        "rename_save_code": save_result.get("code"),
    })


func _submit_and_wait(envelope: Dictionary) -> Dictionary:
    var submitted := submit_validated_operation(envelope)
    if not submitted.get("ok", false):
        return {
            "success": false,
            "code": submitted.get("code", "SUBMIT_FAILED"),
        }
    var operation_id := str(envelope["operation_id"])
    for _index in range(120):
        await get_tree().process_frame
        var result := take_completed_result(operation_id)
        if not result.is_empty():
            return result
    return {"success": false, "code": "PILOT_RESULT_TIMEOUT"}


func _build_envelope(
    capability_id: String,
    arguments: Dictionary,
    observation: Dictionary,
    operation_id: String,
) -> Dictionary:
    var capability := _capability(capability_id)
    var request_hash := "a".repeat(64)
    var preconditions := {
        "expected_target_revision": observation.get("target_revision"),
        "observed_target_revision": observation.get("target_revision"),
        "expected_target_content_sha256": observation.get("target_content_sha256"),
        "observed_target_content_sha256": observation.get("target_content_sha256"),
        "expected_dirty_state": observation.get("dirty_state"),
        "observed_dirty_state": observation.get("dirty_state"),
        "expected_scene_path": observation.get("scene_path"),
        "observed_scene_path": observation.get("scene_path"),
        "conflict_policy": "FAIL_CLOSED",
    }
    var policy := {
        "effect_kind": capability.get("effect_kind"),
        "idempotency": capability.get("idempotency"),
        "approval_policy": capability.get("approval_policy"),
        "execution_mode": capability.get("execution_mode"),
        "rollback_policy": capability.get("rollback_policy"),
    }
    var snapshot := {
        "contract_version": _manifest.get("contract_version"),
        "adapter_version": _manifest.get("adapter_version"),
        "catalog_sha256": _manifest.get("catalog", {}).get("sha256"),
        "capability_input_schema_sha256": capability.get("input_schema_sha256"),
        "capability_output_schema_sha256": capability.get("output_schema_sha256"),
        "protocol_profile": _manifest.get("transport", {}).get("protocol_profile"),
        "protocol_version": _manifest.get("transport", {}).get("protocol_version"),
    }
    var instance_identity := {
        "automation_service_instance_id": SERVICE_INSTANCE_ID,
        "editor_instance_id": editor_instance_id(),
        "runtime_session_id": null,
        "runtime_session_state": "NOT_APPLICABLE",
    }
    var envelope := {
        "schema_version": 2,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": operation_id,
        "capability_id": capability_id,
        "project_identity": _manifest.get("project_identity", {}).duplicate(true),
        "instance_identity": instance_identity,
        "contract_snapshot": snapshot,
        "policy": policy,
        "request": {"arguments": arguments.duplicate(true)},
        "request_hash": request_hash,
        "idempotency_key": operation_id if capability_id == "node.rename" else null,
        "preconditions": preconditions,
        "approval": {
            "state": "NOT_REQUIRED",
            "token_id": null,
            "token_binding": null,
            "expires_at": null,
            "consumed_by_operation_id": null,
        },
        "task": {
            "task_id": null,
            "state": "NOT_APPLICABLE",
            "created_at": null,
            "last_updated_at": null,
            "ttl_ms": null,
            "poll_interval_ms": null,
            "cancellation_policy": "NOT_SUPPORTED",
            "result_binding": null,
        },
        "result": {
            "success": false,
            "code": "NOT_RUN",
            "message": "Not executed.",
            "data": {},
            "result_hash": "b".repeat(64),
            "evidence": [],
        },
    }
    if capability.get("approval_policy") == "REQUIRED":
        envelope["approval"] = {
            "state": "APPROVED",
            "token_id": "token-%s" % operation_id,
            "token_binding": {
                "operation_id": operation_id,
                "capability_id": capability_id,
                "project_identity": envelope["project_identity"].duplicate(true),
                "instance_identity": instance_identity.duplicate(true),
                "contract_snapshot": snapshot.duplicate(true),
                "policy": policy.duplicate(true),
                "request_hash": request_hash,
                "preconditions": preconditions.duplicate(true),
            },
            "expires_at": "2099-01-01T00:00:00Z",
            "consumed_by_operation_id": operation_id,
        }
    return envelope


func _capability(capability_id: String) -> Dictionary:
    for value in _manifest.get("capabilities", []):
        if value is Dictionary and value.get("capability_id") == capability_id:
            return value
    return {}


func _ledger_state(operation_id: String) -> Variant:
    return _ledger.read_record(operation_id).get("state")


func _load_json(path: String) -> Dictionary:
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {}
    var parsed = JSON.parse_string(file.get_as_text())
    return parsed if parsed is Dictionary else {}


func _finish(payload: Dictionary) -> void:
    var absolute := ProjectSettings.globalize_path(RESULT_PATH)
    DirAccess.make_dir_recursive_absolute(absolute.get_base_dir())
    var file := FileAccess.open(absolute, FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(payload, "  ") + "\n")
        file.flush()
        file.close()
    get_tree().quit()
