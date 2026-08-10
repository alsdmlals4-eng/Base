# Source Scan Absorption Plan — 2026-08-10

## Goal

Convert useful external-source findings into the smallest existing Base owner instead of discarding them merely because they do not justify a new rule or Skill. When no new Skill/owner change is justified, still look for bounded incremental improvements that reduce ambiguity, stale references, regression risk, or evidence gaps without creating meaningless churn.

## Intended changes

1. Strengthen `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` with a PR-check + adversarial-retention + absorption-first disposition ladder and add Adobe Premiere official release notes as a second official NLE source.
2. Add `INCREMENTAL_IMPROVEMENT` so tests, counterexamples, adversarial questions, source coverage, freshness/path corrections, checklist/template/evidence fields, and small validation contracts remain valid improvement outcomes even without a new Skill.
3. Require actual Base changes from a source scan to use `branch → PR → adversarial review → related CI/exact-head validation → merge gate`; do not write directly to `main` from scan findings.
4. Strengthen `AI_SKILL_ADOPTION_GUIDE.md` with consumer-surface compatibility and branch-state verification for instructions/prompts/Skills/agents.
5. Strengthen `NARRATIVE_AND_RELATIONSHIP_METHOD.md` with a tool-neutral read-only selection query → post-selection state commit boundary for dynamic narrative systems.
6. Keep new ACTIVE Skill count at zero and do not touch `skills/SKILL_REGISTRY.json` or `[수정제안서]/PROPOSAL_REGISTRY.json` unless a genuinely independent responsibility/authority boundary is found and approved through the existing governance.
7. Validate through the existing periodic-source contract and required repository CI.

## Protected boundaries

- no product/project direction changes;
- no Skill identity/owner/schema changes in this bounded patch;
- no workflow write-permission changes;
- no UI/UX rules that overlap Draft PR #247;
- no tool-specific Premiere/Yarn/Copilot behavior promoted to universal hard rules beyond the narrow cross-tool guardrail supported by the evidence;
- no forced edits solely to avoid `NO_CHANGE`.
