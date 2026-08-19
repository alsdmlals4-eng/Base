# GPT-first / Clean Review Workflow Evidence

Date: 2026-08-19
PR: #531
Baseline main: `1dfa0a19180f64934d7893287925554b45db5915`

## User direction

- GPT is the primary owner for planning, research, design, UX/UI/visual planning and review.
- Codex is optional and used only when repository/runtime implementation or large mechanical inspection materially benefits from an executor.
- When UI/UX/visual context materially affects a PoC/demo, candidate/approved visuals are placed in the exact Project Notion surface and read back before implementation-oriented demo testing.
- Current paid plan is `GPT_PRO` only. Notion paid features require a separate user approval after demonstrated need.
- Deprecated Figma/local visual tooling, external HTML work surfaces and Google Sheets are not normal active workspaces; unique material is absorbed once, read back, then the retired surface is removed from active discovery.
- Adversarial review has no fixed numeric loop quota. It repeats until `CLEAN_REVIEW_EXIT`.
- L1+ completion reports explain important rules, skills/modes, modules, before/after effects, tradeoffs, verification and revisit conditions for user learning.

## TDD / migration evidence

Initial temporary migration run `32208848514`:
- exact policy migration: SUCCESS
- focused contracts: FAILURE
- failure reason: old regression still required `FULL_LOOP_COUNT_MINIMUM: 5`

This was the intended RED signal: the new clean-exit policy exposed a stale numeric regression contract.

Follow-up temporary migration run `32208916516`:
- exact policy migration: SUCCESS
- fixed-loop regression replacement: SUCCESS
- focused contracts: SUCCESS
  - `tests.test_base_long_horizon_work_contract`
  - `tests.test_gpt_codex_workflow_contract`
- final push step encountered a concurrent branch-head race, but the durable migration commit was subsequently present as `9fd15b0d198a603717c1b471835d5a4748616740`.

A later adversarial pass found stale active language for Sheets/HTML in lower policy/Skill surfaces. A second one-shot reconciliation corrected these to migration-only/retired semantics and retained destination-readback requirements.

## Durable policy outcomes

- `AGENTS.md`: `ADVERSARIAL_REVIEW_UNTIL_CLEAN`, `CLEAN_REVIEW_EXIT`, user-learning completion report.
- `docs/GPT_CODEX_WORKFLOW_POLICY.md`: `GPT_FIRST_PLANNING_AND_REVIEW`, `OPTIONAL_CODEX_EXECUTOR`, one-copy/paste PowerShell handoff only when Codex is actually useful.
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`: GPT-first lifecycle, visualized-PoC gate, legacy absorb/verify/remove, paid-plan gate, clean-review termination.
- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`: visualized PoC/demo readiness before runtime testing when visual context is material.
- `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`: `MIGRATION_ONLY_UNTIL_REMOVAL`.
- `skills/running-adversarial-review-and-refinement/SKILL.md`: fixed loop count removed; review repeats until clean exit; stale Sheet comparison language moved to Notion/repository sync.

## Evidence ceiling / remaining cleanup

This PR changes active policy and regression contracts. It does **not** by itself prove that every historical/archive file or every deprecated custom local-tool implementation payload has been physically deleted. Destructive cleanup must first prove that unique reusable behavior/data has been absorbed and active consumers are zero. Until that audit is completed, those remnants are `RETIREMENT_CLEANUP_PENDING`, not active authority.

Do not claim Notion payment, runtime implementation, project PoC integration, or deprecated payload deletion unless separately executed and read back.
