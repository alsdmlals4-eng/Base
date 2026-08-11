# Project-Dedicated Local Execution Environment Design

**Date:** 2026-08-11 KST
**Status:** USER-APPROVED DESIGN / IMPLEMENTATION ACTIVE
**Shared Base owner:** `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`
**New shared invariant:** `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`
**Product decision change:** `false`

## Goal

For any user-executed local shell/Codex task, never assume an earlier shell is still open or still contains the correct project environment. Establish or repair the project's dedicated local execution environment first, then provide one self-contained copy/paste launcher before the Codex task prompt.

For Godot projects the generic environment shape is:

```text
fresh project-scoped shell process
→ dedicated/self-contained Godot
→ project-scoped HiGodot profile/server/ports
→ project-scoped executor profile/CODEX_HOME
→ project-adopted live-QA profile when required
→ Codex -C <exact project/worktree>
→ fresh project-authorized HiGodot receipt
→ live-QA only inside its existing non-authoring boundary
```

A `dedicated PowerShell` consuming project may define is a fresh PowerShell process with project-specific environment injected into it, not a separately installed PowerShell binary.

## Shared invariants

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY
```

If a required local component is absent, ambiguous, or belongs to another project, environment creation/repair precedes product work. Exact matching already-running components may be reused; unrelated processes are not killed to make room.

The launcher must not depend on variables, current directory, aliases, process handles, or shell state from an earlier session. It must not reset/restore/clean/stage/rewrite user work, and it must not require broad Git diff, repository-wide scans, or known line-ending/stat/index noise dumps merely to open Codex.

## Ownership boundary

Base extends the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` and the existing `godot-live-editor-operations` template. It does not create a parallel bootstrap Skill or second persistent authoring authority.

The Godot template already owns generic Hera guidance. Base may therefore name Hera generically as an adopted live-QA owner, but consuming-project exact versions, paths, worktrees, ports, executor homes, credentials, tokens, and profiles remain downstream project authority and are not copied into the shared owner.

Generic Hera boundary remains:

```yaml
role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
persistent_source_mutation: forbidden
authoring_authority: false
```

HiGodot remains the sole persistent Godot authoring authority when a consuming project adopts that model.

## Required handoff order

Whenever the user must run the local step manually, the response order is:

```text
1. Tell the user to open a new project-approved shell window.
2. Give one complete copy/paste launcher first.
3. Inside that launcher:
   resolve exact project/worktree
   → verify/create-or-repair project-dedicated environment
   → reuse/start exact editor/runtime
   → verify/start-or-attach exact project live-authority profile/ports
   → set exact project executor profile/CODEX_HOME
   → verify adopted live-QA profile when the task requires it
   → launch Codex in exact project/worktree
4. Only after Codex opens, give the Codex task prompt.
5. Codex must obtain fresh project/session/version/readiness evidence before persistent mutation.
```

The launcher proves orchestration only. Process existence, a listening port, or a Codex window is not readiness evidence.

## Environment creation / repair

If the dedicated environment does not exist, create/repair it before product implementation. Project-local/self-contained tooling is preferred when that is the project-approved model; do not silently replace global/system tooling.

Fail closed if creation requires an unresolved install location, credential, destructive migration, or port/profile decision not recoverable from current authority.

## Adversarial launcher review

Before presenting any local launcher, attack at minimum:

```text
WRONG_WORKTREE
WRONG_BRANCH_OR_TARGET_WHEN_REQUIRED
OTHER_PROJECT_EDITOR_FALSE_MATCH
DUPLICATE_MATCHING_EDITOR
OTHER_PROJECT_LIVE_AUTHORITY_PORT_OR_PROFILE
PROJECT_PORT_COLLISION
GLOBAL_EXECUTOR_PROFILE_LEAKAGE
MISSING_PROJECT_EXECUTOR_PROFILE
OTHER_PROJECT_LIVE_QA_PROFILE
LIVE_QA_TOKEN_OR_PORT_COLLISION
LIVE_QA_ACCIDENTAL_SOURCE_MUTATION
FRESH_SHELL_ENV_LOSS
PATH_WITH_SPACES_OR_QUOTING_FAILURE
PROCESS_EXISTS_BUT_NOT_READY
PORT_LISTENS_BUT_WRONG_PROJECT
KNOWN_LF_CRLF_OR_STAT_NOISE_FLOOD
RESET_RESTORE_CLEAN_SIDE_EFFECT
UNRELATED_PROCESS_KILL
BROAD_PRE_CODEX_DIAGNOSTIC_DUMP
```

A validated conflict is fixed in the launcher before handoff.

## Downstream synchronization

Base owns only the generic invariant. Each consuming project owns its concrete editor/runtime path, live-authority ports/profile, executor profile/CODEX_HOME, adopted live-QA exact pair, project worktree, and project-specific decision/sync records.

A consuming project may bind this shared rule under its existing tool-authority decision rather than creating a new product decision. Project canon and any project tracking sheet should use the same project Decision ID/Sync ID after merged Base readback.

The Base change itself does not promote any consuming project's product implementation status.

## Acceptance

Focused RED→GREEN must prove:

- dedicated environment first;
- previous PowerShell/shell may be assumed closed;
- create/repair before product work;
- one launcher block before Codex prompt;
- adversarial launcher review;
- project-adopted live-QA remains non-authoring;
- no consuming-project local literals leak into shared policy/template.

Existing Base operating-contract and Game Project OS consumers must remain green at the exact PR head.

## Post-change monitor loop

After implementation:

```text
attack
→ validate critique
→ same-goal open/recent PR recheck
→ untouched consumer/derivative recheck
→ classify OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP
→ minimal follow-up if validated
→ regression recheck
→ exact-head validation
→ merge
→ merged-main readback
→ post-merge PR/canon recheck
```

## Non-goals

This does not create a new broad Base Skill, require a separately installed PowerShell binary, require shells to remain open, define universal project paths/ports/profiles, treat process/port existence as readiness, move persistent authoring away from HiGodot, grant Hera persistent authoring authority, change consuming-project gameplay/product behavior, or authorize destructive repository cleanup.
