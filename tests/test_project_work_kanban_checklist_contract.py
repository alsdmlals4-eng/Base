from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md"
START_CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
CARD = ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md"
GOAL_FORM = ROOT / ".github/ISSUE_TEMPLATE/01-goal-playable-slice.yml"
TASK_FORM = ROOT / ".github/ISSUE_TEMPLATE/02-independent-work-item.yml"


class ProjectWorkKanbanChecklistContractTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"required project work surface must exist: {path}")
        return path.read_text(encoding="utf-8")

    def test_lifecycle_policy_defines_canonical_and_derived_roles(self) -> None:
        text = self._read(POLICY)
        for token in (
            "PROJECT_WORK_KANBAN_CHECKLIST",
            "GOAL_OR_PLAYABLE_SLICE_PARENT_ISSUE",
            "INDEPENDENT_WORK_ITEM",
            "CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON",
            "PROJECTS_DERIVED_VIEW_NOT_CANON",
            "NO_PROJECTS_WRITE_CAPABILITY_IS_NOT_BLOCKER",
            "UNVERIFIED_PROJECTS_CONFIGURATION",
            "UNVERIFIED_SUB_ISSUE_RELATION",
        ):
            self.assertIn(token, text)

    def test_policy_defines_status_wip_and_queue_mapping(self) -> None:
        text = self._read(POLICY)
        for token in (
            "BACKLOG",
            "READY",
            "IN_PROGRESS",
            "VERIFY_REVIEW",
            "BLOCKED_UNVERIFIED",
            "USER_DECISION_REQUIRED",
            "DEFERRED",
            "DONE",
            "IN_PROGRESS_WIP_LIMIT: 1",
            "VERIFY_REVIEW_WIP_LIMIT: 1",
            "ready_tasks",
            "deferred_tasks",
            "completed_tasks",
        ):
            self.assertIn(token, text)

    def test_policy_counts_only_pass_and_excludes_not_applicable(self) -> None:
        text = self._read(POLICY)
        for token in (
            "PASS_ONLY_COUNTS_COMPLETE",
            "NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR",
            "NO_APPLICABLE_CHECKLIST",
            "completed_items / applicable_items",
            "PLAIN_MARKDOWN_TASK_LIST_NOT_RETIRED_TASKLIST_BLOCK",
        ):
            self.assertIn(token, text)

    def test_card_template_has_authority_scope_evidence_and_readback(self) -> None:
        text = self._read(CARD)
        for token in (
            "work_item_id:",
            "parent_issue_ref:",
            "goal_or_slice:",
            "player_or_user_value:",
            "why_now:",
            "depends_on:",
            "blocked_by:",
            "protected_scope:",
            "canon_owner:",
            "actual_consumers:",
            "source_main_sha:",
            "acceptance_criteria:",
            "required_evidence:",
            "evidence_ceiling:",
            "progress:",
            "next_action:",
            "resume_condition:",
            "Repository readback",
        ):
            self.assertIn(token, text)

    def test_card_template_checks_only_pass_items(self) -> None:
        text = self._read(CARD)
        self.assertIn("- [x] PASS —", text)
        for forbidden in (
            "- [x] READY —",
            "- [x] IN_PROGRESS —",
            "- [x] BLOCKED_UNVERIFIED —",
            "- [x] USER_DECISION_REQUIRED —",
            "- [x] DEFERRED —",
            "- [x] FAIL —",
            "- [x] NOT_APPLICABLE —",
        ):
            self.assertNotIn(forbidden, text)

    def test_start_checklist_materializes_remaining_work_into_existing_or_new_cards(self) -> None:
        text = self._read(START_CHECKLIST)
        for token in (
            "PROJECT_WORK_KANBAN_CHECKLIST_REQUIRED",
            "PROJECT_WORK_ITEM_CHECKLIST.md",
            "REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE",
            "NO_ISSUE_EXPLOSION",
            "READY / IN_PROGRESS / VERIFY_REVIEW / BLOCKED_DECISION / DONE",
            "progress_summary:",
            "work_item_refs:",
        ):
            self.assertIn(token, text)

    def test_issue_forms_collect_goal_and_independent_task_contracts(self) -> None:
        goal = self._read(GOAL_FORM)
        task = self._read(TASK_FORM)
        for token in (
            "name:",
            "description:",
            "id: project",
            "id: player_or_user_value",
            "id: scope",
            "id: acceptance_criteria",
            "id: canon_owner",
            "id: evidence",
        ):
            self.assertIn(token, goal)
        for token in (
            "name:",
            "description:",
            "id: parent_issue_ref",
            "id: why_now",
            "id: dependencies",
            "id: actual_consumers",
            "id: acceptance_criteria",
            "id: verification",
        ):
            self.assertIn(token, task)

    def test_policy_and_templates_reject_second_canon_and_extra_pm_products(self) -> None:
        bundle = "\n".join(
            self._read(path)
            for path in (POLICY, START_CHECKLIST, CARD, GOAL_FORM, TASK_FORM)
        )
        for token in (
            "NO_HTML_DASHBOARD",
            "NO_NEW_PAID_PM_TOOL",
            "NO_FLEET_WIDE_EMPTY_ARTIFACT_ROLLOUT",
            "repository",
            "derived",
        ):
            self.assertIn(token, bundle)
        self.assertNotRegex(bundle, re.compile(r"(?i)projects?\s*=\s*canonical"))


if __name__ == "__main__":
    unittest.main()
