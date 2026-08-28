# Repository-First Project Workspace Design

## Status

- Decision: `APPROVED_FOR_IMPLEMENTATION`
- User approval date: `2026-08-28`
- Source main: `7cfc75d607d1ed4d0f8323d4389e64da93df00c8`
- Scope: Base reusable project-workspace, GPT–Codex handoff, asset-delivery and human-review contract
- Evidence ceiling: process and documentation contract only; no project migration or runtime completion is claimed by this Base change

## 1. Problem

The active Base model requires project planning, human-facing canon, approved visual delivery and Codex rehydration to pass through Notion. That made sense when Notion was the primary human browsing and image-delivery surface, but the current operating environment has changed:

- desktop ChatGPT Work can work with local project files;
- GitHub already owns versioned Markdown, JSON, assets, code, tests and runtime evidence;
- ChatGPT Library can preserve generated images, documents and reference files;
- the user plans to review project state at meaningful gates through a detailed human-facing PDF rather than maintain a continuously synchronized Notion Home;
- the default final deliverables are now exactly two products: a human-facing detailed GDD PDF and an AI-facing detailed planning/implementation Markdown specification.

Continuing mandatory Notion writes would add duplicate authoring, duplicate readback and cross-surface drift without providing a required capability.

## 2. Decision

Adopt `REPOSITORY_PRIMARY_CANON` as the default project authority model.

```text
latest user decision
→ project AGENTS.md and approved project contract
→ repository canonical Markdown / JSON / tracked assets / implementation evidence
→ exact-commit human GDD PDF as a derived review view
→ ChatGPT Work as an execution surface, never canon
→ ChatGPT Library as reference or delivery storage, never canon
→ Notion and Google Sheets only as legacy migration sources when unique unmigrated material remains
→ external references and historical discussion
```

Notion is removed from the mandatory intermediate workflow. Existing Notion data is not deleted. It becomes `LEGACY_READ_ONLY_MIGRATION_SOURCE` until unique material is classified and migrated.

## 3. Goals

1. Eliminate mandatory Notion authoring, attachment upload and readback from new work.
2. Keep one versioned project authority in the repository.
3. Preserve a readable human review product through milestone PDF exports.
4. Give Codex deterministic exact-commit planning, asset and implementation inputs.
5. Preserve approved visuals with repository path, consumer, approval state and SHA-256 provenance.
6. Avoid losing unique material from existing Notion or legacy Sheets.
7. Keep additional monetary cost at zero by default.

## 4. Non-goals

- deleting existing Notion pages or databases;
- migrating every project in this Base PR;
- treating ChatGPT conversation history, project memory or Library as canonical version control;
- storing unnecessary large production-source binaries in Git;
- changing game-specific mechanics, balance, story, art direction or implementation;
- claiming that a generated PDF, static test or manifest proves runtime or UX quality.

## 5. Authority surfaces

### 5.1 Repository canonical bundle

Each project should expose these responsibilities, whether implemented as these exact files or mapped equivalents:

```text
AGENTS.md
START_HERE.md
ACTIVE_CONTEXT.md
CURRENT_CONFIRMED_DECISIONS.md
docs/canon/AI_GAME_SPEC.md
docs/handoffs/CURRENT_CODEX_HANDOFF.md
assets/ASSET_MANIFEST.json
docs/exports/HUMAN_GDD_<milestone>_<source-sha>.pdf
```

The AI specification must describe player outcome, meaningful choices, systems, content, UX/UI flow, data semantics, actual asset consumers, implementation constraints, acceptance criteria, evidence ceiling and explicit non-scope.

### 5.2 Human GDD PDF

`HUMAN_GDD_PDF_DERIVED_VIEW` is a generated review artifact, not a second editable canon. Every export records:

- project identity;
- milestone or review gate;
- exact source commit;
- canon version;
- generated timestamp;
- included scope;
- approval status;
- implementation and evidence ceiling;
- unresolved decisions and blockers.

