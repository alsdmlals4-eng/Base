# Unified Work and Lean Delivery Implementation Plan

> Execution: inline with bounded, disjoint consumer updates. Existing user approval is reused; no new scope approval or forced executor switch.

**Goal:** Let an authorized, capable Work session complete approved planning, product implementation, verification and integration without app-name-based handoffs; reduce duplicate procedure without reducing acceptance.

**Authority:** User approval in this task on 2026-09-16, following the research/recommendation report; baseline Base main `d830c0f6967678eed3c208ac6b24f9cd1b262ec3`.

**Owners:** `docs/GPT_CODEX_WORKFLOW_POLICY.md` owns capability/role routing; `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` owns bounded completion; existing game production guides own UI/data principles. No new Skill, scheduler, framework or external subscription.

**Protected:** unrelated PRs/worktrees, released/frozen artifacts, V3 history, project-specific gameplay and engine pins, asset approvals, external permissions. This Base change does not install/uninstall plugins, mutate existing automations or mass-migrate projects.

## Tasks

- [x] Confirm current authority, compare existing rules and official sources, run existing routing baseline and independent scenario baseline.
- [x] Correct canonical routing and existing handoff Skill/reference: capability-scoped execution, optional handoff, honest partial verification, preserved authorization and evidence.
- [x] Propagate to current Work/project entrypoints, templates and machine consumers; retire contradicted role instructions rather than add an overlay only.
- [x] Consolidate same-contract approval/research/review budgets, scoped freshness/testing and milestone publication in existing owners.
- [x] Add simple-control/deep-system/inspectable-causality and JSON-content/module-computation guidance to existing guides without converting current projects.
- [ ] Validate consumer behavior after changes, update superseded tests with current invariants, run repository validation and exactly two independent review rounds.
- [ ] Commit/push current-task branch; pass exact-head CI/review/rulesets, squash merge, read back main and provide a reusable project adoption prompt.

## Evaluation

Baseline scenarios: capable Work with routine implementation request; Work with authoring but no runtime; same-scope correction after approval; missing repo permissions; explicit handoff request; image candidate without approval; exhausted two-round budget. Check decisions and evidence ceilings, not just policy token presence.

Full validation: `python tools/run_local_validation.py --trusted-history-commit d830c0f6967678eed3c208ac6b24f9cd1b262ec3`. Baseline focused routing: 29 tests passed. No actual game runtime, plugin A/B usage reduction or multi-project adoption claim follows from policy tests.

## Research disposition

- ADOPT: OpenAI progressive skill disclosure, https://learn.chatgpt.com/docs/build-skills; task-matching skills, not all-body loading.
- ADAPT: Anthropic long-running agents, https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents; incremental end-to-end delivery and durable progress, not web-demo success as Godot proof.
- ADAPT: DORA small batches, https://dora.dev/capabilities/working-in-small-batches/; internal increments preserve the whole approved scope.
- ADAPT: Godot Resources, https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html; JSON-owned content with native engine resources, no duplicate editable canon.
- REJECT: remove all plugins without measurement; force one executor by product name; copy distinctive commercial game expression and assume reskin makes it safe.

Rollback: revert this bounded policy commit through a normal PR; no project runtime or local tool installation is changed.

## Candidate verification and review receipt

- Baseline consumer probe: ordinary approved implementation in capable Work still forced Codex handoff; explicit Work-only override avoided it. This is the default-routing RED observation, not a tool failure.
- Corrected focused suite: 226 tests, zero failures/errors. Generator freshness, Base v9 integrity, Skill coverage and partition manifest validation passed. Initial whole-suite direct invocation was interrupted after long waits in task-created external temporary fixtures; it is not PASS. The repository-owned temporary-session validation run is tracked separately and does not inherit the focused result.
- Independent round 1: six fresh-reader scenarios selected the intended capable/partial/read-only/explicit-handoff/two-round/image-candidate paths. Whole-scope review found two Important corrections (missing TUNE approval-envelope definition; stale map-tail handoff restriction) and one Minor correction (role-named V4 visual route). All three were corrected in their existing owners; engine compatibility wording and omitted claim/continuation router safeguards were also reconciled. Round 2 and exact-head CI remain required before merge.
- Candidate reports are policy/contract evidence only: runtime, Human, plugin A/B savings and multi-project adoption remain NOT_RUN. Generated/released legacy artifacts and unrelated PRs/worktrees are preserved.
- Existing open PRs were searched. Adjacent earlier work (including #831/#829) is unrelated/read-only, not taken over; this branch implements the new 2026-09-16 approved unified-execution decision on completed main.
