# Base v9.2 release contract

Base v9.2 is a compatible candidate layer over immutable Base v9.0 and does not rewrite v9.1 or product repositories. It activates the Vertical Slice v9 reconciliation contract, project application template, and intermediate visual checkpoint.

## Candidate identity

`base-v9.2.lock.json` is the machine-readable candidate identity. During this candidate PR both `candidate_release_commit` and `candidate_release_evidence_commit` are intentionally `null`: a branch must not self-attest its own release or evidence SHA.

No project may pin Base v9.2 or execute a v9.2 Application Binding until a later trusted-main evidence record and pin-finalization PR provide both values. The release payload pin must be an ancestor of the evidence pin, and the Registry raw-byte SHA must equal the Registry blob at the pinned evidence commit. Unknown, missing, stale, or non-ancestral pins fail closed.

## Required release sequence

1. Merge the v9.2 contract candidate to trusted `main`.
2. Create and merge a separate v9.2 release-evidence record that names that payload commit and test evidence.
3. Create and merge a pin-finalization PR that sets both candidate pins in `base-v9.2.lock.json`.
4. Only then update project adapters, regenerate their compatibility views, and create each project-owned reconciliation PR.

The first project wave remains `RECONCILIATION_PLANNING_PROFILE`: it may add binding, audit, visual-review, and Change Plan records, but cannot modify product code, Scene, data, assets, approved Decision, or Google Sheet values.
