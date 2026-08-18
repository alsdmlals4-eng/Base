# Unified Notion Project Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Notion the single project operating workspace, remove the deprecated Figma/local visual-delivery implementation, and preserve only reusable principles.

**Architecture:** One Notion workspace uses Project Registry + Work Master + Asset & Knowledge Master. Project pages expose only Project-filtered views and a derived Visual Map. Repository runtime truth stays in code/data/scenes/tests; QA Evidence Studio remains independent.

**Tech Stack:** Notion databases/views, Markdown/JSON Base contracts, GitHub Actions, Python contract tests.

**Spec:** `docs/superpowers/specs/2026-08-19-notion-unified-project-workspace-design.md`

## Global Constraints

- `MINIMUM_VIABLE_ALTERNATIVES: 3`
- `BETTER_ALTERNATIVE_SEARCH`
- `LONG_TERM_PLAN_FIT_REQUIRED`
- `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`
- `ZERO_INCREMENTAL_COST_REQUIRED`
- Do not modify another open/draft/ready PR.
- Keep QA Evidence Studio and unrelated Godot/CI validation tooling.
- Remove deprecated visual execution layers only after their reusable rules are represented in active contracts.

---

### Task 1: Establish Notion workspace authority

**Files:**
- Create: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- Modify: `AGENTS.md`
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Modify: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Test: `tests/test_notion_project_workspace_contract.py`

**Interfaces:**
- Consumes: approved Notion workspace design.
- Produces: canonical tokens `NOTION_DEFAULT_PROJECT_WORKSPACE`, `PROJECT_RELATION_REQUIRED`, `WORK_MASTER`, `ASSET_KNOWLEDGE_MASTER`, `VISUAL_MAP_DERIVED`.

- [ ] Write a failing contract test requiring Notion authority tokens and forbidding active Figma-default tokens.
- [ ] Run the focused contract test and confirm RED on current main semantics.
- [ ] Add the machine authority contract and rewrite active visual/GDD compatibility policies.
- [ ] Update AGENTS paid-plan and workspace authority statements.
- [ ] Run focused contract tests to GREEN.

### Task 2: Absorb visual-tool knowledge before deleting implementations

**Files:**
- Create: `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- Modify: `docs/knowledge/game-development/PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Test: `tests/test_notion_project_workspace_contract.py`

**Interfaces:**
- Consumes: identity/provenance/approval/reuse/readback concepts from Expression Studio, Sprite Animation Studio, Asset Vault and Figma flow work.
- Produces: tool-neutral image/asset/flow contract usable through ChatGPT + Notion.

- [ ] Add RED assertions for project boundary, provenance, approval, version, readback and benchmark-decision vocabulary.
- [ ] Add tool-neutral workflow documentation.
- [ ] Point preferred visual references and image review to Notion Asset/Knowledge Master instead of Figma.
- [ ] Run focused tests to GREEN.

### Task 3: Remove abandoned visual execution implementation

**Files:**
- Delete tree: `tools/figma-bridge/`
- Delete tree: `tools/expression-studio/`
- Delete tree: `tools/sprite-animation-studio/`
- Delete tree: `tools/tool-hub/`
- Delete tree: `tools/base-tool-contracts/`
- Delete: `tools/TOOL_REGISTRY.json`
- Delete: `tools/validate_tool_registry.py`
- Delete: Figma-only schemas and project registries.
- Delete: Figma/Studio-only project templates.
- Delete: Figma/Studio/Tool-Hub-only contract tests and CI workflows.

**Interfaces:**
- Consumes: Task 2 neutral workflow.
- Produces: no active Figma/local visual delivery runtime in Base.

- [ ] Remove implementation trees and their exact routing registries.
- [ ] Remove Figma-only schemas/templates/tests/workflows.
- [ ] Search surviving active files for `figma-bridge`, `PROJECT_FIGMA`, `FIGMA_DEFAULT_VISUAL_WORKSPACE`, `expression-studio`, `sprite-animation-studio`, and `tool-hub`.
- [ ] Fix only surviving active references required by current Base behavior; historical Git commits remain the archive.

### Task 4: Keep independent QA and runtime validation coherent

**Files:**
- Modify: `tools/qa-evidence-studio/README.md` only if it references Tool Hub as the required launch path.
- Modify: `docs/CI_EXECUTION_COST_POLICY.md` if removed workflows are listed as active required jobs.
- Modify: `tests/test_ci_workflow_cost_policy.py` if it assumes removed visual workflows.

**Interfaces:**
- Consumes: standalone QA Evidence Studio.
- Produces: QA path independent of Figma/Tool Hub.

- [ ] Verify QA Evidence Studio remains installable/understandable as a standalone developer-PC evidence tool.
- [ ] Remove only obsolete visual-workflow expectations from CI cost contracts.
- [ ] Preserve Android-deferred and real-runtime evidence boundaries.

### Task 5: Remove Figma discovery dependencies but retain transferable UI knowledge

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Modify: `docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json`
- Modify or delete: `tests/test_uiux_external_reference_absorption.py`
- Modify: `skills/auditing-and-refining-ui-art/LEARNING_LOG.md`

**Interfaces:**
- Consumes: already absorbed general UI design-intent guidance.
- Produces: no active periodic Figma watch while keeping generic UI rules.

- [ ] Remove Huddling/Figma-specific periodic source entries.
- [ ] Keep general design-intent, readability and anti-generic UI guidance independent of Figma.
- [ ] Update source-discovery tests accordingly.

### Task 6: Verify exact branch state and open PR

**Files:**
- No new product files unless regression fixes are required.

**Interfaces:**
- Produces: reviewable PR from exact current main without touching other open PRs.

- [ ] Search the branch for deprecated active tokens and classify any remaining matches as current, compatibility-only, or historical.
- [ ] Open a PR against `main`.
- [ ] Run/inspect required GitHub Actions at exact head.
- [ ] Fix regressions until required checks pass or report a concrete blocker.
- [ ] Verify Notion project workspace readback separately from repository CI; never treat Notion planning success as Godot/runtime proof.
