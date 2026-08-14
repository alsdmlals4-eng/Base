extends RefCounted

var _model = null
var _current_beat_id: String = ""
var _line_index: int = 0
var _started: bool = false
var _ended: bool = false
var _last_error: String = ""

func start(model) -> bool:
    _last_error = ""
    if model == null:
        _last_error = "model is null"
        return false

    var entry_beat_id: String = model.get_entry_beat_id()
    if entry_beat_id.is_empty() or model.get_beat(entry_beat_id).is_empty():
        _last_error = "model entry beat is missing"
        return false

    _model = model
    _current_beat_id = entry_beat_id
    _line_index = 0
    _started = true
    _ended = false
    return true

func current_line() -> Dictionary:
    if not _started or _ended or _model == null:
        return {}
    var dialogues: Array = _model.get_dialogues_for_beat(_current_beat_id)
    if _line_index < 0 or _line_index >= dialogues.size():
        return {}
    var line_value: Variant = dialogues[_line_index]
    if typeof(line_value) != TYPE_DICTIONARY:
        return {}
    return (line_value as Dictionary).duplicate(true)

func advance_line() -> bool:
    if not _started or _ended or _model == null:
        return false
    var dialogues: Array = _model.get_dialogues_for_beat(_current_beat_id)
    if _line_index + 1 >= dialogues.size():
        return false
    _line_index += 1
    return true

func is_waiting_for_choice() -> bool:
    if not _started or _ended or _model == null:
        return false
    var dialogues: Array = _model.get_dialogues_for_beat(_current_beat_id)
    if dialogues.is_empty() or _line_index != dialogues.size() - 1:
        return false
    return not _model.get_choices_for_beat(_current_beat_id).is_empty()

func get_choices() -> Array:
    if not is_waiting_for_choice():
        return []
    return _model.get_choices_for_beat(_current_beat_id)

func choose(choice_id: String) -> Dictionary:
    var event: Dictionary = {
        "ok": false,
        "choice_id": choice_id,
        "transition_kind": "",
        "scene_changed": false,
        "ended": _ended,
        "scene_id": get_current_scene_id(),
        "beat_id": _current_beat_id,
        "error": ""
    }

    if not is_waiting_for_choice():
        return _choice_error(event, "session is not waiting for a choice")

    var choice: Dictionary = _model.get_choice(choice_id)
    if choice.is_empty():
        return _choice_error(event, "unknown choice_id: " + choice_id)
    if _model.get_choice_source_beat(choice_id) != _current_beat_id:
        return _choice_error(event, "choice does not belong to current beat: " + choice_id)

    var transition_kind: String = String(choice.get("transition_kind", ""))
    var source_scene_id: String = get_current_scene_id()
    event["transition_kind"] = transition_kind

    if transition_kind == "END":
        _ended = true
        event["ok"] = true
        event["ended"] = true
        event["scene_id"] = source_scene_id
        event["beat_id"] = _current_beat_id
        _last_error = ""
        return event

    var target_beat_id: String = String(choice.get("target_beat_id", ""))
    var target_scene_id: String = _model.get_scene_id_for_beat(target_beat_id)
    if target_beat_id.is_empty() or target_scene_id.is_empty():
        return _choice_error(event, "choice target is missing: " + choice_id)

    _current_beat_id = target_beat_id
    _line_index = 0
    event["ok"] = true
    event["scene_changed"] = source_scene_id != target_scene_id
    event["ended"] = false
    event["scene_id"] = target_scene_id
    event["beat_id"] = target_beat_id
    _last_error = ""
    return event

func _choice_error(event: Dictionary, message: String) -> Dictionary:
    _last_error = message
    event["error"] = message
    return event

func get_current_beat_id() -> String:
    return _current_beat_id

func get_current_scene_id() -> String:
    if _model == null or _current_beat_id.is_empty():
        return ""
    return _model.get_scene_id_for_beat(_current_beat_id)

func get_current_background_ref() -> String:
    if _model == null or _current_beat_id.is_empty():
        return ""
    return _model.get_background_ref_for_beat(_current_beat_id)

func is_ended() -> bool:
    return _ended

func get_last_error() -> String:
    return _last_error
