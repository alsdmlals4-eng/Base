# Project Work Kanban Checklist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an evidence-backed project work checklist and GitHub-native Kanban operating contract that lets GPT act as PM without creating a second project canon.

**Architecture:** Existing project repository owners remain canonical. A Goal/Playable Slice issue owns the durable work goal, independent work items own separately executable tasks, `PROJECT_WORK_ITEM_CHECKLIST.md` owns the reusable card receipt, and GitHub Projects is documented as an optional derived view. Existing startup reconciliation, continuous-work queues, development gates, and GitHub lifecycle policy are extended rather than replaced.

**Tech Stack:** Markdown contracts and templates, GitHub Issue Forms YAML, Python `unittest`, existing GitHub Actions validation.

**Spec:** `docs/superpowers/specs/2026-09-01-project-work-kanban-checklist-design.md`

## Global Constraints

- Repository owners, actual implementation, tests, assets, and evidence remain canonical; checklist and Projects views are derived operational surfaces.
- No HTML dashboard, new paid PM service, new Skill, new runtime schema, new workflow, or fleet-wide empty artifact rollout.
- Plain Markdown task-list checkboxes are used; retired GitHub tasklist blocks are not introduced.
- `[x]` is reserved for `PASS`; `NOT_APPLICABLE` is excluded from the denominator; `0/0` is not complete.
- `IN_PROGRESS` WIP is 1 and `VERIFY_REVIEW` WIP is 1 for the default solo-development profile.
- Missing Projects or sub-issue write capability must not block work and must not be reported as configured.
- Existing open/draft/ready PRs remain read-only.
- Branch baseline is `32f4dd5ba6042dc34611e2c8912f300b90491e0a`.

---

### Task 1: Add the failing contract tests

**Files:**
- Create: `tests/test_project_work_kanban_checklist_contract.py`

**Interfaces:**
- Consumes: existing repository paths and text contracts.
- Produces: `ProjectWorkKanbanChecklistContractTests`, discovered by `python -m unittest discover -s tests -v`.

- [ ] **Step 1: Write the failing test file**

```python
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
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests/test_project_work_kanban_checklist_contract.py -v
```

Expected: FAIL because `PROJECT_WORK_ITEM_CHECKLIST.md` and both Issue Forms do not exist and existing owners do not contain the new contract tokens.

In a connector-only environment, publish this test-only commit to the isolated branch, open a draft PR, and use exact-head GitHub Actions as the authoritative RED evidence.

- [ ] **Step 3: Record RED evidence**

Record the exact HEAD SHA, failing test names, workflow run ID, and failure reason in the draft PR. Do not describe infrastructure errors as product failures.

---

### Task 2: Add the reusable card and lifecycle contract

**Files:**
- Create: `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md`
- Modify: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`

**Interfaces:**
- Consumes: existing `ready_tasks / deferred_tasks / completed_tasks`, development evidence levels, Issue/Goal/PR lifecycle.
- Produces: `PROJECT_WORK_KANBAN_CHECKLIST`, card state/progress rules, optional Projects profile, connector limitation receipts.

- [ ] **Step 1: Create the minimal card template**

Write a template containing the exact metadata and sections asserted by Task 1. Include these checklist examples:

```markdown
- [x] PASS — 완료 항목. evidence: `<command, URL, path, capture, SHA>`
- [ ] IN_PROGRESS — 현재 수행 중인 항목. owner: `<owner>`
- [ ] READY — 선행 조건을 충족한 다음 항목.
- [ ] BLOCKED_UNVERIFIED — blocker: `<missing source, executor, or evidence>`
- [ ] USER_DECISION_REQUIRED — decision: `<meaning-changing choice>`
- [ ] DEFERRED — resume_condition: `<observable condition>`
- [ ] FAIL — evidence: `<reproduced failure>`
- [ ] NOT_APPLICABLE — reason: `<why this item does not apply>`
```

Add a compact evidence matrix for E0–E6 and state explicitly that the complete Development Gates contract is linked rather than duplicated.

- [ ] **Step 2: Extend the lifecycle policy**

Append one bounded section that:

- defines Goal/Slice parent issues and independent work items;
- requires reuse of an existing same-goal Issue before creation;
- distinguishes plain Markdown task lists from retired tasklist blocks;
- defines status, WIP, progress, evidence, queue mappings, and completion conditions;
- documents Projects as optional derived view;
- groups `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, and `DEFERRED` into the derived `BLOCKED_DECISION` board column;
- records `UNVERIFIED_PROJECTS_CONFIGURATION` and `UNVERIFIED_SUB_ISSUE_RELATION` when current tools cannot read back those relationships;
- prohibits HTML dashboards, paid PM tools, and automatic fleet rollout.

- [ ] **Step 3: Run focused tests**

Run:

```bash
python -m unittest tests/test_project_work_kanban_checklist_contract.py -v
```

Expected: remaining failures are limited to startup routing and missing Issue Forms.

