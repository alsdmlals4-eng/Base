# Orchestrating DeepSeek Worktrees — Learning Log

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
