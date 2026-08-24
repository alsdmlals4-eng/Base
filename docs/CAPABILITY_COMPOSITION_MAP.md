# Capability Composition Map

Capabilities are selected by the problem, not artificially restricted to one tool or one document surface. Every use records its context, boundary, and evidence.

| Capability | Allowed contexts | Composition path | Prohibited boundary | Required evidence |
| --- | --- | --- | --- | --- |
| Visual structure (Whimsical/Mermaid) | GDD, external, both | concept → flow → decision → optional UI handoff | cannot own rules, values, or final pixel UI | responsible source + Decision ID or `DRAFT_VISUAL` |
| Visual UI (Figma) | GDD, external, both | UX contract → frame/state → pinned handoff → Godot comparison | cannot own game state or declare runtime complete | frame/node, snapshot, target input/resolution |
| Sheets GDD | GDD | canonical summary → user edit/proposal → GitHub comparison | cannot silently overwrite canon | source link, main SHA, reread status |
| GitHub contract | GDD, external, both | decision → document/schema → implementation handoff | cannot claim unrun runtime/human validation | commit/PR and validation record |
| Godot evidence | external, linked from GDD | pinned contract → render/input test → validation | cannot be inferred from a design tool | capture/test/log and explicit `NOT_RUN` gaps |
| Tool interface surface (`TOOL_INTERFACE_SURFACE_SELECTION`) | BUILD, REVIEW, internal tools | reusable domain core → stable CLI/programmatic contract → optional TUI or thin GUI | surface cannot own canon/state or force GUI-only automation | selection trade study + target-platform/workflow evidence |
| AI game-engine machine boundary (`AI_GAME_ENGINE_MACHINE_BOUNDARY`) | BUILD, TEST, CI, agent-assisted engine/tool operations | exact project identity → typed operation → shared core → CLI/MCP adapter → behavior E2E → IRG evidence | cannot create a second engine/editor writer, infer behavior PASS from MCP connectivity, or turn a benchmark provider into a required runtime | schema/type contract + representative behavior E2E + structured execution evidence |
| External process overlay (`EXTERNAL_PROCESS_OVERLAY`) | PLAN, BUILD, REVIEW; environment-required process | environment/system process → Base routing → discipline owner → validation → execution report | execution-only; cannot own project canon or decisions, weaken Base gates, or manufacture duplicate approval | overlay source, actually applied process skills/gates, approval reuse/conflict, extra evidence |

## Tool interface surface selection contract

`TOOL_INTERFACE_SURFACE_SELECTION` chooses an operation/presentation surface from the actual operator, environment, interaction and lifecycle constraints. It is **not** a GUI-first rule and it does not prohibit TUI.

```text
canonical data / repository / runtime truth
→ reusable domain core
→ stable CLI / programmatic contract
   ├─ CLI
   ├─ TUI
   └─ thin GUI
```

Selection rules:

1. `CORE_LOGIC_SINGLE_OWNER`: domain logic and state mutation stay below the presentation adapters. CLI, TUI and thin GUI must share or wrap the same core rather than reimplementing business rules.
2. `CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL`: automation, CI, agent invocation and deterministic replay must not depend on screen scraping or GUI-only actions when a stable machine-facing contract is feasible.
3. `SURFACE_DOES_NOT_OWN_CANON`: an interface surface is an operation/presentation adapter. It cannot create a second project canon, structured data authority or runtime truth.
4. `HUMAN_SURFACE_REQUIRES_REPAYMENT`: add TUI or thin GUI only when recurring human-operation value repays implementation, packaging, testing and maintenance cost. Novelty or agent-generated implementation speed alone is insufficient.
5. `KEYBOARD_FIRST_IS_CROSS_SURFACE`: keyboard efficiency and high information density are interaction-design properties, not TUI-exclusive properties. Expert thin GUI workflows should retain keyboard operation when it improves throughput.
6. Prefer TUI when terminal residency is itself a material requirement, such as SSH/tmux operation, low-bandwidth remote work, or dense monitoring that must remain beside shell tools. Do not select TUI merely because it appears quick to scaffold.
7. Prefer thin GUI when repeated human work materially benefits from images/previews, visual comparison, drag-and-drop, spatial arrangement, synchronized panels, standard platform controls, or discoverability. Thin GUI remains an adapter over the same core.
8. `NO_DEPRECATED_SURFACE_REVIVAL`: this contract does not revive Tool Hub, QA Evidence Studio, Figma-first routing, external HTML dashboard/workspace authority, or any other retired execution/management surface. Reintroduction still requires its own current Existing Solution First comparison, lifecycle-cost evidence and user approval.
9. `ZERO_INCREMENTAL_COST_DEFAULT`: current/free/local capabilities remain the default. A new paid runtime, metered provider or subscription requires separate justification and approval.

