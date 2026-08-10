# Source Context Extraction and Auto-Merge Design

## Goal

Turn periodic external-source discovery into a traceable, low-risk improvement pipeline:

```text
source scan
→ context extraction
→ Base overlap / owner routing
→ bounded change
→ PR
→ adversarial review
→ exact-head CI
→ automatic squash merge when eligible
```

At the same time, make each unique Watchlist source measurable by cadence, scan freshness, useful findings, and actual Base contribution instead of counting source quantity alone.

## Approval and process overlay

The current user instruction explicitly approves this scope. Under `docs/CAPABILITY_COMPOSITION_MAP.md`, the Superpowers process is an `EXTERNAL_PROCESS_OVERLAY` and reuses the existing approval as `REUSED_APPROVAL`; it does not become Base canon or weaken Base gates.

## Existing Solution First

Reuse these owners instead of adding a new ACTIVE Skill:

- source discovery and source-role policy: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- detailed evidence records: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- evidence tiers and claim ceilings: `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
- prompt / Skill placement: `docs/AI_SKILL_ADOPTION_GUIDE.md`
- adversarial review: `running-adversarial-review-and-refinement`
- Base proposal boundary: `managing-base-change-proposals`
- repository merge policy: `docs/GITHUB_PRO_OPERATING_POLICY.md`
- live Base repository settings: `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`

No new ACTIVE Skill, owner, or repository-wide approval authority is introduced.

## Architecture

### 1. Unique-source operations ledger

Add:

`docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json`

The Watchlist remains the human-readable policy and domain/source pool. The ledger is the machine-readable operational state for unique sources that may appear in multiple domains.

Each entry records:

```json
{
  "source_id": "stable-id",
  "name": "human name",
  "domains": ["GAME_DEVELOPMENT"],
  "roles": ["AUTHORITY_TARGET"],
  "recommended_cadence": "daily-or-weekly",
  "scan_surfaces": ["release notes", "docs"],
  "last_successful_scan_at": null,
  "last_material_candidate_at": null,
  "last_base_contribution_at": null,
  "last_base_contribution_ref": null,
  "material_candidate_count_since_tracking_start": 0,
  "base_contribution_count_since_tracking_start": 0,
  "status": "ACTIVE"
}
```

Unknown historical values remain `null`; they are not backfilled by inference. A source timestamp advances only when that source was actually checked.

To avoid repository churn, scan-only state does not force a PR every day. When a material Base change is retained, the observed source state can travel with that change or its immediate bounded checkpoint. Otherwise truthful `NO_CHANGE` scan state is accumulated into a weekly `SCAN_STATE_BATCH`; freshness-sensitive policy/security deadlines may justify an earlier bounded checkpoint.

### 2. Context extraction packet

Extend the Watchlist execution contract with `SOURCE_CONTEXT_PACKET`:

```yaml
source_id:
source_domain:
source_role:
source_url_or_surface:
original_source_backtrace:
published_or_updated_at:
checked_at:
source_fact:
context_conditions:
freshness:
scope:
sample_or_method:
platform_or_medium:
commercial_or_vendor_interest:
license_or_copying_notes:
base_overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
existing_owner:
decision_delta:
smallest_change_candidate:
disposition: ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
work_disposition: NO_CHANGE | EVIDENCE_ONLY_UPDATE | ABSORB_EXISTING_OWNER | LOW_RISK_BOUNDED_UPDATE | RULE_OR_BCP_CANDIDATE | BCP_OR_USER_DECISION
```

The packet preserves what the source actually supports, the conditions under which it applies, and what Base decision would change. Discovery feeds and vendor summaries must still backtrace to original sources when possible.

### 3. Context-to-change retention gate

`ALREADY_COVERED` is not automatically discarded. A source is retained when it can improve an existing owner through a missing condition, counterexample, freshness check, source cross-check, checklist field, validation scenario, stale-reference correction, or test.

The smallest mechanism wins:

```text
existing owner/reference/test/template
→ instruction
→ Skill
→ specialist agent
→ deterministic tool
```

A new Skill remains exceptional and requires an independent reusable input/output/authority/validation boundary.

### 4. Source-scan automatic merge gate

The source pipeline may automatically create and merge a Base PR only when all of the following are true:

- work disposition is `EVIDENCE_ONLY_UPDATE`, `ABSORB_EXISTING_OWNER`, or `LOW_RISK_BOUNDED_UPDATE`
- the change stays within the already approved source-improvement scope
- original-source verification is sufficient for the claim being added
- same-goal open/recent PR check has no unresolved overlap or conflict
- an existing Base owner or approved destination is identified
- adversarial review finds no unresolved distortion, conflict, omission, overgeneralization, duplication, stale-reference, or scope-expansion blocker
- no `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `BCP_OR_USER_DECISION`, `BLOCKED_UNVERIFIED`, or equivalent blocker remains
- exact reviewed head equals current PR head
- branch is up to date with current `main` under the strict Required Check policy
- all applicable Required Checks, including `ci-gate`, succeed
- unresolved review threads are zero
- repository ruleset and allowed squash merge method remain verified

