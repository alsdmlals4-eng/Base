from __future__ import annotations

import re
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


def markdown_section(text: str, heading: str) -> str:
    """Return one exact level-2 Markdown section, excluding later sections."""
    start = text.find(heading)
    if start < 0:
        raise AssertionError(f"missing section: {heading}")
    match = re.search(r"^## (?!#)", text[start + len(heading) :], flags=re.MULTILINE)
    if match is None:
        return text[start:]
    return text[start : start + len(heading) + match.start()]


def require_markers(test: unittest.TestCase, text: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        test.assertIn(marker, text)


class CharacterAnimationRoutingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.routing = ROUTING.read_text(encoding="utf-8")
        cls.template = TEMPLATE.read_text(encoding="utf-8")
        cls.source_catalog = SOURCE_CATALOG.read_text(encoding="utf-8")
        cls.sprite_controls = SPRITE_CONTROLS.read_text(encoding="utf-8")
        cls.learning_log = LEARNING_LOG.read_text(encoding="utf-8")

    def test_route_owner_compares_four_materially_distinct_paths(self) -> None:
        preamble = self.routing.split("## 1. 먼저 해결할 플레이어 문제", 1)[0]
        comparison = markdown_section(self.routing, "## 2. 비교할 네 경로")
        selection = markdown_section(self.routing, "## 3. Route 선택 규칙")
        require_markers(
            self,
            preamble,
            (
                "FRAME_DEFAULT_UNLESS_EVIDENCE",
                "MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3",
            ),
        )
        for route in (
            "FRAME",
            "GODOT_NATIVE_RIG",
            "EXTERNAL_RIG_RUNTIME",
            "EXTERNAL_RIG_BAKED",
        ):
            self.assertIn(f"`{route}`", comparison)
            self.assertIn(f"### `{route}`", selection)

    def test_route_is_consumer_and_measurement_driven(self) -> None:
        section = markdown_section(self.routing, "## 1. 먼저 해결할 플레이어 문제")
        require_markers(
            self,
            section,
            (
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
            ),
        )

    def test_rig_ready_source_contract_requires_hidden_overlap_and_attachment_data(self) -> None:
        section = markdown_section(self.routing, "## 4. Rig-ready source art 계약")
        require_markers(
            self,
            section,
            (
                "hidden_underlap",
                "overlap_margin",
                "pivot",
                "parent_bone",
                "draw_order",
                "deformation_safe_area",
                "attachment_slot",
                "skin_group",
                "RIG_READY_SOURCE_IS_NOT_RUNTIME_ASSET",
            ),
        )

    def test_state_family_and_interruption_contract_are_explicit(self) -> None:
        states = markdown_section(self.routing, "## 5. 행동 상태군과 단계")
        interruption = markdown_section(self.routing, "## 6. 중단·재진입·접근성 계약")
        require_markers(
            self,
            states,
            (
                "Wind-up",
                "Active",
                "Recovery",
                "Hit",
                "Stagger",
                "Knockdown",
                "Rise",
                "Transition",
            ),
        )
        require_markers(
            self,
            interruption,
            (
                "can_interrupt",
                "interrupt_windows",
                "same_state_reentry",
                "rapid_repeat_behavior",
                "instant_complete_behavior",
                "pause_resume",
                "save_resume_pose",
                "reduced_motion_fallback",
                "missing_asset_fallback",
            ),
        )

    def test_animation_never_owns_domain_outcome(self) -> None:
        section = markdown_section(self.routing, "## 7. Domain 권위 경계")
        require_markers(
            self,
            section,
            (
                "ANIMATION_IS_PRESENTATION_CONSUMER_NOT_DOMAIN_AUTHORITY",
                "damage",
                "cost",
                "reward",
                "save",
                "progress",
                "exactly once",
            ),
        )

    def test_interruptible_windup_commits_only_at_domain_active_transition(self) -> None:
        domain = markdown_section(self.routing, "## 7. Domain 권위 경계")
        require_markers(
            self,
            domain,
            (
                "DOMAIN_OWNS_ACTION_CLOCK_AND_ACTIVE_COMMIT",
                "wind-up",
                "authoritative active transition",
                "exactly once",
                "animation event cannot advance",
                "start cost / reservation",
                "refund·forfeit",
            ),
        )
        self.assertNotIn(
            "결과를 exactly once 확정한 뒤 visual adapter가 표현 sequence를 요청",
            domain,
        )

        start = self.template.index("domain_authority_boundary:")
        end = self.template.index("\nexternal_runtime_trial:", start)
        template_domain = self.template[start:end]
        require_markers(
            self,
            template_domain,
            (
                "wind_up_start_predicate",
                "authoritative_active_transition",
                "start_cost_or_reservation_predicate",
                "active_outcome_commit_predicate",
                "cancel_refund_or_forfeit_predicate",
                "committed_visual_payload",
            ),
        )

    def test_external_runtime_requires_trial_pin_license_performance_and_rollback(self) -> None:
        preamble = self.routing.split("## 1. 먼저 해결할 플레이어 문제", 1)[0]
        section = markdown_section(self.routing, "## 8. 외부 리그 Runtime trial 기록")
        require_markers(
            self,
            preamble,
            ("NO_AUTOMATIC_PURCHASE_INSTALL_OR_FLEET_ROLLOUT",),
        )
        require_markers(
            self,
            section,
            (
                "TRIAL_APPROVED",
                "editor_exact_version",
                "runtime_exact_version_or_commit",
                "godot_exact_version",
                "license_evidence",
                "performance_baseline",
                "platform_export_validation",
                "removal_or_rollback",
                "A = FRAME baseline",
                "B = GODOT_NATIVE_RIG baseline",
                "C = EXTERNAL_RIG_RUNTIME candidate",
            ),
        )

    def test_spine_is_bounded_candidate_not_default_dependency(self) -> None:
        preamble = self.routing.split("## 1. 먼저 해결할 플레이어 문제", 1)[0]
        section = markdown_section(self.routing, "## 9. Spine 후보의 현재 1차 자료 snapshot")
        require_markers(
            self,
            preamble,
            ("SPINE_CANDIDATE_NOT_DEFAULT_DEPENDENCY",),
        )
        require_markers(
            self,
            section,
            (
                "GDExtension",
                "AnimationPlayer",
                "Spine 4.3.xx",
                "two-color tinting",
                "screen blend mode",
                "Godot 4.7.1",
                "PROJECT_IMPORT_EXPORT_RUNTIME_NOT_RUN",
                "REVALIDATE_PRICE_AND_LICENSE_AT_DECISION_TIME",
            ),
        )

    def test_every_route_uses_the_same_auditable_decision_axes(self) -> None:
        alternatives_start = self.template.index("alternatives:")
        alternatives_end = self.template.index("\nselected_route:", alternatives_start)
        alternatives = self.template[alternatives_start:alternatives_end]
        routes = (
            "FRAME",
            "GODOT_NATIVE_RIG",
            "EXTERNAL_RIG_RUNTIME",
            "EXTERNAL_RIG_BAKED",
        )
        axes = (
            "player_value_fit",
            "visual_identity_and_silhouette",
            "authoring_and_revision_cost",
            "runtime_performance",
            "platform_and_export_fit",
            "license_and_distribution",
            "maintenance_and_versioning",
            "removal_and_rollback",
            "evidence",
            "disposition",
        )
        for index, route in enumerate(routes):
            start = alternatives.index(f"  - route: {route}")
            end = (
                alternatives.index(f"  - route: {routes[index + 1]}", start)
                if index + 1 < len(routes)
                else len(alternatives)
            )
            route_block = alternatives[start:end]
            require_markers(self, route_block, axes)

    def test_template_parts_preserve_per_part_source_and_mirroring_fields(self) -> None:
        contract_start = self.template.index("rig_source_contract:")
        parts_start = self.template.index("  parts:", contract_start)
        parts_end = self.template.index("  protected_identity:", parts_start)
        parts = self.template[parts_start:parts_end]
        require_markers(
            self,
            parts,
            (
                "      mirror_allowed:",
                "      source_path:",
                "      source_sha256:",
            ),
        )

    def test_runtime_windows_validation_can_be_not_applicable(self) -> None:
        start = self.template.index("  runtime_windows:")
        end = self.template.index("  runtime_android_or_other_target:", start)
        section = self.template[start:end]
        self.assertIn("NOT_APPLICABLE", section)

    def test_template_preserves_installed_and_imported_evidence_states(self) -> None:
        status_line = next(
            line for line in self.template.splitlines() if line.startswith("status:")
        )
        self.assertIn("INSTALLED", status_line)
        self.assertIn("IMPORTED", status_line)

    def test_template_records_decision_evidence_and_evidence_ceiling(self) -> None:
        require_markers(
            self,
            self.template,
            (
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
            ),
        )
        self.assertLess(self.template.index("actual_consumer:"), self.template.index("selected_route:"))
        self.assertLess(self.template.index("selected_route:"), self.template.index("validation_matrix:"))
        self.assertLess(self.template.index("validation_matrix:"), self.template.index("\nrollback:\n"))

    def test_existing_active_owners_route_to_the_new_reference(self) -> None:
        source_section = markdown_section(
            self.source_catalog, "## 8. 2D 캐릭터 애니메이션·리깅 Route"
        )
        sprite_section = markdown_section(
            self.sprite_controls, "## Animation route and rig-ready source boundary"
        )
        self.assertIn(
            "skills/evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md",
            source_section,
        )
        self.assertIn(
            "../../evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md",
            sprite_section,
        )
        self.assertIn("../../../templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md", sprite_section)
        require_markers(
            self,
            sprite_section,
            (
                "Do not cut a finished flat image",
                "Do not force rig-ready decomposition",
                "not import, machine, runtime, performance, Human, or shipping proof",
            ),
        )

    def test_learning_log_records_no_new_skill_or_retired_studio_reactivation(self) -> None:
        section = markdown_section(
            self.learning_log,
            "## 2026-09-03 — 2D character animation route must precede rig-ready source or runtime adoption",
        )
        require_markers(
            self,
            section,
            (
                "2D character animation route",
                "새 Skill을 만들지 않는다",
                "retired Sprite Animation Studio를 재활성화하지 않는다",
                "문서 계약은 Godot runtime 증거가 아니다",
            ),
        )

    def test_evidence_states_cannot_be_collapsed(self) -> None:
        section = markdown_section(self.routing, "## 11. 검증과 증거 상한")
        self.assertIn(
            "RESEARCHED != TRIAL_APPROVED != INSTALLED != IMPORTED != MACHINE_VERIFIED != RUNTIME_VERIFIED != HUMAN_APPROVED != SHIP_APPROVED",
            section,
        )


if __name__ == "__main__":
    unittest.main()
