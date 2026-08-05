from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.test_cloud_run_game_backend_capability import (
    CloudRunGameBackendCapabilityTests as _CloudRunGameBackendCapabilityTests,
)
from tests.test_godot_editor_transaction_adapter import (
    GodotEditorTransactionAdapterTests as _GodotEditorTransactionAdapterTests,
)
from tests.test_godot_editor_transaction_adapter_runtime import (
    GodotEditorTransactionAdapterRuntimeTests as _GodotEditorTransactionAdapterRuntimeTests,
)
from tests.test_godot_multi_project_pilot import (
    GodotMultiProjectPilotTests as _GodotMultiProjectPilotTests,
)
from tests.test_godot_multi_project_pilot_adversarial import (
    GodotMultiProjectPilotAdversarialTests as _GodotMultiProjectPilotAdversarialTests,
)
from tests.test_godot_pilot_artifact_bundle import (
    GodotPilotArtifactBundleTests as _GodotPilotArtifactBundleTests,
)
from tests.test_godot_live_editor_adapter_resolution import (
    GodotAdapterResolutionTests as _GodotAdapterResolutionTests,
)
from tests.test_godot_live_editor_contract import (
    GodotLiveEditorContractTests as _GodotLiveEditorContractTests,
)
from tests.test_godot_live_editor_contract_v2 import (
    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
)
from tests.test_godot_live_editor_contract_v2_adversarial import (
    GodotLiveEditorContractV2AdversarialTests as _GodotLiveEditorContractV2AdversarialTests,
)
from tests.test_godot_live_editor_contract_v2_docs import (
    GodotLiveEditorContractV2DocsTests as _GodotLiveEditorContractV2DocsTests,
)
from tests.test_godot_live_editor_idempotent_approval import (
    GodotIdempotentApprovalSchemaTests as _GodotIdempotentApprovalSchemaTests,
)
from tests.test_godot_live_editor_runtime_contract_hardening import (
    GodotRuntimeContractHardeningTests as _GodotRuntimeContractHardeningTests,
)
from tests.test_platform_review_asset_rights_reference_production import (
    PlatformReviewAssetRightsReferenceProductionTests
    as _PlatformReviewAssetRightsReferenceProductionTests,
)
from tests.test_game_entitlement_integrity_drm_capability import (
    GameEntitlementIntegrityDrmCapabilityTests
    as _GameEntitlementIntegrityDrmCapabilityTests,
)


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class V9MachineContractTests(unittest.TestCase):
    def test_base_final_release_is_distinct_from_post_release_project_adoption(self) -> None:
        version = read("docs/BASE_RULES_VERSION.md")
        release = read("docs/operations/BASE_V9_RELEASE_CONTRACT.md")

        self.assertIn("v9.0.0", version)
        self.assertIn("BASE_RELEASED", version)
        self.assertIn("585a53a25be1b04c543196f5901551deb49c7691", version)
        self.assertIn("v9.0.0", release)
        self.assertIn("POST_RELEASE_PROJECT_ADOPTION_WAVE", release)
        self.assertIn("must not block the Base v9.0.0 release", release)
        self.assertIn("최종 릴리스", release)

    def test_system_map_declares_complete_recoverable_workflow(self) -> None:
        system_map = read("docs/operations/BASE_V9_SYSTEM_MAP.md")

        for term in (
            "PLAN",
            "BUILD",
            "REVIEW",
            "적대적 검토",
            "증거 검증",
            "Base 승격 후보",
            "실패",
            "재개",
        ):
            self.assertIn(term, system_map)

    def test_maturity_model_is_risk_scaled_and_has_five_levels(self) -> None:
        maturity = read("docs/operations/BASE_V9_MATURITY_MODEL.md")

        for level in range(6):
            self.assertIn(f"Level {level}", maturity)
        self.assertIn("규모", maturity)
        self.assertIn("위험", maturity)
        self.assertIn("강제하지 않는다", maturity)

    def test_migration_map_preserves_legacy_pr_decisions_without_direct_merge(self) -> None:
        migration = read("docs/operations/BASE_V9_MIGRATION_MAP.md")

        for pr in ("#5", "#18", "#28", "#29", "#30"):
            self.assertIn(pr, migration)
        self.assertIn("직접 병합하지 않는다", migration)
        self.assertIn("ROLLBACK", migration)

    def test_terminal_legacy_prs_are_not_reassessed(self) -> None:
        migration = read("docs/operations/BASE_V9_MIGRATION_MAP.md")
        ledger = json.loads(read("docs/operations/GITHUB_OBJECT_LEDGER.json"))

        for marker in ("[구현됨]", "[대체됨]"):
            self.assertIn(marker, migration)
        self.assertIn("do_not_reassess", migration)

        expected = {
            5: ("[구현됨]", "IMPLEMENTED_BY_CURRENT_CONTRACT"),
            18: ("[대체됨]", "SUPERSEDED_BY_CURRENT_CONTRACT"),
            28: ("[구현됨]", "IMPLEMENTED_BY_CURRENT_CONTRACT"),
            29: ("[대체됨]", "SUPERSEDED_BY_CURRENT_CONTRACT"),
            30: ("[대체됨]", "SUPERSEDED_BY_CURRENT_CONTRACT"),
        }
        for pr_number, (marker, resolution) in expected.items():
            with self.subTest(pr_number=pr_number):
                record = next(
                    item
                    for item in ledger["objects"]
                    if item["type"] == "pr" and item["number"] == pr_number
                )
                self.assertEqual(record["status_marker"], marker)
                self.assertEqual(record["resolution"], resolution)
                self.assertTrue(record["terminal"])
                self.assertTrue(record["do_not_reassess"])
                self.assertTrue(record["replacement_paths"])
                self.assertTrue(record["verification_paths"])

    def test_c0_reusable_workflow_invokes_runner_as_package_module(self) -> None:
        workflow = read(".github/workflows/reusable-godot-project-pilot.yml")
        self.assertIn("PYTHONPATH: ${{ github.workspace }}/_base_c0", workflow)
        self.assertIn("python -m tools.godot_multi_project_pilot", workflow)
        self.assertNotIn("python _base_c0/tools/godot_multi_project_pilot.py", workflow)

    def test_c0_binds_archive_timeout_and_unicode_evidence_contracts(self) -> None:
        schema = json.loads(read("schemas/godot-project-pilot-v1.schema.json"))
        self.assertEqual(
            "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
            schema["properties"]["godot"]["properties"]["archive_sha256"]["const"],
        )
        runner = read("tools/godot_multi_project_pilot.py")
        self.assertIn("except subprocess.TimeoutExpired", runner)
        self.assertIn("PROCESS_TIMEOUT", runner)
        self.assertIn("return 5", runner)
        evidence = read("tools/godot_project_pilot_evidence.py")
        self.assertIn("class EvidenceVerificationError", evidence)
        self.assertGreaterEqual(evidence.count("ensure_ascii=False"), 3)

    def test_c0_generated_plugin_cfg_uses_addon_relative_script_path(self) -> None:
        workspace = read("tools/godot_project_pilot_workspace.py")
        self.assertIn('script="plugin.gd"', workspace)
        self.assertNotIn(
            'script="res://addons/base_multi_project_pilot/plugin.gd"',
            workspace,
        )

    def test_c0_wrapper_explicitly_types_variant_file_hashes(self) -> None:
        wrapper = read(
            "templates/project-operations/godot-live-editor/pilot/multi_project_pilot.gd"
        )
        for marker in (
            "var main_hash_before: Variant = _evidence.sha256_file(main_scene)",
            "var main_hash_after_inspect: Variant = _evidence.sha256_file(main_scene)",
            "var main_hash_after: Variant = _evidence.sha256_file(main_scene)",
        ):
            self.assertIn(marker, wrapper)


if __name__ == "__main__":
    unittest.main()
