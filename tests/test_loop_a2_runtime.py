from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tests.test_loop_a2_protocol import valid_request


class RuntimeTests(unittest.TestCase):
    def request(self) -> RunRequest:
        return RunRequest.from_dict(valid_request())

    def test_stale_main_stops_before_builder(self) -> None:
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic()
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha="f" * 40
        )
        self.assertEqual(result.state, "STALE_BASE_SHA")
        self.assertEqual(builder.calls, 0)
        self.assertEqual(critic.calls, 0)

    def test_out_of_scope_write_is_quarantined_before_critic(self) -> None:
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd", "README.md"))
        critic = FakeCritic(verdict="PASS")
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "QUARANTINED")
        self.assertIn("OUT_OF_SCOPE_WRITE", result.finding_codes)
        self.assertEqual(critic.calls, 0)

    def test_critic_cannot_erase_deterministic_failure(self) -> None:
        builder = FakeBuilder(changed_paths=(".github/workflows/pwn.yml",))
        critic = FakeCritic(verdict="PASS")
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertNotEqual(result.state, "WAITING_INTEGRATION")
        self.assertEqual(critic.calls, 0)

    def test_happy_path_waits_for_integration_and_receipt_has_digest(self) -> None:
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",))
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "WAITING_INTEGRATION")
        self.assertRegex(result.receipt_digest, r"^[0-9a-f]{64}$")
        self.assertEqual(builder.calls, 1)
        self.assertEqual(critic.calls, 1)

    def test_critic_pass_without_all_requirements_is_blocked(self) -> None:
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(verdict="PASS", checked_requirement_ids=())
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "BLOCKED_UNVERIFIED")
        self.assertIn("CRITIC_COVERAGE_INCOMPLETE", result.finding_codes)

    def test_same_must_fix_twice_yields_no_progress(self) -> None:
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(
            verdict="MUST_FIX",
            finding_codes=("REQ_MISSING",),
            repeat=True,
        )
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "NO_PROGRESS")
        self.assertEqual(critic.calls, 2)
        self.assertLessEqual(builder.calls, 2)

    def test_three_run_fake_burnin(self) -> None:
        runtime = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        )
        report = runtime.burn_in(
            self.request(), observed_main_sha=self.request().expected_main_sha, runs=3
        )
        self.assertEqual(report["status"], "FAKE_PROVIDER_BURNIN_GREEN")
        self.assertEqual(report["consecutive_runs"], 3)
        self.assertEqual(report["out_of_scope_writes"], 0)
        self.assertEqual(report["false_completion_claims"], 0)


class RuntimeAdversarialIdentityTests(unittest.TestCase):
    def request(self) -> RunRequest:
        return RunRequest.from_dict(valid_request())

    def test_builder_turn_budget_is_enforced_before_critic(self) -> None:
        class OverBudgetBuilder:
            calls = 0

            def invoke(self, request: RunRequest, *, repair_cycle: int):
                from tools.loop_a2_runtime.protocol import WorkerResult
                self.calls += 1
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
                    "summary": "over budget",
                    "usage": {"turns": request.budgets.max_turns + 1},
                    "errors": [],
                })

        builder = OverBudgetBuilder()
        critic = FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",))
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "BUDGET_EXCEEDED")
        self.assertIn("BUILDER_TURN_BUDGET_EXCEEDED", result.finding_codes)
        self.assertEqual(critic.calls, 0)

    def test_empty_changeset_cannot_claim_waiting_integration(self) -> None:
        result = A2Runtime(
            builder=FakeBuilder(changed_paths=()),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertEqual(result.state, "BLOCKED_UNVERIFIED")
        self.assertIn("EMPTY_CHANGESET", result.finding_codes)

    def test_critic_identity_mismatch_is_quarantined(self) -> None:
        class WrongIdentityCritic:
            calls = 0

            def review(self, request: RunRequest, worker_result):
                from tools.loop_a2_runtime.protocol import ReviewResult
                self.calls += 1
                return ReviewResult.from_dict({
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_REVIEW_RESULT",
                    "project_id": "OTHER_PROJECT",
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "CRITIC",
                    "verdict": "PASS",
                    "findings": [],
                    "checked_requirement_ids": list(request.requirement_ids),
                })

        result = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=WrongIdentityCritic(),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertEqual(result.state, "QUARANTINED")
        self.assertIn("CRITIC_IDENTITY_MISMATCH", result.finding_codes)

    def test_pass_with_findings_is_blocked(self) -> None:
        result = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=FakeCritic(
                verdict="PASS",
                finding_codes=("SUSPICIOUS_PASS",),
                checked_requirement_ids=("REQ_001",),
            ),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertEqual(result.state, "BLOCKED_UNVERIFIED")
        self.assertIn("CRITIC_PASS_WITH_FINDINGS", result.finding_codes)

    def test_repair_user_decision_stops_without_more_repairs(self) -> None:
        class SequencedCritic:
            calls = 0

            def review(self, request: RunRequest, worker_result):
                from tools.loop_a2_runtime.protocol import ReviewResult
                self.calls += 1
                if self.calls == 1:
                    verdict = "MUST_FIX"
                    code = "FIX_FIRST"
                else:
                    verdict = "USER_DECISION_REQUIRED"
                    code = "PLANNING_CONFLICT"
                return ReviewResult.from_dict({
                    "schema_version": 1,
                    "contract_role": "LOOP_A2_REVIEW_RESULT",
                    "project_id": request.project_id,
                    "run_id": request.run_id,
                    "package_id": request.package_id,
                    "expected_main_sha": request.expected_main_sha,
                    "role": "CRITIC",
                    "verdict": verdict,
                    "findings": [{
                        "code": code,
                        "severity": "P1",
                        "message": code,
                        "paths": list(worker_result.changed_paths),
                        "requirement_ids": list(request.requirement_ids),
                    }],
                    "checked_requirement_ids": list(request.requirement_ids),
                })

        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = SequencedCritic()
        result = A2Runtime(builder=builder, critic=critic).run(
            self.request(), observed_main_sha=self.request().expected_main_sha
        )
        self.assertEqual(result.state, "USER_DECISION_REQUIRED")
        self.assertEqual(builder.calls, 2)
        self.assertEqual(critic.calls, 2)

    def test_burnin_rejects_non_fake_request(self) -> None:
        value = valid_request()
        value["provider_mode"] = "REAL"
        request = RunRequest.from_dict(value)
        runtime = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        )
        with self.assertRaisesRegex(ValueError, "FAKE"):
            runtime.burn_in(request, observed_main_sha=request.expected_main_sha, runs=3)


if __name__ == "__main__":
    unittest.main()
