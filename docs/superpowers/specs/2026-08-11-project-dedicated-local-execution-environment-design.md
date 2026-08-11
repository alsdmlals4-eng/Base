# Project-Dedicated Local Execution Environment Design

**Date:** 2026-08-11 KST  
**Status:** USER-APPROVED DESIGN / WRITTEN SPEC AWAITING USER REVIEW  
**Shared Base owner:** `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`  
**New shared invariant:** `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`  
**GRIMOIRE consuming Decision ID:** `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`  
**Product decision change:** `false`

## 1. Goal

When a project requires local PowerShell/Codex execution, the handoff must never assume that a previous PowerShell window, environment variable, current directory, or executor session is still alive.

Before product work begins, establish or reuse the project's dedicated local execution environment and provide **one complete copy/paste PowerShell block** that starts the exact local toolchain and Codex target.

For a Godot project, the required dedicated environment components are conceptually:

```text
dedicated self-contained Godot
→ project-scoped HiGodot server/profile/ports
→ project-scoped CODEX_HOME
```

The actual command execution always starts from a fresh PowerShell process:

```text
fresh project-scoped PowerShell
→ verify/create-or-repair dedicated Godot
→ reuse/start exact Godot
→ verify/start-or-attach exact project HiGodot profile/ports
→ set exact project CODEX_HOME
→ launch Codex -C <exact project/worktree>
→ obtain fresh project-authorized HiGodot receipt before persistent mutation
```

This is an execution-orchestration rule. It does not create a second persistent Godot authoring authority.

## 2. Definitions

### 2.1 Dedicated PowerShell

`dedicated PowerShell` does **not** mean a separately installed PowerShell binary.

It means a newly opened PowerShell process for the current local work request, with the target project's environment injected into that process.

Every local work request begins from:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
```

The handoff must therefore be self-contained and must not depend on variables, aliases, current directory, process handles, or shell state from an earlier user session.

### 2.2 Project-dedicated local execution environment

A project-dedicated local execution environment is the smallest isolated host-side toolchain needed to execute the project's approved workflow without silently borrowing another project's editor, ports, Codex profile, or shell state.

For Godot + HiGodot + Codex projects it includes:

1. a dedicated/self-contained Godot distribution approved by the project;
2. a project-scoped HiGodot configuration, including project-specific server/port/profile identity where applicable;
3. a project-scoped `CODEX_HOME`;
4. exact project/worktree identity passed to Codex;
5. a fresh PowerShell process for each user-executed local work session.

Already-running components may be reused only when their identity matches the requested project/worktree exactly.

## 3. Shared Base contract

Extend the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` owner instead of creating a competing broad Skill or second bootstrap policy.

The shared sequence becomes:

```text
LOCAL_WORK_REQUEST
→ ASSUME_PREVIOUS_POWERSHELL_CLOSED
→ resolve exact approved project/worktree
→ verify PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
→ if required environment is absent/incomplete:
     CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
→ adversarially review the launcher
→ provide ONE complete copy/paste PowerShell block
→ inside the fresh PowerShell:
     reuse/start exact project editor/runtime only
     → start/attach exact project-scoped live-authority service only
     → inject project-scoped executor profile/CODEX_HOME
     → launch Codex in exact project/worktree
→ obtain fresh project-authorized session/version/readiness receipt inside Codex
→ only then persistent project work
```

`BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY` remains valid. The new invariant strengthens what must exist before bootstrap; it does not authorize broad pre-launch diagnostics.

## 4. Environment creation/repair rule

If the project does not yet have a dedicated local execution environment, **environment creation or repair takes precedence over product implementation**.

The launcher must fail closed when a required project-local component is unavailable or ambiguous.

Creation/repair may establish project-local directories, approved self-contained tool distributions, project-specific HiGodot configuration, and project-specific Codex profile state, but must not:

- reset, restore, clean, stage, rewrite, or otherwise destroy user repository work;
- silently reuse another project's HiGodot ports/profile;
- silently use a global/default `CODEX_HOME` when a project-scoped profile is required;
- install or replace global/system tooling when the approved model is self-contained/project-local;
- kill unrelated editors/servers to free resources;
- declare readiness solely because a process exists or a port is listening.

If environment creation requires a new install location, credential, destructive migration, or unresolved port-policy decision that current authority does not determine, stop with `USER_DECISION_REQUIRED` rather than inventing a value.

## 5. One-block PowerShell handoff

Whenever the user must perform a local step manually, the response must put the bootstrap **before** the Codex task prompt.

Required response order:

```text
1. Open a new PowerShell window.
2. Paste one complete PowerShell block.
   - define exact project/worktree and project-local tool paths/profile inputs
   - validate/create-or-repair dedicated environment as authorized
   - reuse/start exact Godot
   - start/attach project-specific HiGodot profile/ports
   - set exact project CODEX_HOME
   - launch Codex -C <exact project/worktree>
3. After Codex opens, paste the Codex task prompt.
```

The PowerShell block must be executable from a fresh shell. It must not say or imply “use the PowerShell from earlier”, “keep the previous shell open”, or depend on variables defined in a previous message.

Project-specific literals remain in the consuming project's canon or execution packet. Base owns the invariant, not GRIMOIRE-specific paths, ports, versions, branches, or worktree names.

## 6. Adversarial launcher review

Before presenting a local launcher, attack it against at least these failure modes:

