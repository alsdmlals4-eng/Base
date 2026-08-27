# Work Instruction Superset Reconciliation — Implementation Plan

> **Approval reference:** 2026-08-27 user request to compare v4.8 r5.4, v4.9 Terra-Max and project-derived additions; preserve core capability, correct omissions, require startup core-fun/system/SWOT/remaining-work/work-order canon correction, and absorb only project-neutral lessons.

## Goal

Extend the current Base Work bundle without copying historical instructions into a second canon.

The implementation must preserve the merged startup checklist from PR #735 and add a thin, discoverable evidence-identity contract for recurring Work→Codex→Godot→CI→Notion failures.

## Current authority

- Base completed main: `1df8878d8a99d91a318ad4adff722d78c763a69a`
- Proposal: BCP-2026-039 / PR #737
- Existing active owners retained:
  - `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md`
  - `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
  - `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
  - current CI, Godot, Visual, Git synchronization and continuous-work owners

## Approved implementation scope

1. Add a project-neutral evidence/identity owner.
2. Add a thin current router that loads existing current owners instead of duplicating them.
3. Add a non-regression/case receipt explaining what was preserved, improved, delegated, rejected as project-specific or corrected as unsafe generalization.
4. Add focused RED→GREEN contract tests.
5. Verify exact-head required workflows, five full-scope adversarial loops, safe squash merge and new-main readback.

## Excluded and protected scope

- no modification of another open PR;
- no `[수정제안서]/PROPOSAL_REGISTRY.json` update while PR #678 owns it;
- no Visual generation approval-policy change;
- no engine baseline, dependency, provider, CI workflow or ruleset change;
- no project name, PR/Issue number, exact project SHA, path, resolution, UI composition, style lock or completed feature list;
- no Human/Player evidence promotion;
- no direct main push, force push, reset/clean or ruleset bypass.

## TDD task sequence

### Task 1 — RED contract

Create `tests/test_work_instruction_superset_reconciliation_contract.py` that requires:

- thin current router and current-owner links;
- product baseline vs router/document sync identity separation;
- exact candidate freshness/invalidation;
- CI result-chain integrity and exact validator/head evidence;
- Godot cache/source identity/adopted addon classification;
- Visual candidate vs runtime promotion interface;
- local-only vs remote-synchronized locator state;
- completed automation/heartbeat cleanup;
- project-specific exclusion and Human/Player evidence ceilings.

Verify the test fails on the branch while the required owner/router/case are absent.

### Task 2 — minimal GREEN owner

Create:

- `templates/project-operations/WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
- `templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- `docs/knowledge/cases/WORK_INSTRUCTION_SUPERSET_RECONCILIATION_CASE.md`

The router must remain thin and point to current owners. The evidence contract must be conditional and project-neutral.

### Task 3 — regression and adversarial verification

Run/observe:

- Python syntax;
- focused unittest;
- current Base required workflows on exact head;
- changed-file and open-PR concurrency audit;
- minimum five full-scope adversarial loops.

### Task 4 — closeout

- update PR body with exact RED/GREEN and exact-head evidence;
- verify unresolved threads/reviews/conflicts;
- squash merge only if current repository gates pass;
- read back new `main` and new files;
- update proposal PR #737 with implementation result without taking over its Registry-owned conflict;
- recalculate remaining machine-executable work.

## Rollback

Revert the implementation squash commit. Existing v4.9 Starter, PR #735 startup checklist, current CI/Godot/Visual owners and project canons remain intact because this implementation is additive and thin-routed.
