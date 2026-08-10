# BCP-2026-014 Evidence — Urban Legend Handoff Compatibility Closeout

## Scope

```yaml
source_project: alsdmlals4-eng/urban-legend
source_pr: 187
source_handoff_file: docs/CURRENT_HANDOFF.md
source_final_head: 2b424906c4ecaa4a027719383d3400486b03c72e
base_candidate: BCP-2026-014-handoff-machine-consumer-compatibility-closeout
related_existing_proposal: BCP-2026-013-post-merge-continuation-state-reconciliation
base_active_implementation_changed_in_this_stage: false
```

이 evidence는 프로젝트의 Handoff refresh 과정에서 실제 발생한 **machine-consumer compatibility failure와 복구 lineage**를 보존한다. 제품 기능, Godot runtime, Base 활성 Skill 구현을 제안 단계의 성공으로 오인하지 않는다.

## Exact project lineage

### 1. Initial current-state compression — failure

Commit:

```text
b131bb520172e9252dc5c4e07107ccb3e82fc83e
```

목표는 과거 상태를 장문 복제하지 않고 최신 프로젝트 상태·재개 순서·차단 항목을 `docs/CURRENT_HANDOFF.md`에 압축하는 것이었다.

Exact commit workflow results:

| Workflow | Run | Result |
|---|---:|---|
| Validate Urban Legend BCA Adoption | 31351675825 | PASS |
| Validate Project Base Adapter | 31351675798 | PASS |
| Validate ANNUAL-MVP-001 | 31351675833 | FAIL |
| Validate documentation contracts | 31351675821 | FAIL |
| Validate core and documentation baseline | 31351675802 | FAIL |

Documentation-contract failure showed that active tests still consumed historical identifiers from `docs/CURRENT_HANDOFF.md`.

Observed missing compatibility tokens included:

```text
APPROVED_DESIGN_BASELINE
CORE-VALIDATION-001
UX-PD-001 2A
Ver 4.2
mvp-039
```

These tokens were not all current-state authority. In particular `Ver 4.2` could be misread as a current product version if restored into the current-state sections.

### 2. Explicit historical compatibility section — incomplete recovery

Commit:

```text
71fe4007de1dd9ab14bde0b0b19fdf8fa0535b1c
```

The first recovery separated legacy values into a `Historical Compatibility Anchors` area instead of presenting them as current truth.

Exact commit workflow results:

| Workflow | Run | Result |
|---|---:|---|
| Validate Urban Legend BCA Adoption | 31351765467 | PASS |
| Validate Project Base Adapter | 31351765457 | PASS |
| Validate ANNUAL-MVP-001 | 31351765480 | FAIL |
| Validate documentation contracts | 31351765470 | FAIL |
| Validate core and documentation baseline | 31351765469 | FAIL |

The remaining document-contract failure identified one more machine consumer requirement:

```text
POC_PASSED: NOT_DECLARED
```

This second failure is important evidence: a one-pass manual guess at “which historical strings matter” was insufficient. The safe closeout process requires actual consumer inventory and exact-head validation rather than ad-hoc token restoration.

### 3. Final compatibility-safe Handoff — recovery verified

Final exact Handoff head:

```text
2b424906c4ecaa4a027719383d3400486b03c72e
```

The final document kept current-state facts in the main sections and compatibility-only identifiers in an explicitly labeled historical section.

Exact-head workflow results:

| Workflow | Run | Result |
|---|---:|---|
| Validate documentation contracts | 31351847793 | PASS |
| Validate Urban Legend BCA Adoption | 31351847833 | PASS |
| Validate Project Base Adapter | 31351847790 | PASS |
| Validate core and documentation baseline | 31351847798 | PASS |
| Validate ANNUAL-MVP-001 | 31351847784 | PASS |

The observed recovery pattern was therefore:

```text
fresh human-readable handoff
→ machine consumer contract failure
→ identify historical consumers
→ isolate compatibility-only values
→ rerun exact-head validation
→ discover remaining consumer
→ complete compatibility inventory
→ exact-head GREEN
```

## Root-cause classification

### What failed

The failure was not that the new current-state facts were wrong. The failure was that the Handoff file had two simultaneous roles:

```text
HUMAN_CURRENT_STATE_ROUTER
+
MACHINE_CONSUMED_COMPATIBILITY_SURFACE
```

Refreshing only the first role silently broke the second.

### What did not fail

- No product runtime source was changed by the Handoff checkpoint.
- The route minigame/runtime blocker was unrelated to these document-contract failures.
- The Base active Handoff Skill was not modified.
- The project did not need a new broad Handoff Skill.
- Historical tokens did not need to be promoted back into current authority.

## Existing Base coverage

### `maintaining-project-context-and-handoff`