```text
WRONG_WORKTREE
WRONG_BRANCH_OR_TARGET_WHEN_REQUIRED
OTHER_PROJECT_GODOT_FALSE_MATCH
DUPLICATE_MATCHING_EDITOR
OTHER_PROJECT_HIGODOT_PORT_OWNERSHIP
PROJECT_PORT_COLLISION
GLOBAL_CODEX_HOME_LEAKAGE
MISSING_CODEX_HOME
FRESH_SHELL_ENV_LOSS
PATH_WITH_SPACES_OR_QUOTING_FAILURE
PROCESS_EXISTS_BUT_NOT_READY
PORT_LISTENS_BUT_WRONG_PROJECT
KNOWN_LF_CRLF_OR_STAT_NOISE_FLOOD
RESET_RESTORE_CLEAN_SIDE_EFFECT
UNRELATED_PROCESS_KILL
BROAD_PRE_CODEX_DIAGNOSTIC_DUMP
```

A launcher with a validated conflict must be corrected before it is handed to the user.

Prefer explicit project/worktree/executable/profile variables near the top of the block, bounded identity checks, and fail-closed errors that name the mismatch.

## 7. Evidence boundary

The launcher proves orchestration only. It does **not** prove:

- HiGodot server/plugin version;
- active project/session identity;
- readiness;
- successful persistent authoring;
- test success;
- product correctness.

Those claims require fresh project-authorized receipts after Codex starts.

For projects where HiGodot is the sole persistent Godot authoring authority, `.gd/.tscn/.tres/.res/project.godot` persistent authoring remains under HiGodot. PowerShell/Codex bootstrap does not weaken that boundary.

## 8. GRIMOIRE concrete consumer

GRIMOIRE binds this rule under the existing Decision ID:

```text
GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01
```

No new product Decision ID is created.

Current GRIMOIRE project-local shape:

```text
fresh PowerShell process
→ C:\Users\user\Tools\Godot-GRIMOIRE-4.7.1\Godot_v4.7.1-stable_win64.exe
→ exact requested GRIMOIRE project/worktree
→ project-scoped HiGodot 3.1.4 profile/server using GRIMOIRE-assigned ports
→ $HOME\.codex-grimoire
→ codex.cmd -C <exact GRIMOIRE worktree> <requested sandbox/approval mode>
→ fresh godot-ai exact-project/server/plugin/readiness receipt
```

The current GRIMOIRE HiGodot port convention is project-local authority and must be fresh-read before each execution packet rather than copied permanently into Base.

For every GRIMOIRE local-task response, the one-block PowerShell bootstrap appears **before** the Codex continuation prompt because the user may close PowerShell after every work session.

## 9. GRIMOIRE environment-absence behavior

If the GRIMOIRE dedicated local environment cannot be found, the next instruction creates or repairs that environment first rather than sending a product implementation prompt that assumes it exists.

The creation/repair gate establishes or verifies, as applicable:

- self-contained GRIMOIRE Godot distribution;
- exact approved Godot version/path;
- project-scoped HiGodot profile and GRIMOIRE port ownership;
- project-scoped `CODEX_HOME`;
- exact Git worktree target;
- Codex executable availability.

After creation/repair, a fresh one-block bootstrap is still required. Environment creation does not imply that a prior shell remains open.

## 10. GitHub / Sheet synchronization

The shared Base change and GRIMOIRE consumer are one approved operating-flow improvement but remain separate repository work units.

Base owns the generic invariant. GRIMOIRE owns concrete values.

GRIMOIRE GitHub canon and Google Sheet use the same existing Decision ID `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` for the project consumer sync. Select a fresh Sync ID immediately before writing after confirming no collision.

Sheet synchronization must not falsely promote Task8 product completion. It records only the operating-flow improvement and independently verified current local-tool evidence.

## 11. Testing and acceptance

### Base contract acceptance

Add focused RED→GREEN contract coverage proving that the shared owner requires:

- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`;
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED` semantics;
- create/repair-before-product-work when the dedicated environment is absent;
- one copy/paste launcher before the Codex prompt;
- no project-specific GRIMOIRE literals in Base shared policy/template;
- no weakening of HiGodot sole-authority boundaries;
- adversarial launcher review before handoff.

Run existing Base operating-contract and Game Project OS consumers unchanged.

### GRIMOIRE consumer acceptance

Update planning/operations canon under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` and verify:

- PowerShell bootstrap precedes Codex prompt in the documented local flow;
- fresh-shell assumption is explicit;
- self-contained Godot → project HiGodot → project `CODEX_HOME` → Codex order is explicit inside the fresh PowerShell launcher;
- absent environment routes to creation/repair first;
- no Task8 product source mutation is included in this operating-policy work unit;
- Google Sheet readback carries the same Decision ID.

## 12. Post-change adversarial monitor loop

After implementation, execute the current Base `POST_CHANGE_MONITOR_LOOP` against both shared and consuming surfaces:

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

Important consumers include Base GPT/Codex workflow policy, Godot live-editor operations template, project adapters/templates inheriting the bootstrap, GRIMOIRE development gates/current decisions/sync record, and the Google Sheet tool-authority row.

## 13. Explicit non-goals

This change does not:

- create a new broad Base Skill;
- require a separately installed PowerShell binary;
- require PowerShell to remain open between work sessions;
- define one universal Godot path, HiGodot port, or `CODEX_HOME` for all projects;
- equate process/port existence with readiness;
- move product authoring authority away from HiGodot;
- change Task8 gameplay/product behavior;
- require Task9/root-navigation work;
- authorize destructive repository cleanup.
