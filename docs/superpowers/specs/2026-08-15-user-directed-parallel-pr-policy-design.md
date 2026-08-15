# User-Directed Parallel PR Policy Design

## Goal

When a user explicitly asks work to continue and a same-goal PR is already open/draft/ready, do not modify that in-progress PR and do not stop solely because it exists. Start independent user-directed work from the current completed `main` on a new branch/PR. Treat PR creation authority separately from overlap merge authority.

## Existing owners

Absorb the user-directed start rule into `managing-project-intake-and-work-contract` / `continuous-work-execution.md`. Do not create a new Skill, Work Mode, or repository automation owner.

Actual concurrent ownership and overlap disposition remain owned by `synchronizing-local-and-github-state`. If its preflight classifies the new work as `SAME_GOAL`, `PATH_OVERLAP`, or `SEMANTIC_OVERLAP`, use its existing `PROVISIONAL_INTEGRATION` contract rather than inventing a second merge rule.

## Scope split

### Interactive / user-directed work

- inspect same-goal open/recent PRs for overlap and risk;
- never push to, rebase, update, close, or merge another in-progress PR unless the user explicitly assigns that PR;
- an existing same-goal open PR is not by itself a global blocker when the user explicitly instructs work to continue;
- create a new branch from the current completed `main` and a separate PR for the requested work;
- run `synchronizing-local-and-github-state` concurrent preflight before persistent writes/PR merge decisions;
- if there is no actual overlap, use the normal separate-PR merge gate;
- if actual overlap is explicitly authorized, keep it classified as `PROVISIONAL_INTEGRATION`: owner PR branches remain read-only, owner/main changes trigger semantic reconciliation and fresh exact-head validation, and the new PR must not merge until each overlapping owner is resolved;
- if another PR merged first, remove already-landed duplicate work and retain only still-material delta; if no material delta remains, close the new PR as `superseded` rather than creating churn.

### Scheduled / periodic repository-writing automation

This policy does not weaken active-PR guards owned by scheduled/periodic automation. Such automation may remain fail-closed while open work PRs exist. The scheduled automation active-PR guard is a separate, stricter safety boundary.

## Safety boundaries

- current completed `main` is the baseline for the new user-directed branch;
- no force push, direct `main` push, `--admin`, ruleset bypass, or mutation of another PR branch;
- same-goal PRs are evidence/overlap inputs, not authority to adopt their unmerged code;
- explicit user authorization can allow provisional work to proceed, but does not convert overlap to `CLEAR`;
- `PROVISIONAL_INTEGRATION` owner-resolution and semantic-reconciliation gates take precedence over inherited merge authority;
- exact-head CI, unresolved review threads, current-main ancestry, and repository merge rules still gate merge;
- completed/merged work remains the only canonical retained change for post-change monitoring.

## Adversarial cases

1. **Duplicate PR merges first:** reconcile the new PR against new `main`; drop duplicate portions and close as `superseded` if no material delta remains.
2. **Open PR contains useful but unmerged code:** read-only comparison is allowed; do not treat it as canonical or push to it.
3. **Paths or semantic resources overlap:** independent work may continue only as explicitly authorized `PROVISIONAL_INTEGRATION`; owner branches remain read-only and the provisional PR must not merge until owner resolution.
4. **GitHub says mergeable and CI is green:** this does not satisfy unresolved owner overlap; semantic reconciliation and owner resolution remain mandatory.
5. **Scheduled automation sees open PR:** this design does not authorize it to continue; its own active-PR guard remains authoritative.

## Verification

Extend `tests/test_continuous_work_execution_contract.py` to require the explicit interactive/scheduled split, new-PR-from-current-main behavior, and delegation of actual overlap to the canonical `PROVISIONAL_INTEGRATION` owner. Keep an allowlisted companion assertion in `tests/test_claim_evidence_binding.py`. Run the existing Base required workflows on the exact reviewed head before merge.
