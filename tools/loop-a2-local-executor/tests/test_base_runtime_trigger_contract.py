from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/validate-loop-a2-local-executor.yml"


class BaseRuntimeTriggerContractTests(unittest.TestCase):
    def test_local_executor_validates_base_a2_runtime_consumers_on_pr_and_push(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for path in (
            "      - 'tools/loop_a2.py'",
            "      - 'tools/loop_a2_runtime/**'",
        ):
            self.assertGreaterEqual(
                text.count(path),
                2,
                f"Local Executor must validate Base runtime consumer changes on PR and push: {path}",
            )


if __name__ == "__main__":
    unittest.main()
