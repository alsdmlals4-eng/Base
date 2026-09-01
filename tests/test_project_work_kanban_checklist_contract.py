from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectWorkKanbanChecklistContractTests(unittest.TestCase):
    def test_owner_defines_kanban_checklist_without_new_canon(self):
        owner = read("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md")
        for token in (
            "PROJECT_WORK_KANBAN_CHECKLIST", "CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON",
            "PM_WORK_BREAKDOWN_REQUIRED", "REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE",
            "NO_ISSUE_EXPLOSION", "BACKLOG", "READY", "IN_PROGRESS", "VERIFY_REVIEW",
            "BLOCKED_DECISION", "BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED", "DONE",
            "PROJECTS_DERIVED_VIEW_NOT_CANON", "NO_PROJECTS_WRITE_CAPABILITY_IS_NOT_BLOCKER",
            "UNVERIFIED_PROJECTS_CONFIGURATION", "UNVERIFIED_SUB_ISSUE_RELATION",
            "NO_PROJECT_FACT_WRITEBACK_FROM_CARD", "Progress = PASS 항목 수 / 적용 가능한 항목 수",
            "REQUIRED_CHILD_WORK_ITEM_DONE", "NO_APPLICABLE_CHECKLIST", "서로 다른 퍼센트를 평균내지 않는다",
            "NO_NEW_PAID_PM_TOOL", "NO_HTML_DASHBOARD", "NO_FLEET_WIDE_EMPTY_ARTIFACT_ROLLOUT",
        ):
            self.assertIn(token, owner)

    def test_template_has_operational_card_and_evidence_ceiling(self):
        template = read("templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md")
        for token in (
            "work_item_id:", "GOAL_SLICE | INDEPENDENT_TASK", "required_child_work_item_refs:",
            "CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON", "canon_owner:", "actual_consumers:",
            "acceptance_criteria:", "required_evidence:", "source_main_sha:", "task_branch_or_pr:",
            "blocker:", "next_action:", "resume_condition:", "[x] PASS", "[ ] IN_PROGRESS",
            "[ ] READY", "[ ] BLOCKED_UNVERIFIED", "[ ] USER_DECISION_REQUIRED", "[ ] DEFERRED",
            "[ ] NOT_APPLICABLE", "NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR",
            "PARENT_GOAL_PROGRESS_USES_REQUIRED_CHILD_DONE_COUNT", "DO_NOT_AVERAGE_CHILD_PERCENTAGES",
            "NO_APPLICABLE_CHECKLIST", "E0_CONTRACT", "E1_STATIC", "E2_TEST", "E3_RUNTIME",
            "E4_VISUAL", "E5_PLAY", "E6_HUMAN_PLAYTEST", "NOT_RUN",
            "자동 테스트 PASS는 runtime·화면·UX·Human/Player·사용자 승인·출시 PASS를 의미하지 않는다.",
        ):
            self.assertIn(token, template)

    def test_startup_materializes_existing_work_items_before_new_cards(self):
        startup = read("templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md")
        for token in (
            "PROJECT_WORK_KANBAN_CHECKLIST_REQUIRED", "REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE",
            "PROJECTS_DERIVED_VIEW_NOT_CANON", "UNVERIFIED_PROJECTS_CONFIGURATION",
            "UNVERIFIED_SUB_ISSUE_RELATION", "작은 순차 단계는 부모 카드 내부 체크리스트로 유지",
            "완료 후보에서 remaining-work recalculation", "progress_summary",
        ):
            self.assertIn(token, startup)
        # The startup contract now publishes executable JSON, not the retired YAML sketch.
        section = startup.split("### 12.1 Receipt extension", 1)[1].split("### 12.2", 1)[0]
        match = re.search(r"```json\s*\n(.*?)\n```", section, re.S)
        self.assertIsNotNone(match)
        projection = json.loads(match.group(1))
        board = projection["project_work_kanban"]
        self.assertIn("work_item_refs", board)
        self.assertIn("work_items", board)
        self.assertEqual(board["work_item_refs"], [item["work_item_id"] for item in board["work_items"]])

    def test_issue_forms_use_same_checklist_contract(self):
        for path in (".github/ISSUE_TEMPLATE/feature-task.yml", ".github/ISSUE_TEMPLATE/goal.yml"):
            form = read(path)
            for token in ("id: work_tracking", "PROJECT_WORK_ITEM_CHECKLIST.md", "PM_WORK_TRACKING", "Verification Matrix"):
                self.assertIn(token, form)
            self.assertNotIn("HTML", form)
            self.assertNotIn("Figma", form)

    def test_intake_and_continuation_reuse_existing_pm_owner(self):
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        sequencing = read("skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md")
        continuous = read("skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md")
        for content in (intake, sequencing, continuous):
            self.assertIn("PROJECT_WORK_KANBAN_CHECKLIST", content)
            self.assertIn("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md", content)
        self.assertIn("GPT_PM_CONTINUOUS_CHECKLIST_UPDATE", continuous)
        self.assertIn("NO_BOARD_CREATION_WITHOUT_CAPABILITY_READBACK", continuous)
        self.assertIn("PM_BOARD_UPDATE_AFTER_MATERIAL_TASK_STATE_CHANGE", continuous)

    def test_bootstrap_and_index_route_to_template(self):
        for path in ("templates/project-operations/PROJECT_OPERATING_SYSTEM_BOOTSTRAP_INDEX.md", "templates/project-operations/TEMPLATE_INDEX.md"):
            self.assertIn("PROJECT_WORK_ITEM_CHECKLIST.md", read(path))


if __name__ == "__main__":
    unittest.main()
