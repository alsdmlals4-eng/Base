from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from tools.validate_work_contract_receipt import validate_execution_receipt

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'templates/project-operations'
SOURCE = '1bc9c0cbc679f1d88cf1652d48df9273ba234401'


class PMColdStartContractTests(unittest.TestCase):
    def test_canonical_startup_json_is_root_shaped_and_executable_after_filling(self):
        text = (TEMPLATES / 'WORK_PROJECT_START_CANON_CHECKLIST.md').read_text(encoding='utf-8')
        section = text.split('### 12.1 Receipt extension', 1)[1].split('### 12.2', 1)[0]
        match = re.search(r'```json\s*\n(.*?)\n```', section, re.S)
        self.assertIsNotNone(match)
        value = json.loads(match.group(1))
        for field in ('work_level', 'benchmark_preflight_receipt', 'context_configuration_hygiene', 'project_work_kanban'):
            self.assertIn(field, value)
        self.assertTrue(validate_execution_receipt(value, expected_source_sha=SOURCE))
        def fill(item):
            if isinstance(item, dict): return {k: fill(v) for k, v in item.items()}
            if isinstance(item, list): return [fill(v) for v in item]
            if isinstance(item, str) and item.startswith('<') and item.endswith('>'): return 'explicit test fixture, not production evidence'
            return item
        value = fill(value)
        value['project_work_kanban']['source_main_sha'] = SOURCE
        self.assertEqual([], validate_execution_receipt(value, expected_source_sha=SOURCE))

    def test_cold_start_commands_supply_trusted_source_and_display(self):
        for name in ('PROJECT_START_HERE.md', 'AI_WORKFLOW.md', 'WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md', 'WORK_PROJECT_START_CANON_CHECKLIST.md'):
            text = (TEMPLATES / name).read_text(encoding='utf-8')
            commands = [line for line in text.splitlines() if 'python ' in line and 'validate_work_contract_receipt.py --receipt' in line]
            self.assertTrue(commands, name)
            for line in commands:
                with self.subTest(file=name):
                    self.assertIn('--expected-source-sha', line)
                    self.assertIn('--render-markdown', line)
                    self.assertIn('--phase start', line)

    def test_transition_order_selects_active_before_execution_gate(self):
        text = (TEMPLATES / 'PROJECT_WORK_ITEM_CHECKLIST.md').read_text(encoding='utf-8')
        self.assertNotIn('다음 작업 선택 전 --phase resume', text)
        self.assertIn('다음 승인 작업을 먼저 선택해 IN_PROGRESS', text)
        self.assertIn('INFORMATION ONLY; EXECUTION BLOCKED', text)


if __name__ == '__main__':
    unittest.main()
