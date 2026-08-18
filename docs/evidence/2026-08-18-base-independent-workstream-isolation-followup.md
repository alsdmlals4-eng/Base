# Base Independent Workstream Isolation — Follow-up Evidence

Date: 2026-08-18
PR: #516

## Finding

Final adversarial recheck found that the long-horizon policy covered worktree/port collision handling and open-PR reconciliation but did not directly encode the user's standing rule that other chats and independent workstreams must remain untouched by default.

This was a real `P1` future-concurrency risk because a later integration task could interpret stale/open PR reconciliation as permission to mutate another chat's branch, path, worktree, or PR.

## TDD evidence

Test-first commit: `e438ff06bbc347927b7bb2725e6b03262f4ff81c`

Expected RED:
- `Validate Base Long-Horizon Work Contract` run `32105638578`: `FAILURE`
- the new regression required:
  - `INDEPENDENT_WORKSTREAM_ISOLATION`
  - `OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT`
  - `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`

Minimal implementation commit: `dd35946a148f199b3cf753ed35a866a6aaef539c`

Observed GREEN:
- `Validate Base Long-Horizon Work Contract` run `32105768010`: `SUCCESS`

## Final contract

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

- other chat / independent Goal branches, worktrees, paths, ports, Resource Locks, and PRs are not mutation targets by default;
- same-Goal prior PRs are semantically classified before material-delta reuse, rather than merging stale whole branches;
- an exception requires explicit user authorization for the current work;
- unrelated PRs may remain separate even when some open PRs are authorized for absorption;
- unclear ownership fails closed until authoritative state is re-read.

## Current-session exception

The user explicitly stated that this is the only active Base chat and authorized absorbing/reconciling still-open owner PRs. That instruction is a valid exception for PR #516 only and does not remove the default isolation rule for future concurrent work.

## Evidence ceiling

This proves repository policy and regression wiring. It does not claim that every external client or future agent will obey the policy without loading the current Base entrypoint and policy chain.
