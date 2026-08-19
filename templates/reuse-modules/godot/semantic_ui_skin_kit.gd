class_name ReusableSemanticUiSkinKit
extends RefCounted


func resolve(
	semantic_role: String,
	state: String,
	project_skin: Dictionary,
	fallback_role: String = "default"
) -> Dictionary:
	var candidates: Array[Array] = [
		[semantic_role, state],
		[semantic_role, "normal"],
		[fallback_role, state],
		[fallback_role, "normal"],
	]
	for key_pair: Array in candidates:
		var role := str(key_pair[0])
		var state_key := str(key_pair[1])
		if not project_skin.has(role):
			continue
		var role_map: Variant = project_skin[role]
		if role_map is Dictionary and role_map.has(state_key):
			return {
				"ok": true,
				"semantic_role": semantic_role,
				"state": state,
				"resolved_role": role,
				"resolved_state": state_key,
				"token": role_map[state_key],
				"fallback": role != semantic_role or state_key != state,
				"project_skin": project_skin,
			}
	return {
		"ok": false,
		"semantic_role": semantic_role,
		"state": state,
		"fallback": true,
		"project_skin": project_skin,
		"reason": "SEMANTIC_ROLE_STATE_NOT_MAPPED",
	}


func has_mapping(semantic_role: String, state: String, project_skin: Dictionary) -> bool:
	return bool(resolve(semantic_role, state, project_skin).get("ok", false))
