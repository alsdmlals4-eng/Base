extends SceneTree

# Exercise the existing scene through Godot's GUI input dispatcher, not pressed.emit().
# The explicit rejection probe below is a handler-boundary test, not a user gesture.
const MainScene = preload("res://main.tscn")
const SessionScript = preload("res://src/dialogue_flow_session.gd")

var failures: int = 0
var assertions: int = 0

func _initialize() -> void:
    call_deferred("_run")

func _check(condition: bool, message: String) -> void:
    assertions += 1
    if condition:
        print("PASS: ", message)
    else:
        failures += 1
        push_error("FAIL: " + message)

func _snapshot(session: RefCounted) -> Dictionary:
    return {
        "beat_id": session.get_current_beat_id(),
        "scene_id": session.get_current_scene_id(),
        "background_ref": session.get_current_background_ref(),
        "line": session.current_line(),
        "choices": session.get_choices(),
        "waiting": session.is_waiting_for_choice(),
        "ended": session.is_ended()
    }.duplicate(true)

func _settle() -> void:
    await process_frame
    await process_frame

func _tap_key(keycode: Key, shift: bool = false) -> void:
    var down := InputEventKey.new()
    down.keycode = keycode
    down.physical_keycode = keycode
    down.shift_pressed = shift
    down.pressed = true
    root.push_input(down, true)
    var up := InputEventKey.new()
    up.keycode = keycode
    up.physical_keycode = keycode
    up.shift_pressed = shift
    up.pressed = false
    root.push_input(up, true)

func _click(button: Button) -> void:
    _check(button.is_visible_in_tree() and not button.disabled, "pointer target is actionable")
    var position: Vector2 = button.get_global_rect().get_center()
    var down := InputEventMouseButton.new()
    down.position = position
    down.global_position = position
    down.button_index = MOUSE_BUTTON_LEFT
    down.button_mask = MOUSE_BUTTON_MASK_LEFT
    down.pressed = true
    root.push_input(down, true)
    var up := InputEventMouseButton.new()
    up.position = position
    up.global_position = position
    up.button_index = MOUSE_BUTTON_LEFT
    up.pressed = false
    root.push_input(up, true)

func _capture(name: String) -> void:
    var directory: String = OS.get_environment("EVIDENCE_DIR")
    if directory.is_empty() or DisplayServer.get_name() == "headless":
        print("UI_CAPTURE_NOT_RUN: ", name)
        return
    await RenderingServer.frame_post_draw
    var image: Image = root.get_texture().get_image()
    _check(not image.is_empty(), "render capture contains pixels: " + name)
    if not image.is_empty():
        var error: Error = image.save_png(directory.path_join(name + ".png"))
        _check(error == OK, "render capture saved: " + name)

