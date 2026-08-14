from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tools.loop_a2_runtime.providers import FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tests.test_loop_a2_protocol import valid_request


class TimeoutTests(unittest.TestCase):
    def test_elapsed_timeout_is_enforced_after_provider_returns(self) -> None:
        class FakeClock:
            now = 0.0

            def __call__(self) -> float:
                return self.now

        clock = FakeClock()

        class AdvancingBuilder:
            def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult:
                clock.now += 2.0
                return WorkerResult.from_dict({
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_WORKER_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "BUILDER",
                    "status": "COMPLETED",
                    "changed_paths": ["scripts/feature/a.gd"],
                    "summary": "Returned after deadline.",
                    "usage": {"turns": 1},
                    "errors": [],
                })

        value = valid_request()
        value["budgets"] = {
            "max_turns": 12,
            "max_repair_cycles": 2,
            "timeout_seconds": 1,
        }
        request = RunRequest.from_dict(value)
        critic = FakeCritic(
            verdict="PASS",
            checked_requirement_ids=("REQ_001",),
        )
        outcome = A2Runtime(
            builder=AdvancingBuilder(),
            critic=critic,
            clock=clock,
        ).run(request, observed_main_sha=request.expected_main_sha)
        self.assertEqual(outcome.state, "PROVIDER_TIMEOUT")
        self.assertIn("PROVIDER_TIMEOUT", outcome.finding_codes)
        self.assertEqual(critic.calls, 0)


if __name__ == "__main__":
    unittest.main()
