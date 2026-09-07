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

# Public readback only: diagnostic errors are not domain state.
func _domain_snapshot(session: RefCounted) -> Dictionary:
    return {
        "beat_id": session.get_current_beat_id(),
        "scene_id": session.get_current_scene_id(),
        "background_ref": session.get_current_background_ref(),
        "line": session.current_line(),
        "choices": session.get_choices(),
        "waiting": session.is_waiting_for_choice(),
        "ended": session.is_ended()
    }.duplicate(true)

func _expect_rejected(session: RefCounted, choice_id: String, expected_error: String, label: String) -> void:
    var before: Dictionary = _domain_snapshot(session)
    var event: Dictionary = session.choose(choice_id)
    _check(event.get("ok", true) == false, label + ": rejected")
    _check(event.get("error", "") == expected_error, label + ": precise error")
    _check(session.get_last_error() == expected_error, label + ": diagnostic readback")
    _check(event.get("choice_id", null) == choice_id, label + ": request identity preserved")
    _check(_domain_snapshot(session) == before, label + ": domain state unchanged")
    _check(event.get("beat_id", null) == before["beat_id"] and event.get("scene_id", null) == before["scene_id"] and event.get("ended", null) == before["ended"], label + ": result matches state readback")

func _test_direct_call_boundaries(model: RefCounted, session_script: Script) -> void:
    var session: RefCounted = session_script.new()
    var not_waiting: String = "session is not waiting for a choice"
    _expect_rejected(session, "choice_talk", not_waiting, "before start")
    _check(session.start(model), "direct-call session starts")
    _check(not session.is_waiting_for_choice(), "sample has a pre-choice line")
    _expect_rejected(session, "choice_talk", not_waiting, "premature choice")

    _advance_to_choice(session)
    _check(session.is_waiting_for_choice(), "direct-call fixture reaches choice boundary")
    _expect_rejected(session, "", "unknown choice_id: ", "empty ID")
    _expect_rejected(session, "choice_missing", "unknown choice_id: choice_missing", "unknown ID")
    _expect_rejected(session, "choice_library", "choice does not belong to current beat: choice_library", "foreign beat ID")

    var before_read: Dictionary = _domain_snapshot(session)
    var line_copy: Dictionary = session.current_line()
    line_copy["text"] = "caller-owned edit"
    var choice_copies: Array = session.get_choices()
    _check(not choice_copies.is_empty(), "read-isolation fixture has choices")
    if not choice_copies.is_empty():
        choice_copies[0]["target_beat_id"] = "beat_library"
        choice_copies.clear()
    _check(_domain_snapshot(session) == before_read, "editing read results cannot mutate owned state")

    var event: Dictionary = session.choose("choice_talk")
    _check(event.get("ok", false) and session.get_current_beat_id() == "beat_talk", "valid choice succeeds after rejected calls")
    _check(event.get("error", "missing").is_empty() and session.get_last_error().is_empty(), "valid choice clears old diagnostics")
    _check(event.get("beat_id", "") == session.get_current_beat_id() and event.get("scene_id", "") == session.get_current_scene_id(), "successful result matches state readback")
    event["beat_id"] = "caller-owned-result-edit"
    _check(session.get_current_beat_id() == "beat_talk", "editing event does not mutate session")
    _expect_rejected(session, "choice_talk", not_waiting, "immediate replay")
    _advance_to_choice(session)
    _expect_rejected(session, "choice_talk", "choice does not belong to current beat: choice_talk", "stale ID at next boundary")

    event = session.choose("choice_library")
    _check(event.get("ok", false) and session.get_current_scene_id() == "scene_library", "normal scene move still succeeds")
    _advance_to_choice(session)
    event = session.choose("choice_study_end")
    _check(event.get("ok", false) and session.is_ended(), "normal explicit END still succeeds")
    _expect_rejected(session, "choice_study_end", not_waiting, "terminal replay")
    var terminal: Dictionary = _domain_snapshot(session)
    _check(not session.advance_line(), "terminal line advance rejected")
    _check(_domain_snapshot(session) == terminal, "terminal line rejection preserves state")
    _check(session.current_line().is_empty() and session.get_choices().is_empty(), "terminal readback exposes no actionable choices")

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
                {"beat_id": "b", "title": "b", "dialogues": [{"dialogue_id": "d2", "speaker_id": null, "text": "b"}], "choices": [{"choice_id": "c2", "text": "end", "target_beat_id": null, "transition_kind": "END"}]}
            ]}
        ]
    }
    var invalid_model: RefCounted = model_script.new()
    _check(not invalid_model.load_from_dictionary(invalid_data), "cross-scene STAY_IN_SCENE fails closed")

    var dead_end_data: Dictionary = {
        "format_version": 1,
        "flow_id": "invalid_dead_end",
        "entry_beat_id": "dead",
        "scenes": [
            {"scene_id": "s_dead", "location_id": "l_dead", "title": "dead", "background_ref": "bg_dead", "entry_beat_id": "dead", "beats": [
                {"beat_id": "dead", "title": "dead", "dialogues": [{"dialogue_id": "d_dead", "speaker_id": null, "text": "dead"}], "choices": []}
            ]}
        ]
    }
    var dead_end_model: RefCounted = model_script.new()
    _check(not dead_end_model.load_from_dictionary(dead_end_data), "beat without explicit END or transition fails closed")

    _test_direct_call_boundaries(model, session_script)
    _finish()

func _finish() -> void:
    if failures == 0:
        print("NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS")
        quit(0)
    else:
        push_error("NARRATIVE_DIALOGUE_RUNTIME_TEST_FAIL count=" + str(failures))
        quit(1)
