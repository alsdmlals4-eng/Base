# Universal Loop Engineering — Cross-Project Acceptance Evidence

## Decision

The declarative Project Execution Capsule architecture and deterministic M2→M3 Loop Kernel are portable across materially different project structures without a project-specific Kernel fork.

This evidence does **not** claim that the real Codex Builder / GPT Critic provider transport or paid OpenAI API execution is complete.

## Base runtime reference

Accepted Base Kernel main:

```text
8e7238a1bb9f49bd6e2403a2a6cb20d7aee863c7
```

Merged runtime layers before this checkpoint:

1. M2 Project Execution Capsule contracts — PR #333.
2. M3 deterministic model-free SHADOW Kernel — PR #337.
3. deterministic M2 Capsule→M3 SHADOW adapter — PR #356.
4. bounded A2 Runtime Foundation — PR #343.
5. actual external Git worktree + Diff attestation — PR #351.
6. bounded project test executor — PR #354.
7. PR handoff + direct-evidence postmerge closure — PR #358.
8. durable verified worktree ownership/resume — PR #360.

A3 remains disabled. Scheduler remains `NOT_CONFIGURED`. Automatic product-scope selection remains forbidden.

## Project 1 — Blacksmith

Repository: `alsdmlals4-eng/Blacksmith`

Current accepted main:

```text
5267f542ef6ce99f98b3b407e42b146b5672335b
```

Project shape:

```text
Godot product
+ persistent Save schema
+ item UID lifecycle
+ existing approved Phase C package boundaries
+ visual authority reserved for human approval
```

Evidence:

- Universal Capsule migration: PR #165.
- Base Active Run pointer regression found through cross-project testing and corrected in PR #167.
- postmerge Full Validation: run `31788438786` PASS.
- postmerge Live-Editor Pilot: run `31788439264` PASS.
- Active Run is null.
- legacy Loop Profile/Run Contract remains historical evidence.
- `next_package` remains `UNSELECTED_USER_DECISION_REQUIRED`.
- Task3 remains not separately approved.
- no migration change under product `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.

Acceptance:

```yaml
capsule_portability: PASS
native_project_validation: PASS
unmodified_base_m2_m3_shadow: NOT_RUN
```

Blacksmith therefore proves Capsule migration and project-governance compatibility. A real Blacksmith A2 implementation burn-in remains part of the provider stage rather than being inferred from metadata adoption.

## Project 2 — Coc-Fiction

Repository: `alsdmlals4-eng/Coc-Fiction`

Accepted main:

```text
b096a29afeecdc3129690229c9d4d110797e40e4
```

Project shape:

```text
narrative/data Canon
+ character continuity
+ timeline
+ style authority
+ manuscript constraints
```

Locked authority:

- `fiction/CANON_REGISTRY.json`
- `fiction/FICTION_MASTER.md`
- `fiction/STYLE_GUIDE.md`
- `fiction/ACTIVE_CONTEXT.md`

Pilot PR #27 used the same Base Kernel without a fork.

The first direct translation exposed a project-contract bug: the Active Run role had been written as `LOOP_ACTIVE_RUN`, while Base Schema requires `LOOP_ACTIVE_RUN_POINTER`. The project contract was corrected; Base Kernel behavior was not changed.

Postmerge run `31787666732` passed:

```text
local narrative contract
→ pinned Base Capsule validator/translator
→ pinned unmodified Base SHADOW Kernel
→ SHADOW_COMPLETE
```

No changes were made under `fiction/`, `skills/`, `tools/`, or `templates/`.

Acceptance:

```yaml
capsule_portability: PASS
unmodified_base_m2_m3_shadow: PASS
canon_mutation: 0
```

## Project 3 — GRIMOIRE-

Repository: `alsdmlals4-eng/GRIMOIRE-`

Accepted main:

```text
ca5d004b42e19f775163188da18020de4d5aa2e7
```

Project shape:

```text
Godot visual/UI-heavy project
+ approved low-fi mobile runtime layout
+ multi-solution spell workflow UX
+ accessibility/layout constraints
```

Visual Lock provider:

```text
GITHUB_ART_BIBLE
```

Approved Visual/UX references:

- `STAR_CIRCUIT_MOBILE_LANDSCAPE_WIREFRAME_01_APPROVAL_2026-08-06.md`
- `FROSTBLOOM_STAR_CIRCUIT_UX_MAP_01_APPROVAL_2026-08-06.md`

Locked visual/UX semantics include:

- `FIVE_POINT_STAR` active layout;
- left / center / right / bottom mobile hierarchy;
- circuit preview before target selection;
- explicit commit after final preview;
- 48dp minimum touch target;
- 130% text scale without clipping;
- no auto-target / auto-commit;
- no hidden best-route answer key;
- no 3×3 layout reversion.

Pilot PR #137 changed only ten operations/test/workflow paths. No change was made under `src/`, `assets/`, `data/`, `addons/`, `project.godot`, or `docs/planning/`.

Postmerge run `31788652715` passed the same pinned unmodified Base Visual SHADOW workflow on main.

The premerge exact-head Visual SHADOW also passed on Ubuntu 24.04 and Windows 2025, together with the project's existing visual-platform contract and native Godot planning/runtime gates.

Acceptance:

```yaml
capsule_portability: PASS
unmodified_base_m2_m3_shadow: PASS_UBUNTU_WINDOWS
visual_lock: PASS
visual_drift_escape: 0
```

This remains low-fi automated structural evidence. It does not upgrade `HUMAN_NOT_RUN`, `DEVICE_NOT_RUN`, final-art, performance, or physical-device accessibility claims.

## Cross-project result

```yaml
project_capsule_projects: 3
structurally_different_projects: true
unmodified_base_m2_m3_runtime_projects: 2
kernel_forks_for_pilots: 0
project_specific_agent_implementations: 0
planning_drift_escape: 0
visual_drift_escape: 0
unauthorized_product_path_changes: 0
cross_project_context_import: 0
```

The two direct M2→M3 SHADOW pilots pinned the same Base Kernel commit. The Kernel was not modified between narrative and visual/UI pilots.

Blacksmith is intentionally reported separately because its current evidence is Capsule migration plus native project validation rather than a direct in-project pinned Base SHADOW run. The real provider burn-in will exercise Blacksmith as the first actual A2 implementation project.

## Remaining gate before real autonomous implementation

All remaining blocking work is concentrated at the actual model-provider boundary:

```yaml
real_codex_builder_transport: NOT_IMPLEMENTED
real_gpt_critic_transport: NOT_IMPLEMENTED
real_openai_api: NOT_RUN_USER_CREDENTIAL_DECISION_REQUIRED
real_a2_burnin_runs: 0
```

Before starting that provider implementation, choose whether to reuse an existing OpenAI API key or create a new project-scoped API key.

## Non-goals preserved

- no A3 auto-merge;
- no Scheduler;
- no automatic product-package selection;
- no cross-project Canon/asset/session import;
- no automatic Planning or Visual approval;
- no claim that automated visual SHADOW equals human/device/final-art verification.

## Rollback

This acceptance layer is evidence only. Reverting it does not roll back M2/M3/A2 code or any project data.
