extends SceneTree

const RESULT_PREFIX := "BASE_GODOT_RESULT="
const MANIFEST_PATH := "res://GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
const ARTIFACT_DIR := "res://artifacts"
const STATE_PATH := "res://artifacts/pilot_state.json"
const LEDGER_PATH := "res://artifacts/operation_ledger.json"

func _init() -> void:
    var args := OS.get_cmdline_user_args()
    var command := String(args[0]) if not args.is_empty() else ""
    var request_path := String(args[1]) if args.size() > 1 else ""
    var manifest_result := _load_json(MANIFEST_PATH)
    if not manifest_result["ok"]:
        _finish(_basic_envelope(command, "READ_ONLY", false, "MANIFEST_INVALID", {}, []), 2)
        return

    var manifest: Dictionary = manifest_result["data"]
    var identity_result := _verify_identity(manifest)
    if not identity_result["ok"]:
        _finish(
            _basic_envelope(command, "READ_ONLY", false, "PROJECT_IDENTITY_MISMATCH", identity_result, []),
            2
        )
        return

    var catalog_result := _verify_catalog(manifest)
    if not catalog_result["ok"]:
        _finish(
            _basic_envelope(
                command if not command.is_empty() else "doctor",
                "READ_ONLY",
                false,
                "CATALOG_STALE",
                catalog_result,
                [_evidence("CONTRACT", "CONTRACT_FAIL", MANIFEST_PATH)]
            ),
            2
        )
        return

    var envelope: Dictionary
    match command:
        "doctor":
            envelope = _doctor(manifest, identity_result)
        "status":
            envelope = _status(manifest, identity_result)
        "catalog.compact":
            envelope = _catalog(manifest)
        "scene.inspect":
            envelope = _scene_inspect()
        "state.write_marker":
            envelope = _state_write_marker(request_path, identity_result["project_fingerprint"])
        "task.start":
            envelope = _task_start(request_path, identity_result["project_fingerprint"])
        "task.resume":
            envelope = _task_resume(request_path, identity_result["project_fingerprint"])
        _:
            envelope = _basic_envelope(command, "READ_ONLY", false, "CAPABILITY_NOT_DECLARED", {}, [])

    _finish(envelope, 0 if envelope["result"]["success"] else 2)

func _load_json(path: String) -> Dictionary:
    if path.is_empty() or not FileAccess.file_exists(path):
        return {"ok": false, "code": "FILE_NOT_FOUND"}
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {"ok": false, "code": "FILE_OPEN_FAILED"}
    var parsed = JSON.parse_string(file.get_as_text())
    if typeof(parsed) != TYPE_DICTIONARY:
        return {"ok": false, "code": "JSON_INVALID"}
    return {"ok": true, "data": parsed}

func _write_json(path: String, data: Dictionary) -> bool:
    DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(ARTIFACT_DIR))
    var temporary_path := path + ".tmp"
    var temporary_file := FileAccess.open(temporary_path, FileAccess.WRITE)
    if temporary_file == null:
        return false
    temporary_file.store_string(JSON.stringify(data, "  ") + "\n")
    temporary_file.close()

    var temporary_global := ProjectSettings.globalize_path(temporary_path)
    var destination_global := ProjectSettings.globalize_path(path)
    var rename_error := DirAccess.rename_absolute(temporary_global, destination_global)
    if rename_error != OK:
        DirAccess.remove_absolute(temporary_global)
        return false
    return true

func _verify_identity(manifest: Dictionary) -> Dictionary:
    var identity: Dictionary = manifest.get("project_identity", {})
    var normalized_path := String(identity.get("normalized_project_path", ""))
    var expected_project_hash := String(identity.get("project_godot_sha256", ""))
    var expected_fingerprint := String(identity.get("project_fingerprint", ""))
    var runtime_project_path := ProjectSettings.globalize_path("res://").replace("\\", "/").trim_suffix("/")
    var actual_project_hash := FileAccess.get_sha256("res://project.godot")
    var actual_fingerprint := _sha256_text(normalized_path + ":" + actual_project_hash)
    var path_matches := runtime_project_path.ends_with("/" + normalized_path) or runtime_project_path == normalized_path
    var ok := (
        path_matches
        and actual_project_hash == expected_project_hash
        and actual_fingerprint == expected_fingerprint
    )
    return {
        "ok": ok,
        "normalized_project_path": normalized_path,
        "project_path": normalized_path,
        "project_godot_sha256": actual_project_hash,
        "project_fingerprint": actual_fingerprint,
    }


