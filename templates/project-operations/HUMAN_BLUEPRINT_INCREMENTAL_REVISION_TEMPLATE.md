# Human Blueprint Incremental Revision Receipt

```text
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

Use this receipt inside the existing two-artifact Blueprint generation workflow. It is generation metadata and verification evidence, not a third project deliverable or a parallel canon.

## 1. Revision identity

```yaml
project:
blueprint_scope:
revision_mode: INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS | INITIAL_CREATION_NO_VALID_PREDECESSOR | PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED
publication_status: READY | BLOCKED_UNVERIFIED
successor_source_branch:
successor_source_commit:
work_status_snapshot_at:

predecessor_blueprint_ref:
predecessor_source_branch:
predecessor_source_commit:
predecessor_generated_at:
predecessor_scope:
predecessor_approval_status:
predecessor_evidence_ceiling:
```

- Use `INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS` whenever a valid prior Blueprint exists.
- Use `INITIAL_CREATION_NO_VALID_PREDECESSOR` only after repository, PDF/export, Library, and applicable legacy searches find no valid predecessor.
- Use `PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED` when a predecessor is known but cannot be read reliably. This mode cannot publish a successor.

## 2. Source readback

| Source | Exact locator | Read result | Authority/role | Unique information or conflict |
|---|---|---|---|---|
| latest valid human Blueprint PDF |  | PASS / PARTIAL / FAIL | predecessor human snapshot |  |
| predecessor generation source |  | PASS / PARTIAL / FAIL | editable predecessor source |  |
| AI production specification |  | PASS / PARTIAL / FAIL | active planning/implementation specification |  |
| confirmed decisions |  | PASS / PARTIAL / FAIL | decision owner |  |
| Active Context / handoff |  | PASS / PARTIAL / FAIL | current execution state |  |
| actual code/data/scenes/resources |  | PASS / PARTIAL / FAIL | runtime implementation truth |  |
| automated/runtime/UX evidence |  | PASS / PARTIAL / FAIL | verification truth |  |
| Library/legacy unique material |  | PASS / N/A / FAIL | migration input only |  |

### Predecessor search evidence

Required only for `INITIAL_CREATION_NO_VALID_PREDECESSOR`.

```yaml
predecessor_search_evidence:
  - repository search:
  - exported PDF search:
  - Library search:
  - applicable legacy search:
```

### Predecessor access blockers

Required for `PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED`.

```yaml
predecessor_access_blockers:
  - missing or unreadable locator:
  - affected IDs or sections:
  - safe bounded work still possible:
  - recovery route:
```

## 3. Predecessor inventory

`PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY`

```yaml
predecessor_inventory:
  stable_ids: []
  section_ids: []
  diagram_ids: []
  approved_asset_ids: []
  consumer_refs: []
  evidence_refs: []
  status_facts: {}
```

Inventory must cover the valid predecessor's material content, including:

- goal, system, case, content, screen, UX, asset, audio, data, QA, decision, and work-item IDs;
- section anchors, flow/system/content cards, tables, and cross-references;
- confirmed rules, values, exceptions, terminology, non-goals, and unresolved decisions;
- text-native diagram sources and rendered diagrams;
- approved images, captions, provenance, state families, paths, and consumers;
- scene/node/script/data/resource ownership and public boundaries;
- automated-test, runtime, visual, play, UX, and user-approval evidence;
- blockers, resume conditions, next safe action, known risks, and N/A reasons.

## 4. Touched scope and preservation

```yaml
touched_scope:
  add: []
  modify: []
  remove_or_replace: []
  status_revalidate: []
