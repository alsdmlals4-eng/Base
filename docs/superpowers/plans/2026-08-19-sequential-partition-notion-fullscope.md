# Sequential Partition, Cross-Part Repair, Notion Full-View, and Full-Scope Adversarial Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace multi-chat write-isolated Partition execution with one-chat sequential P01→P09 operation, permit validated cross-Part repairs without mutating independent active workstreams, make Notion main/Home views human-complete, and make five full adversarial loops mechanically distinct from five review lenses.

**Architecture:** P01~P09 remain stable responsibility and learning lenses in the Manifest, but execution authority moves to a coordinator-sequential model. Cross-Part ownership remains attribution/provenance rather than a hard repair prohibition. GitHub structured/runtime truth stays canonical; Notion becomes a self-contained human-facing projection. Adversarial review tests require each counted loop to contain whole-scope lifecycle evidence.

**Tech Stack:** Markdown, JSON contracts, Python unittest, GitHub Actions, Notion.

**Spec:** `docs/superpowers/specs/2026-08-19-sequential-partition-notion-fullscope-design.md`

## Global Constraints

- Latest user instruction outranks earlier multi-chat Partition rules.
- Open/draft/ready independent PRs remain protected from direct mutation.
- `FULL_LOOP_COUNT_MINIMUM: 5` and clean-exit-after-five remain unchanged.
- No new paid service/API.
- Notion is human-facing; GitHub is structured/runtime truth.
- Do not claim P03/P08 complete while their PRs remain open/unmerged.

---

### Task 1: RED contracts for sequential operation and cross-Part repair

**Files:**
- Modify: `tests/test_base_partition_contract.py`
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: existing `BASE_PARTITION_MANIFEST.json`, worker/integration prompts, adversarial Skill.
- Produces: regression requirements for `ONE_COORDINATOR_CHAT_SEQUENTIAL_P01_TO_P09`, `PART_BOUNDARY_IS_ANALYSIS_AND_ACCOUNTABILITY_NOT_A_FIX_PROHIBITION`, and `FULL_LOOP_IS_NOT_A_REVIEW_LENS`.

- [ ] Add tests that reject `ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END` as the active default and require one coordinator sequential P01→P09.
- [ ] Add tests that allow validated cross-Part/CP0 repair by the coordinator while retaining independent-active-workstream protection.
- [ ] Add tests that require explicit text saying five review lenses do not count as five full loops.
- [ ] Run the focused contract CI and observe RED against current production text.

### Task 2: Migrate Partition operating model and prompts

