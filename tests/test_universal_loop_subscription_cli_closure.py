from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "operations" / "UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json"


class UniversalLoopSubscriptionCliClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    def test_checkpoint_records_no_paid_api_provider_policy(self) -> None:
        policy = self.checkpoint["provider_policy"]
        self.assertEqual(policy["paid_openai_api"], "FORBIDDEN")
        self.assertEqual(policy["paid_provider_smoke"], "NOT_PLANNED")
        self.assertEqual(policy["primary_real_provider"], "CHATGPT_AUTHENTICATED_CODEX_CLI")
        self.assertEqual(policy["api_key_fallback"], "FORBIDDEN")

    def test_checkpoint_records_subscription_transport_implementation_evidence(self) -> None:
        evidence = self.checkpoint["subscription_codex_cli_evidence"]
        self.assertEqual(evidence["implementation_issue"], 379)
        self.assertEqual(evidence["implementation_pr"], 380)
        self.assertEqual(evidence["exact_head"], "c6ee0f6765ed166619cc6e39c3dd5b5e05b01f83")
        self.assertEqual(evidence["merge_main"], "ef5f1f79945d3b083c96a89295ac4bcd88d61e2d")
        self.assertEqual(evidence["postmerge_a2_foundation_run"], 31809731573)
        self.assertEqual(evidence["postmerge_openai_transport_run"], 31809731526)
        self.assertEqual(evidence["postmerge_base_v9_run"], 31809731528)
        self.assertEqual(evidence["postmerge_game_project_os_run"], 31809731626)
        self.assertEqual(evidence["postmerge_validation"], "PASS")
        self.assertEqual(evidence["model_shell_tool"], "DISABLED_BY_STRICT_CONFIG")
        self.assertEqual(evidence["model_web_search_features"], "DISABLED_BY_STRICT_CONFIG")
        self.assertEqual(evidence["real_subscription_smoke"], "NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED")
        self.assertEqual(evidence["live_openai_api_request"], "NOT_APPLICABLE_POLICY_FORBIDDEN")
        self.assertEqual(evidence["paid_api_cost"], "NOT_RUN")

    def test_checkpoint_replaces_paid_smoke_gate_with_local_subscription_smoke(self) -> None:
        gate = self.checkpoint["remaining_external_gate"]
        self.assertEqual(gate["real_openai_api"], "NOT_APPLICABLE_POLICY_FORBIDDEN")
        self.assertEqual(gate["subscription_codex_cli_smoke"], "NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED")
        self.assertEqual(gate["real_a2_burnin_runs"], 0)
        self.assertIsNone(gate["paid_smoke_issue"])

    def test_preserved_limits_remain_closed(self) -> None:
        limits = self.checkpoint["preserved_limits"]
        self.assertEqual(limits["a3_auto_merge"], "DISABLED")
        self.assertEqual(limits["scheduler"], "NOT_CONFIGURED")
        self.assertEqual(limits["automatic_product_scope_selection"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
