# Base v9.1 release contract

Base v9.1 preserves the v9.0 release artifacts and history. It adds compatible project operating contracts only; it does not alter game product code or retroactively rewrite the v9.0 release.

The machine-readable candidate identity is `base-v9.1.lock.json` with
`release_state=RELEASE_CANDIDATE`. Candidate payload/evidence commits remain
null until the corresponding commits exist; the lock must not invent them.
The current candidate Registry path and raw-byte hash are recorded independently,
but while either candidate commit pin is null, v9.1 adapter generation and
migration still fail closed. The v9.0 pins are compatibility history, not
runnable v9.1 adapter pins.

All eight outputs declared by `tools/build_base_v9_artifacts.py` are the exact
v9.0 frozen set. Each is compared with its release-evidence Git blob using the
repository clean filter, so Windows CRLF checkout conversion does not create a
false failure while a real content mutation still fails.

## Release pins

Every project adapter records two distinct immutable pins:

- `release_commit`: the release payload.
- `release_evidence_commit`: evidence and release-state metadata; the payload must be an ancestor.

Unknown, stale, mismatched, or non-ancestral pins fail closed. Registry content hashes must match the pinned contract before route execution.
`compatibility_base.historical_registry` binds the v9.0 Registry commit, path,
and raw-byte SHA-256 to frozen `base.lock.json` and its Git blob. It is historical
authority only; `base.lock.json.source_of_truth` is never interpreted as the
current checkout. `candidate_registry` separately binds the current v9.1
checkout Registry path and raw-byte SHA-256. Once candidate commits are issued,
a released project adapter reads the matching Registry blob with
`git show <release_evidence_commit>:<candidate_registry.path>`.

## Supply chain

GitHub workflows use least permissions and official Actions pinned to full commit SHAs. Dependency review runs for pull requests that change dependency manifests or lockfiles. Binary attestation is `DEFERRED_UNTIL_RELEASE_ARTIFACT`; no attestation claim is made before a releasable binary exists.

## Evidence boundary

This Base change may verify schemas, generators, validators, repositories, CI syntax, and publication tooling. Godot runtime, device, accessibility, and human evidence remain `NOT_RUN`. Project migrations require separate project-owned branches and evidence.
