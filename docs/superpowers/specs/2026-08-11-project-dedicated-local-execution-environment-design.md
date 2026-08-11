# Project-Dedicated Local Execution Environment Design

**Date:** 2026-08-11 KST  
**Status:** USER-APPROVED DESIGN / IMPLEMENTATION ACTIVE  
**Shared Base owner:** `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`  
**New shared invariant:** `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`  
**GRIMOIRE consuming Decision ID:** `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`  
**Product decision change:** `false`

## Goal

For any user-executed local PowerShell/Codex task, never assume an earlier shell is still open or still contains the correct project environment. Establish or repair the project-dedicated local execution environment first, then provide one self-contained copy/paste PowerShell launcher before the Codex task prompt.

For Godot projects the generic environment shape is:

```text
fresh PowerShell process
→ dedicated/self-contained Godot
→ project-scoped HiGodot profile/server/ports
→ project-scoped executor profile/CODEX_HOME
→ project-adopted live-QA profile when required
→ Codex -C <exact project/worktree>
→ fresh project-authorized HiGodot receipt
→ live-QA only inside its existing non-authoring boundary
```

`dedicated PowerShell` means a new PowerShell process with project-specific environment injected into it, not a separately installed PowerShell binary.

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

## Base ownership boundary

Base extends the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` and the existing `godot-live-editor-operations` template. It does not create a parallel bootstrap Skill or second persistent authoring authority.

The Godot template already owns generic Hera guidance. Therefore Base **may name Hera generically** as an adopted live-QA example/owner, but it must not hard-code consuming-project values such as GRIMOIRE paths, worktrees, ports, exact project CODEX_HOME, Hera project token/profile, or GRIMOIRE-specific exact version policy.

Generic Hera boundary remains:

```yaml
role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
persistent_source_mutation: forbidden
authoring_authority: false
```

HiGodot remains the sole persistent Godot authoring authority when the consuming project adopts that model.

## Required handoff order

Whenever the user must run the local step manually, the response order is:

```text
1. Tell the user to open a new PowerShell window.
2. Give one complete copy/paste PowerShell block first.
3. Inside that block:
   resolve exact project/worktree
   → verify/create-or-repair project-dedicated environment
   → reuse/start exact Godot
   → verify/start-or-attach exact project HiGodot profile/ports
   → set exact project CODEX_HOME/executor profile
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
OTHER_PROJECT_GODOT_FALSE_MATCH
DUPLICATE_MATCHING_EDITOR
OTHER_PROJECT_HIGODOT_PORT_OR_PROFILE
PROJECT_PORT_COLLISION
GLOBAL_CODEX_HOME_LEAKAGE
MISSING_CODEX_HOME
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

## GRIMOIRE consumer

GRIMOIRE binds the rule under the existing Decision ID:

```text
GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01
```

GRIMOIRE concrete local shape is project-owned, not Base-owned:

```text
fresh PowerShell
→ self-contained GRIMOIRE Godot 4.7.1
→ project-scoped HiGodot 3.1.4 profile/ports
→ project-scoped CODEX_HOME
→ Hera 1.0.0 exact pair when Task acceptance requires live QA
→ Codex exact requested GRIMOIRE worktree
→ fresh godot-ai receipt
→ Hera LIVE_QA_AND_OBSERVABILITY_ONLY
→ HERA_SOURCE_DELTA: NONE
```

The project must fresh-read current HiGodot/Hera profile details before generating each execution packet. Base does not own those concrete values.

For GRIMOIRE local-task responses, the PowerShell bootstrap always appears before the Codex prompt because the user may close PowerShell after every session.

## Synchronization

Base and GRIMOIRE are separate repository work units. After Base merged-main readback, GRIMOIRE canon is updated under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` with a fresh non-colliding Sync ID. Google Sheet then receives the same Decision ID/Sync ID after fresh cell readback.

This operating-policy sync must not falsely promote Task8 product completion.

## Acceptance

Base focused RED→GREEN must prove:

- dedicated environment first;
- previous PowerShell assumed closed;
- create/repair before product work;
- one launcher block before Codex prompt;
- adversarial launcher review;
- project-adopted live-QA remains non-authoring;
- no GRIMOIRE-specific local literals leak into shared policy/template.

GRIMOIRE acceptance must prove:

- self-contained Godot → project HiGodot → project CODEX_HOME → Hera-if-required → Codex ordering inside a fresh PowerShell;
- Hera remains live-QA/observability only with `HERA_SOURCE_DELTA: NONE`;
- missing dedicated components route to environment creation/repair first;
- no Task8 product source mutation is part of the operating-policy sync.

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

This does not create a new broad Base Skill, require a separately installed PowerShell binary, require shells to remain open, define universal project paths/ports/profiles, treat process/port existence as readiness, move persistent authoring away from HiGodot, grant Hera persistent authoring authority, change Task8 gameplay, pull Task9 scope forward, or authorize destructive repository cleanup.
