# Universal Loop Capsule Contracts Evidence

## Identity

- Design merge: `ec0880cbda0517e62c9c404d17d9409cbc0cfa02`
- Protected-path prerequisite: PR #332 / merge `fe34a10a8607ff288d973bff8a6a0eee6545317c`
- M2 PR: `#333`
- Source main: `fe34a10a8607ff288d973bff8a6a0eee6545317c`

## TDD RED

- Intentional RED head: `cdefc65a1725378eec07439e7145108c78aae534`
- Base-v9 run: `31725452665`
- Result: `340` tests, one expected template failure, `12` expected missing-schema/module errors, and one configured Godot skip.
- Existing tests and generated/integrity checks passed before the new contract failures.

## Production GREEN

- Verified payload SHA-256: `30f4620ea80b8b8cb94f5dc92c98ab820233e53a0aa36078519796814a0054ef`.
- First production run `31727551366` reached all new Schema and semantic gates; one test fixture incorrectly violated Schema before reaching the intended missing-coverage finding.
- The fixture was corrected to retain a valid non-matching requirement entry.
- Second production run `31727717288` passed all six semantic contract tests and exposed a direct-CLI import-path defect.
- A direct CLI regression was added; the CLI now bootstraps the repository root before importing `tools.loop_contracts`.
- Corrected production run `31728168446` passed seven focused tests, direct CLI validation, payload SHA verification, and `git diff --check`, then created the production commit.
- Independent review found OS-dependent handling of `..\` references. Run `31728906263` added Windows-separator normalization and a cross-platform escape regression; focused tests passed.
- Temporary Payload fragments and write Workflows were removed before the final Ready-state exact-head validation.

## Production surface

- Eight closed JSON Schema Draft 2020-12 contracts.
- Valid project-operation templates.
- Fail-closed project-bound loader and bundle validator.
- Read-only `tools/check_loop_execution_capsule.py` CLI.
- Planning/Visual Lock, Package, Coverage, Active Run, and Immutable Run documentation.
- Existing Base-v9 CI consumer updated to execute the contract regression.

## Preserved boundaries

- No new ACTIVE Skill or Work Mode.
- No Agent Runtime or model call.
- No project product, planning canon, Figma file, asset, permission, or repository-setting mutation.
- Maximum initial autonomy remains A2.
- A3 allowlist remains empty.
- Scheduler remains `NOT_CONFIGURED`.

## Ready-state integration

- PR #333 changed from Draft to Ready for Review on `2026-08-14`.
- This user-authored evidence commit is the definitive Ready-state exact-head validation target.
- Independent review status before final workflows: P0 `0`, P1 `0`; the cross-platform path-isolation finding is fixed and covered by regression.

## Final integration target

- Complete Base-v9 and Game Project OS workflows.
- Independent review: P0 `0`, P1 `0`.
- Unresolved review threads `0`.
- Merge-time current-main and path-overlap preflight.
- Squash merge with expected head.
- Postmerge main readback and push workflows.

## Rollback

Revert the eventual M2 squash merge. Project repositories and product data are not migrated by this Base contract PR.