Then the agent may enable auto-merge or execute the repository-approved squash merge path.

GitHub's current model is deliberately reused: auto-merge waits for required reviews/checks, and strict status checks require the topic branch to be up to date with the base branch.

### 5. Automatic merge blockers

Do not auto-merge a source-derived change when it materially changes any of the following:

- repository/global policy meaning
- `AGENTS.md` authority order or approval semantics
- ACTIVE Skill ID, owner, trigger identity, or behavior schema
- security, permission, secrets, license, or dependency trust policy
- repository Ruleset / Required Check / workflow authority
- product, game, fiction, or channel core direction
- save/data compatibility or runtime behavior with meaningful blast radius
- a new specialist agent or new ACTIVE Skill
- a disputed or weakly verified external claim

Such a candidate becomes `RULE_OR_BCP_CANDIDATE`, `BCP_OR_USER_DECISION`, `TEST`, or `REFERENCE_ONLY` as appropriate. The pipeline may prepare evidence/proposal material but cannot silently merge the protected semantic change.

A low-risk edit inside an existing `SKILL.md` may still auto-merge only when adversarial review verifies that it adds a bounded reference/checklist/evidence/freshness guardrail without changing Skill identity, owner, trigger, permission, approval, or behavior schema. Ambiguity fails closed.

## Source efficiency metrics

The ledger is not a popularity score. It supports operational questions:

- Is this source being scanned at its intended cadence?
- When did it last produce a material candidate?
- When did it last cause an actual Base improvement?
- Does it repeatedly return only duplicated evidence?
- Is a discovery/vendor source earning its maintenance cost through original-source backtraces?

Do not remove a source solely for low contribution count. Static or high-authority sources can remain valuable despite infrequent changes.

## Error handling

- source not actually checked → do not advance `last_successful_scan_at`
- candidate found but context incomplete → `BLOCKED_UNVERIFIED` or `REFERENCE_ONLY`
- current main moved during PR validation → synchronize with current main and rerun exact-head checks
- CI not run or missing → `NOT_RUN`, never PASS
- merge API blocked by Ruleset → preserve the PR and resolve the real gate; never bypass main protection
- no meaningful delta → preserve truthful scan state for the next weekly batch checkpoint; `NO_CHANGE` remains valid

## Testing

Extend `tests/test_periodic_external_source_watchlist.py` to verify:

1. the ledger exists, is valid JSON, has unique `source_id` values, and covers every unique Watchlist source family;
2. each entry has cadence and truthful nullable scan/contribution fields;
3. Watchlist contains `SOURCE_CONTEXT_PACKET` and the source-to-PR flow;
4. auto-merge is limited to the three low-risk work dispositions;
5. protected semantic changes and unverified states block auto-merge;
6. strict-main freshness, exact-head CI, `ci-gate`, adversarial review, PR conflict check, and zero unresolved threads are required;
7. scan-only `NO_CHANGE` state is batched rather than forcing daily Ledger-only PRs;
8. no new ACTIVE Skill is introduced for this orchestration.

## Scope

Planned implementation changes:

- add `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`
- update `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- extend `tests/test_periodic_external_source_watchlist.py`
- no workflow-permission increase
- no new Skill or Registry entry
- update the existing ChatGPT `Base 개선 소스 스캔` automation so each run performs context extraction and, for eligible low-risk changes, carries the PR through verified merge

The automation remains external to Base; Base stores the contract, not the scheduler state.
