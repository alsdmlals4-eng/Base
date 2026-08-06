# HiGodot Single Authority and Reuse-First Design

## Status

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approved_by_user: true
approved_at: 2026-08-06
implementation_branch: agent/higodot-single-authority-policy
merge_authorization: NOT_GRANTED
```

## Goal

Adopt `hi-godot/godot-ai` as the only Godot MCP/addon execution authority, allow its full practical authoring surface including Node deletion, file writes, project settings, autoload, and structural changes, and move Base's custom MCP/adapter work into reusable policy, routing, evidence, and upgrade controls.

Prevent recurrence of the current duplication by requiring an existing-solution-first gate before any new MCP, addon, CLI, framework, Skill, Mode, or execution layer is designed or implemented.

## Authority model

```yaml
godot_execution_authority:
  provider: hi-godot/godot-ai
  addon: Godot AI / HiGodot
  authority_count: 1
  external_provider_role: PRIMARY_EXECUTION

custom_base_mcp:
  authority: false
  disposition: ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION

custom_base_godot_bridge:
  authority: false
  disposition: STOP_AND_ARCHIVE

hera_agent_godot:
  enabled: false
  authority: false
  disposition: BENCHMARK_REFERENCE_ONLY

deepseek:
  higodot_mcp_registration: forbidden
  credential: none
  godot_read: false
  godot_write: false
```

No Base MCP server, Base network Bridge, Hera addon, or second Godot mutation addon may coexist as an active execution authority in an adopted project.

## Existing Solution First Gate

The gate applies before creating or materially expanding any:

- MCP server or client integration;
- Godot addon, EditorPlugin, runtime bridge, debugger bridge, or CLI;
- framework, SDK wrapper, automation server, or tool registry;
- Base Skill, Skill Mode, template, or cross-project execution structure;
- functionality that resembles an existing dependency, open PR, installed tool, connected service, or public maintained project.

Required sequence:

```text
current environment inventory
→ current user tooling and project adoption check
→ Base and project implementation search
→ open and recently merged PR comparison
→ external maintained alternative research
→ capability, security, license, maintenance, integration, and migration comparison
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW disposition
→ adversarial review
→ user-visible recommendation and approval
→ design and implementation
```

The inventory must include, when applicable:

```yaml
current_environment:
  - conversation and handoff decisions
  - connected MCP servers and host profiles
  - Godot addons and project.godot plugin enablement
  - package and dependency manifests
  - Codex and VS Code MCP configuration
  - Base Skill Registry and project adapters
  - related branches, open PRs, merged PRs, and abandoned implementations
  - installed or already-used external tools named by the user
```

`BUILD_NEW` is permitted only when evidence shows at least one of the following:

- a required core capability is absent;
- a blocking safety or platform defect cannot be mitigated by configuration, isolation, a bounded upstream patch, or workflow controls;
- license terms conflict with the intended use;
- the existing project is abandoned or operationally unusable;
- performance, engine-version, operating-system, or client support is insufficient;
- the user reviews the comparison and explicitly approves new construction.

"A custom implementation could be stricter" is not sufficient evidence by itself.

## HiGodot operation policy

HiGodot's broad operation surface remains available. Base does not prohibit destructive or structural capabilities. Instead, execution is classified by impact and guarded by scope, rollback, and verification.

### L0 — Observe

Examples:

- Editor and session status;
- Scene hierarchy and Node property inspection;
- logs, diagnostics, resource metadata, and test discovery.

Requirements:

- verify the active project and Editor session;
- query only the domain required for the task;
- keep output bounded and progressively load schemas.

### L1 — Reversible write

Examples:

- Node creation or rename;
- property changes;
- script attachment;
- ordinary Scene or Resource save.

Requirements:

- record the target and intended result;
- inspect the result;
- review changed files;
- run related parse/import/tests.

### L2 — Destructive or structural write

Examples:

- Node deletion;
- file creation, modification, move, or deletion;
- Scene restructuring;
- project settings or input map changes;
- autoload changes;
- Resource replacement.

Requirements:

- confirm the action is inside the user's named scope;
- capture Git status and target inventory before execution;
- establish a rollback path through Git or an equivalent exact backup;
- execute in a branch or otherwise recoverable workspace;
- review the complete diff and unexpected files;
- run Godot import/parse and affected tests;
- report any unverified runtime or human gates.

An explicitly requested destructive action is approved only within its named scope. Newly discovered destructive work, unrelated cleanup, or scope expansion requires fresh user approval.

### L3 — High-impact batch or project-wide change

Examples:

- large multi-file migration;
- deletion of a core Scene or subsystem;
- broad project settings, autoload, input, or filesystem migration;
- repository-wide generated or serialized asset rewrite.

Requirements:

- written execution plan;
- adversarial review before mutation;
- explicit user approval;
- isolated branch;
- checkpoint commit;
- full project regression and rollback evidence.

## Tool selection and context controls

HiGodot exposes a large tool surface. The routing contract must prevent context flooding and wrong-tool wandering.

```text
identify task domain
→ read Editor/session readiness
→ load one primary domain and the minimum exact schema
→ execute or inspect one bounded operation group
→ validate result
→ change domain only with a recorded reason
```

Rules:

- do not preload every tool or operation schema;
- use HiGodot's domain/rollup tools and deferred schema loading when supported;
- keep one primary domain per operation step;
- do not cycle through unrelated tools after failure;
- re-observe current state before retrying mutation;
- use stable operation IDs or returned references rather than guessing Node paths or session targets;
- summarize large results instead of injecting entire trees or logs into context.

## Client isolation

HiGodot cannot reliably attest which model is behind a shared VS Code host. Isolation is therefore established at the host-profile boundary.

```yaml
VS_Code_Profile_Godot_Authoring:
  intended_client: GPT
  higodot_mcp: registered

