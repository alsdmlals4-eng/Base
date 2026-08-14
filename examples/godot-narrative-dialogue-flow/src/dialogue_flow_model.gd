extends RefCounted

const FORMAT_VERSION: int = 1
const VALID_TRANSITIONS: Array[String] = ["STAY_IN_SCENE", "MOVE_SCENE", "END"]

var _data: Dictionary = {}
var _errors: PackedStringArray = PackedStringArray()
var _scene_by_id: Dictionary = {}
var _beat_by_id: Dictionary = {}
var _scene_id_by_beat: Dictionary = {}
var _dialogue_by_id: Dictionary = {}
var _choice_by_id: Dictionary = {}
var _choice_source_beat: Dictionary = {}

func load_from_file(path: String) -> bool:
    _reset()
    if not FileAccess.file_exists(path):
        _errors.append("dialogue file not found: " + path)
        return false

    var file: FileAccess = FileAccess.open(path, FileAccess.READ)
    if file == null:
        _errors.append("dialogue file could not be opened: " + path)
        return false

    var parser: JSON = JSON.new()
    var parse_result: Error = parser.parse(file.get_as_text())
    if parse_result != OK:
        _errors.append("invalid JSON at line %d: %s" % [parser.get_error_line(), parser.get_error_message()])
        return false

    if typeof(parser.data) != TYPE_DICTIONARY:
        _errors.append("dialogue root must be a JSON object")
        return false

    return load_from_dictionary(parser.data)

func load_from_dictionary(data: Dictionary) -> bool:
    _reset()
    _data = data.duplicate(true)

    if int(_data.get("format_version", -1)) != FORMAT_VERSION:
        _errors.append("format_version must be %d" % FORMAT_VERSION)

    _require_string(_data, "flow_id", "root")
    var entry_beat_id: String = _require_string(_data, "entry_beat_id", "root")

    var scenes_value: Variant = _data.get("scenes", null)
    if typeof(scenes_value) != TYPE_ARRAY or scenes_value.is_empty():
        _errors.append("root.scenes must be a non-empty array")
        return false

    for scene_index in range(scenes_value.size()):
        var scene_value: Variant = scenes_value[scene_index]
        if typeof(scene_value) != TYPE_DICTIONARY:
            _errors.append("root.scenes[%d] must be an object" % scene_index)
            continue
        var scene: Dictionary = scene_value
        var scene_context: String = "root.scenes[%d]" % scene_index
        var scene_id: String = _require_string(scene, "scene_id", scene_context)
        _require_string(scene, "location_id", scene_context)
        _require_string(scene, "title", scene_context)
        _require_string(scene, "background_ref", scene_context)
        _require_string(scene, "entry_beat_id", scene_context)

        if not scene_id.is_empty():
            if _scene_by_id.has(scene_id):
                _errors.append("duplicate scene_id: " + scene_id)
            else:
                _scene_by_id[scene_id] = scene

        var beats_value: Variant = scene.get("beats", null)
        if typeof(beats_value) != TYPE_ARRAY or beats_value.is_empty():
            _errors.append(scene_context + ".beats must be a non-empty array")
            continue

        for beat_index in range(beats_value.size()):
            var beat_value: Variant = beats_value[beat_index]
            if typeof(beat_value) != TYPE_DICTIONARY:
                _errors.append("%s.beats[%d] must be an object" % [scene_context, beat_index])
                continue
            var beat: Dictionary = beat_value
            var beat_context: String = "%s.beats[%d]" % [scene_context, beat_index]
            var beat_id: String = _require_string(beat, "beat_id", beat_context)
            _require_string(beat, "title", beat_context)

            if not beat_id.is_empty():
                if _beat_by_id.has(beat_id):
                    _errors.append("duplicate beat_id: " + beat_id)
                else:
                    _beat_by_id[beat_id] = beat
                    _scene_id_by_beat[beat_id] = scene_id

            _index_dialogues(beat, beat_id, beat_context)
            _index_choices(beat, beat_id, beat_context)

    if not entry_beat_id.is_empty() and not _beat_by_id.has(entry_beat_id):
        _errors.append("entry_beat_id does not exist: " + entry_beat_id)

    _validate_scene_entries()
    _validate_choice_targets()
    return _errors.is_empty()

func _index_dialogues(beat: Dictionary, beat_id: String, context: String) -> void:
    var dialogues_value: Variant = beat.get("dialogues", null)
    if typeof(dialogues_value) != TYPE_ARRAY or dialogues_value.is_empty():
        _errors.append(context + ".dialogues must be a non-empty array")
        return

    for dialogue_index in range(dialogues_value.size()):
        var dialogue_value: Variant = dialogues_value[dialogue_index]
        if typeof(dialogue_value) != TYPE_DICTIONARY:
            _errors.append("%s.dialogues[%d] must be an object" % [context, dialogue_index])
            continue
        var dialogue: Dictionary = dialogue_value
        var dialogue_context: String = "%s.dialogues[%d]" % [context, dialogue_index]
        var dialogue_id: String = _require_string(dialogue, "dialogue_id", dialogue_context)
        _require_string(dialogue, "text", dialogue_context)

        var speaker_value: Variant = dialogue.get("speaker_id", null)
        if speaker_value != null and typeof(speaker_value) != TYPE_STRING:
            _errors.append(dialogue_context + ".speaker_id must be a string or null")

        if not dialogue_id.is_empty():
            if _dialogue_by_id.has(dialogue_id):
                _errors.append("duplicate dialogue_id: " + dialogue_id)
            else:
                _dialogue_by_id[dialogue_id] = dialogue

