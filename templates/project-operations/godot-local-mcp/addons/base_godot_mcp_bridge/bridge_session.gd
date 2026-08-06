@tool
extends RefCounted

const STATE_WAIT_HELLO := "WAIT_HELLO"
const STATE_READY := "READY"
const STATE_WAIT_RESULT := "WAIT_RESULT"
const STATE_CLOSED := "CLOSED"

var _peer: StreamPeerTCP
var _codec
var _profile_store
var _handler := Callable()
var _protocol := ""
var _project_fingerprint := ""
var _bridge_instance_id := ""
var _descriptor_nonce := ""
var _state := STATE_WAIT_HELLO
var _profile_id := ""
var _secret := ""
var _session_id := ""
var _client_nonce := ""
var _server_nonce := ""
var _seen_request_ids: Dictionary = {}
var _waiting_request_id := ""
var _waiting_operation_id := ""


func configure(
    peer: StreamPeerTCP,
    codec,
    profile_store,
    handler: Callable,
    protocol: String,
    project_fingerprint: String,
    bridge_instance_id: String,
    descriptor_nonce: String,
) -> void:
    _peer = peer
    _codec = codec
    _profile_store = profile_store
    _handler = handler
    _protocol = protocol
    _project_fingerprint = project_fingerprint
    _bridge_instance_id = bridge_instance_id
    _descriptor_nonce = descriptor_nonce


func poll() -> void:
    if is_closed() or _peer == null:
        return
    _peer.poll()
    var status := _peer.get_status()
    if status == StreamPeerTCP.STATUS_ERROR or status == StreamPeerTCP.STATUS_NONE:
        close()
        return
    var available := _peer.get_available_bytes()
    if available <= 0:
        return
    var chunk_result := _peer.get_partial_data(available)
    if chunk_result.size() != 2 or int(chunk_result[0]) != OK:
        close()
        return
    var chunk: PackedByteArray = chunk_result[1]
    for frame in _codec.feed_bytes(chunk):
        if frame.has("_frame_error"):
            close()
            return
        if _state == STATE_WAIT_HELLO:
            _handle_hello(frame)
        elif _state == STATE_READY:
            _handle_request(frame)
        else:
            close()
        if is_closed():
            return


func complete_operation(operation_id: String, result: Dictionary) -> bool:
    if _state != STATE_WAIT_RESULT or operation_id != _waiting_operation_id:
        return false
    _send_response(_waiting_request_id, result)
    _waiting_operation_id = ""
    _waiting_request_id = ""
    _state = STATE_READY
    return true


func waiting_operation_id() -> String:
    return _waiting_operation_id


func is_closed() -> bool:
    return _state == STATE_CLOSED


func close() -> void:
    _state = STATE_CLOSED
    if _peer != null:
        _peer.disconnect_from_host()
    _peer = null
    if _codec != null:
        _codec.reset()


func _handle_hello(frame: Dictionary) -> void:
    var profile_id := str(frame.get("profile_id", ""))
    var profile: Dictionary = _profile_store.load_profile(profile_id, _project_fingerprint)
    if not profile.get("ok", false):
        close()
        return
    var secret := str(profile.get("credential_secret", ""))
    var verified: Dictionary = _codec.verify_signed(secret, frame)
    if not verified.get("ok", false):
        close()
        return
    var hello: Dictionary = verified.get("payload", {})
    if (
        hello.get("type") != "HELLO"
        or hello.get("protocol") != _protocol
        or hello.get("project_fingerprint") != _project_fingerprint
        or hello.get("bridge_instance_id") != _bridge_instance_id
        or hello.get("descriptor_nonce") != _descriptor_nonce
    ):
        close()
        return
    _client_nonce = str(hello.get("client_nonce", ""))
    if _client_nonce.length() < 32 or _client_nonce.length() > 256:
        close()
        return
    var session_bytes := Crypto.new().generate_random_bytes(16)
    var nonce_bytes := Crypto.new().generate_random_bytes(32)
    if session_bytes.size() != 16 or nonce_bytes.size() != 32:
        close()
        return
    _profile_id = profile_id
    _secret = secret
    _session_id = "session-%s" % session_bytes.hex_encode()
    _server_nonce = nonce_bytes.hex_encode()
    var ack := {
        "type": "HELLO_ACK",
        "protocol": _protocol,
        "bridge_instance_id": _bridge_instance_id,
        "session_id": _session_id,
        "client_nonce": _client_nonce,
        "server_nonce": _server_nonce,
    }
    if not _send(_codec.signed_frame(_secret, ack)):
        close()
        return
    _state = STATE_READY


func _handle_request(frame: Dictionary) -> void:
    var verified: Dictionary = _codec.verify_signed(_secret, frame)
    if not verified.get("ok", false):
        close()
        return
    var request: Dictionary = verified.get("payload", {})
    var request_id := str(request.get("request_id", ""))
    if (
        request.get("type") != "REQUEST"
        or request.get("protocol") != _protocol
        or request.get("session_id") != _session_id
        or request.get("server_nonce") != _server_nonce
        or request_id.is_empty()
        or _seen_request_ids.has(request_id)
    ):
        close()
        return
    _seen_request_ids[request_id] = true
    var method := str(request.get("method", ""))
    var payload = request.get("payload", {})
    if method.is_empty() or not (payload is Dictionary) or not _handler.is_valid():
        _send_response(
            request_id,
            {"success": false, "code": "BRIDGE_REQUEST_INVALID", "data": {}},
        )
        return
    var result: Dictionary = _handler.call(method, payload, _profile_id)
    if result.get("_deferred", false):
        _waiting_request_id = request_id
        _waiting_operation_id = str(result.get("operation_id", ""))
        if _waiting_operation_id.is_empty():
            close()
            return
        _state = STATE_WAIT_RESULT
        return
    _send_response(request_id, result)


func _send_response(request_id: String, result: Dictionary) -> void:
    var response := {
        "type": "RESPONSE",
        "protocol": _protocol,
        "session_id": _session_id,
        "request_id": request_id,
        "result": result,
    }
    if not _send(_codec.signed_frame(_secret, response)):
        close()


func _send(payload: Dictionary) -> bool:
    if _peer == null:
        return false
    var frame: PackedByteArray = _codec.encode_frame(payload)
    if frame.is_empty():
        return false
    return _peer.put_data(frame) == OK
