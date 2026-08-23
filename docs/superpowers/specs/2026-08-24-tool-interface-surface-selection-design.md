# Tool Interface Surface Selection Design

## Status

- approval: user-approved in the current conversation on 2026-08-24
- authority: Base reusable method/pattern only; no project canon mutation
- scope: tool-interface selection policy and reusable case guidance
- out of scope: reviving Tool Hub, QA Evidence Studio, Figma-first workflow, external HTML dashboards, or adding a new broad Skill

## Problem

Base currently favors repository-native automation, Notion human-facing planning, and runtime evidence while explicitly retiring prior dedicated management/visual execution surfaces. That simplification is correct, but it leaves one reusable decision under-specified: when a recurring tool should expose only a CLI, when a TUI is justified, and when a thin graphical interface materially improves human operation without becoming a competing authority.

The external source reviewed for this change argues that agent-assisted native UI generation has reduced some historical GUI implementation cost while CLI remains uniquely valuable for automation and remote control. It also argues that many benefits commonly attributed to TUI—keyboard-first operation and high information density—are design properties that can be implemented in GUI. However, its direct validation is primarily macOS/SwiftUI, so Base must not generalize that experience into a universal GUI-first rule.

## Decision

Adopt `TOOL_INTERFACE_SURFACE_SELECTION` as a reusable decision pattern.

The default architecture is:

```text
Reusable Core / Library
→ machine-readable CLI or stable programmatic contract
→ choose optional human-facing surface from actual usage constraints
   → CLI only
   → TUI
   → thin GUI
```

The interface surface is a presentation/operation adapter. It does not become a new project canon, runtime authority, or independent state owner.

## Selection contract

### CLI

Prefer CLI when one or more of these dominate:

- automation, CI, scripting, agent/tool invocation, or composability;
- deterministic replay and easy testability matter more than visual discoverability;
- headless or remote execution is normal;
- output can be represented well as structured text/JSON/files;
- the task is infrequent enough that a separate human UI would not repay lifecycle cost.

CLI is the default machine-facing contract when practical. A GUI/TUI may wrap it or share the same core, but must not fork business logic.

### TUI

Choose TUI only when terminal residency is itself a material requirement, such as:

- SSH/tmux workflows where leaving the terminal is costly;
- low-bandwidth remote operation;
- cross-platform terminal deployment where a graphical runtime would add disproportionate burden;
- keyboard-first dense monitoring/operation that genuinely benefits from living beside shell tools.

Do not select TUI merely because it appears faster to implement. Do not claim accessibility superiority by default; accessibility must be validated in the actual target environment.

### Thin GUI

Choose a thin GUI when repeated human operation materially benefits from capabilities that are costly or awkward in terminal interfaces, including:

- image/visual comparison, previews, drag-and-drop, spatial arrangement, or direct manipulation;
- multiple synchronized panels/windows or dense visual filtering;
- standard platform controls and discoverability;
- repeated selection, inspection, triage, or side-by-side review where interaction friction dominates implementation cost.

A GUI should remain keyboard-capable when the workflow is expert/dense. Mouse-first behavior is not assumed.

## Architecture boundary

```text
canonical data / repository / project runtime truth
                 ↓
        reusable domain core
                 ↓
      stable CLI / API contract
          ↙             ↘
       TUI              thin GUI
```

Rules:

1. `CORE_LOGIC_SINGLE_OWNER`: domain logic and state mutation live below interface adapters.
2. `CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL`: machine automation must not require screen scraping or GUI-only actions when a stable programmatic path is feasible.
3. `SURFACE_DOES_NOT_OWN_CANON`: CLI/TUI/GUI surfaces do not create a second data or project truth.
4. `HUMAN_SURFACE_REQUIRES_REPAYMENT`: a TUI/GUI is justified by recurring user-value or operational savings, not novelty.
5. `KEYBOARD_FIRST_IS_CROSS_SURFACE`: high information density and keyboard efficiency are design goals, not TUI-exclusive properties.
6. `NO_DEPRECATED_SURFACE_REVIVAL`: this pattern must not revive Tool Hub, QA Evidence Studio, Figma-first, or external dashboard authorities.
7. `ZERO_INCREMENTAL_COST_DEFAULT`: prefer current/free/local capabilities; a new paid runtime or subscription requires separate evidence and user approval.

## Decision gate

For a new or materially revised internal tool, compare at least these three materially distinct candidates when applicable:

| Candidate | Strength | Typical risk |
| --- | --- | --- |
| CLI-only | simplest automation and lowest surface cost | human discoverability/visual comparison can be poor |
| CLI + TUI | terminal residency and remote density | terminal rendering/accessibility/interaction complexity |
| core/CLI + thin GUI | strong repeated human operation and visual workflows | extra UI stack, platform validation, lifecycle cost |

Selection must consider:

- primary operator: agent/automation vs human;
- frequency and duration of human interaction;
- remote/SSH requirement;
- visual/spatial information need;
- keyboard density requirement;
- target platforms and packaging burden;
- accessibility requirements;
- testability and deterministic replay;
- lifecycle cost and dependency count;
- incremental monetary cost;
- ability to reuse the same domain core.

## Implementation Reality Gate

A generated or implemented UI is not considered validated because it compiles or looks plausible.

Evidence ceiling:

```text
DESIGN_ONLY
→ STATIC_BUILD_VERIFIED
→ INTERACTION_PATH_VERIFIED
→ TARGET_PLATFORM_VERIFIED
→ HUMAN_WORKFLOW_VALUE_VERIFIED
```

Required checks depend on the claim, but may include:

- actual build/package on the claimed target OS;
- keyboard navigation and mouse behavior where supported;
- window resizing/scaling and relevant resolutions;
- file/drag-and-drop behavior when required;
- error/recovery paths;
- accessibility semantics or platform checks when accessibility is claimed;
- comparison against the CLI-only baseline for repeated-work savings;
- exact project/build identity for evidence.

No macOS-only result may be promoted to Windows/Linux support without target-platform evidence.

## Base integration

This pattern belongs in existing owners rather than a new broad Skill:

- `docs/BENCHMARKING_REFERENCE_GUIDE.md`: reusable `TOOL_PATTERN` extraction and ADOPT/ADAPT/REJECT guidance;
- `docs/CAPABILITY_COMPOSITION_MAP.md`: surface-selection composition and authority boundary;
- `docs/knowledge/cases/`: one reusable case recording the external observation, counterarguments, limits, and Base adaptation;
- focused regression contract: prevent accidental GUI-first/TUI-ban interpretation and prevent revival of deprecated management surfaces.

## Non-goals

- No requirement that every CLI receive a GUI.
- No blanket ban on TUI.
- No claim that native GUI is universally cheaper than web/TUI/CLI.
- No new desktop framework dependency.
- No project migration in this change.
- No mutation of open PR #630 or #631.

## Acceptance criteria

1. Base documents expose a clear CLI/TUI/thin-GUI selection gate.
2. CLI remains the preferred machine-facing automation contract where practical.
3. TUI remains valid for terminal-resident/remote workflows.
4. Thin GUI is conditional on measurable recurring human-operation value.
5. All surfaces share or wrap one domain core and cannot own canon independently.
6. Generated UI claims are bounded by the Implementation Reality Gate and target-platform evidence.
7. Deprecated Tool Hub/QA Studio/Figma-first/external dashboard authorities remain retired.
8. No new broad Skill, paid dependency, or project runtime mutation is introduced.