func _verify_catalog(manifest: Dictionary) -> Dictionary:
    var catalog: Dictionary = manifest.get("catalog", {})
    var expected_hash := String(catalog.get("sha256", ""))
    var canonical_capabilities := JSON.stringify(_canonicalize(manifest.get("capabilities", [])))
    var actual_hash := _sha256_text(canonical_capabilities)
    var ok := (
        String(catalog.get("freshness_state", "")) == "FRESH"
        and _is_sha256(expected_hash)
        and expected_hash == actual_hash
    )
    return {
        "ok": ok,
        "expected_sha256": expected_hash,
        "actual_sha256": actual_hash,
        "freshness_state": catalog.get("freshness_state", ""),
    }

func _canonicalize(value: Variant) -> Variant:
    if typeof(value) == TYPE_DICTIONARY:
        var source: Dictionary = value
        var keys := source.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[String(key)] = _canonicalize(source[key])
        return result
    if typeof(value) == TYPE_ARRAY:
        var result_array: Array = []
        for item in value:
            result_array.append(_canonicalize(item))
        return result_array
    return value

func _doctor(manifest: Dictionary, identity: Dictionary) -> Dictionary:
    var data := {
        "engine_version": Engine.get_version_info().get("string", ""),
        "configuration_state": manifest.get("configuration_state", ""),
        "transport_kind": manifest.get("transport", {}).get("kind", ""),
        "capability_count": manifest.get("capabilities", []).size(),
        "identity": identity,
    }
    return _basic_envelope("doctor", "READ_ONLY", true, "OK", data, [_evidence("CONTRACT", "EXECUTION_PASS", MANIFEST_PATH)])

func _status(manifest: Dictionary, identity: Dictionary) -> Dictionary:
    var data := {
        "project_name": ProjectSettings.get_setting("application/config/name", ""),
        "main_scene": ProjectSettings.get_setting("application/run/main_scene", ""),
        "project_path": identity["project_path"],
        "project_fingerprint": identity["project_fingerprint"],
        "catalog_freshness": manifest.get("catalog", {}).get("freshness_state", ""),
    }
    return _basic_envelope("status", "READ_ONLY", true, "OK", data, [_evidence("ENGINE_STATE", "EXECUTION_PASS", "res://project.godot")])

func _catalog(manifest: Dictionary) -> Dictionary:
    var compact: Array = []
    for capability in manifest.get("capabilities", []):
        compact.append({
            "capability_id": capability.get("capability_id", ""),
            "operation_class": capability.get("operation_class", ""),
            "execution_path": capability.get("execution_path", ""),
        })
    return _basic_envelope(
        "catalog.compact",
        "READ_ONLY",
        true,
        "OK",
        {"catalog_sha256": manifest.get("catalog", {}).get("sha256", ""), "capabilities": compact},
        [_evidence("CONTRACT", "EXECUTION_PASS", MANIFEST_PATH)]
    )

func _scene_inspect() -> Dictionary:
    var main_scene := String(ProjectSettings.get_setting("application/run/main_scene", ""))
    var packed = load(main_scene)
    if packed == null or not packed is PackedScene:
        return _basic_envelope("scene.inspect", "READ_ONLY", false, "SCENE_LOAD_FAILED", {"main_scene": main_scene}, [])
    var instance: Node = packed.instantiate()
    var data := {
        "main_scene": main_scene,
        "root_name": String(instance.name),
        "root_class": instance.get_class(),
        "child_count": instance.get_child_count(),
    }
    instance.free()
    return _basic_envelope("scene.inspect", "READ_ONLY", true, "OK", data, [_evidence("ENGINE_STATE", "EXECUTION_PASS", main_scene)])

