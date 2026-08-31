"""Structural fixtures only; none is a game/runtime/approval receipt."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/auditing-and-refining-ui-art/scripts/validate_player_surface_plan.py'


def packet():
    return {
        'schema_version': 1,
        'artifact_role': 'DERIVED_REVIEW_PACKET',
        'benchmark_order': 'EXTERNAL_THEN_PROJECT_FIT',
        'asset_strategy': 'MODULAR_PARTS_FIRST',
        'modules': [], 'compositions': [],
        'repository': 'example/fixture-game',
        'source_revision': 'a' * 40,
        'scope_owner': 'docs/game.md#accepted-slice',
        'approval_ref': 'fixture-only-not-real-user-approval',
        'entry': 'title',
        'required_surfaces': ['title', 'settings'],
        'required_actions': ['open', 'back', 'quit'],
        'surfaces': [
            {'id': key, 'kind': 'SCREEN', 'owner': 'docs/ui.md#' + key,
             'consumer_status': 'PLANNED', 'consumer_path': 'res://ui/' + key + '.tscn',
             'consumer_slot': 'Root/Panel', 'states': ['normal'],
             'back_policy': 'Return to title; title quits only on explicit input.',
             'persistence_policy': 'Settings owner stores committed values, UI stores no game progress.'}
            for key in ['title', 'settings']
        ],
        'actions': [
            {'id': key, 'from': source, 'to': target, 'trigger': 'ui_accept',
             'command_owner': 'settings_controller', 'expected_result': 'Destination displayed once.',
             'failure_recovery': 'Keep previous state and show retry.',
             'repeat_policy': 'Reject duplicate pending command.',
             'acceptance_ref': 'tests/' + key}
            for key, source, target in [('open', 'title', 'settings'), ('back', 'settings', 'title'), ('quit', 'title', '@exit')]
        ],
        'visual_families': [
            {'id': 'screen-controls', 'surfaces': ['title', 'settings'], 'owner': 'docs/ui.md#tabs',
             'kind': 'TABS', 'required_states': ['selected', 'focused', 'disabled'],
             'state_methods': {'selected': 'persistent indicator', 'focused': 'focus outline', 'disabled': 'locked reason'},
             'production': 'NATIVE_UI', 'asset_status': 'NOT_REQUIRED',
             'asset_manifest_ref': 'NO_NEW_IMAGE_FILE_REQUIRED'}
        ],
        'references': [
            {'source': 'https://github.com/Anuken/Mindustry/blob/da3b3358cd03e47ef32a87ee5b40231e656d1c76/core/src/mindustry/ui/dialogs/DatabaseDialog.java',
             'evidence_kind': 'SOURCE_CODE', 'version': 'fixture-research-version',
             'observed': 'DatabaseDialog separates search, category selection and unlock state.',
             'apply': 'Use existing tab owner.', 'reject': 'Do not import a second game state.',
             'verification': 'Verify focus and committed option after reopen.'}
        ],
    }


def add_modular_parts(p, status='USER_APPROVED'):
    p['visual_families'][0]['module_ids'] = ['frame']
    p['modules'] = [
        {'id': 'frame', 'asset_manifest_ref': 'assets/manifest.json#frame',
         'style_family': 'fixture-paper-v1', 'role': 'FRAME', 'version': 'v1',
         'canvas': [128, 128], 'anchor': [0.5, 0.5], 'alpha': 'RGBA',
         'functional_text_baked': False, 'readiness': status}
    ]
    p['compositions'] = [
        {'id': 'assembly-' + surface, 'surface': surface,
         'assembly_owner': 'docs/ui.md#' + surface, 'style_family': 'fixture-paper-v1',
         'required_slots': ['frame'], 'approval_ref': 'fixture-only-layout-review',
         'parts': [{'slot': 'frame', 'module_id': 'frame', 'z': 10}]}
        for surface in ['title', 'settings']
    ]
    return p


class SurfacePlanTests(unittest.TestCase):
    def validate(self, value, gate='plan'):
        self.assertTrue(SCRIPT.is_file(), 'Missing executable player-surface plan validator')
        spec = importlib.util.spec_from_file_location('surface_plan_validator', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.validate_packet(value, gate)

    def rejected(self, value, code, gate='plan'):
        self.assertTrue(any(code in error for error in self.validate(value, gate)), code)

    def test_planned_consumers_are_accepted_without_fictitious_runtime_files(self):
        self.assertEqual(self.validate(packet()), [])

    def test_native_ui_handoff_does_not_demand_new_bitmap(self):
        self.assertEqual(self.validate(packet(), 'handoff'), [])

    def test_missing_required_surface_is_not_removed_from_denominator(self):
        p = packet(); p['required_surfaces'].append('codex')
        self.rejected(p, 'MISSING_SURFACE')

    def test_missing_required_action(self):
        p = packet(); p['required_actions'].append('continue')
        self.rejected(p, 'MISSING_ACTION')

    def test_unreachable_page(self):
        p = packet(); p['surfaces'].append({**p['surfaces'][1], 'id': 'codex'})
        p['required_surfaces'].append('codex')
        self.rejected(p, 'UNREACHABLE_SURFACE')

    def test_return_trap(self):
        p = packet(); p['actions'][1]['to'] = 'settings'
        self.rejected(p, 'NO_RETURN_OR_EXIT')

    def test_dangling_route(self):
        p = packet(); p['actions'][0]['to'] = 'missing'
        self.rejected(p, 'DANGLING_ROUTE')

    def test_duplicate_ids(self):
        p = packet(); p['surfaces'].append(copy.deepcopy(p['surfaces'][0]))
        self.rejected(p, 'DUPLICATE_ID')

    def test_dynamic_tab_is_not_a_new_scene_requirement(self):
        p = packet(); p['surfaces'][1]['kind'] = 'TAB'
        p['surfaces'][1]['consumer_path'] = p['surfaces'][0]['consumer_path']
        p['surfaces'][1]['consumer_slot'] = 'Root/Options/Tabs/Audio'
        self.assertEqual(self.validate(p), [])

    def test_missing_back_and_persistence_contract(self):
        p = packet(); p['surfaces'][1]['back_policy'] = ''
        p['surfaces'][1]['persistence_policy'] = ''
        self.rejected(p, 'SURFACE_CONTRACT')

    def test_missing_state_method(self):
        p = packet(); del p['visual_families'][0]['state_methods']['focused']
        self.rejected(p, 'MISSING_STATE_METHOD')

    def test_empty_reference_list_rejected(self):
        p = packet(); p['references'] = []
        self.rejected(p, 'REFERENCE_REQUIRED')

    def test_reference_needs_application_and_negative_boundary(self):
        p = packet(); p['references'][0]['reject'] = ''
        self.rejected(p, 'REFERENCE_CONTRACT')

    def test_candidate_is_valid_planning_but_not_ready_handoff(self):
        p = packet(); family = p['visual_families'][0]
        family.update(production='GENERATE_CANDIDATE', asset_status='CANDIDATE', asset_manifest_ref='docs/assets.md#candidate')
        add_modular_parts(p, status='CANDIDATE')
        self.assertEqual(self.validate(p), [])
        self.rejected(p, 'ASSET_NOT_READY', 'handoff')

    def frame_packet(self):
        p = packet(); family = p['visual_families'][0]
        family.update(kind='FRAME', production='REUSE_APPROVED', asset_status='USER_APPROVED', asset_manifest_ref='assets/manifest.json#frame',
                      frame={'source_size': [128, 128], 'slice': [16, 16, 16, 16], 'padding': [24, 16, 24, 16],
                             'text_is_live': True, 'stretch_policy': 'tile sides; preserve corners', 'small_size_test': 'tests/frame_narrow'})
        add_modular_parts(p)
        return p

    def test_frame_handoff(self):
        self.assertEqual(self.validate(self.frame_packet(), 'handoff'), [])

    def test_frame_without_geometry(self):
        p = self.frame_packet(); del p['visual_families'][0]['frame']
        self.rejected(p, 'FRAME_CONTRACT')

    def test_invalid_nine_slice(self):
        p = self.frame_packet(); p['visual_families'][0]['frame']['slice'] = [80, 16, 80, 16]
        self.rejected(p, 'FRAME_GEOMETRY')

    def test_baked_functional_text(self):
        p = self.frame_packet(); p['visual_families'][0]['frame']['text_is_live'] = False
        self.rejected(p, 'BAKED_FUNCTIONAL_TEXT')

    def test_unknown_lifecycle_value(self):
        p = packet(); p['surfaces'][0]['consumer_status'] = 'RUNTIME_VERIFIED'
        self.rejected(p, 'CONSUMER_STATUS')

    def test_unsafe_path(self):
        p = packet(); p['surfaces'][0]['consumer_path'] = 'res://../secret'
        self.rejected(p, 'UNSAFE_CONSUMER_PATH')

    def test_invalid_top_level(self):
        self.rejected([], 'PACKET_TYPE')

    def test_invalid_nested_type(self):
        p = packet(); p['actions'] = [None]
        self.rejected(p, 'RECORD_TYPE')

    def test_revision_and_role(self):
        p = packet(); p['source_revision'] = 'main'; p['artifact_role'] = 'CANON'
        self.rejected(p, 'SOURCE_IDENTITY')

    def test_no_input_mutation(self):
        p = self.frame_packet(); before = copy.deepcopy(p)
        self.validate(p)
        self.assertEqual(p, before)

    def test_cli_valid_and_broken_packets(self):
        self.assertTrue(SCRIPT.is_file(), 'Missing executable player-surface plan validator')
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'packet.json'
            path.write_text(json.dumps(packet()), encoding='utf-8')
            good = subprocess.run([sys.executable, str(SCRIPT), '--packet', str(path)], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr + good.stdout)
            self.assertIn('STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL', good.stdout)
            p = packet(); p['actions'][0]['to'] = 'missing'
            path.write_text(json.dumps(p), encoding='utf-8')
            bad = subprocess.run([sys.executable, str(SCRIPT), '--packet', str(path)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1, bad.stderr + bad.stdout)

    def test_malformed_enum_fields_report_errors_not_exceptions(self):
        for collection, field in [('surfaces', 'kind'), ('surfaces', 'consumer_status'),
                                  ('visual_families', 'production'), ('visual_families', 'asset_status'),
                                  ('references', 'evidence_kind')]:
            for wrong in [[], {}, True, 123]:
                with self.subTest(collection=collection, field=field, wrong=wrong):
                    p = packet(); p[collection][0][field] = wrong
                    self.assertTrue(self.validate(p))

    def test_missing_required_surface_visual_family(self):
        p = packet(); p['visual_families'][0]['surfaces'] = ['settings']
        self.rejected(p, 'MISSING_SURFACE_VISUAL_FAMILY')

    def test_required_action_on_optional_unreachable_surface(self):
        p = packet(); p['surfaces'].append({**p['surfaces'][1], 'id': 'hidden'})
        p['actions'][2]['from'] = 'hidden'
        self.rejected(p, 'UNREACHABLE_ACTION')

    def test_raster_cannot_claim_no_new_file(self):
        p = self.frame_packet(); p['visual_families'][0]['asset_manifest_ref'] = 'NO_NEW_IMAGE_FILE_REQUIRED'
        self.rejected(p, 'ASSET_CONTRADICTION')

    def test_huge_frame_number_is_rejected_without_overflow(self):
        p = self.frame_packet(); p['visual_families'][0]['frame']['source_size'][0] = 10 ** 1000
        self.rejected(p, 'FRAME_GEOMETRY')

    def test_cli_duplicate_keys_and_nonfinite_numbers(self):
        self.assertTrue(SCRIPT.is_file())
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'packet.json'
            for raw in ['{"schema_version":1,"schema_version":2}', '{"value":NaN}']:
                path.write_text(raw, encoding='utf-8')
                result = subprocess.run([sys.executable, str(SCRIPT), '--packet', str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)

    def test_cli_malformed_json(self):
        self.assertTrue(SCRIPT.is_file(), 'Missing executable player-surface plan validator')
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'packet.json'; path.write_text('{', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--packet', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)

    def test_external_benchmark_first_order_is_explicit(self):
        p = packet(); p['benchmark_order'] = 'PROJECT_FIRST'
        self.rejected(p, 'BENCHMARK_ORDER')

    def test_modular_strategy_is_explicit(self):
        p = packet(); p['asset_strategy'] = 'ONE_FLAT_IMAGE_PER_SCREEN'
        self.rejected(p, 'MODULAR_STRATEGY')

    def test_internal_reuse_alone_does_not_satisfy_external_benchmark(self):
        p = packet(); p['references'][0]['evidence_kind'] = 'INTERNAL_REUSE'
        self.rejected(p, 'EXTERNAL_BENCHMARK_REQUIRED')

    def test_official_api_alone_does_not_replace_comparable_game(self):
        p = packet(); p['references'][0]['evidence_kind'] = 'OFFICIAL_API'
        self.rejected(p, 'EXTERNAL_BENCHMARK_REQUIRED')

    def test_shared_frame_has_two_independent_compositions(self):
        p = self.frame_packet()
        self.assertEqual(len(p['modules']), 1)
        self.assertEqual(len(p['compositions']), 2)
        self.assertEqual(self.validate(p, 'handoff'), [])

    def test_raster_family_requires_actual_module_contract(self):
        p = self.frame_packet(); p['modules'] = []
        self.rejected(p, 'MISSING_MODULE')

    def test_duplicate_module_ids_are_rejected(self):
        p = self.frame_packet(); p['modules'].append(copy.deepcopy(p['modules'][0]))
        self.rejected(p, 'DUPLICATE_ID')

    def test_missing_composition_required_slot(self):
        p = self.frame_packet(); p['compositions'][0]['required_slots'].append('portrait')
        self.rejected(p, 'MISSING_COMPOSITION_SLOT')

    def test_duplicate_slot_is_not_ambiguous(self):
        p = self.frame_packet(); part = copy.deepcopy(p['compositions'][0]['parts'][0])
        p['compositions'][0]['parts'].append(part)
        self.rejected(p, 'DUPLICATE_SLOT')

    def test_incompatible_art_family_rejected(self):
        p = self.frame_packet(); p['modules'][0]['style_family'] = 'unreviewed-other-style'
        self.rejected(p, 'STYLE_FAMILY_MISMATCH')

    def test_module_anchor_outside_canvas_rejected(self):
        p = self.frame_packet(); p['modules'][0]['anchor'] = [1.1, 0.5]
        self.rejected(p, 'MODULE_GEOMETRY')

    def test_baked_text_rejected_for_every_module_not_only_frames(self):
        p = self.frame_packet(); p['modules'][0]['functional_text_baked'] = True
        p['modules'][0]['role'] = 'ICON'
        self.rejected(p, 'BAKED_FUNCTIONAL_TEXT')

    def test_all_raster_surfaces_need_composition(self):
        p = self.frame_packet(); p['compositions'] = p['compositions'][:1]
        self.rejected(p, 'MISSING_SURFACE_COMPOSITION')

    def test_module_approval_does_not_imply_assembly_approval(self):
        p = self.frame_packet(); p['compositions'][0]['approval_ref'] = ''
        self.assertEqual(self.validate(p), [])
        self.rejected(p, 'COMPOSITION_NOT_REVIEWED', 'handoff')

    def test_family_approval_cannot_hide_unapproved_part(self):
        p = self.frame_packet(); p['modules'][0]['readiness'] = 'CANDIDATE'
        self.rejected(p, 'MODULE_NOT_READY', 'handoff')

    def test_flattened_static_art_requires_bounded_exception(self):
        p = self.frame_packet(); p['modules'][0]['role'] = 'FLATTENED_STATIC'
        self.rejected(p, 'FLATTENED_EXCEPTION_REQUIRED')
        p['modules'][0]['flattened_exception'] = 'Single noninteractive event illustration; text and controls remain separate.'
        self.assertEqual(self.validate(p), [])

    def test_json_object_module_ids_do_not_crash(self):
        for field in ['module_id', 'slot']:
            p = self.frame_packet(); p['compositions'][0]['parts'][0][field] = {}
            self.assertTrue(self.validate(p))

    def test_native_only_screens_need_no_new_images_or_compositions(self):
        self.assertEqual(self.validate(packet(), 'handoff'), [])

    def test_unknown_runtime_gate_is_rejected(self):
        self.rejected(packet(), 'GATE', 'runtime')

    def test_invalid_module_enum_reports_error(self):
        for field in ['role', 'readiness', 'alpha']:
            p = self.frame_packet(); p['modules'][0][field] = {}
            self.assertTrue(self.validate(p))

    def test_undeclared_extra_slot_rejected(self):
        p = self.frame_packet(); p['compositions'][0]['parts'].append({'slot': 'extra', 'module_id': 'frame', 'z': 20})
        self.rejected(p, 'UNDECLARED_COMPOSITION_SLOT')

    def test_orphan_module_is_not_counted_as_prepared_work(self):
        p = self.frame_packet(); p['modules'].append({**p['modules'][0], 'id': 'unused'})
        self.rejected(p, 'ORPHAN_MODULE')

    def test_intended_raster_module_is_used_on_each_consumer_surface(self):
        p = self.frame_packet(); p['modules'].append({**p['modules'][0], 'id': 'portrait', 'role': 'PORTRAIT'})
        p['visual_families'][0]['module_ids'].append('portrait')
        first = p['compositions'][0]
        first['required_slots'].append('portrait')
        first['parts'].append({'slot': 'portrait', 'module_id': 'portrait', 'z': 20})
        self.rejected(p, 'MISSING_FAMILY_MODULE_USE')

    def test_image_canvas_requires_integer_pixels(self):
        p = self.frame_packet(); p['modules'][0]['canvas'][0] = 128.5
        self.rejected(p, 'MODULE_GEOMETRY')

    def test_frame_metadata_cannot_disagree_with_frame_part(self):
        p = self.frame_packet(); p['modules'][0]['canvas'][0] = 256
        self.rejected(p, 'FRAME_SOURCE_SIZE_MISMATCH')

    def test_cli_overflow_exponent_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'packet.json'
            raw = json.dumps(packet())[:-1] + ', "irrelevant_number": 1e99999}'
            path.write_text(raw, encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--packet', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