- [ ] **Step 4: Commit**

```bash
git add docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md
git commit -m "docs: define evidence-backed project work cards"
```

---

### Task 3: Route startup remaining work and add Issue Forms

**Files:**
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- Create: `.github/ISSUE_TEMPLATE/01-goal-playable-slice.yml`
- Create: `.github/ISSUE_TEMPLATE/02-independent-work-item.yml`

**Interfaces:**
- Consumes: startup receipt `remaining_required_work` and `work_order`.
- Produces: work-item refs, progress summary, bounded Goal/Slice and task intake forms.

- [ ] **Step 1: Extend startup routing**

Add `PROJECT_WORK_KANBAN_CHECKLIST_REQUIRED` and a receipt section:

```yaml
project_work_kanban:
  goal_or_slice_issue_ref:
  work_item_refs: []
  active_work_item_ref:
  board_or_view_ref:
  board_configuration_status: NOT_APPLICABLE | VERIFIED | UNVERIFIED_PROJECTS_CONFIGURATION
  sub_issue_relation_status: NOT_APPLICABLE | VERIFIED | UNVERIFIED_SUB_ISSUE_RELATION
  progress_summary:
    completed_items:
    applicable_items:
    display:
  blocked_or_decision_items: []
  next_action:
```

Require existing same-goal Issue/card reuse, no issue explosion, and user-visible status order `READY / IN_PROGRESS / VERIFY_REVIEW / BLOCKED_DECISION / DONE`.

- [ ] **Step 2: Create the Goal/Slice Issue Form**

Use GitHub Issue Form fields with required IDs:

- `project`
- `player_or_user_value`
- `scope`
- `acceptance_criteria`
- `canon_owner`
- `evidence`

Include derived-view and no-second-canon guidance in a Markdown block.

- [ ] **Step 3: Create the independent work item form**

Use required IDs:

- `parent_issue_ref`
- `why_now`
- `dependencies`
- `actual_consumers`
- `acceptance_criteria`
- `verification`

Include `NO_ISSUE_EXPLOSION` guidance and a field for blocker/resume condition.

- [ ] **Step 4: Run focused tests**

Run:

```bash
python -m unittest tests/test_project_work_kanban_checklist_contract.py -v
```

Expected: all focused tests PASS.

- [ ] **Step 5: Commit**

```bash
git add templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md .github/ISSUE_TEMPLATE/01-goal-playable-slice.yml .github/ISSUE_TEMPLATE/02-independent-work-item.yml
git commit -m "docs: route project work through kanban checklists"
```

---

### Task 4: Verify integration and close the branch gate

**Files:**
- Read and update only if required by validation: `.github/reference-freshness.json`, `docs/DOCUMENTATION_MAP.md`, or existing tests.
- Do not modify Skill Registry, workflows, or unrelated PRs unless a concrete failing validator proves the need.

**Interfaces:**
- Consumes: all Task 1–3 outputs.
- Produces: exact-head verification, review findings, readback, and merge-ready evidence.

- [ ] **Step 1: Run focused and adjacent tests**

```bash
python -m unittest \
  tests/test_project_work_kanban_checklist_contract.py \
  tests/test_github_work_item_lifecycle_policy.py \
  tests/test_work_project_start_canon_checklist_contract.py \
  -v
```

Expected: PASS with zero failures and zero errors.

- [ ] **Step 2: Run full local validation when the repository is available**

```bash
python tools/run_local_validation.py
```

If the complete repository cannot be materialized, record `LOCAL_FULL_VALIDATION_NOT_RUN` and rely on exact-head remote CI; do not claim local PASS.

- [ ] **Step 3: Run structural negative controls**

Temporarily mutate a disposable local copy so each control fails, then restore:

- mark `READY` with `[x]`;
- count `NOT_APPLICABLE` in the denominator;
- call Projects canonical;
- remove the repository owner/readback section;
- remove the connector limitation receipt;
- remove the no-issue-explosion rule.

- [ ] **Step 4: Push exact HEAD and inspect CI**

Verify all required checks for the exact branch HEAD. Record workflow run IDs and conclusions. A previous SHA does not count.

- [ ] **Step 5: Perform five full-scope adversarial loops**

Each loop re-reads the entire retained diff and checks:

1. authority and second-canon drift;
2. issue/card granularity and WIP;
3. progress/evidence overclaim;
4. connector capability and fallback honesty;
5. existing owner, PR, cost, and rollout non-regression.

Fix validated findings and rerun impacted tests after every change.

- [ ] **Step 6: Complete PR and merge gates**

Confirm latest main, exact HEAD, required checks, independent review, unresolved threads zero, ruleset, and no conflicting same-goal PR. Use normal squash merge only when all gates pass; never force push, direct-push main, or bypass rules.

- [ ] **Step 7: Postmerge readback**

Read the new main SHA and every changed file, rerun required checks on the merged state when available, and report evidence ceilings separately from project adoption/runtime/Human/Player evidence.