User feedback from a PDF review is written back into repository canon before another export is considered current.

Recommended export gates:

1. core direction and core-system approval;
2. pre-Codex implementation handoff;
3. meaningful Slice or Vertical Slice completion;
4. release-candidate review.

### 5.3 ChatGPT Work and Library

- `CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON`: Work may read, edit and generate project files, but completion requires repository persistence and readback.
- `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`: Library may preserve candidates, source references and generated PDFs. It must not be the only location for current implementation inputs or decisions.
- conversation memory and project memory are discovery aids only.

### 5.4 Approved visual delivery

A visual becomes implementation-ready only when the repository can identify it without a Notion attachment:

```text
asset_id
repository_path
actual_consumer
approval_status
version
sha256
source_or_provenance
rights_or_license_state
implementation_status
supersedes_or_replaced_by
```

The tracked runtime asset must be readable at the recorded path and its SHA-256 must match the manifest. Large editable masters may remain in local source storage or Library when they are not runtime inputs, but the manifest must identify the durable source boundary without exposing private data.

## 6. GPT–Codex handoff

The default handoff becomes:

```text
GPT Work planning / research / adversarial review
→ repository canon update and readback
→ required visual/audio inputs stored or explicitly blocked
→ exact source commit recorded
→ Codex fresh-reads repository canon and actual project files at that commit
→ Godot product implementation and machine/runtime evidence
→ GPT final review
→ repository canon and evidence update
→ optional human GDD PDF export at the gate
```

Codex must not be blocked solely because a Notion page, attachment or readback is absent. A missing implementation asset is reported as `GPT_VISUAL_REQUEST`, but fulfilment is repository path + manifest readback, not Notion upload.

## 7. Legacy migration

Existing Notion and Sheets follow a one-time compatibility workflow:

```text
inventory legacy source
→ classify each material set as UNIQUE | DUPLICATE | OBSOLETE | BLOCKED_UNVERIFIED
→ migrate UNIQUE material to repository canon, tracked asset storage or non-canonical Library reference storage
→ preserve provenance
→ read back the destination
→ identify active consumers
→ set source to LEGACY_READ_ONLY
```

A project may claim Notion retirement only when:

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

If access or provenance is unavailable, the item remains `BLOCKED_UNVERIFIED`; it is not silently treated as duplicate or obsolete.

## 8. Compatibility and precedence

Historical Notion-first plans, cases and tests may remain for rollback and migration evidence. The current owner is the repository-first contract linked from root `AGENTS.md`.

The following tokens remain discoverable only as compatibility or historical identifiers and must not restore mandatory Notion work:

- `NOTION_DEFAULT_PROJECT_WORKSPACE`
- `NOTION_HUMAN_FACING_CANON`
- `CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION`
- `CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY`
- `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`

When an older lower-priority document conflicts with this design and the current machine contract, the repository-first owner wins unless a project-specific latest user decision explicitly preserves Notion.

## 9. Concurrency boundary

Pre-existing open PRs remain read-only. In particular, PR #660 continues to own its existing planning-surface reconciliation diff and is not edited, rebased, closed, merged or absorbed by this work. This change starts from completed main and adds a superseding owner rather than rewriting that PR.

## 10. Validation

The implementation must provide a focused contract test that verifies:

- repository primary canon and derived PDF semantics;
- Work and Library non-canon boundaries;
- Notion new-write prohibition and legacy migration states;
- exact-commit Codex rehydration;
- repository asset path + SHA-256 handoff;
- root routing to the new owner;
- legacy Notion tokens cannot override the new default.

The full Base validation and required GitHub `ci-gate` remain authoritative. Static policy success does not prove any individual project has completed migration.

## 11. Rollback

Rollback this transition as one unit by reverting:

- the repository-first machine contract;
- repository-first workflow policy and templates;
- root routing changes;
- focused regression test.

Existing Notion content is not deleted by this change, so rollback does not require reconstructing migrated pages. Any project material migrated later must retain its own provenance and rollback record.
