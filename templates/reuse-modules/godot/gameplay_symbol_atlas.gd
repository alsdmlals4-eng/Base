class_name ReusableGameplaySymbolAtlas
extends RefCounted

const color_is_not_sufficient := true


func resolve(
	symbol_id: String,
	project_symbols: Dictionary,
	fallback_id: String = "unknown"
) -> Dictionary:
	var resolved_id := symbol_id
	var fallback := false
	if not project_symbols.has(resolved_id):
		resolved_id = fallback_id
		fallback = true
	if not project_symbols.has(resolved_id):
		return {
			"ok": false,
			"symbol_id": symbol_id,
			"fallback": true,
			"color_is_not_sufficient": color_is_not_sufficient,
			"reason": "SYMBOL_NOT_MAPPED",
		}

	var descriptor: Variant = project_symbols[resolved_id]
	if not descriptor is Dictionary:
		return {
			"ok": false,
			"symbol_id": symbol_id,
			"fallback": fallback,
			"color_is_not_sufficient": color_is_not_sufficient,
			"reason": "SYMBOL_DESCRIPTOR_NOT_DICTIONARY",
		}

	var shape_cue := str(descriptor.get("shape_cue", ""))
	var text_cue := str(descriptor.get("text_cue", ""))
	if shape_cue.is_empty() or text_cue.is_empty():
		return {
			"ok": false,
			"symbol_id": symbol_id,
			"resolved_id": resolved_id,
			"fallback": fallback,
			"color_is_not_sufficient": color_is_not_sufficient,
			"reason": "REDUNDANT_NON_COLOR_CUE_REQUIRED",
		}

	return {
		"ok": true,
		"symbol_id": symbol_id,
		"resolved_id": resolved_id,
		"fallback": fallback,
		"shape_cue": shape_cue,
		"text_cue": text_cue,
		"icon": descriptor.get("icon"),
		"color_token": descriptor.get("color_token"),
		"color_is_not_sufficient": color_is_not_sufficient,
		"descriptor": descriptor,
	}
