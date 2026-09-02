from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md"
START_CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
CARD = ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md"
EVIDENCE_LOOP_PLAN = (
    ROOT / "docs/superpowers/plans/2026-09-02-evidence-loop-operational-projection.md"
)
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
            "work_item_type:",
            "parent_issue_ref:",
            "required_child_work_item_refs:",
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
            "progress_basis:",
            "next_action:",
            "resume_condition:",
            "Repository readback",
        ):
            self.assertIn(token, text)

    def test_card_distinguishes_parent_and_independent_progress(self) -> None:
        text = self._read(CARD)
        for token in (
            "PARENT_GOAL_PROGRESS_USES_REQUIRED_CHILD_DONE_COUNT",
            "DO_NOT_AVERAGE_CHILD_PERCENTAGES",
            "CHECKLIST_PASS",
            "REQUIRED_CHILD_WORK_ITEM_DONE",
            "required child work items whose status is DONE",
        ):
            self.assertIn(token, text)

    def test_card_template_checks_only_pass_items(self) -> None:
        text = self._read(CARD)
        checked_lines = [
            line.strip()
            for line in text.splitlines()
            if re.match(r"^\s*-\s*\[x\]", line)
        ]
        self.assertTrue(checked_lines, "card must show at least one evidence-backed PASS example")
        self.assertTrue(
            all(line.startswith("- [x] PASS —") for line in checked_lines),
            f"all checked examples must be PASS only: {checked_lines}",
        )
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

    def test_evidence_loop_projection_reuses_existing_owners_and_gates(self) -> None:
        policy = self._read(POLICY)
        card = self._read(CARD)
        for token in (
            "EVIDENCE_WORK_LOOP_PROJECTION",
            "PROJECT_WORK_ITEM_CHECKLIST.md §11",
        ):
            with self.subTest(surface="policy", token=token):
                self.assertIn(token, policy)
        for token in (
            "READ → PICK → BUILD → CHECK → COMMIT",
            "PROMPT / DESIGN / INBOX / STATUS",
            "PROMPT_DESIGN_INBOX_STATUS_ARE_ROLE_MAPS_NOT_DEFAULT_FILES",
            "INBOX_IS_NOT_EXECUTION_AUTHORITY",
            "HISTORICAL_ISSUE_825_NOT_CURRENT_WORK_AUTHORITY",
            "CURRENT_WORK_RECORD_IS_CURRENT_GOAL_ISSUE_OR_CARD",
            "Base Issue #825는 기존 PM execution-gate 구현을 마친 CLOSED 역사 증거",
            "종료된 Issue를 재사용해 triage·WIP·dependency·evidence readback을 건너뛰지 않는다.",
            "GUIDES_PROGRESSIVELY_LOADED_BY_SELECTED_WORK",
            "CHECKPOINT_IS_NOT_COMPLETION",
            "HUMAN_PLAYTEST_EXPLICIT_USER_GATE",
            "QUALITY_NOT_ASSUMED_TO_INCREASE_PER_LOOP",
            "NO_UNBOUNDED_REPEAT_WITHOUT_NEW_EVIDENCE",
        ):
            with self.subTest(surface="card", token=token):
                self.assertIn(token, card)

    def test_evidence_loop_plan_uses_the_rebased_base_and_mutable_head(self) -> None:
        plan = self._read(EVIDENCE_LOOP_PLAN)
        rebased_base = "9a620220cae371a41af92adbc2cfa9935860c000"
        retired_base = "a5a1e7eecc4c58a13c11b98b6c225cb1879e7167"

        self.assertIn(f"Base branch: `{rebased_base}`", plan)
        self.assertIn(
            f"--trusted-history-commit {rebased_base}",
            plan,
        )
        self.assertIn(
            f"--base {rebased_base} --head HEAD",
            plan,
        )
        self.assertNotIn(f"Base branch: `{retired_base}`", plan)
        self.assertNotIn(f"--trusted-history-commit {retired_base}", plan)
        self.assertNotIn(f"--base {retired_base}", plan)

    def test_start_checklist_materializes_remaining_work_into_existing_or_new_cards(self) -> None:
        text = self._read(START_CHECKLIST)
        for token in (
            "PROJECT_WORK_KANBAN_CHECKLIST_REQUIRED",
            "PROJECT_WORK_ITEM_CHECKLIST.md",
            "REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE",
            "NO_ISSUE_EXPLOSION",
            "READY / IN_PROGRESS / VERIFY_REVIEW / BLOCKED_DECISION / DONE",
            "progress_summary",
            "work_item_refs",
        ):
            self.assertIn(token, text)

        section = text.split("### 12.1 Receipt extension", 1)[1].split("### 12.2", 1)[0]
        match = re.search(r"```json\s*\n(.*?)\n```", section, re.S)
        self.assertIsNotNone(match, "startup checklist must publish one executable root JSON example")
        projection = json.loads(match.group(1))
        board = projection["project_work_kanban"]
        self.assertIn("source_main_sha", board)
        self.assertIn("work_item_refs", board)
        self.assertIn("work_items", board)
        self.assertEqual(
            board["work_item_refs"],
            [item["work_item_id"] for item in board["work_items"]],
        )

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
