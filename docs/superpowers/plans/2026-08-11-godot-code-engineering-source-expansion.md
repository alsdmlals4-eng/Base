# Godot and Code Engineering Source Expansion Plan

## Goal

Extend periodic external-source discovery so Base continuously covers Godot implementation/proposal/example surfaces and general code-engineering sources without collapsing proposal, example, discovery, professional-practice, and shipped-authority evidence into one tier.

## Existing Solution First

- Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as the source-pool and decision-policy owner.
- Keep `PERIODIC_SOURCE_OPERATIONS_LEDGER.json` as unique-source operational state.
- Reuse `SOURCE_CONTEXT_PACKET`, `ORIGINAL_SOURCE_BACKTRACE`, Existing Owner First, adversarial review, exact-head CI, and source auto-merge gates.
- Do not create a new ACTIVE Skill or coding-policy owner.

## Planned coverage

Add `CODE_ENGINEERING` as a source domain and track these new source families:

- `godot-proposals`
- `godot-demo-projects`
- `godot-asset-library`
- `python-official`
- `github-platform-engineering`
- `git-scm`
- `owasp`
- `google-engineering-practices`

Also expand the existing `godot` source family to include source repository, issues/PRs, changelog, and contributing guidance.

## Evidence boundaries

- Godot proposal status is evidence about a proposal/discussion state, not shipped runtime behavior.
- Official Godot demos are implementation examples tied to engine/version context, not universal project architecture.
- Godot Asset Library is a discovery surface for user-submitted dependencies, not a vetted dependency allowlist; source repository, maintenance, compatibility, permissions, and license still require verification.
- Python/GitHub/Git official docs are authoritative only for their own language/platform/tool behavior.
- OWASP is security guidance/verification reference, not automatic proof that a project is secure or legally compliant.
- Google Engineering Practices is professional practice, not a universal Base hard rule.

## TDD

1. Add a failing regression requiring `CODE_ENGINEERING`, the eight new source IDs, expanded Godot source-repository surface, and explicit authority-limit phrases.
2. Verify RED on the PR head.
3. Update Watchlist and Ledger minimally.
4. Verify GREEN and full relevant CI.
5. Adversarially check duplication, cadence inflation, proposal-as-release mistakes, example-as-architecture mistakes, dependency trust/license mistakes, and vendor/organization practice overgeneralization.
6. Re-read current main, require exact-head CI and zero unresolved review threads, then merge if the existing low-risk gate remains satisfied.

## Automation

After merge, update the existing daily Base source scan and weekly work-improvement review so `CODE_ENGINEERING` participates in due-source scanning and only maps into project/Base recommendations when it changes a real engineering decision.
