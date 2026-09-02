from __future__ import annotations
import copy
import unittest
from tests.test_project_work_tracking import tracked_receipt, done_receipt, run_cli
from tools.validate_work_contract_receipt import validate_execution_receipt
SOURCE = '1bc9c0cbc679f1d88cf1652d48df9273ba234401'


def check(value, **kwargs):
    return validate_execution_receipt(value, **({'expected_source_sha': SOURCE} | kwargs))


class ReviewRegressions(unittest.TestCase):
    def test_missing_trusted_source_is_not_execution_authority(self):
        self.assertTrue(validate_execution_receipt(tracked_receipt()))

    def test_nonpass_evidence_containers_are_checked(self):
        for field in ('checklist', 'verification'):
            for status in ('NOT_RUN', 'PARTIAL', 'FAIL', 'BLOCKED_UNVERIFIED'):
                for bad in ({}, 'proof', [7], None):
                    with self.subTest(field=field, status=status, bad=bad):
                        value = tracked_receipt()
                        value['project_work_kanban']['work_items'][0][field][0].update(status=status, evidence=bad)
                        self.assertTrue(check(value))

    def test_terminal_controls_are_rejected(self):
        for bad in ('\x1bc', '\x9b2J', '\u202e1/1', '\x00'):
            value = tracked_receipt()
            value['project_work_kanban']['work_items'][0]['title'] = bad
            self.assertTrue(check(value))

    def test_stored_progress_display_must_match(self):
        value = tracked_receipt()
        value['project_work_kanban']['progress_summary'] = dict(completed_items=0, applicable_items=1, display='1 / 1')
        self.assertTrue(check(value))

    def test_done_next_action_is_not_printed_as_an_instruction(self):
        value = done_receipt()
        value['project_work_kanban']['work_items'][0]['next_action'] = 'Start unrelated next goal'
        result = run_cli(value, '--phase', 'closeout', '--render-markdown')
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertNotIn('Start unrelated next goal', result.stdout)

    def test_done_cannot_hide_recorded_blocker(self):
        value = done_receipt()
        value['project_work_kanban']['work_items'][0]['verification'].append(dict(level='E3_RUNTIME', status='BLOCKED_UNVERIFIED', evidence=[]))
        self.assertTrue(check(value, phase='closeout'))

    def test_valid_blocked_board_is_visible_but_not_authorized(self):
        value = tracked_receipt(); board = value['project_work_kanban']
        board['active_work_item_ref'] = None
        board['work_items'][0].update(status='BLOCKED_UNVERIFIED', blocker='engine unavailable', resume_condition='verified engine ready')
        result = run_cli(value, '--render-markdown')
        self.assertNotEqual(0, result.returncode)
        for text in ('0 / 1', 'engine unavailable', 'verified engine ready'):
            self.assertIn(text, result.stdout)

    def test_blocked_view_suppresses_untrusted_execution_actions(self):
        value = tracked_receipt(); board = value['project_work_kanban']
        board.update(active_work_item_ref=None, next_action='Deploy the release now')
        board['work_items'][0].update(
            status='BLOCKED_UNVERIFIED',
            blocker='approval missing',
            resume_condition='verified approval recorded',
            next_action='Deploy the release now',
        )
        result = run_cli(value, '--render-markdown')
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn('Deploy the release now', result.stdout)
        self.assertIn('approval missing', result.stdout)
        self.assertIn('verified approval recorded', result.stdout)

    def test_next_task_is_selected_before_resume_gate(self):
        value = done_receipt(); board = value['project_work_kanban']
        second = copy.deepcopy(tracked_receipt()['project_work_kanban']['work_items'][0])
        second.update(work_item_id='PM-02', depends_on=['PM-01'])
        board['work_items'].append(second); board['work_item_refs'].append('PM-02')
        board.update(active_work_item_ref='PM-02', next_action='Execute approved PM-02')
        self.assertEqual([], check(value, phase='resume'))

    def test_verify_review_only_task_can_be_active_for_resume(self):
        value = tracked_receipt(); board = value['project_work_kanban']
        board['work_items'][0].update(status='VERIFY_REVIEW', next_action='Review exact-head evidence')
        result = run_cli(value, '--phase', 'resume', '--render-markdown')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('VERIFY_REVIEW', result.stdout)

    def test_noncanonical_whitespace_in_identifiers_is_rejected(self):
        value = tracked_receipt(); board = value['project_work_kanban']
        board['work_items'][0]['work_item_id'] = ' PM-01 '
        board['work_item_refs'] = [' PM-01 ']
        board['active_work_item_ref'] = ' PM-01 '
        errors = '\n'.join(check(value))
        self.assertIn('canonical', errors)

    def test_closeout_binds_done_evidence_to_trusted_current_head(self):
        value = done_receipt()
        wrong_head_errors = validate_execution_receipt(
            value,
            phase='closeout',
            expected_source_sha=SOURCE,
            expected_head_sha='b' * 40,
        )
        self.assertIn(
            'verified_head_sha does not match trusted expected head',
            '\n'.join(wrong_head_errors),
        )

        missing_head_errors = validate_execution_receipt(
            value,
            phase='closeout',
            expected_source_sha=SOURCE,
        )
        self.assertIn(
            'expected_head_sha from the trusted final-head caller is required for closeout',
            missing_head_errors,
        )

    def test_failed_closeout_render_does_not_claim_stale_head_complete(self):
        result = run_cli(
            done_receipt(),
            '--phase', 'closeout',
            '--expected-head-sha', 'b' * 40,
            '--render-markdown',
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn('0 / 1', result.stdout)
        self.assertNotIn('[x]', result.stdout)
        self.assertIn('VERIFY_REVIEW_STALE_HEAD', result.stdout)

    def test_missing_closeout_head_render_does_not_claim_complete(self):
        # Bypass run_cli's convenience injection so the actual missing-argument path is exercised.
        import json
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        from tests.test_project_work_tracking import CLI

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'receipt.json'
            path.write_text(json.dumps(done_receipt()), encoding='utf-8')
            result = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    '--receipt', str(path),
                    '--phase', 'closeout',
                    '--expected-source-sha', SOURCE,
                    '--render-markdown',
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn('expected_head_sha from the trusted final-head caller is required for closeout', result.stdout)
        self.assertIn('0 / 1', result.stdout)
        self.assertNotIn('[x]', result.stdout)
        self.assertIn('VERIFY_REVIEW_STALE_HEAD', result.stdout)


if __name__ == '__main__':
    unittest.main()
