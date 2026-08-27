from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class VisualGenerationScopeAndBatchIntegrityTests(unittest.TestCase):
    def test_ui_owner_defines_bounded_visual_generation_integrity(self):
        skill = read("skills/auditing-and-refining-ui-art/SKILL.md")
        for token in (
            "VISUAL_TASK_SCOPE_FIDELITY",
            "visual_question / target_screen / target_state / excluded_scope",
            "BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES",
            "DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY",
        ):
            self.assertIn(token, skill)

    def test_notion_workflow_records_bounded_outputs_without_weakening_original_first(self):
        workflow = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        for token in (
            "visual_question / target_screen / target_state / excluded_scope",
            "BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES",
            "NOTION_APPROVED_ORIGINAL_FIRST_GATE",
            "preview derivative",
        ):
            self.assertIn(token, workflow)

    def test_project_neutral_problem_lesson_case_is_discoverable_and_evidence_bounded(self):
        case_path = ROOT / "docs/knowledge/cases/AI_VISUAL_SCOPE_AND_BATCH_INTEGRITY_CASE.md"
        self.assertTrue(case_path.exists(), "approved BCP-035 case study must exist")
        case = case_path.read_text(encoding="utf-8")
        index = read("docs/knowledge/cases/README.md")
        for token in (
            "BCP-2026-035",
            "VISUAL_TASK_SCOPE_FIDELITY",
            "BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES",
            "DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY",
            "human comprehension",
        ):
            self.assertIn(token, case)
        self.assertIn("AI_VISUAL_SCOPE_AND_BATCH_INTEGRITY_CASE.md", index)
        for project_only_token in (
            "E+D HYBRID",
            "SX59-POC-ACCEPT-003",
            "토끼 기관사",
        ):
            self.assertNotIn(project_only_token, case)


if __name__ == "__main__":
    unittest.main()
