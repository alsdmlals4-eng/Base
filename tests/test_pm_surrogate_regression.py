import unittest
from tests.test_project_work_tracking import tracked_receipt, run_cli


class PMSurrogateRegression(unittest.TestCase):
    def test_escaped_lone_surrogate_fails_before_success_output(self):
        for scalar in ('\ud800', '\udfff'):
            with self.subTest(scalar=repr(scalar)):
                value = tracked_receipt()
                value['project_work_kanban']['work_items'][0]['title'] = scalar
                result = run_cli(value, '--render-markdown')
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn('WORK CONTRACT RECEIPT: PASS', result.stdout)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
