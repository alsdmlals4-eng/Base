@tool
extends RefCounted


func observe(
    editor_interface: EditorInterface,
    undo_redo: EditorUndoRedoManager,
    target_path: NodePath,
) -> Dictionary:
    var root := editor_interface.get_edited_scene_root()
    if root == null:
        return {"error": "EDITED_SCENE_REQUIRED"}

    var target: Node = root
    if not target_path.is_empty() and target_path != NodePath("."):
        target = root.get_node_or_null(target_path)
    if target == null:
        return {"error": "TARGET_NODE_NOT_FOUND"}
    if target != root and not root.is_ancestor_of(target):
        return {"error": "NODE_OUTSIDE_EDITED_SCENE"}

    var scene_path := str(root.scene_file_path)
    var unsaved_scenes := EditorInterface.get_unsaved_scenes()
    var history_id := undo_redo.get_object_history_id(root)
    var history := undo_redo.get_history_undo_redo(history_id)
    var version := -1
    if history != null:
        version = history.get_version()

    return {
        "scene_path": scene_path,
        "dirty_state": "DIRTY" if unsaved_scenes.has(scene_path) else "CLEAN",
        "target_content_sha256": _sha256_file(scene_path),
        "target_revision": "%s:%s" % [history_id, version],
        "target_node": target,
    }


func _sha256_file(res_path: String) -> Variant:
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
