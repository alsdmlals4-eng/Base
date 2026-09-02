from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V4_CONTRACT = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json"
BLUEPRINT_POLICY = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"
BLUEPRINT_INSTRUCTION = (
    ROOT
    / "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md"
)
IMAGE_POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
IMAGE_GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
CODEX_HANDOFF = ROOT / "templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md"


TWO_PASS_SEQUENCE = (
    "PLAN\n"
    "→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT\n"
    "→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION\n"
    "→ BLUEPRINT_REVIEW_PUBLICATION\n"
    "→ USER_FINAL_REVIEW_APPROVAL\n"
    "→ IMPLEMENTATION_AUTHORIZED"
)


class BaseFreshReadTwoPassBlueprintContractTests(unittest.TestCase):
    def test_v4_machine_contract_defines_bounded_base_revision_lifecycle(self) -> None:
        contract = json.loads(V4_CONTRACT.read_text(encoding="utf-8"))
        lifecycle = contract["base_revision_lifecycle"]

        self.assertEqual("LATEST_BASE_DISCOVERY_REQUIRED", lifecycle["latest_discovery"])
        self.assertEqual(
            "PIN_IS_EVIDENCE_NOT_FRESHNESS_BYPASS", lifecycle["pin_semantics"]
        )
        self.assertEqual(
            "PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED", lifecycle["project_adoption"]
        )
        self.assertEqual(
            "BASE_DRIFT_CLASSIFICATION_REQUIRED", lifecycle["drift_gate"]
        )
        self.assertEqual(
            "BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK",
            lifecycle["execution_pin"],
        )
        self.assertEqual(
            ["NO_PERMANENT_STALE_PIN", "NO_FLOATING_EXECUTION"],
            lifecycle["forbidden_modes"],
        )
        self.assertEqual(
            "BOUNDARY_FRESH_READ_REQUIRED", lifecycle["boundary_recheck"]
        )
        self.assertEqual(
            [
                "IMPLEMENTATION_HANDOFF",
                "PRE_MERGE",
                "POST_MERGE",
                "CLOSEOUT",
            ],
            lifecycle["boundary_recheck_points"],
        )
        self.assertEqual(
            [
                "base_observed_head_sha",
                "base_adopted_contract_sha",
                "base_execution_sha",
            ],
            lifecycle["required_revision_fields"],
        )

        invariants = "\n".join(contract["invariants"])
        for token in (
            "latest completed Base main",
            "does not silently replace project canon",
            "selected Base execution SHA remains fixed",
            "impact classification",
        ):
            self.assertIn(token, invariants)

    def test_v4_machine_contract_defines_two_pass_blueprint_lifecycle(self) -> None:
        contract = json.loads(V4_CONTRACT.read_text(encoding="utf-8"))

        self.assertEqual(
            [
                "PLAN",
                "BLUEPRINT_PASS_1_STRUCTURAL_DRAFT",
                "REQUIRED_IMAGE_AND_MATERIAL_PREPARATION",
                "BLUEPRINT_REVIEW_PUBLICATION",
                "USER_FINAL_REVIEW_APPROVAL",
                "IMPLEMENTATION_AUTHORIZED",
            ],
            contract["blueprint_preimplementation_lifecycle"],
        )
        self.assertEqual(
            {
                "pass_1": "STRUCTURAL_BLUEPRINT_DRAFT",
                "pass_2": "BLUEPRINT_PASS_2_FINAL",
                "artifact_boundary": "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            },
            contract["blueprint_pass_roles"],
        )

    def test_planning_and_image_consumers_share_the_two_pass_sequence(self) -> None:
        for path in (
            BLUEPRINT_POLICY,
            BLUEPRINT_INSTRUCTION,
            IMAGE_POLICY,
            IMAGE_GATE,
        ):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn(TWO_PASS_SEQUENCE, text)
                self.assertNotIn(
                    "PLAN\n→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION",
                    text,
                )

    def test_blueprint_passes_are_revisions_not_extra_artifacts(self) -> None:
        for path in (BLUEPRINT_POLICY, BLUEPRINT_INSTRUCTION):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                for token in (
                    "PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH",
                    "BLUEPRINT_PASS_1_STRUCTURAL_DRAFT",
                    "STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT",
                    "BLUEPRINT_PASS_2_FINAL",
                    "NO_SEPARATE_BLUEPRINT_ARTIFACT",
                ):
                    self.assertIn(token, text)

    def test_material_and_vfx_preparation_is_consumer_bounded(self) -> None:
        for path in (BLUEPRINT_POLICY, BLUEPRINT_INSTRUCTION, IMAGE_POLICY):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                for token in (
                    "BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT",
                    "REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS",
                    "VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT",
                    "ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD",
                ):
                    self.assertIn(token, text)

    def test_codex_handoff_pins_base_and_final_blueprint_revisions(self) -> None:
        text = CODEX_HANDOFF.read_text(encoding="utf-8")

        for token in (
            "LATEST_BASE_DISCOVERY_REQUIRED",
            "PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED",
            "BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK",
            "BASE_DRIFT_CLASSIFICATION_REQUIRED",
            "NO_PERMANENT_STALE_PIN",
            "NO_FLOATING_EXECUTION",
            "BOUNDARY_FRESH_READ_REQUIRED",
            "base_observed_head_sha:",
            "base_adopted_contract_sha:",
            "base_execution_sha:",
            "base_drift_classification:",
            "blueprint_pass_1_revision:",
            "blueprint_pass_2_final_revision:",
            "user_final_approval_decision_id:",
            "implementation_authority_revision:",
        ):
            self.assertIn(token, text)

        self.assertIn(
            "BLUEPRINT_PASS_2_FINAL exact revision",
            text,
        )


if __name__ == "__main__":
    unittest.main()
