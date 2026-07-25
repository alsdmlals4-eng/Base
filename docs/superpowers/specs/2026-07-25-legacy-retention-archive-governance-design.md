# Legacy Retention and Archive Governance Skill Design

- Date: 2026-07-25
- Status: `DESIGN_APPROVED_PENDING_USER_SPEC_REVIEW`
- Source repository: `alsdmlals4-eng/Base`
- Target repositories:
  - `alsdmlals4-eng/Base`
  - `alsdmlals4-eng/omenward`
  - `alsdmlals4-eng/urban-legend`
  - `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
  - `alsdmlals4-eng/Blacksmith`

## 1. Problem

Projects accumulate superseded design documents, inactive Skill packages, generated publications, old implementation plans, evidence artifacts and merged branches. Treating all old material as active creates stale-reference risk and cold-start confusion. Deleting it or emptying files destroys decision provenance, rollback evidence and compatibility context.

The repositories need one reusable judgment contract that separates current authority from historical retention without copying the same policy body into every project.

## 2. Goals

1. Preserve unique decisions, evidence, exceptions, approved assets and compatibility information.
2. Remove superseded material from active discovery, routing and implementation authority.
3. Prohibit blank placeholder files as a retirement technique.
4. Distinguish document archival, inactive Skill compatibility and Git branch retention.
5. Make each archive decision traceable through metadata and a manifest.
6. Let projects adopt a pinned Base policy through routes and path adapters.
7. Keep project-specific canon and path decisions inside each project.

## 3. Non-goals

- Bulk-moving existing legacy files in this rollout.
- Automatically deleting branches, files, tags or generated artifacts.
- Replacing Git history with repository archive folders.
- Archiving secrets, credentials, private keys or regulated data.
- Treating `old`, `v2`, `final` or a date suffix as sufficient evidence of obsolescence.
- Migrating project Registry generations.
- Changing product canon, game data or implementation behavior.

## 4. Architecture

### 4.1 Base shared Skill

Create one Foundation Skill:

```text
skill_id: governing-legacy-retention-and-archives
path: skills/governing-legacy-retention-and-archives/SKILL.md
layer: foundation
load_by_default: false
```

Discovery triggers:

```text
legacy-retention
archive-policy
superseded-document
obsolete-plan
inactive-skill
backup-folder
blank-placeholder
branch-retention
archive-manifest
historical-evidence
```

The Skill owns the judgment boundary for preserving historical material while removing active authority. It does not choose project canon and does not authorize destructive cleanup by itself.

### 4.2 Responsibility boundaries

| Concern | Responsible Skill |
|---|---|
| Operating-system inventory, migration and reconciliation execution | `managing-game-project-operating-system` |
| Determine whether material is stale or nonfunctional without losing capabilities | `pruning-stale-and-nonfunctional-material` |
| Define retention class, archive metadata, authority removal, branch/tag retention and archive verification | `governing-legacy-retention-and-archives` |
| Verify paths, IDs, schemas and active references after change | `auditing-canonical-reference-freshness` |
| Review evidence and completion claims | `reviewing-and-validating-project-changes` |

Select the new Skill when the question is not merely “is this stale?” but “how must it remain recoverable while being proven non-authoritative?”

### 4.3 Adoption model

The Base `SKILL.md` is the single method source. Projects use one of three explicit adapter forms according to their current Registry generation.

```text
Base Skill body
→ pinned Base commit
→ project route or thin adapter
→ project archive-path adapter
→ project validator
```

A project adapter declares:

- active canon roots;
- archive root and manifest path;
- inactive Skill compatibility policy;
- generated-publication retention path;
- protected evidence and asset roots;
- branch/tag retention policy;
- project validation commands.

Projects must not copy the full Base workflow into local Skill bodies.

## 5. Retention classifications

Each candidate receives exactly one primary classification.

```text
CURRENT_AUTHORITY
COMPATIBILITY_ONLY
ARCHIVE_HISTORY
EVIDENCE_RETENTION
GENERATED_DERIVATIVE
DELETE_PROHIBITED_SECRET
DELETE_APPROVED
KEEP_UNRESOLVED
```

- `CURRENT_AUTHORITY`: active responsibility source; never placed under archive roots.
- `COMPATIBILITY_ONLY`: retained for old IDs, paths or consumers but excluded from normal routing.
- `ARCHIVE_HISTORY`: superseded human-readable material retained with its original body.
- `EVIDENCE_RETENTION`: logs, captures, audits or approval evidence without implementation authority.
- `GENERATED_DERIVATIVE`: PDF, DOCX, diagram or export with source and freshness metadata.
- `DELETE_PROHIBITED_SECRET`: never archived; revoke and remove through security procedure.
- `DELETE_APPROVED`: deletion allowed only with approval, reference verification and rollback evidence.
- `KEEP_UNRESOLVED`: authority or unique content remains uncertain; no movement or deletion.

## 6. Archive content contract

### 6.1 Original content

Archived documents retain their original body. A migration may add a metadata header but must not rewrite history to resemble current canon.

**Blanking content is prohibited.** A blank file preserves a misleading path while destroying provenance.

### 6.2 Metadata

Each archived item must declare or be represented by equivalent manifest data:

```yaml
archive_metadata:
  status: SUPERSEDED
  archived_at: YYYY-MM-DD
  original_path: path/before/archive
  archived_path: docs/archive/category/file
  superseded_by:
    - current/canonical/path
  reason: concise retirement reason
  unique_material_preserved:
    - decisions
    - evidence
  active_authority: false
  implementation_authority: NONE
  compatibility_consumers: []
  rollback_ref: commit-or-tag
