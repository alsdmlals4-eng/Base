# One-Click Play Handoff Implementation Plan

> Approved design: `docs/superpowers/specs/2026-08-06-one-click-play-handoff-design.md`

## Task 1 — Contract test (RED)

Create `tests/test_one_click_play_handoff_contract.py`.

Assert that active responsibility sources contain:

- default Project Play as the user verification entrypoint
- no manual Scene selection or editor setup
- commit·push → Fetch origin → Pull origin
- repository·branch·commit SHA in handoff
- runtime failure state `FAIL · RETEST_REQUIRED`

Run:

```bash
python -m unittest tests.test_one_click_play_handoff_contract
```

Expected RED: required contract phrases are absent from one or more active sources.

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

Update `templates/project-operations/AI_WORKFLOW.md` with the one-click handoff gate and Fetch/Pull delivery checklist. Do not create a second policy owner.

Run:

```bash
python -m unittest tests.test_one_click_play_handoff_contract
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

Run repository-required CI and reference-freshness checks. Open a Draft PR and report exact Branch, Commit, changed files, checks, remaining manual evidence and rollback.
