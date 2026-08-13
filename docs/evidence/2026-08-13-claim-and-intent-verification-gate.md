# Claim and Intent Verification Gate — Exact-Head Evidence

## Scope

- Proposal: `BCP-2026-027-claim-and-intent-verification-gate`
- Implementation PR: `https://github.com/alsdmlals4-eng/Base/pull/319`
- Base: `main@e2c1d0c4b6fd0a7ce7874d200176d267a7d614d5`
- Protected: 30 ACTIVE Skills, `PLAN / BUILD / REVIEW`, PR #312 visual-tool paths, PR #316 correction paths

## RED

- Exact RED head: `bf0890439cbef96777171cc00a0229c65e852af8`
- Game Project Operating System run: `31657742630`
- Result: existing contracts reached the new contract suite; six expected Claim/Intent contract assertions failed because the production Mode, reference, routing, Template/workflow integration, `SBE-038`, and central learning record were absent.
- Additional finding: three trailing-whitespace errors in the implementation plan were detected and removed during production mutation.

## Production generation

- Temporary mutation runner final input head: `839109f74035bc61ebf71642890f06df95dcb780`
- Temporary mutation run: `31697594695`
- Result: success
  - canonical contract dependencies installed
  - approved production mutation applied
  - Base v9 derivative regenerated with `--write`
  - focused Claim/Intent contract: `6/6 PASS`
  - behavior-eval contract checker: PASS
  - whitespace check: PASS
  - temporary workflow and mutator script removed before commit
- Production contract commit: `7a6fbc13938d2945293da914af9b7c0494397541`

## Registered consumer reconciliation

The first normal exact-head run on user commit `1e8947258e3d72d206c5e4f404c45d1c312ff04e` showed that the feature contracts and publication jobs passed, while canonical reference-freshness correctly required registered consumers for the changed Skill body, Registry metadata, behavior fixture, and generated implementation-evidence surface.

- Reconciliation input head: `0a363bd5f94308d886ad94c477aef686f5958ba3`
- Temporary reconciliation run: `31698256705`
- Result: success
  - focused Claim/Intent contract and all five coupled consumer regression modules passed
  - behavior-eval checker passed
  - `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md` regenerated
  - canonical reference-freshness passed on the committed local tree
  - `git diff --check` passed
  - temporary workflow and both reconciliation scripts were removed before push
- Consumer reconciliation production commit: `9c4d0c833f2548b8d56a8b4a83043075b8a44b05`

## Evidence boundary

The production commits created by `github-actions[bot]` with `GITHUB_TOKEN` did not produce reusable recursive exact-head validation. Their `action_required` or absent push runs are not accepted as PASS. User-authored evidence commits trigger normal PR workflows on the complete production tree. Merge and post-merge sections remain pending until their direct evidence exists.

## First complete exact-head GREEN

- Exact head: `eef62df811ae64ff92fa6692a3e91edb8a5e343b`
- Required workflows: all success
  - Evidence-Based Game Development Knowledge: `31698327100`
  - BCA Visual and Sheet Workflow: `31698327110`
  - Skill Behavior Evidence: `31698327112`
  - Integrated Vertical Slice Prompt: `31698327128`
  - Game UX UI System: `31698327132`
  - Base v9 Operating Contracts: `31698327204`
  - Game Project Operating System: `31698327106`
- Base v9 contract evidence: generated artifacts current; integrity and v9.4.1/.2/.3 checks passed; 328 tests passed; 1 Godot exact-engine test skipped because the executable was not configured; adversarial gate passed.
- Game Project OS evidence: proposal validation passed for 27 proposals; reference-freshness passed across 749 scanned files and 23 changed files; 410 tests passed with 15 environment-bound skips; publication validation and `ci-gate` passed.
- Dedicated Claim/Intent contract: `6/6 PASS`.
- Registered consumer regressions and Skill behavior-evidence workflow: PASS.
- Active Skill count: 30; Work Modes: `PLAN / BUILD / REVIEW`; generated active map current.
- External model behavior run: `NOT_RUN`; no model-run success is claimed.

## BCP lifecycle closeout

- Registry transition: `APPROVED_FOR_IMPLEMENTATION → IMPLEMENTED`
- Implementation PR: `https://github.com/alsdmlals4-eng/Base/pull/319`
- Closeout production commit: `eaa992313265da292a9ce3775cb17b0235e58fc5`
- Closeout mutation run: `31698751719` — lifecycle and focused regressions, proposal checker, reference-freshness and whitespace all passed; temporary workflow and script were removed before push.
- Rollback: revert the eventual PR #319 squash merge commit; no product code/data or PR #312/#316 path is affected.

## Adversarial document-consistency correction

A full final diff review found two stale historical claims that would have undermined the Gate itself:

1. the proposal closeout still contained `구현 PR: 아직 없음` below its implemented status;
2. the design and plan still cited abandoned PR #317 RED identifiers instead of canonical PR #319 evidence.

- Correction production commit: `7b97572ccd05daffb08a893e44f3eccf6b9887f5`
- Temporary correction run: `31699079157` — lifecycle and focused regressions, proposal checker, reference-freshness and whitespace all passed; temporary workflow and script were removed before push.
- Regression: the BCP lifecycle test now rejects the stale implementation-PR phrase and the superseded PR #317 RED identifiers, while requiring canonical RED head `bf0890439cbef96777171cc00a0229c65e852af8` in both plan and design.

A subsequent full proposal readback found one more active-state contradiction: the approval section still said `신규 제안 Registry 상태: SUBMITTED` below the implemented Registry and closeout.

- Final wording production commit: `a255442133ed31b602f5895f51d94f8c4fd54573`
- Temporary wording run: `31699245466` — lifecycle regressions, proposal checker, reference-freshness and whitespace all passed; temporary workflow and script were removed before push.
- Regression: the lifecycle test now rejects the stale submitted-status sentence and requires `최종 Registry 상태: IMPLEMENTED`.
- Definitive exact-head workflows are triggered by the user-authored commit containing this record; run IDs and the independent review are recorded on PR #319 without another tree change.

## Integration

- Independent adversarial review: `READY_TO_MERGE` on exact head `c9e85cad9f663b214a370cf873cc1bfa2a3a1947`; `P0 0 / P1 0 / unresolved P2 0`; unresolved review threads `0`.
- PR: `https://github.com/alsdmlals4-eng/Base/pull/319`
- Merge method: `squash`
- Merged at: `2026-08-13T12:23:49Z`
- Merge SHA: `f08a78b33aa1d458376da8f783553fe9ce7aa9cd`
- Post-merge main readback: `main@f08a78b33aa1d458376da8f783553fe9ce7aa9cd`; PR `merged=true`; the canonical Skill, dedicated reference, Registry-derived active map, behavior fixture, BCP proposal, and this evidence record were read back from that SHA.
- Post-merge workflows:
  - Base v9 Operating Contracts: `31699823282` — `success`
  - Game UX UI System: `31699823298` — `success`
  - Game Project Operating System: `31699823241` — `success`; Windows publication smoke, publication validation, and final `ci-gate` passed.
- External model behavior run: `NOT_RUN`; no model-behavior success is claimed.
- Final integration verdict: `MERGED_VERIFIED`
