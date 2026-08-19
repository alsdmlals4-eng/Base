from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class GptFirstNotionProjectLifecycleTests(unittest.TestCase):
    def test_long_horizon_declares_gpt_primary_and_codex_optional(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "GPT_PRIMARY_PLANNING_REVIEW",
            "CODEX_OPTIONAL_SUB_EXECUTOR",
            "GPT_FINAL_REVIEW_AUTHORITY",
            "ONE_SHOT_CODEX_HANDOFF_WHEN_NEEDED",
        ):
            self.assertIn(term, policy)

    def test_visual_checkpoint_precedes_poc_or_demo_when_visuals_matter(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        visual = read("docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md")
        for term in (
            "NOTION_VISUAL_CHECKPOINT_BEFORE_POC",
            "UX_UI_REPRESENTATIVE_STATE_REQUIRED",
            "APPROVED_VISUALS_FEED_POC",
        ):
            self.assertIn(term, policy)
            self.assertIn(term, visual)

    def test_retired_user_facing_surfaces_are_absorbed_then_removed(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        retirement = read("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md")
        for term in (
            "DEPRECATED_SURFACE_ABSORB_THEN_DELETE",
            "USER_FACING_LOCAL_TOOL_DEFAULT: RETIRED",
            "HTML_PROJECT_SURFACE: RETIRED",
            "GOOGLE_SHEETS_MIGRATE_THEN_REMOVE",
        ):
            self.assertIn(term, policy)
            self.assertIn(term, retirement)
        self.assertIn("Git history", retirement)
        self.assertIn("repository-native", retirement)

    def test_cost_policy_keeps_gpt_pro_only_and_notion_paid_opt_in(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "CURRENT_PAID_PLANS: GPT_PRO",
            "PAID_PLAN_COUNT: 1",
            "NOTION_PAID_ON_REQUEST_ONLY",
            "COST_BENEFIT_EVIDENCE_BEFORE_NOTION_UPGRADE",
        ):
            self.assertIn(term, policy)

    def test_completion_report_teaches_rules_skills_modules_and_effects(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "USER_LEARNING_COMPLETION_REPORT",
            "핵심 규칙",
            "핵심 Skill",
            "핵심 모듈",
            "변경 전",
            "변경 후",
            "장기 효과",
            "재검토 조건",
        ):
            self.assertIn(term, policy)

    def test_approval_cycle_requires_review_sync_pr_gate_and_readback(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "APPROVAL_TO_ADVERSARIAL_REVIEW_SYNC_PR_READBACK",
            "GitHub",
            "Notion",
            "EXACT-HEAD PR GATE",
            "POSTMERGE READBACK",
        ):
            self.assertIn(term, policy)


if __name__ == "__main__":
    unittest.main()
