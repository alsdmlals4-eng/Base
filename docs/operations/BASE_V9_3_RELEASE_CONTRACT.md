# Base v9.3 release contract

Base v9.3 is a compatible correction over released Base v9.2. It does not rewrite
the v9.2 payload, evidence, or pin-finalization commits. It restores the active
v9 prompt's single-attachment integrated execution behavior while keeping
repository binding, dynamic Skill routing, conditional reconciliation, visual
checkpoints, and evidence gates.

## Candidate identity

`base-v9.3.lock.json` is the machine-readable candidate identity. Its release
and evidence pins stay `null` on the candidate branch. A separate trusted-main
evidence PR and a later pin-finalization PR must set them; a branch must not
self-attest either SHA.

Projects must not pin Base v9.3 until the candidate, evidence, and pin
finalization PRs have all merged. Existing Base v9.1 and v9.2 project pins remain
valid and unchanged. Until that finalization, new migrations select the newest
locally available lock with usable release and evidence pins (v9.2 where it is
present); selecting `9.3.0` requires explicit released pins. This retains
compatibility with a v9.1-only Base checkout that exposes its verified pins as a
candidate identity.

The Base v9 integrity check and Base v9 contract workflow validate the v9.3 lock
on candidate, evidence, and pin-only PRs. An evidence PR is checked against
Issue `#107`, its payload Git blob, and the candidate Registry before it may be
merged. A released lock must then draw that evidence record from trusted pre-PR
main history, prove payload-to-evidence ancestry, and match the evidence commit's
raw Registry bytes.

## Single-attachment behavior

The active v9 prompt begins with `APPLICATION_BINDING` and
`REPOSITORY_FIRST_INTERVIEW`. It then selects `RECONCILIATION_PLANNING_PROFILE`
only for audit-only, unapproved, or blocked work; otherwise it uses
`INTEGRATED_DELIVERY_PROFILE` to link planning, Issue/Goal, Codex implementation,
validation, merge, and merged-main synchronization.

The prompt never treats an attachment alone as permission to invent product scope,
change a protected path, or promote a Sheet-only edit into canonical truth.
