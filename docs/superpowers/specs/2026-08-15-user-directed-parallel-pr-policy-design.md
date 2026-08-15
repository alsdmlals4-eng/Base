# User-Directed Parallel PR Policy Design

## Goal

When a user explicitly asks work to continue and a same-goal PR is already open/draft/ready, do not modify that in-progress PR and do not stop solely because it exists. Start independent user-directed work from the current completed `main` on a new branch/PR, then reconcile at the merge gate.

## Existing owner

Absorb this rule into `managing-project-intake-and-work-contract` / `continuous-work-execution.md`. Do not create a new Skill, Work Mode, or repository automation owner.

## Scope split

### Interactive / user-directed work

- inspect same-goal open/recent PRs for overlap and risk;
- never push to, rebase, update, close, or merge another in-progress PR unless the user explicitly assigns that PR;
- an existing same-goal open PR is not by itself a global blocker when the user explicitly instructs work to continue;
- create a new branch from the current completed `main` and a separate PR for the requested work;
- before merge, re-read current `main` and same-goal PR state;
- if another PR merged first, remove already-landed duplicate work and retain only still-material delta; if no material delta remains, close the new PR as superseded rather than creating churn.

### Scheduled / periodic repository-writing automation

This policy does not weaken active-PR guards owned by scheduled/periodic automation. Such automation may remain fail-closed while open work PRs exist. PR #422 is an example of that separate safety boundary and is not modified by this change.

## Safety boundaries

- current completed `main` is the baseline for the new user-directed branch;
- no force push, direct `main` push, `--admin`, ruleset bypass, or mutation of another PR branch;
- same-goal PRs are evidence/overlap inputs, not authority to adopt their unmerged code;
- exact-head CI, unresolved review threads, current-main ancestry, and repository merge rules still gate merge;
- completed/merged work remains the only canonical retained change for post-change monitoring.

## Adversarial cases

1. **Duplicate PR merges first:** reconcile new PR against new `main`; drop duplicate portions.
2. **Open PR contains useful but unmerged code:** read-only comparison is allowed; do not treat it as canonical or push to it.
3. **Paths overlap:** independent PR may still be created on explicit user instruction, but merge must wait until current-main reconciliation proves a non-conflicting material delta.
4. **Scheduled automation sees open PR:** this design does not authorize it to continue; its own active-PR guard remains authoritative.

## Verification

Extend `tests/test_continuous_work_execution_contract.py` to require the explicit interactive/scheduled split and new-PR-from-current-main behavior in both the continuous-work reference and its owning Skill. Run the existing Base required workflows on the exact reviewed head before merge.
