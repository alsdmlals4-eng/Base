# 목적 있는 보스 경고 색상을 검증하는 감사 fixture다.
# base-ui-audit: allow G-E-COLOR-LITERAL reason=게임플레이 위험 상태에만 쓰는 승인된 색상
extends Control

func apply_warning() -> void:
	add_theme_color_override("font_color", Color(1.0, 0.12, 0.05, 1.0))
