# External Operator Case Reconstruction Design

**Date:** 2026-09-08
**Status:** USER-APPROVED / IMPLEMENTING
**Baseline:** Base `68792fc38340a19945ba6b15eedef39f55d50705`
**Approval:** Current user message `진행해`, following the requested analysis of stronger users' GPT-6 Astra workflows.

## Goal

Make an external user/operator case useful as bounded evidence when it changes a Base or project workflow, tool, Skill, evaluation, QA, or content-pipeline decision. The record must expose the supplied input anchor, observed stages and handoffs, human gate, evidence ceiling, non-transferable conditions, and one smallest project trial with an acceptance gate.

## Existing owners retained

- `docs/BENCHMARKING_REFERENCE_GUIDE.md` continues to own source priority, pattern extraction, and project-fit decisions.
- `templates/KNOWLEDGE_CASE_STUDY.md` continues to own reusable case-study analysis.
- `skills/optimizing-ai-model-and-prompt-costs/references/model-stack-routing.md` continues to own execution strategy, actual observations, and failure routing.
- `benchmark_preflight_receipt.entries` remains the one machine-checked decision record. No external-case registry, agent framework, paid service, or new shared status taxonomy is introduced.

## Decision

Add an optional `operator_case_reconstruction` object to a benchmark receipt entry. It is required by policy only when an external operator case is used to alter a `WORKFLOW_PATTERN`, `TOOL_PATTERN`, `SKILL_PATTERN`, evaluation, QA, or content-pipeline decision. The object has six nonempty narrative fields:

```text
input_anchor_and_source
staged_execution_and_handoffs
human_decision_and_approval_boundary
observable_outcome_and_evidence_ceiling
nontransferable_or_unobserved
project_trial_and_acceptance_gate
```

The validator checks the object shape when present; it cannot establish that a public claim, a metric, or a tool result is true. Direct-source access remains preferred. If the original material is unavailable, the record must state that limitation and must not promote the claim into runtime, productivity, or project-adoption proof.

## Evidence used for this decision

- OpenAI's Playco case describes a reusable sequence: unthemed greybox prototype, play/test/validate, then themed variants. It reports fewer manual fixes but is first-party reported evidence, not independent reproduction: <https://openai.com/index/playco-game-prototyping-with-astra/>.
- The GPT-6 Astra discovery cards identify potentially useful examples but label many entries self-reported or unverified; they are discovery anchors, not outcome proof: <https://cheerselfai.com/en/usecase/gpt-6-astra>.
- OpenAI's Legora case records each check and keeps the human as final decision-maker, supporting an evidence ledger and human gate rather than unattended execution: <https://openai.com/index/legora-financial-statement-review-with-astra/>.

## Rejected alternatives

| Alternative | Decision | Reason |
|---|---|---|
| New external-case database or dedicated Skill | REJECT | Duplicates the existing case-study, benchmark, execution-strategy, and receipt owners. |
| Require the six-field reconstruction for every benchmark | REJECT | Burdens ordinary repository/reference comparisons that do not rely on an external operator's workflow. |
| Accept one-prompt demos or vendor claims as automatic adoption proof | REJECT | A public card can establish neither reproducible outcome nor fit for a specific project. |
| Remove approval gates based on a short agent-allocation anecdote | REJECT | The case is contextual, unverified for this Base, and conflicts with the existing human approval boundary. |

## Scope and safeguards

- No new runtime code, dependencies, external service, agent, project database, or paid tool.
- No claim that the validator independently verifies sources or productivity outcomes.
- Existing entries without an operator reconstruction remain valid.
- A reconstruction must include an explicit project trial and acceptance gate; it does not itself authorize broad adoption.
- Rollback is one revert of this branch's commit; no historical or project data is deleted.