**Files:**
- Modify: `docs/operations/BASE_PARTITION_MANIFEST.json`
- Modify: `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- Modify: `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`
- Modify: `templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md`
- Modify as needed: `docs/operations/base-partitions/P01_*.md` through `P09_*.md`

**Interfaces:**
- Consumes: Task 1 regression tokens.
- Produces: sequential coordinator execution contract, repair-authority conditions, and Part checkpoint model.

- [ ] Set coordinator model to one chat executing P01→P09 sequentially.
- [ ] Keep Part IDs, responsibility maps, learning logs, source-discovery questions, and per-Part completion checkpoints.
- [ ] Replace hard cross-Part repair prohibition with validated repair conditions.
- [ ] Preserve independent active workstream protection and same-semantic-change conflict detection.
- [ ] Require latest-main re-pin between Part-sized merges.
- [ ] Run focused tests to GREEN.

### Task 3: Correct adversarial review contract

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Modify: `skills/running-adversarial-review-and-refinement/LEARNING_LOG.md`
- Modify: `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md` only if current-main ownership permits; otherwise record active-workstream conflict and apply correction to unowned canonical surfaces.
- Test: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Produces: `FULL_LOOP_IS_NOT_A_REVIEW_LENS` and explicit counted-loop evidence requirements.

- [ ] Add a normative definition of a counted full loop.
- [ ] Add invalid-example text showing five domain lenses are not five loops.
- [ ] Require every loop record to show whole-scope review plus alternatives, verification, better-alternative search, and long-term-fit recheck.
- [ ] Preserve minimum-five-plus-until-clean semantics.
- [ ] Record the superseding learning lesson without deleting history.
- [ ] Run focused adversarial tests.

### Task 4: Integrate completed-Part CP0/cross-Part findings

**Files:**
- Modify only canonical owner files needed after deduplication, likely including `docs/operations/BASE_PARTITION_MANIFEST.json`, `skills/SKILL_REGISTRY.json`, `.github/reference-freshness.json`, selected legacy Sheet/Figma authority consumers/tests, and ownership/path declarations.

**Interfaces:**
- Consumes: completed P01/P02/P04/P05/P06/P07/P09 packets and P07 handoff file; excludes unmerged P03/P08 implementation bodies.
- Produces: one deduplicated coordinator repair set.

- [ ] Re-pin latest main.
- [ ] Deduplicate completed-Part cross-Part requests by semantic owner.
- [ ] Fix stale/nonexistent Manifest paths, legacy Sheet/Figma active authority, owner-local freshness companion deadlocks where possible without mutating P08 branch, P07 read-only dependency declarations, P09 path drift, and CI-consumption claims.
- [ ] Do not copy/absorb P03/P08 open PR implementation.
- [ ] Add/adjust tests proving owner-correct semantics.
- [ ] Run canonical freshness and Base-wide contracts.

### Task 5: Make Notion Base main human-complete

**Files:**
- Notion: `Base · 작업 시스템 & Skill 지도`
- Notion: P01~P09 pages as supporting evidence only.

**Interfaces:**
- Consumes: latest merged Base contracts and active Skill Registry.
- Produces: one-page human learning/reading surface.

- [ ] Expand Base purpose and authority model.
- [ ] Explain every active Skill or coherent Skill family with purpose, trigger, process, output, expected effect, dependencies/tests.
- [ ] Expand module flow into step-by-step responsibilities and transitions.
- [ ] Expand P01~P09 with responsibility, inputs, outputs, representative Skills/Modules, interactions, expected effect, failure risk.
- [ ] Explain adversarial review full-loop semantics with valid/invalid examples.
- [ ] Show current merged/open work state and evidence ceilings.
- [ ] Read back the page and verify essential understanding does not require child-page navigation.

### Task 6: Define and apply project Home completeness contract

**Files:**
- Modify canonical project-workspace policy/Skill/template files under their current owner.
- Notion: representative Project Home(s), beginning with currently connected examples such as OMENWARD, then propagate contract rather than manually duplicating stale data everywhere.
- Test: relevant Notion/project workspace tests.

**Interfaces:**
- Produces: `PROJECT_HOME_MUST_BE_HUMAN_COMPLETE`.

- [ ] Require Home to include direction, player/user promise, core loop, major systems, UX/UI/visual direction, implementation/runtime status, validation/NOT_RUN, decisions, blockers/risks, next work, and authority/source locations.
- [ ] Keep detailed child pages for evidence/data, but forbid essential-context-only-in-child-page designs.
- [ ] Update representative Home and read back.
- [ ] Add regression coverage for the contract.

### Task 7: Full verification and adversarial convergence

**Files:**
- Update plan/evidence/PR body as needed; no unrelated refactors.

- [ ] Run Partition, Skill routing, Base v9, Evidence Knowledge, project workspace, Game Project OS, freshness, and changed-domain suites.
- [ ] Compare changed paths with any currently open/draft/ready PRs; do not mutate overlapping active semantic owners without explicit resolution.
- [ ] Perform full-scope adversarial loop 1 over the entire resulting state.
- [ ] Repeat loops 2, 3, 4, and 5 over the entire resulting state; do not assign one lens per loop.
- [ ] If any valid finding remains after loop 5, fix/verify and continue 6..N until clean.
- [ ] Require unresolved review threads = 0 and exact-head CI GREEN.
- [ ] Merge with expected-head protection.
- [ ] Read back new main, Notion Base main, and representative project Home.
- [ ] Report completed vs still-open P03/P08 state without unsupported completion claims.
