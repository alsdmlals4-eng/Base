@tool
extends RefCounted

const HEADER_BYTES := 4
const MAX_FRAME_BYTES := 262_144
const MAX_JSON_DEPTH := 32

var _buffer := PackedByteArray()
var _crypto := Crypto.new()


func reset() -> void:
    _buffer.clear()


func feed_bytes(bytes: PackedByteArray) -> Array[Dictionary]:
    var frames: Array[Dictionary] = []
    if bytes.is_empty():
        return frames
    _buffer.append_array(bytes)
    while _buffer.size() >= HEADER_BYTES:
        var length := (
            (int(_buffer[0]) << 24)
            | (int(_buffer[1]) << 16)
            | (int(_buffer[2]) << 8)
            | int(_buffer[3])
        )
        if length <= 0 or length > MAX_FRAME_BYTES:
            reset()
            return [{"_frame_error": "FRAME_LENGTH_INVALID"}]
        if _buffer.size() < HEADER_BYTES + length:
            break
        var body := _buffer.slice(HEADER_BYTES, HEADER_BYTES + length)
        _buffer = _buffer.slice(HEADER_BYTES + length)
        var text := body.get_string_from_utf8()
        var parsed = JSON.parse_string(text)
        if not (parsed is Dictionary) or _json_depth(parsed) > MAX_JSON_DEPTH:
            reset()
            return [{"_frame_error": "FRAME_JSON_INVALID"}]
        frames.append(parsed)
    return frames


func encode_frame(payload: Dictionary) -> PackedByteArray:
    var body := canonical_json(payload).to_utf8_buffer()
    if body.is_empty() or body.size() > MAX_FRAME_BYTES:
        return PackedByteArray()
    var frame := PackedByteArray()
    frame.resize(HEADER_BYTES)
    var length := body.size()
    frame[0] = (length >> 24) & 0xff
    frame[1] = (length >> 16) & 0xff
    frame[2] = (length >> 8) & 0xff
    frame[3] = length & 0xff
    frame.append_array(body)
    return frame


func canonical_json(value: Variant) -> String:
    match typeof(value):
        TYPE_NIL:
            return "null"
        TYPE_BOOL:
            return "true" if value else "false"
        TYPE_INT:
            return str(value)
        TYPE_FLOAT:
            return JSON.stringify(value)
        TYPE_STRING, TYPE_STRING_NAME:
            return JSON.stringify(str(value))
        TYPE_ARRAY:
            var array_parts := PackedStringArray()
            for item in value:
                array_parts.append(canonical_json(item))
            return "[%s]" % ",".join(array_parts)
        TYPE_DICTIONARY:
            var dictionary: Dictionary = value
            var keys: Array = dictionary.keys()
            keys.sort()
            var object_parts := PackedStringArray()
            for key in keys:
                object_parts.append(
                    "%s:%s" % [
                        JSON.stringify(str(key)),
                        canonical_json(dictionary[key]),
                    ]
                )
            return "{%s}" % ",".join(object_parts)
        _:
            return JSON.stringify(value)


func canonical_sha256(value: Variant) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(canonical_json(value).to_utf8_buffer())
    return context.finish().hex_encode()


func sign(secret: String, payload: Dictionary) -> String:
    return _crypto.hmac_digest(
        HashingContext.HASH_SHA256,
        secret.to_utf8_buffer(),
        canonical_json(payload).to_utf8_buffer(),
    ).hex_encode()


func verify_signed(secret: String, frame: Dictionary) -> Dictionary:
    var received_text := str(frame.get("mac", ""))
    if received_text.length() != 64 or not received_text.is_valid_hex_number(false):
        return {"ok": false, "code": "BRIDGE_MAC_INVALID"}
    var unsigned := frame.duplicate(true)
    unsigned.erase("mac")
    var expected := sign(secret, unsigned).hex_decode()
    var received := received_text.hex_decode()
    if expected.size() != received.size() or not _crypto.constant_time_compare(expected, received):
        return {"ok": false, "code": "BRIDGE_MAC_INVALID"}
    return {"ok": true, "payload": unsigned}


func signed_frame(secret: String, payload: Dictionary) -> Dictionary:
    var result := payload.duplicate(true)
    result["mac"] = sign(secret, payload)
    return result


func _json_depth(value: Variant, depth: int = 0) -> int:
    if depth > MAX_JSON_DEPTH:
        return depth
    if value is Dictionary:
        var maximum := depth
        for child in value.values():
            maximum = maxi(maximum, _json_depth(child, depth + 1))
        return maximum
    if value is Array:
        var maximum := depth
        for child in value:
            maximum = maxi(maximum, _json_depth(child, depth + 1))
        return maximum
    return depth
