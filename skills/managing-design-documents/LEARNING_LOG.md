# Managing Design Documents — Learning Log

## 2026-08-10 — BCP-011 game feature design spec hierarchy

### Observation

Base already separated concept/PoC ownership, canonical design-document ownership, and post-approval traceability, but a reusable gap remained between a feature surviving PoC and multiple disciplines being able to implement the same intended behavior.

### Decision

Absorb the gap into existing owners instead of adding a new ACTIVE Skill.

```text
analyzing-and-refining-game-concepts
→ benchmark / PoC / adversarial review
→ promote only surviving major L2 features

managing-design-documents
→ canonical GAME_FEATURE_DESIGN_SPEC authoring

FEATURE_SPEC_TRACEABILITY_PACKET
→ post-approval Task / implementation / verification linkage
```

### Added contract

- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` owns intended player-facing behavior, rules, states, feedback, edge cases, data/balance, dependencies, acceptance, telemetry/playtest plan, and cut-down/rollback.
- The feature spec does **not** own Task progress, implementation completion, PR state, or executed verification results.
- Specialized design contracts remain authoritative where they are more precise; the generic feature spec references/composes them.
- L0/L1 and pre-PoC ideas do not receive mandatory L2 detail.
- Google Sheets remains a summary/workspace and does not duplicate the detailed canonical source.

### Rejected alternatives

- New broad `game-feature-design` ACTIVE Skill.
- Monolithic MASTER_GDD.
- Mandatory detailed spec for every feature or idea.
- Expanding Traceability Packet into a second detailed canonical source.
- Copying the full detailed spec into Google Sheets.

### Evidence and limits

- Industry evidence was recorded in `BCP-2026-011` from GDC one-page/layered design documentation, Ubisoft production-stage separation, and contemporary GDD communication practice.
- TDD RED was observed on the exact implementation PR head before production changes: the CI-executed regression failed specifically because `GAME_FEATURE_DESIGN_SPEC.md` was missing.
- GREEN repository CI must be re-run on the exact final implementation head.
- Real-project pilot: `NOT_RUN`.
- Human usability/comprehension: `HUMAN_NOT_RUN`.
- Gameplay quality improvement caused by this template: `BLOCKED_UNVERIFIED` until applied to a real project and tested.