func _validate_request_shape(capability_id: String, request: Dictionary) -> bool:
    var required: Array[String] = []
    var allowed: Array[String] = []
    match capability_id:
        "state.write_marker":
            required = ["operation_id", "marker", "idempotency_key", "request_hash", "approval"]
            allowed = required.duplicate()
            if (
                typeof(request.get("operation_id")) != TYPE_STRING
                or typeof(request.get("marker")) != TYPE_STRING
                or typeof(request.get("idempotency_key")) != TYPE_STRING
                or typeof(request.get("request_hash")) != TYPE_STRING
                or typeof(request.get("approval")) != TYPE_DICTIONARY
            ):
                return false
        "task.start":
            required = ["operation_id", "request_hash", "approval"]
            allowed = required.duplicate()
            if (
                typeof(request.get("operation_id")) != TYPE_STRING
                or typeof(request.get("request_hash")) != TYPE_STRING
                or typeof(request.get("approval")) != TYPE_DICTIONARY
            ):
                return false
        "task.resume":
            required = ["operation_id", "task_id", "request_hash", "approval"]
            allowed = required.duplicate()
            if (
                typeof(request.get("operation_id")) != TYPE_STRING
                or typeof(request.get("task_id")) != TYPE_STRING
                or typeof(request.get("request_hash")) != TYPE_STRING
                or typeof(request.get("approval")) != TYPE_DICTIONARY
            ):
                return false
        _:
            return false

    for key in required:
        if not request.has(key):
            return false
    for key in request.keys():
        if not String(key) in allowed:
            return false
    return true

