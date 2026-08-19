class_name ReusableCandidateDraftWeightEngine
extends RefCounted

const DUPLICATE_FORBID := "FORBID"
const DUPLICATE_ALLOW := "ALLOW"


func generate(
	pool: Array,
	candidate_count: int,
	seed: int,
	state: Dictionary = {},
	duplicate_policy: String = DUPLICATE_FORBID,
	eligibility: Callable = Callable(),
	weight_modifier: Callable = Callable()
) -> Dictionary:
	var rng := RandomNumberGenerator.new()
	rng.seed = seed
	var working: Array = []
	var reason_trace: Array[Dictionary] = []

	for raw_candidate: Variant in pool:
		if not raw_candidate is Dictionary:
			continue
		var candidate: Dictionary = raw_candidate.duplicate(true)
		var candidate_id := str(candidate.get("id", ""))
		if candidate_id.is_empty():
			reason_trace.append({"id": candidate_id, "decision": "REJECT", "reason": "MISSING_ID"})
			continue
		if eligibility.is_valid() and not bool(eligibility.call(candidate, state)):
			reason_trace.append({"id": candidate_id, "decision": "REJECT", "reason": "INELIGIBLE"})
			continue
		var weight := float(candidate.get("weight", 1.0))
		if weight_modifier.is_valid():
			weight = float(weight_modifier.call(candidate, state, weight))
		if weight <= 0.0:
			reason_trace.append({"id": candidate_id, "decision": "REJECT", "reason": "NON_POSITIVE_WEIGHT"})
			continue
		candidate["_effective_weight"] = weight
		working.append(candidate)

	if working.is_empty():
		return {
			"ok": false,
			"reason": "NO_ELIGIBLE_CANDIDATES",
			"candidates": [],
			"reason_trace": reason_trace,
		}

	var selected: Array[Dictionary] = []
	var count := maxi(candidate_count, 0)
	for slot: int in range(count):
		if working.is_empty():
			break
		var chosen_index := _weighted_index(working, rng)
		if chosen_index < 0:
			break
		var chosen: Dictionary = working[chosen_index].duplicate(true)
		chosen.erase("_effective_weight")
		selected.append(chosen)
		reason_trace.append({"id": str(chosen.get("id", "")), "decision": "SELECT", "slot": slot})
		if duplicate_policy == DUPLICATE_FORBID:
			working.remove_at(chosen_index)

	return {
		"ok": not selected.is_empty() or count == 0,
		"reason": "OK",
		"candidates": selected,
		"seed": seed,
		"duplicate_policy": duplicate_policy,
		"reason_trace": reason_trace,
	}


func _weighted_index(candidates: Array, rng: RandomNumberGenerator) -> int:
	var total := 0.0
	for candidate_variant: Variant in candidates:
		var candidate: Dictionary = candidate_variant
		total += float(candidate.get("_effective_weight", 0.0))
	if total <= 0.0:
		return -1
	var roll := rng.randf() * total
	var cursor := 0.0
	for index: int in range(candidates.size()):
		var candidate: Dictionary = candidates[index]
		cursor += float(candidate.get("_effective_weight", 0.0))
		if roll <= cursor:
			return index
	return candidates.size() - 1
