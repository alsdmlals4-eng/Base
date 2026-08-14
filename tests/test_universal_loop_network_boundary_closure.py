from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "operations" / "UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json"


class UniversalLoopNetworkBoundaryClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    def test_runtime_foundation_records_denied_network_boundary(self) -> None:
        self.assertEqual(
            self.value["runtime_foundation"]["denied_network_boundary"],
            "MERGED_MAIN_VALIDATED",
        )

    def test_boundary_evidence_is_exact_and_postmerge_validated(self) -> None:
        evidence = self.value["denied_network_boundary_evidence"]
        self.assertEqual(evidence["implementation_pr"], 374)
        self.assertEqual(
            evidence["exact_head"],
            "8ad0980a9ec9f5913422b95ddaf6db3511c4bb81",
        )
        self.assertEqual(
            evidence["merge_main"],
            "c6400874fbd4947d6279cc1b009e2eaceaac0870",
        )
        self.assertEqual(evidence["boundary_id"], "DOCKER_NONE_DENIED_V1")
        self.assertEqual(evidence["postmerge_denied_network_run"], 31803084020)
        self.assertEqual(evidence["postmerge_a2_foundation_run"], 31803084028)
        self.assertEqual(evidence["postmerge_base_v9_run"], 31803084003)
        self.assertEqual(evidence["postmerge_game_project_os_run"], 31803084001)
        self.assertEqual(evidence["postmerge_validation"], "PASS")
        self.assertEqual(evidence["live_openai_request"], "NOT_RUN")
        self.assertEqual(evidence["paid_api_cost"], "NOT_RUN")

    def test_successor_provider_policy_and_autonomy_limits_remain_closed(self) -> None:
        self.assertEqual(
            self.value["status"],
            "PORTABILITY_CONFIRMED_UNATTENDED_LOCAL_EXECUTOR_READY_BLACKSMITH_BURNIN_AUTHORITY_READY_LOCAL_MACHINE_GATED",
        )
        gate = self.value["remaining_external_gate"]
        self.assertEqual(gate["real_openai_api"], "NOT_APPLICABLE_POLICY_FORBIDDEN")
        self.assertEqual(gate["subscription_codex_cli_smoke"], "NOT_RUN_LOCAL_CHATGPT_AUTH_REQUIRED")
        self.assertEqual(gate["real_a2_burnin_runs"], 0)
        self.assertIsNone(gate["paid_smoke_issue"])
        limits = self.value["preserved_limits"]
        self.assertEqual(limits["a3_auto_merge"], "DISABLED")
        self.assertEqual(limits["scheduler"], "NOT_CONFIGURED")
        self.assertEqual(limits["automatic_product_scope_selection"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
