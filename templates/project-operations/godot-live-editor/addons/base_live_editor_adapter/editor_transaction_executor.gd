@tool
extends RefCounted

var _editor_interface: EditorInterface
var _undo_redo: EditorUndoRedoManager
var _guard
var _registry
var _probe
var _ledger
var _evidence


func configure(
    editor_interface: EditorInterface,
    undo_redo: EditorUndoRedoManager,
    guard,
    registry,
    probe,
    ledger,
    evidence,
) -> void:
    _editor_interface = editor_interface
    _undo_redo = undo_redo
    _guard = guard
    _registry = registry
    _probe = probe
    _ledger = ledger
    _evidence = evidence


func execute(envelope: Dictionary) -> Dictionary:
    var capability_id := str(envelope.get("capability_id", ""))
    var arguments: Dictionary = envelope.get("request", {}).get("arguments", {})
    var argument_errors: PackedStringArray = _registry.validate_arguments(
        capability_id,
        arguments,
    )
    if not argument_errors.is_empty():
        return _failure(str(argument_errors[0]))

    var target_path := NodePath(".")
    if capability_id == "node.rename":
        target_path = NodePath(str(arguments.get("node_path", "")))
    var observation: Dictionary = _probe.observe(
        _editor_interface,
        _undo_redo,
        target_path,
    )
    if observation.has("error"):
        return _failure(str(observation["error"]))

    var execution_errors: PackedStringArray = _guard.validate_before_execute(
        envelope,
        observation,
    )
    if not execution_errors.is_empty():
        var code := str(execution_errors[0])
        if execution_errors.has("TARGET_STATE_CONFLICT"):
            code = "TARGET_STATE_CONFLICT"
        return _failure(code)

    if capability_id == "scene.inspect":
        return _inspect_scene(envelope, observation)
    if capability_id != "node.rename":
        return _failure("UNKNOWN_CAPABILITY")

    var serializable_observation := observation.duplicate(true)
    serializable_observation.erase("target_node")
    var started: Dictionary = _ledger.record_started(
        envelope,
        serializable_observation,
    )
    if not started.get("ok", false):
        return _failure("LEDGER_START_FAILED")
    if started.get("replay", false):
        var replay_record: Dictionary = started.get("record", {})
        return replay_record.get("result", _failure("LEDGER_REPLAY_INVALID"))

    if _undo_redo.is_committing_action():
        return _fail_terminal(envelope, "UNDO_REDO_BUSY")
    var target: Node = observation["target_node"]
    var old_name := target.name
    var new_name := StringName(arguments["new_name"])

    _undo_redo.create_action(
        "Base Live Editor: Rename Node",
        UndoRedo.MERGE_DISABLE,
        target,
    )
    _undo_redo.add_do_property(target, &"name", new_name)
    _undo_redo.add_undo_property(target, &"name", old_name)
    _undo_redo.commit_action()
    EditorInterface.mark_scene_as_unsaved()

    if str(target.name) != str(new_name):
        return _fail_terminal(envelope, "POSTCONDITION_FAILED")

    var scene_path := str(observation.get("scene_path", ""))
    var save_mode := str(arguments["save_mode"])
    var dirty_state := "DIRTY"
    var saved_scene_sha256: Variant = null
    if save_mode == "SAVE_CURRENT_SCENE":
        var save_error := EditorInterface.save_scene()
        if save_error != OK:
            return _fail_terminal(envelope, "SAVE_FAILED")
        EditorInterface.get_resource_filesystem().update_file(scene_path)
        saved_scene_sha256 = _evidence.sha256_file(scene_path)
        if saved_scene_sha256 == null:
            return _fail_terminal(envelope, "SAVE_FAILED")
        dirty_state = "CLEAN"
    elif not EditorInterface.get_unsaved_scenes().has(scene_path):
        return _fail_terminal(envelope, "DIRTY_STATE_MISMATCH")

    var output := {
        "scene_path": scene_path,
        "node_path": str(arguments["node_path"]),
        "old_name": str(old_name),
        "new_name": str(new_name),
        "save_mode": save_mode,
        "dirty_state": dirty_state,
        "saved_scene_sha256": saved_scene_sha256,
    }
    var output_errors: PackedStringArray = _registry.validate_output(
        capability_id,
        output,
    )
    if not output_errors.is_empty():
        return _fail_terminal(envelope, "OUTPUT_SCHEMA_INVALID")

    var evidence_result: Dictionary = _evidence.write_json(
        str(envelope["operation_id"]),
        {
            "operation_id": envelope["operation_id"],
            "capability_id": capability_id,
            "output": output,
        },
    )
    if not evidence_result.get("ok", false):
        return _fail_terminal(envelope, "EVIDENCE_WRITE_FAILED")

    var result := _success(
        "OK",
        "Node rename completed.",
        output,
        [_evidence_entry(capability_id, evidence_result)],
    )
    var terminal: Dictionary = _ledger.record_terminal(
        str(envelope["operation_id"]),
        "COMPLETED",
        result,
    )
    if not terminal.get("ok", false):
        return _failure("LEDGER_TERMINAL_FAILED")
    return result


func _inspect_scene(
    envelope: Dictionary,
    observation: Dictionary,
) -> Dictionary:
    var output: Dictionary = _registry.inspect_scene(_editor_interface, observation)
    var output_errors: PackedStringArray = _registry.validate_output(
        "scene.inspect",
        output,
    )
    if not output_errors.is_empty():
        return _failure("OUTPUT_SCHEMA_INVALID")
    var evidence_result: Dictionary = _evidence.write_json(
        str(envelope["operation_id"]),
        {
            "operation_id": envelope["operation_id"],
            "capability_id": "scene.inspect",
            "output": output,
        },
    )
    if not evidence_result.get("ok", false):
        return _failure("EVIDENCE_WRITE_FAILED")
    return _success(
        "OK",
        "Scene inspection completed.",
        output,
        [_evidence_entry("scene.inspect", evidence_result)],
    )


func _fail_terminal(envelope: Dictionary, code: String) -> Dictionary:
    var result := _failure(code)
    var terminal: Dictionary = _ledger.record_terminal(
        str(envelope.get("operation_id", "")),
        "FAILED",
        result,
    )
    if not terminal.get("ok", false):
        return _failure("LEDGER_TERMINAL_FAILED")
    return result


func _evidence_entry(
    capability_id: String,
    evidence_result: Dictionary,
) -> Dictionary:
    return {
        "kind": "ENGINE_STATE",
        "state": "EXECUTION_PASS",
        "path": evidence_result.get("path"),
        "artifact_sha256": evidence_result.get("artifact_sha256"),
        "generated_at": Time.get_datetime_string_from_system(true, false) + "Z",
        "producer": "%s@2.0.0" % capability_id,
    }


func _success(
    code: String,
    message: String,
    data: Dictionary,
    evidence: Array,
) -> Dictionary:
    return {
        "success": true,
        "code": code,
        "message": message,
        "data": data,
        "result_hash": _guard.canonical_json_sha256(data),
        "evidence": evidence,
    }


func _failure(code: String) -> Dictionary:
    var data := {}
    return {
        "success": false,
        "code": code,
        "message": code,
        "data": data,
        "result_hash": _guard.canonical_json_sha256(data),
        "evidence": [],
    }
