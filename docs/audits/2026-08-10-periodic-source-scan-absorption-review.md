# 2026-08-10 Periodic Source Scan — Absorption Review

Status: `PR_GATED_AUDIT_RECORD`

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

`NO_CHANGE` is valid only when no rule/BCP candidate, existing-owner absorption, evidence/reference retention, test/adversarial scenario, source-coverage improvement, stale/freshness correction, or bounded incremental improvement is useful.

## PR check

- scan baseline: Base main `0bb1da2553737b15bfe2a22b4ef93ecb9db79dde`
- same-goal periodic-source implementation PR: none open at scan start
- overlapping Draft PR #247: UI/UX/accessibility; those findings were deferred instead of duplicated
- dependency PRs: outside this scan goal
- recently merged PR #250 remains the canonical Watchlist implementation and owner structure
- during implementation main advanced to `39eaea7b5bc5687970698c069d50823b73399954`; the branch was explicitly synchronized before the final validation cycle

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

### Incremental improvement retention

User direction clarified that future scans should continue improving Base even when a new Skill or owner change is not justified. The Watchlist therefore adds an `INCREMENTAL_IMPROVEMENT` layer for bounded test, adversarial-question, reference/source coverage, stale/freshness, checklist/template/evidence-field, and small validation-contract improvements.

Disposition:

`USER_APPROVED_BASE_BEHAVIOR_CLARIFICATION → LOW_RISK_BOUNDED_UPDATE`

Guardrail: do not create meaningless churn, duplicate rules, or file-count inflation merely to avoid `NO_CHANGE`.

### PR-gated Base mutation

The latest user direction also requires actual Base changes discovered by a scan to pass through PR review rather than treating low-risk authority as permission for direct `main` writes.

Disposition:

`USER_APPROVED_BASE_BEHAVIOR_CLARIFICATION → LOW_RISK_BOUNDED_UPDATE`

Applied to the Watchlist as `branch → PR → adversarial review → related CI/exact-head validation → merge gate`, while preserving the existing BCP/user-decision boundaries for higher-risk changes.

## Rejected or deferred

- Hada rewrite-all-code claim: `CONFLICT / AVOID`
- UI/UX/accessibility findings overlapping Draft PR #247: `DEFER_OPEN_PR`
- new ACTIVE Skill: `NOT_JUSTIFIED`
- new Skill owner/behavior schema/Proposal Registry entry: `NOT_NEEDED`

## TDD evidence

First RED was observed on Draft PR #255, exact branch head `8f33a8e8e6429a3f40c2422d2f9a6f8e1a717938`:

- `Validate Evidence-Based Game Development Knowledge` run `31365123081`: `FAILURE`
- focused contract produced exactly three intended failures:
  - missing `Adobe Premiere official release notes`
  - missing `consumer surface` / branch-state validation
  - missing `SELECTION_QUERY_READ_ONLY`

A second RED was observed for the incremental-improvement clarification, exact branch head `b64049f0956070674e1cf324056c2866271ca894`:

- `Validate Evidence-Based Game Development Knowledge` run `31365726190`: `FAILURE`
- the focused suite had one intended failure: missing `INCREMENTAL_IMPROVEMENT`
- the prior three focused findings were already GREEN at that head

A third RED was observed for the PR-gated mutation clarification, exact branch head `ce9da6680af8c91bd6401d6ce73c3a3d5e6b2905`:

- `Validate Evidence-Based Game Development Knowledge` run `31366214247`: `FAILURE`
- the focused suite had one intended failure: missing `실제 Base 변경은 별도 PR`
- the other 59 tests in that suite passed at that head

Production owner changes were applied only after their corresponding RED evidence.

## Adversarial review

Findings handled:

1. **Over-conservative discard bias:** `NO_CHANGE` was being treated too close to `NO_NEW_RULE`. Fixed with absorption-first retention semantics.
2. **File-count inflation:** the RED/evidence process temporarily created many tiny audit files. This violated consolidation-first. They were removed and consolidated into this single audit record.
3. **Vendor/tool overgeneralization:** Copilot, Yarn, and Premiere behavior is kept within exact product/tool scope; only narrow tool-neutral guardrails are absorbed.
4. **Open PR duplication:** UI/UX findings remain deferred to PR #247.
5. **New-Skill bias:** new ACTIVE Skill count remains zero.
6. **Forced-change bias:** incremental improvement is required as a search/retention lens, not as a quota. Meaningless churn remains prohibited.
7. **Self-staling audit status:** this audit no longer claims a future exact-head validation result. The PR/CI and eventual merge result own that evidence.
8. **Direct-main ambiguity:** low-risk absorption authority could otherwise be misread as permission to mutate `main` directly. The Watchlist now requires a PR path for actual Base changes.
9. **Plan/spec drift:** late incremental-improvement and PR-gate instructions were synchronized back into both the implementation plan and design spec before final validation.

## Protected boundaries

- `skills/SKILL_REGISTRY.json`: unchanged
- `[수정제안서]/PROPOSAL_REGISTRY.json`: unchanged
- ACTIVE Skill count: unchanged
- workflow write permissions: unchanged
- product/game/fiction/channel direction: unchanged
- no tool-specific syntax/API promoted to Base-wide hard rule

## Validation ownership

This document records RED evidence, design decisions, and adversarial findings. It does **not** self-certify the latest branch head or future merge. The authoritative GREEN/FAIL result is the exact-head GitHub PR CI plus the latest-main/open-PR race check performed immediately before merge. Unrun checks must not be reported as PASS.
