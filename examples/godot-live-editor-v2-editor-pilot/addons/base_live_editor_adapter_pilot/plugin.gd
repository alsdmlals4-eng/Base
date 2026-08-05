@tool
extends "res://addons/base_live_editor_adapter/plugin.gd"

const RESULT_PATH := "res://artifacts/godot-live-editor/editor_transaction_pilot_result.json"
const SCENE_PATH := "res://main.tscn"
const SERVICE_INSTANCE_ID := "pilot-service-001"
const BATCH_SIZE := 64

var _manifest: Dictionary = {}


func _enter_tree() -> void:
    super._enter_tree()
    call_deferred("_run_pilot")


func _run_pilot() -> void:
    var pilot_started_usec := Time.get_ticks_usec()
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

    root = EditorInterface.get_edited_scene_root()
    var stale_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("RenamedSaved"),
    )
    var stale_envelope := _build_envelope(
        "node.rename",
        {
            "node_path": "RenamedSaved",
            "new_name": "ShouldNotApply",
            "save_mode": "KEEP_DIRTY",
        },
        stale_observation,
        "op-rename-stale-001",
    )
    stale_envelope["preconditions"]["expected_target_revision"] = "stale-revision"
    _refresh_request_security(stale_envelope, _capability("node.rename"))
    var stale_result: Dictionary = await _submit_and_wait(stale_envelope)
    var stale_state_block_pass: bool = (
        not stale_result.get("success", false)
        and stale_result.get("code") == "TARGET_STATE_CONFLICT"
        and root.get_node_or_null("RenamedSaved") != null
        and root.get_node_or_null("ShouldNotApply") == null
        and _ledger_state("op-rename-stale-001") == null
    )

    var hash_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("."),
    )
    var hash_envelope := _build_envelope(
        "scene.inspect",
        {},
        hash_observation,
        "op-hash-tamper-001",
    )
    hash_envelope["request"]["arguments"] = {"tampered": true}
    var hash_submit := submit_validated_operation(hash_envelope)
    var request_hash_block_pass: bool = (
        not hash_submit.get("ok", false)
        and hash_submit.get("code") == "REQUEST_HASH_MISMATCH"
        and _ledger_state("op-hash-tamper-001") == null
    )

    var approval_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("RenamedSaved"),
    )
    var expired_envelope := _build_envelope(
        "node.rename",
        {
            "node_path": "RenamedSaved",
            "new_name": "ExpiredShouldNotApply",
            "save_mode": "KEEP_DIRTY",
        },
        approval_observation,
        "op-rename-expired-001",
    )
    expired_envelope["approval"]["expires_at"] = "2000-01-01T00:00:00Z"
    var expired_submit := submit_validated_operation(expired_envelope)
    var expired_approval_block_pass: bool = (
        not expired_submit.get("ok", false)
        and expired_submit.get("code") == "APPROVAL_EXPIRED"
        and root.get_node_or_null("RenamedSaved") != null
        and root.get_node_or_null("ExpiredShouldNotApply") == null
        and _ledger_state("op-rename-expired-001") == null
    )

    var binding_envelope := _build_envelope(
        "node.rename",
        {
            "node_path": "RenamedSaved",
            "new_name": "BindingShouldNotApply",
            "save_mode": "KEEP_DIRTY",
        },
        approval_observation,
        "op-rename-binding-001",
    )
    binding_envelope["approval"]["token_binding"]["policy"]["rollback_policy"] = "MANUAL"
    var binding_submit := submit_validated_operation(binding_envelope)
    var approval_binding_block_pass: bool = (
        not binding_submit.get("ok", false)
        and binding_submit.get("code") == "APPROVAL_BINDING_MISMATCH"
        and root.get_node_or_null("RenamedSaved") != null
        and root.get_node_or_null("BindingShouldNotApply") == null
        and _ledger_state("op-rename-binding-001") == null
    )

    var batch_observation: Dictionary = _probe.observe(
        get_editor_interface(),
        get_undo_redo(),
        NodePath("."),
    )
    var batch_ids: Array[String] = []
    var queue_capacity_pass := true
    var batch_started_usec := Time.get_ticks_usec()
    for index in range(BATCH_SIZE):
        var operation_id := "op-batch-%03d" % index
        var submitted := submit_validated_operation(
            _build_envelope(
                "scene.inspect",
                {},
                batch_observation,
                operation_id,
            )
        )
        if not submitted.get("ok", false):
            queue_capacity_pass = false
        batch_ids.append(operation_id)
    var overflow := submit_validated_operation(
        _build_envelope(
            "scene.inspect",
            {},
            batch_observation,
            "op-batch-overflow",
        )
    )
    queue_capacity_pass = (
        queue_capacity_pass
        and not overflow.get("ok", false)
        and overflow.get("code") == "QUEUE_FULL"
    )

    var batch_64_completed := 0
    var batch_64_pass := true
    for _frame_index in range(BATCH_SIZE + 60):
        await get_tree().process_frame
        var pending := batch_ids.duplicate()
        for operation_id in pending:
            var batch_result := take_completed_result(operation_id)
            if batch_result.is_empty():
                continue
            batch_ids.erase(operation_id)
            batch_64_completed += 1
            if not batch_result.get("success", false) or not _valid_result_hash(batch_result):
                batch_64_pass = false
        if batch_ids.is_empty():
            break
    var batch_64_elapsed_usec := Time.get_ticks_usec() - batch_started_usec
    batch_64_pass = batch_64_pass and batch_ids.is_empty() and batch_64_completed == BATCH_SIZE

    var saved_hash = null
    if save_result.get("success", false):
        saved_hash = save_result.get("data", {}).get("saved_scene_sha256")
    var ledger_states := [
        _ledger_state("op-rename-dirty-001"),
        _ledger_state("op-rename-save-001"),
    ]
    var result_hash_pass: bool = (
        _valid_result_hash(inspect_result)
        and _valid_result_hash(dirty_result)
        and _valid_result_hash(save_result)
        and _valid_result_hash(stale_result)
    )
    var passed: bool = (
        inspect_result.get("success", false)
        and dirty_result.get("success", false)
        and undo_pass
        and save_result.get("success", false)
        and stale_state_block_pass
        and request_hash_block_pass
        and expired_approval_block_pass
        and approval_binding_block_pass
        and result_hash_pass
        and queue_capacity_pass
        and batch_64_pass
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
        "stale_state_block_pass": stale_state_block_pass,
        "request_hash_block_pass": request_hash_block_pass,
        "expired_approval_block_pass": expired_approval_block_pass,
        "approval_binding_block_pass": approval_binding_block_pass,
        "result_hash_pass": result_hash_pass,
        "queue_capacity_pass": queue_capacity_pass,
        "batch_64_pass": batch_64_pass,
        "batch_64_completed": batch_64_completed,
        "batch_64_elapsed_usec": batch_64_elapsed_usec,
        "saved_scene_sha256": saved_hash,
        "ledger_states": ledger_states,
        "network_listener_enabled": network_listener_enabled,
        "elapsed_usec": Time.get_ticks_usec() - pilot_started_usec,
        "inspect_code": inspect_result.get("code"),
        "rename_keep_dirty_code": dirty_result.get("code"),
        "rename_save_code": save_result.get("code"),
        "stale_code": stale_result.get("code"),
        "request_hash_code": hash_submit.get("code"),
        "expired_approval_code": expired_submit.get("code"),
        "approval_binding_code": binding_submit.get("code"),
    })


