from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json"
BURNIN_RUNTIME_SHA = "f4deebfc06de828cc956e47220e829cd98b1eb09"
BLACKSMITH_AUTHORITY_SHA = "6b241f28969410de78156c90cc10f33a067426a2"
HISTORICAL_KERNEL_SHA = "8e7238a1bb9f49bd6e2403a2a6cb20d7aee863c7"
COUNTED_ISSUES = [490, 491, 492]
COUNTED_RUN_IDS = [
    "BS_A2_BURNIN_001_R1",
    "BS_A2_BURNIN_001_R2",
    "BS_A2_BURNIN_001_R3",
]
COUNTED_RECEIPT_DIGESTS = [
    "fcf3663d3d62c8364276488f3d9f29d9d510d91c0274fe27571cb5e2bb3e8ca9",
    "9cc4f5066d21af7d8463dd87f73a45e2c5a25f581fb6e15c378dd41d82eefb4a",
    "e19b7d060843bc4b6e0c352c88cb08a370a71a07a31deeeb5c82169fbaa7937c",
]


def load_checkpoint() -> dict[str, object]:
    return json.loads(CHECKPOINT.read_text(encoding="utf-8"))


class UniversalLoopV1RealBurninClosureTests(unittest.TestCase):
    def test_machine_checkpoint_records_real_three_run_closure(self) -> None:
        checkpoint = load_checkpoint()

        self.assertEqual(
            checkpoint["status"],
            "PORTABILITY_CONFIRMED_UNIVERSAL_LOOP_V1_REAL_A2_BURNIN_COMPLETE",
        )
        # This is historical cross-project kernel provenance, not a moving latest-main pointer.
        self.assertEqual(checkpoint["base_kernel_main_sha"], HISTORICAL_KERNEL_SHA)

        closure = checkpoint["universal_loop_v1_closure_evidence"]
        self.assertEqual(closure["status"], "COMPLETE")
        self.assertEqual(closure["base_runtime_sha"], BURNIN_RUNTIME_SHA)
        self.assertEqual(closure["blacksmith_authority_sha"], BLACKSMITH_AUTHORITY_SHA)
        self.assertEqual(closure["provider_mode"], "REAL")
        self.assertEqual(closure["terminal_state"], "WAITING_INTEGRATION")
        self.assertEqual(closure["non_counting_diagnostic_issue"], 489)
        self.assertEqual(closure["non_counting_diagnostic_run_id"], "BS_A2_DIAG_20260817_005")
        self.assertEqual(closure["non_counting_diagnostic_receipt_digest"], "061e9c3c921bbc8a46698de1c1ba3513c76ca6cac7d88f6374fb6e660a420a06")
        self.assertEqual(closure["counted_issue_numbers"], COUNTED_ISSUES)
        self.assertEqual(closure["counted_run_ids"], COUNTED_RUN_IDS)
        self.assertEqual(closure["counted_receipt_digests"], COUNTED_RECEIPT_DIGESTS)
        self.assertEqual(closure["consecutive_real_a2_burnin_runs"], 3)
        self.assertEqual(closure["omission_escape"], 0)
        self.assertEqual(closure["drift_escape"], 0)
        self.assertEqual(closure["unauthorized_addition_escape"], 0)

    def test_real_local_execution_gates_are_closed_without_opening_a3(self) -> None:
        checkpoint = load_checkpoint()

        local = checkpoint["local_executor_evidence"]
        self.assertEqual(local["local_installation"], "PASS")
        self.assertEqual(local["windows_startup_registration"], "PASS_REGISTERED")
        self.assertEqual(local["local_gh_auth_status"], "PASS")
        self.assertEqual(local["local_codex_chatgpt_auth_status"], "PASS")
        self.assertEqual(local["real_local_chatgpt_codex_call"], "PASS")

        windows = checkpoint["windows_docker_host_evidence"]
        self.assertEqual(windows["windows_live_docker_desktop"], "PASS")
        self.assertEqual(windows["reviewed_image_preload"], "PASS")

        subscription = checkpoint["subscription_codex_cli_evidence"]
        self.assertEqual(subscription["real_subscription_smoke"], "PASS")

        burnin = checkpoint["blacksmith_burnin_authority_evidence"]
        self.assertEqual(burnin["real_a2_burnin_runs"], 3)

        remaining = checkpoint["remaining_external_gate"]
        self.assertEqual(remaining["local_executor_installation"], "PASS")
        self.assertEqual(remaining["windows_docker_desktop_smoke"], "PASS")
        self.assertEqual(remaining["subscription_codex_cli_smoke"], "PASS")
        self.assertEqual(remaining["real_a2_burnin_runs"], 3)

        self.assertEqual(checkpoint["provider_policy"]["paid_openai_api"], "FORBIDDEN")
        self.assertEqual(checkpoint["provider_policy"]["api_key_fallback"], "FORBIDDEN")
        limits = checkpoint["preserved_limits"]
        self.assertEqual(limits["a3_auto_merge"], "DISABLED")
        self.assertEqual(limits["scheduler"], "NOT_CONFIGURED")
        self.assertEqual(limits["automatic_product_scope_selection"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
