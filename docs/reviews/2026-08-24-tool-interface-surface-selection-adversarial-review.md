# Adversarial Review — Tool Interface Surface Selection

Date: 2026-08-24
PR: #632
Scope: `TOOL_INTERFACE_SURFACE_SELECTION` design, owner integration, reusable case, regression/CI wiring

## Full-loop protocol

Each loop attacks the whole approved scope rather than one isolated sentence: source interpretation → 3-option trade study → authority boundary → Base owner integration → regression evidence → Implementation Reality Gate. A valid finding is corrected before the next whole-scope loop. Open PR #630/#631 remain read-only throughout.

### Full Loop 1 — Is the new rule actually enforced, or only documented?

**Attack:** A regression file can create false confidence if permanent CI never executes it.

**Finding:** Initial PR CI passed even though `tests/test_tool_interface_surface_selection_contract.py` existed, because `validate-base-v9-rc.yml` uses an explicit unittest module list and the new module was not included.

**Refinement:** Add the focused module to the existing permanent Base v9 contract job. Do not add a second validation authority or one-shot success-only workflow.

**Validation:** After wiring, run `32669672320` produced the expected RED: the new contract test failed only because production owner docs did not yet contain `TOOL_INTERFACE_SURFACE_SELECTION` and its required invariants. This proved the regression was live before production changes.

**Whole-scope verdict after refinement:** enforcement path is real; proceed to owner implementation.

### Full Loop 2 — Did the source get distorted into GUI-first or a TUI ban?

**Attack:** The motivating article title can be overgeneralized into “never build TUI” or “native GUI is always cheaper now.”

**Validation:** The integrated contract explicitly keeps three candidates: CLI-only, CLI+TUI, and reusable core/CLI+thin GUI. TUI is retained for SSH/tmux/terminal residency and low-bandwidth remote operation. Thin GUI requires recurring human-work repayment. The reusable case explicitly REJECTs universal GUI-first generalization.

**Source-limit check:** The external article's direct implementation evidence is primarily macOS/SwiftUI. The Base contract therefore requires `TARGET_PLATFORM_VERIFIED` before Windows/Linux support claims.

**Verdict:** no new blocking finding.

### Full Loop 3 — Did the surface become a second state/canon owner or revive retired management tooling?

**Attack:** A “thin GUI” rule could silently rebuild Tool Hub/QA Evidence Studio/external dashboards or duplicate repository/Notion state.

**Validation:** The contract requires `CORE_LOGIC_SINGLE_OWNER`, `CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL`, and `SURFACE_DOES_NOT_OWN_CANON`. `NO_DEPRECATED_SURFACE_REVIVAL` explicitly retains the retirement of Tool Hub, QA Evidence Studio, Figma-first routing and external HTML dashboard/workspace authority.

**Protected pre-existing context:** `CAPABILITY_COMPOSITION_MAP.md` already contains legacy Figma/Sheets capability rows while the newer visual policy owns their current authority/retirement semantics. This task does not reinterpret or modernize those rows because Notion information-architecture work is active in protected PR #630. The new row cannot elevate them to canon and explicitly defers retired-surface reintroduction to a new comparison/approval gate.

**Open-PR collision check:** #630 and #631 are not modified, rebased, merged, closed or selectively copied.

**Verdict:** no new blocking finding in approved scope; protected pre-existing drift is not absorbed.

### Full Loop 4 — Are platform, accessibility or human-value claims stronger than the evidence?

**Attack:** Agent-generated UI may compile or look plausible on one platform while failing packaging, keyboard interaction, accessibility, resizing, file operations or other target OSes.

**Validation:** Evidence ceiling is explicit:

```text
DESIGN_ONLY
→ STATIC_BUILD_VERIFIED
→ INTERACTION_PATH_VERIFIED
→ TARGET_PLATFORM_VERIFIED
→ HUMAN_WORKFLOW_VALUE_VERIFIED
```

The contract forbids using one-platform evidence to claim other platforms and does not treat surface type alone as accessibility proof. Human-workflow value requires comparison with the simpler machine-facing baseline.

**Verdict:** no new blocking finding. Current PR itself only proves Base policy/contract behavior; it does not claim an actual GUI/TUI product reached target-platform or human-workflow verification.

### Full Loop 5 — Does the change improve long-term efficiency without creating another framework/Skill burden?

**Attack:** A reusable rule can still increase complexity if it introduces a broad Skill, UI framework, paid provider, duplicate state model or mandatory GUI work for every CLI.

**Validation:** No broad Skill, desktop framework dependency, paid capability, project runtime mutation or blanket GUI migration is added. Surface creation is conditional on `HUMAN_SURFACE_REQUIRES_REPAYMENT` and `ZERO_INCREMENTAL_COST_DEFAULT`. Benchmark extraction routes the result through existing `TOOL_PATTERN` and capability owners instead of creating another owner.

**Regression/lifecycle check:** The only CI expansion is one focused test module in the existing permanent Base v9 contract suite. The test also guards that deprecated management surfaces remain retired and that the capability map does not introduce `GUI_ALWAYS_FIRST` or `TUI_PROHIBITED` semantics.

**Verdict:** no new blocking finding.

## Five-loop result

- Full loops completed: 5/5
- Valid finding discovered: permanent CI did not initially execute the new regression
- Finding corrected: yes; existing Base v9 job now runs it and produced real RED before production owner changes
- New broad Skill: 0
- New paid/runtime UI dependency: 0
- Project canon/runtime mutation: 0
- Protected PR #630/#631 mutation: 0
- New P0: 0
- New P1: 0 after Loop 1 correction
- Remaining pre-existing protected context: legacy capability rows handled outside this PR; not promoted or modified here

## Implementation Reality Gate ceiling

This review plus final exact-head CI can prove that Base consistently documents and regression-guards the CLI/TUI/thin-GUI selection contract. It **cannot** prove that any concrete GUI/TUI implementation is usable, accessible, faster, cross-platform or valuable to a human operator.

Concrete tool adoption must separately climb from `DESIGN_ONLY` through `TARGET_PLATFORM_VERIFIED` and, when productivity value is claimed, `HUMAN_WORKFLOW_VALUE_VERIFIED`.

Final exact-head required gates must run after this review commit. This document alone is not merge evidence or `CLEAN_REVIEW_EXIT` evidence.
