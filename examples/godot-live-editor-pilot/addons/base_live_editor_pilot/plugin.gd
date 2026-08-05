@tool
extends EditorPlugin

const MARKER_PATH := "res://artifacts/editor_plugin_loaded.json"

func _enter_tree() -> void:
    DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://artifacts"))
    var file := FileAccess.open(MARKER_PATH, FileAccess.WRITE)
    if file == null:
        push_error("BASE_GODOT_PILOT_PLUGIN_MARKER_WRITE_FAILED")
        return
    var marker := {
        "plugin_id": "base_live_editor_pilot",
        "state": "LOADED",
        "network_listener_enabled": false,
        "engine_version": Engine.get_version_info().get("string", ""),
        "project_path": "examples/godot-live-editor-pilot",
    }
    file.store_string(JSON.stringify(marker, "  ") + "\n")
    print("BASE_GODOT_PILOT_PLUGIN=LOADED")

func _exit_tree() -> void:
    print("BASE_GODOT_PILOT_PLUGIN=UNLOADED")
