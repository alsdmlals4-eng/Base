# Human Blueprint Incremental Revision Contract

## 0. Status and purpose

```text
HUMAN_BLUEPRINT_INCREMENTAL_REVISION_CONTRACT
EXISTING_BLUEPRINT_INCREMENTAL_REVISION_REQUIRED
NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS
PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY
STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION
SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED
UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN
BLUEPRINT_LOSS_REGRESSION_GATE
PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED
INITIAL_CREATION_NO_VALID_PREDECESSOR
```

This contract extends, but does not replace, the two-artifact Master GDD policy and the human Blueprint progress-projection contract.

Its purpose is to prevent a newly generated human Blueprint PDF from becoming shorter, less accurate, less traceable, or less verified merely because the document was regenerated. A valid existing Blueprint is a predecessor revision, not disposable reference material.

The authority boundary remains:

```text
repository canon + AI production specification + actual implementation/evidence
→ validated progress and revision receipts
→ one derived HUMAN_MASTER_GDD_PDF
```

The PDF remains a derived human review snapshot. It is not a writable PM database or project canon.

## 1. Artifact boundary

The following existing rules remain mandatory:

```text
EXACTLY_TWO_DELIVERABLES
NO_SEPARATE_BLUEPRINT_ARTIFACT
NO_SEPARATE_PM_PDF_OR_HTML
NO_PARALLEL_BLUEPRINT_STATUS_CANON
NO_MASS_BLUEPRINT_BACKFILL
RUNTIME_TRUTH_SEPARATE
```

The project still publishes only:

1. the human Master GDD / Blueprint PDF; and
2. the repository-owned AI production specification Markdown.

A predecessor inventory, semantic-delta receipt, validator output, or PM projection is part of the generation and verification process. It is not a third project deliverable or another truth source.

## 2. When incremental revision is required

Use `INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS` when any valid human Blueprint revision exists for the project or approved scope.

A valid predecessor set normally includes:

1. the latest valid human Blueprint PDF;
2. the exact source branch and commit used to generate it;
3. the source document or generator input, when present;
4. `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` or the project-specific equivalent;
5. current confirmed decisions, Active Context, and handoff records;
6. actual code, data, scenes, resources, assets, tests, and runtime or UX evidence;
7. unique unmigrated Library or legacy material only when repository owners do not yet contain it.

Do not select a predecessor from filename or recency alone. Confirm its source revision, scope, status, and relationship to current project authority.

`NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS`: once a valid predecessor exists, the successor must be produced by modifying and extending that predecessor's source and stable structure. Reconstructing the whole document from a blank template, chat memory, a summary, or partial snippets is prohibited.

## 3. Predecessor inventory

`PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY`

Before editing, inventory the predecessor and current repository owners. At minimum record:

- predecessor Blueprint locator, source branch, source commit, generated time, scope, approval status, and evidence ceiling;
- project, goal, system, content, screen, UX, asset, audio, data, QA, decision, case, and work-item IDs;
- table-of-contents entries, section anchors, reusable flow/system/content cards, and cross-references;
- confirmed rules, values, exceptions, terminology, glossary entries, non-goals, and unresolved decisions;
- text-native flow, state, sequence, system, and data-diagram sources;
- approved visuals, captions, provenance, state families, repository paths, and actual consumers;
- implementation owners, scene/node/script/data/resource paths, public boundaries, and migration rules;
- automated-test, runtime, visual, play, UX, and user-approval evidence;
- blockers, resume conditions, next safe actions, known risks, and `N/A` reasons;
- the current goal/system/case/work projection snapshot used by the human PDF.

The inventory may be machine-readable JSON embedded in or adjacent to the existing generation source. It must remain within the existing two-artifact workflow and must not become a parallel product canon.

## 4. Preservation default

`STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION`

Everything outside the explicitly touched scope is carried forward by default. Preserve:

- stable IDs and predecessor-to-successor mappings;
- confirmed decisions and player-facing meanings;
- detailed explanations, rules, numeric values, constraints, exceptions, and terminology;
- section anchors, cards, tables, traceability, and internal links;
- editable text-native diagram sources and their rendered forms;
- approved visuals, captions, provenance, consumers, and implementation states;
- actual repository paths and public interfaces;
- test, runtime, UX, and user-approval evidence and their exact evidence ceilings;
- blockers, remaining work, rollback routes, and historical semantic deltas.

Layout cleanup, shortening, visual redesign, page-count reduction, or a new template is not sufficient reason to delete meaningful content.

A rename, split, or merge of IDs requires an explicit predecessor-to-successor mapping. A section may move without being considered lost only when its stable ID or exact replacement remains traceable.

## 5. Integrated PM and Blueprint progress

The human Blueprint continues to include the validated views from `HUMAN_BLUEPRINT_PROGRESS_PROJECTION_CONTRACT.md`:

```text
PROJECT_GOAL_STATUS_SUMMARY
GOAL_LEVEL_CHECKLIST
SYSTEM_LEVEL_CHECKLIST
CASE_LEVEL_STATUS_MATRIX
BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION
```

These views are regenerated from the current Goal/Issue, Active Context, `project_work_kanban`, AI production specification, actual consumers, and evidence. They are not manually edited inside the PDF.

The evidence dimensions remain separate:

```text
DOCUMENTED
IMPLEMENTED
AUTOMATED_TEST_PASS
RUNTIME_VERIFIED
UX_VERIFIED
USER_APPROVED
```

