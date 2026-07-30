# Base v9.1 system map

Base v9.1 is a compatible operating layer over the preserved v9.0 release. It changes project integration contracts, not game product code.

```text
Base release payload commit
  -> Base release evidence commit (payload must be an ancestor)
  -> skills/PROJECT_BASE_ADAPTER.json (only editable project integration authority)
     -> Base and project Registry path/hash validation
     -> project-local/shared route resolution
     -> skills/PROJECT_SKILL_SNAPSHOT.json
     -> docs/PROJECT_OPERATING_HEALTH.json
     -> docs/PROJECT_OPERATING_DASHBOARD.html
     -> requested, source-backed one-cycle GENERATED_COMPATIBILITY_VIEW outputs
```

## Authority and routing

Base owns shared Skill bodies. Projects own canon, paths, project-specific Skills, protected paths, GDD Sheet bindings, and approved overrides. Route precedence is always `PROJECT_LOCAL_THEN_BASE_SHARED`; a local same-name route wins without duplicating a Base body.

The repository-discovered `.agents/skills/base-project-router/SKILL.md` is deliberately thin. It reads the canonical adapter and generated snapshot, refuses invalid state, and routes to the selected package.

## Integrity verdict rules

- `FAIL`: any stale or mismatched pin, failed ancestry, Registry hash mismatch, missing route/path, duplicate ID, alias cycle, copied shared Skill body, protected-path change, or generated-view drift.
- `BLOCKED`: required evidence cannot be obtained or a critical validator cannot run.
- `PASS_WITH_NOT_RUN_GATES`: static operating integrity passes, but runtime, device, accessibility, or human gates remain `NOT_RUN`.
- `PASS`: operating integrity and every applicable critical gate have direct evidence.

No score can hide a critical failure. Migration and execution fail closed, preserve the input, and report exact recovery commands.

## Cross-repository boundary

`tools/migrate_project_operating_contract.py` creates the canonical adapter without modifying legacy inputs and requires explicit lock-matching v9.1 pins plus an approved baseline commit. For a first migration it reads the explicit legacy input from that Git commit, extracts `/protected_paths`, and records `FIRST_MIGRATION_LEGACY_SOURCE` with the policy hash; missing or unextractable policy fails. Later waves may record `CANONICAL_ADAPTER_SOURCE`. `tools/build_project_operating_artifacts.py` runs the same full validator before writing or checking deterministic views. `tools/check_project_operating_contract.py` validates Base and project repositories together, verifies the exact commit-qualified policy source and hash, rejects weakening, and compares protected changes during standard `--check`.
