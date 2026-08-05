@tool
extends EditorPlugin

const RequestQueue = preload("request_queue.gd")
const RuntimeContractGuard = preload("runtime_contract_guard.gd")
const EditorStateProbe = preload("editor_state_probe.gd")
const CapabilityRegistry = preload("capability_registry.gd")
const OperationLedger = preload("operation_ledger.gd")
const EvidenceWriter = preload("evidence_writer.gd")
const EditorTransactionExecutor = preload("editor_transaction_executor.gd")
const MANIFEST_PATH := "res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
const MAX_COMPLETED_RESULTS := 64
const IN_PROCESS_ENDPOINT := "in-process-editor-plugin"

var network_listener_enabled := false
var _available := false
var _unavailable_code := "ADAPTER_NOT_CONFIGURED"
var _editor_instance_id := ""
var _queue
var _guard
var _probe
var _registry
var _ledger
var _evidence
var _executor
var _completed_results: Dictionary = {}
var _completed_order: Array[String] = []


func _enter_tree() -> void:
    set_process(false)
    var manifest := _load_manifest()
    if manifest.is_empty() or not _manifest_is_usable(manifest):
        _unavailable_code = "ADAPTER_NOT_CONFIGURED"
        return

    _editor_instance_id = _new_instance_id()
    if _editor_instance_id.is_empty():
        _unavailable_code = "EDITOR_INSTANCE_ID_FAILED"
        return

    _queue = RequestQueue.new()
    _guard = RuntimeContractGuard.new()
    _probe = EditorStateProbe.new()
    _registry = CapabilityRegistry.new()
    _ledger = OperationLedger.new()
    _evidence = EvidenceWriter.new()
    _executor = EditorTransactionExecutor.new()

    var project_identity: Dictionary = manifest.get("project_identity", {})
    _guard.configure(
        manifest,
        str(project_identity.get("project_fingerprint", "")),
        _editor_instance_id,
    )
    _ledger.configure()
    _evidence.configure()
    _executor.configure(
        get_editor_interface(),
        get_undo_redo(),
        _guard,
        _registry,
        _probe,
        _ledger,
        _evidence,
    )
    _available = true
    _unavailable_code = "OK"
    set_process(true)


func submit_validated_operation(envelope: Dictionary) -> Dictionary:
    if not _available:
        return {"ok": false, "code": "ADAPTER_NOT_CONFIGURED"}
    var errors: PackedStringArray = _guard.validate_for_enqueue(envelope)
    if not errors.is_empty():
        return {"ok": false, "code": str(errors[0])}
    return _queue.enqueue(envelope)


func take_completed_result(operation_id: String) -> Dictionary:
    if not _completed_results.has(operation_id):
        return {}
    var result: Dictionary = _completed_results[operation_id]
    _completed_results.erase(operation_id)
    _completed_order.erase(operation_id)
    return result


func editor_instance_id() -> String:
    return _editor_instance_id


func availability() -> Dictionary:
    return {
        "available": _available,
        "code": _unavailable_code,
        "network_listener_enabled": network_listener_enabled,
        "editor_instance_id": _editor_instance_id if _available else null,
    }


func _process(_delta: float) -> void:
    if not _available or _queue.size() == 0:
        return
    var envelope: Dictionary = _queue.pop_next()
    var operation_id := str(envelope.get("operation_id", ""))
    var result: Dictionary = _executor.execute(envelope)
    _store_result(operation_id, result)


func _exit_tree() -> void:
    set_process(false)
    _available = false
    _editor_instance_id = ""
    if _queue != null:
        _queue.clear()
    _completed_results.clear()
    _completed_order.clear()
    _executor = null
    _evidence = null
    _ledger = null
    _registry = null
    _probe = null
    _guard = null
    _queue = null


func _load_manifest() -> Dictionary:
    var file := FileAccess.open(MANIFEST_PATH, FileAccess.READ)
    if file == null:
        return {}
    var parsed = JSON.parse_string(file.get_as_text())
    return parsed if parsed is Dictionary else {}


func _manifest_is_usable(manifest: Dictionary) -> bool:
    if manifest.get("schema_version") != 2:
        return false
    if manifest.get("configuration_state") != "CONFIGURED":
        return false
    var transport: Dictionary = manifest.get("transport", {})
    if transport.get("kind") != "PROJECT_DEFINED":
        return false
    if transport.get("enabled") != true:
        return false
    if transport.get("bind_host") != null:
        return false
    if transport.get("endpoint_identity") != IN_PROCESS_ENDPOINT:
        return false
    var access: Dictionary = transport.get("access_control", {})
    if access.get("authentication_mode") != "NOT_APPLICABLE":
        return false
    if access.get("origin_policy") != "NOT_APPLICABLE":
        return false
    if access.get("session_binding") != "NOT_APPLICABLE":
        return false
    if access.get("os_access_control") != "CURRENT_USER_ONLY":
        return false
    var project_identity: Dictionary = manifest.get("project_identity", {})
    if str(project_identity.get("project_fingerprint", "")).is_empty():
        return false
    var capabilities: Array = manifest.get("capabilities", [])
    return not capabilities.is_empty()


func _new_instance_id() -> String:
    var bytes := Crypto.new().generate_random_bytes(16)
    if bytes.size() != 16:
        return ""
    return "editor-%s" % bytes.hex_encode()


func _store_result(operation_id: String, result: Dictionary) -> void:
    if operation_id.is_empty():
        return
    if not _completed_results.has(operation_id):
        _completed_order.append(operation_id)
    _completed_results[operation_id] = result.duplicate(true)
    while _completed_order.size() > MAX_COMPLETED_RESULTS:
        var oldest := _completed_order.pop_front()
        _completed_results.erase(oldest)