protected_untouched_scope: []
carry_forward_summary: []
```

`STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION`

- Modify the predecessor source rather than rebuilding a blank document.
- Preserve untouched IDs, sections, explanations, diagrams, approved assets, consumers, and evidence.
- Layout cleanup or shorter wording is not a valid reason to remove project meaning.
- Record predecessor-to-successor mappings for every rename, split, or merge.
- Retain the predecessor PDF until the successor passes publication and readback.

## 5. Integrated Blueprint progress projection

Use the same validated repository source for the PDF views:

- [ ] `PROJECT_GOAL_STATUS_SUMMARY`
- [ ] `GOAL_LEVEL_CHECKLIST`
- [ ] `SYSTEM_LEVEL_CHECKLIST`
- [ ] `CASE_LEVEL_STATUS_MATRIX`
- [ ] `BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION`

Traceability check:

```text
Goal → System → Case → Work Item → Evidence
```

Evidence dimensions remain separate:

```text
DOCUMENTED
IMPLEMENTED
AUTOMATED_TEST_PASS
RUNTIME_VERIFIED
UX_VERIFIED
USER_APPROVED
```

- [ ] PASS/DONE only counts complete.
- [ ] N/A items include a reason and are excluded from the denominator.
- [ ] Existing PASS/DONE/runtime/UX/user-approval facts are preserved or explicitly downgraded with counterevidence.
- [ ] PDF status snapshot matches the current repository receipt and exact source SHA.

## 6. Semantic delta

`SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED`

```yaml
semantic_delta_summary:
  - CARRIED_FORWARD_UNCHANGED:
  - ADDED:
  - MODIFIED:
  - RENAMED_OR_MAPPED:
  - REMOVED_OR_REPLACED:
  - STATUS_DOWNGRADED:
```

For each material delta:

| ID or change key | Before | After | Reason/source | Consumer impact | Verification impact | Replacement/rollback |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 7. Removal or downgrade justifications

`UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN`

Leave the array empty only when no detected predecessor item or protected status is removed or downgraded.

```json
{
  "removal_or_downgrade_justifications": [
    {
      "change_key": "stable_ids:SYS-OLD",
      "change_type": "REMOVED | REPLACED | RENAMED | STATUS_DOWNGRADE",
      "reason": "Exact current reason",
      "replacement_refs": ["SYS-NEW"],
      "affected_consumers": ["res://path/to/consumer.tscn"],
      "verification_impact": "Exact checks that must be repeated",
      "evidence": ["DEC-...", "test/runtime locator"]
    }
  ]
}
```

## 8. Successor inventory

```yaml
successor_inventory:
  stable_ids: []
  section_ids: []
  diagram_ids: []
  approved_asset_ids: []
  consumer_refs: []
  evidence_refs: []
  status_facts: {}
```

The successor inventory must include all current Goal, System, Case, and Work Item IDs, their actual consumers and evidence, and their current checklist/maturity/work/verification statuses.

## 9. Machine gate

```bash
python tools/human_blueprint_incremental_publication.py \
  --input <projection-and-revision.json> \
  --expected-source-sha <fresh-read-40-character-source-sha> \
  --render-markdown
```

```yaml
progress_projection_validation: PASS | FAIL
revision_inventory_validation: PASS | FAIL
BLUEPRINT_LOSS_REGRESSION_GATE: PASS | FAIL
validator_target_sha:
validator_output_locator:
```

A failed command blocks successor publication. Do not edit the generated Markdown/PDF status by hand to bypass it.

## 10. Physical PDF comparison

The machine receipt cannot see every visible PDF regression. Inspect the actual document.

- [ ] predecessor and successor text were extracted and compared by stable ID/section anchor;
- [ ] every successor page was rendered and inspected;
- [ ] no clipped table, missing paragraph, blank page, broken glyph, or illegible label exists;
- [ ] diagrams retain their source ID and intended meaning;
- [ ] approved images retain caption, provenance, path, consumer, and status metadata;
- [ ] internal links and cross-references resolve;
- [ ] PDF and AI Markdown source SHA, IDs, semantic delta, and evidence ceiling agree;
- [ ] existing implementation/runtime/UX/user-approval evidence was not demoted by template migration;
- [ ] the predecessor remains recoverable until final publication/readback passes.

## 11. Completion receipt

```yaml
revision_mode:
predecessor_blueprint_ref:
predecessor_source_commit:
successor_source_commit:
semantic_delta_summary:
removal_or_downgrade_justifications:
carry_forward_summary:
progress_projection_validation:
revision_inventory_validation:
pdf_text_comparison:
pdf_page_render_inspection:
pdf_ai_spec_cross_check:
BLUEPRINT_LOSS_REGRESSION_GATE:
publication_status:
remaining_blockers:
rollback:
```

Publication is permitted only when all required validation and physical readback fields are PASS and `remaining_blockers` is empty. Document PASS does not imply runtime, UX, user-approval, or release PASS.