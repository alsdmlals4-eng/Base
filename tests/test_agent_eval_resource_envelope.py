from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = (
    ROOT
    / "docs"
    / "knowledge"
    / "ai"
    / "agent-tools"
    / "EXTERNAL_AGENT_ADAPTER_CONTRACT.md"
)


class AgentEvalResourceEnvelopeTests(unittest.TestCase):
    """Protect resource-sensitive agent eval evidence; not a runtime benchmark."""

    def test_resource_envelope_is_first_class_eval_identity(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "EVAL_RESOURCE_ENVELOPE_REQUIRED",
            "RESOURCE_ENVELOPE_IS_EVAL_IDENTITY",
            "guaranteed CPU/RAM",
            "hard limit / kill threshold",
            "wall-clock timeout",
            "concurrency",
            "egress/network policy",
            "runner/hardware identity",
            "cache/warm-state conditions",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

    def test_infrastructure_failures_do_not_become_task_failures(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "INFRA_FAILURE_IS_NOT_TASK_FAILURE",
            "OOM",
            "container/pod termination",
            "infrastructure timeout",
            "infra failure count/rate",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

    def test_resource_envelope_is_conditional_and_does_not_copy_benchmark_thresholds(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("RESOURCE_ENVELOPE_NOT_APPLICABLE", adapter)
        self.assertIn("resource-sensitive", adapter)
        self.assertIn("environment-conditioned", adapter)
        self.assertNotIn("3x ceiling", adapter)
        self.assertNotIn("below 3 percentage points", adapter)


if __name__ == "__main__":
    unittest.main()