func _index_choices(beat: Dictionary, beat_id: String, context: String) -> void:
    var choices_value: Variant = beat.get("choices", null)
    if typeof(choices_value) != TYPE_ARRAY:
        _errors.append(context + ".choices must be an array")
        return

    for choice_index in range(choices_value.size()):
        var choice_value: Variant = choices_value[choice_index]
        if typeof(choice_value) != TYPE_DICTIONARY:
            _errors.append("%s.choices[%d] must be an object" % [context, choice_index])
            continue
        var choice: Dictionary = choice_value
        var choice_context: String = "%s.choices[%d]" % [context, choice_index]
        var choice_id: String = _require_string(choice, "choice_id", choice_context)
        _require_string(choice, "text", choice_context)
        var transition_kind: String = _require_string(choice, "transition_kind", choice_context)
        if not transition_kind.is_empty() and not VALID_TRANSITIONS.has(transition_kind):
            _errors.append(choice_context + ".transition_kind is invalid: " + transition_kind)

        if not choice_id.is_empty():
            if _choice_by_id.has(choice_id):
                _errors.append("duplicate choice_id: " + choice_id)
            else:
                _choice_by_id[choice_id] = choice
                _choice_source_beat[choice_id] = beat_id

func _validate_scene_entries() -> void:
    for scene_id_value in _scene_by_id.keys():
        var scene_id: String = String(scene_id_value)
        var scene: Dictionary = _scene_by_id[scene_id]
        var scene_entry: String = String(scene.get("entry_beat_id", ""))
        if not _beat_by_id.has(scene_entry):
            _errors.append("scene %s entry_beat_id does not exist: %s" % [scene_id, scene_entry])
        elif String(_scene_id_by_beat.get(scene_entry, "")) != scene_id:
            _errors.append("scene %s entry_beat_id belongs to another scene: %s" % [scene_id, scene_entry])

func _validate_choice_targets() -> void:
    for choice_id_value in _choice_by_id.keys():
        var choice_id: String = String(choice_id_value)
        var choice: Dictionary = _choice_by_id[choice_id]
        var transition_kind: String = String(choice.get("transition_kind", ""))
        var source_beat_id: String = String(_choice_source_beat.get(choice_id, ""))
        var source_scene_id: String = String(_scene_id_by_beat.get(source_beat_id, ""))
        var target_value: Variant = choice.get("target_beat_id", null)

        if transition_kind == "END":
            if target_value != null and String(target_value) != "":
                _errors.append("END choice %s must not have a target_beat_id" % choice_id)
            continue

        if transition_kind != "STAY_IN_SCENE" and transition_kind != "MOVE_SCENE":
            continue
        if typeof(target_value) != TYPE_STRING or String(target_value).is_empty():
            _errors.append("choice %s requires a target_beat_id" % choice_id)
            continue

        var target_beat_id: String = String(target_value)
        if not _beat_by_id.has(target_beat_id):
            _errors.append("choice %s target_beat_id does not exist: %s" % [choice_id, target_beat_id])
            continue

        var target_scene_id: String = String(_scene_id_by_beat.get(target_beat_id, ""))
        if transition_kind == "STAY_IN_SCENE" and source_scene_id != target_scene_id:
            _errors.append("STAY_IN_SCENE choice %s crosses scenes (%s -> %s)" % [choice_id, source_scene_id, target_scene_id])
        elif transition_kind == "MOVE_SCENE" and source_scene_id == target_scene_id:
            _errors.append("MOVE_SCENE choice %s stays inside scene %s" % [choice_id, source_scene_id])

func _require_string(object: Dictionary, key: String, context: String) -> String:
    var value: Variant = object.get(key, null)
    if typeof(value) != TYPE_STRING or String(value).is_empty():
        _errors.append(context + "." + key + " must be a non-empty string")
        return ""
    return String(value)

func _reset() -> void:
    _data = {}
    _errors = PackedStringArray()
    _scene_by_id = {}
    _beat_by_id = {}
    _scene_id_by_beat = {}
    _dialogue_by_id = {}
    _choice_by_id = {}
    _choice_source_beat = {}

func get_errors() -> PackedStringArray:
    return _errors.duplicate()

func get_flow_id() -> String:
    return String(_data.get("flow_id", ""))

func get_entry_beat_id() -> String:
    return String(_data.get("entry_beat_id", ""))

func get_beat(beat_id: String) -> Dictionary:
    if not _beat_by_id.has(beat_id):
        return {}
    return (_beat_by_id[beat_id] as Dictionary).duplicate(true)

func get_dialogues_for_beat(beat_id: String) -> Array:
    var beat: Dictionary = get_beat(beat_id)
    if beat.is_empty():
        return []
    return (beat.get("dialogues", []) as Array).duplicate(true)

func get_choices_for_beat(beat_id: String) -> Array:
    var beat: Dictionary = get_beat(beat_id)
    if beat.is_empty():
        return []
    return (beat.get("choices", []) as Array).duplicate(true)

func get_choice(choice_id: String) -> Dictionary:
    if not _choice_by_id.has(choice_id):
        return {}
    return (_choice_by_id[choice_id] as Dictionary).duplicate(true)

func get_choice_source_beat(choice_id: String) -> String:
    return String(_choice_source_beat.get(choice_id, ""))

func get_scene_id_for_beat(beat_id: String) -> String:
    return String(_scene_id_by_beat.get(beat_id, ""))

func get_scene(scene_id: String) -> Dictionary:
    if not _scene_by_id.has(scene_id):
        return {}
    return (_scene_by_id[scene_id] as Dictionary).duplicate(true)

func get_background_ref_for_beat(beat_id: String) -> String:
    var scene_id: String = get_scene_id_for_beat(beat_id)
    var scene: Dictionary = get_scene(scene_id)
    return String(scene.get("background_ref", ""))
