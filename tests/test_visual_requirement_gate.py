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
        self.assertIn("선정", image_policy)

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

        for content in (guide, policy):
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
                self.assertIn(token, content)

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
        for content in (guide, policy):
            self.assertIn("primary-use success", content)
            self.assertIn("reuse promotion", content)
            self.assertIn("PROJECT_ASSET_APPROVED", content)
            self.assertIn("title-specific identity", content)

    def test_image_generation_requires_two_turn_hard_barrier(self) -> None:
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        layout = read("docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md")
        combined = "\n".join((policy, workflow, layout))
        for term in (
            "IMAGE_TWO_TURN_HARD_BARRIER",
            "PROJECT_REVIEW_COMPLETE",
            "VISUAL_NEED_DEFINED",
            "TEXT_BRIEF_COMPLETE",
            "STOP_REQUIRED",
            "EXPLICIT_IMAGE_APPROVAL",
            "GENERATE_EXACTLY_ONE",
        ):
            self.assertIn(term, combined)
        self.assertIn("동일 assistant 응답", combined)
        self.assertIn("자동", combined)

    def test_image_policy_uses_notion_first_and_keeps_google_sheets_migration_only(self) -> None:
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE", policy)
        self.assertIn("GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL", policy)
        self.assertNotIn("## 2. B — 프로젝트 Google Sheets 구조", policy)
        self.assertNotIn("PROJECT_SHEET_CONFIGURED", policy)
        self.assertNotIn("필수 탭:", policy)


if __name__ == "__main__":
    unittest.main()
