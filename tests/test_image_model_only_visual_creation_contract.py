from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
MODEL_POLICY = (
    ROOT
    / "docs/knowledge/game-development/IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md"
)
SCREEN_MATRIX = (
    ROOT
    / "docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md"
)


class ImageModelOnlyVisualCreationContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required image creation owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_conversation_gate_routes_all_generation_and_editing_to_model_policy(self) -> None:
        gate = self._read(GATE)
        for token in (
            "IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md",
            "IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING",
            "DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED",
            "IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION",
            "NO_VECTOR_OR_CODE_DRAWN_FALLBACK",
        ):
            self.assertIn(token, gate)

    def test_policy_forbids_direct_vector_and_code_drawn_image_substitutes(self) -> None:
        policy = self._read(MODEL_POLICY)
        for token in (
            "DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED",
            "NO_SVG_OR_VECTOR_PATH_AS_IMAGE_GENERATION_SUBSTITUTE",
            "NO_CODE_DRAWN_IMAGE_AS_IMAGE_MODEL_BYPASS",
            "SVG/XML path",
            "HTML/CSS/Canvas",
            "Python/Pillow/Cairo/matplotlib",
            "Godot draw_* / Line2D / Polygon2D / primitive drawing",
        ):
            self.assertIn(token, policy)

    def test_policy_fails_closed_when_the_image_model_is_unavailable(self) -> None:
        policy = self._read(MODEL_POLICY)
        for token in (
            "IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION",
            "BLOCKED_IMAGE_MODEL_UNAVAILABLE",
            "NO_VECTOR_OR_CODE_DRAWN_FALLBACK",
            "TEXT_BRIEF_AND_REQUIREMENT_WORK_MAY_CONTINUE",
        ):
            self.assertIn(token, policy)

    def test_runtime_and_information_exceptions_cannot_authorize_new_vector_art(self) -> None:
        policy = self._read(MODEL_POLICY)
        screen_matrix = self._read(SCREEN_MATRIX)
        self.assertIn("PROCEDURAL_OR_ENGINE_RENDERED", screen_matrix)
        self.assertIn("NO_NEW_IMAGE_FILE_REQUIRED", screen_matrix)
        for token in (
            "EXISTING_APPROVED_VECTOR_ASSET_REUSE_ONLY",
            "ENGINE_NATIVE_UI_AND_EFFECT_IMPLEMENTATION_IS_NOT_IMAGE_DELIVERABLE_CREATION",
            "STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE",
            "PROCEDURAL_OR_ENGINE_RENDERED_IS_IMPLEMENTATION_MODE_NOT_IMAGE_CREATION_AUTHORITY",
            "NO_NEW_IMAGE_FILE_REQUIRED_DOES_NOT_AUTHORIZE_NEW_VECTOR_ART",
            "TEXT_TABLE_FLOW_DB_FIRST",
        ):
            self.assertIn(token, policy)

    def test_required_vector_delivery_is_model_first_and_conversion_only(self) -> None:
        policy = self._read(MODEL_POLICY)
        for token in (
            "IMAGE_MODEL_SOURCE_FIRST",
            "EXPLICIT_VECTOR_FORMAT_REQUIREMENT",
            "NON_CREATIVE_VECTORIZATION_POSTPROCESS_ONLY",
            "SOURCE_RESULT_FIDELITY_READBACK_REQUIRED",
            "BLOCKED_VECTOR_POSTPROCESS_UNAVAILABLE",
            "NO_MANUAL_VECTOR_REDRAW",
        ):
            self.assertIn(token, policy)

    def test_existing_consumer_approval_and_evidence_gates_are_preserved(self) -> None:
        policy = self._read(MODEL_POLICY)
        for token in (
            "ACTUAL_CONSUMER_REQUIRED",
            "Visual Requirement Gate",
            "Image Conversation Approval Gate",
            "GENERATE_EXACTLY_ONE",
            "STOP_REQUIRED_AFTER_GENERATION",
            "HOST_PLATFORM_PRECEDENCE",
            "image generation success != user approval != PROJECT_ASSET_APPROVED != runtime integration",
        ):
            self.assertIn(token, policy)


if __name__ == "__main__":
    unittest.main()
