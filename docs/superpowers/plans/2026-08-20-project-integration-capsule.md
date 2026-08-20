# Project Integration Capsule Implementation Plan

## Goal

Ship a fail-closed, zero-incremental-cost Base sidecar that verifies local receipts
binding one Git/Notion/Godot project without creating a new MCP or writer.

## Completed work

- [x] Inspect Base authority, skill, adapter, loop capsule, Notion, and HiGodot contracts.
- [x] Inspect open PR paths and avoid all paths owned by PR #556.
- [x] Compare monolithic MCP, API orchestrator, paid full-MCP, and modular local-first options.
- [x] Confirm current official plan and product constraints.
- [x] Add strict JSON Schema and non-ready template.
- [x] Add semantic/live local validator and machine-readable CLI.
- [x] Bind existing `PROJECT_BASE_ADAPTER` and `HIGODOT_ADOPTION_RECORD` by path/hash.
- [x] Add permanent CI test route and template discovery.
- [x] Add real temporary-Git-repository tests plus targeted process-failure mocks.
- [x] Complete five full-scope adversarial review loops with RED/GREEN evidence.
- [x] Run full local Base validation and compare full discovery with clean baseline.
- [x] Complete independent final code review and remediate all P0/P1 findings.
- [ ] Commit, push, open PR, verify CI and exact head, merge safely, verify main.

## Verification commands

```bash
python -m unittest tests.test_project_integration_capsule_contract -v
python -m unittest discover -s tests -v
python tools/build_base_v9_artifacts.py --check
python tools/run_local_validation.py --trusted-history-commit e222e93e79e95364dca668eaaf0f156676123342
git diff --check
git fsck --strict
```

The template schema smoke is:

```bash
python tools/check_project_integration_capsule.py \
  templates/project-operations/PROJECT_INTEGRATION_CAPSULE.json \
  --schema-only --format json
```

## Rollback

The feature adds a sidecar contract, template, schema, tool, test, and CI route, plus
optional safe-runner hooks in the existing Base release-lock validator/index. It does
not migrate a product project or Notion workspace. Revert the integration commit to
remove the complete change coherently. Do not delete Notion pages, Godot files,
credentials, adapters, or adoption records as part of rollback.