func _state_write_marker(request_path: String, project_fingerprint: String) -> Dictionary:
    var request_result := _load_json(request_path)
    if not request_result["ok"]:
        return _basic_envelope("state.write_marker", "IDEMPOTENT_MUTATION", false, "REQUEST_INVALID", {}, [])
    var request: Dictionary = request_result["data"]
    if not _validate_request_shape("state.write_marker", request):
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "REQUEST_SCHEMA_INVALID", {}, [])

    var operation_id := String(request.get("operation_id", ""))
    var marker := String(request.get("marker", ""))
    var idempotency_key := String(request.get("idempotency_key", ""))
    var request_hash := String(request.get("request_hash", ""))
    var expected_hash := _sha256_text(
        "marker=" + marker + "|idempotency_key=" + idempotency_key + "|operation_id=" + operation_id
    )
    if operation_id.is_empty() or marker.is_empty() or idempotency_key.is_empty() or request_hash != expected_hash:
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "REQUEST_HASH_MISMATCH", {}, [])

    var ledger := _load_ledger()
    var idempotency: Dictionary = ledger.get("idempotency", {})
    if idempotency.has(idempotency_key):
        var existing: Dictionary = idempotency[idempotency_key]
        if String(existing.get("request_hash", "")) != request_hash:
            return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "IDEMPOTENCY_KEY_CONFLICT", {}, [])
        return _request_envelope(
            "state.write_marker",
            "IDEMPOTENT_MUTATION",
            request,
            true,
            "IDEMPOTENT_REPLAY",
            existing.get("data", {}),
            [_evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
        )

    var approval_code := _approval_code(
        request.get("approval", {}),
        project_fingerprint,
        "state.write_marker",
        request_hash,
        "IDEMPOTENT_MUTATION",
        ledger
    )
    if approval_code != "OK":
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, approval_code, {}, [])

    var approval_token_id := _approval_token_id(request.get("approval", {}))
    var operations: Dictionary = ledger.get("operations", {})
    var consumed_tokens: Dictionary = ledger.get("consumed_approval_tokens", {})
    operations[operation_id] = {
        "operation_id": operation_id,
        "project_fingerprint": project_fingerprint,
        "capability_id": "state.write_marker",
        "request_hash": request_hash,
        "idempotency_key": idempotency_key,
        "approval_token_id": approval_token_id,
        "state": "STARTED",
        "result_code": "PENDING",
        "result_hash": null,
        "evidence_paths": [],
    }
    consumed_tokens[approval_token_id] = {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "capability_id": "state.write_marker",
    }
    ledger["operations"] = operations
    ledger["consumed_approval_tokens"] = consumed_tokens
    if not _write_json(LEDGER_PATH, ledger):
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "LEDGER_WRITE_FAILED", {}, [])

    var state := {
        "marker": marker,
        "operation_id": operation_id,
        "request_hash": request_hash,
        "idempotency_key": idempotency_key,
        "project_fingerprint": project_fingerprint,
    }
    if not _write_json(STATE_PATH, state):
        operations[operation_id]["state"] = "FAILED"
        operations[operation_id]["result_code"] = "STATE_WRITE_FAILED"
        ledger["operations"] = operations
        _write_json(LEDGER_PATH, ledger)
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "STATE_WRITE_FAILED", {}, [])

    var result_hash := _sha256_text(JSON.stringify(_canonicalize(state)))
    idempotency[idempotency_key] = {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "result_hash": result_hash,
        "data": state,
    }
    operations[operation_id]["state"] = "COMPLETED"
    operations[operation_id]["result_code"] = "OK"
    operations[operation_id]["result_hash"] = result_hash
    operations[operation_id]["evidence_paths"] = [STATE_PATH, LEDGER_PATH]
    ledger["idempotency"] = idempotency
    ledger["operations"] = operations
    if not _write_json(LEDGER_PATH, ledger):
        return _request_envelope("state.write_marker", "IDEMPOTENT_MUTATION", request, false, "LEDGER_WRITE_FAILED", {}, [])

    return _request_envelope(
        "state.write_marker",
        "IDEMPOTENT_MUTATION",
        request,
        true,
        "OK",
        state,
        [_evidence("ENGINE_STATE", "EXECUTION_PASS", STATE_PATH), _evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
    )

func _task_start(request_path: String, project_fingerprint: String) -> Dictionary:
    var request_result := _load_json(request_path)
    if not request_result["ok"]:
        return _task_failure_envelope("task.start", {}, "REQUEST_INVALID")
    var request: Dictionary = request_result["data"]
    if not _validate_request_shape("task.start", request):
        return _task_failure_envelope("task.start", request, "REQUEST_SCHEMA_INVALID")
    var operation_id := String(request.get("operation_id", ""))
    var request_hash := String(request.get("request_hash", ""))
    var expected_hash := _sha256_text("operation_id=" + operation_id + "|capability_id=task.start")
    if operation_id.is_empty() or request_hash != expected_hash:
        return _task_failure_envelope("task.start", request, "REQUEST_HASH_MISMATCH")

    var ledger := _load_ledger()
    var tasks: Dictionary = ledger.get("tasks", {})
    if tasks.has(operation_id):
        var existing: Dictionary = tasks[operation_id]
        if String(existing.get("start_request_hash", "")) != request_hash:
            return _task_failure_envelope("task.start", request, "OPERATION_ID_CONFLICT", existing.get("task_id"), "STALE")
        return _task_envelope(
            "task.start",
            request,
            true,
            "TASK_PENDING" if String(existing.get("state", "")) != "COMPLETED" else "OK",
            String(existing.get("task_id", "")),
            String(existing.get("state", "PENDING")),
            existing.get("result_binding"),
            {"reused_existing_task": true},
            [_evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
        )

    var approval_code := _approval_code(
        request.get("approval", {}), project_fingerprint, "task.start", request_hash, "LONG_RUNNING_TASK", ledger
    )
    if approval_code != "OK":
        return _task_failure_envelope("task.start", request, approval_code)

    var task_id := "task-" + _sha256_text(operation_id).substr(0, 16)
    var approval_token_id := _approval_token_id(request.get("approval", {}))
    tasks[operation_id] = {
        "task_id": task_id,
        "operation_id": operation_id,
        "project_fingerprint": project_fingerprint,
        "state": "PENDING",
        "result_binding": null,
        "start_request_hash": request_hash,
        "approval_token_id": approval_token_id,
    }
    var consumed_tokens: Dictionary = ledger.get("consumed_approval_tokens", {})
    consumed_tokens[approval_token_id] = {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "capability_id": "task.start",
    }
    ledger["tasks"] = tasks
    ledger["consumed_approval_tokens"] = consumed_tokens
    if not _write_json(LEDGER_PATH, ledger):
        return _task_failure_envelope("task.start", request, "LEDGER_WRITE_FAILED", task_id)
    return _task_envelope(
        "task.start", request, true, "TASK_PENDING", task_id, "PENDING", null,
        {"reused_existing_task": false}, [_evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
    )

func _task_resume(request_path: String, project_fingerprint: String) -> Dictionary:
    var request_result := _load_json(request_path)
    if not request_result["ok"]:
        return _task_failure_envelope("task.resume", {}, "REQUEST_INVALID")
    var request: Dictionary = request_result["data"]
    if not _validate_request_shape("task.resume", request):
        return _task_failure_envelope("task.resume", request, "REQUEST_SCHEMA_INVALID")
    var operation_id := String(request.get("operation_id", ""))
    var task_id := String(request.get("task_id", ""))
    var request_hash := String(request.get("request_hash", ""))
    var expected_hash := _sha256_text("operation_id=" + operation_id + "|capability_id=task.resume|task_id=" + task_id)
    if operation_id.is_empty() or task_id.is_empty() or request_hash != expected_hash:
        return _task_failure_envelope("task.resume", request, "REQUEST_HASH_MISMATCH", task_id)

    var ledger := _load_ledger()
    var tasks: Dictionary = ledger.get("tasks", {})
    if not tasks.has(operation_id):
        return _task_failure_envelope("task.resume", request, "TASK_NOT_FOUND", task_id, "STALE")
    var record: Dictionary = tasks[operation_id]
    if String(record.get("task_id", "")) != task_id or String(record.get("project_fingerprint", "")) != project_fingerprint:
        return _task_failure_envelope("task.resume", request, "TASK_RESULT_STALE", task_id, "STALE")
    if String(record.get("state", "")) == "COMPLETED":
        return _task_envelope(
            "task.resume", request, true, "OK", task_id, "COMPLETED", record.get("result_binding"),
            {"resumed_existing_task": true, "replayed_completed_result": true},
            [_evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
        )

    var approval_code := _approval_code(
        request.get("approval", {}), project_fingerprint, "task.resume", request_hash, "LONG_RUNNING_TASK", ledger
    )
    if approval_code != "OK":
        return _task_failure_envelope("task.resume", request, approval_code, task_id, "PENDING")

    var result_hash := _sha256_text(project_fingerprint + "|task.resume|" + operation_id + "|" + task_id)
    var result_binding := {
        "project_fingerprint": project_fingerprint,
        "capability_id": "task.resume",
        "operation_id": operation_id,
        "task_id": task_id,
        "result_hash": result_hash,
    }
    var approval_token_id := _approval_token_id(request.get("approval", {}))
    record["state"] = "COMPLETED"
    record["result_binding"] = result_binding
    record["resume_request_hash"] = request_hash
    record["resume_approval_token_id"] = approval_token_id
    tasks[operation_id] = record
    var consumed_tokens: Dictionary = ledger.get("consumed_approval_tokens", {})
    consumed_tokens[approval_token_id] = {
        "operation_id": operation_id,
        "request_hash": request_hash,
        "capability_id": "task.resume",
    }
    ledger["tasks"] = tasks
    ledger["consumed_approval_tokens"] = consumed_tokens
    if not _write_json(LEDGER_PATH, ledger):
        return _task_failure_envelope("task.resume", request, "LEDGER_WRITE_FAILED", task_id)
    return _task_envelope(
        "task.resume", request, true, "OK", task_id, "COMPLETED", result_binding,
        {"resumed_existing_task": true}, [_evidence("LOG", "EXECUTION_PASS", LEDGER_PATH)]
    )

func _task_failure_envelope(
    capability_id: String,
    request_variant: Variant,
    code: String,
    provided_task_id: Variant = null,
    task_state: String = "FAILED"
) -> Dictionary:
    var request: Dictionary = {}
    if typeof(request_variant) == TYPE_DICTIONARY:
        request = request_variant.duplicate(true)

    var operation_id := String(request.get("operation_id", ""))
    if operation_id.is_empty():
        operation_id = "pilot-" + capability_id.replace(".", "-") + "-invalid"
    request["operation_id"] = operation_id

    var request_hash := String(request.get("request_hash", ""))
    if not _is_sha256(request_hash):
        request_hash = _sha256_text(capability_id + "|" + operation_id + "|" + code)
    request["request_hash"] = request_hash
    request["approval"] = _normalized_failure_approval(request.get("approval"), code)

    var preflight_codes := [
        "REQUEST_INVALID", "REQUEST_SCHEMA_INVALID", "REQUEST_HASH_MISMATCH",
        "APPROVAL_REQUIRED", "APPROVAL_TOKEN_MISMATCH", "APPROVAL_EXPIRED", "APPROVAL_TOKEN_REUSED"
    ]
    if provided_task_id == null and code in preflight_codes:
        return _task_envelope(
            capability_id, request, false, code, null, "NOT_STARTED", null,
            {"task_started": false}, []
        )

    var task_id := String(provided_task_id) if provided_task_id != null else ""
    if task_id.is_empty():
        task_id = "task-failed-" + _sha256_text(operation_id + "|" + capability_id + "|" + code).substr(0, 16)
    var project_fingerprint := _current_fingerprint()
    var result_binding := {
        "project_fingerprint": project_fingerprint,
        "capability_id": capability_id,
        "operation_id": operation_id,
        "task_id": task_id,
        "result_hash": _sha256_text(project_fingerprint + "|" + capability_id + "|" + operation_id + "|" + task_id + "|" + code),
    }
    return _task_envelope(
        capability_id, request, false, code, task_id, task_state, result_binding,
        {"failure_bound": true}, []
    )

func _normalized_failure_approval(approval_variant: Variant, code: String) -> Dictionary:
    if code == "APPROVAL_REQUIRED":
        return {"state": "REQUIRED", "token_binding": null, "expires_at": null}
    if code in ["APPROVAL_TOKEN_MISMATCH", "APPROVAL_TOKEN_REUSED"]:
        return {"state": "REJECTED", "token_binding": null, "expires_at": null}
    if code == "APPROVAL_EXPIRED":
        return {"state": "EXPIRED", "token_binding": null, "expires_at": null}
    if typeof(approval_variant) == TYPE_DICTIONARY:
        var approval: Dictionary = approval_variant
        if (
            String(approval.get("state", "")) == "APPROVED"
            and typeof(approval.get("token_binding")) == TYPE_DICTIONARY
            and not String(approval.get("expires_at", "")).is_empty()
        ):
            return approval.duplicate(true)
    return {"state": "REQUIRED", "token_binding": null, "expires_at": null}

func _approval_for_result(approval_variant: Variant, code: String) -> Dictionary:
    if code in ["APPROVAL_REQUIRED", "APPROVAL_TOKEN_MISMATCH", "APPROVAL_TOKEN_REUSED", "APPROVAL_EXPIRED"]:
        return _normalized_failure_approval(approval_variant, code)
    if typeof(approval_variant) == TYPE_DICTIONARY:
        return approval_variant.duplicate(true)
    return {"state": "REQUIRED", "token_binding": null, "expires_at": null}

func _approval_token_id(approval_variant: Variant) -> String:
    if typeof(approval_variant) != TYPE_DICTIONARY:
        return ""
    var approval: Dictionary = approval_variant
    var binding_variant = approval.get("token_binding")
    if typeof(binding_variant) != TYPE_DICTIONARY:
        return ""
    return String(binding_variant.get("token_id", ""))

func _is_sha256(value: String) -> bool:
    if value.length() != 64:
        return false
    for character in value:
        if not String(character).to_lower() in "0123456789abcdef":
            return false
    return true

func _approval_code(
    approval_variant: Variant,
    project_fingerprint: String,
    capability_id: String,
    request_hash: String,
    operation_class: String,
    ledger: Dictionary
) -> String:
    if typeof(approval_variant) != TYPE_DICTIONARY:
        return "APPROVAL_REQUIRED"
    var approval: Dictionary = approval_variant
    if String(approval.get("state", "")) != "APPROVED":
        return "APPROVAL_REQUIRED"
    var binding_variant = approval.get("token_binding")
    if typeof(binding_variant) != TYPE_DICTIONARY:
        return "APPROVAL_TOKEN_MISMATCH"
    var binding: Dictionary = binding_variant
    if (
        String(binding.get("project_fingerprint", "")) != project_fingerprint
        or String(binding.get("capability_id", "")) != capability_id
        or String(binding.get("request_hash", "")) != request_hash
        or String(binding.get("operation_class", "")) != operation_class
    ):
        return "APPROVAL_TOKEN_MISMATCH"
    var token_id := String(binding.get("token_id", ""))
    var expires_at := String(approval.get("expires_at", ""))
    if token_id.is_empty() or expires_at.is_empty():
        return "APPROVAL_TOKEN_MISMATCH"
    var expiry_unix := Time.get_unix_time_from_datetime_string(expires_at)
    if expiry_unix <= 0:
        return "APPROVAL_TOKEN_MISMATCH"
    if float(expiry_unix) <= Time.get_unix_time_from_system():
        return "APPROVAL_EXPIRED"
    var consumed_tokens: Dictionary = ledger.get("consumed_approval_tokens", {})
    if consumed_tokens.has(token_id):
        return "APPROVAL_TOKEN_REUSED"
    return "OK"

func _load_ledger() -> Dictionary:
    var empty := {
        "idempotency": {},
        "tasks": {},
        "operations": {},
        "consumed_approval_tokens": {},
    }
    if not FileAccess.file_exists(LEDGER_PATH):
        return empty
    var loaded := _load_json(LEDGER_PATH)
    if not loaded["ok"]:
        return empty
    var ledger: Dictionary = loaded["data"]
    for key in empty.keys():
        if typeof(ledger.get(key, {})) != TYPE_DICTIONARY:
            ledger[key] = {}
    return ledger

func _basic_envelope(capability_id: String, operation_class: String, success: bool, code: String, data: Dictionary, evidence: Array) -> Dictionary:
    return {
        "schema_version": 1,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": "pilot-" + capability_id.replace(".", "-"),
        "project_fingerprint": _current_fingerprint(),
        "capability_id": capability_id,
        "operation_class": operation_class,
        "request_hash": _sha256_text(capability_id),
        "approval": {"state": "NOT_REQUIRED", "token_binding": null, "expires_at": null},
        "task": {"task_id": null, "state": "NOT_APPLICABLE", "result_binding": null},
        "result": {"success": success, "code": code, "message": code, "data": data, "evidence": evidence},
    }

func _request_envelope(
    capability_id: String,
    operation_class: String,
    request: Dictionary,
    success: bool,
    code: String,
    data: Dictionary,
    evidence: Array
) -> Dictionary:
    return {
        "schema_version": 1,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": String(request.get("operation_id", "unknown")),
        "project_fingerprint": _current_fingerprint(),
        "capability_id": capability_id,
        "operation_class": operation_class,
        "request_hash": String(request.get("request_hash", _sha256_text(capability_id))),
        "approval": _approval_for_result(request.get("approval"), code),
        "task": {"task_id": null, "state": "NOT_APPLICABLE", "result_binding": null},
        "result": {"success": success, "code": code, "message": code, "data": data, "evidence": evidence},
    }


func _task_envelope(
    capability_id: String,
    request: Dictionary,
    success: bool,
    code: String,
    task_id: Variant,
    task_state: String,
    result_binding: Variant,
    data: Dictionary,
    evidence: Array
) -> Dictionary:
    return {
        "schema_version": 1,
        "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
        "operation_id": String(request.get("operation_id", "unknown")),
        "project_fingerprint": _current_fingerprint(),
        "capability_id": capability_id,
        "operation_class": "LONG_RUNNING_TASK",
        "request_hash": String(request.get("request_hash", _sha256_text(capability_id))),
        "approval": _approval_for_result(request.get("approval"), code),
        "task": {"task_id": task_id, "state": task_state, "result_binding": result_binding},
        "result": {"success": success, "code": code, "message": code, "data": data, "evidence": evidence},
    }

func _current_fingerprint() -> String:
    var loaded := _load_json(MANIFEST_PATH)
    if not loaded["ok"]:
        return "unknown"
    return String(loaded["data"].get("project_identity", {}).get("project_fingerprint", "unknown"))

func _evidence(kind: String, state: String, path: String) -> Dictionary:
    return {"kind": kind, "state": state, "path": path}

func _sha256_text(value: String) -> String:
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(value.to_utf8_buffer())
    return context.finish().hex_encode()

func _finish(envelope: Dictionary, exit_code: int) -> void:
    print(RESULT_PREFIX + JSON.stringify(envelope))
    quit(exit_code)
