# Orchestrating DeepSeek Worktrees — Learning Log

## 2026-08-25 · Correction — code format is not Codex ownership

```yaml
work_ref: "PR #674 GPT-Codex role split correction"
status: CURRENT_CORRECTION
finding: >-
  The first 2026-08-25 role migration over-broadened Codex ownership from actual game implementation
  to generic repository code/data/tests/Registry/generated/CI. That was incorrect. A Base Python test or
  generated checker is code-shaped but remains Base governance work owned by GPT.
change:
  - external AI remains optional and REVIEW_PENDING
  - GPT owns Base, Notion, planning, documents, tables, visuals, Registry/generated/CI/test-contract maintenance
  - Codex owns only actual game-project Godot product implementation: GDScript, Scene/Resource/runtime wiring,
    build/export, and implementation/runtime/play tests
  - if external-AI output affects Base/non-product work, GPT applies and validates it
  - if it produces an actual Godot implementation task, create a project-specific Codex Godot handoff
  - Codex rehydrates that game project's GitHub + Notion before product mutation
  - Codex image generation/editing remains forbidden; missing visual = GPT_VISUAL_REQUEST
reusable_lesson: >-
  Execution ownership follows product responsibility, not file extension or the existence of code.
  External-AI optionality, Base maintenance ownership, and Godot product implementation ownership are
  separate dimensions and must not be collapsed into one generic executor rule.
evidence:
  - docs/GPT_CODEX_WORKFLOW_POLICY.md
  - docs/WORK_MODE_AND_SKILL_ROUTING.md
  - skills/orchestrating-deepseek-worktrees/SKILL.md
  - templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md
verification_status: PENDING_EXACT_HEAD_BASE_VALIDATION
final_gate_owner: "PR #674 GPT Base maintenance + exact-head CI + final adversarial review"
```

## 2026-08-25 · SUPERSEDED INTERIM — External AI optionality must not make implementation ownership optional

이 기록은 같은 날의 중간 설계다. `code/data/... mutation이면 Codex`라는 범위가 너무 넓었으며 위 CURRENT_CORRECTION이 대체한다. 역사적 finding 과정만 보존한다.

```yaml
work_ref: "PR #674 GPT-Codex role split — superseded interim"
finding: >-
  The old P08 contract mixed external-AI optionality and executor ownership.
interim_change:
  - external AI optional and REVIEW_PENDING
  - generic implementation was temporarily routed to Codex
superseded_reason: >-
  Generic Base/repository maintenance is not Codex work. Only actual game-project Godot product implementation is.
verification_status: SUPERSEDED
```

## 2026-08-19 · P08 authority and freshness audit

```yaml
work_ref: "PR #535 historical P08 source; revalidated by current-main takeover PR #551"
baseline: df8ef644d30fc96456da23a5157e5efb61b620bb
finding: >-
  External-AI orchestration had a Codex-specific review step even though Base then treated GPT as the primary planner/reviewer and Codex as an optional executor.
change:
  - keep external-AI results REVIEW_PENDING
  - make GPT the default responsible reviewer
  - use execution workers only when then-current scope required them
  - re-read current AGENTS.md, canon, exact branch/commit, protected paths, and tests immediately before executor work
reusable_lesson: >-
  A handoff package is not current canon. External executors must rehydrate authority and exact repository state at execution time, and provider-specific naming must not silently create provider-specific authority.
evidence:
  - skills/orchestrating-deepseek-worktrees/SKILL.md
  - tests/test_p08_ai_operations_contract.py
  - docs/operations/base-partitions/learning/P08_LEARNING_LOG.md
verification_status: REVALIDATED_FOCUSED_AND_BASE_V9_ON_727ecb15
final_gate_owner: "PR #551 exact-head required CI and post-merge readback"
```
