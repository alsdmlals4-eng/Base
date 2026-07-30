# Capability Composition Map

Capabilities are selected by the problem, not artificially restricted to one tool or one document surface. Every use records its context, boundary, and evidence.

| Capability | Allowed contexts | Composition path | Prohibited boundary | Required evidence |
| --- | --- | --- | --- | --- |
| Visual structure (Whimsical/Mermaid) | GDD, external, both | concept → flow → decision → optional UI handoff | cannot own rules, values, or final pixel UI | responsible source + Decision ID or `DRAFT_VISUAL` |
| Visual UI (Figma) | GDD, external, both | UX contract → frame/state → pinned handoff → Godot comparison | cannot own game state or declare runtime complete | frame/node, snapshot, target input/resolution |
| Sheets GDD | GDD | canonical summary → user edit/proposal → GitHub comparison | cannot silently overwrite canon | source link, main SHA, reread status |
| GitHub contract | GDD, external, both | decision → document/schema → implementation handoff | cannot claim unrun runtime/human validation | commit/PR and validation record |
| Godot evidence | external, linked from GDD | pinned contract → render/input test → validation | cannot be inferred from a design tool | capture/test/log and explicit `NOT_RUN` gaps |

The map expands composition paths; it does not require a tool, artifact type, or context when the task does not benefit from it.
