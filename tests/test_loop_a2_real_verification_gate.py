from __future__ import annotations

from dataclasses import dataclass
import unittest

from tools.loop_a2_runtime.protocol import ReviewResult, RunRequest, WorkerResult
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tools.loop_a2_runtime.test_executor import TestSuiteResult
from tests.test_loop_a2_protocol import valid_request


def _request() -> RunRequest:
    value = valid_request()
    value["provider_mode"] = "REAL"
    return RunRequest.from_dict(value)


@dataclass
class _Verifier:
    status: str = "PASS"
    calls: int = 0

    def verify(self, request: RunRequest, worker_result: WorkerResult) -> TestSuiteResult:
        self.calls += 1
        return TestSuiteResult(
            project_id=request.project_id,
            expected_main_sha=request.expected_main_sha,
            status=self.status,
            commands=(),
        )


class _RepairBuilder:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult:
        self.calls += 1
        return WorkerResult.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_WORKER_RESULT",
                "project_id": request.project_id,
                "run_id": request.run_id,
                "package_id": request.package_id,
                "expected_main_sha": request.expected_main_sha,
                "role": "BUILDER",
                "status": "COMPLETED",
                "changed_paths": ["scripts/feature/a.gd"],
                "summary": f"candidate {repair_cycle}",
                "usage": {"turns": 1},
                "errors": [],
            }
        )


class _RepairCritic:
    def __init__(self) -> None:
        self.calls = 0

    def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult:
        self.calls += 1
        if self.calls == 1:
            return ReviewResult.from_dict(
                {
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_REVIEW_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "CRITIC",
                    "verdict": "MUST_FIX",
                    "findings": [
                        {
                            "code": "FIX_ONE",
                            "severity": "P1",
                            "message": "repair once",
                            "paths": ["scripts/feature/a.gd"],
                            "requirement_ids": ["REQ_001"],
                        }
                    ],
                    "checked_requirement_ids": ["REQ_001"],
                }
            )
        return ReviewResult.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_REVIEW_RESULT",
                "project_id": request.project_id,
                "run_id": request.run_id,
                "package_id": request.package_id,
                "expected_main_sha": request.expected_main_sha,
                "role": "CRITIC",
                "verdict": "PASS",
                "findings": [],
                "checked_requirement_ids": ["REQ_001"],
            }
        )


class RealVerificationGateTests(unittest.TestCase):
    def test_real_runtime_without_verifier_blocks_before_builder_subscription_usage(self) -> None:
        request = _request()
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(
            verdict="PASS",
            checked_requirement_ids=("REQ_001",),
        )
        runtime = A2Runtime(
            builder=builder,
            critic=critic,
            provider_mode="REAL",
        )

        outcome = runtime.run(request, observed_main_sha=request.expected_main_sha)

        self.assertEqual(outcome.state, "BLOCKED_UNVERIFIED")
        self.assertIn("PROJECT_TEST_GATE_REQUIRED", outcome.finding_codes)
        self.assertEqual(builder.calls, 0)
        self.assertEqual(critic.calls, 0)

    def test_real_runtime_invokes_critic_only_after_candidate_tests_pass(self) -> None:
        request = _request()
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(
            verdict="PASS",
            checked_requirement_ids=("REQ_001",),
        )
        verifier = _Verifier(status="PASS")
        runtime = A2Runtime(
            builder=builder,
            critic=critic,
            candidate_verifier=verifier,
            provider_mode="REAL",
        )

        outcome = runtime.run(request, observed_main_sha=request.expected_main_sha)

        self.assertEqual(outcome.state, "WAITING_INTEGRATION")
        self.assertEqual(builder.calls, 1)
        self.assertEqual(verifier.calls, 1)
        self.assertEqual(critic.calls, 1)

    def test_real_runtime_test_failure_blocks_before_critic(self) -> None:
        for status in ("FAIL", "BLOCKED"):
            with self.subTest(status=status):
                request = _request()
                builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
                critic = FakeCritic(
                    verdict="PASS",
                    checked_requirement_ids=("REQ_001",),
                )
                verifier = _Verifier(status=status)
                runtime = A2Runtime(
                    builder=builder,
                    critic=critic,
                    candidate_verifier=verifier,
                    provider_mode="REAL",
                )

                outcome = runtime.run(
                    request,
                    observed_main_sha=request.expected_main_sha,
                )

                self.assertEqual(outcome.state, "BLOCKED_UNVERIFIED")
                self.assertIn("PROJECT_TEST_GATE_NOT_PASS", outcome.finding_codes)
                self.assertEqual(builder.calls, 1)
                self.assertEqual(verifier.calls, 1)
                self.assertEqual(critic.calls, 0)

    def test_every_real_repair_candidate_is_retested_before_next_critic(self) -> None:
        request = _request()
        builder = _RepairBuilder()
        critic = _RepairCritic()
        verifier = _Verifier(status="PASS")
        runtime = A2Runtime(
            builder=builder,
            critic=critic,
            candidate_verifier=verifier,
            provider_mode="REAL",
        )

        outcome = runtime.run(request, observed_main_sha=request.expected_main_sha)

        self.assertEqual(outcome.state, "WAITING_INTEGRATION")
        self.assertEqual(builder.calls, 2)
        self.assertEqual(verifier.calls, 2)
        self.assertEqual(critic.calls, 2)


if __name__ == "__main__":
    unittest.main()
