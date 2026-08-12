# Project Adapter Finalization Evidence

## Artifact identities

Initial extraction artifact:

```text
PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.6.md
SHA256: 6875473193259cfb126cc5d8b9e682decb7c47d57fdadda510e0e34c182e65a7
```

Final reviewed project artifact:

```text
PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.6.md
SHA256: 2482e1d86514e1089dc58cd6db21f80bee125555e7e9c08b02c480105fa5da32
lines: 3270
bytes: 96886
code_fences_even: true
required_contract_tokens_missing: []
```

The proposal registry retains the initial extraction identity. This file records the later project-specific review correction.

## Adversarial correction

The initial v4.6 draft had a planning-stage `DRAFT_VISUAL` exception. Re-reading the project instruction showed a stricter required order:

```text
기획 완료
→ 검수 완료
→ 이미지/인게임아트/PPT/UI component visual production
→ Codex
```

The final project adapter therefore uses:

```text
DISABLED_UNTIL_FINAL_REVIEW_COMPLETE_UNLESS_USER_EXPLICITLY_CHANGES_SEQUENCE
```

Before `FINAL_REVIEW_COMPLETE`, the project may inspect existing approved references/assets and prepare text specifications, but it does not start new project image generation. Any future sequence change requires a new explicit user decision and canon update.

## Base generalization boundary

The BCP keeps conditional planning-visual handling only as a Base-wide proposal candidate because other projects may have different needs. That candidate is not the current project's policy and is not approved for active Base implementation by this proposal.

A later implementation review can decide whether generic Base should keep a project-selected draft-visual mode, omit it, or route it through an existing visual owner.
