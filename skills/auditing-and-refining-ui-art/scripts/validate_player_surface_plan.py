#!/usr/bin/env python3
"""Validate a derived UI plan, never runtime behavior or approval authenticity.

No network, subprocess, project writes, asset promotion, or capture generation.
Existing project canon is projected into this bounded interchange shape only
when its own validator cannot check the same declared route/state contract.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path, PurePosixPath
from typing import Any

CEILING = 'STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL'
MAX_PACKET_BYTES = 2 * 1024 * 1024
MAX_RECORDS = 10000
KINDS = {'SCREEN', 'PAGE', 'TAB', 'MODAL', 'DIALOGUE', 'PANEL'}
PRODUCTIONS = {'NATIVE_UI', 'REUSE_APPROVED', 'GENERATE_CANDIDATE'}
ASSET_STATES = {'NOT_REQUIRED', 'NEEDED', 'CANDIDATE', 'REVIEWED', 'USER_APPROVED'}
REFERENCE_KINDS = {'OFFICIAL_API', 'SOURCE_CODE', 'PRODUCT_OBSERVATION', 'INTERNAL_REUSE'}
MODULE_ROLES = {'FRAME', 'FILL', 'NAMEPLATE', 'ICON', 'PORTRAIT', 'BACKGROUND', 'PROP', 'SHADOW', 'OVERLAY', 'VFX', 'MASK', 'FLATTENED_STATIC'}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any, *, nonempty: bool = True) -> bool:
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and len(value) <= MAX_RECORDS and all(_text(v) for v in value)
            and len(value) == len(set(value)))


def _enum(value: Any, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices


def _numbers(value: Any, count: int) -> bool:
    return (isinstance(value, list) and len(value) == count
            and all(type(v) in (int, float) and 0 <= v <= 10_000_000
                    and math.isfinite(v) for v in value))


def _safe_consumer_path(value: Any) -> bool:
    if not _text(value) or '\\' in value or '\x00' in value:
        return False
    relative = value[6:] if value.startswith('res://') else value
    return bool(relative) and not PurePosixPath(relative).is_absolute() and ':' not in relative and '..' not in relative.split('/')


def validate_packet(packet: Any, gate: str = 'plan') -> list[str]:
    """Return deterministic errors; a clean result is only structural evidence."""
    errors: list[str] = []
    if not _enum(gate, {'plan', 'handoff'}):
        return ['GATE: expected plan or handoff, not a runtime verification gate']
    if not isinstance(packet, dict):
        return ['PACKET_TYPE: expected object']
    if (type(packet.get('schema_version')) is not int or packet['schema_version'] != 1
            or packet.get('artifact_role') != 'DERIVED_REVIEW_PACKET'
            or not isinstance(packet.get('source_revision'), str)
            or not re.fullmatch(r'[0-9a-f]{40}', packet.get('source_revision', ''))
            or not all(_text(packet.get(k)) for k in ('repository', 'scope_owner', 'approval_ref'))):
        errors.append('SOURCE_IDENTITY: version, derived role, exact revision, owner and approval locator required')

    if packet.get('benchmark_order') != 'EXTERNAL_THEN_PROJECT_FIT':
        errors.append('BENCHMARK_ORDER: external comparison precedes project fit and reuse mapping')
    if packet.get('asset_strategy') != 'MODULAR_PARTS_FIRST':
        errors.append('MODULAR_STRATEGY: independent image parts and named assemblies required')

    def records(name: str) -> list[dict[str, Any]]:
        value = packet.get(name)
        if not isinstance(value, list) or len(value) > MAX_RECORDS:
            errors.append(f'RECORD_TYPE: {name} must be a bounded array'); return []
        result = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f'RECORD_TYPE: {name}[{index}] must be an object')
            else:
                result.append(item)
        return result

    def indexed(name: str) -> dict[str, dict[str, Any]]:
        result = {}
        for row in records(name):
            key = row.get('id')
            if not _text(key) or len(key) > 128 or key == '@exit':
                errors.append(f'RECORD_ID: {name} has invalid or reserved id'); continue
            if key in result:
                errors.append(f'DUPLICATE_ID: {name}/{key}')
            else:
                result[key] = row
        return result

    surfaces = indexed('surfaces')
    actions = indexed('actions')
    families = indexed('visual_families')
    required: dict[str, list[str]] = {}
    for key, rows, code in [('required_surfaces', surfaces, 'MISSING_SURFACE'),
                            ('required_actions', actions, 'MISSING_ACTION')]:
        value = packet.get(key)
        if not _strings(value):
            errors.append(f'SCOPE_DENOMINATOR: {key} needs unique, nonempty IDs')
            required[key] = []
        else:
            required[key] = value
            for item in value:
                if item not in rows:
                    errors.append(f'{code}: {item}')

    entry = packet.get('entry')
    if not _text(entry) or entry not in surfaces:
        errors.append('ENTRY: must identify a declared surface')
        entry = None
    graph = {key: set() for key in surfaces}
    reverse = {key: set() for key in surfaces}
    reverse['@exit'] = set()

    for key, row in surfaces.items():
        if (not _enum(row.get('kind'), KINDS)
                or not all(_text(row.get(f)) for f in ('owner', 'consumer_slot', 'back_policy', 'persistence_policy'))
                or not _strings(row.get('states'))):
            errors.append(f'SURFACE_CONTRACT: {key} needs owner, kind, slot, states, back and persistence policies')
        if not _enum(row.get('consumer_status'), {'PLANNED', 'IMPLEMENTED'}):
            errors.append(f'CONSUMER_STATUS: {key} must distinguish PLANNED from IMPLEMENTED')
        if not _safe_consumer_path(row.get('consumer_path')):
            errors.append(f'UNSAFE_CONSUMER_PATH: {key}')

    for key, row in actions.items():
        source, target = row.get('from'), row.get('to')
        if (not _text(source) or not _text(target) or source not in surfaces
                or (target != '@exit' and target not in surfaces)):
            errors.append(f'DANGLING_ROUTE: {key}')
        else:
            graph[source].add(target); reverse[target].add(source)
        fields = ('trigger', 'command_owner', 'expected_result', 'failure_recovery', 'repeat_policy', 'acceptance_ref')
        if not all(_text(row.get(field)) for field in fields):
            errors.append(f'ACTION_CONTRACT: {key} needs input, owner, result, failure, repeat and acceptance')

    def reachable(starts: list[str], adjacency: dict[str, set[str]]) -> set[str]:
        visited, pending = set(), list(starts)
        while pending:
            item = pending.pop()
            if item not in visited:
                visited.add(item); pending.extend(adjacency.get(item, ()))
        return visited

    if entry is not None:
        reached = reachable([entry], graph)
        can_return = reachable([entry, '@exit'], reverse)
        for key in required['required_surfaces']:
            if key in surfaces and key not in reached:
                errors.append(f'UNREACHABLE_SURFACE: {key}')
            if key in surfaces and key not in can_return:
                errors.append(f'NO_RETURN_OR_EXIT: {key}')

    if entry is not None:
        for action_id in required['required_actions']:
            source = actions.get(action_id, {}).get('from')
            if _text(source) and source in surfaces and source not in reached:
                errors.append(f'UNREACHABLE_ACTION: {action_id}')

    covered = set()
    for family in families.values():
        if _strings(family.get('surfaces')):
            covered.update(family['surfaces'])
    for surface in required['required_surfaces']:
        if surface in surfaces and surface not in covered:
            errors.append(f'MISSING_SURFACE_VISUAL_FAMILY: {surface}')

    if not families:
        errors.append('VISUAL_FAMILY_REQUIRED: declare native/reused/generated component states')
    for key, row in families.items():
        if (not _text(row.get('owner')) or not _text(row.get('kind'))
                or not _strings(row.get('surfaces'))
                or not _strings(row.get('required_states'))):
            errors.append(f'VISUAL_CONTRACT: {key} needs owner, kind, surfaces and required states')
        if _strings(row.get('surfaces')):
            for surface in row['surfaces']:
                if surface not in surfaces:
                    errors.append(f'DANGLING_COMPONENT: {key}/{surface}')
        methods = row.get('state_methods')
        states = row.get('required_states')
        if isinstance(states, list):
            for state in states:
                if not _text(state) or not isinstance(methods, dict) or not _text(methods.get(state)):
                    errors.append(f'MISSING_STATE_METHOD: {key}')
        production, status = row.get('production'), row.get('asset_status')
        if not _enum(production, PRODUCTIONS) or not _enum(status, ASSET_STATES) or not _text(row.get('asset_manifest_ref')):
            errors.append(f'ASSET_CONTRACT: {key}')
        if production == 'NATIVE_UI' and status != 'NOT_REQUIRED':
            errors.append(f'ASSET_CONTRADICTION: {key} native UI is not a new raster approval')
        if production != 'NATIVE_UI' and row.get('asset_manifest_ref') == 'NO_NEW_IMAGE_FILE_REQUIRED':
            errors.append(f'ASSET_CONTRADICTION: {key} raster needs a manifest locator')
        if production != 'NATIVE_UI' and status == 'NOT_REQUIRED':
            errors.append(f'ASSET_CONTRADICTION: {key} raster requirement cannot be NOT_REQUIRED')
        if production == 'REUSE_APPROVED' and status != 'USER_APPROVED':
            errors.append(f'ASSET_CONTRADICTION: {key} approved reuse needs an approval locator')
        if gate == 'handoff' and not _enum(status, {'USER_APPROVED', 'NOT_REQUIRED'}):
            errors.append(f'ASSET_NOT_READY: {key}')
        if row.get('kind') == 'FRAME':
            frame = row.get('frame')
            if (not isinstance(frame, dict) or not _numbers(frame.get('padding'), 4)
                    or not all(_text(frame.get(f)) for f in ('stretch_policy', 'small_size_test'))):
                errors.append(f'FRAME_CONTRACT: {key}')
                continue
            if frame.get('text_is_live') is not True:
                errors.append(f'BAKED_FUNCTIONAL_TEXT: {key}')
            if production != 'NATIVE_UI':
                size, slices = frame.get('source_size'), frame.get('slice')
                if (not _numbers(size, 2) or not _numbers(slices, 4)
                        or size[0] <= 0 or size[1] <= 0
                        or slices[0] + slices[2] >= size[0]
                        or slices[1] + slices[3] >= size[1]):
                    errors.append(f'FRAME_GEOMETRY: {key}')

    references = records('references')
    if not references:
        errors.append('REFERENCE_REQUIRED: cite observed source and concrete adaptation method')
    for index, row in enumerate(references):
        fields = ('source', 'version', 'observed', 'apply', 'reject', 'verification')
        if not _enum(row.get('evidence_kind'), REFERENCE_KINDS) or not all(_text(row.get(f)) for f in fields):
            errors.append(f'REFERENCE_CONTRACT: {index}')
    if not any(_enum(row.get('evidence_kind'), {'SOURCE_CODE', 'PRODUCT_OBSERVATION'}) for row in references):
        errors.append('EXTERNAL_BENCHMARK_REQUIRED: comparable product/source observation, not internal reuse or API alone')

    modules = indexed('modules')
    compositions = indexed('compositions')
    _validate_modules(modules, compositions, families, surfaces, gate, errors)
    return errors


def _validate_modules(modules: dict, compositions: dict, families: dict,
                      surfaces: dict, gate: str, errors: list[str]) -> None:
    """Check declared assembly compatibility; never create or approve an image."""
    for key, module in modules.items():
        if (not all(_text(module.get(f)) for f in ('asset_manifest_ref', 'style_family', 'version'))
                or module.get('asset_manifest_ref') == 'NO_NEW_IMAGE_FILE_REQUIRED'
                or not _enum(module.get('role'), MODULE_ROLES)
                or not _enum(module.get('readiness'), ASSET_STATES - {'NOT_REQUIRED'})
                or not _enum(module.get('alpha'), {'RGBA', 'OPAQUE'})):
            errors.append(f'MODULE_CONTRACT: {key}')
        canvas, anchor = module.get('canvas'), module.get('anchor')
        if (not _numbers(canvas, 2) or not all(type(v) is int for v in canvas) or not _numbers(anchor, 2)
                or min(canvas) <= 0 or max(anchor) > 1):
            errors.append(f'MODULE_GEOMETRY: {key}')
        if module.get('functional_text_baked') is not False:
            errors.append(f'BAKED_FUNCTIONAL_TEXT: module/{key}')
        if module.get('role') == 'FLATTENED_STATIC' and not _text(module.get('flattened_exception')):
            errors.append(f'FLATTENED_EXCEPTION_REQUIRED: {key}')
        if gate == 'handoff' and module.get('readiness') != 'USER_APPROVED':
            errors.append(f'MODULE_NOT_READY: {key}')

    used_by_surface = {key: set() for key in surfaces}
    used_modules: set[str] = set()
    for key, composition in compositions.items():
        surface = composition.get('surface')
        if not _text(surface) or surface not in surfaces:
            errors.append(f'DANGLING_COMPOSITION: {key}')
            surface = None
        if not all(_text(composition.get(f)) for f in ('assembly_owner', 'style_family')):
            errors.append(f'COMPOSITION_CONTRACT: {key}')
        if gate == 'handoff' and not _text(composition.get('approval_ref')):
            errors.append(f'COMPOSITION_NOT_REVIEWED: {key}')
        required = composition.get('required_slots')
        if not _strings(required):
            errors.append(f'COMPOSITION_SLOTS: {key}')
            required = []
        parts = composition.get('parts')
        if not isinstance(parts, list) or len(parts) > MAX_RECORDS:
            errors.append(f'COMPOSITION_PARTS: {key}')
            parts = []
        seen: set[str] = set()
        for part in parts:
            if not isinstance(part, dict):
                errors.append(f'COMPOSITION_PART: {key}'); continue
            slot, module_id = part.get('slot'), part.get('module_id')
            if not _text(slot):
                errors.append(f'COMPOSITION_SLOT: {key}')
            else:
                if slot in seen:
                    errors.append(f'DUPLICATE_SLOT: {key}/{slot}')
                seen.add(slot)
                if slot not in required:
                    errors.append(f'UNDECLARED_COMPOSITION_SLOT: {key}/{slot}')
            if type(part.get('z')) is not int or not -10000 <= part['z'] <= 10000:
                errors.append(f'COMPOSITION_LAYER: {key}')
            if not _text(module_id) or module_id not in modules:
                errors.append(f'MISSING_MODULE: {key}'); continue
            used_modules.add(module_id)
            if surface is not None:
                used_by_surface[surface].add(module_id)
            if modules[module_id].get('style_family') != composition.get('style_family'):
                errors.append(f'STYLE_FAMILY_MISMATCH: {key}/{module_id}')
        for slot in required:
            if slot not in seen:
                errors.append(f'MISSING_COMPOSITION_SLOT: {key}/{slot}')

    for key, family in families.items():
        if family.get('production') == 'NATIVE_UI':
            continue
        module_ids, targets = family.get('module_ids'), family.get('surfaces')
        if not _strings(module_ids):
            errors.append(f'MISSING_MODULE: family/{key}')
            continue
        for module_id in module_ids:
            if module_id not in modules:
                errors.append(f'MISSING_MODULE: {key}/{module_id}')
        if family.get('kind') == 'FRAME' and isinstance(family.get('frame'), dict):
            for module_id in module_ids:
                module = modules.get(module_id, {})
                if module.get('role') == 'FRAME' and module.get('canvas') != family['frame'].get('source_size'):
                    errors.append(f'FRAME_SOURCE_SIZE_MISMATCH: {key}/{module_id}')
        if _strings(targets):
            for target in targets:
                if target not in used_by_surface or not used_by_surface[target]:
                    errors.append(f'MISSING_SURFACE_COMPOSITION: {key}/{target}')
                elif not set(module_ids).issubset(used_by_surface[target]):
                    errors.append(f'MISSING_FAMILY_MODULE_USE: {key}/{target}')
    for key in modules:
        if key not in used_modules:
            errors.append(f'ORPHAN_MODULE: {key}')


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', required=True, type=Path)
    parser.add_argument('--gate', choices=['plan', 'handoff'], default='plan')
    args = parser.parse_args()
    try:
        with args.packet.open('rb') as stream:
            raw = stream.read(MAX_PACKET_BYTES + 1)
        if len(raw) > MAX_PACKET_BYTES:
            raise ValueError('packet exceeds bounded input size')
        def reject_constant(value: str) -> None:
            raise ValueError('non-finite JSON number')
        def finite_float(value: str) -> float:
            number = float(value)
            if not math.isfinite(number):
                raise ValueError('non-finite JSON exponent')
            return number
        packet = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_object,
                            parse_constant=reject_constant, parse_float=finite_float)
        errors = validate_packet(packet, args.gate)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({'result': 'INPUT_ERROR', 'type': type(error).__name__, 'evidence_ceiling': CEILING}))
        return 2
    print(json.dumps({'result': 'STRUCTURE_INVALID' if errors else 'STRUCTURE_VALID',
                      'gate': args.gate, 'errors': errors, 'evidence_ceiling': CEILING}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