```

Approved migrations contain no `TBD`, `TODO` or unresolved placeholder. Unknown values use `UNKNOWN` plus a blocking note and remain `KEEP_UNRESOLVED`.

### 6.3 Manifest

Recommended path:

```text
docs/archive/MANIFEST.json
```

Required record fields:

```text
archive_id
classification
original_path
current_path
content_sha256
archived_at
superseded_by
reason
active_authority
implementation_authority
compatibility_consumers
rollback_ref
validation_status
```

A project with no archived items still creates a valid non-placeholder manifest with `records: []`. The manifest indexes retention state; it does not replace Git history.

### 6.4 Archive README

`docs/archive/README.md` states:

- archive material is not current canon;
- how to locate the replacement;
- how to add or restore an item;
- why blank files are forbidden;
- which material must never be archived.

## 7. Content-type rules

### 7.1 Design and planning documents

- Move only after current authority and unique content are identified.
- Preserve the original body.
- Add metadata and a manifest record.
- Update active references to the current source.
- Exclude archives from current-canon registries and default cold-start reading.

### 7.2 Legacy Skills

Retain legacy Skill packages as inactive compatibility when old IDs or records still matter.

```text
status: inactive or project-equivalent BACKUP state
routable: false
load_by_default: false
replaced_by: active-skill-id
```

Physical movement is permitted only when Router, Registry, aliases and tests change together. Validators must prove inactive packages cannot route directly.

### 7.3 Tests and evidence

Tests are not removed to hide failure or reduce maintenance. Historical evidence is retained when it supports an approved claim, prior defect or migration result. Executable tests that no longer describe current behavior are migrated, explicitly retired with rationale, or kept unresolved.

### 7.4 Generated publications

PDF, DOCX and diagrams declare source, generator, input hash or source commit, and freshness status. Stale derivatives are archived or regenerated and cannot remain presented as current.

### 7.5 Source code and runtime assets

The active source tree is not an archive. Unique code is preserved through Git history, tags, releases or a dedicated archival repository before approved removal from runtime paths. Large binary assets follow storage and license policy.

### 7.6 Secrets

Secrets, tokens, credentials and private keys are never archived. Revoke them, remove them through the security procedure and document the incident without reproducing the value.

### 7.7 Git branches

Branches cannot be moved into folders.

```text
unique commits audited
→ PR merged or explicitly superseded and closed
→ optional archive tag created
→ tag pushed and verified
→ branch deleted when deletion capability exists
```

Until branch deletion is available, a closed PR plus verified archive tag is acceptable retention evidence. Long-lived `archive/*` branches are discouraged.

## 8. Project-specific adoption

### 8.1 Base

- Add the shared Skill to `skills/SKILL_REGISTRY.json`.
- Add metadata, manifest and path-adapter templates under `templates/project-operations/`.
- Add validator and test coverage for required fields, non-empty archived content and secret exclusions.
- Add required cross-references to operating-system and pruning Skills without duplicating the new workflow.

### 8.2 Omenward — Registry v4 local-path validation

Omenward cannot route directly to an external Base file because its v4 validator requires registered local package paths. It adopts the policy through a thin local Foundation adapter:

```text
id: foundation.legacy-retention
path: skills/foundation/governing-omenward-legacy-retention/SKILL.md
status: active
load_by_default: false
depends_on:
  - foundation.project-operating-system
base_method: Base@<merged-sha>/skills/governing-legacy-retention-and-archives/SKILL.md
```

The local adapter contains only:

- pinned Base source and method ID;
- Omenward canon and archive roots;
- V2 authority exclusions;
- inactive compatibility Skill rules;
- CI evidence paths and project validation commands.

It must not copy the Base workflow. Omenward active Skill accounting changes explicitly:

```text
Foundation: 7 → 8
Omenward Discipline: 4
Specialist: 1
Active total: 12 → 13
```

Registry, README, validator expectations and routing tests change in the same PR. Product code, V2 canon content and implementation state remain unchanged.

### 8.3 Urban Legend — Registry v4 Base index adoption

- Add `governing-legacy-retention-and-archives` to the pinned Base shared-skill index and relevant `support_skills` routes.
- Add `skills/ARCHIVE_RETENTION_ADAPTER.json` for project paths and validation.
- Add `docs/archive/README.md` and a valid empty manifest.
- Extend active-reference tests so archive roots cannot be resolved as current canon.
- Do not create a copied local Base Skill body.

### 8.4 Ten Paces Hidden Moves — Registry v3 shared route

- Add `legacy_retention` to `base_integration.shared_skill_routes` with the pinned Base Skill ID.
- Add a Registry-v3-compatible archive adapter.
- Add `docs/archive/README.md` and a valid empty manifest.
- Update governance tests for the shared route, metadata and current-reference exclusion.
- Do not migrate the Registry schema.

### 8.5 Blacksmith — Registry v2 adoption profile

Blacksmith Registry v2 contains project specialists only. It therefore adopts the Base method through `docs/BASE_ADOPTION_PROFILE.json`, not through the project-specialist list.

- Pin the merged Base commit and Skill ID in the adoption profile.
- Add a project archive adapter under the existing project hub.
- Add an archive README and valid empty manifest at paths selected by the adapter.
- Extend `tools/audit_project_operating_system.py` to verify adoption and retention invariants.
- Do not migrate Registry v2.

## 9. Routing contract

The shared Skill is never always-on.

Select it when:

- a superseded artifact must remain recoverable;
- a backup or archive folder is proposed;
- a file is being emptied instead of retired;
- inactive Skill compatibility is being designed;
- evidence must remain without current authority;
- a merged branch needs tag-and-delete treatment;
- archive metadata or manifests are missing or inconsistent.

Do not select it for ordinary document editing, current canon lookup, temporary build cleanup, secret retention, or a stale-reference check requiring no retention decision.

## 10. Skill TDD

The Skill follows RED-GREEN-REFACTOR.

### 10.1 RED baseline scenarios

Run fresh-context scenarios without the Skill and record whether the agent:

1. empties a superseded document while keeping its path;
2. copies all old files into generic `backup/` without metadata;
3. treats Git history alone as sufficient active-project documentation;
4. archives a secret instead of revoking and removing it;
5. moves inactive Skills without updating Registry aliases and tests;
6. deletes a branch before auditing unique commits or creating rollback evidence;
7. leaves archive files in default cold-start reading or current-canon maps.

At least one baseline scenario must demonstrate the target failure before the Skill body is authored. Otherwise narrow or cancel the new Skill.

### 10.2 GREEN requirements

With the Skill loaded, the same scenarios produce:

- an explicit classification;
- preserved original content;
- removal of active authority;
- metadata and manifest requirements;
- the correct project adapter form;
- no secret archival;
- no destructive action without approval and rollback evidence;
- reference, routing and cold-start verification.

### 10.3 REFACTOR pressure

Re-run with time pressure, instructions to “just clear the file,” large candidate counts and mixed Registry versions. Add counters only for observed rationalizations.

## 11. Automated validation

Base provides reusable checks or templates for these invariants:

1. archived Markdown is non-empty beyond metadata;
2. archive records have `active_authority: false`;
3. every `superseded_by` path exists or is explicitly external;
4. moved items have a rollback ref and content hash;
5. inactive Skills are not directly routable;
6. current registries and default start documents do not present archive material as current;
7. archive manifest paths and IDs are unique;
8. secret patterns are blocked from archive changes;
9. generated derivatives declare source and freshness;
10. project adapters match the project Registry generation.

Reports use `PASS / PARTIAL / FAIL / NOT_RUN`; file existence alone is never enforcement evidence.

## 12. Rollout

Use five independent PRs:

1. Base: Skill, templates, TDD evidence, automated tests and cross-references.
2. Omenward: thin local adapter, Registry v4 update and validation.
3. Urban Legend: Base-index route, adapter and active-reference tests.
4. Ten Paces: Registry v3 route, adapter and governance tests.
5. Blacksmith: adoption profile, adapter and audit validation.

Each project PR pins the exact merged Base commit. No project PR merges before project-specific validation succeeds.

## 13. Completion criteria

- Base shared Skill passes baseline, pressure and automated tests.
- Base Registry and related Skills have non-overlapping responsibilities.
- All four projects explicitly adopt the merged Base commit.
- Each project has a version-correct adapter, archive README and valid empty manifest.
- Existing current canon remains authoritative.
- No file is emptied as a retirement action.
- No secret is archived.
- No existing legacy content is bulk-moved or deleted in this rollout.
- No branch or tag is deleted in this rollout.
- Each repository has independent validation evidence.

## 14. Deferred work

- Classification and migration of existing legacy files.
- Archive tag creation and remote branch deletion.
- Repository history rewriting.
- Large-binary archival storage design.
- Cross-repository automatic Base update bots.
