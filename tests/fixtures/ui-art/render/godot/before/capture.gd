# UI 아트 감사 전 화면을 렌더하고 캡처한다.
extends Control

func _ready() -> void:
	await get_tree().create_timer(0.5).timeout
	var image := get_viewport().get_texture().get_image()
	var result := image.save_png(ProjectSettings.globalize_path("res://render.png"))
	if result != OK:
		push_error("render.png 저장 실패: %s" % result)
	get_tree().quit(result)
