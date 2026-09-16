from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools.skill_context import load_skill_context, read_skill_contract


class SkillContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'references').mkdir()
        self.skill = self.root / 'SKILL.md'
        self.skill.write_text('# Intake\n[Receipt](references/receipt.md)\n[Video](references/video.md)\n<!-- contract-module: references/receipt.md -->\n', encoding='utf-8')
        (self.root / 'references/receipt.md').write_text('receipt contract\n[deep](hidden.md)', encoding='utf-8')
        (self.root / 'references/video.md').write_text('video route', encoding='utf-8')
        (self.root / 'references/hidden.md').write_text('must not be loaded', encoding='utf-8')

    def test_default_context_does_not_eagerly_load_references(self):
        pack = load_skill_context(self.skill)
        self.assertEqual([self.skill.resolve()], list(pack))
        self.assertNotIn('receipt contract', '\n'.join(pack.values()))

    def test_selected_reference_is_loaded_completely_without_recursive_expansion(self):
        pack = load_skill_context(self.skill, ['references/receipt.md'])
        self.assertEqual(2, len(pack))
        self.assertEqual('receipt contract\n[deep](hidden.md)', pack[(self.root / 'references/receipt.md').resolve()])
        self.assertNotIn('video route', '\n'.join(pack.values()))
        self.assertNotIn('must not be loaded', '\n'.join(pack.values()))

    def test_contract_validation_reads_declared_modules_not_every_reference(self):
        text = read_skill_contract(self.skill)
        self.assertIn('receipt contract', text)
        self.assertNotIn('video route', text)

    def test_missing_declared_module_fails_instead_of_silently_losing_contract(self):
        (self.root / 'references/receipt.md').unlink()
        with self.assertRaises((ValueError, FileNotFoundError)):
            read_skill_contract(self.skill)

    def test_unlinked_reference_is_not_discoverable(self):
        with self.assertRaises(ValueError):
            load_skill_context(self.skill, ['references/hidden.md'])

    def test_traversal_and_absolute_paths_are_rejected(self):
        for path in ('../outside.md', '/outside.md', 'C:/outside.md', 'references/../../outside.md'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                load_skill_context(self.skill, [path])

    def test_repeated_selection_reads_one_copy(self):
        self.assertEqual(2, len(load_skill_context(self.skill, ['references/receipt.md'] * 2)))

    def test_contract_marker_requires_user_visible_link(self):
        self.skill.write_text('<!-- contract-module: references/receipt.md -->', encoding='utf-8')
        with self.assertRaises(ValueError):
            read_skill_contract(self.skill)

    def test_reference_directory_redirect_outside_package_is_rejected(self):
        original = Path.resolve
        reference_dir = self.root / 'references'
        def redirected(path, *args, **kwargs):
            if path == reference_dir:
                return original(self.root.parent, *args, **kwargs)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'resolve', redirected), self.assertRaises(ValueError):
            load_skill_context(self.skill, ['references/receipt.md'])

    def test_real_intake_entrypoint_discovers_only_selected_module(self):
        source = Path(__file__).resolve().parents[1] / 'skills/managing-project-intake-and-work-contract/SKILL.md'
        pack = load_skill_context(source, ['references/preflight-and-evidence.md'])
        self.assertEqual({source.resolve(), (source.parent / 'references/preflight-and-evidence.md').resolve()}, set(pack))
        self.assertIn('PRE_BUILD', '\n'.join(pack.values()))

    def test_real_intake_execution_references_are_selectable_without_eager_loading(self):
        source = Path(__file__).resolve().parents[1] / 'skills/managing-project-intake-and-work-contract/SKILL.md'
        for name in ('first-prompt-direction-anchoring', 'continuous-work-execution', 'work-decomposition-and-sequencing', 'grill-me-protocol'):
            with self.subTest(reference=name):
                selected = f'references/{name}.md'
                pack = load_skill_context(source, [selected])
                self.assertEqual({source.resolve(), (source.parent / selected).resolve()}, set(pack))

    def test_production_coverage_suite_imports_in_an_isolated_process(self):
        result = subprocess.run([sys.executable, '-m', 'unittest', 'tests.test_skill_system_coverage', '-q'],
                                cwd=Path(__file__).resolve().parents[1], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=60)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