Codex_CLI:
  intended_client: Codex
  higodot_mcp: registered

VS_Code_Profile_DeepSeek_Analysis:
  intended_client: DeepSeek
  higodot_mcp: absent
  credential: absent
```

Active project `.vscode/mcp.json` files must not be committed as a shared authority. A project may record the adopted provider version and verification evidence, but personal MCP registration remains user/profile scoped.

## Local transport boundary

Base does not create a second authentication addon around HiGodot. It limits the operating environment instead.

```yaml
network:
  loopback_only: true
  lan_mode: forbidden
  public_url_mode: forbidden
  port_forwarding: forbidden
  remote_tunnel: forbidden

host:
  local_development_machine_only: true
  shared_account_or_public_pc: forbidden
  disable_when_not_needed: recommended
```

A future upstream authentication improvement may be adopted through the normal version-review process. It must not create a forked second execution authority without passing the Existing Solution First Gate.

## Version, upgrade, and rollback policy

Every project adoption records an exact verified release or commit. Automatic unreviewed updates are forbidden.

```yaml
provider: hi-godot/godot-ai
exact_release_or_commit: required
godot_version: required
host_clients: required
enabled_domains: recorded
disabled_or_unverified_domains: recorded
last_verified_at: required
verification_evidence: required
rollback_release_or_commit: required
production_readiness: separate_from_connection_success
```

Upgrade sequence:

```text
new release identified
→ release notes, dependency, tool-schema, transport, and security diff
→ compatibility and adversarial review
→ isolated fixture install
→ Godot import and plugin startup smoke
→ read and destructive canary operations with restoration
→ representative project canary
→ project regression
→ staged project adoption
→ retain rollback package and previous pin
```

A connection handshake, tool listing, or single successful mutation does not establish production readiness.

## Base integration

Do not create three new broad Skills. Integrate the policy into existing owners:

- `managing-project-intake-and-work-contract`: enforce the Existing Solution First Gate before new construction;
- `evolving-project-discipline-skills`: require consolidation and external-solution comparison before new Skill or Mode creation;
- `managing-game-project-operating-system`: own third-party provider adoption, exact pins, project evidence, canary upgrade, and rollback;
- project template `godot-live-editor-operations`: route Godot execution to HiGodot and apply L0–L3 operation gates;
- `reviewing-and-validating-project-changes`: retain diff, regression, evidence, and unverified-gate review responsibilities.

A single canonical policy document owns the cross-cutting rules. Other files link to it and must not restate divergent versions.

## Existing custom PR disposition

```yaml
Base_PR_198:
  disposition: SUPERSEDED_BY_HIGODOT_POLICY_AFTER_EXTRACTION
  merge: false

Base_PR_201:
  disposition: ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION
  merge: false

Base_PR_202:
  disposition: STOP_AND_ARCHIVE
  merge: false
```

The PRs remain open until this policy PR preserves their reusable findings and passes exact-head review. Closing them is a separate explicit action and does not authorize deletion of their branches or history.

## Required evidence and tests

The implementation must add focused static contract tests proving:

1. AGENTS requires the Existing Solution First Gate before new construction;
2. the canonical policy names HiGodot as the sole execution authority;
3. destructive operations remain allowed under L2/L3 gates;
4. DeepSeek has no HiGodot MCP registration or credential;
5. network use is loopback-only with LAN, public URL, forwarding, and tunnel modes forbidden;
6. exact pin, canary, regression, and rollback are required;
7. the Godot project Skill routes to HiGodot and does not retain Base custom addon authority;
8. intake, operating-system, and Skill-evolution owners link to the canonical policy;
9. no active workspace `.vscode/mcp.json` or second addon is introduced;
10. custom MCP PRs remain unmerged references until the policy extraction is reviewed.

## Non-goals

- installing HiGodot into every project in this PR;
- enabling or modifying personal Codex or VS Code MCP settings;
- forking HiGodot;
- adding Hera;
- building a Base MCP server or Godot network Bridge;
- claiming Windows, project runtime, or production readiness without execution evidence;
- merging or closing PR #198, #201, or #202 without a separate explicit decision.

## Definition of done

- the canonical policy is discoverable from AGENTS and the affected Skills;
- the existing-solution gate is mandatory for all relevant new-construction requests;
- HiGodot is the sole Godot execution authority in the project template;
- Node deletion, file writes, project settings, autoload, and structural operations are allowed with explicit L2/L3 controls;
- tool-selection, DeepSeek isolation, local transport, upgrade, rollback, and evidence weaknesses have enforceable mitigations;
- focused RED→GREEN tests and existing Base operating-contract tests pass at the exact PR head;
- adversarial PR review reports no unresolved P0/P1 findings;
- no merge occurs without fresh user authorization.
