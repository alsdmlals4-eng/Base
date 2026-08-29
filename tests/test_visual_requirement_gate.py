from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class VisualRequirementGateTests(unittest.TestCase):
    def test_existing_art_guide_owns_visual_requirement_gate(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        for term in (
            "Visual Requirement Gate",
            "Delete Test",
            "FUNCTIONAL",
            "INFORMATIONAL",
            "FEEDBACK",
            "EXPLANATORY",
            "IDENTITY",
            "EMOTIONAL",
            "DECORATIVE",
            "PLATFORM_REQUIRED",
            "REFERENCE_ONLY",
            "P0 BLOCKER",
            "P1 CLARITY",
            "P2 CONSISTENCY",
            "P3 DELIGHT",
            "REUSE_SYSTEM",
            "REUSE_PROJECT",
            "ADAPT_EXISTING",
            "SOURCE_EXISTING",
            "GENERATE_EXPLORATION",
            "CREATE_CUSTOM",
            "DEFER",
            "CUT",
        ):
            self.assertIn(term, guide)

    def test_planning_templates_capture_selection_reasoning(self) -> None:
        art_brief = read("templates/planning/ART_DIRECTION_BRIEF.md")
        for term in (
            "requirement_id",
            "surface_or_flow",
            "player_question",
            "element_type",
            "role",
            "why_needed",
            "delete_test",
            "consumer",
            "priority",
            "reuse_candidate",
            "disposition",
            "required_states",
            "accessibility_equivalent",
            "validation",
        ):
            self.assertIn(term, art_brief)

        ui_template = read("templates/planning/GAME_UX_UI_SYSTEM.md")
        for term in (
            "Visual Requirement Gate",
            "why_needed",
            "delete_test",
            "reuse_candidate",
            "priority",
            "disposition",
        ):
            self.assertIn(term, ui_template)

    def test_existing_consumers_use_gate_without_new_broad_skill(self) -> None:
        for path in (
            "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
        ):
            self.assertIn("Visual Requirement Gate", read(path), path)

        image_policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        self.assertIn("Visual Requirement Gate", image_policy)
        self.assertIn("requirement_id", image_policy)
        self.assertIn("REUSE_SYSTEM", image_policy)
        self.assertIn("GENERATE_EXPLORATION", image_policy)

        registry = read("skills/SKILL_REGISTRY.json")
        self.assertNotIn("selecting-project-visual-assets", registry)
        self.assertFalse((ROOT / "skills" / "selecting-project-visual-assets").exists())

    def test_routes_and_asset_authority_boundaries_are_explicit(self) -> None:
        for path in (
            "START_HERE.md",
            "docs/DOCUMENTATION_MAP.md",
            "docs/knowledge/game-development/README.md",
        ):
            content = read(path)
            self.assertIn("Visual Requirement Gate", content, path)

        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        self.assertIn("ASSET_MANIFEST.yml", guide)
        self.assertIn("PROJECT_LOCAL_ASSET_VAULT_POLICY.md", guide)
        self.assertIn("요구사항", guide)
        self.assertIn("파일", guide)

    def test_visual_workflow_routes_primary_use_and_harvest_to_existing_owner(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
        plan = read("templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md")

        for token in (
            "Primary Use Gate",
            "Reusable Visual Harvest Gate",
            "REUSE_AS_IS",
            "VARIANT_SEED",
            "STRUCTURE_PATTERN",
            "STYLE_DNA",
            "REBUILD_FOR_REUSE",
            "ONE_OFF_KEEP",
            "REJECT_REUSE",
            "SOURCE_LAYER",
            "MASK_CUTOUT",
            "MANUAL_OR_SEMANTIC_REBUILD",
            "DERIVED_GENERATIVE_RECOVERY",
        ):
            self.assertIn(token, guide)
            self.assertIn(token, gate)

        self.assertIn("IMAGE_CONVERSATION_APPROVAL_GATE.md", policy)
        self.assertIn("PRIMARY_USE_GATE_REQUIRED_AFTER_USER_LOCK", gate)
        self.assertIn("REUSABLE_VISUAL_HARVEST_ONLY_AFTER_PRIMARY_USE_SUCCESS", gate)

        for token in (
            "primary_use_status",
            "harvest_status",
            "reuse_classification",
            "decomposition_method",
            "asset_vault_harvest_record_id",
            "second_use_validation",
        ):
            self.assertIn(token, plan)

    def test_reuse_never_auto_promotes_or_overrides_primary_quality(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
        for content in (guide, gate):
            self.assertIn("primary-use success", content)
            self.assertIn("reuse promotion", content)
            self.assertIn("PROJECT_ASSET_APPROVED", content)
            self.assertIn("title-specific identity", content)

    def test_image_conversation_uses_candidate_first_then_post_generation_lock(self) -> None:
        gate = read(
            "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
        )
        for token in (
            "PROJECT_REVIEW_COMPLETE",
            "NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK",
            "GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION",
            "USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION",
            "GENERATE_EXACTLY_ONE",
            "STOP_REQUIRED_AFTER_GENERATION",
            "NO_AUTOMATIC_IMAGE_CHAIN",
        ):
            self.assertIn(token, gate)
        self.assertLess(
            gate.index("NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK"),
            gate.rindex("LEGACY_SUPERSEDED_ONLY"),
        )

    def test_legacy_two_turn_tokens_are_inactive_compatibility_only(self) -> None:
        gate = read(
            "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
        )
        self.assertIn("LEGACY_SUPERSEDED_ONLY", gate)
        for token in (
            "ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE",
            "TEXT_BRIEF_STOP_REQUIRED",
            "NEXT_USER_EXPLICIT_APPROVAL",
        ):
            self.assertIn(token, gate)
            self.assertGreater(gate.rindex(token), gate.index("LEGACY_SUPERSEDED_ONLY"))

    def test_image_conversation_gate_declares_host_platform_precedence(self) -> None:
        gate = read(
            "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
        )
        for token in (
            "HOST_PLATFORM_PRECEDENCE",
            "HOST_POLICY_OVERRIDE",
            "RUNTIME_ENFORCEMENT_NOT_GUARANTEED",
        ):
            self.assertIn(token, gate)
        self.assertIn("상위", gate)
        self.assertIn("시스템", gate)

    def test_current_visual_owners_route_to_image_conversation_gate(self) -> None:
        contract = read(
            "docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md"
        )
        dashboard_skill = read("skills/building-project-visual-dashboards/SKILL.md")
        project_visual_gate = read(
            "skills/designing-art-prompts-and-technique-cards/references/"
            "notion-project-visual-continuity-gate.md"
        )
        for content in (contract, dashboard_skill, project_visual_gate):
            self.assertIn("IMAGE_CONVERSATION_APPROVAL_GATE.md", content)
            self.assertIn("GENERATE_EXACTLY_ONE", content)
        self.assertIn("STOP_REQUIRED_AFTER_GENERATION", project_visual_gate)

    def test_candidate_first_contract_is_not_weakened_by_legacy_visual_consumers(self) -> None:
        gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
        self.assertIn("CURRENT_TURN_EXPLICIT_IMAGE_REQUEST", gate)
        self.assertIn("VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK", gate)
        self.assertIn("LOCK / REVISE / REJECT / REFERENCE_ONLY", gate)

    def test_comparison_sheet_is_not_runtime_asset(self) -> None:
        pipeline = read(
            "docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md"
        )
        self.assertIn("COMPARISON_SHEET_NOT_PRODUCTION_ASSET", pipeline)
        self.assertIn("SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR", pipeline)


if __name__ == "__main__":
    unittest.main()
