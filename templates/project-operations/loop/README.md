# Project Execution Capsule Template

Copy this directory into `docs/operations/loop/` and bind every source to the exact project authority. The Capsule is not a second GDD or Art Bible.

Entry requires `PLANNING_LOCKED`, a compatible Visual Lock, `PROJECT_ADAPTER_VALIDATED`, and initialized Requirement Coverage. Figma is optional as a provider; the visual gate is not optional for visually affected packages.

A3 auto-merge stays empty and Scheduler stays `NOT_CONFIGURED` until separately validated.

## Completion

Readiness and completion are separate phases. The copied `VERIFICATION_RECEIPT.json` is completed only after approved requirements are closed, required checks have executable evidence, and required GitHub/Notion/other destinations have been read back.

```bash
python tools/check_loop_execution_capsule.py docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json --phase completion
```

Do not mark a destination `SYNCED` from a successful write alone. `expected_ref` and the fresh `observed_ref` must match. The Base-owned contract and adoption guidance are in `docs/COMPLETION_AND_DESTINATION_FRESHNESS_GATE.md`.
