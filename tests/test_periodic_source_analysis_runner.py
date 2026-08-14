from __future__ import annotations

import unittest

from tools.periodic_source_analysis import run_analysis


class PeriodicSourceAnalysisRunnerTests(unittest.TestCase):
    def test_runner_entry_point_is_available(self) -> None:
        self.assertTrue(callable(run_analysis))


if __name__ == "__main__":
    unittest.main()
