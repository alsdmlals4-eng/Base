# Base v9.1 release contract

Base v9.1 preserves the v9.0 release artifacts and history. It adds compatible project operating contracts only; it does not alter game product code or retroactively rewrite the v9.0 release.

The machine-readable candidate identity is `base-v9.1.lock.json` with
`release_state=RELEASE_CANDIDATE`. Candidate payload/evidence commits remain
null until the corresponding commits exist; the lock must not invent them.
While either candidate pin or the candidate Registry hash is null, v9.1 adapter
generation and migration fail closed. The v9.0 pins are compatibility history,
not runnable v9.1 adapter pins.

## Release pins

Every project adapter records two distinct immutable pins:

- `release_commit`: the release payload.
- `release_evidence_commit`: evidence and release-state metadata; the payload must be an ancestor.

Unknown, stale, mismatched, or non-ancestral pins fail closed. Registry content hashes must match the pinned contract before route execution.
The Base Registry authority for a released adapter is the blob read with
`git show <release_evidence_commit>:skills/SKILL_REGISTRY.json`; the current
working-tree Registry may evolve and is not substituted for that historical blob.

## Supply chain

GitHub workflows use least permissions and official Actions pinned to full commit SHAs. Dependency review runs for pull requests that change dependency manifests or lockfiles. Binary attestation is `DEFERRED_UNTIL_RELEASE_ARTIFACT`; no attestation claim is made before a releasable binary exists.

## Evidence boundary

This Base change may verify schemas, generators, validators, repositories, CI syntax, and publication tooling. Godot runtime, device, accessibility, and human evidence remain `NOT_RUN`. Project migrations require separate project-owned branches and evidence.
