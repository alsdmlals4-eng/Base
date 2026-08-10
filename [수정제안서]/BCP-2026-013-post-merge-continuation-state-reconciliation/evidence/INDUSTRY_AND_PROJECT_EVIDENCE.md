# BCP-2026-013 Evidence — Post-Merge Continuation-State Reconciliation

## Project evidence

Source project: `alsdmlals4-eng/ninja-survival-godot`

Observed sequence on 2026-08-10:

1. `docs/mvp4-handoff-20260810` persisted MVP-4 design continuation state.
2. Draft PR `#5` targeted `main@7ef8eeaec1e5e4bad65a7bf00061274b60641e6a`.
3. The PR head was `c930aeb2ee58e37c6e686cb2bddde6b98c67511b`.
4. Exact PR-head/merge-ref CI succeeded before integration.
5. The user explicitly approved integration.
6. PR #5 was squash merged.
7. Actual new project main became `9b85cf65a3ca4278f7d8ec1a7e527ecc857cbad1`.
8. The PR state became `closed / merged=true`.
9. A separate default-branch `push` workflow started for the new main commit and then succeeded.
10. The newly merged `docs/ACTIVE_CONTEXT.md` still contained the pre-merge values:
    - `main_sha: 7ef8ee...`
    - `handoff_pr_state: OPEN_DRAFT`
    - `handoff_pr_merged: NOT_RUN_USER_APPROVAL_REQUIRED`

This was not a failure of pre-merge documentation accuracy. The file correctly described the repository before the merge. The problem was that the same file also served as a **live resume router** after the merge.

## Failure mode

```text
current-state file is authored on feature branch
→ file correctly says feature PR is open
→ file is merged by that PR
→ repository truth changes
→ merged file now describes the immediately previous state
```

This creates a self-invalidating metadata edge whenever a mutable current-state document carries information about the integration operation that is delivering the document itself.

## Why exact-head CI does not solve it

Pre-merge verification can prove:

- branch content is valid;
- simulated merged tree is valid;
- tests pass against the PR merge ref.

It cannot prove future runtime facts that do not exist yet, such as:

- final squash/merge commit SHA;
- final PR `merged_at` state;
- post-merge default-branch push run result;
- whether another commit raced onto main after the pre-merge observation.

Those facts must be observed after integration.

## GitHub benchmark

Primary reference:

- GitHub Docs — Events that trigger workflows:
  `https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows`
- GitHub Docs — About pull requests:
  `https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests`

Relevant behaviors documented by GitHub:

### Pull request merge ref is not the final default-branch state

For an open, mergeable PR, GitHub exposes:

```text
refs/pull/<PR>/head
refs/pull/<PR>/merge
```

The merge ref is a simulated merge representation. It is useful for pre-merge validation but is still PR context.

### `pull_request` and `push` use different truth points

GitHub documents that `pull_request` workflows can run against the PR merge ref, while a `push` workflow uses the tip commit actually pushed to the updated ref.

Therefore:

```text
PR merge-ref validation
!=
post-merge default-branch observation
```

This distinction maps directly to continuation-state lifecycle.

### Merge is an observable state transition

A merged PR becomes closed/merged, and GitHub exposes merge-specific event data. Systems that need current state should react to or observe that state transition rather than treating the pre-merge PR metadata as final.

## Existing Base fit

Existing owner:

`skills/maintaining-project-context-and-handoff/SKILL.md`

Already covers:

- runtime truth first;
- state separation;
- responsibility-source refresh;
- Active Context refresh;
- session handoff;
- resume by re-reading latest branch/commit/files.

The proposal therefore does not justify a new Skill. It identifies a missing lifecycle edge inside the existing owner:

```text
integration complete
→ runtime truth changed
→ live continuation state must be reconciled
```

## Distinguishing historical evidence from live state

The project also showed why blindly rewriting all handoff documents would be wrong.

A dated handoff that says:

> At handoff time, PR #5 was draft and main was 7ef8ee...

remains valid historical evidence after merge.

A live router that says:

> Current PR #5 is draft and current main is 7ef8ee...

is stale after merge.

Recommended generic distinction:

```text
HISTORICAL_SNAPSHOT
- immutable or append-only
- preserves observation-at-time

LIVE_CONTINUATION_STATE
- mutable
- must track current observed repository truth
```

## Candidate acceptance contract

A future Base implementation should be testable with fixtures equivalent to:

```yaml
before_merge:
  live_state:
    main_sha: A
    pr_state: OPEN
actual_repo_after_merge:
  main_sha: B
  pr_state: MERGED
  post_merge_ci: IN_PROGRESS
expected:
  close_handoff_allowed: false_until_reconciled
  live_state_after_reconcile:
    main_sha: B_or_equivalent_observed_ref
    pr_state: MERGED
    post_merge_ci: IN_PROGRESS
```

After the push run finishes:

```yaml
actual_repo:
  post_merge_ci: PASS
expected_live_state:
  post_merge_ci: PASS
```

Historical snapshots are excluded from this mutation requirement.

## Non-goals

- No automatic GitHub write workflow is proposed.
- No mandatory exact-SHA field is proposed for every project.
- No project-specific Active Context schema is proposed.
- No change to user merge-approval gates is proposed.
- No claim is made that every merge needs a follow-up commit.

The general requirement is only that **a live continuation-state owner must not be closed as current while known to contradict post-integration runtime truth**.
