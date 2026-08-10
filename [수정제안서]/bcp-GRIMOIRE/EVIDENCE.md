# bcp-GRIMOIRE Evidence

## Source project

`alsdmlals4-eng/GRIMOIRE-`

## Source state

- observed project main: `fcb5dbe1cbbb23ef195633b1f6680f45d46c5a3f`
- active work: `Task 8 — Spell Use Screen, Target Selection, and Expected Result`
- project issue: `#111`
- local branch: `task8/spell-use-screen`
- local worktree: `C:/Users/user/Documents/GitHub/Ninza/GRIMOIRE-/.worktrees/task8-spell-use-screen/`
- interruption: `CODEX_USAGE_LIMIT`
- persistent GDScript authoring authority: `HIGODOT_ONLY`
- Hera authority: `LIVE_QA_AND_OBSERVABILITY_ONLY`

## Observed interruption evidence

Task 8 was not complete when the executor limit ended the session.

The persisted project checkpoint records:

- Task 7 already merged and verified.
- Task 8 implementation existed only in the local worktree.
- last Editor regression: `90 assertions / 0 failures`.
- earlier whole headless regression: `43 suites / 1639 assertions / 0 failures`.
- the whole-headless result predates final local edits and therefore requires rerun.
- no Task 8 remote branch or PR existed at the checkpoint.
- destructive reset/clean and reimplementation from scratch were explicitly prohibited.

The SESSION HANDOFF stored on project Issue #111 records the exact resume sequence:

1. fresh-read origin/main, Issue #111, local worktree/branch/dirty state and execution packet;
2. reconnect a fresh HiGodot session to the existing worktree;
3. fresh-read authored `.gd/.tscn` artifacts through authorized paths;
4. rerun Editor + workflow/state/atomic-use + full headless regressions;
5. run final adversarial review and verify P0/P1=0;
6. verify protected delta and `HERA_SOURCE_DELTA: NONE`;
7. write/read back a fresh HiGodot receipt;
8. commit/push/PR/exact-head CI/review-thread gate;
9. merge within approved scope;
10. fresh post-merge readback and Project Learning extraction.

## Existing Base coverage

### BCP-2026-010

`BCP-2026-010-continuous-work-execution-trigger` already defines the continuous execution loop and blocker-aware continuation behavior.

GRIMOIRE adds a concrete case where the blocker is an executor usage limit and the newest product state is local-only.

### maintaining-project-context-and-handoff

The existing handoff owner already covers the semantic need for:

- current-state recovery,
- resume locator,
- next exact work,
- blockers,
- runtime/repository truth over stale narrative state.

### BCP-2026-013

`BCP-2026-013-post-merge-continuation-state-reconciliation` covers the later lifecycle edge after integration, when main SHA, PR state, merge state and post-merge verification change.

Task 8 has not reached that edge yet, but the handoff explicitly requires applying it after merge.

### BCP-2026-014

`BCP-2026-014-handoff-machine-consumer-compatibility-closeout` covers compatibility-safe Handoff refresh/closeout and exact-head validation of machine-consumed surfaces.

GRIMOIRE does not currently show a distinct new machine-consumer contract failure beyond that owner.

## Existing Solution First result

```yaml
finding: executor_usage_limit_with_local_only_authoritative_work
verdict: REUSE
primary_existing_coverage:
  - BCP-2026-010-continuous-work-execution-trigger
  - maintaining-project-context-and-handoff
supporting_existing_coverage:
  - BCP-2026-013-post-merge-continuation-state-reconciliation
  - BCP-2026-014-handoff-machine-consumer-compatibility-closeout
new_broad_skill: false
new_active_base_rule: false
```

## Why this record still belongs in Base proposals

The proposal directory is also the preserved review area for project-derived lessons before active Base promotion.

`bcp-GRIMOIRE` makes three things explicit without creating duplicate behavior:

1. provenance: the evidence came from GRIMOIRE;
2. reuse decision: existing Base owners are sufficient so far;
3. continuation point: Task 8 post-merge learning must be re-evaluated before claiming there is no additional reusable gap.

This keeps project evidence discoverable while respecting Existing Solution First.

## Naming evidence

The user explicitly changed the proposal naming preference to **`BCP - 프로젝트 이름`**.

For this project the canonical project-scoped record is:

```text
bcp-GRIMOIRE
```

The intent is project discoverability, not creation of a competing numeric rule for every observation.

## Concurrency evidence

Base state was re-read before write:

- latest Base main observed before branch creation: `fbc0abd117066f45200b5cb440801cdd8f0c80a0`;
- Registry included through `BCP-2026-014`;
- open proposal PR #238 existed for `bcp-Switchy-Express-Cargo-Puzzle`;
- PR #238 intentionally did not edit `PROPOSAL_REGISTRY.json` at that checkpoint;
- older active Base PRs #136/#137 were unrelated active-implementation proposals and were not modified.

The GRIMOIRE branch was created from the latest Base main and modifies only its own proposal record plus the Registry entry added later in the same branch.

## Evidence limits

- Task 8 is not yet merged.
- fresh final Task 8 headless/Editor evidence is not available in Base and must not be inferred from the pre-interruption snapshot.
- no active Base implementation is validated or authorized by this record.
- post-merge Project Learning may add or change the reuse classification if a materially distinct gap is discovered.
