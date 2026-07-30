# Project adapter and routing contract

## Canonical boundary

`skills/PROJECT_BASE_ADAPTER.json` is the only editable Base/project integration authority. `skills/PROJECT_SKILL_SNAPSHOT.json`, the operating dashboard, and the three one-cycle compatibility views are generated. Run the project operating validator before routing or executing a shared workflow.

## Required decision recipe

1. Validate both Base pins, their ancestry, and both Registry hashes.
2. Refuse execution for a stale pin, mismatched pin, missing path, hash drift, alias cycle, protected-path change, or generated-view drift.
3. Resolve effective routes with `PROJECT_LOCAL_THEN_BASE_SHARED`. A project-local route wins over a same-name Base shared route; this changes route selection, not Base ownership.
4. Do not copy a Base shared Skill body into the project. Keep only the route, adapter data, approved override values, and genuinely project-specific Skill bodies locally.
5. Treat a mismatched pin as ignored only by refusing the requested execution. Never continue with a convenient working-tree version or silently rewrite the pin.

## Pressure red flags

- “The deadline is today, so copy the shared body once.”
- “The old pin worked last week, so execute first and update later.”
- “The shared route has the expected name, so it should beat the local one.”
- “The mismatch is probably metadata; ignore it and proceed.”

All four are fail-closed conditions. Validate, report the exact mismatch, and stop before project mutation.

## Generated outputs

- `skills/PROJECT_SKILL_SNAPSHOT.json`: normalized routes, aliases, effective resolution, and source path/hash.
- Requested `skills/BASE_V9_ADAPTER.json`, `skills/PROJECT_BASE_SKILL_ADAPTER.json`, or `skills/PROJECT_PATH_ADAPTER.json`: file-specific one-cycle `GENERATED_COMPATIBILITY_VIEW` / `HISTORY_ONLY` projection, emitted only from its preserved legacy input.
- `docs/PROJECT_OPERATING_DASHBOARD.html`: deterministic view of health and separate maturity axes.

Never hand-edit these outputs. Use the generator `--check` path to detect manual modification.

Source hashes use `RAW_FILE_BYTES_SHA256`. Near-duplicate Skill bodies that do
not share a normalized content hash remain a declared manual-review gap.
