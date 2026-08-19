# Workstream backlog reconciliation · 2026-08-19

> **Supersession:** the earlier assumption "open PR = protected active worker" is superseded by `OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`. The user confirmed `CURRENT_COORDINATOR_CHAT` is the only active work chat. Findings below remain evidence, but #530/#535/#537 are now coordinator backlog to revalidate and finish; they are not protected merely because they are open.

## P01 / Project workspace schema consumer
- current completed main has schema v2 while `tests/test_notion_project_workspace_contract.py` still asserts v1.
- active PR #530 already changes this consumer and advances the workspace contract toward schema v3.
- coordinator disposition: `DUPLICATE_ACTIVE_WORKSTREAM / READ_ONLY`; recheck after #530 completes.

## P02 / strict multi-alias legacy parser
- multi-alias stale-ID parsing remains a valid robustness improvement.
- implementing it requires `.github/reference-freshness.json` companion semantics currently edited by #530.
- coordinator disposition: `DEFER_PROTECTED_ACTIVE_WORKSTREAM`; do not lose the finding.

## P04 / legacy Sheet planning inventory
- `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md` still contains active-looking Sheet/Figma legacy language on completed main.
- its canonical migration policy/tests are actively modified by #530.
- coordinator disposition: preserve main file during #530; revalidate and migrate after #530 completes.

## Human Home absorption into Project OS
- the new self-contained Home policy is implemented in a conflict-free canonical document and Notion contract.
- `skills/managing-game-project-operating-system/SKILL.md` and `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` are #530-owned active paths, so direct absorption is deferred until #530 completion.
