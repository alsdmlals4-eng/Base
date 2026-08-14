from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import ProtocolError, ReviewResult, RunRequest, WorkerResult
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tests.test_loop_a2_protocol import valid_request


class AuthorityHardeningTests(unittest.TestCase):
    def request(self, **overrides: object) -> RunRequest:
        value = valid_request()
        value.update(overrides)
        return RunRequest.from_dict(value)

    def test_system_governance_path_is_blocked_even_when_package_allows_it(self) -> None:
        request = self.request(allowed_paths=[".github/**"])
        outcome = A2Runtime(
            builder=FakeBuilder(changed_paths=(".github/workflows/unsafe.yml",)),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        ).run(request, observed_main_sha=request.expected_main_sha)
        self.assertEqual(outcome.state, "QUARANTINED")
        self.assertIn("SYSTEM_PROTECTED_WRITE", outcome.finding_codes)

    def test_critic_cannot_expand_requirement_authority(self) -> None:
        class ExpandingCritic:
            def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult:
                return ReviewResult.from_dict({
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_REVIEW_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "CRITIC",
                    "verdict": "MUST_FIX",
                    "findings": [{
                        "code": "EXTRA_REQUIREMENT",
                        "severity": "P1",
                        "message": "Implement an unapproved requirement.",
                        "paths": list(worker_result.changed_paths),
                        "requirement_ids": ["REQ_999"],
                    }],
                    "checked_requirement_ids": ["REQ_001"],
                })

        request = self.request()
        outcome = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=ExpandingCritic(),
        ).run(request, observed_main_sha=request.expected_main_sha)
        self.assertEqual(outcome.state, "QUARANTINED")
        self.assertIn("CRITIC_REQUIREMENT_EXPANSION", outcome.finding_codes)

    def test_critic_cannot_expand_path_authority(self) -> None:
        class ExpandingCritic:
            def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult:
                return ReviewResult.from_dict({
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_REVIEW_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "CRITIC",
                    "verdict": "MUST_FIX",
                    "findings": [{
                        "code": "EXTRA_PATH",
                        "severity": "P1",
                        "message": "Modify an unapproved path.",
                        "paths": ["README.md"],
                        "requirement_ids": ["REQ_001"],
                    }],
                    "checked_requirement_ids": ["REQ_001"],
                })

        request = self.request()
        outcome = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=ExpandingCritic(),
        ).run(request, observed_main_sha=request.expected_main_sha)
        self.assertEqual(outcome.state, "QUARANTINED")
        self.assertIn("CRITIC_PATH_EXPANSION", outcome.finding_codes)

    def test_turn_budget_is_cumulative_across_repairs(self) -> None:
        class EightTurnBuilder:
            def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult:
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
                    "summary": "Eight turns.",
                    "usage": {"turns": 8},
                    "errors": [],
                })

        request = self.request(budgets={"max_turns": 12, "max_repair_cycles": 2, "timeout_seconds": 600})
        outcome = A2Runtime(
            builder=EightTurnBuilder(),
            critic=FakeCritic(verdict="MUST_FIX", finding_codes=("FIX_ME",), checked_requirement_ids=("REQ_001",)),
        ).run(request, observed_main_sha=request.expected_main_sha)
        self.assertEqual(outcome.state, "BUDGET_EXCEEDED")
        self.assertIn("BUILDER_TURN_BUDGET_EXCEEDED", outcome.finding_codes)

    def test_completed_worker_cannot_report_errors(self) -> None:
        value = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40,
            "role": "BUILDER",
            "status": "COMPLETED",
            "changed_paths": ["scripts/feature/a.gd"],
            "summary": "Contradictory.",
            "usage": {"turns": 1},
            "errors": [{"code": "FAILED_ANYWAY", "message": "contradiction"}],
        }
        with self.assertRaises(ProtocolError):
            WorkerResult.from_dict(value)

    def test_failed_worker_must_explain_failure(self) -> None:
        value = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40,
            "role": "BUILDER",
            "status": "FAILED",
            "changed_paths": [],
            "summary": "Failed without evidence.",
            "usage": {"turns": 1},
            "errors": [],
        }
        with self.assertRaises(ProtocolError):
            WorkerResult.from_dict(value)


if __name__ == "__main__":
    unittest.main()
