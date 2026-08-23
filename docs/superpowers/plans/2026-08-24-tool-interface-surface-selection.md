# Tool Interface Surface Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Absorb a reusable CLI/TUI/thin-GUI surface-selection gate into existing Base owners without reviving deprecated management surfaces or creating a new broad Skill.

**Architecture:** Preserve one domain/core owner and a stable machine-facing CLI/programmatic contract; treat TUI and thin GUI as optional presentation/operation adapters selected by actual workflow constraints. Integrate the rule into existing benchmarking and capability-composition owners, record one bounded reusable case, and add a focused repository regression that locks the non-goals and Implementation Reality Gate.

**Tech Stack:** Markdown policy/case documents, Python `unittest` regression contract, existing Base repository validation.

**Spec:** `docs/superpowers/specs/2026-08-24-tool-interface-surface-selection-design.md`

## Global Constraints

- Do not mutate open PR #630 or #631.
- No new broad Skill, Tool Hub, QA Evidence Studio, Figma-first path, or external HTML dashboard authority.
- No paid dependency or project runtime mutation.
- CLI/programmatic automation remains available when practical; no GUI-only machine contract.
- TUI remains conditionally valid for terminal-resident/remote workflows.
- Any GUI is thin, shares the existing domain core, and cannot own canon or runtime truth.
- Platform/accessibility claims remain bounded by actual target-platform evidence.

---

### Task 1: Add focused regression contract

**Files:**
- Create: `tests/test_tool_interface_surface_selection_contract.py`

**Interfaces:**
- Consumes: canonical policy paths `docs/BENCHMARKING_REFERENCE_GUIDE.md`, `docs/CAPABILITY_COMPOSITION_MAP.md`, `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Produces: repository-level assertions for `TOOL_INTERFACE_SURFACE_SELECTION`, core/CLI ownership, conditional TUI/GUI selection, target-platform evidence, and deprecated-surface non-revival

- [ ] **Step 1: Write the failing test**

Create a `unittest.TestCase` that reads the three owner documents and asserts all of the following tokens/semantics are present:

```python
TOOL_INTERFACE_SURFACE_SELECTION
CORE_LOGIC_SINGLE_OWNER
CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL
SURFACE_DOES_NOT_OWN_CANON
HUMAN_SURFACE_REQUIRES_REPAYMENT
KEYBOARD_FIRST_IS_CROSS_SURFACE
NO_DEPRECATED_SURFACE_REVIVAL
TARGET_PLATFORM_VERIFIED
```

Also assert the visual policy still contains its current retirement rule for dedicated Tool Hub / QA Evidence Studio / external HTML surfaces.

- [ ] **Step 2: Run the focused test to verify RED**

Run:

```bash
python -m unittest tests.test_tool_interface_surface_selection_contract -v
```

Expected: FAIL because the new interface-selection tokens are not yet present in the current owner documents.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_tool_interface_surface_selection_contract.py
git commit -m "test: guard tool interface surface selection"
```

### Task 2: Integrate the selection gate into existing owners

