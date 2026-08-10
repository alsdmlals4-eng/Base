# Source Scan Absorption Plan — 2026-08-10

## Goal

Convert useful external-source findings into the smallest existing Base owner instead of discarding them merely because they do not justify a new rule or Skill.

## Intended changes

1. Strengthen `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` with a PR-check + adversarial-retention + absorption-first disposition ladder and add Adobe Premiere official release notes as a second official NLE source.
2. Strengthen `AI_SKILL_ADOPTION_GUIDE.md` with consumer-surface compatibility and branch-state verification for instructions/prompts/Skills/agents.
3. Strengthen `NARRATIVE_AND_RELATIONSHIP_METHOD.md` with a tool-neutral read-only selection query → post-selection state commit boundary for dynamic narrative systems.
4. Keep new ACTIVE Skill count at zero and do not touch `skills/SKILL_REGISTRY.json` or `[수정제안서]/PROPOSAL_REGISTRY.json`.
5. Validate through the existing periodic-source contract and required repository CI.

## Protected boundaries

- no product/project direction changes;
- no Skill identity/owner/schema changes;
- no workflow write-permission changes;
- no UI/UX rules that overlap Draft PR #247;
- no tool-specific Premiere/Yarn/Copilot behavior promoted to universal hard rules beyond the narrow cross-tool guardrail supported by the evidence.
