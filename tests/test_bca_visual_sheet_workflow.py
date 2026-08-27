from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class BCAVisualSheetWorkflowTests(unittest.TestCase):
    def test_v9_is_active_and_v6_to_v8_are_compatibility_only(self) -> None:
        v9 = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md")
        v8 = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md")
        v7 = read("templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md")
        self.assertIn('contract_version: "9.1"', v9)
        self.assertIn("SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION", v9)
        self.assertIn("REPOSITORY_FIRST_INTERVIEW", v9)
        self.assertIn("INTEGRATED_DELIVERY_PROFILE", v9)
        self.assertIn("CONDITIONAL_RECONCILIATION", v9)
        self.assertIn("INTERMEDIATE_VISUAL_CHECKPOINT", v9)
        self.assertIn("SUPERSEDED_COMPATIBILITY", v8)
        self.assertIn("SUPERSEDED_COMPATIBILITY", v7)

    def test_notion_workspace_contract_separates_projects_and_runtime_truth(self) -> None:
        machine = json.loads(read("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"))
        self.assertEqual(machine["project_workspace"], "NOTION_DEFAULT_PROJECT_WORKSPACE")
        self.assertEqual(machine["project_relation"], "PROJECT_RELATION_REQUIRED")
        self.assertEqual(machine["visual_map"], "VISUAL_MAP_DERIVED")
        self.assertEqual(machine["runtime_truth"], "REPOSITORY_RUNTIME_TRUTH")

    def test_dashboard_skill_routes_to_notion_home_not_standalone_html(self) -> None:
        skill = read("skills/building-project-visual-dashboards/SKILL.md")
        registry = json.loads(read("skills/SKILL_REGISTRY.json"))
        entry = next(item for item in registry["skills"] if item["skill_id"] == "building-project-visual-dashboards")
        self.assertIn("NOTION_PROJECT_HOME_AND_VISUAL_MAP", skill)
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", skill)
        self.assertIn("Notion Project Home", skill)
        self.assertIn("standalone HTML", skill)
        self.assertIn("금지", skill)
        self.assertEqual("ACTIVE", entry["status"])
        self.assertTrue(any("notion" in text.lower() for text in entry["use_when"]))
        self.assertNotIn("html-dashboard", entry["trigger_tags"])
        self.assertNotIn("standalone-dashboard", entry["trigger_tags"])

    def test_rich_human_home_keeps_project_specific_data_and_ai_metadata_boundary(self) -> None:
        skill = read("skills/building-project-visual-dashboards/SKILL.md")
        policy = read("docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md")
        for token in (
            "PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED",
            "PROJECT_SPECIFIC_CORE_DATA",
            "AI_INTERPRETATION_FOR_USER_CORRECTION",
            "AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED",
            "HUMAN_EDIT_GUIDE_REQUIRED",
            "HOME_PROJECTION_IS_NOT_DUPLICATE_CANON",
        ):
            self.assertIn(token, policy)
        for token in (
            "PROJECT_SPECIFIC_CORE_DATA",
            "AI_INTERPRETATION_FOR_USER_CORRECTION",
            "HUMAN_EDIT_GUIDE_REQUIRED",
            "NO_UNIVERSAL_GAME_DATA_TEMPLATE",
        ):
            self.assertIn(token, skill)
        self.assertIn("30초 전체 그림", skill)
        self.assertIn("5분 핵심 Flow/System/Data/Visual", skill)
        self.assertIn("Prompt / AI Note / Hash / Implementation Path", skill)

    def test_image_conversation_gate_is_consumed_by_human_visual_owner(self) -> None:
        skill = read("skills/building-project-visual-dashboards/SKILL.md")
        gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
        layout = read("docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md")
        for token in (
            "TEXT_BRIEF_STOP_REQUIRED",
            "NEXT_USER_EXPLICIT_APPROVAL",
            "GENERATE_EXACTLY_ONE",
            "STOP_REQUIRED_AFTER_GENERATION",
            "NO_AUTOMATIC_IMAGE_CHAIN",
        ):
            self.assertIn(token, gate)
        for consumer in (skill, layout):
            self.assertIn("IMAGE_CONVERSATION_APPROVAL_GATE.md", consumer)
            self.assertIn("TEXT_BRIEF_STOP_REQUIRED", consumer)
            self.assertIn("GENERATE_EXACTLY_ONE", consumer)

    def test_explicit_image_request_routes_anchor_pipeline_without_removing_assistant_gate(self) -> None:
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
        pipeline = read(
            "docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md"
        )
        for text in (policy, gate):
            self.assertIn("PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md", text)
            self.assertIn("CURRENT_TURN_EXPLICIT_IMAGE_REQUEST", text)
            self.assertIn("EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY", text)
            self.assertIn("ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE", text)
            self.assertIn("NO_AUTOMATIC_IMAGE_CHAIN", text)
        self.assertIn("APPROVED_VISUAL_ANCHOR_FOUND", pipeline)
        self.assertIn("NO_USABLE_APPROVED_VISUAL_ANCHOR", pipeline)
        self.assertIn("COMPARISON_SHEET_NOT_PRODUCTION_ASSET", pipeline)

    def test_art_skill_contains_generation_and_review_modes(self) -> None:
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        for mode in (
            "planning-visualization",
            "intermediate-visual-checkpoint",
            "final-visual-candidate",
            "visual-qa-and-approval",
        ):
            self.assertIn(f"`{mode}`", skill)
        for status in (
            "GENERATED_EXPLORATION",
            "REVISION_REQUIRED",
            "PROJECT_ASSET_APPROVED",
            "APPLIED_AND_RUNTIME_VERIFIED",
        ):
            self.assertIn(status, skill)
        self.assertIn("생성 결과는 자동 최종 자산이 아니다", skill)

    def test_information_artifacts_are_not_promoted_to_explanatory_image_sheets(self) -> None:
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        plan = read("templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md")
        for text in (skill, policy, plan):
            self.assertIn("ACTUAL_CONSUMER_REQUIRED", text)
            self.assertIn("PRODUCTION_INFORMATION", text)
            self.assertIn("TEXT_TABLE_FLOW_DB_FIRST", text)
        for token in (
            "GAME_RUNTIME",
            "PLANNED_GAME_SURFACE",
            "PLAYER_FACING_EXPLANATORY",
            "PRODUCT_DISTRIBUTION",
        ):
            self.assertIn(token, policy)
            self.assertIn(token, plan)
        self.assertIn("DO_NOT_GENERATE", skill)
        self.assertIn("DO_NOT_GENERATE", policy)
        self.assertIn("시스템 설명", policy)
        self.assertIn("세계관", policy)
        self.assertIn("관계도", policy)
        self.assertIn("제작 체크리스트", policy)
        self.assertIn("structured information artifact", plan)

    def test_visual_workflow_absorbs_old_tool_principles_without_tool_dependency(self) -> None:
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for token in (
            "PROJECT_RELATION_REQUIRED",
            "source provenance",
            "Identity-preserving image edits",
            "version",
            "readback",
            "ASSET",
            "COMPONENT",
            "SCREEN",
            "REFERENCE",
            "BENCHMARK",
        ):
            self.assertIn(token, workflow)
        self.assertIn("Figma Bridge", workflow)
        self.assertIn("not required", workflow)
        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE", policy)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", policy)

    def test_visual_requirement_gate_is_consumed_without_duplicate_skill(self) -> None:
        guide = read("docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md")
        art_skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        slice_skill = read("skills/designing-vertical-slices/SKILL.md")
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        for text in (guide, art_skill, slice_skill, policy):
            self.assertIn("Visual Requirement Gate", text)
        self.assertIn("Delete Test", guide)
        self.assertIn("requirement_id", art_skill)
        self.assertIn("requirement_id", slice_skill)
        registry = read("skills/SKILL_REGISTRY.json")
        self.assertNotIn("selecting-project-visual-assets", registry)

    def test_reference_visuals_are_recreated_not_surface_copied(self) -> None:
        skill = read("skills/designing-art-prompts-and-technique-cards/SKILL.md")
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        for text in (skill, policy):
            self.assertIn("PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md", text)
            self.assertIn("reference_brief", text)
            self.assertIn("forbidden_expression", text)
            self.assertIn("reference_similarity_status", text)
            self.assertIn("RELEASE_BLOCKED_UNVERIFIED", text)

    def test_registry_routes_existing_visual_work_without_duplicate_skill(self) -> None:
        registry = json.loads(read("skills/SKILL_REGISTRY.json"))
        entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "designing-art-prompts-and-technique-cards"
        )
        for tag in (
            "planning-visualization",
            "intermediate-visual-checkpoint",
            "final-visual-candidate",
            "visual-qa-and-approval",
            "image-mockup",
            "image-approval",
        ):
            self.assertIn(tag, entry["trigger_tags"])

    def test_active_entrypoints_reference_v9_not_v7(self) -> None:
        for path in (
            "START_HERE.md",
            "docs/DOCUMENTATION_MAP.md",
            "templates/project-operations/README.md",
        ):
            text = read(path)
            self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md", text, path)

    def test_sheets_are_migration_only_until_verified_removal(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        self.assertIn("MIGRATION_ONLY_UNTIL_REMOVAL", policy)
        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE", policy)
        self.assertIn("UNIQUE / DUPLICATE / OBSOLETE", policy)
        self.assertIn("MIGRATED_READBACK_VERIFIED", policy)
        self.assertIn("active consumer/reference", policy)
        self.assertIn("Do not bulk-copy", policy)

    def test_project_asset_delivery_requires_readback_and_explicit_promotion(self) -> None:
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        local_policy = read("docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md")
        image_policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        self.assertIn("read back", workflow)
        self.assertIn("PROJECT_ASSET_APPROVED", local_policy)
        self.assertIn("PROJECT_ASSET_APPROVED", image_policy)
        self.assertIn("promotion", workflow.lower())

    def test_visual_workspace_supports_gdd_external_and_both_contexts_without_new_authority(self) -> None:
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for context in ("GDD", "EXTERNAL_COLLABORATION", "BOTH"):
            self.assertIn(context, policy)
        self.assertIn("PROJECT_RELATION_REQUIRED", policy)
        self.assertIn("REPOSITORY_RUNTIME_TRUTH", policy)

    def test_reusable_visual_harvest_uses_asset_master_not_figma_profile(self) -> None:
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        visual_policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        self.assertIn("REUSE_AS_IS", workflow)
        self.assertIn("REBUILD_FOR_REUSE", workflow)
        self.assertIn("ONE_OFF_KEEP", workflow)
        self.assertIn("ASSET_KNOWLEDGE_MASTER", visual_policy)
        self.assertFalse((ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").exists())

    def test_player_experience_validation_uses_release_near_visual_audio_vfx_integration(self) -> None:
        visual_policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        slice_skill = read("skills/designing-vertical-slices/SKILL.md")
        for text in (visual_policy, slice_skill):
            self.assertIn("RELEASE_NEAR_VERTICAL_SLICE_FIRST", text)
            self.assertIn("SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED", text)
            self.assertIn("SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE", text)
        self.assertNotIn("VISUALIZED_POC_BEFORE_DEMO_TEST", visual_policy)
        self.assertNotIn("VISUAL_NOT_MATERIAL_TO_THIS_POC", visual_policy)


if __name__ == "__main__":
    unittest.main()