When materially applicable, compare at least three candidates under the same criteria:

| Candidate | Best fit | Main risk |
| --- | --- | --- |
| CLI-only | automation, CI, agents, headless work, composability | weak discoverability or visual comparison for repeated human work |
| CLI + TUI | SSH/tmux/terminal-resident operation, low-bandwidth remote work | terminal rendering, interaction and accessibility burden |
| core/CLI + thin GUI | repeated visual/spatial inspection, selection and direct manipulation | extra UI stack, packaging and target-platform lifecycle cost |

Compare primary operator, interaction frequency, remote requirement, visual/spatial information need, keyboard density, target platforms, packaging burden, accessibility, deterministic testability, dependencies, lifecycle cost, monetary cost and reuse of the same domain core.

A generated or plausible-looking interface does not prove operation quality. Apply the evidence ceiling:

```text
DESIGN_ONLY
→ STATIC_BUILD_VERIFIED
→ INTERACTION_PATH_VERIFIED
→ TARGET_PLATFORM_VERIFIED
→ HUMAN_WORKFLOW_VALUE_VERIFIED
```

`TARGET_PLATFORM_VERIFIED` requires actual evidence on every platform being claimed. A macOS-only result cannot establish Windows/Linux support; accessibility claims likewise require evidence in the target environment. `HUMAN_WORKFLOW_VALUE_VERIFIED` additionally requires evidence that the added human surface actually reduces repeated-work friction or improves decision quality compared with the simpler machine-facing path.

## AI game-engine machine boundary contract

`AI_GAME_ENGINE_MACHINE_BOUNDARY` is a reusable pattern for game-engine and development-tool operations that must be callable by humans, CI, and agents without making a GUI, MCP transport, or benchmark provider a second authority. It extends the existing machine-facing surface rule; it does not select or replace the game engine.

```text
exact project identity
→ typed operation
→ reusable domain / engine-operation core
   ├─ CLI adapter
   └─ MCP adapter
→ behavior E2E
→ Implementation Reality Gate
→ structured execution evidence
```

Machine-boundary rules:

1. `PROJECT_IDENTITY_BEFORE_OPERATION`: resolve and validate the exact project identity, repository/workspace root, and relevant version/pin before an operation. Do not guess from whichever editor window, current directory, scene, port, or process happens to be active.
2. `SHARED_CORE_FOR_CLI_AND_MCP`: CLI, MCP, and any optional human surface call the same bounded operation core. They must not duplicate engine mutation rules, state transitions, validation, or evidence semantics in separate adapters.
3. `SCHEMA_GENERATED_TOOL_SURFACE`: when the implementation stack supports it, keep one closed operation schema/type source and generate or mechanically validate CLI arguments, MCP tool definitions/types, and representative test fixtures from that source. Code generation itself is optional when it adds no value; schema/type drift is not.
4. `MCP_E2E_BEHAVIOR_CONTRACT`: representative operations must have behavior E2E coverage through the real machine-facing adapter into the project/result/evidence boundary. Tool discovery, schema listing, server startup, or a successful handshake is transport evidence only.
5. `MCP_CONNECTED_IS_NOT_BEHAVIOR_PASS`: an MCP server being reachable does not establish that the requested engine action occurred, persisted correctly, targeted the intended project, or produced valid evidence. Promote the claim only after the applicable Implementation Reality Gate checks pass.
6. `NONINTERACTIVE_AUTOMATION_PATH`: approved bounded CI/agent operations should have a non-interactive path when practical, while preserving existing approval, security, destructive-action, and protected-path gates. Headless convenience cannot bypass authority checks.
7. `STRUCTURED_EXECUTION_EVIDENCE`: machine-facing execution records should bind the exact project/ref, tool or adapter version, typed operation, result state, changed artifacts or observed outputs, logs/evidence locations, and explicit `NOT_RUN`/`BLOCKED` gaps needed for the claim.
8. `ENGINE_AND_WRITER_AUTHORITY_PRESERVED`: this composition rule does not create a new engine, editor, MCP writer, or persistent mutation authority. Provider-specific benchmarks remain evidence inputs. Current project/Base authority decides what engine and tool owns each action.
9. `NO_BENCHMARK_RUNTIME_DEPENDENCY_BY_DEFAULT`: extracting a useful architecture from an external engine/tool does not install that engine, CLI, SDK, service, or paid dependency. Runtime adoption requires a separate Existing Solution First comparison and target-project evidence.

