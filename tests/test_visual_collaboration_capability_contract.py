from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class VisualCollaborationCapabilityContractTests(unittest.TestCase):
    def test_policy_keeps_collaboration_contexts_noncanonical(self):
        text = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for token in (
            "GDD",
            "EXTERNAL_COLLABORATION",
            "BOTH",
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "V4_NOTION_EXCEPTION_ONLY",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "PROJECT_RELATION_REQUIRED",
            "REPOSITORY_RUNTIME_TRUTH",
            "Intermediate visual checkpoint",
            "MISSING_CANON",
            "DRAFT_VISUAL",
        ):
            self.assertIn(token, text)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", text)

    def test_registry_template_keeps_generic_handoff_evidence(self):
        data = json.loads(read("templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json"))
        item = data["artifacts"][0]
        for field in (
            "usage_context",
            "responsible_document_id",
            "related_decision_ids",
            "snapshot_path",
            "source_commit",
            "implementation_scope",
            "excluded_scope",
            "screen_id",
            "flow_id",
            "interpretation_status",
            "runtime_compare_status",
        ):
            self.assertIn(field, item)

    def test_documentation_map_routes_shared_visual_responsibilities(self):
        text = read("docs/DOCUMENTATION_MAP.md")
        self.assertIn("VISUAL_COLLABORATION_TOOL_POLICY.md", text)
        self.assertIn("NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md", text)
        self.assertIn("CAPABILITY_COMPOSITION_MAP.md", text)

    def test_notion_asset_workflow_preserves_stage_and_authority_boundaries(self):
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        for token in (
            "PROJECT_RELATION_REQUIRED",
            "ASSET_KNOWLEDGE_MASTER",
            "VISUAL_MAP_DERIVED",
            "PROJECT_ASSET_APPROVED",
            "REPOSITORY_RUNTIME_TRUTH",
        ):
            self.assertIn(token, policy + workflow)
        for token in (
            "WIP",
            "APPROVED",
            "REPLACED",
            "ARCHIVED",
            "source provenance",
            "readback",
        ):
            self.assertIn(token, workflow)
        self.assertFalse((ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").exists())
        self.assertFalse((ROOT / "templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md").exists())

    def test_art_generation_routes_through_project_visual_continuity_gate(self):
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        gate = read(
            "skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md"
        )
        plan = read("templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md")

        self.assertIn("references/notion-project-visual-continuity-gate.md", skill)
        self.assertNotIn("figma-visual-bible-continuity-gate.md", skill)
        for token in (
            "APPROVED_VISUAL_REFERENCE",
            "Keep / Avoid / Do Not Drift",
            "BLOCKED_UNVERIFIED",
            "VISUAL_CANONICAL_CONFLICT",
            "PROJECT_ASSET_APPROVED",
            "PROJECT_RELATION_REQUIRED",
        ):
            self.assertIn(token, gate)
        for token in (
            "project_relation",
            "approved_visual_reference_ids",
            "visual_map_status",
            "readback_status",
            "screen_id",
            "flow_id",
        ):
            self.assertIn(token, plan)

    def test_visual_flow_records_interpretation_and_runtime_compare_without_tool_lock_in(self):
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        gate = read(
            "skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md"
        )
        plan = read("templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md")
        registry = json.loads(read("templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json"))
        item = registry["artifacts"][0]

        for token in (
            "VISUAL_MAP_DERIVED",
            "screen IDs",
            "primary/secondary/conditional",
            "runtime evidence",
        ):
            self.assertIn(token, policy)
        for token in (
            "screen_id",
            "flow_id",
            "INTERPRETATION_RECORD",
            "DISCOVERED_IDEA",
            "AI_ASSUMPTION",
            "RUNTIME_CAPTURE",
        ):
            self.assertIn(token, gate)
        for token in (
            "screen_id",
            "flow_id",
            "interpretation_record_id",
            "interpretation_status",
            "runtime_compare_required",
            "runtime_capture_path",
            "drift_status",
        ):
            self.assertIn(token, plan)
        for field in ("screen_id", "flow_id", "interpretation_status", "runtime_compare_status"):
            self.assertIn(field, item)

    def test_reusable_visual_harvest_uses_asset_master_without_becoming_asset_authority(self):
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        registry = json.loads(read("templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json"))
        item = registry["artifacts"][0]

        for token in (
            "REUSE_AS_IS",
            "VARIANT_SEED",
            "STRUCTURE_PATTERN",
            "STYLE_DNA",
            "REBUILD_FOR_REUSE",
            "ONE_OFF_KEEP",
            "REJECT_REUSE",
        ):
            self.assertIn(token, workflow)
        for field in (
            "reuse_classification",
            "reuse_source_artifact_id",
            "asset_vault_harvest_record_id",
            "derived_pixel_status",
        ):
            self.assertIn(field, item)
        self.assertIn("reuse promotion", policy)
        self.assertIn("PROJECT_ASSET_APPROVED", workflow)

    def test_persistent_character_additive_visual_layer_gate(self):
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        for token in (
            "PERSISTENT_CHARACTER_ADDITIVE_VISUAL_LAYER_GATE",
            "persistent character identity",
            "additive visual layers",
            "final composite",
            "small gameplay scale",
            "identity / motif / palette / hierarchy",
            "true transformation",
        ):
            self.assertIn(token, workflow)

    def test_deprecated_visual_execution_surfaces_stay_deleted(self):
        for path in (
            "tools/figma-bridge",
            "tools/expression-studio",
            "tools/sprite-animation-studio",
            "tools/tool-hub",
            "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md",
            "templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md",
            "templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md",
        ):
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
