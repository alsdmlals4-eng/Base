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

A later adversarial pass found stale active language for Sheets/HTML in lower policy/Skill surfaces. The reconciliation changed active long-horizon terms to `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` and `EXTERNAL_HTML_WORKSPACE_RETIRED`, migrated post-merge review wording to Notion/repository sync, and retained destination-readback requirements.

Canonical-reference freshness then correctly required two companion updates:
- the adversarial Skill change required its Learning Log to record why the fixed numeric loop was superseded;
- the Sheets policy change required an active BCA/Sheets regression test to require migration-only removal semantics.

Both companions were added. A final active-Skill audit also found and removed the last `Sheets evidence` wording from `BLOCKED_UNVERIFIED`, replacing it with `Notion readback/sync evidence`.

## Durable policy outcomes

- `AGENTS.md`: `ADVERSARIAL_REVIEW_UNTIL_CLEAN`, `CLEAN_REVIEW_EXIT`, user-learning completion report.
- `docs/GPT_CODEX_WORKFLOW_POLICY.md`: `GPT_FIRST_PLANNING_AND_REVIEW`, `OPTIONAL_CODEX_EXECUTOR`, one-copy/paste PowerShell handoff only when Codex is actually useful.
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`: GPT-first lifecycle, visualized-PoC gate, legacy absorb/verify/remove, paid-plan gate, clean-review termination, Sheets migration-only removal, HTML workspace retired.
- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`: visualized PoC/demo readiness before runtime testing when visual context is material.
- `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`: `MIGRATION_ONLY_UNTIL_REMOVAL`.
- `skills/running-adversarial-review-and-refinement/SKILL.md`: fixed loop count removed; review repeats until clean exit; active sync/readback language uses Notion/repository authority.
- `skills/running-adversarial-review-and-refinement/LEARNING_LOG.md`: records the fixed-quota → clean-exit supersession and preserves the older five-loop decision only as historical evidence.
- `tests/test_base_long_horizon_work_contract.py`, `tests/test_bca_visual_sheet_workflow.py`, `tests/test_gpt_codex_workflow_contract.py`: enforce the new durable contracts.

## Verification evidence before latest exact-head re-run

Observed Green evidence during this PR:
- focused clean-review / GPT-Codex contract run `32208916516`.
- exact-head `4349a0f2a8da8b75f1d08b6aed55669c432ca4ba`:
  - Validate Game UX UI System: SUCCESS
  - Validate Skill Routing Precision: SUCCESS
  - Validate One-Shot Local Executor Bootstrap: SUCCESS
  - Validate Base Long-Horizon Work Contract: SUCCESS
- Integrated Vertical Slice functional test suite itself ran 38 tests successfully; its run failed only at canonical-reference freshness before the required companion updates above.

A newer exact-head CI run is required after this evidence commit. Do not infer its outcome from earlier Green runs.

## Evidence ceiling / remaining cleanup

This PR changes active policy and regression contracts. It does **not** by itself prove that every historical/archive file or every deprecated custom local-tool implementation payload has been physically deleted. Destructive cleanup must first prove that unique reusable behavior/data has been absorbed and active consumers are zero. Until that audit is completed, those remnants are `RETIREMENT_CLEANUP_PENDING`, not active authority.

Do not claim Notion payment, runtime implementation, project PoC integration, or deprecated payload deletion unless separately executed and read back.
