# Sequential Part Coordinator and Human-Facing Notion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the nine-chat hard ownership model with one coordinator chat that reviews P01→P09 sequentially, permits validated cross-Part fixes, enforces true full adversarial loops, and makes Base/Project Notion Homes self-contained for human learning.

**Architecture:** Keep P01~P09 as stable semantic responsibility and learning checkpoints, but remove their role as write barriers. Preserve active independent PR/worktree isolation as a separate protection. GitHub remains structured/runtime truth; Notion Home becomes a self-contained human-facing projection, with drilldown pages used for evidence and depth rather than basic comprehension.

**Tech Stack:** Markdown, JSON, Python unittest, GitHub Actions, Notion human-facing pages.

**Spec:** `docs/superpowers/specs/2026-08-19-sequential-part-coordinator-and-human-facing-notion-design.md`

## Global Constraints

- Latest user instruction overrides earlier nine-chat workflow.
- P01~P09 remain stable semantic responsibility/learning checkpoints.
- One coordinator chat executes Parts sequentially.
- A validated cross-Part finding may be fixed by the coordinator; semantic ownership must still be recorded.
- Open/draft/ready independent PR branches remain protected unless explicitly taken over.
- `FULL_LOOP_COUNT_MINIMUM: 5` remains a minimum floor, and each counted loop must be full-scope.
- Notion Home must be self-contained before drilldown.
- No new paid service/API is introduced.

---

### Task 1: RED contract for sequential coordinator and cross-Part repair

**Files:**
- Modify: `tests/test_base_partition_contract.py`
- Test: `tests/test_base_partition_contract.py`

**Interfaces:**
- Consumes: current `BASE_PARTITION_MANIFEST.json`, operating model, worker/integration prompts, scope checker.
- Produces: failing assertions for `SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`, semantic ownership, sequential Part order, and coordinator cross-Part repair mode.

- [ ] Replace assertions that require nine new worker chats and `ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END` with assertions requiring one coordinator chat, sequential `P01..P09`, and zero required new Part chats.
- [ ] Add assertions for `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER` and `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`.
- [ ] Add scope-checker assertions for a coordinator/sequential mode that accepts a P01 semantic-owner file and a P04 semantic-owner file in the same validated change set while reporting attribution.
- [ ] Run `python -m unittest tests.test_base_partition_contract -v`; expected RED because production contract still encodes nine-chat hard boundaries.

### Task 2: GREEN sequential coordinator operating model

**Files:**
- Modify: `docs/operations/BASE_PARTITION_MANIFEST.json`
- Modify: `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- Modify: `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`
- Modify: `templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md`
- Modify: `tools/check_base_partition_scope.py`
- Test: `tests/test_base_partition_contract.py`

**Interfaces:**
- Consumes: RED assertions from Task 1.
- Produces: sequential coordinator execution contract and semantic-owner attribution.

- [ ] Set coordinator execution policy to `SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` with ordered Parts `P01..P09` and `required_new_worker_chats: 0`.
- [ ] Replace hard `OWN_PART_PAGE_ONLY`/write-barrier semantics with semantic owner attribution while keeping Part Notion pages as learning/evidence surfaces.
- [ ] Add `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER` and explicit `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED` distinction.
- [ ] Update prompt to tell one chat to complete P01→P09 sequentially and allow validated cross-Part fixes in the current PR, recording `CROSS_PART_CHANGE` with owner/paths/reason/tests.
- [ ] Keep `CROSS_PART_CHANGE_REQUEST` only for protected active workstreams, missing authority/evidence, or intentionally deferred coordination.
- [ ] Extend scope checker with coordinator/sequential classification that reports semantic owner per changed path rather than rejecting cross-Part/CP0 changes solely for ownership.
- [ ] Run partition contract and manifest validation; expected GREEN.

### Task 3: RED/GREEN true full adversarial loop counting

**Files:**
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Modify: `skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md`
- Modify: `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md` if present on current main after collision check.
- Test: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: existing full-loop minimum-five contract.
- Produces: `FULL_LOOP_IS_NOT_A_REVIEW_LENS` invariant and regression assertions.

- [ ] Add test assertions requiring `FULL_LOOP_IS_NOT_A_REVIEW_LENS` and explicit rejection of `Loop 1=scope, Loop 2=UX, Loop 3=CI` style counting.
- [ ] Run focused test; expected RED.
- [ ] Add invariant to adversarial Skill: every counted loop must repeat current-state readback, alternatives/current option recheck, full attack, critique validation, fixes, verification, better-alternative search, long-term fit, and whole-state re-attack.
- [ ] Clarify that a representative finding may label a loop report but never defines its scope.
- [ ] Update finding/report protocol/template so loop evidence records full-scope coverage, not one lens per index.
- [ ] Run focused test; expected GREEN.

### Task 4: Project Home self-contained human-facing contract

**Files:**
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `tests/test_notion_project_isolation_core_system_contract.py`
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` if current main consumer structure requires it.

**Interfaces:**
- Consumes: existing `NOTION_HUMAN_FACING_CANON` / `REPOSITORY_STRUCTURED_CANON` split.
- Produces: `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN` project contract.