The predecessor progress snapshot is compared with the successor. Existing PASS/DONE/runtime/UX/user-approval facts may not disappear or be demoted without explicit counterevidence and a recorded verification impact.

## 6. Semantic delta

`SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED`

Each successor records:

```yaml
revision_mode:
publication_status:
predecessor_blueprint_ref:
predecessor_source_commit:
predecessor_inventory:
successor_inventory:
predecessor_search_evidence:
semantic_delta_summary:
removal_or_downgrade_justifications:
predecessor_access_blockers:
```

For each material change, record:

| Change | Required record |
|---|---|
| Added | new ID, source, reason, owner, consumer, and required evidence |
| Modified | predecessor value, successor value, reason, affected IDs/consumers, and revalidation impact |
| Renamed | predecessor ID, successor ID, migration mapping, reason, evidence |
| Split or merged | all predecessor/successor IDs, ownership change, migration and rollback impact |
| Removed | exact item, reason, replacement or supersession when applicable, affected consumers, evidence |
| Status downgraded | counterevidence or stale-evidence reason, affected acceptance, and revalidation plan |
| Carried forward | `CARRIED_FORWARD_UNCHANGED` plus preserved source locator or inventory coverage |

A removal or downgrade justification uses:

```json
{
  "change_key": "stable_ids:SYS-LEGACY",
  "change_type": "REMOVED | REPLACED | RENAMED | STATUS_DOWNGRADE",
  "reason": "Why this change is correct now",
  "replacement_refs": ["SYS-CURRENT"],
  "affected_consumers": ["res://path/to/consumer.tscn"],
  "verification_impact": "What must be rechecked",
  "evidence": ["DEC-...", "test or runtime locator"]
}
```

`UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN`: a missing ID, section, diagram, approved asset, consumer, evidence locator, or status fact without a matching justification is a publication failure, not editorial cleanup.

## 7. Machine validation

The combined publication command is:

```bash
python tools/human_blueprint_incremental_publication.py \
  --input <projection-and-revision.json> \
  --expected-source-sha <fresh-read-40-character-source-sha> \
  --render-markdown
```

The command first runs the existing human Blueprint progress validator, then validates the predecessor/successor revision receipt. The renderer emits the semantic delta and loss-regression result before the progress view.

The machine inventory gate verifies at least:

1. every current Goal, System, Case, and Work Item appears in the successor stable-ID inventory;
2. actual consumers and evidence locators in the current projection appear in the successor inventory;
3. current checklist, maturity, work, and verification statuses match the successor status facts;
4. predecessor inventory items that disappear have explicit justification;
5. PASS/DONE and maturity evidence does not silently regress;
6. incremental, initial, and blocked modes satisfy their distinct requirements.

The tool validates declared facts. It does not prove that every PDF page visibly contains them. Physical PDF validation remains required.

## 8. PDF loss-regression inspection

`BLUEPRINT_LOSS_REGRESSION_GATE`

Before promoting the successor PDF:

1. compare predecessor and successor inventory results;
2. compare extracted PDF text by stable ID and required section anchor;
3. render every successor page and inspect for clipping, blank pages, broken glyphs, illegible tables, missing images, and broken captions;
4. compare diagrams and approved images with their source IDs, captions, provenance, and consumer metadata;
5. confirm the AI Markdown and PDF use the same source commit, IDs, semantic delta, and evidence ceiling;
6. confirm no existing implementation/runtime/UX/user-approval evidence was demoted solely because the template or Base policy changed;
7. retain the predecessor file until successor publication and readback pass.

A successful document render alone is not a loss-regression PASS. Both machine inventory validation and page/text readback are required.

## 9. Initial creation

`INITIAL_CREATION_NO_VALID_PREDECESSOR` is permitted only when no valid predecessor exists.

The receipt must contain nonempty `predecessor_search_evidence` showing that the repository, known exported PDFs, Library, and applicable legacy sources were searched. The predecessor locator and source commit must be empty, and the predecessor inventory must be empty.

Once the first valid Blueprint is published, every later publication uses it as a predecessor unless a documented supersession identifies another valid lineage.

## 10. Unavailable predecessor

`PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED`

When a predecessor is known to exist but its PDF, source revision, embedded visual, or AI specification cannot be read reliably:

- do not recreate missing facts from memory, chat history, or inference;
- record the known predecessor locator and concrete access blockers;
- limit any safe work to unaffected, explicitly bounded sections;
- keep publication status `BLOCKED_UNVERIFIED`;
- preserve the last valid predecessor as the current human snapshot.

The validator deliberately returns failure for this mode. It is a truthful blocker receipt, not a publication route.

## 11. Completion criteria

A successor may be presented as the current Blueprint revision only when:

- the valid predecessor and source revision were fresh-read;
- the revision mode is correct;
- the predecessor and successor inventories are complete for the touched scope;
- goal/system/case/work progress is reconciled with repository owners and evidence;
- every removal, replacement, rename, or downgrade is explicitly justified;
- the combined validator passes against a caller-provided fresh source SHA;
- PDF text extraction, page rendering, images, captions, links, and glyphs pass readback;
- PDF and AI Markdown IDs, source SHA, semantic delta, and evidence ceiling agree;
- existing two-artifact, image, runtime-truth, and approval boundaries still pass regression tests;
- the predecessor is retained until successor publication and repository readback succeed.

Document PASS is distinct from runtime PASS, UX PASS, user approval, and release PASS.