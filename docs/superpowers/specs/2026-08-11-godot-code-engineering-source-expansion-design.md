# Godot and Code Engineering Source Expansion Design

## Decision

Extend the existing periodic external-source system instead of creating a new coding research Skill. The missing capability is source coverage, not a new execution owner.

## Source model

`CODE_ENGINEERING` is cross-project evidence coverage for implementation quality, testing, versioning, security, CI, review, and tool behavior. Godot-specific coding sources may belong to both `GAME_DEVELOPMENT` and `CODE_ENGINEERING`.

### Godot

- Existing `godot`: docs/blog/releases plus source repository, issues/PRs, changelog, and contributor guidance.
- `godot-proposals`: official improvement proposals. `AUTHORITY_TARGET` only for proposal/discussion state; proposal != shipped behavior.
- `godot-demo-projects`: official demos/examples. `AUTHORITY_TARGET` for example compatibility/usage at the matching engine context; example != universal architecture.
- `godot-asset-library`: official discovery index of user-submitted addons/scripts/tools. `DISCOVERY_FEED`; each dependency requires source/license/maintenance/compatibility/permission verification.

### Code engineering

- `python-official`: Python docs, What's New, PEPs, unittest, typing, deprecations.
- `github-platform-engineering`: GitHub Actions, secure-use guidance, dependency review, CodeQL/code scanning, Rulesets and related platform docs.
- `git-scm`: Git official documentation for worktree, bisect, rebase/merge, hooks and repository operations.
- `owasp`: OWASP Cheat Sheet Series / ASVS, including secure coding, CI/CD, supply-chain and AI-assisted coding security guidance.
- `google-engineering-practices`: public Google code-review/change-author guidance as `PROFESSIONAL_PRACTICE`, not universal policy.

## Cadence

- `daily-or-weekly`: existing `godot`, `github-platform-engineering`
- `weekly`: `godot-proposals`, `python-official`, `owasp`
- `monthly-or-on-demand`: `godot-demo-projects`, `godot-asset-library`, `git-scm`
- `quarterly-or-when-relevant`: `google-engineering-practices`

Cadence is a scan default, not evidence strength.

## Guardrails

When a coding source is retained, `SOURCE_CONTEXT_PACKET` must preserve exact version/runtime/tool scope. A proposal, draft PEP, open issue, PR, demo, blog post, or vendor/community addon does not prove shipped runtime behavior. Security guidance does not prove compliance. Professional code-review practice is adapted only when it improves the current repository decision.

## Validation

The existing periodic-source regression will require the new domain/source IDs and explicit evidence boundaries. No workflow permission, ACTIVE Skill identity, Ruleset, or approval semantics change is required.
