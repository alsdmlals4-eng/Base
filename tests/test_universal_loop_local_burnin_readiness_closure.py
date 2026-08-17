from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "operations" / "UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json"
STATUS = "PORTABILITY_CONFIRMED_UNIVERSAL_LOOP_V1_REAL_A2_BURNIN_COMPLETE"


class UniversalLoopLocalBurninReadinessClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    def test_checkpoint_preserves_repository_readiness_under_real_burnin_success(self) -> None:
        self.assertEqual(self.value["status"], STATUS)
        runtime = self.value["runtime_foundation"]
        self.assertEqual(runtime["unattended_local_executor"], "MERGED_MAIN_VALIDATED")
        self.assertEqual(runtime["windows_docker_denied_network_host"], "MERGED_MAIN_VALIDATED")
        self.assertEqual(runtime["blacksmith_burnin_authority"], "MERGED_MAIN_VALIDATED")

    def test_blacksmith_checkpoint_points_to_burnin_authority_main_without_product_promotion(self) -> None:
        blacksmith = next(
            item for item in self.value["validated_projects"] if item["project_id"] == "BLACKSMITH"
        )
        self.assertEqual(blacksmith["main_sha"], "6b241f28969410de78156c90cc10f33a067426a2")
        evidence = blacksmith["evidence"]
        self.assertEqual(evidence["burnin_authority_pr"], 169)
        self.assertEqual(evidence["full_validation_run"], 31828561974)
        self.assertEqual(evidence["live_editor_pilot_run"], 31828562392)
        self.assertEqual(evidence["product_scope_selection"], "UNCHANGED_UNSELECTED")

    def test_local_executor_evidence_preserves_implementation_and_records_live_success(self) -> None:
        evidence = self.value["local_executor_evidence"]
        self.assertEqual(evidence["implementation_issue"], 397)
        self.assertEqual(evidence["implementation_pr"], 398)
        self.assertEqual(evidence["exact_head"], "c576a4831cd1fdd76bb4a248ee6f8a33ba0015b5")
        self.assertEqual(evidence["merge_main"], "f71f6c14f4a7119cfa7c0bf29097c04fd1c7adaf")
        self.assertEqual(evidence["postmerge_local_executor_run"], 31825097578)
        self.assertEqual(evidence["postmerge_base_v9_run"], 31825097617)
        self.assertEqual(evidence["postmerge_game_project_os_run"], 31825097579)
        self.assertEqual(evidence["postmerge_validation"], "PASS")
        self.assertEqual(evidence["local_installation"], "PASS")
        self.assertEqual(evidence["windows_startup_registration"], "PASS_REGISTERED")
        self.assertEqual(evidence["local_gh_auth_status"], "PASS")
        self.assertEqual(evidence["local_codex_chatgpt_auth_status"], "PASS")
        self.assertEqual(evidence["real_local_chatgpt_codex_call"], "PASS")
        self.assertEqual(evidence["real_windows_diagnostic_issue"], 489)
        self.assertEqual(
            evidence["real_windows_diagnostic_receipt_digest"],
            "061e9c3c921bbc8a46698de1c1ba3513c76ca6cac7d88f6374fb6e660a420a06",
        )

    def test_windows_docker_evidence_preserves_host_proof_and_records_user_pc_smoke(self) -> None:
        evidence = self.value["windows_docker_host_evidence"]
        self.assertEqual(evidence["implementation_issue"], 400)
        self.assertEqual(evidence["implementation_pr"], 401)
        self.assertEqual(evidence["exact_head"], "6a022b2364d061a3802fee87d56d7c9b2b28929c")
        self.assertEqual(evidence["merge_main"], "3b3af0706db1b861c1bec6a237192595944b79a5")
        self.assertEqual(evidence["postmerge_windows_host_contract_run"], 31827788722)
        self.assertEqual(evidence["postmerge_denied_network_run"], 31827788644)
        self.assertEqual(evidence["postmerge_a2_foundation_run"], 31827788793)
        self.assertEqual(evidence["postmerge_base_v9_run"], 31827788642)
        self.assertEqual(evidence["postmerge_game_project_os_run"], 31827788674)
        self.assertEqual(evidence["windows_plan_construction"], "PASS")
        self.assertEqual(evidence["linux_real_docker_loopback_only"], "PASS")
        self.assertEqual(evidence["windows_live_docker_desktop"], "PASS")
        self.assertEqual(evidence["reviewed_image_preload"], "PASS")
        self.assertEqual(evidence["postmerge_validation"], "PASS")
        self.assertEqual(
            self.value["denied_network_boundary_evidence"]["non_linux_production_boundary"],
            "WINDOWS_HOST_PLAN_MERGED_MAIN_VALIDATED_LIVE_LOCAL_SMOKE_PASS",
        )

    def test_blacksmith_burnin_authority_evidence_is_exact_and_run_count_reaches_three(self) -> None:
        evidence = self.value["blacksmith_burnin_authority_evidence"]
        self.assertEqual(evidence["implementation_issue"], 168)
        self.assertEqual(evidence["implementation_pr"], 169)
        self.assertEqual(evidence["exact_head"], "b1bc083f95538ce9e5deab43f17aa2582281324c")
        self.assertEqual(evidence["merge_main"], "6b241f28969410de78156c90cc10f33a067426a2")
        self.assertEqual(evidence["product_baseline_sha"], "5267f542ef6ce99f98b3b407e42b146b5672335b")
        self.assertEqual(evidence["package_id"], "BS_A2_BURNIN_TEST_ONLY_PKG_001")
        self.assertEqual(
            evidence["allowed_runtime_output"],
            "docs/operations/loop/burnin/BS_A2_BURNIN_MARKER.txt",
        )
        self.assertEqual(evidence["postmerge_full_validation_run"], 31828561974)
        self.assertEqual(evidence["postmerge_live_editor_pilot_run"], 31828562392)
        self.assertEqual(evidence["product_scope_selection"], "UNCHANGED_UNSELECTED")
        self.assertEqual(evidence["real_a2_burnin_runs"], 3)
        self.assertEqual(evidence["postmerge_validation"], "PASS")

    def test_external_gates_close_while_policy_limits_remain_closed(self) -> None:
        gate = self.value["remaining_external_gate"]
        self.assertEqual(gate["blacksmith_burnin_authority"], "MERGED_MAIN_VALIDATED")
        self.assertEqual(gate["local_executor_installation"], "PASS")
        self.assertEqual(gate["windows_docker_desktop_smoke"], "PASS")
        self.assertEqual(gate["subscription_codex_cli_smoke"], "PASS")
        self.assertEqual(gate["real_a2_burnin_runs"], 3)
        self.assertEqual(self.value["provider_policy"]["paid_openai_api"], "FORBIDDEN")
        self.assertEqual(self.value["provider_policy"]["api_key_fallback"], "FORBIDDEN")
        limits = self.value["preserved_limits"]
        self.assertEqual(limits["a3_auto_merge"], "DISABLED")
        self.assertEqual(limits["scheduler"], "NOT_CONFIGURED")
        self.assertEqual(limits["automatic_product_scope_selection"], "FORBIDDEN")

    def test_historical_provider_and_denied_network_evidence_remain_unchanged(self) -> None:
        provider = self.value["provider_transport_evidence"]
        self.assertEqual(provider["implementation_pr"], 365)
        self.assertEqual(provider["exact_head"], "6d351ad7b60ca3ae339ace419f1e6e7eae7c501a")
        self.assertEqual(provider["merge_main"], "77da090833757e84486a10cc9a30a9ec1de8da6c")
        boundary = self.value["denied_network_boundary_evidence"]
        self.assertEqual(boundary["implementation_pr"], 374)
        self.assertEqual(boundary["exact_head"], "8ad0980a9ec9f5913422b95ddaf6db3511c4bb81")
        self.assertEqual(boundary["merge_main"], "c6400874fbd4947d6279cc1b009e2eaceaac0870")
        self.assertEqual(boundary["boundary_id"], "DOCKER_NONE_DENIED_V1")


if __name__ == "__main__":
    unittest.main()
