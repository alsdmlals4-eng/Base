@tool
extends RefCounted

const DEFAULT_ROOT := "res://artifacts/godot-live-editor/ledger"
const TERMINAL_STATES := ["COMPLETED", "FAILED"]
const SAFE_NAME_CHARACTERS := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
const MAX_SAFE_NAME_LENGTH := 128

var _root_path := DEFAULT_ROOT


func configure(root_path: String = DEFAULT_ROOT) -> void:
    if root_path.begins_with("res://artifacts/godot-live-editor/"):
        _root_path = root_path.trim_suffix("/")
    else:
        _root_path = DEFAULT_ROOT


func record_started(
    envelope: Dictionary,
    observation: Dictionary,
) -> Dictionary:
    var operation_id := str(envelope.get("operation_id", ""))
    if not _safe_name(operation_id):
        return {"ok": false, "code": "OPERATION_ID_INVALID"}
    var request_hash := str(envelope.get("request_hash", ""))
    var existing := read_record(operation_id)
    if not existing.is_empty():
        if existing.get("state") == "COMPLETED" and existing.get("request_hash") == request_hash:
            return {
                "ok": true,
                "code": "IDEMPOTENT_REPLAY",
                "replay": true,
                "record": existing,
            }
        return {"ok": false, "code": "LEDGER_CONFLICT"}

    var payload := {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "state": "STARTED",
        "observation": observation.duplicate(true),
        "result": null,
        "updated_at": _rfc3339_now(),
    }
    var write_result := _write_record(operation_id, payload)
    if not write_result.get("ok", false):
        return write_result
    return {"ok": true, "code": "STARTED", "replay": false, "record": payload}


func record_terminal(
    operation_id: String,
    state: String,
    result: Dictionary,
) -> Dictionary:
    if not TERMINAL_STATES.has(state):
        return {"ok": false, "code": "LEDGER_STATE_INVALID"}
    var existing := read_record(operation_id)
    if existing.get("state") != "STARTED":
        return {"ok": false, "code": "LEDGER_STATE_INVALID"}
    existing["state"] = state
    existing["result"] = result.duplicate(true)
    existing["updated_at"] = _rfc3339_now()
    var write_result := _write_record(operation_id, existing)
    if not write_result.get("ok", false):
        return write_result
    return {"ok": true, "code": state, "record": existing}


func read_record(operation_id: String) -> Dictionary:
    if not _safe_name(operation_id):
        return {}
    var file := FileAccess.open(
        ProjectSettings.globalize_path(_record_path(operation_id)),
        FileAccess.READ,
    )
    if file == null:
        return {}
    var parsed = JSON.parse_string(file.get_as_text())
    return parsed if parsed is Dictionary else {}


func _write_record(operation_id: String, payload: Dictionary) -> Dictionary:
    if not _safe_name(operation_id):
        return {"ok": false, "code": "OPERATION_ID_INVALID"}
    var target_path := ProjectSettings.globalize_path(_record_path(operation_id))
    var temp_path := target_path + ".tmp"
    if DirAccess.make_dir_recursive_absolute(target_path.get_base_dir()) != OK:
        return {"ok": false, "code": "LEDGER_WRITE_FAILED"}
    var file := FileAccess.open(temp_path, FileAccess.WRITE)
    if file == null:
        return {"ok": false, "code": "LEDGER_WRITE_FAILED"}
    file.store_string(JSON.stringify(payload) + "\n")
    file.flush()
    file.close()
    if DirAccess.rename_absolute(temp_path, target_path) != OK:
        DirAccess.remove_absolute(temp_path)
        return {"ok": false, "code": "LEDGER_WRITE_FAILED"}
    return {"ok": true, "code": "LEDGER_WRITTEN"}


func _record_path(operation_id: String) -> String:
    return "%s/%s.json" % [_root_path, operation_id]


func _rfc3339_now() -> String:
    return Time.get_datetime_string_from_system(true, false) + "Z"


func _safe_name(value: String) -> bool:
    if value.is_empty() or value.length() > MAX_SAFE_NAME_LENGTH:
        return false
    for character in value:
        if not SAFE_NAME_CHARACTERS.contains(character):
            return false
    return true
