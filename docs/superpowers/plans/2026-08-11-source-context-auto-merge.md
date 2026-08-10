# Source Context Extraction and Auto-Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add measurable per-source operations state and connect periodic source discovery to context extraction, existing-owner absorption, verified PR creation, and fail-closed automatic merge for already-approved low-risk Base improvements.

**Architecture:** Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as the human-readable policy and source pool, add one machine-readable JSON ledger keyed by unique source families, and extend the existing Watchlist execution contract with a context packet and auto-merge gate. Reuse Base's existing adversarial review, BCP boundary, strict `ci-gate`, and squash auto-merge policy; do not add a new Skill, owner, workflow permission, or scheduler inside Base.

**Tech Stack:** Markdown contracts, JSON operational state, Python `unittest`, GitHub Actions, existing GitHub Ruleset/auto-merge.

## Global Constraints

- Baseline: `main@7ce3fb64fa6303c5da6c7fc27c979f7233b761ac` at plan start; re-read and synchronize if `main` advances before merge.
- Branch: `agent/source-context-auto-merge`; never write directly to `main`.
- Preserve `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as the source-policy owner.
- Preserve `REFERENCE_SOURCE_CATALOG.md` as detailed evidence/reference catalog; do not duplicate article-level records into the new ledger.
- Add no ACTIVE Skill, Skill Registry entry, new policy owner, new GitHub workflow permission, or repository setting.
- Unknown historical scan/contribution state stays `null`; do not infer prior per-source timestamps.
- Auto-merge only `EVIDENCE_ONLY_UPDATE`, `ABSORB_EXISTING_OWNER`, or `LOW_RISK_BOUNDED_UPDATE` after all existing PR/Ruleset gates pass.
- Protected semantic changes remain proposal/user-decision work and cannot be silently auto-merged.
- Use exact-head validation; unrun validation is `NOT_RUN`, never PASS.

---

### Task 1: Define the failing operational-ledger and context-to-merge contract

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Test: `tests/test_periodic_external_source_watchlist.py`

**Interfaces:**
- Consumes: existing Watchlist text and the planned ledger path.
- Produces: regression tests that define the JSON ledger schema, unique-source count, context packet, and auto-merge blockers.

- [ ] **Step 1: Add constants and JSON parsing**

Add `import json` and:

```python
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
```

- [ ] **Step 2: Add a failing ledger schema test**

Add a test that requires:

```python
self.assertTrue(LEDGER.is_file())
data = json.loads(LEDGER.read_text(encoding="utf-8"))
self.assertEqual(1, data["schema_version"])
self.assertEqual("2026-08-11", data["tracking_started_at"])
self.assertEqual(33, len(data["sources"]))
self.assertEqual(33, len({row["source_id"] for row in data["sources"]}))
```

For every row require keys:

```text
source_id
name
domains
roles
recommended_cadence
scan_surfaces
last_successful_scan_at
last_material_candidate_at
last_base_contribution_at
last_base_contribution_ref
material_candidate_count_since_tracking_start
base_contribution_count_since_tracking_start
status
```

Require cadence in:

```text
daily-or-weekly
weekly
monthly-or-on-demand
quarterly-or-when-relevant
```

Require `status == "ACTIVE"`, all historical timestamp/ref fields initially `None`, and both counters initially `0`.

- [ ] **Step 3: Add a failing coverage test for unique source families**

Require all 33 stable IDs below and verify each row name is represented by the Watchlist or maps to its explicit source family:

```text
godot
steamworks
android-games
google-play-policy
xbox-accessibility
gpuopen
gdc-vault
game-developer
games-user-research
80-level
level-design-book
game-accessibility-guidelines
how-to-market-a-game
deconstructor-of-fun
hada-geeknews
gamediscoverco
gameanalytics
steamdb
openai
a​nthropic
github-copilot
google-ai-adk
microsoft-learn
reedsy
inkle-ink
yarn-spinner
igda-game-writing
emily-short
youtube-official
blackmagic-davinci
adobe-premiere
frameio
vidiq
```

Remove the zero-width character from `anthropic` in the actual test string; it is shown here only to prevent accidental editor autolinking.

- [ ] **Step 4: Add a failing Watchlist pipeline test**

Require the Watchlist to contain all of:

```text
SOURCE_OPERATIONS_LEDGER
SOURCE_CONTEXT_PACKET
CONTEXT_EXTRACTION
CONTEXT_TO_CHANGE
SOURCE_SCAN_AUTO_MERGE_GATE
EVIDENCE_ONLY_UPDATE
ABSORB_EXISTING_OWNER
LOW_RISK_BOUNDED_UPDATE
RULE_OR_BCP_CANDIDATE
BCP_OR_USER_DECISION
reviewed_head_sha
current_head_sha
strict up-to-date
ci-gate
unresolved review thread
```

Also require explicit blockers for `ACTIVE Skill ID`, `behavior schema`, `security`, `permission`, `license`, `Ruleset`, `Required Check`, and core product/game/fiction/channel direction.

- [ ] **Step 5: Run focused test and verify RED**

Run:

```bash
python -m unittest tests.test_periodic_external_source_watchlist -v
```

Expected: FAIL because the ledger does not exist and the new Watchlist tokens are absent. Existing pre-change tests should continue to pass.

- [ ] **Step 6: Commit the test-only RED state**

```bash
git add tests/test_periodic_external_source_watchlist.py
git commit -m "test: define source context auto merge contract"
```

---

### Task 2: Add the unique-source operations ledger

**Files:**
- Create: `docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json`
- Test: `tests/test_periodic_external_source_watchlist.py`

**Interfaces:**
- Consumes: the 5 Watchlist domains and their current source rows.
- Produces: `schema_version=1` JSON with exactly 33 unique source-family records.

- [ ] **Step 1: Create the JSON root**

Use:

```json
{
  "schema_version": 1,
  "ledger_role": "periodic-source-operational-state",
  "tracking_started_at": "2026-08-11",
  "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
  "state_semantics": "Timestamps and counters apply only from tracking_started_at unless an individual source scan provides direct evidence. Null means not yet verified in this ledger.",
  "sources": []
}
```

- [ ] **Step 2: Populate 33 unique source families**

Use the stable IDs from Task 1. A source reused across domains appears once with multiple domains/roles where applicable.

Cadence assignment:

```text
daily-or-weekly:
  hada-geeknews, openai, anthropic, github-copilot, google-ai-adk,
  microsoft-learn, godot, steamworks, android-games, google-play-policy,
  youtube-official

