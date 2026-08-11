# Post-Change Adversarial Monitor Loop — Design

**Date:** 2026-08-11
**Base baseline:** `7ce96181d0a97930300fcc6d383dacc75ad08f6a`

## Goal

Make adversarial review and same-goal PR/recent-merge rechecks an explicit completion condition after every retained Base/project change, so omissions, conflicts, stale consumers, duplicate work, and follow-up gaps are caught before completion and again after merge.

## Existing Solution First

Disposition: `ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`.

Reuse:

- `skills/running-adversarial-review-and-refinement/SKILL.md` as the review owner.
- `docs/OPERATING_MODEL.md` as the lifecycle owner.
- existing `reviewing-and-validating-project-changes` for actual diff/CI/runtime evidence.
- existing canonical-reference freshness and repository-wide audit contracts for untouched consumers and derivative drift.
- existing PR / exact-head / post-merge gates; no new ACTIVE Skill, agent, workflow permission, Ruleset, or repository setting.

## Problem

The adversarial Skill already supports `regression-recheck`, `post-merge-review`, same-goal PR checks, untouched-consumer attacks, and post-merge comparison. However the operating lifecycle does not state one compact mandatory post-change monitoring loop as a completion invariant. This leaves room for an otherwise valid change to be reported complete after local validation while a concurrent/recent PR, untouched consumer, post-merge drift, or complementary follow-up is missed.

## Design

Add a named `POST_CHANGE_MONITOR_LOOP` owned by the existing adversarial Skill.

```text
retained-change-or-merge
→ attack
→ validate-critique
→ same-goal-open-and-recent-pr-recheck
→ untouched-consumer-and-derivative-recheck
→ omission-conflict-complement-gap-classification
→ approved-minimal-fix-if-needed
→ regression-recheck
→ exact-head-validation
→ merge-or-post-merge-main-readback
→ post-merge-pr-and-canon-recheck
→ completion-report
```

The loop classifies findings as:

- `OMISSION`: a required owner/consumer/test/template/derivative was not updated.
- `CONFLICT`: current canon, approved decision, actual diff, open/recent PR, or merged result disagree.
- `COMPLEMENT_GAP`: the change is correct but a small adjacent test/reference/checklist/freshness/consumer improvement is materially needed to make the change durable.
- `DUPLICATE_WORK`: another open/recent PR already owns the same goal.
- `NO_MATERIAL_FOLLOWUP`: no additional repository change is justified.

## Boundaries

- This is not an infinite synchronous loop and does not imply background execution by Base itself.
- No change is created merely to satisfy the loop; `NO_MATERIAL_FOLLOWUP` is valid.
- Existing Solution First still applies; complementary findings are absorbed into existing owners before proposing new files or Skills.
- User-decision, protected-policy, security/permission/license, product-direction, and other protected changes remain blocked behind existing approval gates.
- Unrun CI/runtime/Sheets/human validation remains `NOT_RUN` / `BLOCKED_UNVERIFIED`.
- A PR check is required both before merge/completion and after merge when the repository state can have changed.

## Expected surfaces

- `skills/running-adversarial-review-and-refinement/SKILL.md`
- `docs/OPERATING_MODEL.md`
- `skills/SKILL_LEARNING_LOG.md`
- `tests/test_neutral_adversarial_feature_lifecycle.py`

No Registry identity change is expected.

## Validation

TDD RED first. The focused test must require the named loop, PR recheck, omission/conflict/complement classification, untouched-consumer recheck, exact-head validation, post-merge main readback, and a no-churn terminal state. Then run repository CI and exact-head validation before merge.