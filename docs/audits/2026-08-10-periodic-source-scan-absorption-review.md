# 2026-08-10 Periodic Source Scan — Absorption Review

Status: `IMPLEMENTED_ON_BRANCH / VALIDATION_PENDING`

## Scope and governing rule

This scan corrects an over-narrow `NO_CHANGE` interpretation.

A periodic source scan must use:

```text
latest main
→ same-goal open/recent PR check
→ Existing Solution First / consolidation-first
→ original-source verification
→ adversarial review
→ retain useful outcomes at the smallest existing owner
→ new rule/BCP only for genuinely new responsibility or authority boundaries
```

`ALREADY_COVERED` and `PARTIAL` do not mean discard. A candidate can still become `ABSORB_EXISTING_OWNER`, `EVIDENCE_ONLY_UPDATE`, `REFERENCE_ONLY`, or `LOW_RISK_BOUNDED_UPDATE` when it materially improves an existing trigger, condition, failure state, evidence boundary, source cross-check, adversarial question, or regression scenario.

`NO_CHANGE` is valid only when no rule/BCP candidate, existing-owner absorption, evidence/reference retention, test/adversarial scenario, source-coverage improvement, or stale/freshness correction is useful.

## PR check

- scan baseline: Base main `0bb1da2553737b15bfe2a22b4ef93ecb9db79dde`
- same-goal periodic-source implementation PR: none open at scan start
- overlapping Draft PR #247: UI/UX/accessibility; those findings were deferred instead of duplicated
- dependency PRs: outside this scan goal
- recently merged PR #250 remains the canonical Watchlist implementation and owner structure

## Primary evidence and disposition

### GitHub Copilot customization surfaces

Current GitHub official documentation distinguishes support for repository-wide instructions, path-specific instructions, agent instructions, prompt files, Skills, and agents across GitHub.com, IDE, CLI, cloud-agent, and code-review consumer surfaces. Current docs also show that branch semantics can matter for PR review and may differ across documentation/surfaces.

Disposition:

`ALREADY_COVERED → ADAPT → ABSORB_EXISTING_OWNER`

Applied to `docs/AI_SKILL_ADOPTION_GUIDE.md` as a consumer-surface, current-support-matrix, preview-status, branch/ref, and harness/configuration validation guardrail. No new Skill.

### Yarn Spinner saliency

Yarn Spinner's current official saliency documentation separates a read-only content query from the later notification that content was actually selected. A queried candidate is not guaranteed to run.

Disposition:

`PARTIAL → ADAPT → LOW_RISK_BOUNDED_UPDATE`

Applied to `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` as a tool-neutral `SELECTION_QUERY_READ_ONLY → STATE_COMMIT_AFTER_SELECTION` boundary. It is limited to dynamic game narrative and is not imposed on linear fiction.

### Adobe Premiere official release notes

Adobe maintains a recurring official Premiere release-notes surface covering feature, bug-fix, security, timeline, media-management, audio, and export changes.

Disposition:

`PARTIAL → REFERENCE_ONLY → LOW_RISK_BOUNDED_UPDATE`

Added to the Watchlist beside DaVinci as a second official NLE change surface. Premiere-specific features are explicitly not universal editing rules.

## Rejected or deferred

- Hada rewrite-all-code claim: `CONFLICT / AVOID`
- UI/UX/accessibility findings overlapping Draft PR #247: `DEFER_OPEN_PR`
- new ACTIVE Skill: `NOT_JUSTIFIED`
- new Skill owner/behavior schema/Proposal Registry entry: `NOT_NEEDED`

## TDD evidence

RED was observed on Draft PR #255, exact branch head `8f33a8e8e6429a3f40c2422d2f9a6f8e1a717938`:

- `Validate Evidence-Based Game Development Knowledge` run `31365123081`: `FAILURE`
- focused contract produced exactly three intended failures:
  - missing `Adobe Premiere official release notes`
  - missing `consumer surface` / branch-state validation
  - missing `SELECTION_QUERY_READ_ONLY`

Production owner changes were applied only after this RED evidence.

## Adversarial review

Findings handled:

1. **Over-conservative discard bias:** `NO_CHANGE` was being treated too close to `NO_NEW_RULE`. Fixed with absorption-first retention semantics.
2. **File-count inflation:** the RED/evidence process temporarily created many tiny audit files. This violated consolidation-first. They were removed and consolidated into this single audit record.
3. **Vendor/tool overgeneralization:** Copilot, Yarn, and Premiere behavior is kept within exact product/tool scope; only narrow tool-neutral guardrails are absorbed.
4. **Open PR duplication:** UI/UX findings remain deferred to PR #247.
5. **New-Skill bias:** new ACTIVE Skill count remains zero.

## Protected boundaries

- `skills/SKILL_REGISTRY.json`: unchanged
- `[수정제안서]/PROPOSAL_REGISTRY.json`: unchanged
- ACTIVE Skill count: unchanged
- workflow write permissions: unchanged
- product/game/fiction/channel direction: unchanged
- no tool-specific syntax/API promoted to Base-wide hard rule

## Validation

Final exact-head CI and latest-main race check must be green before merge. Until then the result is `IMPLEMENTED_ON_BRANCH / VALIDATION_PENDING`.
