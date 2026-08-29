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
        for term in (
            "Visual Requirement Gate",
            "requirement_id",
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "EXISTING_APPROVED_ASSET_REUSE_FIRST",
        ):
            self.assertIn(term, image_policy)

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

    def test_visual_workflow_produces_first_and_harvests_only_after_primary_use(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
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

        for token in (
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "PROJECT_LOCAL_ASSET_VAULT_POLICY.md",
            "EXISTING_APPROVED_ASSET_REUSE_FIRST",
            "LOCAL_CANDIDATE",
            "explicit promotion",
        ):
            self.assertIn(token, policy)

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
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        for token in (
            "primary-use success",
            "reuse promotion",
            "PROJECT_ASSET_APPROVED",
            "title-specific identity",
        ):
            self.assertIn(token, guide)
        for token in (
            "LOCAL_CANDIDATE",
            "TRACKED_PRODUCTION_ASSET",
            "PROJECT_ASSET_APPROVED",
            "명시적 `promote`",
            "GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED",
        ):
            self.assertIn(token, policy)

    def test_image_conversation_uses_generate_then_lock_and_marks_two_turn_route_superseded(self) -> None:
        gate = read(
            "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
        )
        for token in (
            "PROJECT_REVIEW_COMPLETE",
            "NEED_DRIVEN_GENERATE_THEN_LOCK",
            "GENERATE_ONE_CANDIDATE_BEFORE_LOCK",
            "USER_LOCK_REVISE_REJECT_AFTER_GENERATION",
            "GENERATE_EXACTLY_ONE",
            "STOP_REQUIRED_AFTER_GENERATION",
            "NO_AUTOMATIC_IMAGE_CHAIN",
            "ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE__SUPERSEDED",
        ):
            self.assertIn(token, gate)

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
        self.assertIn("system", gate)

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
            self.assertIn("TEXT_BRIEF_STOP_REQUIRED", content)
            self.assertIn("GENERATE_EXACTLY_ONE", content)
        self.assertIn("NEXT_USER_EXPLICIT_APPROVAL", project_visual_gate)
        self.assertIn("STOP_REQUIRED_AFTER_GENERATION", project_visual_gate)


if __name__ == "__main__":
    unittest.main()
