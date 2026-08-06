@tool
extends VBoxContainer

var _store
var _on_approved := Callable()
var _on_rejected := Callable()
var _list := VBoxContainer.new()


func _ready() -> void:
    name = "Base Godot MCP Approvals"
    var heading := Label.new()
    heading.text = "Godot MCP pending approvals"
    add_child(heading)
    add_child(_list)


func configure(store, on_approved: Callable, on_rejected: Callable) -> void:
    _store = store
    _on_approved = on_approved
    _on_rejected = on_rejected
    refresh()


func refresh() -> void:
    if _list == null:
        return
    for child in _list.get_children():
        child.queue_free()
    if _store == null:
        return
    for record in _store.pending_records():
        var operation_id := str(record.get("operation_id", ""))
        var row := HBoxContainer.new()
        var label := Label.new()
        label.text = "%s — node.rename" % operation_id
        row.add_child(label)
        var allow := Button.new()
        allow.text = "Approve"
        allow.pressed.connect(_approve.bind(operation_id))
        row.add_child(allow)
        var reject := Button.new()
        reject.text = "Reject"
        reject.pressed.connect(_reject.bind(operation_id))
        row.add_child(reject)
        _list.add_child(row)


func _approve(operation_id: String) -> void:
    if _store == null:
        return
    var result: Dictionary = _store.human_approved(operation_id)
    if result.get("ok", false) and _on_approved.is_valid():
        _on_approved.call(operation_id)
    refresh()


func _reject(operation_id: String) -> void:
    if _store == null:
        return
    var result: Dictionary = _store.human_rejected(operation_id)
    if result.get("ok", false) and _on_rejected.is_valid():
        _on_rejected.call(operation_id)
    refresh()
