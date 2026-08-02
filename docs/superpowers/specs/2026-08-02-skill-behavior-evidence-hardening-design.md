# Skill Behavior and Evidence Hardening Design

## Status

Approved for implementation by the user on 2026-08-02 after the Base active-Skill audit.

## Problem

Base has strong static Skill contracts, routing fixtures, coupled-change rules, and CI coverage, but three evidence gaps remain:

1. `skills/SKILL_BEHAVIOR_EVALS.json` does not make active-Skill coverage completeness visible or fail when an active Skill has no primary routing case.
2. `tools/check_skill_behavior_evals.py` can score an external result file, but the result artifact has no dedicated schema or reproducibility metadata contract.
3. Reviewers cannot inspect one generated surface that shows, per active Skill, its routing coverage and explicitly registered repository implementation evidence.

The result is a truthful but incomplete state: fixture contracts may pass while practical routing coverage and implementation evidence remain difficult to audit.

## Goals

- Detect active Skills that have no primary behavior-evaluation case.
- Detect active Skills that are never exercised as a non-selection or forbidden boundary.
- Define a strict, reproducible external model-result artifact with run and independence metadata.
- Generate a deterministic per-Skill evidence matrix from explicit, validated repository evidence paths.
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

Extend `tools/check_skill_behavior_evals.py` so contract validation builds coverage sets from active Registry entries and the combined behavior cases.

- `skills/SKILL_BEHAVIOR_EVALS.json` preserves focused pressure, boundary, and regression fixtures.
- `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json` supplies the complete active-Skill coverage layer without obscuring the focused set.

For every active Skill:

- `primary_case_count >= 1` is required.
- `non_selection_case_count >= 1` is required, where non-selection means the Skill appears in `forbidden_skills` for a prompt where selecting it would be wrong.
- Supporting-only coverage does not satisfy primary coverage.
- Unknown, inactive, duplicated, selected-and-forbidden, or label-leaking cases remain failures.

The checker prints concise coverage totals and missing Skill IDs.

### 2. Reproducible external result artifact

Add `schemas/skill-behavior-results-v1.schema.json` and `skills/SKILL_BEHAVIOR_RESULTS.template.json`.

The result artifact records:

- schema version and artifact role;
- repository and exact 40-character commit SHA;
- evaluation-set paths and combined SHA-256;
- Registry path and SHA-256;
- model/provider identifier and run timestamp;
- author context ID and reviewer context ID;
- whether the reviewer context is independent;
- one result for every behavior case;
- selected Work Mode, primary Skill, supporting Skills, Skill Modes, evidence, user decision state, and optional notes.

`tools/check_skill_behavior_evals.py --results <path>` validates the result schema before scoring. A result from a different commit, Registry hash, evaluation-set hash, or same-context review fails closed.

### 3. Generated Skill evidence matrix

Add `skills/SKILL_IMPLEMENTATION_EVIDENCE.json` as the explicit evidence index and `tools/build_skill_implementation_evidence.py` as its validator and deterministic generator. The output is `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md`.

Automatic whole-repository string search was rejected because a Skill ID appearing in a test or document does not prove that the file exercises that Skill. The index therefore declares reviewed evidence paths explicitly and the generator verifies that every active Skill has exactly one entry and every declared path exists.

For each active Skill, the matrix reports:

- owner discipline;
- primary and forbidden/non-selection behavior coverage;
- explicitly registered test, tool, workflow, script, or contract paths;
- implementation-evidence classification;
- external model-run state.

Evidence classification is conservative:

- `EXECUTABLE_EVIDENCE`: at least one registered Test, Tool, Workflow, or Script path exists.
- `CONTRACT_EVIDENCE`: only a registered contract/documentation path exists.
- `MISSING_EVIDENCE`: required package, coverage, index entry, or evidence path is absent.

The generator does not claim a test passed; it only reports validated repository evidence links. Actual CI and model-run status remain separate.

### 4. Integration and coupled-change protection

- Update `evolving-project-discipline-skills/SKILL.md` so `behavior-eval` explicitly requires complete coverage, reproducible result identity, independent review metadata, and evidence-matrix review.
- Add `skills/evolving-project-discipline-skills/LEARNING_LOG.md` as a focused companion while preserving the released Registry and global Learning Log index.
- Add focused tests for coverage failures, result-schema and source-identity failures, independent-review failure, missing evidence-index entries, and deterministic evidence generation.
- Update `.github/reference-freshness.json` so behavior-evaluation and Skill-body changes require the focused tests, focused Learning Log, and generated evidence artifact to stay synchronized.
- Preserve the released Registry bytes and lock hashes.

## Data flow

```text
SKILL_REGISTRY.json
+ SKILL_BEHAVIOR_EVALS.json
+ SKILL_BEHAVIOR_COVERAGE_EVALS.json
→ contract and complete coverage validation
→ optional external model execution outside CI
→ schema-valid result artifact
→ exact commit/hash and independent-context verification
→ routing and evidence scoring

SKILL_REGISTRY.json
+ combined behavior cases
+ SKILL_IMPLEMENTATION_EVIDENCE.json
→ evidence-path validation
→ deterministic evidence builder
→ BASE_SKILL_IMPLEMENTATION_EVIDENCE.md
→ review and CI freshness checks
```

## Failure handling

- Missing primary or non-selection coverage: contract failure.
- Missing or malformed external result metadata: model-run failure.
- Commit, Registry hash, evaluation paths, or evaluation hash mismatch: model-run failure; never silently score stale results.
- Same-context or non-independent review: model-run failure.
- Missing Skill package, evidence-index entry, evidence path, or generated evidence drift: test failure.
- No executable consumer: report `CONTRACT_EVIDENCE`, not failure by itself.
- No external result file: `MODEL_RUN_STATUS: NOT_RUN` remains a successful contract-only outcome.

## Testing

- Unit tests create temporary Registry, evaluation, result, and evidence-index fixtures to verify coverage, schema, identity, and evidence boundaries.
- Evidence-generation tests compare generated output with the checked-in derivative and verify every active Skill appears exactly once.
- Governance tests verify Skill-body discovery, focused Learning Log limits, and reference-freshness coupled-change rules.
- Existing Skill routing, reference freshness, release-lock, and neutral adversarial lifecycle tests remain unchanged and must pass.
- Exact-head GitHub Actions are the repository-level verification source when local full checkout is unavailable.

## Acceptance criteria

- Every active Skill has at least one primary behavior case and one forbidden/non-selection case.
- Result artifacts are schema-valid and tied to exact repository/evaluation/Registry hashes.
- Stale, incomplete, or non-independent result artifacts fail closed.
- The explicit evidence index contains all 28 active Skills and only valid repository paths.
- The generated evidence matrix contains all 28 active Skills and is deterministic.
- The released Registry SHA-256 remains `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- No new broad Skill is added.
- External model behavior remains `NOT_RUN` unless a real result artifact is provided.

## Rollback

Revert the specification, implementation plan, checker changes, coverage fixtures, schema/template, evidence index and generator, generated evidence, tests, focused Learning Log, Skill integration, and coupled-change update together. Registry and release-lock rollback is not required because they are protected and unchanged.