Already owns:

- current runtime/repository truth first;
- context refresh;
- session handoff;
- resume read order;
- stale handoff correction;
- compact current-state routing.

### `auditing-canonical-reference-freshness`

Already owns:

- impact mapping;
- stale/orphan references;
- untouched consumer detection;
- `LEGACY_REFERENCE_ALLOWED` classification;
- closure reporting.

### Gap

The source-project failure shows a missing explicit handoff-closeout connection:

```text
handoff refresh
→ freshness impact map for machine consumers
→ current/history/stale classification
→ exact-head contract validation
→ closeout
```

Verdict: `ABSORB`, not `BUILD_NEW`.

## BCP-2026-013 comparison

| Dimension | BCP-2026-013 | BCP-2026-014 |
|---|---|---|
| Lifecycle point | after merge/integration | before merge, during refresh/closeout |
| Trigger | integration changes repository truth | Handoff rewrite changes a machine-consumed surface |
| Failure | live current-state router becomes stale after merge | machine consumer contract breaks when legacy/current tokens are removed or conflated |
| Required observation | post-merge main/PR/CI truth | machine consumer inventory + exact-head contract result |
| Main mitigation | reconcile live continuation state | classify current vs historical compatibility vs stale/remove |
| Base owner | maintaining-project-context-and-handoff | same owner + canonical-reference-freshness support |

They are related lifecycle edges and may later share one implementation package if separately approved. They are not identical failure modes.

## External benchmark

External material was used only as analogy for compatibility discipline, not as a direct mandate for Handoff file schemas.

### GitHub required status checks

GitHub documents that if a workflow is skipped by path/branch filtering or commit-message conditions, checks associated with that workflow can remain Pending and block a pull request. The relevant principle is that a machine-consumed contract surface cannot be treated as absent merely because a human believes that path does not need the check.

Project adaptation:

```text
machine consumer exists
→ account for it explicitly
→ migrate consumer or preserve a compatibility boundary
→ do not silently remove the consumed surface
```

### Semantic Versioning 2.0.0

Semantic Versioning treats a declared public API as a compatibility contract and requires incompatible changes to be handled explicitly. Documentation can be part of the declared public interface.

Project adaptation: a document token that external tests/parsers consume can behave as a public compatibility surface even when it looks like prose to a human editor.

### Kubernetes API deprecation policy

Kubernetes uses staged deprecation/version rules instead of arbitrary removal of stable API elements.

Project adaptation: historical Handoff tokens should not be preserved forever merely because they once existed, but consumer migration/removal should be deliberate and evidenced instead of incidental to prose cleanup.

Primary references:

- GitHub Docs — Troubleshooting required status checks
- Semantic Versioning 2.0.0
- Kubernetes Documentation — API deprecation policy

## Counterexamples

### Consumer migration is preferable

If one stale test is the only consumer of a token and that test itself encodes a superseded requirement, changing the test in an independently approved migration is better than indefinitely preserving the token.

### Historical snapshots are not current routers

A dated review or evidence document can accurately record an old version or PR state forever. It should not be rewritten merely because the repository advanced.

### No machine consumer

A private note or handoff surface with no parser/test/workflow consumer does not need this entire compatibility classification process.

## Future acceptance fixtures if implemented

### Fixture A — current truth plus historical compatibility

```yaml
current:
  product_version: 4.3
compatibility_consumers:
  - token: Ver 4.2
    classification: HISTORICAL_COMPATIBILITY_ONLY
expected:
  current_section_contains_old_version_as_authority: false
  compatibility_section_contains_required_old_token: true
  exact_head_contracts: PASS
```

### Fixture B — stale consumer should be migrated

```yaml
consumer:
  requirement_is_superseded: true
  only_consumer: true
expected:
  action: MIGRATE_CONSUMER
  add_permanent_compatibility_anchor: false
```

### Fixture C — missing consumer inventory

```yaml
handoff_rewrite_is_material: true
machine_consumer_inventory: NOT_RUN
expected:
  closeout_status: BLOCKED_UNVERIFIED
```

### Fixture D — exact-head failure after partial compatibility restoration

```yaml
known_consumers_restored: true
exact_head_validation: FAIL_NEW_MISSING_CONSUMER
expected:
  closeout_status: NOT_GREEN
  action: EXPAND_CONSUMER_INVENTORY_AND_RETRY
```

## Evidence ceiling

```yaml
single_source_project_reproduction: VERIFIED
source_project_recovery: VERIFIED
source_project_exact_head_green: VERIFIED
second_project_pilot_same_exact_gap: NOT_RUN
human_usability_of_future_base_contract: NOT_RUN
base_active_implementation: NOT_STARTED
base_active_files_changed_by_proposal_stage: 0
```