- [ ] Add failing test requiring Project Home to contain project definition/value, protected direction, Core Loop/Flow, system purpose/interactions, UX/Visual direction, implementation status, evidence-ceiling validation status, blockers/next work, important decisions, risks/revisit conditions before drilldown.
- [ ] Run focused test; expected RED.
- [ ] Implement the same requirements in project operating-system Skill and workspace contract, while preserving GitHub structured/runtime truth.
- [ ] Require drilldown pages for detail/evidence only, not basic project understanding.
- [ ] Run focused test; expected GREEN.

### Task 5: Coordinator integration of completed Part findings

**Files:**
- Modify only current-main canonical owners that remain stale after revalidation, including likely `docs/operations/BASE_PARTITION_MANIFEST.json`, `skills/SKILL_REGISTRY.json`, `.github/reference-freshness.json`, legacy Sheet/Figma policy consumers, and affected focused tests.
- Do not modify active PR #537 or #535 branches directly.

**Interfaces:**
- Consumes: supplied P01~P09 completion packets and P07 coordinator handoff; current latest main is authority.
- Produces: deduplicated accepted cross-Part fixes on one coordinator-owned branch.

- [ ] Revalidate every P01/P02/P04/P05/P06/P07/P09 cross-Part request against current main; drop already-resolved requests.
- [ ] Preserve P07 evidence ceiling: `ACTIVE_IN_MAIN` is publication lifecycle only, never device/human/store/runtime PASS. fileciteturn375file0L57-L79
- [ ] Resolve current CP0/Manifest/freshness/legacy routing findings that are still valid, recording semantic owner and actual consuming tests.
- [ ] Recheck P03 #537 and P08 #535 without mutating them; use their findings as evidence, not as merged canon.
- [ ] If a blocker can be solved entirely on current main via coordinator-owned CP0 change, implement it here so a later copy/finish can proceed without touching the original open PR.

### Task 6: Notion Base Home self-contained detailed learning view

**Files / Surfaces:**
- Update: Notion `Base · 작업 시스템 & Skill 지도`
- Read: `skills/SKILL_REGISTRY.json`, current Part manifest, current main Skill bodies/Modules.

**Interfaces:**
- Consumes: merged GitHub facts only.
- Produces: one-screen human learning view; Part pages remain drilldown/evidence.

- [ ] Replace nine-new-chat wording with one coordinator chat sequential P01→P09 workflow.
- [ ] Expand lifecycle modules with purpose, input, decision/process, output, downstream consumer, expected effect, and failure if absent.
- [ ] Expand active Skill catalog so each Skill has purpose, trigger, input, process, output, expected effect, connected Module/Test.
- [ ] Expand P01~P09 table to responsibility, representative Skills/Modules, execution flow, cross-Part links, expected effect, risks/revisit conditions.
- [ ] Add current-state/validation section distinguishing merged completed Parts from protected open P03/P08 workstreams.
- [ ] Read back page and confirm core understanding does not require opening child pages.

### Task 7: Project Home template/pilot detailed readback

**Files / Surfaces:**
- Update: human-facing project Home guidance and at least representative current Project Home(s) needed to verify the contract.

**Interfaces:**
- Consumes: Task 4 project Home contract.
- Produces: verified self-contained Home pattern without changing project structured/runtime canon.

- [ ] Use current project Home content to expand project definition, Core Loop, systems, UX/Visual, implementation/evidence status, blockers/next work, decisions, risks/revisit conditions directly on Home.
- [ ] Preserve child pages and databases; use mentions only as drilldown.
- [ ] Read back and verify all mandatory Home sections are visible without navigation.

### Task 8: Finish P03 and P08 without mutating their active branches

**Files:**
- Create new coordinator-owned finish branches/PRs only if required after governance/CP0 merge.
- Source evidence: open PR #537 and #535, current main, merged CP0 fixes.

**Interfaces:**
- Consumes: current main after Tasks 1–7 and protected open PR evidence.
- Produces: completed P03/P08 semantic outcomes without rewriting original active workstreams.

- [ ] Recheck #537 exact-head CI and diff against new main. If still valuable, copy/reapply its validated P03 semantic changes onto a new coordinator-owned P03 finish branch; leave #537 untouched.
- [ ] Recheck #535 after CP0 freshness-companion resolution. If still valuable, copy/reapply validated P08 semantic changes onto a new coordinator-owned P08 finish branch; leave #535 untouched.
- [ ] Run current required CI, true full adversarial loops, merge, post-merge readback for each copied finish PR.
- [ ] Mark original #537/#535 only according to explicit user policy; do not close them merely because a coordinator copy merged.

### Task 9: Final whole-Base integration and clean exit

**Files / Surfaces:**
- GitHub current main, Base Notion Home, Part pages, representative Project Homes.

**Interfaces:**
- Consumes: completed Tasks 1–8.
- Produces: final Base-wide completion report and clean main.

- [ ] Pin latest main and run whole-Base/changed-domain regression, reference freshness, generated artifact checks, scope/semantic-owner audit, required CI, review-thread audit.
- [ ] Perform at least five **true full-scope adversarial loops**; each loop repeats the complete lifecycle from current state/canon through alternatives, attack, validation, fixes, verification, better alternative, long-term fit, whole-state re-attack.
- [ ] Continue 6..N if any valid error/conflict/omission/blocker/regression remains.
- [ ] Merge exact head only after `CLEAN_REVIEW_EXIT`.
- [ ] Post-merge readback GitHub main and Notion Base/Project Homes.
- [ ] Report completed/merged work, protected open workstreams, tests, NOT_RUN, remaining risks, lessons, and revisit conditions.
