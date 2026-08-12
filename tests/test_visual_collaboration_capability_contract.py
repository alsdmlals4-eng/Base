from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VisualCollaborationCapabilityContractTests(unittest.TestCase):
    def test_policy_keeps_tools_reusable_and_noncanonical(self):
        text = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        for token in ("GDD", "EXTERNAL_COLLABORATION", "BOTH", "VISUAL_CANONICAL_CONFLICT", "IMPLEMENTATION_PINNED", "NOT_RUN"):
            self.assertIn(token, text)
        self.assertIn("do not create a `figma-*`", text.lower())

    def test_registry_template_records_context_and_handoff_evidence(self):
        data = json.loads((ROOT / "templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json").read_text(encoding="utf-8"))
        item = data["artifacts"][0]
        for field in ("usage_context", "responsible_document_id", "related_decision_ids", "snapshot_path", "source_commit", "implementation_scope", "excluded_scope"):
            self.assertIn(field, item)

    def test_documentation_map_routes_existing_responsibilities_to_the_shared_policy(self):
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("VISUAL_COLLABORATION_TOOL_POLICY.md", text)
        self.assertIn("CAPABILITY_COMPOSITION_MAP.md", text)

    def test_figma_visual_bible_profile_keeps_stage_and_authority_boundaries(self):
        policy = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        profile = (ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").read_text(encoding="utf-8")

        for token in (
            "Project Figma Visual Bible",
            "00_DIRECTION",
            "01_APPROVED_REFERENCE",
            "02_WIP",
            "03_REJECTED",
            "04_FINAL",
            "APPROVED_VISUAL_REFERENCE",
            "PROJECT_ASSET_APPROVED",
        ):
            self.assertIn(token, policy)

        for token in (
            "VISUAL_CANONICAL_CONFLICT",
            "visual_status",
            "product_asset_status",
            "Keep / Avoid / Do Not Drift",
            "CHAR_",
            "UI_",
            "BATTLE_",
        ):
            self.assertIn(token, profile)

        self.assertIn("제품 자산 승격은 별도 asset lifecycle", profile)

    def test_art_generation_routes_through_figma_continuity_gate(self):
        skill = (ROOT / "skills/designing-art-prompts-and-technique-cards/SKILL.md").read_text(encoding="utf-8")
        gate = (
            ROOT
            / "skills/designing-art-prompts-and-technique-cards/references/figma-visual-bible-continuity-gate.md"
        ).read_text(encoding="utf-8")
        plan = (ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md").read_text(encoding="utf-8")

        self.assertIn("references/figma-visual-bible-continuity-gate.md", skill)
        self.assertIn("APPROVED_VISUAL_REFERENCE", skill)
        self.assertIn("Keep / Avoid / Do Not Drift", skill)

        for token in (
            "APPROVED_VISUAL_REFERENCE",
            "Keep / Avoid / Do Not Drift",
            "BLOCKED_UNVERIFIED",
            "VISUAL_CANONICAL_CONFLICT",
            "PROJECT_ASSET_APPROVED",
        ):
            self.assertIn(token, gate)

        for token in (
            "figma_visual_bible_status",
            "figma_approved_reference_ids",
            "figma_approved_frame_or_node_ids",
            "figma_wip_target",
            "figma_sync_status",
        ):
            self.assertIn(token, plan)

        self.assertIn("Figma `04_FINAL`", plan)
        self.assertIn("PROJECT_ASSET_APPROVED", plan)


if __name__ == "__main__":
    unittest.main()
