# Base v9.5 Skill Operating Refinement Design

## Status

- Candidate label: `Base v9.5 focused maintenance candidate`
- Approval basis: the user approved option A and instructed implementation to proceed.
- Release claim: none. Base v9.4 remains the latest released compatible line.
- Protected history: released v9.0-v9.4 locks, evidence records, v7/v8 compatibility prompts, and historical Git records remain unchanged.

## Problem

Base already has strong file, schema, reference, and release checks, but four gaps remain:

1. current authority and frozen release derivatives are not explained clearly enough;
2. several active Skill descriptions consume more discovery context than necessary;
3. there is no reusable prompt-to-Skill behavior evaluation contract or scorer;
4. Issue #74's hypothesis, decomposition, multi-lens review, E2E, and learning requirements are distributed across existing procedures without one testable integration path.

## Goals

- Make the immutable v9.0 baseline, released v9.4 compatible line, current Registry, and historical generated artifacts distinguishable at cold start.
- Reduce aggregate active-Skill discovery metadata below 8,000 characters without changing Skill IDs, Registry triggers, responsibility boundaries, or required behavior.
- Add realistic prompt fixtures, expected routing, required output evidence, forbidden routing, and a deterministic result scorer.
- Integrate Build-Measure-Learn and Issue #74 into existing Skills rather than adding another broad Skill.
- Correct active documentation contradictions and release-history hierarchy without rewriting history.

## Non-goals

- Do not finalize, release, or pin Base v9.5.
- Do not modify `skills/SKILL_REGISTRY.json`, v9.4 release identity, project repositories, Google Sheets, product code, scenes, resources, assets, balance, or art direction.
- Do not delete or shorten v7/v8 compatibility fixtures.
- Do not claim that model routing quality passed unless actual model-run result files are scored.

## Architecture

### 1. Authority clarification

`docs/BASE_RULES_VERSION.md` will state four separate roles:

- immutable rules baseline: v9.0.0;
- latest released compatible line: v9.4.0;
- current active routing authority: Registry plus active Skill frontmatter;
- frozen v9.0 derivatives: plugin, lock, and snapshot, which are historical release artifacts rather than current routing authority.

The v9.4 release contract will move project adoption out of the completed release-stage list. The Changelog will place v9.4 entries at top-level release-history headings and mark the old merge-approval entry as superseded.

### 2. Skill discovery budget

Only YAML `description` fields are shortened. Each description remains an observable trigger statement beginning with `Use when`, while process details stay in the Skill body and Registry. The budget calculation is deterministic:

```text
sum(len(skill_id) + len(description) + len(path)) for every active Skill)
```

The acceptance ceiling is 8,000 Unicode characters. This is a discovery guardrail, not a SKILL.md body-size limit.

### 3. Behavior evaluation

`skills/SKILL_BEHAVIOR_EVALS.json` will hold non-leaking Korean user prompts and expected contracts:

- expected Work Mode;
- expected primary and supporting Skills;
- expected Skill Modes;
- forbidden Skills;
- required evidence tokens;
- expected user-decision state.

`tools/check_skill_behavior_evals.py` will provide two deterministic operations:

- contract validation against the active Registry and actual Skill packages;
- scoring an external result JSON by exact routing and required-evidence rules.

The tool does not call a model. Contract validation may pass while model execution remains `NOT_RUN`.

### 4. Issue #74 integration

The existing `decompose-and-sequence` reference will add:

- explicit hypothesis, minimum test unit, observation, success/failure thresholds, and decision after evidence;
- composite work decomposition from element purpose through interface integration;
- Build-Measure-Learn outcomes: keep, revise, reduce, remove, or retest.

The existing integrated review Skill will add four selectable lenses:

- Simplify;
- Style Guide;
- Domain Review;
- Security/Safety/Trust Boundary.

It will also name three mandatory result-path categories when applicable: Golden Path, Edge, and Regression. An omitted lens requires a reason.

The Skill evolution Skill will gain `behavior-eval` as an internal mode. Learning reports will distinguish reusable Base candidates from project-only findings.

## Files

### Create

- `skills/SKILL_BEHAVIOR_EVALS.json`
- `schemas/skill-behavior-eval-v1.schema.json`
- `tools/check_skill_behavior_evals.py`
- `tests/test_base_v9_5_skill_operating_refinement.py`

### Modify

- all active `skills/*/SKILL.md` frontmatter descriptions
- `skills/evolving-project-discipline-skills/SKILL.md`
- `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`
- `docs/BASE_RULES_VERSION.md`
- `docs/operations/BASE_V9_4_RELEASE_CONTRACT.md`
- `docs/CHANGELOG.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/SKILL_COVERAGE_MAP.md`
- `README.md`
- `skills/SKILL_LEARNING_LOG.md`

## Validation

1. Run the new focused test before implementation and confirm it fails for the intended missing contracts.
2. Implement the minimum changes until the focused test passes.
3. Run the behavior-eval contract checker.
4. Run Skill package, routing, reference-freshness, documentation-governance, v9.4, and full regression tests.
5. Run Base integrity and `git diff --check`.
6. Adversarially inspect untouched consumers, historical paths, release claims, and false model-evaluation claims.

## Acceptance criteria

- Active Skill IDs and Registry bytes are unchanged.
- Discovery metadata is at most 8,000 characters.
- At least eight realistic evaluation cases cover positive, negative, boundary, and cross-Skill routing.
- The scorer rejects missing expected Skills, forbidden Skills, wrong Work Mode, and missing required evidence.
- Issue #74's hypothesis, decomposition, four review lenses, three E2E paths, and Base/project learning boundary are testable.
- v9.4 project adoption is not presented as completed.
- Changelog hierarchy and merge-policy history are unambiguous.
- All executed checks and all unexecuted model/runtime/human checks are reported separately.

## Rollback

Revert only the v9.5 candidate files and edits. Released locks, evidence records, Registry bytes, and compatibility prompts remain valid and require no rollback.
