@tool
extends RefCounted

const INSPECT_CAPABILITY := "scene.inspect"
const RENAME_CAPABILITY := "node.rename"
const SAVE_MODES := ["KEEP_DIRTY", "SAVE_CURRENT_SCENE"]
const INVALID_NAME_CHARACTERS := [".", ":", "@", "/", "\"", "%"]
const DIRTY_STATES := ["CLEAN", "DIRTY"]


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
    match capability_id:
        INSPECT_CAPABILITY:
            return _validate_inspect_output(output)
        RENAME_CAPABILITY:
            return _validate_rename_output(output)
        _:
            return PackedStringArray(["UNKNOWN_CAPABILITY"])


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


func _validate_inspect_output(output: Dictionary) -> PackedStringArray:
    var expected := [
        "scene_path",
        "root_name",
        "child_count",
        "dirty_state",
        "target_revision",
        "target_content_sha256",
    ]
    if not _has_exact_keys(output, expected):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if typeof(output["scene_path"]) != TYPE_STRING or not str(output["scene_path"]).begins_with("res://"):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if typeof(output["root_name"]) != TYPE_STRING or str(output["root_name"]).is_empty():
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if typeof(output["child_count"]) != TYPE_INT or int(output["child_count"]) < 0:
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if not DIRTY_STATES.has(str(output["dirty_state"])):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if typeof(output["target_revision"]) != TYPE_STRING or str(output["target_revision"]).is_empty():
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if not _is_sha256_or_null(output["target_content_sha256"]):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    return PackedStringArray()


func _validate_rename_output(output: Dictionary) -> PackedStringArray:
    var expected := [
        "scene_path",
        "node_path",
        "old_name",
        "new_name",
        "save_mode",
        "dirty_state",
        "saved_scene_sha256",
    ]
    if not _has_exact_keys(output, expected):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    for key in ["scene_path", "node_path", "old_name", "new_name", "save_mode", "dirty_state"]:
        if typeof(output[key]) != TYPE_STRING or str(output[key]).is_empty():
            return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if not str(output["scene_path"]).begins_with("res://"):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    var save_mode := str(output["save_mode"])
    if not SAVE_MODES.has(save_mode):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    if save_mode == "KEEP_DIRTY":
        if output["dirty_state"] != "DIRTY" or output["saved_scene_sha256"] != null:
            return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    elif output["dirty_state"] != "CLEAN" or not _is_sha256(output["saved_scene_sha256"]):
        return PackedStringArray(["OUTPUT_SCHEMA_INVALID"])
    return PackedStringArray()


func _has_exact_keys(value: Dictionary, expected: Array) -> bool:
    if value.size() != expected.size():
        return false
    for key in expected:
        if not value.has(key):
            return false
    return true


func _is_sha256_or_null(value: Variant) -> bool:
    return value == null or _is_sha256(value)


func _is_sha256(value: Variant) -> bool:
    return (
        typeof(value) == TYPE_STRING
        and str(value).length() == 64
        and str(value).is_valid_hex_number(false)
    )
