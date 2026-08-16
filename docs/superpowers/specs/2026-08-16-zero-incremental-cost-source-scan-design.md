# Zero Incremental Cost Source Scan — Design

**Date:** 2026-08-16
**Approval:** user-approved in the current task

## Goal

Make **zero incremental monetary cost** a Base-wide operating invariant and change Periodic Source Scan so scheduled automation prepares a trustworthy review Queue without invoking metered AI/API services.

## Existing Solution First

Disposition: `ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`.

Reuse:

- `AGENTS.md` for the always-on Base invariant and routing to the existing detailed cost owner.
- `docs/CI_EXECUTION_COST_POLICY.md` as the existing CI execution/cost authority; extend it rather than creating a second budget policy.
- `docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md` for Source Queue ownership and evidence boundaries.
- `.github/workflows/periodic-source-scan-queue.yml` and `tools/run_periodic_source_scan_queue.sh` for the existing scheduler/Issue update path.
- `tools/periodic_source_scan_queue.py` for deterministic due-Source selection and Queue rendering.
- existing ChatGPT sessions for human-directed research/review when that use is already included in the user's existing subscription and does not trigger separate API or credit billing.

Do not add a new ACTIVE Skill, paid provider, local model dependency, daemon, second Source ledger, duplicate Queue, or duplicate cost-policy owner.

## Problem

The previous scheduled Source Queue passed a separately metered model credential into `tools.periodic_source_analysis` and recorded a model-auth blocker when that credential was absent. That active design assumed a separately billed API path even though the user's standing constraint is that Base work must use only methods that create **no additional cost**.

The concurrency improvement from `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` is correct and must remain. Only the metered model-execution part of Source automation is removed.

## Base-wide cost invariant

Introduce the standing token:

```text
ZERO_INCREMENTAL_COST_REQUIRED
```

Meaning:

- Default and approved Base work may use only execution paths that do not create incremental monetary charges for the user.
- Existing subscriptions already owned by the user may be used only when the requested action is included in that subscription and does not silently route through separately metered API, credit, marketplace, runner, storage, or SaaS billing.
- Pay-as-you-go API calls, paid credits, new paid subscriptions, marketplace purchases, paid hosted compute, or other metered services are forbidden unless the user later explicitly changes this standing policy.
- If cost status cannot be established, do not make the live call; return `COST_GATE_BLOCKED` or an equivalent bounded blocked state.
- A free or already-included manual/human review path is preferred over a metered automation path when both satisfy the same goal.

`AGENTS.md` owns the always-on invariant; `docs/CI_EXECUTION_COST_POLICY.md` remains the specialized CI/runner cost owner. This is a budget/authority gate, not a claim that every third-party service will remain free forever. Cost-sensitive external services must be rechecked before enabling a path that could charge money.

## Periodic Source Scan architecture

Replace the active scheduled flow:

```text
Queue selection
→ metered model analysis
→ Evidence mutation
→ PR validation
→ merge
```

with:

```text
GitHub schedule / workflow_dispatch
→ deterministic due-Source selection
→ refresh [Periodic Source Scan Queue] Issue
→ record ZERO_INCREMENTAL_COST_QUEUE_PREP
→ state: AWAITING_CHATGPT_REVIEW
→ stop with no AI/API call and no repository mutation

Later user-directed ChatGPT review
→ original-source web research
→ Candidate Packet / Evidence disposition
→ if a material repository change is justified:
   latest-main branch → normal validation → PR → merge
→ if no material change:
   Queue receipt only; no churn PR
```

## Scheduled automation permissions

The scheduled workflow needs only what Queue preparation actually consumes:

- repository contents: read
- issues: write

It must not require model/provider credentials, repository contents write, pull-request write, Actions dispatch write for downstream validators, or automated merge authority.

No automated Evidence PR is created by the zero-cost Queue preparation run.

## State semantics

New successful preparation state:

```text
AWAITING_CHATGPT_REVIEW
```

Required receipt fields:

```yaml
mode: ZERO_INCREMENTAL_COST_QUEUE_PREP
ai_api_call: NONE
repository_change: NONE
ledger_scan_timestamp_change: NONE
candidate_evidence_claim: NOT_RUN
next_executor: USER_DIRECTED_CHATGPT_REVIEW
```

`AWAITING_CHATGPT_REVIEW` is not `NO_CHANGE` and not a completed Source scan. It proves only that the deterministic Queue was prepared without paid AI/API execution.

The previous model-auth blocked path is removed from the active scheduler because model authentication is no longer a prerequisite for Queue preparation.

## Evidence and ledger boundaries

- Queue preparation does not count as Source research.
- It must not update `last_successful_scan_at` or contribution counters.
- It must not create Candidate Packets, Evidence records, or Source-scan JSON merely to prove activity.
- Actual ChatGPT/web research must still follow the Evidence Method, original-source backtrace, claim ceilings, owner boundaries, stale recheck, security/policy restrictions, and `NO_CHANGE` semantics.

## Concurrency

Keep `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` unchanged for later repository-changing work.

The Queue-preparation workflow itself only updates the Queue Issue, so it does not need a repository changed-path conflict gate. A later Source review that produces a repository diff uses the ordinary latest-main copy-integration and overlap gates.

## Adversarial review

Rejected approaches:

1. **Create a separately metered API key.** Rejected because API/credit billing is an incremental-cost path.
2. **Install a local LLM solely to preserve automation.** Rejected for YAGNI, model/runtime maintenance burden, hardware variability, and quality uncertainty; no current requirement justifies it.
3. **Remove the Source scheduler entirely.** Rejected because deterministic due-Source rotation and Queue visibility are useful and can remain without model cost.
4. **Pretend Queue preparation is a completed scan.** Rejected because that would inflate Evidence and freshness timestamps.
5. **Keep metered model code in the active scheduled path but depend on missing credentials to block it.** Rejected because a later credential addition could silently re-enable incremental billing.
6. **Create another Base cost-policy document.** Rejected because `docs/CI_EXECUTION_COST_POLICY.md` already owns CI execution/cost detail.

## Validation

TDD must require the active workflow/runner to contain `ZERO_INCREMENTAL_COST_QUEUE_PREP` and `AWAITING_CHATGPT_REVIEW`, and to exclude model credentials, metered analysis invocation, automated Source PR creation, downstream validation dispatch, and merge commands.

Existing executed Source contract tests must bind `AGENTS.md` to `ZERO_INCREMENTAL_COST_REQUIRED` / `COST_GATE_BLOCKED` and verify that `docs/CI_EXECUTION_COST_POLICY.md` remains the detailed cost owner. Avoid a new standalone workflow or test surface solely to prove the policy.

Run exact-head Base v9, Evidence Knowledge, and full Game Project OS validation before merge, preserve unresolved review threads = 0, re-read current `main` before merge, and perform a post-merge Queue workflow readback.

## Rollback

Revert this change as one unit. Rollback would restore the prior metered scheduled-analysis architecture, so doing so would also restore the incremental-cost conflict and therefore requires a new user decision before re-enabling that behavior.