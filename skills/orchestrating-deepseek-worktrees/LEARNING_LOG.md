# Orchestrating DeepSeek Worktrees — Learning Log

## 2026-08-25 · External AI optionality must not make implementation ownership optional

```yaml
work_ref: "PR #674 GPT-Codex role split"
finding: >-
  The old P08 contract correctly made external AI and extra executor use optional for planning-only work,
  but the same OPTIONAL_CODEX_EXECUTOR literal became wrong after the user separated GPT planning/review/visual
  from Codex implementation/coding. Reusing that literal for actual product mutation would let GPT or an external
  model become the de facto implementation owner again.
change:
  - keep external AI optional and REVIEW_PENDING
  - keep GPT as planning/review/visual owner
  - when code/data/Scene/Resource/config/test/build/runtime mutation exists, route to CODEX_IMPLEMENTATION_HANDOFF
  - require Codex to rehydrate current GitHub plus relevant Notion canon
  - prohibit Codex image generation/generative editing and route missing visuals through GPT_VISUAL_REQUEST
  - retain worktree isolation, protected-path, current branch/commit, and fail-closed evidence rules
reusable_lesson: >-
  Optionality belongs to optional planning helpers and optional technical preflight, not to an implementation owner
  once the workflow has explicitly separated planning from implementation. Provider/worktree isolation and execution
  ownership are independent dimensions and must be modeled separately.
evidence:
  - docs/GPT_CODEX_WORKFLOW_POLICY.md
  - skills/orchestrating-deepseek-worktrees/SKILL.md
  - docs/handoffs/2026-08-25-gpt-codex-consumer-migration-packet.md
verification_status: PARTIAL_CONSUMER_MIGRATION_PENDING
final_gate_owner: "PR #674 exact-head CI + canonical-reference freshness + GPT final review"
```

## 2026-08-19 · P08 authority and freshness audit

```yaml
work_ref: "PR #535 historical P08 source; revalidated by current-main takeover PR #551"
baseline: df8ef644d30fc96456da23a5157e5efb61b620bb
finding: >-
  External-AI orchestration had a Codex-specific review step even though Base now treats GPT as the primary planner/reviewer and Codex as an optional executor.
change:
  - keep external-AI results REVIEW_PENDING
  - make GPT the default responsible reviewer
  - use Codex only when separate filesystem/runtime/build execution authority is needed
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