func _submit_and_wait(envelope: Dictionary) -> Dictionary:
    var submitted := submit_validated_operation(envelope)
    if not submitted.get("ok", false):
        return {
            "success": false,
            "code": submitted.get("code", "SUBMIT_FAILED"),
            "message": submitted.get("code", "SUBMIT_FAILED"),
            "data": {},
            "result_hash": _guard.canonical_json_sha256({}),
            "evidence": [],
        }
    var operation_id := str(envelope["operation_id"])
    for _index in range(120):
        await get_tree().process_frame
        var result := take_completed_result(operation_id)
        if not result.is_empty():
            return result
    return {
        "success": false,
        "code": "PILOT_RESULT_TIMEOUT",
        "message": "PILOT_RESULT_TIMEOUT",
        "data": {},
        "result_hash": _guard.canonical_json_sha256({}),
        "evidence": [],
    }


func _build_envelope(
    capability_id: String,
    arguments: Dictionary,
    observation: Dictionary,
    operation_id: String,
) -> Dictionary:
    var capability := _capability(capability_id)
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
        "request_hash": "",
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
            "result_hash": _guard.canonical_json_sha256({}),
            "evidence": [],
        },
    }
    _refresh_request_security(envelope, capability)
    return envelope


func _refresh_request_security(envelope: Dictionary, capability: Dictionary) -> void:
    var request_hash: String = _guard.canonical_json_sha256(
        _guard.operation_request_material(envelope)
    )
    envelope["request_hash"] = request_hash
    if capability.get("approval_policy") == "REQUIRED":
        envelope["approval"] = {
            "state": "APPROVED",
            "token_id": "token-%s" % envelope["operation_id"],
            "token_binding": {
                "operation_id": envelope["operation_id"],
                "capability_id": envelope["capability_id"],
                "project_identity": envelope["project_identity"].duplicate(true),
                "instance_identity": envelope["instance_identity"].duplicate(true),
                "contract_snapshot": envelope["contract_snapshot"].duplicate(true),
                "policy": envelope["policy"].duplicate(true),
                "request_hash": request_hash,
                "preconditions": envelope["preconditions"].duplicate(true),
            },
            "expires_at": "2099-01-01T00:00:00Z",
            "consumed_by_operation_id": envelope["operation_id"],
        }


func _valid_result_hash(result: Dictionary) -> bool:
    var expected: String = _guard.canonical_json_sha256(result.get("data", {}))
    return str(result.get("result_hash", "")) == expected and expected.length() == 64


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
