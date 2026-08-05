@tool
extends RefCounted

const MAX_PENDING := 64

var _items: Array[Dictionary] = []
var _operation_ids: Dictionary = {}


func enqueue(envelope: Dictionary) -> Dictionary:
    var operation_id := str(envelope.get("operation_id", ""))
    if operation_id.is_empty():
        return {"ok": false, "code": "OPERATION_ID_REQUIRED"}
    if _operation_ids.has(operation_id):
        return {"ok": false, "code": "DUPLICATE_OPERATION_ID"}
    if _items.size() >= MAX_PENDING:
        return {"ok": false, "code": "QUEUE_FULL"}
    _items.push_back(envelope.duplicate(true))
    _operation_ids[operation_id] = true
    return {"ok": true, "code": "QUEUED"}


func pop_next() -> Dictionary:
    if _items.is_empty():
        return {}
    var envelope: Dictionary = _items.pop_front()
    _operation_ids.erase(str(envelope.get("operation_id", "")))
    return envelope


func size() -> int:
    return _items.size()


func clear() -> void:
    _items.clear()
    _operation_ids.clear()
