# v4.7 Notion-First Workflow Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align Base current owners and the project v4.7 instruction around Notion-first planning, GPT-first review, one-block PowerShell/Codex execution, creative benchmark synthesis, retired Tool Hub/QA surfaces, and evidence-backed completion.

**Architecture:** Reuse existing semantic owners instead of adding a broad Skill. Correct stale consumers and the recent reusable-module catalog, then lock the change with one focused regression workflow. Preserve Loop Engineering independently from retired Tool Hub/QA Studio.

**Tech Stack:** Markdown policy/docs, Python `unittest`, GitHub Actions, Notion human-facing readback.

**Spec:** `docs/superpowers/specs/2026-08-20-v47-notion-first-workflow-alignment-design.md`

## Global Constraints

- Baseline is `61862f9a4f7995f1676acca4bb6d5365e46b7630`.
- Do not mutate another chat's explicitly active branch/path.
- Do not add Figma, external HTML workspace, Google Sheets, Tool Hub, or QA Evidence Studio to the active default project flow.
- Preserve `LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT` without making it depend on retired surfaces.
- Preserve current `MINIMUM_VIABLE_ALTERNATIVES: 3`, `BETTER_ALTERNATIVE_SEARCH`, `LONG_TERM_PLAN_FIT_REQUIRED`, `FULL_LOOP_COUNT_MINIMUM: 5`, `BALANCE_BUDGET`, `WORLD_STORYLINE_FIT_REQUIRED`, `RELEASE_NEAR_VERTICAL_SLICE_FIRST`, and `REQUIRED_WORK_REMAINING: 0`.
- No new broad Skill.
- Zero incremental cost; current paid AI plan is GPT Pro only.

---

### Task 1: Add focused RED contract

**Files:**
- Create: `tests/test_v47_workflow_alignment.py`
- Create: `.github/workflows/validate-v47-workflow-alignment.yml`

**Interfaces:**
- Consumes: current owner documents and merged reuse module registry.
- Produces: deterministic assertions for active/retired workspace routing and creative benchmark frontier.

- [ ] **Step 1: Write failing tests**

Assertions must require:

```text
TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW
QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW
NOTION_DEFAULT_PROJECT_WORKSPACE
GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL
REPOSITORY_NATIVE_EVIDENCE_CAPTURE
CREATIVE_BENCHMARK_FRONTIER
ORIGINALITY_FUN_CREATIVITY_REVIEW
PROJECT_VISUALIZATION_NEED_MAP
ACTIVE_OTHER_WORKER
BEGINNER_SAFE_USER_ACTION
```

and reject active/default Tool Hub/QA routing in entrypoints.

- [ ] **Step 2: Trigger RED**

Create a draft PR with test/workflow only. Expected: focused workflow fails because current docs still contain active Tool Hub/QA routing and lack the new creative-frontier tokens.

- [ ] **Step 3: Record RED run and exact failing assertions**

Do not treat unrelated or unconsumed Green checks as TDD evidence.

---

### Task 2: Correct active tool/workspace authority

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`
- Modify: `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`
- Modify: `docs/OPERATING_MODEL.md`

**Interfaces:**
- Consumes: latest user tool-surface decisions and existing Notion/repository domain-split canon.
- Produces: one discoverable active workflow with retired surfaces excluded.

- [ ] **Step 1: Remove stale Tool Hub/QA Studio default routing from `START_HERE.md`**
- [ ] **Step 2: Change retirement policy so Tool Hub and QA Evidence Studio are retired from active project flow**
- [ ] **Step 3: Replace Tool Hub-priority PowerShell language with direct one-block PowerShell/Codex + Loop Engineering when relevant**
- [ ] **Step 4: Replace stale Google Sheets `USER_FACING_GDD_WORKSPACE` wording in Operating Model with Notion human-facing / repository structured/runtime authority**
- [ ] **Step 5: Preserve historical tool code/evidence as archive/rollback, not active default**

---

### Task 3: Repair reusable-module catalog after QA retirement

**Files:**
- Modify: `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`

**Interfaces:**
- Consumes: `RM-TOOL-004` identity and repository/runtime evidence concepts.
- Produces: repository-native evidence capture contract with no dedicated QA Studio dependency.

- [ ] **Step 1: Preserve module ID `RM-TOOL-004` but replace implementation owner**

New semantic name:

```text
REPOSITORY_NATIVE_EVIDENCE_CAPTURE
```

- [ ] **Step 2: Define capture inputs as existing build/test/runtime outputs**

```yaml
project_identity:
build_identity:
validation_contract:
capture_sources:
  screenshots:
  logs:
  test_results:
  runtime_state:
storage:
  repository_or_ci_artifact:
  notion_human_link_when_useful:
verdict:
  evidence_ceiling:
```

- [ ] **Step 3: Mark `tools/qa-evidence-studio` as historical/superseded, not Existing Owner reuse**
- [ ] **Step 4: Update module fit/composition examples without creating another capture app**

---

### Task 4: Strengthen creative benchmark and visualization planning

**Files:**
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Modify: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`

**Interfaces:**
- Consumes: 3-alternative trade study, benchmark synthesis, `NOVELTY_DELTA`, Notion visual workflow.
- Produces: explicit creative frontier and project visualization need map.

- [ ] **Step 1: Add `CREATIVE_BENCHMARK_FRONTIER`**

Require direct best-in-class, adjacent best-in-class, distinctive/innovative, failure/mixed, and project-internal strengths.

- [ ] **Step 2: Add `ORIGINALITY_FUN_CREATIVITY_REVIEW`**

Keep fun as a hypothesis until player evidence; judge recombination rather than copy count.

- [ ] **Step 3: Add `PROJECT_VISUALIZATION_NEED_MAP`**

After project understanding, list which diagrams/images/screens/storyboards materially reduce ambiguity and where each belongs in the exact Project Notion workspace.

- [ ] **Step 4: Preserve image generation during planning when it improves decisions, while release-near player testing still requires integrated shipping-intent visuals**

---

### Task 5: GREEN verification and five full adversarial loops

**Files:** all changed files above.

**Interfaces:**
- Consumes: exact PR head.
- Produces: clean reviewed head or additional bounded fixes.

- [ ] **Step 1: Run focused v4.7 workflow**
- [ ] **Step 2: Run Base v9 / Game Project OS / relevant Evidence and long-horizon checks**
- [ ] **Step 3: Full adversarial loop #1 — authority/stale consumer attack**
- [ ] **Step 4: Full adversarial loop #2 — omission/consumer/test attack**
- [ ] **Step 5: Full adversarial loop #3 — over-generalization/cost/tool-sprawl attack**
- [ ] **Step 6: Full adversarial loop #4 — benchmark/creativity/player-evidence attack**
- [ ] **Step 7: Full adversarial loop #5 — PR/main/freshness/long-term fit attack**
- [ ] **Step 8: Continue #6..N if any new valid blocker remains**

Each loop is `FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK`, not five lenses in one pass.

---

### Task 6: PR completion, merge, Notion and v4.7 artifact

**Files:** Base branch + external artifact `/mnt/data/PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.7.md`.

**Interfaces:**
- Consumes: clean exact PR head and merged main.
- Produces: merged Base, updated Base Notion human view, final v4.7 instruction.

- [ ] **Step 1: Recheck all open PRs and current-owner evidence**
- [ ] **Step 2: Verify required checks and unresolved threads**
- [ ] **Step 3: Squash merge expected exact head**
- [ ] **Step 4: Read new main and same-goal/open PR state**
- [ ] **Step 5: Update `Base · 작업 시스템 & Skill 지도` Notion with human-readable workflow/tool-retirement/creative-frontier summary and read back**
- [ ] **Step 6: Build v4.7 from the prior project instruction, removing Sheet/Tool Hub/QA/Figma/HTML active references and aligning with merged Base**
- [ ] **Step 7: Validate v4.7 required tokens, code fences, stale references and SHA metadata**
- [ ] **Step 8: Final user-learning report: responsibility, core rules/Skills/modules, BEFORE→AFTER, long-term effect, trade-offs, evidence ceiling, remaining/revisit conditions**
