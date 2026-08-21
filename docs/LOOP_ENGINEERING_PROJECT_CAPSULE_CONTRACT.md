# Loop Engineering Project Capsule Contract

Base owns a project- and genre-agnostic Kernel. Each adopted repository owns a declarative Capsule under `docs/operations/loop/`.

## Entry gate

```text
PLANNING_LOCKED
+ VISUAL_LOCKED or VISUAL_NOT_APPLICABLE
+ PROJECT_ADAPTER_VALIDATED
+ REQUIREMENT_COVERAGE_INITIALIZED
= AUTONOMOUS_IMPLEMENTATION_READY
```

Figma is an optional Visual Lock provider. A visually affected package still requires a Visual Lock. `NEW_VISUAL_REQUIRED` returns `USER_DECISION_REQUIRED`.

Requirement Coverage is bidirectional: every approved requirement needs tasks, outputs, tests, and evidence, and every output must be allowed by an approved package. Cross-project identity, stale source SHA, unsafe relative paths, omissions, and unauthorized additions fail closed.

The Capsule is not a second GDD or Art Bible. It binds exact authority documents. A3 remains empty and Scheduler remains `NOT_CONFIGURED` in v1.

Validate readiness with:

```bash
python tools/check_loop_execution_capsule.py templates/project-operations/loop/PROJECT_EXECUTION_CAPSULE.json --format json
```

## Completion phase

Readiness and completion are separate claims. The entry gate above remains the pre-execution readiness contract. When claiming a run complete or closed, follow [Completion & Destination Freshness Gate](./COMPLETION_AND_DESTINATION_FRESHNESS_GATE.md) and validate the completion receipt with:

```bash
python tools/check_loop_execution_capsule.py templates/project-operations/loop/PROJECT_EXECUTION_CAPSULE.json --phase completion --format text
```

Do not label a required GitHub, Notion, or other declared destination `SYNCED` until its observed readback matches the expected reference.
