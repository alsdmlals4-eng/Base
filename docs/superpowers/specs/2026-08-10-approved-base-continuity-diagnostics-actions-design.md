# Approved Base Continuity, Diagnostics, and Actions Design

## Decision record

The user approved all three recommendations on 2026-08-10:

1. implement the shared continuation/handoff improvements represented by BCP-013,
   BCP-014, BCP-016, and BCP-019;
2. implement the fail-closed Godot pilot diagnostic-preservation improvement in
   BCP-018; and
3. re-port the complete Node 24-compatible GitHub Actions update, including its
   immutable-action allowlist and regression contracts.

This approval is the implementation authority. It does not approve BCP-012,
BCP-015, or BCP-017, and does not authorize automatic writes to project state.

## Goal

Make Base safer to resume after a merge, safer to compress machine-consumed
handoff documents, able to preserve sanitized diagnostic evidence when a Godot
pilot fails, and free of the known Node 20 action-runtime warnings without
weakening CI or changing game/product behavior.

## Chosen approach

Use four small, sequential pull requests rather than one broad change:

1. **Approval-record PR** updates only the approved BCP records and
   `PROPOSAL_REGISTRY.json` to `APPROVED_FOR_IMPLEMENTATION`, with this design
   as the approval reference.
2. **Continuation-contract PR** extends the existing
   `maintaining-project-context-and-handoff` and
   `auditing-canonical-reference-freshness` owners. It adds a post-merge fresh
   read, distinguishes mutable live state from historical snapshots, and requires
   a consumer inventory before compressing a machine-consumed handoff. Existing
   consumers must be preserved only when they encode a real semantic contract;
   accidental literal-shape consumers must be migrated, not fossilized.
3. **Diagnostic-preservation PR** changes the existing Godot pilot evidence path
   so a sanitized, bounded snapshot is written before terminal semantic
   verification. A `FAIL` remains non-zero; preserving evidence never converts a
   failure into a pass, retries never overwrite a prior attempt, and tracked
   project source remains unchanged.
4. **Actions-runtime PR** updates only the five approved action families
   (`checkout`, `setup-python`, `setup-node`, `upload-artifact`, and
   `dependency-review-action`) to currently supported immutable Node 24-capable
   releases. It updates the repository's action-pin authority and regression
   fixtures in the same PR. Exact SHAs are selected from the official action
   release/tag at execution time, never guessed or copied from an old PR.

## Why not the alternatives

- A single implementation PR would mix approval state, docs/contracts, Python
  evidence behavior, and workflow pins. A failed CI or review finding would then
  obscure its cause and make rollback broad.
- Directly merging the old dependency PRs would retain their stale base, omitted
  allowlist/contract updates, and in one case unrelated BOM churn.
- Adding a new broad Skill for either handoff or diagnostics would duplicate
  established owners and make routing less clear.

## Architecture and boundaries

| Area | Existing owner extended | Explicitly excluded |
| --- | --- | --- |
| Continuation state | `maintaining-project-context-and-handoff` | automatic project-state writing; rewriting dated historical reports |
| Consumer compatibility | `auditing-canonical-reference-freshness` | permanent storage of obsolete literal tokens |
| Pilot diagnostics | existing Godot pilot/evidence tooling | retry policy changes; Godot runtime/product changes |
| Action runtime | workflow pin authority and its tests | workflow trigger, permission, or branch-protection changes |

The continuation contract is documentation and validation guidance, not a new
background workflow. It applies only when a live continuation router exists and
integration changes truth that the next session reads.

The diagnostics contract uses an isolated temporary/artifact workspace. Its
preservation order is:

```text
receive raw runtime result
→ redact and bound it
→ save attempt-identified diagnostic snapshot
→ run terminal semantic verifier
→ retain non-zero failure or finish normal PASS bundle
```

## Acceptance criteria

### Approval record

- BCP-013, BCP-014, BCP-016, BCP-018, and BCP-019 have an immutable approval
  reference and `APPROVED_FOR_IMPLEMENTATION` status.
- No other proposal status changes.

### Continuation contract

- A merged PR with a stale live router is identified for post-merge
  reconciliation, while dated pre-merge history remains valid history.
- A closeout that changes a machine-consumed handoff requires consumer inventory,
  classification, exact-head validation, and a post-merge re-read.
- Tests prove that semantic consumer migration is allowed only after the
  canonical protocol is identified; a real literal protocol cannot be weakened.
- Existing owners, registry bytes, and generated active-skill view remain
  unchanged unless a dedicated coupled-change test proves otherwise.

### Diagnostic preservation

- A synthetic `FAIL` retains a sanitized, bounded runtime-result snapshot before
  the terminal verifier returns non-zero.
- The failure bundle connects descriptor, relevant ledger/state, wrapper
  metadata, and attempt identity without exposing secret fixtures.
- PASS behavior and artifact semantics remain intact.
- A retry is a separate attempt, and tracked source hashes/diff do not change.

### Actions runtime

- Every pinned occurrence of the five approved action families uses the selected
  official immutable SHA.
- The allowlist/authoritative constants and all fixtures assert those same SHAs.
- No BOM-only or unrelated workflow formatting change is included.
- Local topology/pin tests and exact-head hosted CI remain green; the final PR
  reports runner compatibility rather than assuming self-hosted runners meet the
  Node 24 minimum.

## Validation and rollback

Each PR begins with a focused failing test and ends with the targeted suite,
canonical-reference freshness audit when a canonical owner changes, adversarial
review, and the repository validation entry point with the exact trusted main
SHA. Hosted CI must pass on the exact PR head before merge.

Each PR is independently squash-revertible. Reverting the continuation contract
does not change project state, reverting diagnostic preservation restores the
previous evidence order without altering PASS/FAIL rules, and reverting action
pins restores the prior pinned releases. Proposal records and historical
evidence are retained in every case.
