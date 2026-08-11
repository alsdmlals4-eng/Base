# One-Shot Local Executor Bootstrap Design

## Decision

User-approved operating improvement on 2026-08-11 KST.

Goal: when a project-local implementation/review step requires a local shell, Godot editor, and Codex CLI, provide one copy/paste bootstrap command that opens or reuses the required local runtime and then launches Codex in the exact project/worktree, instead of making the user manually perform three separate startup steps.

This is an operating-flow improvement, not a new game/product decision.

## Existing Owner First

Do not create a new broad Skill.

Shared Base owners:

- `docs/GPT_CODEX_WORKFLOW_POLICY.md` — GPT→Codex handoff and executor policy.
- `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md` — installed-project Godot/HiGodot bootstrap template.
- `tests/test_gpt_codex_workflow_contract.py` — canonical GPT/Codex workflow contract.

Project-local concrete values remain in the consuming project. Base must not hard-code a project path, Godot executable, CODEX_HOME, port, plugin version, worktree, or branch.

## New Shared Contract

Token: `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`.

When local execution is actually required and the user must start the executor manually, the handoff should prefer one copy/paste shell block that performs the bounded startup sequence:

```text
one shell invocation
→ resolve the exact approved project/worktree inputs
→ reuse the exact matching editor if already running
→ otherwise start the required editor
→ perform only the minimum startup/readiness checks needed before executor handoff
→ launch Codex with the exact approved project/worktree as its working directory
→ Codex performs fresh runtime/session/readiness verification before persistent authoring
```

The bootstrap block is a launcher, not proof of runtime readiness. It must not promote an editor launch, open port, or process existence to product/tool readiness without the project-authorized live receipt.

## Noise and Failure Rules

The launcher must avoid expensive or noisy pre-Codex diagnostics that are not required to start the session. In particular, known line-ending/stat/index noise must not be re-emitted on every bootstrap merely to prove a previously classified condition.

`BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`:

- verify only identity/state required to avoid launching the wrong target;
- do not front-load broad `git diff`, repository scans, or long diagnostic dumps when Codex can perform them after startup;
- if a minimum prerequisite fails, stop before launching Codex and show the single actionable blocker;
- do not `reset`, `restore`, `clean`, stage, or rewrite user work as part of bootstrap;
- do not kill/restart unrelated project editors or servers;
- exact matching editor reuse is preferred over duplicate startup.

## Godot Consumer Contract

For projects using the `godot-live-editor-operations` template:

```text
project/worktree identity
→ matching Godot editor reuse-or-start
→ bounded startup wait/readiness opportunity
→ Codex launch in exact project/worktree
→ fresh HiGodot session/readiness receipt inside Codex before mutation
```

If the project has a sole persistent Godot authoring authority such as HiGodot, the one-shot launcher does not weaken that boundary. Shell startup is orchestration only; persistent Godot authoring still uses the authorized provider.

## Project-Specific Consumer Example

A project may bind concrete values such as:

- exact worktree path;
- exact Godot executable path;
- project-scoped `CODEX_HOME`;
- Codex sandbox mode;
- expected branch/head when that check is required;
- local server/port conventions.

Those values belong to project canon or the current execution packet, not Base.

## GRIMOIRE Binding Intent

GRIMOIRE should consume this rule under its existing Godot/Codex tool authority decision `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` without creating a new product decision.

Its concrete handoff should prefer one PowerShell block that:

```text
starts from Windows PowerShell
→ opens/reuses the exact requested GRIMOIRE Godot worktree
→ uses the GRIMOIRE CODEX_HOME profile
→ launches Codex with `-C <exact worktree>` and the requested sandbox
```

The Codex prompt must still obtain a fresh Godot-AI session receipt before persistent mutation.

## Evidence Boundary

The one-shot block proves only that the requested local applications/process entrypoints were invoked successfully enough to reach Codex. It does not by itself prove:

- exact HiGodot session identity;
- server/plugin readiness;
- tests passing;
- Godot import/parse success;
- Hera acceptance;
- human/device/performance/export/full-slice validation.

Those remain separate evidence stages.

## Acceptance Criteria

- Base canonical Codex policy explicitly defines `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`.
- Base Godot live-editor template consumes the same token and preserves HiGodot sole-authority boundaries.
- Base contract test fails before policy/template changes and passes after them.
- Base contains no GRIMOIRE-specific path, port, version, CODEX_HOME, or branch value.
- GRIMOIRE concrete consumer records the exact project convention under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`.
- GRIMOIRE Sheet sync uses the same existing Decision ID.
- Known LF/CRLF/stat noise is not made a mandatory pre-Codex dump.
- Wrong worktree/editor/session conditions fail closed without reset/restore/clean.
- Post-change adversarial monitor loop rechecks same-goal PRs and untouched consumers before completion.
