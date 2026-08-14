extends Control

const DialogueFlowModel = preload("res://src/dialogue_flow_model.gd")
const DialogueFlowSession = preload("res://src/dialogue_flow_session.gd")

var model = DialogueFlowModel.new()
var session = DialogueFlowSession.new()

var background: ColorRect
var location_label: Label
var beat_label: Label
var speaker_label: Label
var dialogue_label: Label
var choices_box: VBoxContainer
var status_label: Label
var next_button: Button

func _ready() -> void:
    _build_ui()
    if not model.load_from_file("res://data/sample_dialogue.json"):
        _show_fatal("Dialogue data validation failed:\n" + "\n".join(model.get_errors()))
        return
    if not session.start(model):
        _show_fatal("Dialogue session failed to start: " + session.get_last_error())
        return
    _refresh_view()
    print("NARRATIVE_DIALOGUE_SAMPLE_READY flow=%s beat=%s scene=%s" % [model.get_flow_id(), session.get_current_beat_id(), session.get_current_scene_id()])

func _build_ui() -> void:
    background = ColorRect.new()
    background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    add_child(background)

    var margin := MarginContainer.new()
    margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    margin.add_theme_constant_override("margin_left", 48)
    margin.add_theme_constant_override("margin_right", 48)
    margin.add_theme_constant_override("margin_top", 36)
    margin.add_theme_constant_override("margin_bottom", 36)
    add_child(margin)

    var root_box := VBoxContainer.new()
    root_box.add_theme_constant_override("separation", 14)
    margin.add_child(root_box)

    location_label = Label.new()
    location_label.add_theme_font_size_override("font_size", 16)
    root_box.add_child(location_label)

    beat_label = Label.new()
    beat_label.add_theme_font_size_override("font_size", 28)
    root_box.add_child(beat_label)

    var spacer := Control.new()
    spacer.custom_minimum_size = Vector2(0, 150)
    spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
    root_box.add_child(spacer)

    var dialogue_panel := PanelContainer.new()
    dialogue_panel.custom_minimum_size = Vector2(0, 190)
    root_box.add_child(dialogue_panel)

    var dialogue_margin := MarginContainer.new()
    dialogue_margin.add_theme_constant_override("margin_left", 24)
    dialogue_margin.add_theme_constant_override("margin_right", 24)
    dialogue_margin.add_theme_constant_override("margin_top", 20)
    dialogue_margin.add_theme_constant_override("margin_bottom", 20)
    dialogue_panel.add_child(dialogue_margin)

    var dialogue_box := VBoxContainer.new()
    dialogue_box.add_theme_constant_override("separation", 10)
    dialogue_margin.add_child(dialogue_box)

    speaker_label = Label.new()
    speaker_label.add_theme_font_size_override("font_size", 17)
    dialogue_box.add_child(speaker_label)

    dialogue_label = Label.new()
    dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    dialogue_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
    dialogue_label.add_theme_font_size_override("font_size", 22)
    dialogue_box.add_child(dialogue_label)

    next_button = Button.new()
    next_button.text = "다음"
    next_button.pressed.connect(_on_next_pressed)
    dialogue_box.add_child(next_button)

    choices_box = VBoxContainer.new()
    choices_box.add_theme_constant_override("separation", 8)
    dialogue_box.add_child(choices_box)

    status_label = Label.new()
    status_label.add_theme_font_size_override("font_size", 12)
    root_box.add_child(status_label)

func _refresh_view() -> void:
    if session.is_ended():
        _clear_choices()
        next_button.visible = false
        speaker_label.text = "END"
        dialogue_label.text = "샘플 대화 흐름이 종료되었습니다."
        status_label.text = "session=ENDED"
        return

    var beat: Dictionary = model.get_beat(session.get_current_beat_id())
    var scene: Dictionary = model.get_scene(session.get_current_scene_id())
    var line: Dictionary = session.current_line()

    location_label.text = "%s · %s" % [String(scene.get("location_id", "")), session.get_current_scene_id()]
    beat_label.text = String(beat.get("title", session.get_current_beat_id()))
    var speaker: Variant = line.get("speaker_id", null)
    speaker_label.text = "내레이션" if speaker == null else String(speaker)
    dialogue_label.text = String(line.get("text", ""))
    status_label.text = "beat=%s  dialogue=%s  background=%s" % [session.get_current_beat_id(), String(line.get("dialogue_id", "")), session.get_current_background_ref()]
    _apply_scene_visual(session.get_current_scene_id())

    _clear_choices()
    if session.is_waiting_for_choice():
        next_button.visible = false
        for choice_value in session.get_choices():
            if typeof(choice_value) != TYPE_DICTIONARY:
                continue
            var choice: Dictionary = choice_value
            var button := Button.new()
            button.text = "%s  [%s]" % [String(choice.get("text", "")), String(choice.get("transition_kind", ""))]
            button.pressed.connect(_on_choice_pressed.bind(String(choice.get("choice_id", ""))))
            choices_box.add_child(button)
    else:
        next_button.visible = true

func _on_next_pressed() -> void:
    session.advance_line()
    _refresh_view()

func _on_choice_pressed(choice_id: String) -> void:
    var event: Dictionary = session.choose(choice_id)
    if not bool(event.get("ok", false)):
        status_label.text = "ERROR: " + String(event.get("error", "choice failed"))
        return
    print("NARRATIVE_DIALOGUE_CHOICE choice=%s transition=%s beat=%s scene=%s ended=%s" % [choice_id, String(event.get("transition_kind", "")), String(event.get("beat_id", "")), String(event.get("scene_id", "")), str(event.get("ended", false))])
    _refresh_view()

func _clear_choices() -> void:
    for child in choices_box.get_children():
        child.queue_free()

func _apply_scene_visual(scene_id: String) -> void:
    match scene_id:
        "scene_hallway":
            background.color = Color("17132b")
        "scene_classroom":
            background.color = Color("101d2b")
        "scene_library":
            background.color = Color("2b1b12")
        _:
            background.color = Color("0b0b13")

func _show_fatal(message: String) -> void:
    next_button.visible = false
    _clear_choices()
    speaker_label.text = "ERROR"
    dialogue_label.text = message
    status_label.text = "runtime initialization failed"
    push_error(message)
