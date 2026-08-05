@tool
extends RefCounted

var _manifest: Dictionary = {}
var _project_fingerprint := ""
var _editor_instance_id := ""
var _capabilities_by_id: Dictionary = {}


func configure(
    manifest: Dictionary,
    project_fingerprint: String,
    editor_instance_id: String,
) -> void:
    _manifest = manifest.duplicate(true)
    _project_fingerprint = project_fingerprint
    _editor_instance_id = editor_instance_id
    _capabilities_by_id.clear()
    for value in _manifest.get("capabilities", []):
        if value is Dictionary:
            var capability: Dictionary = value
            var capability_id := str(capability.get("capability_id", ""))
            if not capability_id.is_empty():
                _capabilities_by_id[capability_id] = capability


func validate_for_enqueue(envelope: Dictionary) -> PackedStringArray:
    var errors := PackedStringArray()
    if _manifest.get("configuration_state") != "CONFIGURED":
        _append_unique(errors, "ADAPTER_NOT_CONFIGURED")
        return errors
    if envelope.get("schema_version") != 2:
        _append_unique(errors, "SCHEMA_VERSION_UNSUPPORTED")
    if envelope.get("artifact_role") != "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE":
        _append_unique(errors, "ARTIFACT_ROLE_INVALID")

    var project_identity: Dictionary = envelope.get("project_identity", {})
    if str(project_identity.get("project_fingerprint", "")) != _project_fingerprint:
        _append_unique(errors, "PROJECT_IDENTITY_MISMATCH")
    if project_identity != _manifest.get("project_identity", {}):
        _append_unique(errors, "PROJECT_IDENTITY_MISMATCH")

    var instance_identity: Dictionary = envelope.get("instance_identity", {})
    if str(instance_identity.get("automation_service_instance_id", "")).is_empty():
        _append_unique(errors, "AUTOMATION_SERVICE_INSTANCE_REQUIRED")
    if str(instance_identity.get("editor_instance_id", "")) != _editor_instance_id:
        _append_unique(errors, "EDITOR_INSTANCE_MISMATCH")
    if instance_identity.get("runtime_session_state") != "NOT_APPLICABLE":
        _append_unique(errors, "RUNTIME_SESSION_NOT_APPLICABLE")

    var capability_id := str(envelope.get("capability_id", ""))
    if not _capabilities_by_id.has(capability_id):
        _append_unique(errors, "UNKNOWN_CAPABILITY")
        return errors
    var capability: Dictionary = _capabilities_by_id[capability_id]
    if capability.get("execution_path") != "EDITOR_PLUGIN":
        _append_unique(errors, "EXECUTION_PATH_MISMATCH")

    if envelope.get("contract_snapshot", {}) != _contract_snapshot(capability):
        _append_unique(errors, "CONTRACT_SNAPSHOT_MISMATCH")
    if envelope.get("policy", {}) != _policy_snapshot(capability):
        _append_unique(errors, "POLICY_MISMATCH")

    var request_hash := str(envelope.get("request_hash", ""))
    if request_hash.length() != 64 or not request_hash.is_valid_hex_number(false):
        _append_unique(errors, "REQUEST_HASH_REQUIRED")

    var approval: Dictionary = envelope.get("approval", {})
    if capability.get("approval_policy") == "REQUIRED":
        if approval.get("state") != "APPROVED":
            _append_unique(errors, "APPROVAL_REQUIRED")
        elif approval.get("consumed_by_operation_id") != envelope.get("operation_id"):
            _append_unique(errors, "APPROVAL_BINDING_MISMATCH")
    elif approval.get("state") != "NOT_REQUIRED":
        _append_unique(errors, "APPROVAL_STATE_INVALID")

    var preconditions: Dictionary = envelope.get("preconditions", {})
    if preconditions.get("conflict_policy") != "FAIL_CLOSED":
        _append_unique(errors, "PRECONDITION_POLICY_INVALID")
    return errors


func validate_before_execute(
    envelope: Dictionary,
    observation: Dictionary,
) -> PackedStringArray:
    var errors := validate_for_enqueue(envelope)
    var preconditions: Dictionary = envelope.get("preconditions", {})
    var pairs := [
        ["expected_target_revision", observation.get("target_revision")],
        ["expected_target_content_sha256", observation.get("target_content_sha256")],
        ["expected_dirty_state", observation.get("dirty_state")],
        ["expected_scene_path", observation.get("scene_path")],
    ]
    for pair in pairs:
        if preconditions.get(pair[0]) != pair[1]:
            _append_unique(errors, "TARGET_STATE_CONFLICT")
            break
    return errors


func _contract_snapshot(capability: Dictionary) -> Dictionary:
    return {
        "contract_version": _manifest.get("contract_version"),
        "adapter_version": _manifest.get("adapter_version"),
        "catalog_sha256": _manifest.get("catalog", {}).get("sha256"),
        "capability_input_schema_sha256": capability.get("input_schema_sha256"),
        "capability_output_schema_sha256": capability.get("output_schema_sha256"),
        "protocol_profile": _manifest.get("transport", {}).get("protocol_profile"),
        "protocol_version": _manifest.get("transport", {}).get("protocol_version"),
    }


func _policy_snapshot(capability: Dictionary) -> Dictionary:
    return {
        "effect_kind": capability.get("effect_kind"),
        "idempotency": capability.get("idempotency"),
        "approval_policy": capability.get("approval_policy"),
        "execution_mode": capability.get("execution_mode"),
        "rollback_policy": capability.get("rollback_policy"),
    }


func _append_unique(errors: PackedStringArray, code: String) -> void:
    if not errors.has(code):
        errors.append(code)
