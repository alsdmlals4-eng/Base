# Base v9.1 release contract

Base v9.1 preserves the v9.0 release artifacts and history. It adds compatible project operating contracts only; it does not alter game product code or retroactively rewrite the v9.0 release.

The machine-readable candidate identity is `base-v9.1.lock.json` with
`release_state=RELEASE_CANDIDATE`. Candidate payload/evidence commits remain
null until the corresponding commits exist; the lock must not invent them.
The current candidate Registry path and raw-byte hash are recorded independently,
but while either candidate commit pin is null, v9.1 adapter generation and
migration still fail closed. The v9.0 pins are compatibility history, not
runnable v9.1 adapter pins.

All eight outputs declared by `tools/build_base_v9_artifacts.py` form the v9.0
historical freeze set. For each path, `base-v9.1.lock.json` pins the Git blob OID
and raw SHA-256 resolved at `release_evidence_commit`. The checker validates
those immutable historical identities directly from Git, so Windows CRLF
checkout conversion cannot create a false failure. Current working paths may
evolve through a separately approved change, such as the #72 terminal-state
update to `GITHUB_OBJECT_LEDGER.json`; current-path equality is not the v9.0
freeze boundary.

The evidence commit is valid only when it is the exact `base.lock.json`
transition from `BASE_RELEASE_PENDING_CI` to `BASE_RELEASED` for release line
`v9.0.0`. Its released payload pin must match `release_commit`, that payload
must be an ancestor of the evidence commit, and the evidence commit must be an
ancestor of an externally trusted history tip. Local validation resolves
`refs/remotes/origin/main`; pull-request CI supplies the pull-request base SHA,
and other CI events supply `github.sha`. Missing or non-ancestral trust fails
closed, so a later commit cannot rebind the historical evidence and frozen
outputs to itself.

## Release pins

Every project adapter records two distinct immutable pins:

- `release_commit`: the release payload.
- `release_evidence_commit`: evidence and release-state metadata; the payload must be an ancestor.

Unknown, stale, mismatched, or non-ancestral pins fail closed. Registry content hashes must match the pinned contract before route execution.
`compatibility_base.historical_registry` binds the v9.0 Registry commit, path,
and raw-byte SHA-256 to the `base.lock.json` Git blob at
`release_evidence_commit`. It is historical authority only; later evolution of
the current `base.lock.json` has no effect on that comparison.
`candidate_registry` separately binds the current v9.1
checkout Registry path and raw-byte SHA-256. Once candidate commits are issued,
a released project adapter reads the matching Registry blob with
`git show <release_evidence_commit>:<candidate_registry.path>`.

## v9.1 evidence record and pin finalization

The v9.1 payload and its evidence boundary are deliberately separate. The
release-evidence record at
[`BASE_V9_1_RELEASE_EVIDENCE.json`](BASE_V9_1_RELEASE_EVIDENCE.json) is first
merged to trusted `main` without changing the candidate Registry. A subsequent
pin-finalization PR may then set both candidate pins in `base-v9.1.lock.json`.
The validator reads the evidence record from that pinned historical commit and
requires its payload SHA and Registry identity to match the lock. This prevents
an untrusted feature branch from self-attesting a newly invented release pin.

## Supply chain

GitHub workflows use least permissions and official Actions pinned to full commit SHAs. Dependency review is capability-gated for pull requests that change dependency manifests or lockfiles: the repository owner enables the dependency graph/security capability first, then sets `DEPENDENCY_REVIEW_ENABLED=true`. Until that explicit opt-in exists, the workflow records `DEFERRED_UNTIL_REPOSITORY_SECURITY_ENABLED` rather than reporting a false security pass. Binary attestation is `DEFERRED_UNTIL_RELEASE_ARTIFACT`; no attestation claim is made before a releasable binary exists.

The project adoption workflow passes `github.event.pull_request.base.sha` to
the validator and requires exact equality with the adapter's recorded commit.
When `GITHUB_PR_BASE` is selected, its authority ref is exactly that event
expression; local validation instead selects and resolves an explicit
remote-tracking ref. `--protected-base` is trusted input from the caller's CI
boundary; it is not a replacement baseline and does not provide cryptographic
attestation.

## Evidence boundary

This Base change may verify schemas, generators, validators, repositories, CI syntax, and publication tooling. Godot runtime, device, accessibility, and human evidence remain `NOT_RUN`. Project migrations require separate project-owned branches and evidence.
