@tool
extends RefCounted

const CONFIG_ENV := "BASE_GODOT_MCP_CONFIG_DIR"
const AUTHORIZED_PROFILE_IDS := ["codex", "gpt-vscode"]
const DENIED_PROFILE_ID := "deepseek"
const ALLOWED_CAPABILITIES := [
    "editor.status",
    "capabilities.list",
    "scene.inspect",
    "node.rename",
    "task.status",
]

var _config_root := ""
var _project_root := ""


func configure(project_root: String) -> Dictionary:
    _project_root = project_root.simplify_path()
    var resolved := resolve_config_root()
    if not resolved.get("ok", false):
        return resolved
    _config_root = str(resolved["path"])
    return {"ok": true, "path": _config_root}


func config_root() -> String:
    return _config_root


func resolve_config_root() -> Dictionary:
    var requested := OS.get_environment(CONFIG_ENV).strip_edges()
    if requested.is_empty():
        requested = _platform_default_root()
    if requested.begins_with("res://") or requested.begins_with("user://"):
        return {"ok": false, "code": "CONFIG_ROOT_PROJECT_LOCAL_FORBIDDEN"}
    var absolute := requested.simplify_path()
    if not absolute.is_absolute_path():
        return {"ok": false, "code": "CONFIG_ROOT_ABSOLUTE_REQUIRED"}
    if _is_nested(absolute, _project_root):
        return {"ok": false, "code": "CONFIG_ROOT_PROJECT_LOCAL_FORBIDDEN"}
    if DirAccess.make_dir_recursive_absolute(absolute) != OK:
        return {"ok": false, "code": "CONFIG_ROOT_CREATE_FAILED"}
    return {"ok": true, "path": absolute}


func load_profile(profile_id: String, project_fingerprint: String) -> Dictionary:
    if profile_id == DENIED_PROFILE_ID or not AUTHORIZED_PROFILE_IDS.has(profile_id):
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_DENIED"}
    if _config_root.is_empty():
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_REQUIRED"}
    var path := _config_root.path_join("%s.json" % profile_id)
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_REQUIRED"}
    var parsed = JSON.parse_string(file.get_as_text())
    if not (parsed is Dictionary):
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_INVALID"}
    var profile: Dictionary = parsed
    if profile.get("schema_version") != 1:
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_INVALID"}
    if profile.get("profile_id") != profile_id or profile.get("enabled") != true:
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_DISABLED"}
    var secret := str(profile.get("credential_secret", ""))
    if secret.length() < 32 or secret.length() > 512:
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_INVALID"}
    var projects: Array = profile.get("allowed_project_fingerprints", [])
    if not projects.has(project_fingerprint):
        return {"ok": false, "code": "MCP_PROJECT_NOT_AUTHORIZED"}
    var capabilities: Array = profile.get("allowed_capabilities", [])
    if capabilities.is_empty():
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_INVALID"}
    for capability in capabilities:
        if not ALLOWED_CAPABILITIES.has(str(capability)):
            return {"ok": false, "code": "MCP_CLIENT_PROFILE_INVALID"}
    var expires_at := str(profile.get("expires_at", ""))
    if not expires_at.is_empty() and _expired(expires_at):
        return {"ok": false, "code": "MCP_CLIENT_PROFILE_EXPIRED"}
    return {
        "ok": true,
        "profile_id": profile_id,
        "credential_secret": secret,
        "allowed_capabilities": capabilities.duplicate(),
    }


func _platform_default_root() -> String:
    var home := OS.get_environment("HOME")
    match OS.get_name():
        "Windows":
            var local_app_data := OS.get_environment("LOCALAPPDATA")
            return local_app_data.path_join("BaseGodotMcp")
        "macOS":
            return home.path_join("Library/Application Support/BaseGodotMcp")
        _:
            var xdg := OS.get_environment("XDG_CONFIG_HOME")
            if xdg.is_empty():
                xdg = home.path_join(".config")
            return xdg.path_join("base-godot-mcp")


func _is_nested(candidate: String, root: String) -> bool:
    var normalized_candidate := candidate.trim_suffix("/") + "/"
    var normalized_root := root.trim_suffix("/") + "/"
    return normalized_candidate.begins_with(normalized_root)


func _expired(value: String) -> bool:
    if not value.ends_with("Z"):
        return true
    var normalized := value.trim_suffix("Z")
    var unix := Time.get_unix_time_from_datetime_string(normalized)
    return unix <= 0 or unix <= Time.get_unix_time_from_system()
