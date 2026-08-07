# One-Click Play Handoff Implementation Plan

> Approved design: `docs/superpowers/specs/2026-08-06-one-click-play-handoff-design.md`
>
> Reconciliation 2026-08-07: the original focused-test path below is historical planning evidence. The active required-CI consumer is now `tests/test_repository_governance_baseline.py`, which carries the One-Click Play contract and the Godot entrypoint-extension regression. Do not recreate a duplicate standalone test file.

## Task 1 — Contract test (RED)

Original plan: create `tests/test_one_click_play_handoff_contract.py`.

Current implementation: keep the contract in the already-required `tests/test_repository_governance_baseline.py` suite so docs and contract CI both execute it.

Assert that active responsibility sources contain:

- default Project Play as the user verification entrypoint
- no manual Scene selection or editor setup
- commit·push → Fetch origin → Pull origin
- repository·branch·commit SHA in handoff
- runtime failure state `FAIL · RETEST_REQUIRED`

Current focused run:

```bash
python -m unittest tests.test_repository_governance_baseline
```

Expected RED for a new contract requirement: the required phrase or consumer link is absent from one or more active sources.

## Task 2 — Synchronization and handoff responsibilities (GREEN)

Update:

- `skills/synchronizing-local-and-github-state/SKILL.md`
- `skills/maintaining-project-context-and-handoff/SKILL.md`

Add a user-facing delivery path that distinguishes Fetch from Pull and requires local HEAD equality before runtime verification. Add repository, branch, commit, update steps, default Play, expected first screen, manual gates and rollback to the handoff output contract.

Run the focused contract test.

## Task 3 — Vertical Slice and runtime validation responsibilities (GREEN)

Update:

- `skills/designing-vertical-slices/SKILL.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`

Require default Project Play to reach a representative playable flow without manual Scene selection or editor configuration. Require boot, gameplay surface, success/failure, retry/edit/return evidence. Keep runtime/device/human gates fail-closed.

Run the focused contract test.

## Task 4 — Project operating template exposure

Expose the one-click handoff gate through the current project-operation templates without creating a second policy owner. The active PR consumes the policy through:

- `templates/planning/VERTICAL_SLICE_PLAN.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `templates/project-operations/HANDOFF.md`

Run:

```bash
python -m unittest tests.test_repository_governance_baseline
python -m unittest discover -s tests -p 'test_*.py'
```

## Task 5 — Reference freshness and adversarial review

Verify:

- no new Skill was introduced
- existing responsibility boundaries remain distinct
- no implication that packaging PASS equals runtime PASS
- validation harness and platform overrides remain allowed
- no force push, hard reset or automatic overwrite path
- generated views or Registry changes are unnecessary because no Skill identity/path changed

Run repository-required CI and reference-freshness checks. Report exact Branch, Commit, changed files, checks, remaining manual evidence and rollback.

## Task 6 — Godot bounded real-entrypoint clarification (2026-08-07)

User-approved requirement: when the delivery goal explicitly includes the user launching and validating the result in Godot, do not stop at an isolated Scene solely because the primary task folders are narrow.

TDD evidence:

- RED head: `bfc91f6eda5b31a28a13e55aa9aec4f3e08204f3`
- Required docs-validation failed because `application/run/main_scene` and the bounded integration contract were absent from `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`.
- GREEN implementation head before this reconciliation note: `f2c7f9fd903f043640df6c369cc27dbb7638250a`.

Required behavior:

- user-runnable Project Play makes the minimal real entrypoint integration part of the approved delivery edge
- for Godot this can include `project.godot` `application/run/main_scene`, MainMenu/App Router, and only the essential Autoload/InputMap/Resource links
- `B — actual project entrypoint integration` is the default when user real validation is part of the approved goal
- `A — isolated Scene` remains valid for explicit Main Scene preservation, intentional Prototype/Test Scene or fixture work, a new unapproved product decision, or unsafe/high-impact expansion without rollback
- structural Godot changes keep their existing rollback, diff, import/parse, test, and regression gates
- unrelated Project Settings cleanup or migration is not authorized by this rule

Adversarial checks:

- duplicate policy authority: reject; absorb into `ONE_CLICK_PLAY_HANDOFF_POLICY.md`
- over-broad scope: blocked by minimal integration-edge language
- false human-validation claim: existing `NOT_RUN / PASS / FAIL · RETEST_REQUIRED / BLOCKED` manual states remain authoritative
- test/validation harness regression: protected as an explicit exception
- duplicate PR: close the temporary duplicate and continue on PR #200