weekly:
  gamediscoverco, how-to-market-a-game, game-developer, reedsy,
  adobe-premiere, frameio, vidiq, steamdb, blackmagic-davinci

monthly-or-on-demand:
  gdc-vault, games-user-research, 80-level, gameanalytics,
  deconstructor-of-fun, gpuopen, igda-game-writing, inkle-ink, yarn-spinner

quarterly-or-when-relevant:
  level-design-book, game-accessibility-guidelines, emily-short,
  xbox-accessibility
```

This explicitly closes the current cadence omission for Xbox Accessibility, SteamDB, and Blackmagic/DaVinci.

- [ ] **Step 3: Preserve truthful initial state**

Every row starts with:

```json
"last_successful_scan_at": null,
"last_material_candidate_at": null,
"last_base_contribution_at": null,
"last_base_contribution_ref": null,
"material_candidate_count_since_tracking_start": 0,
"base_contribution_count_since_tracking_start": 0,
"status": "ACTIVE"
```

Do not infer historical contribution dates from older PRs.

- [ ] **Step 4: Run the focused ledger tests**

Run:

```bash
python -m unittest tests.test_periodic_external_source_watchlist -v
```

Expected: ledger tests pass; Watchlist pipeline test remains RED until Task 3.

- [ ] **Step 5: Commit the ledger**

```bash
git add docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
git commit -m "docs: add periodic source operations ledger"
```

---

### Task 3: Connect scan → context → existing owner → PR → auto-merge

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Test: `tests/test_periodic_external_source_watchlist.py`

**Interfaces:**
- Consumes: ledger records and existing evidence/BCP/GitHub policies.
- Produces: source scan execution contract with `SOURCE_CONTEXT_PACKET` and `SOURCE_SCAN_AUTO_MERGE_GATE`.

- [ ] **Step 1: Add the ledger ownership boundary**

Add a short section after the Source role explanation:

```text
Watchlist = source pool / role / decision policy
REFERENCE_SOURCE_CATALOG = article- and claim-level evidence catalog
PERIODIC_SOURCE_OPERATIONS_LEDGER.json = unique-source cadence and observed scan/contribution state
```

State that the ledger is operational evidence, not authority, and may only advance a source's scan timestamp when that source was actually checked.

- [ ] **Step 2: Add `SOURCE_CONTEXT_PACKET`**

Add the exact fields from the design:

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

- [ ] **Step 3: Add the context-to-change flow**

Use:

```text
SOURCE_INDEX_REFRESH
→ SOURCE_OPERATIONS_LEDGER
→ NEW_OR_CHANGED_CANDIDATES
→ ORIGINAL_SOURCE_BACKTRACE
→ CONTEXT_EXTRACTION / SOURCE_CONTEXT_PACKET
→ CURRENT_BASE_AND_PR_OVERLAP
→ CONTEXT_TO_CHANGE / EXISTING_OWNER_FIRST
→ ADVERSARIAL_ATTACK
→ CRITIQUE_VALIDATION
→ NO_CHANGE | EVIDENCE_ONLY_UPDATE | ABSORB_EXISTING_OWNER | LOW_RISK_BOUNDED_UPDATE | RULE_OR_BCP_CANDIDATE | BCP_OR_USER_DECISION
→ PR when a repository change is retained
→ EXACT_HEAD_VALIDATION
→ SOURCE_SCAN_AUTO_MERGE_GATE
→ MERGED | BLOCKED | USER_DECISION_REQUIRED
```

- [ ] **Step 4: Add the fail-closed source auto-merge gate**

Require:

```yaml
SOURCE_SCAN_AUTO_MERGE_GATE:
  work_disposition:
  approval_scope: REUSED_APPROVAL | NEW_APPROVAL | BLOCKED
  original_source_verified:
  existing_owner_confirmed:
  same_goal_pr_conflict: NONE | PARTIAL | CONFLICT
  adversarial_blockers: []
  reviewed_head_sha:
  current_head_sha:
  base_main_sha:
  strict_up_to_date:
  required_check: ci-gate
  required_checks_passed:
  unresolved_review_threads:
  protected_semantic_change:
  result: AUTO_MERGE_ELIGIBLE | AUTO_MERGE_ENABLED | AUTO_MERGE_BLOCKED
