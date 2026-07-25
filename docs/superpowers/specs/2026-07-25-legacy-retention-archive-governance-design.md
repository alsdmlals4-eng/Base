# Legacy Retention and Archive Governance Skill Design

- Date: 2026-07-25
- Status: DESIGN_APPROVED_PENDING_USER_SPEC_REVIEW
- Source repository: `alsdmlals4-eng/Base`
- Target repositories:
  - `alsdmlals4-eng/Base`
  - `alsdmlals4-eng/omenward`
  - `alsdmlals4-eng/urban-legend`
  - `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
  - `alsdmlals4-eng/Blacksmith`

## 1. Problem

Projects accumulate superseded design documents, inactive Skill packages, generated publications, old implementation plans, evidence artifacts and merged branches. Treating all old material as active creates stale-reference risk and cold-start confusion. Deleting it or emptying files destroys decision provenance, rollback evidence and compatibility context.

The repositories need one reusable judgment contract that separates current authority from historical retention without copying the same policy into every project.

## 2. Goals

1. Preserve unique decisions, evidence, exceptions, approved assets and compatibility information.
2. Remove superseded material from active discovery, routing and implementation authority.
3. Prohibit blank placeholder files as a retirement technique.
4. Distinguish document archival, inactive Skill compatibility and Git branch retention.
5. Make every archive decision traceable through metadata and a manifest.
6. Let projects adopt the Base policy through Registry routes and path adapters rather than copied Skill bodies.
7. Keep project-specific canon and path decisions inside each project.

## 3. Non-goals

- Automatically moving every old file.
- Automatically deleting branches, files, tags or generated artifacts.
- Replacing Git history with repository archive folders.
- Archiving secrets, credentials, private keys or regulated data.
- Treating `old`, `v2`, `final` or a date suffix as sufficient evidence of obsolescence.
- Changing project product canon, game data or implementation behavior.

## 4. Recommended architecture

### 4.1 Base shared Skill

Create one Foundation Skill:

```text
skill_id: governing-legacy-retention-and-archives
path: skills/governing-legacy-retention-and-archives/SKILL.md
layer: foundation
load_by_default: false
```

Discovery triggers include:

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

The Skill owns the judgment boundary for preserving historical material while removing active authority. It does not own project-specific canon selection or destructive cleanup execution.

### 4.2 Responsibility boundaries

| Concern | Responsible Skill |
|---|---|
| Operating-system inventory, migration and legacy reconciliation | `managing-game-project-operating-system` |
| Decide KEEP, MERGE, ARCHIVE, STUB or DELETE candidates without capability loss | `pruning-stale-and-nonfunctional-material` |
| Define retention class, archive metadata, active-authority removal, branch/tag preservation and archive verification | `governing-legacy-retention-and-archives` |
| Verify paths, IDs, schemas and active references after change | `auditing-canonical-reference-freshness` |
| Review evidence and completion claims | `reviewing-and-validating-project-changes` |

The new Skill is selected when the question is not merely “is this stale?” but “how must it be retained, isolated and proven non-authoritative?”

### 4.3 Project adoption

Projects do not copy the Base Skill body. Each project adds a Registry route or shared-skill mapping and a small path adapter describing:

- active canon roots;
- archive root;
- archive manifest path;
- inactive Skill compatibility policy;
- generated-publication retention path;
- protected evidence and asset roots;
- branch/tag retention policy;
- project validation commands.

## 5. Retention classifications

Every candidate receives exactly one primary classification.

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

### 5.1 Meaning

- `CURRENT_AUTHORITY`: active responsibility source; must not be placed under archive roots.
- `COMPATIBILITY_ONLY`: retained for old IDs, paths or consumers but excluded from normal routing.
- `ARCHIVE_HISTORY`: superseded human-readable material retained with original content.
- `EVIDENCE_RETENTION`: test logs, captures, audit results or approval evidence retained without implementation authority.
- `GENERATED_DERIVATIVE`: PDF, DOCX, diagram or export whose source and generation status are recorded.
- `DELETE_PROHIBITED_SECRET`: must not be archived; revoke and remove through security procedure.
- `DELETE_APPROVED`: deletion allowed only with approval, reference verification and rollback evidence.
- `KEEP_UNRESOLVED`: authority or uniqueness is uncertain; no movement or deletion.

## 6. Archive content contract

### 6.1 Original content preservation

Archived documents retain their original body. The migration may add a metadata header but must not rewrite history to resemble the current canon.

Blanking content is prohibited because it preserves the path while destroying provenance.

### 6.2 Metadata header

Each archived document must declare or be represented by equivalent manifest data:

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

No field may contain an unresolved placeholder in an approved migration. Unknown values use explicit `UNKNOWN` with a blocking note.

### 6.3 Archive manifest

Each project maintains one machine-readable manifest, recommended path:

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

The manifest is an index, not a replacement for Git history.

### 6.4 Archive README

`docs/archive/README.md` explains:

- archive material is not current canon;
- how to find the current replacement;
- how to add or restore an item;
- why blank files are forbidden;
- which content must never be archived.

## 7. Content-type policies

### 7.1 Design and planning documents

- Move superseded originals to a categorized archive root.
- Preserve the original body.
- Add metadata and manifest record.
- Update active references to the current source.
- Do not let archive files appear in current-canon registries or default cold-start reading.

### 7.2 Legacy Skills

Legacy Skill packages use inactive compatibility retention when old IDs or records still matter.

```text
status: inactive or BACKUP-compatible project value
routable: false
load_by_default: false
replaced_by: active-skill-id
```

Physical movement to an archive folder is optional and only allowed if the Router, Registry, aliases and tests are updated together. Project validators must prove inactive packages cannot be selected directly.

### 7.3 Tests and evidence

Tests must not be removed merely to hide failure or reduce maintenance. Obsolete test evidence is retained under an evidence archive when it documents an approved claim, prior defect or migration result. Executable tests that no longer describe current behavior are either migrated, explicitly retired with rationale, or kept unresolved.

### 7.4 Generated publications

Generated PDF, DOCX and diagrams must declare source, generator, input hash or source commit, and freshness status. Stale derivatives are archived or regenerated; they must not remain presented as current.

### 7.5 Source code and runtime assets

Do not use the active source tree as a museum for unreachable code. Preserve unique code through Git history, tags, releases or a dedicated archival repository, then remove it from active runtime paths only through an approved migration. Large binary assets follow storage-cost and license policy.

### 7.6 Secrets and sensitive data

Secrets, tokens, credentials and private keys are never archived. Revoke them, remove them from active history using the approved security process, and document the incident without reproducing the secret.

### 7.7 Git branches

A branch cannot be moved into a folder. Merged or superseded branch retention uses:

```text
unique commits audited
→ PR merged or explicitly closed
→ optional archive tag created
→ tag pushed and verified
→ branch deleted when deletion capability exists
```

Until branch deletion is available, closed PR state and an archive tag are acceptable retention evidence. Long-lived `archive/*` branches are discouraged because they pollute active branch discovery.

## 8. Project adapters

### 8.1 Base

- Add the shared Skill to `skills/SKILL_REGISTRY.json`.
- Add archive paths and metadata templates under `templates/project-operations/`.
- Add validator/test coverage for required fields and forbidden blank placeholders.
- Update operating-system and pruning Skills with required cross-references, without duplicating the new workflow.

### 8.2 Omenward

- Add the shared route to Registry v4 aliases or active Foundation mapping.
- Add project archive adapter for `docs/design`, V2 canon, inactive compatibility Skills and CI evidence.
- Preserve current V2 canon priority.
- Do not archive or rewrite product implementation because implementation remains not started.

### 8.3 Urban Legend

- Add the Base shared route to Registry v4 `support_skills` and path adapter.
- Keep project Skill bodies local only for domain-specific decisions.
- Extend active-reference tests so archive roots cannot be treated as current canon.

### 8.4 Ten Paces Hidden Moves

- Add a new `base_integration.shared_skill_routes` entry without changing Registry schema generation.
- Add project archive adapter compatible with Registry v3.
- Update governance tests to validate the route and archive metadata contract.

### 8.5 Blacksmith

- Because Registry v2 contains only project specialists, adopt the Base Skill through `BASE_ADOPTION_PROFILE.json` and operating-system documentation rather than inserting a foreign entry into the project-specialist list.
- Add a project archive adapter and audit validation.
- Do not force Registry v4 migration as part of this scope.

## 9. Routing contract

The shared Skill is not always-on.

Select it when one or more are true:

- a superseded artifact must remain recoverable;
- a backup or archive folder is proposed;
- a file is being emptied instead of retired;
- inactive Skill compatibility is being designed;
- evidence must be retained without current authority;
- a merged branch needs tag-and-delete treatment;
- archive metadata or manifests are missing or inconsistent.

Do not select it for:

- ordinary document editing;
- a current canon lookup;
- temporary build artifacts already governed by cleanup policy;
- security-secret retention;
- a simple stale-reference check that requires no retention decision.

## 10. Skill TDD design

The new Skill must be developed with RED-GREEN-REFACTOR.

### 10.1 RED baseline scenarios

Run fresh-context scenarios without the Skill and capture whether the agent:

1. empties a superseded document while keeping the path;
2. copies every old file into a generic `backup/` folder without metadata;
3. treats Git history alone as sufficient active-project documentation;
4. archives a secret instead of revoking and removing it;
5. moves inactive Skill files without updating Registry aliases and tests;
6. deletes a merged branch before auditing unique commits or creating a rollback ref;
7. leaves archive files in default cold-start reading or current-canon maps.

At least one baseline scenario must exhibit the target failure before authoring the Skill. If no scenario fails, narrow or cancel the Skill rather than manufacturing guidance.

### 10.2 GREEN requirements

With the Skill loaded, the same scenarios must produce:

- explicit classification;
- preserved original content;
- active-authority removal;
- metadata and manifest requirements;
- project-specific adapter use;
- no secret archival;
- no destructive action without approval and rollback evidence;
- validation steps for references, routing and cold start.

### 10.3 REFACTOR pressure tests

Add time pressure, user pressure to “just clear the file,” large file counts and mixed project versions. Capture rationalizations and close only observed loopholes.

## 11. Automated validation

Base should provide reusable checks or templates for projects to adapt.

Minimum invariants:

1. archived Markdown is non-empty beyond metadata;
2. `active_authority` is `false` for archive records;
3. every `superseded_by` path exists or is explicitly external;
4. every moved item has a rollback ref and hash;
5. inactive Skills are not directly routable;
6. current registries and default start documents do not point to archive material as current;
7. archive manifest paths are unique;
8. secret patterns are blocked from archive commits;
9. generated derivatives declare source and freshness;
10. project adapters match the project Registry generation.

Validation reports use `PASS / PARTIAL / FAIL / NOT_RUN` and must not equate file existence with successful enforcement.

## 12. Rollout sequence

Implementation is split into five separate PRs to isolate project risk.

1. Base PR: Skill, templates, tests and cross-references.
2. Omenward PR: Registry v4 route, adapter and validation.
3. Urban Legend PR: Registry v4 route, adapter and active-reference tests.
4. Ten Paces PR: Registry v3 route, adapter and governance tests.
5. Blacksmith PR: adoption profile, adapter and audit validation.

Each project PR pins the exact merged Base commit. A project PR does not merge before its project-specific validation succeeds.

## 13. Completion criteria

- Base shared Skill exists and passes its pressure scenarios and automated tests.
- Base Registry and related Skills describe non-overlapping responsibilities.
- All four project repositories adopt the merged Base commit explicitly.
- Each project has an archive adapter and machine-readable manifest contract.
- Existing current canon remains authoritative and unchanged except for routing/adoption metadata.
- No file is emptied as a retirement action.
- No secret is archived.
- No destructive migration or branch deletion is performed in this rollout.
- Each repository has independent CI or local validation evidence.

## 14. Deferred work

- Bulk migration of existing legacy files.
- Archive tag creation and remote branch deletion.
- Repository history rewriting.
- Large-binary archival storage design.
- Cross-repository automated Base update bots.
