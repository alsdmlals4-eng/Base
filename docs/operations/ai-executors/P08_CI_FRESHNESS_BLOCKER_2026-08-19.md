# P08 · CI Freshness Blocker Addendum — 2026-08-19

## Context

PR #535 initially reached head `caaf941ec6eb893a08121e682a3bfd7ac5d36fa6` after five full adversarial loops. Five relevant workflows were green, but `Validate Game Project Operating System / ubuntu-contract` failed the canonical reference freshness gate.

## Exact failure

`check_canonical_reference_freshness.py` reported two companion requirements after these P08-owned sources changed:

```text
skills/optimizing-ai-model-and-prompt-costs/SKILL.md
skills/orchestrating-deepseek-worktrees/SKILL.md
```

1. at least one companion under `skills/**/LEARNING_LOG.md`
2. at least one companion from the freshness config's fixed test allowlist

P08 can satisfy item 1 inside its owned Skill packages, so PR #535 added:

- `skills/orchestrating-deepseek-worktrees/LEARNING_LOG.md`
- `skills/optimizing-ai-model-and-prompt-costs/LEARNING_LOG.md`

Item 2 cannot be satisfied without leaving P08 write scope. The freshness allowlist contains tests such as `tests/test_gpt_codex_workflow_contract.py` and global/other-discipline skill tests, while the P08 Manifest authorizes `tests/test_ai_*.py`, `tests/test_*model*.py`, `tests/test_*source_radar*.py`, `tests/test_*deepseek*.py`, and new `tests/test_p08_*.py` only. `.github/reference-freshness.json` is CP0-protected.

Therefore P08 must not touch a foreign companion merely to make CI green.

## Loop 6 — full re-attack after exact-head CI

This is a sixth complete P08 attack triggered by real CI evidence, not a synthetic finding.

### Finding A — skill-learning companion

- severity: MUST_FIX
- owner: P08
- status: FIXED
- action: add Skill-local learning logs in each modified P08 Skill package

### Finding B — reference-freshness companion test ownership deadlock

- severity: BLOCKING_CROSS_PART
- owner: CP0 Integration, with P01/P02 ownership review as applicable
- status: OPEN
- reason: P08 Skill mutation is required to fix verified P08 authority/cost issues, but the global freshness rule requires a companion test that P08 cannot legally write.

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P08
  target_owner: CP0
  target_paths:
    - .github/reference-freshness.json
    - tests/test_p08_*.py
    - tests/test_gpt_codex_workflow_contract.py
    - other configured local-skill-contract companion tests
  reason: >-
    P08-owned SKILL.md changes fail the global reference-freshness gate unless a fixed-list companion test changes,
    but none of the currently configured acceptable test companions is a P08-owned/allowed test path.
  evidence:
    - PR #535 Game Project OS run 32223379656, ubuntu-contract canonical freshness failure
    - P08 Manifest owned/allowed test patterns
    - CP0 protection of .github/**
  required_semantic_change: >-
    Integration should make the freshness contract accept an owner-local focused test such as tests/test_p08_*.py,
    or explicitly assign a canonical cross-Part companion owner and synchronized change protocol without forcing
    a Part worker to violate Manifest scope.
  acceptance_criteria:
    - P08 SKILL.md changes can satisfy freshness using a P08-owned test companion
    - no weakening of canonical freshness coverage
    - no control-plane write by P08 worker
    - exact-head CI green
  blocking: true
```

## Decision after Loop 6

Do **not** bypass, force-merge, edit CP0, or modify P01/other-Part tests from this P08 branch.

The selected semantic design remains Alternative B (bounded P08 tightening), but PR #535 is not merge-ready until the blocking cross-Part freshness coupling is resolved by Integration or the appropriate owner.

```yaml
FULL_LOOP_COUNT: 6
P08_owned_MUST_FIX_remaining: 0
blocking_cross_part_finding: 1
unsupported_PASS: 0
CLEAN_REVIEW_EXIT: false
merge_ready: false
```

## Evidence ceiling

- PASS: P08-owned Skill-local Learning Log companion was added.
- PASS: before the blocker surfaced, Base v9, Evidence-Based Knowledge, Partition Contract, Skill Routing Precision, and Long-Horizon workflows were green at the previous exact head.
- FAIL: Game Project OS canonical reference freshness at the previous exact head.
- PENDING: workflows for the new Skill-local-learning head.
- NOT_RUN: local checkout scope command, local model-pattern unittest discovery, model behavior eval, provider billing/cache measurement, real external-executor runtime.

No failed or pending item is reported as PASS.
