@tool
extends RefCounted

const PROTOCOL := "BASE_GODOT_BRIDGE_V1"
const CONFIG_ENV := "BASE_GODOT_MCP_CONFIG_DIR"

var _config_root := ""
var _project_root := ""
var _descriptor_path := ""


func configure(config_root: String, project_root: String) -> Dictionary:
    if config_root.begins_with("res://") or config_root.begins_with("user://"):
        return {"ok": false, "code": "CONFIG_ROOT_PROJECT_LOCAL_FORBIDDEN"}
    _config_root = config_root.simplify_path()
    _project_root = project_root.simplify_path()
    if _config_root.trim_suffix("/").begins_with(_project_root.trim_suffix("/") + "/"):
        return {"ok": false, "code": "CONFIG_ROOT_PROJECT_LOCAL_FORBIDDEN"}
    var bridge_root := _config_root.path_join("bridges")
    if DirAccess.make_dir_recursive_absolute(bridge_root) != OK:
        return {"ok": false, "code": "BRIDGE_DESCRIPTOR_ROOT_FAILED"}
    return {"ok": true}


func create_descriptor(
    profile_id: String,
    project_fingerprint: String,
    bridge_instance_id: String,
    port: int,
    ttl_seconds: int,
) -> Dictionary:
    if _config_root.is_empty() or port <= 0 or ttl_seconds <= 0:
        return {"ok": false, "code": "BRIDGE_DESCRIPTOR_INVALID"}
    var nonce_bytes := Crypto.new().generate_random_bytes(32)
    if nonce_bytes.size() != 32:
        return {"ok": false, "code": "BRIDGE_DESCRIPTOR_NONCE_FAILED"}
    var expires_unix := int(Time.get_unix_time_from_system()) + ttl_seconds
    var expires_at := Time.get_datetime_string_from_unix_time(expires_unix, true) + "Z"
    var payload := {
        "schema_version": 1,
        "protocol": PROTOCOL,
        "host": "127.0.0.1",
        "port": port,
        "bridge_instance_id": bridge_instance_id,
        "descriptor_nonce": nonce_bytes.hex_encode(),
        "profile_id": profile_id,
        "project_fingerprint": project_fingerprint,
        "expires_at": expires_at,
    }
    var name := "%s-%s.json" % [project_fingerprint, bridge_instance_id]
    var destination := _config_root.path_join("bridges").path_join(name)
    var temporary := "%s.tmp" % destination
    var file := FileAccess.open(temporary, FileAccess.WRITE)
    if file == null:
        return {"ok": false, "code": "BRIDGE_DESCRIPTOR_WRITE_FAILED"}
    file.store_string(JSON.stringify(payload, "  ") + "\n")
    file.flush()
    file.close()
    if FileAccess.file_exists(destination):
        DirAccess.remove_absolute(destination)
    if DirAccess.rename_absolute(temporary, destination) != OK:
        DirAccess.remove_absolute(temporary)
        return {"ok": false, "code": "BRIDGE_DESCRIPTOR_WRITE_FAILED"}
    _descriptor_path = destination
    return {"ok": true, "path": destination, "descriptor": payload}


func descriptor_path() -> String:
    return _descriptor_path


func cleanup() -> void:
    if not _descriptor_path.is_empty() and FileAccess.file_exists(_descriptor_path):
        DirAccess.remove_absolute(_descriptor_path)
    _descriptor_path = ""