func _run() -> void:
    print("NARRATIVE_DIALOGUE_UI_TEST_START")
    root.size = Vector2i(1280, 720)
    var view = MainScene.instantiate()
    root.add_child(view)
    await _settle()
    var direct: RefCounted = SessionScript.new()
    _check(direct.start(view.model), "independent direct-call session starts")
    _check(_snapshot(view.session) == _snapshot(direct), "UI and direct initial state agree")
    _check(root.gui_get_focus_owner() == view.next_button, "initial keyboard focus targets Next")
    await _capture("01-initial")

    # Pointer input proves that the actual Button, handler and session are connected.
    _click(view.next_button)
    _check(direct.advance_line(), "direct line advance succeeds")
    await _settle()
    _check(_snapshot(view.session) == _snapshot(direct), "pointer Next matches direct state")
    if not view.session.is_waiting_for_choice():
        await _close_and_finish(view)
        return
    _check(view.choices_box.get_child_count() == direct.get_choices().size(), "choice controls match current domain choices")
    _check(root.gui_get_focus_owner() == view.choices_box.get_child(0), "choice replacement restores first meaningful focus")

    # No frame passes here: deferred deletion must not leave obsolete controls in the live UI.
    var old_controls: Array[Node] = view.choices_box.get_children()
    var before_refresh: Dictionary = _snapshot(view.session)
    view._refresh_view()
    view._refresh_view()
    _check(view.choices_box.get_child_count() == direct.get_choices().size(), "same-frame refresh does not accumulate choice controls")
    for old_control in old_controls:
        _check(not old_control.is_inside_tree(), "replaced choice leaves the input tree immediately")
    _check(_snapshot(view.session) == before_refresh, "refresh does not mutate domain state")
    await _settle()
    await _capture("02-choices")

    # No test-side grab_focus rescue: these keys must use production focus management.
    _tap_key(KEY_TAB)
    _check(root.gui_get_focus_owner() == view.choices_box.get_child(1), "Tab reaches the second current choice")
    _tap_key(KEY_TAB, true)
    _check(root.gui_get_focus_owner() == view.choices_box.get_child(0), "Shift-Tab returns to the first current choice")
    _tap_key(KEY_ENTER)
    var event: Dictionary = direct.choose("choice_talk")
    _check(bool(event.get("ok", false)), "direct STAY choice succeeds")
    await _settle()
    _check(_snapshot(view.session) == _snapshot(direct), "keyboard choice matches direct STAY state")
    if view.session.get_current_beat_id() != "beat_talk":
        await _close_and_finish(view)
        return
    _check(root.gui_get_focus_owner() == view.next_button, "choice to line restores Next focus")
    _check(view.choices_box.get_child_count() == 0, "old choices are absent in line view")
    await _capture("03-stay-result")

    _tap_key(KEY_ENTER)
    _check(direct.advance_line(), "direct second beat line advance succeeds")
    await _settle()
    _check(_snapshot(view.session) == _snapshot(direct), "keyboard Next matches direct second choice boundary")
    _tap_key(KEY_ENTER)
    event = direct.choose("choice_library")
    _check(bool(event.get("ok", false)), "direct MOVE choice succeeds")
    await _settle()
    _check(_snapshot(view.session) == _snapshot(direct), "keyboard MOVE matches direct scene and background")
    if view.session.get_current_scene_id() != "scene_library":
        await _close_and_finish(view)
        return
    _tap_key(KEY_ENTER)
    _check(direct.advance_line(), "direct library line advance succeeds")
    await _settle()

    # Fault injection is deliberately labeled separately from real GUI input coverage.
    var before_rejection: Dictionary = _snapshot(view.session)
    view._on_choice_pressed("choice_talk")
    event = direct.choose("choice_talk")
    _check(not bool(event.get("ok", true)), "stale handler-boundary choice is rejected")
    _check(_snapshot(view.session) == before_rejection, "handler rejection preserves domain state")
    _check(_snapshot(view.session) == _snapshot(direct), "UI-handler and direct rejection agree")
    _check(view.status_label.text == "ERROR: " + String(event.get("error", "")), "rejection diagnostic reflects the domain result")
    _check(root.gui_get_focus_owner() == view.choices_box.get_child(0), "rejection preserves a valid recovery focus")
    await _capture("04-rejected-action")

    _tap_key(KEY_ENTER)
    event = direct.choose("choice_study_end")
    _check(bool(event.get("ok", false)), "direct END after rejection succeeds")
    await _settle()
    _check(_snapshot(view.session) == _snapshot(direct), "keyboard recovery reaches the same terminal state")
    _check(view.status_label.text == "session=ENDED", "successful recovery replaces error feedback")
    _check(view.choices_box.get_child_count() == 0 and not view.next_button.visible, "terminal UI has no actionable controls")
    var terminal: Dictionary = _snapshot(view.session)
    _tap_key(KEY_ENTER)
    await _settle()
    _check(_snapshot(view.session) == terminal, "terminal keyboard repeat cannot mutate state")
    await _capture("05-ended")

    root.remove_child(view)
    view.queue_free()
    await _settle()
    view = MainScene.instantiate()
    root.add_child(view)
    await _settle()
    _check(view.session.get_current_beat_id() == "beat_intro" and not view.session.is_ended(), "fresh scene reentry starts the existing sample normally")
    _check(view.choices_box.get_child_count() == 0, "reentry retains no previous choice controls")
    _check(root.gui_get_focus_owner() == view.next_button, "reentry restores meaningful keyboard focus")
    await _capture("06-reentry")
    await _close_and_finish(view)

func _close_and_finish(view: Node) -> void:
    if view.get_parent() != null:
        view.get_parent().remove_child(view)
    view.queue_free()
    await _settle()
    print("NARRATIVE_DIALOGUE_UI_ASSERTIONS count=%d failures=%d" % [assertions, failures])
    if failures == 0:
        print("NARRATIVE_DIALOGUE_UI_TEST_PASS")
        quit(0)
    else:
        print("NARRATIVE_DIALOGUE_UI_TEST_FAIL count=%d" % failures)
        quit(1)
