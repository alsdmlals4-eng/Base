# Copy Integration Default Design

## Status

```yaml
status: USER_APPROVED
approval_source: explicit_user_instruction_2026-08-16
policy_id: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
scope: Base shared repository work coordination
```

## Problem

Base currently has two partially conflicting concurrency rules:

1. explicit user-directed work may start a separate PR while another same-goal PR is open;
2. scheduled/periodic repository-writing automation stops whenever any foreign PR is open.

The second rule serializes unrelated work and creates long idle periods. The existing `PROVISIONAL_INTEGRATION` rule also requires a fresh per-case replacement approval even when the user has now selected copy-and-integrate as the standing Base workflow.

## Approved direction

Use **copy integration from latest completed `main`** as the default recovery path for concurrent PR/file conflicts.

```text
observe current main + open/recent PRs
→ classify NO_OVERLAP / PATH_OVERLAP / SEMANTIC_OVERLAP / SAME_GOAL
→ NO_OVERLAP: continue normally on a separate branch/PR
→ overlap: snapshot owner PR heads + changed paths + semantic resources
→ create a new integration branch from exact latest completed main
→ selectively copy/reproduce only the required material delta
→ semantically reconcile with stronger/newer main state
→ remove stale or duplicate pieces
→ exact-head validation + adversarial review
→ merge the integration PR when material coverage is complete
→ mark fully absorbed owner PRs superseded; preserve residual unique work when any remains
```

## Core contract

### 1. Owner PRs are read-only inputs

An in-progress PR is evidence, not the write target. Do not rebase, force-push, amend, or directly repair another active PR branch unless the user explicitly assigns that PR itself.

### 2. Latest completed main is always the integration base

The integration branch starts from the exact current completed `main`, never from a stale owner branch. If `main` moves, reconcile to the new `main` and rerun affected validation.

### 3. Copy is selective, not wholesale

Copy/reproduce only the material delta needed for the approved goal. Do not replace a whole file with a stale PR version when newer `main` content exists. Path overlap requires hunk/semantic reconciliation; semantic overlap can exist even when paths differ.

### 4. Standing replacement authority

`BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` is a standing user approval for this coordination method. A same-goal/path/semantic overlap may enter `PROVISIONAL_INTEGRATION` without asking the user again merely for replacement authority.

This standing authority does **not** authorize:

- product-scope expansion;
- destructive data migration;
- payment or account/security privilege expansion;
- direct `main` push, force push, `--admin`, ruleset bypass;
- claiming runtime/human evidence that was not run.

### 5. Merge gate changes

An overlapping owner PR no longer blocks the integration PR solely because it remains open. Merge is allowed when all of the following are true:

- exact current main has been reconciled;
- owner PR exact heads and overlap are recorded;
- every material owner delta needed by the approved goal is either absorbed, intentionally rejected with evidence, or preserved as residual work;
- no stale duplicate remains in the integration branch;
- required exact-head checks pass;
- unresolved review threads = 0;
- P0/P1 findings = 0;
- expected head is pinned at merge.

After merge:

- if an owner PR has no unique material delta left, comment that it was absorbed and close it as superseded;
- if unique work remains, keep it open but reduce the remaining scope conceptually to that residual delta; do not falsely mark it complete.

### 6. Scheduled/periodic automation

Open PR existence by itself is no longer a global blocker.

```text
foreign open PR exists
→ inspect changed paths / relevant semantic ownership
→ no overlap: continue analysis/write/validation/merge
→ actual overlap: use copy-integration reconciliation when deterministic and bounded
→ reconciliation not safely automatable: defer only the conflicted write/task, record the overlap, keep unrelated analysis/observation work running
```

The periodic Source Scan Queue must therefore remove the `any open PR => BLOCKED_ACTIVE_PR_GUARD` entry gate. It still fails closed when the open-PR set cannot be queried and that evidence is required for overlap classification.

## Data recorded for overlap

```yaml
copy_integration_policy: DEFAULT_ON_CONFLICT
standing_authorization: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
owner_pr_head_shas: {}
provisional_overlap_paths: []
provisional_semantic_resources: []
absorbed_owner_deltas: []
residual_owner_deltas: []
last_reconciled_main_sha:
expected_head_sha:
```

## Adversarial constraints

Reject these shortcuts:

1. copying an entire stale file over newer main;
2. treating GitHub `mergeable=true` as semantic reconciliation;
3. merging owner branches wholesale when only one file/hunk is needed;
4. closing an owner PR when unique unabsorbed work remains;
5. using the standing policy as permission for high-risk actions or scope expansion;
6. scheduled automation ignoring actual path/semantic overlap;
7. keeping unrelated open PRs as a reason to idle.

## Validation

Required contract coverage:

- sync policy recognizes standing copy-integration authorization;
- continuous-work policy no longer requires owner resolution before merge when material delta is absorbed;
- periodic Source Scan no longer blocks merely because a foreign PR exists;
- periodic Source Scan still detects actual overlapping paths before publish/merge;
- direct-main, force, admin and deferred auto-merge remain forbidden;
- exact-head validation and post-merge readback remain mandatory.

## Rollback

Revert the policy implementation PR as one unit. This restores the previous stricter concurrency behavior. No runtime/save/schema/project data migration is involved.
