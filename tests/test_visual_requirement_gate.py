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

    def test_existing_skills_consume_gate_without_new_broad_skill(self) -> None:
        for path in (
            "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            "skills/auditing-and-refining-ui-art/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
        ):
            self.assertIn("Visual Requirement Gate", read(path), path)

        image_policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
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


if __name__ == "__main__":
    unittest.main()
