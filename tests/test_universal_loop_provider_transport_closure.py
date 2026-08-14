from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "operations" / "UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json"


class UniversalLoopProviderTransportClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    def test_checkpoint_preserves_provider_transport_under_successor_policy(self) -> None:
        self.assertEqual(
            self.value["status"],
            "PORTABILITY_CONFIRMED_SUBSCRIPTION_TRANSPORT_READY_LOCAL_SMOKE_GATED",
        )
        gate = self.value["remaining_external_gate"]
        self.assertEqual(gate["real_codex_builder_transport"], "MERGED_MAIN_VALIDATED")
        self.assertEqual(gate["real_gpt_critic_transport"], "MERGED_MAIN_VALIDATED")
        self.assertEqual(gate["real_openai_api"], "NOT_APPLICABLE_POLICY_FORBIDDEN")
        self.assertEqual(gate["subscription_codex_cli_smoke"], "NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED")
        self.assertEqual(gate["real_a2_burnin_runs"], 0)
        self.assertIsNone(gate["paid_smoke_issue"])

    def test_transport_evidence_is_exact_and_postmerge_validated(self) -> None:
        evidence = self.value["provider_transport_evidence"]
        self.assertEqual(evidence["implementation_pr"], 365)
        self.assertEqual(
            evidence["exact_head"],
            "6d351ad7b60ca3ae339ace419f1e6e7eae7c501a",
        )
        self.assertEqual(
            evidence["merge_main"],
            "77da090833757e84486a10cc9a30a9ec1de8da6c",
        )
        self.assertEqual(evidence["postmerge_openai_transport_run"], 31796573727)
        self.assertEqual(evidence["postmerge_a2_foundation_run"], 31796573695)
        self.assertEqual(evidence["postmerge_base_v9_run"], 31796573709)
        self.assertEqual(evidence["postmerge_game_project_os_run"], 31796573680)
        self.assertEqual(evidence["postmerge_validation"], "PASS")
        self.assertEqual(evidence["live_openai_request"], "NOT_RUN")
        self.assertEqual(evidence["paid_api_cost"], "NOT_RUN")

    def test_autonomy_limits_remain_closed(self) -> None:
        limits = self.value["preserved_limits"]
        self.assertEqual(limits["a3_auto_merge"], "DISABLED")
        self.assertEqual(limits["scheduler"], "NOT_CONFIGURED")
        self.assertEqual(limits["automatic_product_scope_selection"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