```

Only the three low-risk work dispositions can reach `AUTO_MERGE_ELIGIBLE`.

- [ ] **Step 5: Add protected-semantic blockers**

Explicitly block automatic merge for repository/global policy meaning, `AGENTS.md` authority/approval semantics, ACTIVE Skill ID/owner/trigger/behavior schema, security/permission/secrets/license/trust policy, Ruleset/Required Check/workflow authority, core product/game/fiction/channel direction, meaningful save/data/runtime blast radius, new ACTIVE Skill/specialist agent, or weakly verified/disputed claims.

A bounded edit to an existing `SKILL.md` may pass only if it changes reference/checklist/evidence/freshness guidance without changing protected semantics; ambiguity is `AUTO_MERGE_BLOCKED`.

- [ ] **Step 6: Add source operational update rules**

On each run:

- update `last_successful_scan_at` only for sources actually checked;
- update `last_material_candidate_at` and increment its counter only for retained material candidates;
- update `last_base_contribution_at`, ref, and counter only after the Base change actually merges;
- `NO_CHANGE` may still advance truthful scan timestamps but not contribution fields.

- [ ] **Step 7: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_periodic_external_source_watchlist -v
```

Expected: PASS.

- [ ] **Step 8: Commit the Watchlist implementation**

```bash
git add docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md tests/test_periodic_external_source_watchlist.py
git commit -m "docs: connect source context extraction to verified merge"
```

