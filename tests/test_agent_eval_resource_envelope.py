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

    def test_failure_classification_is_causal_not_termination_based(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "FAILURE_CLASSIFICATION_IS_CAUSAL",
            "INFRA_FAILURE_IS_NOT_TASK_FAILURE",
            "failed to deliver the declared envelope",
            "agent's chosen strategy",
            "task/resource-efficiency failure",
            "FAILURE_CAUSE_UNVERIFIED",
            "infra failure count/rate separated causally",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

    def test_resource_sensitivity_applies_even_to_deterministic_transforms(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "RESOURCE_ENVELOPE_NOT_APPLICABLE",
            "completion, correctness, fidelity, and comparison outcome",
            "Determinism of the algorithm does not by itself establish resource insensitivity",
            "deterministic transform over a large capture",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

    def test_fixed_resource_confounding_cannot_establish_adapter_benefit(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "FIXED_RESOURCE_CONFOUNDING_IS_NOT_CURED_BY_REPEATS",
            "counterbalanced/randomized assignment",
            "ENVIRONMENT_CONDITIONED_NON_COMPARATIVE",
            "Environment-conditioned non-comparative observations cannot by themselves establish adapter benefit",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

    def test_contract_prohibits_benchmark_specific_resource_thresholds_generically(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("NO_BENCHMARK_SPECIFIC_RESOURCE_THRESHOLDS", adapter)
        self.assertIn("numeric resource multiplier", adapter)
        self.assertIn("infrastructure-error cutoff", adapter)
        self.assertIn("score-difference threshold", adapter)
        self.assertNotIn("Terminal-Bench", adapter)
        self.assertNotIn("SWE-bench", adapter)


if __name__ == "__main__":
    unittest.main()
