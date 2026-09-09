# Federated GitHub + Approved PDF Dual Canon Design

- Status: `USER_APPROVED`
- Approval reference: `current-user-message:2026-09-04:앞으로-둘-다-정본`
- Existing implementation workstream: Issue #846 / PR #847
- Related proposal lineage: `BCP-2026-051-desktop-two-artifact-master-gdd`
- Supersedes active “repository canon + non-canonical PDF” wording only; historical proposal and plan evidence remains immutable history.

## 1. Problem

The current V4 workspace contract treats the repository as the only project canon and the human Blueprint PDF as a non-canonical derived snapshot. That protects machine-readable data, but it leaves the user-approved visual explanation, information hierarchy, whole-project flow, milestone scope, and prior Blueprint composition too weak to block visual omission or semantic regression.

Making both surfaces fully editable owners of the same facts would create a worse failure mode: values, status, IDs, and decisions could diverge with no deterministic conflict rule. The approved design therefore uses two canonical surfaces with disjoint authority and one editable owner for every atomic fact.

## 2. Alternatives

### A. Repository-only canon; PDF remains derived

- Strength: simplest implementation and machine validation.
- Weakness: an approved human-facing visual baseline can be silently regenerated with lost sections, changed hierarchy, or altered flow and dismissed as “only a derivative.”
- Disposition: `REJECT` for the requested operating model.

### B. Repository and PDF are equal, independently editable owners of all facts

- Strength: either surface can be changed directly.
- Weakness: unavoidable double entry, ambiguous conflict resolution, stale status, and non-deterministic implementation handoff.
- Disposition: `REJECT`.

### C. Federated dual canon with one editable owner per atomic fact

- Strength: the repository retains deterministic executable and structured truth, while the approved PDF becomes the immutable human visual/review baseline. Shared IDs, exact revision metadata, coverage checks, and fail-closed conflict states connect them.
- Weakness: publication and approval require a manifest and comparison gate.
- Disposition: `ADOPT`.

## 3. Authority model

```text
FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER

REPOSITORY_EXECUTION_DATA_CANON
├─ code, scenes, resources, assets, data, schemas, IDs
├─ formulas, numeric values, conditions, state machines
├─ editable planning sources, decisions, work status and evidence
└─ implementation, tests, runtime and release facts

APPROVED_HUMAN_BLUEPRINT_PDF_CANON
├─ user-approved human interpretation baseline
├─ project/player experience map and reading order
├─ visual hierarchy, flow composition and information priority
├─ approved milestone scope and visible checklist coverage
└─ immutable rendered evidence of what the user reviewed
```

The shared invariant is:

```text
ONE_EDITABLE_OWNER_PER_ATOMIC_FACT
```

The PDF does not become a second editable database. Structured values, IDs, completion states, and evidence locators appearing in the PDF are projections from repository owners. The approved PDF binary and its approved visual composition are canonical in the human visual/review domain.

## 4. PDF canon activation and lifecycle

A generated PDF is not automatically canonical.

```text
GENERATED_CANDIDATE
→ USER_APPROVED_PENDING_REGISTRATION
→ USER_APPROVED_AND_MANIFEST_REGISTERED
→ CANON_ALIGNED
```

Activation requires:

- exact `source_commit`;
- `pdf_sha256`;
- reproducible `approval_ref`;
- `approved_at`;
- `canonical_status`;
- `supersedes_pdf_ref`;
- repository-controlled `pdf_canon_manifest_ref`;
- included scope and evidence ceiling;
- stable ID and coverage readback.

An approved canonical PDF is immutable. A correction produces a new filename/hash/version and supersedes the old PDF without deleting history.

```text
APPROVED_PDF_IMMUTABLE_NEW_VERSION_REQUIRED
NEW_VERSION_NEW_HASH_KEEP_HISTORY
```

Candidate PDFs, previews, Library-only copies, and unregistered annotations are not canon.

## 5. Ownership and edit flow

### Repository-owned structured fact

Example: `action_slot_count: 3`.

1. Change the repository owner and decision/evidence.
2. Regenerate a PDF candidate from the new exact revision.
3. Compare it with the current approved PDF.
4. Obtain user approval.
5. Register the new PDF hash and supersession.

Editing the PDF to show `4` without repository reflection is a change request, not a canon mutation.

```text
PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION
PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION
```

