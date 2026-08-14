extends SceneTree

var failures: int = 0

func _check(condition: bool, message: String) -> void:
    if condition:
        print("PASS: ", message)
    else:
        failures += 1
        push_error("FAIL: " + message)

func _advance_to_choice(session: RefCounted) -> void:
    while session.advance_line():
        pass

func _initialize() -> void:
    print("NARRATIVE_DIALOGUE_RUNTIME_TEST_START")

    var model_script: Script = load("res://src/dialogue_flow_model.gd")
    _check(model_script != null, "model implementation exists")
    if model_script == null:
        _finish()
        return

    var session_script: Script = load("res://src/dialogue_flow_session.gd")
    _check(session_script != null, "session implementation exists")
    if session_script == null:
        _finish()
        return

    var model: RefCounted = model_script.new()
    var loaded: bool = model.load_from_file("res://data/sample_dialogue.json")
    _check(loaded, "sample JSON loads and validates")
    if not loaded:
        for error in model.get_errors():
            push_error("MODEL_ERROR: " + str(error))
        _finish()
        return

    _check(model.get_entry_beat_id() == "beat_intro", "entry beat is stable")
    _check(model.get_scene_id_for_beat("beat_talk") == "scene_hallway", "same-scene beat indexes correctly")
    _check(model.get_scene_id_for_beat("beat_library") == "scene_library", "moved scene indexes correctly")
    _check(model.get_background_ref_for_beat("beat_intro") == model.get_background_ref_for_beat("beat_talk"), "STAY_IN_SCENE preserves background continuity")

    var session: RefCounted = session_script.new()
    _check(session.start(model), "session starts from model entry")
    _check(session.current_line().get("dialogue_id", "") == "dlg_intro_001", "first dialogue line is addressable by stable id")

    _advance_to_choice(session)
    _check(session.is_waiting_for_choice(), "intro waits for a choice after its final line")
    var stay_event: Dictionary = session.choose("choice_talk")
    _check(stay_event.get("transition_kind", "") == "STAY_IN_SCENE", "stay transition is typed")
    _check(stay_event.get("scene_changed", true) == false, "stay transition does not change scene")
    _check(session.get_current_beat_id() == "beat_talk", "stay transition reaches target beat")

    _advance_to_choice(session)
    var move_event: Dictionary = session.choose("choice_library")
    _check(move_event.get("transition_kind", "") == "MOVE_SCENE", "move transition is typed")
    _check(move_event.get("scene_changed", false) == true, "move transition changes scene")
    _check(session.get_current_scene_id() == "scene_library", "move transition reaches target scene")
    _check(session.current_line().get("dialogue_id", "") == "dlg_library_001", "moved scene begins at target beat first line")

    _advance_to_choice(session)
    var end_event: Dictionary = session.choose("choice_study_end")
    _check(end_event.get("transition_kind", "") == "END", "end transition is typed")
    _check(end_event.get("ended", false) == true, "end transition closes the session")
    _check(session.is_ended(), "session reports terminal state")

    var invalid_data: Dictionary = {
        "format_version": 1,
        "flow_id": "invalid_stay_cross_scene",
        "entry_beat_id": "a",
        "scenes": [
            {"scene_id": "s1", "location_id": "l1", "title": "one", "background_ref": "bg1", "entry_beat_id": "a", "beats": [
                {"beat_id": "a", "title": "a", "dialogues": [{"dialogue_id": "d1", "speaker_id": null, "text": "a"}], "choices": [{"choice_id": "c1", "text": "bad", "target_beat_id": "b", "transition_kind": "STAY_IN_SCENE"}]}
            ]},
            {"scene_id": "s2", "location_id": "l2", "title": "two", "background_ref": "bg2", "entry_beat_id": "b", "beats": [
                {"beat_id": "b", "title": "b", "dialogues": [{"dialogue_id": "d2", "speaker_id": null, "text": "b"}], "choices": []}
            ]}
        ]
    }
    var invalid_model: RefCounted = model_script.new()
    _check(not invalid_model.load_from_dictionary(invalid_data), "cross-scene STAY_IN_SCENE fails closed")

    _finish()

func _finish() -> void:
    if failures == 0:
        print("NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS")
        quit(0)
    else:
        push_error("NARRATIVE_DIALOGUE_RUNTIME_TEST_FAIL count=" + str(failures))
        quit(1)
