@tool
extends RefCounted

const DEFAULT_ROOT := "res://artifacts/godot-live-editor/evidence"
const SAFE_NAME_CHARACTERS := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
const MAX_SAFE_NAME_LENGTH := 128

var _root_path := DEFAULT_ROOT


func configure(root_path: String = DEFAULT_ROOT) -> void:
    if root_path.begins_with("res://artifacts/godot-live-editor/"):
        _root_path = root_path.trim_suffix("/")
    else:
        _root_path = DEFAULT_ROOT


func write_json(name: String, payload: Dictionary) -> Dictionary:
    if not _safe_name(name):
        return {"ok": false, "code": "EVIDENCE_PATH_INVALID"}
    var res_path := "%s/%s.json" % [_root_path, name]
    var target_path := ProjectSettings.globalize_path(res_path)
    var temp_path := target_path + ".tmp"
    if DirAccess.make_dir_recursive_absolute(target_path.get_base_dir()) != OK:
        return {"ok": false, "code": "EVIDENCE_WRITE_FAILED"}
    var file := FileAccess.open(temp_path, FileAccess.WRITE)
    if file == null:
        return {"ok": false, "code": "EVIDENCE_WRITE_FAILED"}
    file.store_string(JSON.stringify(payload) + "\n")
    file.flush()
    file.close()
    if DirAccess.rename_absolute(temp_path, target_path) != OK:
        DirAccess.remove_absolute(temp_path)
        return {"ok": false, "code": "EVIDENCE_WRITE_FAILED"}
    var artifact_hash = sha256_file(res_path)
    if artifact_hash == null:
        return {"ok": false, "code": "EVIDENCE_HASH_FAILED"}
    return {
        "ok": true,
        "code": "EVIDENCE_WRITTEN",
        "path": res_path.trim_prefix("res://"),
        "artifact_sha256": artifact_hash,
    }


func sha256_file(res_path: String) -> Variant:
    if res_path.is_empty() or not res_path.begins_with("res://"):
        return null
    var absolute_path := ProjectSettings.globalize_path(res_path)
    var file := FileAccess.open(absolute_path, FileAccess.READ)
    if file == null:
        return null
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return null
    while file.get_position() < file.get_length():
        var remaining := file.get_length() - file.get_position()
        context.update(file.get_buffer(mini(65536, remaining)))
    return context.finish().hex_encode()


func _safe_name(value: String) -> bool:
    if value.is_empty() or value.length() > MAX_SAFE_NAME_LENGTH:
        return false
    for character in value:
        if not SAFE_NAME_CHARACTERS.contains(character):
            return false
    return true
