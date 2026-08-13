# Universal Loop Engineering SHADOW Kernel

## Purpose

The SHADOW Kernel is the deterministic, model-free control plane for milestone M3 of the Universal Loop Engineering program. It evaluates one project-bound implementation request, records an immutable receipt, and never writes product files.

The Kernel is deliberately separate from the M2 Capsule Schema implementation. M2 owns Capsule/Lock/Package contract documents. M3 consumes a normalized SHADOW request and owns only runtime state under the selected project's local `.loop-engineering/` directory.

## Non-authority boundary

The Kernel does not decide game design, player experience, art direction, or approved scope. Those remain human-approved Planning and Visual authority.

The Kernel must not:

- invoke an LLM or model Provider;
- access the network;
- execute a subprocess;
- open, create, update, or merge a pull request;
- write product source, data, scene, asset, or planning files;
- enable A3 auto-merge;
- configure a Scheduler;
- import another project's Canon, visual reference, asset, or session.

Its receipt records these boundaries explicitly:

```json
{
  "mode": "SHADOW",
  "product_mutation": "NONE",
  "model_invocation": "NONE",
  "network": "DENIED",
  "a3_auto_merge": "DISABLED",
  "scheduler_runtime_provider": "NOT_CONFIGURED"
}
```

## Commands

```bash
python tools/loopctl.py validate REQUEST.json \
  --project-root /absolute/project/root \
  --state-root /absolute/project/root/.loop-engineering

python tools/loopctl.py shadow REQUEST.json \
  --project-root /absolute/project/root \
  --state-root /absolute/project/root/.loop-engineering

python tools/loopctl.py status \
  --project-id PROJECT_ID \
  --run-id RUN_ID \
  --project-root /absolute/project/root \
  --state-root /absolute/project/root/.loop-engineering

python tools/loopctl.py leases \
  --project-id PROJECT_ID \
  --project-root /absolute/project/root \
  --state-root /absolute/project/root/.loop-engineering
```

`validate` is read-only and does not create the state directory. `shadow` may write only Kernel receipts and lease state under `.loop-engineering/`.

## State machine

The successful deterministic path is:

```text
CREATED
→ PREFLIGHT
→ AUTHORITY_SYNCED
→ CONTRACT_VALIDATED
→ COVERAGE_INITIALIZED
→ LEASE_ACQUIRED
→ SHADOW_RUNNING
→ SHADOW_VERIFIED
→ ADVERSARIAL_REVIEWED
→ SHADOW_COMPLETE
```

Illegal transitions fail closed. The request supplies a bounded transition budget; a value below the required successful path produces `BLOCKED_BUDGET`.

## Gates

The Kernel evaluates gates in fail-closed order:

1. closed request shape and safe A2-only constants;
2. project-local state-root confinement;
3. immutable run-id receipt collision;
4. prior receipt integrity;
5. duplicate successful semantic input;
6. repeated failure and `NO_PROGRESS` threshold;
7. transition budget;
8. source-main SHA freshness;
9. project identity, path, separator, Unicode, and symlink isolation;
10. Requirement Coverage completeness and allowed-output reconciliation;
11. Planning Drift;
12. Visual Lock and Visual Drift;
13. semantic resource lease ownership;
14. read-only product snapshot and immutable receipt publication.

## Project isolation

Repository-relative paths are normalized to Unicode NFC and `/` separators. Absolute paths, Windows drive paths, UNC paths, empty components, `.` and `..` are rejected. Both `/` and `\\` traversal forms are treated identically.

A path is checked lexically and physically. Existing symlink components are rejected before a referenced or product path is read. The state root must be the project-local `.loop-engineering/` directory or its descendant, and internal state paths may not traverse symlinks.

Project and run identifiers are closed identifiers rather than filesystem paths. Status and lease queries therefore cannot use path-like values to escape their project namespace.

## Requirement Coverage

Every package requirement must be approved and represented by one Coverage entry. Each entry must map:

```text
Requirement → Task → Output → Test → Evidence
```

Changed paths must be both allowed by the package and mapped to an approved requirement. Missing mappings, incomplete entries, missing required evidence, and unapproved outputs block the run.

## Visual and drift boundary

`NEW_VISUAL_REQUIRED` never becomes autonomous work. It produces `USER_DECISION_REQUIRED` until a human-approved Visual Lock exists.

`EXISTING_LOCKED` requires `VISUAL_LOCKED` with `NO_DRIFT` or `MINOR_TECHNICAL_DRIFT`. Planning conflicts and unverified planning state block before execution.

## Leases

Semantic resources are guarded by project-local leases. Lease updates use an exclusive guard and atomic replacement. A conflicting owner or a busy/corrupt lease ledger blocks the run; it is not silently overwritten.

Successful SHADOW evaluation releases its leases before publishing the terminal receipt. `leases` is therefore normally empty after `SHADOW_COMPLETE`.

## Immutable receipts

Receipts are written once using exclusive publication. An existing run-id receipt is never overwritten. Every receipt contains a canonical SHA-256 `receipt_digest`; reads recompute it and fail closed on corruption.

The semantic input digest excludes `run_id`, allowing the Kernel to detect the same approved input presented under another run identifier. A successful duplicate is blocked rather than re-executed. Repeated identical failures eventually become `BLOCKED_NO_PROGRESS`.

## Recovery and rollback

- A stale SHA requires rebuilding the request from the current trusted main.
- A Coverage or Drift block requires correcting the approved contract or obtaining a user decision; deleting the finding is not remediation.
- A lease conflict requires the owning run to close or an explicit recovery decision. Do not delete another run's lease blindly.
- A corrupt receipt or lease ledger requires quarantine and forensic review. The Kernel does not self-repair trusted evidence.
- Roll back the Kernel by reverting its Base PR. No product or project data migration is part of M3.

## M2 integration

This Kernel remains on an isolated branch while M2 PR #333 is owned by another workstream. The Kernel does not edit M2 files. After M2 is merged, a separate adapter must translate validated Capsule/Planning/Visual/Package/Coverage documents into the closed SHADOW request. That adapter is not implemented by M3 and must have its own TDD and compatibility evidence.
