# Skill Behavior and Evidence Hardening Design

## Status

Approved for implementation by the user on 2026-08-02 after the Base active-Skill audit.

## Problem

Base has strong static Skill contracts, routing fixtures, coupled-change rules, and CI coverage, but three evidence gaps remain:

1. `skills/SKILL_BEHAVIOR_EVALS.json` does not make active-Skill coverage completeness visible or fail when an active Skill has no primary routing case.
2. `tools/check_skill_behavior_evals.py` can score an external result file, but the result artifact has no dedicated schema or reproducibility metadata contract.
3. Reviewers cannot inspect one generated surface that shows, per active Skill, its routing cases and repository implementation evidence such as references, package scripts, tests, workflows, and knowledge state.

The result is a truthful but incomplete state: fixture contracts may pass while practical routing coverage and implementation evidence remain difficult to audit.

## Goals

- Detect active Skills that have no primary behavior-evaluation case.
- Detect active Skills that are never exercised as a non-selection or forbidden boundary.
- Define a strict, reproducible external model-result artifact with run and independence metadata.
- Generate a deterministic per-Skill evidence matrix from repository facts.
- Keep `MODEL_RUN_STATUS: NOT_RUN` truthful until an external result artifact is actually supplied and scored.
- Strengthen the existing `evolving-project-discipline-skills: behavior-eval` responsibility instead of adding a new broad Skill.

## Non-goals

- Do not call or pay for an external model from repository CI.
- Do not claim actual model routing passed without a scored result artifact.
- Do not change `skills/SKILL_REGISTRY.json`, Base v9.4 release locks, or frozen release artifacts.
- Do not modify project repositories or Google Sheets.
- Do not merge or rewrite open PR #134, #136, or #137.

## Design

### 1. Behavior coverage audit

Extend `tools/check_skill_behavior_evals.py` so contract validation builds coverage sets from active Registry entries and behavior cases.

For every active Skill:

- `primary_case_count >= 1` is required.
- `non_selection_case_count >= 1` is required, where non-selection means the Skill appears in `forbidden_skills` for a prompt where selecting it would be wrong.
- Supporting-only coverage does not satisfy primary coverage.
- Unknown, inactive, duplicated, selected-and-forbidden, or label-leaking cases remain failures.

The checker prints concise coverage totals and missing Skill IDs. `skills/SKILL_BEHAVIOR_EVALS.json` is expanded with focused cases until all active Skills satisfy both conditions.

### 2. Reproducible external result artifact

Add `schemas/skill-behavior-results-v1.schema.json` and `skills/SKILL_BEHAVIOR_RESULTS.template.json`.

The result artifact records:

- schema version and artifact role;
- repository and exact 40-character commit SHA;
- evaluation set path and SHA-256;
- Registry path and SHA-256;
- model/provider identifier and run timestamp;
- author context ID and reviewer context ID;
- whether the reviewer context is independent;
- one result for every behavior case;
- selected Work Mode, primary Skill, supporting Skills, Skill Modes, evidence, user decision state, and optional notes.

`tools/check_skill_behavior_evals.py --results <path>` validates the result schema before scoring. A result from a different commit, Registry hash, or evaluation-set hash fails closed.

### 3. Generated Skill evidence matrix

Add `tools/build_skill_implementation_evidence.py` to inspect active Registry entries and repository paths. It generates `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md` deterministically.

For each active Skill, the matrix reports:

- owner discipline and knowledge state;
- primary, supporting, and forbidden behavior-case counts;
- package references and package scripts;
- repository tests that mention the exact Skill ID;
- workflows that mention the exact Skill ID;
- implementation-evidence classification;
- external model-run state.

Evidence classification is conservative:

- `EXECUTABLE_EVIDENCE`: at least one package script/tool, test, or workflow consumer exists.
- `CONTRACT_EVIDENCE`: Skill body and routing cases exist but no executable consumer was found.
- `MISSING_EVIDENCE`: required package or primary behavior case is absent.

The generator does not claim a test passed; it only reports discoverable repository evidence. Actual CI and model-run status remain separate.

### 4. Integration and coupled-change protection

- Update `evolving-project-discipline-skills/SKILL.md` so `behavior-eval` explicitly requires coverage audit, reproducible result metadata, and generated evidence review.
- Update `skills/SKILL_LEARNING_LOG.md` with the observed gap, change, and remaining limits.
- Add focused tests for coverage failures, result-schema failures, commit/hash mismatch, and deterministic evidence generation.
- Update `.github/reference-freshness.json` so behavior-evaluation contract changes require the new tests and generated evidence artifact to stay synchronized.
- Preserve the released Registry bytes and lock hashes.

## Data flow

```text
SKILL_REGISTRY.json + SKILL_BEHAVIOR_EVALS.json
→ contract and coverage validation
→ optional external model execution outside CI
→ schema-valid result artifact
→ exact commit/hash verification
→ routing and evidence scoring

SKILL_REGISTRY.json + repository packages/tests/workflows + behavior cases
→ deterministic evidence builder
→ BASE_SKILL_IMPLEMENTATION_EVIDENCE.md
→ review and CI freshness checks
```

## Failure handling

- Missing primary or non-selection coverage: contract failure.
- Missing or malformed external result metadata: model-run failure.
- Commit or hash mismatch: model-run failure; never silently score stale results.
- Missing Skill package or generated evidence drift: test failure.
- No executable consumer: report `CONTRACT_EVIDENCE`, not failure by itself.
- No external result file: `MODEL_RUN_STATUS: NOT_RUN` remains a successful contract-only outcome.

## Testing

- Unit tests create temporary Registry/evaluation/result fixtures to verify coverage and schema boundaries.
- Evidence-generation tests compare generated output with the checked-in derivative and verify every active Skill appears exactly once.
- Existing Skill routing, reference freshness, release-lock, and neutral adversarial lifecycle tests remain unchanged and must pass.
- Exact-head GitHub Actions are the repository-level verification source when local full checkout is unavailable.

## Acceptance criteria

- Every active Skill has at least one primary behavior case and one forbidden/non-selection case.
- Result artifacts are schema-valid and tied to exact repository/evaluation/Registry hashes.
- Stale or incomplete result artifacts fail closed.
- The generated evidence matrix contains all 28 active Skills and is deterministic.
- The released Registry SHA-256 remains `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- No new broad Skill is added.
- External model behavior remains `NOT_RUN` unless a real result artifact is provided.

## Rollback

Revert the specification, implementation plan, checker changes, expanded fixtures, schema/template, generator, generated evidence, tests, Learning Log entry, and coupled-change update together. Registry and release-lock rollback is not required because they are protected and unchanged.
