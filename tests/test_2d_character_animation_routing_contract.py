from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING = (
    ROOT
    / "skills/evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md"
)
TEMPLATE = ROOT / "templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md"
SOURCE_CATALOG = (
    ROOT
    / "skills/evaluating-godot-assets-and-plugins-before-creation/references/source-catalog.md"
)
SPRITE_CONTROLS = (
    ROOT
    / "skills/designing-art-prompts-and-technique-cards/references/sprite-pose-sequence-controls.md"
)
LEARNING_LOG = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md"
)


class CharacterAnimationRoutingContractTests(unittest.TestCase):
    def test_route_owner_compares_four_materially_distinct_paths(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "FRAME",
            "GODOT_NATIVE_RIG",
            "EXTERNAL_RIG_RUNTIME",
            "EXTERNAL_RIG_BAKED",
            "FRAME_DEFAULT_UNLESS_EVIDENCE",
            "MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3",
        ):
            self.assertIn(marker, text)

    def test_route_is_consumer_and_measurement_driven(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "actual_consumer",
            "camera_scale",
            "screen_time",
            "concurrent_instance_peak",
            "animation_count",
            "direction_count",
            "outfit_variant_count",
            "weapon_attachment_count",
            "requires_continuous_deformation",
            "requires_extreme_smear_or_redraw",
            "target_platforms",
        ):
            self.assertIn(marker, text)

    def test_rig_ready_source_contract_requires_hidden_overlap_and_attachment_data(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "hidden_underlap",
            "overlap_margin",
            "pivot",
            "parent_bone",
            "draw_order",
            "deformation_safe_area",
            "attachment_slot",
            "skin_group",
            "RIG_READY_SOURCE_IS_NOT_RUNTIME_ASSET",
        ):
            self.assertIn(marker, text)

    def test_state_family_and_interruption_contract_are_explicit(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "Wind-up",
            "Active",
            "Recovery",
            "Hit",
            "Stagger",
            "Knockdown",
            "Rise",
            "Transition",
            "can_interrupt",
            "interrupt_windows",
            "same_state_reentry",
            "rapid_repeat_behavior",
            "instant_complete_behavior",
            "pause_resume",
            "save_resume_pose",
            "reduced_motion_fallback",
            "missing_asset_fallback",
        ):
            self.assertIn(marker, text)

    def test_animation_never_owns_domain_outcome(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "ANIMATION_IS_PRESENTATION_CONSUMER_NOT_DOMAIN_AUTHORITY",
            "damage",
            "cost",
            "reward",
            "save",
            "progress",
            "exactly once",
        ):
            self.assertIn(marker, text)

    def test_external_runtime_requires_trial_pin_license_performance_and_rollback(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "TRIAL_APPROVED",
            "editor_exact_version",
            "runtime_exact_version_or_commit",
            "godot_exact_version",
            "license_evidence",
            "performance_baseline",
            "platform_export_validation",
            "removal_or_rollback",
            "NO_AUTOMATIC_PURCHASE_INSTALL_OR_FLEET_ROLLOUT",
        ):
            self.assertIn(marker, text)

    def test_spine_is_bounded_candidate_not_default_dependency(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        for marker in (
            "SPINE_CANDIDATE_NOT_DEFAULT_DEPENDENCY",
            "GDExtension",
            "AnimationPlayer",
            "Spine 4.3.xx",
            "two-color tinting",
            "screen blend mode",
            "Godot 4.7.1",
            "PROJECT_IMPORT_EXPORT_RUNTIME_NOT_RUN",
            "REVALIDATE_PRICE_AND_LICENSE_AT_DECISION_TIME",
        ):
            self.assertIn(marker, text)

    def test_template_records_decision_evidence_and_evidence_ceiling(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "route_record_id",
            "actual_consumer",
            "selected_route",
            "rejected_routes",
            "state_family",
            "rig_source_contract",
            "external_runtime_trial",
            "domain_authority_boundary",
            "validation_matrix",
            "rollback",
            "RESEARCHED",
            "RUNTIME_VERIFIED",
            "SHIP_APPROVED",
        ):
            self.assertIn(marker, text)

    def test_existing_active_owners_route_to_the_new_reference(self) -> None:
        route = "2d-character-animation-routing-and-rigging.md"
        self.assertIn(route, SOURCE_CATALOG.read_text(encoding="utf-8"))
        self.assertIn(route, SPRITE_CONTROLS.read_text(encoding="utf-8"))

    def test_learning_log_records_no_new_skill_or_retired_studio_reactivation(self) -> None:
        text = LEARNING_LOG.read_text(encoding="utf-8")
        for marker in (
            "2D character animation route",
            "새 Skill을 만들지 않는다",
            "retired Sprite Animation Studio를 재활성화하지 않는다",
            "문서 계약은 Godot runtime 증거가 아니다",
        ):
            self.assertIn(marker, text)

    def test_evidence_states_cannot_be_collapsed(self) -> None:
        text = ROUTING.read_text(encoding="utf-8")
        self.assertIn(
            "RESEARCHED != TRIAL_APPROVED != INSTALLED != IMPORTED != MACHINE_VERIFIED != RUNTIME_VERIFIED != HUMAN_APPROVED != SHIP_APPROVED",
            text,
        )


if __name__ == "__main__":
    unittest.main()
