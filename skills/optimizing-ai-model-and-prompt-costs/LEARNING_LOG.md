# Optimizing AI Model and Prompt Costs — Learning Log

## 2026-09-07 · Selective execution-pattern reference

- Approved scope: user accepted existing-Skill extension after HydraFusion comparison; no provider installation, paid path, model switch or runner.
- Baseline: `1072e201900e3aa4a403330d4132c737fc86142a`. Separate-context reader applied three hypothetical tasks before edits: model/effort and cost gates were found, but execution-pattern/role/failure record slots were absent; single-model exclusion prevented treating the Skill as a universal workflow router.
- Reusable correction: retain Registry activation boundaries; extend existing reference and map its advisory output to the existing report. Single-model tasks reuse the reference through their existing owner, not a fictional cost-Skill activation.
- Failure lesson: distinguish output defects from missing environment, missing authority and unknown external effects before escalation; reuse current recovery/verification owners.
- Knowledge state: bounded reference application observed; a fresh candidate reader on `e0442512d8cce49bec5fc44a02c2c9547e708b0f` applied the same three tasks and four variations with explicit source support for the previously missing route/failure/record boundaries. These were instructed retrieval/application samples, not blind activation or statistical efficacy. Final evidence belongs to `docs/superpowers/plans/2026-09-07-execution-pattern-routing.md` and its current-task PR. No production efficacy, savings, automatic activation, cross-family model comparison or game runtime claim.
- Regression finding: existing freshness policy rejected the first candidate because a Skill companion test was absent. The P08 test now parses the real Markdown navigation graph and resolves local owner paths/anchors; baseline report routing fails, candidate navigation passes. This structural test is not reported as agent compliance.
- Source: [GitHub HydraFusion announcement](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/), read 2026-09-07. Adapt workflow reasoning; reject package adoption and vendor results as local measurements.
- Rollback: revert only this task's additions to Skill, reference, report template, learning, P08 navigation test, plan and start receipt together; preserve existing and later work.

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
