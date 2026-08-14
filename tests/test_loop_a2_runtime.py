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


if __name__ == "__main__":
    unittest.main()