**Files:**
- Modify: `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- Modify: `docs/CAPABILITY_COMPOSITION_MAP.md`

**Interfaces:**
- Consumes: the design spec selection contract and existing `TOOL_PATTERN` / capability-composition ownership
- Produces: one documented tool-surface decision gate shared by benchmarking/reuse and capability routing

- [ ] **Step 1: Extend `BENCHMARKING_REFERENCE_GUIDE.md`**

Under the existing reusable `TOOL_PATTERN` guidance, add a compact subsection named `TOOL_INTERFACE_SURFACE_SELECTION` that:

- separates reusable core from CLI/TUI/GUI surfaces;
- requires comparison of CLI-only, CLI+TUI, and core/CLI+thin-GUI when materially applicable;
- states CLI/programmatic automation preference, conditional TUI use, conditional thin-GUI use;
- states keyboard-first/information density are cross-surface properties;
- records Implementation Reality Gate ceilings through `TARGET_PLATFORM_VERIFIED` and `HUMAN_WORKFLOW_VALUE_VERIFIED`;
- rejects UI generation as proof of cross-platform/accessibility quality.

- [ ] **Step 2: Extend `CAPABILITY_COMPOSITION_MAP.md`**

Add a capability row and contract section that defines:

```text
canonical data/runtime truth
→ reusable domain core
→ stable CLI/programmatic contract
→ optional TUI or thin GUI adapter
```

Include exact invariants:

```text
CORE_LOGIC_SINGLE_OWNER
CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL
SURFACE_DOES_NOT_OWN_CANON
HUMAN_SURFACE_REQUIRES_REPAYMENT
KEYBOARD_FIRST_IS_CROSS_SURFACE
NO_DEPRECATED_SURFACE_REVIVAL
```

- [ ] **Step 3: Run the focused test**

```bash
python -m unittest tests.test_tool_interface_surface_selection_contract -v
```

Expected: PASS for the new owner tokens and retirement guard.

- [ ] **Step 4: Commit owner integration**

```bash
git add docs/BENCHMARKING_REFERENCE_GUIDE.md docs/CAPABILITY_COMPOSITION_MAP.md
git commit -m "docs: add tool interface surface selection gate"
```

### Task 3: Record the reusable benchmark case

**Files:**
- Create: `docs/knowledge/cases/AGENT_GENERATED_UI_SURFACE_SELECTION_CASE.md`
- Modify: `docs/knowledge/cases/README.md`

**Interfaces:**
- Consumes: external source observations, counterarguments, Base decision pattern
- Produces: bounded reusable case with source limits and ADOPT/ADAPT/REJECT decisions

- [ ] **Step 1: Create the case document**

Record:

- observation: agent-assisted native GUI generation reduces some implementation friction;
- strong retained claim: CLI remains uniquely useful for automation/composability;
- adapted claim: keyboard-first/high-density interaction can be designed in GUI;
- conditional TUI value: SSH/tmux/terminal-resident and low-bandwidth workflows;
- rejected overgeneralization: macOS/SwiftUI evidence does not prove Windows/Linux/native-GUI superiority;
- Base adaptation: `TOOL_INTERFACE_SURFACE_SELECTION` with one core and optional surfaces;
- status: `가설/채택`, pending repeated project/runtime validation before promotion beyond the method/pattern level.

- [ ] **Step 2: Add the case to the case index**

Add it to the benchmark/reusable workflow section and problem-routing table in `docs/knowledge/cases/README.md` without changing project canon.

- [ ] **Step 3: Run the focused contract again**

```bash
python -m unittest tests.test_tool_interface_surface_selection_contract -v
```

Expected: PASS.

- [ ] **Step 4: Commit the case**

```bash
git add docs/knowledge/cases/AGENT_GENERATED_UI_SURFACE_SELECTION_CASE.md docs/knowledge/cases/README.md
git commit -m "docs: record agent-generated UI selection case"
```

### Task 4: Full validation and adversarial review

**Files:**
- Modify only if a validated finding requires correction within the approved scope.

**Interfaces:**
- Consumes: completed Tasks 1–3
- Produces: validated branch ready for PR review with evidence ceiling explicitly bounded

- [ ] **Step 1: Run focused contract**

```bash
python -m unittest tests.test_tool_interface_surface_selection_contract -v
```

Expected: PASS.

- [ ] **Step 2: Run existing Base local validation entry point**

```bash
python tools/run_local_validation.py
```

Expected: PASS, or explicit `BLOCKED_UNVERIFIED` for environment-only checks without reclassifying them as pass.

- [ ] **Step 3: Run five full adversarial review loops**

Each loop reviews the complete approved scope for:

1. GUI-first/TUI-ban overgeneralization;
2. duplicated state/canon ownership;
3. Tool Hub/QA Studio/Figma/external-dashboard revival;
4. cross-platform/accessibility overclaim;
5. unnecessary Skill/dependency/surface expansion and lifecycle cost.

Any valid finding is corrected, validation is rerun, and the next loop attacks the corrected whole.

- [ ] **Step 4: Reconcile against latest completed main and open PR impact**

Confirm #630/#631 remain untouched and the branch does not absorb their material deltas. If latest completed `main` changed, reconcile only non-conflicting completed-main updates and rerun validation.

- [ ] **Step 5: Open a bounded PR**

PR title:

```text
docs: add tool interface surface selection gate
```

PR body must state the source-derived limitation, 3-option comparison, IRG evidence ceiling, no-project-mutation scope, open-PR protection, and validation results.

### Task 5: Completion verification

**Files:** none unless verification identifies a defect.

**Interfaces:**
- Consumes: PR branch and validation evidence
- Produces: completion report with exact claims and remaining unverified scope

- [ ] **Step 1: Read back the PR diff/files**

Confirm the PR contains only the approved policy/case/test/spec/plan changes.

- [ ] **Step 2: Verify required checks/review state without bypass**

Do not use admin/ruleset bypass. If checks cannot be run from the current environment, report the exact evidence ceiling.

- [ ] **Step 3: Report before/after/effect**

Report:

- before: no explicit reusable CLI/TUI/thin-GUI selection gate;
- after: one-core + machine-contract + conditional-human-surface pattern;
- practical effect: avoids both needless TUI constraints and GUI proliferation while preserving automation and human usability;
- remaining scope: project-specific GUI/TUI adoption is not performed until an actual tool demonstrates repayment and target-platform evidence.
