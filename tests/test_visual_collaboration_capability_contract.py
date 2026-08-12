from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VisualCollaborationCapabilityContractTests(unittest.TestCase):
    def test_policy_keeps_tools_reusable_and_noncanonical(self):
        text = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        for token in (
            "GDD",
            "EXTERNAL_COLLABORATION",
            "BOTH",
            "VISUAL_CANONICAL_CONFLICT",
            "IMPLEMENTATION_PINNED",
            "NOT_RUN",
            "Project Visual Flow Workspace",
            "INTERPRETATION_RECORD",
            "DISCOVERED_IDEA",
            "AI_ASSUMPTION",
            "PROTOTYPE_FLOW",
            "RUNTIME_CAPTURE",
            "COMPARE_BOARD",
            "IMPLEMENTATION_GAP",
            "AI_MOCKUP_ERROR",
        ):
            self.assertIn(token, text)
        self.assertIn("do not create a `figma-*`", text.lower())
        self.assertIn("prototype", text.lower())
        self.assertIn("runtime", text.lower())
        self.assertIn("정본", text)

    def test_existing_skills_own_interpretation_and_runtime_compare(self):
        art_text = (ROOT / "skills/designing-art-prompts-and-technique-cards/SKILL.md").read_text(encoding="utf-8")
        for token in ("INTERPRETATION_RECORD", "CONFIRMED", "DISCOVERED_IDEA", "AI_ASSUMPTION"):
            self.assertIn(token, art_text)

        ui_text = (ROOT / "skills/auditing-and-refining-ui-art/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "PROTOTYPE_FLOW",
            "RUNTIME_CAPTURE",
            "COMPARE_BOARD",
            "MATCHED",
            "INTENDED_DIFFERENCE",
            "IMPLEMENTATION_GAP",
            "PLANNING_CHANGE_REQUIRED",
            "AI_MOCKUP_ERROR",
        ):
            self.assertIn(token, ui_text)

    def test_registry_template_records_context_and_handoff_evidence(self):
        data = json.loads((ROOT / "templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json").read_text(encoding="utf-8"))
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

    def test_image_review_plan_tracks_visual_flow_interpretation(self):
        text = (ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md").read_text(encoding="utf-8")
        for token in (
            "screen_id",
            "flow_id",
            "figma_artifact_id",
            "interpretation_status",
            "runtime_compare_required",
            "runtime_capture_path",
            "drift_status",
        ):
            self.assertIn(token, text)

    def test_sheet_visual_index_stays_compact_but_tracks_flow_state(self):
        text = (ROOT / "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md").read_text(encoding="utf-8")
        self.assertIn("06_시각_작업면", text)
        self.assertIn("Screen/Flow ID", text)
        self.assertIn("해석 요약", text)
        self.assertIn("Runtime 비교 상태", text)
        self.assertIn("전문을 복사하지 않는다", text)

    def test_documentation_map_routes_existing_responsibilities_to_the_shared_policy(self):
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("VISUAL_COLLABORATION_TOOL_POLICY.md", text)
        self.assertIn("CAPABILITY_COMPOSITION_MAP.md", text)


if __name__ == "__main__":
    unittest.main()