### PDF-owned human visual baseline

Example: the approved out-game flow shows the user journey, screen order, information hierarchy, and system-card composition.

If implementation or a new PDF materially differs, it does not silently replace the approved baseline. The work must either:

- correct the implementation/publication to match the approved PDF; or
- publish a new candidate, show the semantic and visual delta, and obtain a new user approval.

## 6. Alignment and conflict states

```text
CANON_ALIGNED
REPOSITORY_ADVANCED_PDF_REVIEW_REQUIRED
PDF_FEEDBACK_PENDING_REPOSITORY_REFLECTION
CANON_CONFLICT
SUPERSEDED
```

Rules:

- Repository source SHA advances with no material human-baseline change: retain the approved PDF as a historical baseline, but mark current publication review required when the included scope changed.
- PDF annotation or user feedback is not yet reflected in repository owners: `PDF_FEEDBACK_PENDING_REPOSITORY_REFLECTION`.
- Structured data differs between repository and PDF: repository owner controls the value; the PDF cannot be current and must be regenerated.
- Approved visual flow/hierarchy differs from implementation: implementation is not automatically authoritative; correct it or obtain reapproval.
- Simultaneous unresolved differences: `CANON_CONFLICT`.

```text
CANON_CONFLICT_BLOCKS_COMPLETION_AND_RELEASE
```

Document generation, static tests, machine tests, runtime verification, UX verification, PDF approval, and release approval remain separate evidence levels.

## 7. Work-status projection inside the canonical PDF

The PDF as a whole may be canonical for the human visual/review domain while mutable work status remains repository-owned.

```text
PROJECT_WORK_KANBAN_IS_PROGRESS_SOURCE
PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION
NO_PARALLEL_BLUEPRINT_STATUS_CANON
```

Goal/system/case/work completion is recalculated from repository receipts and evidence at the PDF source revision. Hand-editing a checkbox in the PDF never changes work status.

This distinction prevents “dual canon” from becoming duplicate PM state.

## 8. Loss and regression prevention

Every successor candidate compares with the current approved PDF and source inventory.

Required checks:

- stable IDs preserved or explicitly mapped;
- sections, diagrams, approved assets, captions, consumers, and evidence carried forward or justified;
- goal → system → case → work item → evidence traceability intact;
- source SHA and shared IDs match;
- PDF page render has no clipping, blank pages, broken glyphs, or missing links;
- semantic removals and status downgrades have explicit reason and impact;
- visual hierarchy and flow deltas are shown to the user before approval.

A failed check preserves the prior approved PDF and blocks successor promotion.

## 9. Active Base propagation

The correction applies to current authority and cold-start routing surfaces:

- root `AGENTS.md`, `README.md`, `START_HERE.md`;
- V4 workspace policy and machine contract;
- Operating Model, Documentation Map, planning/visual/decision policies;
- active design-document Skill;
- project AGENTS and GPT/Codex/Copilot/project-operation templates;
- two-artifact Blueprint policy and instruction;
- repository contract tests.

Historical BCPs, old plans, review evidence, and legacy V3 records remain unchanged as historical evidence.

## 10. Interaction with open PR #845

PR #845 contains a complementary progress renderer and publication validator, but its current contract says the PDF is never a canonical status or live authority. It remains read-only and must not merge until rebased conceptually on this model:

- retain repository-owned progress state;
- replace blanket “PDF not canon” wording with the domain-specific split;
- consume the V4 dual-canon fields and approved-PDF manifest;
- add candidate/approval/conflict/supersession tests.

No content from #845 is silently copied into #847.

## 11. Validation

Repository tests must prove:

- exact V4 authority fields and PDF registration metadata;
- old non-canonical PDF tokens absent from active routing surfaces;
- candidate PDFs cannot become canon without approval + registration;
- annotations cannot mutate repository-owned values;
- work status remains a repository projection;
- unresolved conflicts block completion/release;
- predecessor/successor loss gates remain intact;
- legacy Notion/V3 and runtime evidence boundaries remain unchanged.

Repository tests cannot prove a specific project PDF’s visual quality, a user’s actual approval, Godot runtime, UX, device behavior, or release readiness.

## 12. Rollback

Rollback reverts the eventual squash commit. Historical approved PDFs and proposal records are not deleted. Projects that have not adopted the new Base revision retain their existing explicit contract until reconciled.
