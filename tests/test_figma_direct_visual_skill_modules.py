from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART_ROOT = ROOT / "skills/designing-art-prompts-and-technique-cards"


class FigmaDirectVisualSkillModuleTests(unittest.TestCase):
    def test_existing_art_skill_routes_figma_direct_modules_without_registry_expansion(self) -> None:
        art_skill = (ART_ROOT / "SKILL.md").read_text(encoding="utf-8")
        gate = (
            ART_ROOT / "references/figma-visual-bible-continuity-gate.md"
        ).read_text(encoding="utf-8")
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        profile = (ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").read_text(encoding="utf-8")

        modules = (
            "figma-direct-placement-and-canon.md",
            "character-identity-expression-controls.md",
            "sprite-pose-sequence-controls.md",
            "effect-stage-compositing-controls.md",
            "candidate-review-and-reusable-harvest.md",
            "local-visual-tool-lessons-and-fallback.md",
        )
        for module in modules:
            self.assertTrue((ART_ROOT / "references" / module).exists(), module)
            self.assertIn(module, gate)

        self.assertIn("references/figma-visual-bible-continuity-gate.md", art_skill)
        self.assertIn("FIGMA_DIRECT_VISUAL_ORGANIZATION", gate)

        entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "designing-art-prompts-and-technique-cards"
        )
        for existing_tag in (
            "image-prompt",
            "image-mockup",
            "image-approval",
            "visual-qa-and-approval",
        ):
            self.assertIn(existing_tag, entry["trigger_tags"])

        self.assertFalse(
            any(item["skill_id"].startswith("figma-") for item in registry["skills"]),
            "Figma direct operation must remain a module of the existing art Skill",
        )
        self.assertFalse(
            any(item["skill_id"].startswith("expression-") for item in registry["skills"]),
            "Expression controls must remain a module of the existing art Skill",
        )
        self.assertFalse(
            any(item["skill_id"].startswith("sprite-") for item in registry["skills"]),
            "Sprite controls must remain a module of the existing art Skill",
        )

        for page in ("01_APPROVED_REFERENCE", "02_WIP", "04_FINAL"):
            self.assertIn(page, profile)

    def test_figma_module_prefers_auto_placement_with_exact_manual_fallback(self) -> None:
        figma_module = (
            ART_ROOT / "references/figma-direct-placement-and-canon.md"
        ).read_text(encoding="utf-8")

        for token in (
            "FIGMA_WRITE_AVAILABLE",
            "AUTO_PLACE_WIP",
            "FIGMA_WRITE_UNAVAILABLE",
            "EXACT_PLACEMENT_GUIDANCE",
            "02_WIP",
            "01_APPROVED_REFERENCE",
            "04_FINAL",
        ):
            self.assertIn(token, figma_module)
        self.assertIn("explicit user approval", figma_module)
        self.assertIn("readback", figma_module)
        self.assertIn("PROJECT_ASSET_APPROVED", figma_module)

    def test_modules_preserve_existing_harvest_and_product_authority(self) -> None:
        candidate_module = (
            ART_ROOT / "references/candidate-review-and-reusable-harvest.md"
        ).read_text(encoding="utf-8")
        for classification in (
            "REUSE_AS_IS",
            "VARIANT_SEED",
            "STRUCTURE_PATTERN",
            "STYLE_DNA",
            "REBUILD_FOR_REUSE",
            "ONE_OFF_KEEP",
            "REJECT_REUSE",
        ):
            self.assertIn(classification, candidate_module)
        self.assertIn("Reusable Visual Harvest Gate", candidate_module)
        self.assertIn("PROJECT_ASSET_APPROVED", candidate_module)

    def test_local_visual_runtime_is_reference_only_not_deleted(self) -> None:
        fallback_module = (
            ART_ROOT / "references/local-visual-tool-lessons-and-fallback.md"
        ).read_text(encoding="utf-8")
        for source_path in (
            ROOT / "tools/tool-hub",
            ROOT / "tools/expression-studio",
            ROOT / "tools/sprite-animation-studio",
        ):
            self.assertTrue(source_path.exists(), str(source_path))
        for token in (
            "REFERENCE_ONLY_FOR_VISUAL_WORKFLOW",
            "2026-08-18",
            "Tool Hub",
            "Expression Studio",
            "Sprite Animation Studio",
            "normal image-work path",
        ):
            self.assertIn(token, fallback_module)


if __name__ == "__main__":
    unittest.main()
