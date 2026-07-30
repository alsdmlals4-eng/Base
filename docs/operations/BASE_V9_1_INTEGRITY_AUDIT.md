# Base v9.1 integrity audit

## Scope

Static review of GitHub Issue #71 Base-only changes: schemas, project-contract tools, generated-view contracts, shared-Skill guidance, publication runner, CI workflows, and governance documents. No game product repository, Google Sheet, Godot runtime, device, accessibility session, or human playtest was changed or executed.

## Review cycle 2: verified blocker remediation

The earlier pre-remediation zero-finding statement is withdrawn. Independent
review found blocking gaps in Action provenance, historical immutability,
release-lock binding, health evidence, routing, path/protected boundaries,
generation preflight, compatibility projections, migration, PDF wrappers, and
clean-runner dependencies.

| Severity | Review state | Evidence recorded in this cycle |
|---|---|---|
| P0 | `CLOSED_BY_POST_FIX_VERIFICATION` | v9.0 one-byte tamper fixtures; v9.1 null/mismatched lock fixtures; root/symlink/reparse escape fixtures |
| P1 | `CLOSED_BY_POST_FIX_VERIFICATION` | health counterexamples; ACTIVE route/alias resolution; normalized shared-body/provenance fixtures; protected tracked/untracked/policy fixtures |
| P2 | `CLOSED_BY_POST_FIX_VERIFICATION` | exact Action allowlist; source-backed legacy projections; dashboard escaping; explicit migration pins; trusted Windows wrapper execution/rejection |

Post-fix review cycle 2 records all verified blockers as closed by focused
RED/GREEN evidence and a complete 279-test run with one declared Mermaid
environment skip. This is a static repository verdict, not runtime or human evidence.

## Review cycle 3: verified second-review remediation

A second independent review found that cycle 2 still trusted self-reported
health evidence, froze only three of eight v9.0 generator outputs, compared
worktree bytes in a CRLF-sensitive way, conflated historical/current Registry
authority, and allowed the protected baseline to be omitted. It also found
dependency-review and adapter-hash consistency gaps.

| Severity | Review state | Evidence recorded in this cycle |
|---|---|---|
| P0 | `CLOSED_BY_POST_FIX_VERIFICATION` | missing/fake/duplicate/escaped/reparse evidence fixtures; complete eight-output historical pin set; blob OID/SHA-256 mutation; clean clone with `core.autocrlf=true` |
| P1 | `CLOSED_BY_POST_FIX_VERIFICATION` | commit-qualified historical Registry versus current candidate Registry; standard `--check` protection without a CLI baseline; explicit migration baseline |
| P2 | `CLOSED_BY_POST_FIX_VERIFICATION` | workflow/Action dependency-review paths; snapshot/dashboard `RAW_FILE_BYTES_SHA256` consistency |

Cycle 3 focused tests passed, including the clean-clone CRLF regression. The
first complete post-fix repository run passed 283 tests with one declared
Mermaid environment skip. The final verification below was repeated after this
audit update; no runtime, device, accessibility, human, or binary evidence is
inferred from these static checks.

## Review cycle 4: first-migration baseline source correction

Final review found that the required protected baseline still assumed
`skills/PROJECT_BASE_ADAPTER.json` existed before the first migration. That
made a real legacy-only migration impossible despite the fail-closed baseline
requirement.

The adapter now records a commit-qualified protected-policy source contract:
`FIRST_MIGRATION_LEGACY_SOURCE` reads the explicit legacy JSON blob, while
`CANONICAL_ADAPTER_SOURCE` supports later waves. Both bind source path,
`/protected_paths` pointer, and canonical policy SHA-256. Missing sources,
non-regular blobs, extraction failures, hash mismatch, weakening, and protected
product changes fail closed.

Cycle 4 RED/GREEN fixtures use a baseline commit containing a real legacy
adapter and protected product file but no canonical adapter. They cover
successful migration and standard validation, missing source, fake hash,
unextractable policy, weakening, later canonical baseline, and protected
product mutation. Focused tests passed, followed by a complete 284-test run
with one declared Mermaid environment skip.

## Review cycle 5: external protected-baseline authority

Final adversarial review found that a feature branch could move the adapter's
recorded baseline after changing a protected product file, allowing the mutable
adapter to attest its own comparison base. A CLI baseline could also replace
the adapter record.

The adapter now records `authority_kind` and `authority_ref` in addition to the
baseline commit. Local standard validation resolves a `REMOTE_TRACKING_REF`
and requires exact commit equality. Pull-request CI passes the exact
`github.event.pull_request.base.sha` as trusted caller input and requires it to
equal the adapter commit; it never overrides the record. This boundary is not
a cryptographic attestation claim. Migration requires an explicit baseline,
authority kind, and authority ref and never derives them from `HEAD`.

Cycle 5 RED/GREEN fixtures cover a correct remote baseline, a mismatched CLI
baseline, a missing authority ref, a feature-branch self-attestation attempt,
and confirmation that the externally fixed old baseline still detects the
protected product change. The 30 focused tests passed, followed by a complete
285-test run with one declared Mermaid environment skip. Deterministic Base v9
generation, Base v9 integrity, `git diff --check`, `git fsck --strict`, all
eight frozen v9.0 evidence-blob identities, and unchanged Godot product paths
also passed. After #72, approved current governance artifacts may differ from
their v9.0 historical blobs without changing those pinned identities.

## Protected scope

Base v9.1 changed no Godot project product path, scene, Resource, gameplay data, asset, balance, or player-facing rule. The cross-repository validator uses an externally resolved commit that must exactly equal the adapter baseline; trusted CLI input can verify equality but cannot replace the adapter record.

## Evidence status

- Focused static remediation evidence: `PASS`, including clean-clone `core.autocrlf=true` coverage.
- Final full repository evidence: `PASS` — 285 tests, one declared Mermaid environment skip.
- Runtime: `NOT_RUN`.
- Device: `NOT_RUN`.
- Accessibility: `NOT_RUN`.
- Human validation: `NOT_RUN`.
- Binary attestation: `DEFERRED_UNTIL_RELEASE_ARTIFACT`.
