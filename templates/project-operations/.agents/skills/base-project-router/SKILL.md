---
name: base-project-router
description: Use when a project must resolve a Base shared route or a project-local route from repository contracts.
---

# Base Project Router

Confirm that `skills/PROJECT_BASE_ADAPTER.json` records a `protected_baseline` contract containing the approved commit, policy source type/path, `/protected_paths` JSON Pointer, and policy SHA-256. A first migration uses `FIRST_MIGRATION_LEGACY_SOURCE`; later waves use `CANONICAL_ADAPTER_SOURCE`. Then run `python tools/check_project_operating_contract.py --project-root . --base-repository ../Base --check` before reading `skills/PROJECT_SKILL_SNAPSHOT.json`. The validator reads the recorded commit-qualified source unless an explicit commit override is supplied. On any nonzero exit, stop without reading or executing routes.

After a zero exit, read `skills/PROJECT_BASE_ADAPTER.json` and the current generated snapshot. Refuse routing when the validator reports a stale pin, mismatched pin, hash drift, alias cycle, or generated-view drift.

Resolve `effective_routes` exactly as generated. A project-local route has precedence over a same-name Base route. The router contains no reusable workflow instructions; follow the selected canonical project package or Base package at its recorded path.