---

### Task 4: Adversarial review, full validation, PR, and automation update

**Files:**
- Review: the spec, plan, Watchlist, ledger, and test diff.
- External scheduler state: existing ChatGPT automation `Base 개선 소스 스캔`.

**Interfaces:**
- Consumes: exact branch diff and current GitHub/automation state.
- Produces: merged Base contract and an updated recurring scan that can carry eligible low-risk source improvements through verified merge.

- [ ] **Step 1: Run adversarial review on the exact diff**

Attack for:

```text
source-count inflation
source duplication across domains
false historical timestamps
cadence over-scanning
vendor/discovery authority escalation
context extraction dropping limiting conditions
ALREADY_COVERED being discarded too early
new-Skill bias
forced weekly churn
semantic policy changes mislabeled low-risk
SKILL.md behavior changes slipping through
CI or review bypass
main moving after review
merge before contribution-state update
ledger becoming a second source-of-truth for evidence claims
```

- [ ] **Step 2: Run focused and repository validation**

Run locally if available:

```bash
python -m unittest tests.test_periodic_external_source_watchlist -v
python -m unittest tests.test_weekly_work_improvement_review -v
```

Then require the repository's PR-triggered `Validate Evidence-Based Game Development Knowledge`, `Validate Base v9 Operating Contracts`, `Dependency Review`, and canonical `Validate Game Project Operating System` / final `ci-gate` on the exact reviewed head. Do not report an unrun check as PASS.

- [ ] **Step 3: Re-read current main and synchronize if needed**

If `main` advanced, compare changed files for overlap, merge/rebase the current main into the branch without rewriting protected history, and rerun exact-head validation. Require `strict_up_to_date=true` before merge.

- [ ] **Step 4: Open/refresh PR and verify zero actionable review threads**

PR body must record Existing Solution First, no new ACTIVE Skill, RED→GREEN evidence, adversarial findings, exact head, and auto-merge disposition.

- [ ] **Step 5: Enable repository-approved squash auto-merge only after gate eligibility**

If the PR itself is a low-risk bounded update and all gates pass, enable auto-merge or execute the approved squash merge path. Never bypass the active Ruleset.

- [ ] **Step 6: Update the existing `Base 개선 소스 스캔` automation**

Preserve its current cadence and five domains, but add this required run flow:

```text
latest Base main + Watchlist + operations ledger
→ check due/valuable sources
→ scan actual source
→ update truthful scan state
→ SOURCE_CONTEXT_PACKET
→ original-source backtrace
→ same-goal PR / current Base overlap
→ existing owner first
→ adversarial attack + critique validation
→ retain NO_CHANGE/evidence/absorb/low-risk/rule-BCP disposition
→ for retained low-risk Base change: branch + PR + tests + exact-head CI + strict-main sync + zero review threads
→ source auto-merge gate
→ repository-approved squash merge when eligible
→ only after merged: update contribution timestamp/ref/counter in a follow-up bounded PR or the same scan's next checkpoint
```

If the candidate is protected-semantic, weakly verified, or BCP/user-decision scope, stop automatic merge and report the blocker/candidate instead.

- [ ] **Step 7: Post-merge readback**

Re-read `main`, Watchlist, ledger, and merged PR state. Report the final main SHA, changed files, validation, auto-merge state, and any unverified scope.
