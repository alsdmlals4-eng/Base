class_name ReusableGridPlacementRuleEngine
extends RefCounted

const REASON_OUT_OF_BOUNDS := "OUT_OF_BOUNDS"
const REASON_OCCUPIED := "OCCUPIED"
const REASON_PREDICATE_FAILED := "PREDICATE_FAILED"


func evaluate(
	board_size: Vector2i,
	occupied_cells: Dictionary,
	piece_footprint: Array,
	anchor: Vector2i,
	quarter_turns: int = 0,
	placement_context: Dictionary = {},
	project_predicates: Array = []
) -> Dictionary:
	var target_cells: Array[Vector2i] = []
	var reason_codes: Array[String] = []
	var normalized_turns := posmod(quarter_turns, 4)

	for raw_cell: Variant in piece_footprint:
		var local_cell: Vector2i = raw_cell
		var rotated := _rotate(local_cell, normalized_turns)
		var target := anchor + rotated
		target_cells.append(target)
		if target.x < 0 or target.y < 0 or target.x >= board_size.x or target.y >= board_size.y:
			_append_unique(reason_codes, REASON_OUT_OF_BOUNDS)
		elif occupied_cells.has(target):
			_append_unique(reason_codes, REASON_OCCUPIED)

	if reason_codes.is_empty():
		for predicate_variant: Variant in project_predicates:
			if not predicate_variant is Callable:
				continue
			var predicate: Callable = predicate_variant
			var verdict: Variant = predicate.call(target_cells, placement_context)
			if verdict is bool and not verdict:
				_append_unique(reason_codes, REASON_PREDICATE_FAILED)
			elif verdict is Dictionary and not bool(verdict.get("ok", false)):
				var code := str(verdict.get("reason", REASON_PREDICATE_FAILED))
				_append_unique(reason_codes, code)

	return {
		"valid": reason_codes.is_empty(),
		"target_cells": target_cells,
		"reason_codes": reason_codes,
		"preview_payload": {
			"anchor": anchor,
			"rotation_quarter_turns": normalized_turns,
			"target_cells": target_cells,
			"valid": reason_codes.is_empty(),
			"reason_codes": reason_codes,
		},
	}


func _rotate(cell: Vector2i, quarter_turns: int) -> Vector2i:
	var result := cell
	for _turn: int in range(quarter_turns):
		result = Vector2i(-result.y, result.x)
	return result


func _append_unique(items: Array[String], value: String) -> void:
	if not items.has(value):
		items.append(value)
