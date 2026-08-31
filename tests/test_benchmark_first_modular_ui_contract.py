"""Workflow/document regressions. They do not execute or approve a game UI."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = 'skills/auditing-and-refining-ui-art/references/ui-surface-production-readiness.md'

REQUIREMENTS = (
    'BENCHMARK_FIRST: establish the external interaction and implementation pattern before auditing project gaps.',
    'RECONCILE_BEFORE_MUTATION: external findings are candidates until current project authority, approved assets and consumers have been read.',
    'SEPARATE_MODULE_MASTERS: author each reusable image module as an independent source file; compose screens from module references.',
    'ATLAS_IS_DERIVED_PACKAGING: an atlas is a build/import derivative, not the only editable master or an image-model collage deliverable.',
    'COMPOSITION_IS_NOT_NEW_ART: reuse compatible module versions instead of regenerating a complete screen for each combination.',
    'TEXT_AND_ACTIONS_STAY_LIVE: localized text, numbers, hit targets and callbacks remain runtime controls, not baked image content.',
    'REUSE_WITHIN_APPROVED_FAMILY: share technical structure across projects, not unapproved palettes, motifs or character identities.',
    'COMPOSITION_COVERAGE_IS_BOUNDED: test declared consumers and distinct risky combinations, not an unbounded Cartesian product.',
    'NO_PROMOTION_BY_ASSEMBLY: assembling candidate modules does not approve their pixels, replace locked assets or prove runtime behavior.',
)


def missing_requirements(text):
    return [sentence for sentence in REQUIREMENTS if sentence not in text]


class BenchmarkFirstModularUiContract(unittest.TestCase):
    def source(self):
        self.assertTrue((ROOT / REFERENCE).is_file(), 'Missing modular UI workflow reference')
        return (ROOT / REFERENCE).read_text(encoding='utf-8')

    def test_bootstrap_explicitly_routes_to_reference(self):
        self.assertIn(REFERENCE, (ROOT / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_benchmark_precedes_project_gap_analysis(self):
        text = self.source()
        self.assertEqual(missing_requirements(text), [])
        order = ('EXTERNAL_BENCHMARK', 'CANDIDATE_STRUCTURE', 'PROJECT_RECONCILIATION', 'MODULE_PREPARATION')
        flow = re.search(r'BENCHMARK_FIRST_EXECUTION_ORDER\n```text\n(.*?)\n```', text, re.S)
        self.assertIsNotNone(flow)
        positions = [flow.group(1).index(stage) for stage in order]
        self.assertEqual(positions, sorted(positions))

    def test_missing_or_reversed_statement_is_not_satisfied_by_keyword(self):
        text = self.source()
        for sentence in REQUIREMENTS:
            with self.subTest(sentence=sentence):
                self.assertIn(sentence, missing_requirements(text.replace(sentence, '')))
                reversed_text = text.replace(sentence, sentence.split(':', 1)[0] + ': opposite behavior is allowed.')
                self.assertIn(sentence, missing_requirements(reversed_text))

    def test_real_games_and_sample_are_distinguished(self):
        text = self.source()
        for value in ('Shattered Pixel Dungeon', 'Mindustry', 'The Battle for Wesnoth', "Ren'Py", '공식 샘플', '7b8b845a76fe76c6b7c031ae9e570852411f56db', 'da3b3358cd03e47ef32a87ee5b40231e656d1c76'):
            self.assertIn(value, text)

    def test_composition_recipes_reuse_separate_parts(self):
        text = self.source()
        for value in ('fill', 'frame_9slice', 'nameplate', 'button_plate', 'tab_plate', 'state_overlay', 'icon', 'portrait', 'module_id', 'module_version', 'layer_order', 'anchor', 'slot', 'compatible_family'):
            self.assertIn(value, text)
        for value in ('메인메뉴 조합', '대화창 조합', '도감·기록 조합'):
            self.assertIn(value, text)

    def test_import_and_readability_failure_cases(self):
        text = self.source()
        for value in ('texture_margin', 'content_margin', 'alpha', 'atlas bleed', 'minimum_size', 'tile', 'mouse_filter', '긴 한국어', 'focus', 'disabled', 'state_overlay'):
            self.assertIn(value, text)

    def test_no_automatic_adoption_or_universal_reskin(self):
        text = self.source()
        for value in ('PINNED_CONTRACT_PRESERVED', 'OPEN_OTHER_PR_IS_READ_ONLY', 'PROJECT_CANON_WINS', 'USER_APPROVED', 'REVIEW_SELF_IS_NOT_INDEPENDENT'):
            self.assertIn(value, text)
        self.assertIn('PROJECT_PIN_UNCHANGED', (ROOT / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_bootstrap_explicitly_reconciles_older_reuse_order(self):
        text = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn('EXTERNAL_ORDER_OVERRIDE_FOR_UI', text)
        self.assertIn('일반 재사용 조사 순서보다 이 범위의 외부 벤치마크 순서가 우선', text)

    def test_data_motion_audio_and_save_not_certified_by_screenshot(self):
        text = self.source()
        self.assertIn('CAPTURE_IS_NOT_ACTION_PROOF:', text)
        self.assertIn('VISUAL_RUNTIME_CLAIM_REQUIRES_CAPTURE:', text)
        self.assertIn('실제 입력/저장 시험', text)


if __name__ == '__main__':
    unittest.main()
