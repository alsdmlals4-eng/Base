@tool
extends RefCounted

var _pending: Dictionary = {}
var _ttl_seconds := 60


func configure(ttl_seconds: int) -> void:
    _ttl_seconds = clampi(ttl_seconds, 1, 600)
    _pending.clear()


func store_pending(
    operation_id: String,
    request_hash: String,
    request: Dictionary,
) -> Dictionary:
    expire_stale()
    if operation_id.is_empty() or _pending.has(operation_id):
        return {"ok": false, "code": "OPERATION_ID_CONFLICT"}
    _pending[operation_id] = {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "request": request.duplicate(true),
        "state": "PENDING_APPROVAL",
        "created_unix": Time.get_unix_time_from_system(),
        "expires_unix": Time.get_unix_time_from_system() + _ttl_seconds,
        "human_approved": false,
    }
    return {"ok": true, "code": "APPROVAL_REQUIRED"}


func status(operation_id: String) -> Dictionary:
    expire_stale()
    if not _pending.has(operation_id):
        return {"success": false, "code": "OPERATION_NOT_FOUND", "data": {}}
    var record: Dictionary = _pending[operation_id]
    return {
        "success": true,
        "code": "OK",
        "data": {
            "operation_id": operation_id,
            "state": record.get("state"),
            "request_hash": record.get("request_hash"),
        },
    }


func pending_records() -> Array[Dictionary]:
    expire_stale()
    var result: Array[Dictionary] = []
    for value in _pending.values():
        var record: Dictionary = value
        if record.get("state") == "PENDING_APPROVAL":
            result.append(record.duplicate(true))
    return result


func human_approved(operation_id: String) -> Dictionary:
    expire_stale()
    if not _pending.has(operation_id):
        return {"ok": false, "code": "OPERATION_NOT_FOUND"}
    var record: Dictionary = _pending[operation_id]
    if record.get("state") != "PENDING_APPROVAL":
        return {"ok": false, "code": "APPROVAL_STATE_INVALID"}
    record["human_approved"] = true
    record["state"] = "APPROVED_BY_HUMAN"
    _pending[operation_id] = record
    return {"ok": true, "record": record.duplicate(true)}


func human_rejected(operation_id: String) -> Dictionary:
    expire_stale()
    if not _pending.has(operation_id):
        return {"ok": false, "code": "OPERATION_NOT_FOUND"}
    var record: Dictionary = _pending[operation_id]
    record["state"] = "REJECTED_BY_HUMAN"
    _pending[operation_id] = record
    return {"ok": true}


func take_approved(operation_id: String) -> Dictionary:
    if not _pending.has(operation_id):
        return {}
    var record: Dictionary = _pending[operation_id]
    if record.get("state") != "APPROVED_BY_HUMAN" or record.get("human_approved") != true:
        return {}
    _pending.erase(operation_id)
    return record


func expire_stale() -> void:
    var now := Time.get_unix_time_from_system()
    for operation_id in _pending.keys():
        var record: Dictionary = _pending[operation_id]
        if float(record.get("expires_unix", 0.0)) <= now:
            record["state"] = "APPROVAL_EXPIRED"
            _pending[operation_id] = record


func clear() -> void:
    _pending.clear()
