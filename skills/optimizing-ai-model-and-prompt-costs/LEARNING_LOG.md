# Optimizing AI Model and Prompt Costs — Learning Log

## 2026-08-19 · P08 cost-surface audit

```yaml
work_ref: "PR #535 historical P08 source; revalidated by current-main takeover PR #551"
baseline: df8ef644d30fc96456da23a5157e5efb61b620bb
finding: >-
  Model/caching cost optimization could be read as applying provider API billing assumptions before distinguishing plan-included usage from separately metered credits/API/SaaS.
change:
  - classify the cost surface before model/price calculations
  - keep GPT_PRO included usage distinct from credits, API, auto top-up, and new paid services
  - block separately metered paths until explicit user approval when Base requires zero incremental cost
  - avoid fictional cache-savings calculations on subscription surfaces that do not expose billing data
reusable_lesson: >-
  Cost optimization must first identify who is actually charging for the execution surface. A paid subscription does not imply approval for every metered add-on or API from the same provider.
evidence:
  - skills/optimizing-ai-model-and-prompt-costs/SKILL.md
  - tests/test_p08_ai_operations_contract.py
  - docs/operations/base-partitions/learning/P08_LEARNING_LOG.md
verification_status: REVALIDATED_FOCUSED_AND_BASE_V9_ON_727ecb15
final_gate_owner: "PR #551 exact-head required CI and post-merge readback"
```