For current Godot work, this pattern composes with the existing P06 authority model rather than replacing it: Godot remains the engine, current authoring/test/live-QA owners retain their existing scopes, and any machine-facing improvement must preserve the single-writer boundary.

## External process overlay contract

`EXTERNAL_PROCESS_OVERLAY` is a composition role for an external process or orchestration framework that the current execution environment requires or that the user explicitly asks to use. Examples can include Superpowers-style brainstorming, planning, TDD, debugging, review, or completion-verification workflows. The framework remains **process infrastructure**, not a new Base domain owner.

```yaml
external_process_overlay:
  authority: EXECUTION_PROCESS_ONLY
  overlay_name_or_source:
  applied_process_skills_or_gates: []
  approval_state: NEW_APPROVAL | REUSED_APPROVAL | NOT_REQUIRED | BLOCKED
  approval_reference:
  conflict_state: NONE | OVERLAY_CONFLICT | BLOCKED_UNVERIFIED
  extra_evidence: []
```

Composition rules:

1. The overlay may add a stricter brainstorming, planning, TDD, debugging, code-review, verification, or delivery step when the environment requires it. It does not silently create project scope, product direction, or repository canon.
2. The overlay **프로젝트 정본·CURRENT_CONFIRMED_DECISIONS를 소유하거나 덮어쓰지 않는다**. Project/domain canon continues to answer what is true; the overlay only constrains how the current worker executes the approved work.
3. The overlay **Base 안전·증거·보호 Gate를 약화하지 않는다**. A process framework may demand more evidence or an earlier design step, but it cannot convert `NOT_RUN`, `BLOCKED_UNVERIFIED`, protected-path constraints, or user-only decisions into a pass.
4. When the exact scope already has a valid approval reference and the overlay's own prerequisite gate has closed, use `REUSED_APPROVAL` and **동일 승인 범위를 재승인받지 않는다**. Re-open approval only when scope, core assumptions, protected behavior, or user-decision content materially changes.
5. If the environment's process instruction and Base/project canon appear incompatible, record `OVERLAY_CONFLICT`. Follow the higher-priority execution instruction for the current run while preserving the repository's existing canon; do not rewrite canon merely to make the process conflict disappear. If the safe resolution cannot be established, remain `BLOCKED_UNVERIFIED`.
6. Reading an external skill or instruction is not the same as executing it. The execution report records `overlay_name_or_source`, `applied_process_skills_or_gates`, `approval_reference`, reuse/conflict state, and `extra_evidence` actually produced.
7. A repeated external process pattern becomes a Base Skill only if it later proves an independent reusable input/output/authority/validation boundary and passes the normal Base promotion/consolidation gates. The overlay role itself is not a reason to add a Skill.

The map expands composition paths; it does not require a tool, artifact type, process framework, or context when the task does not benefit from it. It also does not turn an external framework's internal instruction hierarchy into Base canon; current environment instructions and Base/project authorities remain separate evidence layers that must be reported when they interact.
