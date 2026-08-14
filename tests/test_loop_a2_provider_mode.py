from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tests.test_loop_a2_protocol import valid_request


class ProviderModeTests(unittest.TestCase):
    def test_real_request_cannot_run_on_default_fake_runtime(self) -> None:
        value = valid_request()
        value["provider_mode"] = "REAL"
        request = RunRequest.from_dict(value)
        builder = FakeBuilder(changed_paths=("scripts/feature/a.gd",))
        critic = FakeCritic(
            verdict="PASS",
            checked_requirement_ids=("REQ_001",),
        )
        outcome = A2Runtime(builder=builder, critic=critic).run(
            request,
            observed_main_sha=request.expected_main_sha,
        )
        self.assertEqual(outcome.state, "QUARANTINED")
        self.assertIn("PROVIDER_MODE_MISMATCH", outcome.finding_codes)
        self.assertEqual(builder.calls, 0)
        self.assertEqual(critic.calls, 0)


if __name__ == "__main__":
    unittest.main()
