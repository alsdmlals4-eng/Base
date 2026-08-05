@tool
extends RefCounted

const INSPECT_CAPABILITY := "scene.inspect"
const RENAME_CAPABILITY := "node.rename"
const SAVE_MODES := ["KEEP_DIRTY", "SAVE_CURRENT_SCENE"]
const INVALID_NAME_CHARACTERS := [".", ":", "@", "/", "\"", "%"]


func validate_arguments(
    capability_id: String,
    arguments: Dictionary,
) -> PackedStringArray:
    match capability_id:
        INSPECT_CAPABILITY:
            if not arguments.is_empty():
                return PackedStringArray(["ARGUMENT_SCHEMA_INVALID"])
            return PackedStringArray()
        RENAME_CAPABILITY:
            return _validate_rename_arguments(arguments)
        _:
            return PackedStringArray(["UNKNOWN_CAPABILITY"])


func validate_output(
    capability_id: String,
    output: Dictionary,
) -> PackedStringArray:
    var expected := PackedStringArray()
    match capability_id:
        INSPECT_CAPABILITY:
            expected = PackedStringArray([
                "scene_path",
                "root_name",
                "child_count",
                "dirty_state",
                "target_revision",
                "target_content_sha256",
            ])
        RENAME_CAPABILITY:
            expected = PackedStringArray([
                "scene_path",
                "node_path",
                "old_name",
                "new_name",
                "save_mode",
                "dirty_state",
                "saved_scene_sha256",
            ])
        _:
            return PackedStringArray(["UNKNOWN_CAPABILITY"])

    if output.size() != expected.size():
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    for key in expected:
        if not output.has(key):
            return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    return PackedStringArray()


func inspect_scene(
    editor_interface: EditorInterface,
    observation: Dictionary,
) -> Dictionary:
    var root := editor_interface.get_edited_scene_root()
    if root == null:
        return {"error": "EDITED_SCENE_REQUIRED"}
    return {
        "scene_path": observation.get("scene_path"),
        "root_name": str(root.name),
        "child_count": root.get_child_count(),
        "dirty_state": observation.get("dirty_state"),
        "target_revision": observation.get("target_revision"),
        "target_content_sha256": observation.get("target_content_sha256"),
    }


func resolve_rename_target(
    scene_root: Node,
    arguments: Dictionary,
) -> Dictionary:
    var errors := _validate_rename_arguments(arguments)
    if not errors.is_empty():
        return {"error": errors[0]}
    var node_path := NodePath(str(arguments["node_path"]))
    var target := scene_root.get_node_or_null(node_path)
    if target == null:
        return {"error": "TARGET_NODE_NOT_FOUND"}
    if target != scene_root and not scene_root.is_ancestor_of(target):
        return {"error": "NODE_OUTSIDE_EDITED_SCENE"}
    return {"target": target, "node_path": node_path}


func _validate_rename_arguments(arguments: Dictionary) -> PackedStringArray:
    var expected := ["node_path", "new_name", "save_mode"]
    if arguments.size() != expected.size():
        return PackedStringArray(["ARGUMENT_SCHEMA_INVALID"])
    for key in expected:
        if not arguments.has(key):
            return PackedStringArray(["ARGUMENT_SCHEMA_INVALID"])

    var raw_path := str(arguments["node_path"])
    var node_path := NodePath(raw_path)
    if raw_path.is_empty():
        return PackedStringArray(["NODE_PATH_REQUIRED"])
    if node_path.is_absolute():
        return PackedStringArray(["ABSOLUTE_NODE_PATH_FORBIDDEN"])
    for segment in raw_path.split("/", false):
        if segment == "..":
            return PackedStringArray(["NODE_PATH_ESCAPE_FORBIDDEN"])

    var new_name := str(arguments["new_name"])
    if new_name.is_empty() or new_name.length() > 128:
        return PackedStringArray(["INVALID_NODE_NAME"])
    for character in INVALID_NAME_CHARACTERS:
        if new_name.contains(character):
            return PackedStringArray(["INVALID_NODE_NAME"])
    if not SAVE_MODES.has(str(arguments["save_mode"])):
        return PackedStringArray(["SAVE_MODE_INVALID"])
    return PackedStringArray()
