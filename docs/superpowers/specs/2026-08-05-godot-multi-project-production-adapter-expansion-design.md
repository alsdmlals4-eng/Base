# Godot Multi-Project Production Adapter Expansion Design

```yaml
design_id: BASE-GODOT-ADOPT-20260805-MULTIPROJECT-PILOT-01
status: APPROVED_DESIGN_PENDING_WRITTEN_SPEC_REVIEW
approved_by_user: true
approval_time_kst: 2026-08-05T23:10:00+09:00
base_repository: alsdmlals4-eng/Base
base_design_baseline: ecbd93f16b65a1527269bfd8fef9facad6b2f40b
production_readiness_claim: NOT_READY
```

## 1. Purpose

Base의 Godot live-editor v2 계약과 project-local Editor transaction adapter를 실제 게임 프로젝트에 안전하게 확장한다.

이번 설계는 서로 다른 여섯 저장소에 같은 파일을 무조건 복사하는 작업이 아니다. 기존 Godot AI 3.0.5, 프로젝트별 보호 경로, 기획 단계, 제품 구현 권한, 실제 Godot 프로젝트 존재 여부를 구분하고 다음 순서로 증거를 만든다.

```text
Base 다중 프로젝트 Pilot runner
→ 프로젝트별 임시 복제·격리 실행
→ 실제 main Scene read-only inspect
→ 임시 scratch Scene mutation·Undo·save
→ 원본 저장소 무변경 증명
→ 프로젝트별 Draft PR과 exact-head 검증
→ Base 통합 증거 정본
```

## 2. Program decomposition

전체 확장은 세 개의 독립 프로그램으로 나눈다.

### Program A — Multi-project isolated Pilot

이번 설계와 다음 구현 계획의 직접 범위다.

- Base reusable project-pilot runner
- Base reusable GitHub Actions workflow
- 다섯 실제 Godot 프로젝트의 격리 Pilot
- GRIMOIRE의 preproject readiness 검증
- 기존 Godot AI와 Base v2 authority의 공존 경계
- 원본 프로젝트 무변경 증거
- 프로젝트별 evidence artifact
- Base 통합 결과 정본

### Program B — Authenticated STDIO MCP bridge

Program A의 실제 프로젝트 증거가 통과한 뒤 별도 설계·계획·승인으로 진행한다.

- protocol-only stdout
- diagnostics-only stderr
- current-user process boundary
- exact project/service/editor identity
- session token과 request binding
- bounded frame, depth, batch, idle, task lifetime
- v2 operation envelope 매핑
- Editor main-thread queue에만 제출
- arbitrary SceneTree, Resource, shell, script execution 금지

Program A는 외부 transport를 구현하거나 production MCP readiness를 주장하지 않는다.

### Program C — Opt-in runtime debugger

Program B 이후 별도 설계·계획·승인으로 진행한다.

초기 capability 후보는 다음으로 제한한다.

```yaml
runtime.session.inspect: READ_ONLY
runtime.logs.read: READ_ONLY
runtime.pause: MUTATION_APPROVAL_REQUIRED
runtime.resume: MUTATION_APPROVAL_REQUIRED
runtime.step_frame: MUTATION_APPROVAL_REQUIRED
```

임의 Expression, 임의 GDScript, shell, memory patch, arbitrary property mutation은 포함하지 않는다.

## 3. Source baselines

설계 조사 시점의 기준 SHA는 다음과 같다.

| Repository | Baseline main SHA | Classification |
|---|---|---|
| `alsdmlals4-eng/Base` | `ecbd93f16b65a1527269bfd8fef9facad6b2f40b` | canonical contract owner |
| `alsdmlals4-eng/Ten-Paces-Hidden-Moves` | `bbed0fd4d278ca0e0d52f4e6d9083aafa1997318` | real Godot project, legacy Godot AI active |
| `alsdmlals4-eng/Blacksmith` | `476ddc380079dd61d67cda4c065a80819355292f` | real Godot project, product implementation blocked |
| `alsdmlals4-eng/omenward` | `6b23ca2bb627827651a42ba6db01829e44ee8a14` | real Godot project, total-planning authority only |
| `alsdmlals4-eng/urban-legend` | `55721e905bf24fc3deb0de061a529ecb992aee80` | real Godot project, multiple existing autoloads |
| `alsdmlals4-eng/GRIMOIRE-` | `4c50b462a8e296e24583b727ab93c82ba1e9c041` | product Godot project not created |
| `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle` | `6cdbda34da61de7b5175ad08d7aaffaf186a0dcf` | clean real-project Pilot baseline |

Implementation begins from fresh then-current main SHAs. These design baselines are audit evidence, not permission to overwrite later project work.

## 4. Existing-system audit

### 4.1 Legacy Godot AI projects

Ten Paces, Blacksmith, OMENWARD, and urban-legend currently enable:

```text
res://addons/godot_ai/plugin.cfg
_mcp_game_helper = res://addons/godot_ai/runtime/game_helper.gd
```

The existing addon identifies itself as Godot AI 3.0.5 and can auto-start a Python MCP server, connect over WebSocket, inspect and mutate scenes, create nodes, modify properties, run tests, and expose runtime helpers.

It is classified as:

```yaml
legacy_system: GODOT_AI_3_0_5
base_v2_authority: false
legacy_external_mcp: true
allowed_to_prove_base_v2_completion: false
```

Base v2 approval tokens, operation envelopes, queue ordering, atomic ledger, and evidence requirements cannot be inferred from successful legacy MCP execution.

### 4.2 Clean Pilot project

Switchy Express has a Godot 4.7.1 project without the legacy Godot AI addon enabled. It is the first real-project clean baseline.

### 4.3 Preproject repository

GRIMOIRE records `product_project: NOT_CREATED`. Program A must detect this state and reject false runtime claims. It receives a readiness contract only; no fabricated `project.godot`, Scene, runtime PASS, or product implementation is added.

## 5. Goals

Program A must prove the following without modifying product behavior.

1. A project can be checked out and copied to a temporary workspace.
2. Base adapter files can be injected into the temporary copy only.
3. Legacy Godot AI can be disabled in the temporary copy without deleting it from source.
4. The real project loads under the declared Godot version or fails with bounded evidence.
5. The actual configured main Scene can be inspected read-only.
6. A runner-created scratch Scene can be renamed through the Base transaction adapter.
7. Editor Undo restores the prior scratch Scene state.
8. Save produces a physical file-byte SHA-256.
9. Atomic STARTED and terminal ledger records are valid.
10. The checked-out source tree remains byte-identical after execution.
11. Base creates no network listener during Program A.
12. Project-specific product tests remain unaffected or explicitly blocked by pre-existing project policy.

## 6. Non-goals

Program A does not:

- install the Base adapter permanently into product projects;
- remove or upgrade Godot AI 3.0.5 in source repositories;
- enable two live mutation authorities simultaneously;
- modify product Scenes, Resources, scripts, data, saves, input maps, export presets, autoloads, or plugin lists in source;
- add MCP, HTTP, WebSocket, TCP, UDP, named-pipe, or remote endpoint support;
- add runtime debugger capabilities;
- run arbitrary GDScript, shell commands, expressions, or property paths through the adapter;
- claim Android, Windows production operation, physical input, accessibility, performance, or human usability PASS;
- synchronize a Google Sheet because no game-design Decision changes;
- change Skill Registry, release locks, frozen derivatives, or v1 Pilot evidence;
- claim `PRODUCTION_ADAPTER_READY`.

## 7. Architecture

### 7.1 Base-owned runner

Base adds a reusable runner with four layers.

```text
project descriptor validation
→ temporary materialization
→ Godot Editor Pilot execution
→ evidence and source-integrity verification
```

Recommended Base paths:

```text
tools/godot_multi_project_pilot.py
schemas/godot-project-pilot-v1.schema.json
.github/workflows/reusable-godot-project-pilot.yml
tests/test_godot_multi_project_pilot.py
tests/test_godot_multi_project_pilot_adversarial.py
templates/project-operations/godot-live-editor/PROJECT_PILOT_DESCRIPTOR.json
```

The implementation plan may refine filenames but must preserve these responsibility boundaries.

### 7.2 Project-owned descriptor

Each project PR adds a small, reviewable descriptor rather than copying Base implementation code.

```text
.godot-live-editor/project-pilot.json
```

Descriptor fields include:

```yaml
schema_version: "1"
project_identity: exact repository and project identifier
base_pilot_commit: exact merged Base C0 SHA
godot_version: exact required or accepted version range
project_file: project.godot or explicit absent state
main_scene_source: project.godot application/run/main_scene
legacy_editor_plugins: declared list
legacy_autoloads: declared list
legacy_disable_mode: TEMPORARY_COPY_ONLY
source_mutation_policy: FORBIDDEN
scratch_scene_path: runner-owned temporary path
project_behavior_test_commands: bounded explicit list
expected_platform: informational only
```

`additionalProperties: false` is required.

### 7.3 Reusable workflow

Project PRs call the Base reusable workflow by an exact merged Base C0 commit SHA.

```yaml
uses: alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@<exact-base-c0-sha>
```

A floating `main`, tag without immutable resolution, project branch name, or unreviewed fork is forbidden.

The called workflow checks out the caller repository, verifies the descriptor, materializes a temporary copy, obtains the declared Godot binary through the approved Base mechanism, runs the Pilot, and uploads bounded evidence.

### 7.4 Temporary materialization

The runner creates two roots.

```text
source_checkout/   # read-only integrity baseline
pilot_workspace/   # disposable mutation target
```

It records a source inventory before and after execution. The inventory excludes known transient checkout metadata only and hashes relevant tracked files. Any source change is `SOURCE_TREE_MUTATED` and fails the Pilot.

The runner may alter only the disposable workspace:

- inject `addons/base_godot_live_editor/`;
- write a configured v2 capability manifest bound to the temporary project path;
- temporarily remove legacy Godot AI from `[editor_plugins]`;
- temporarily remove `_mcp_game_helper` from `[autoload]`;
- create a runner-owned scratch Scene;
- create bounded ledger and evidence paths;
- restore or discard the workspace after evidence capture.

## 8. Legacy Godot AI coexistence policy

### 8.1 Source repository

Legacy Godot AI remains untouched in Program A.

```yaml
source_addon_removed: false
source_plugin_disabled: false
source_autoload_removed: false
legacy_workflow_migrated: false
```

### 8.2 Pilot workspace

Legacy mutation authority is disabled before Base adapter activation.

The runner must verify:

- `res://addons/godot_ai/plugin.cfg` is not enabled in the temporary `project.godot`;
- `_mcp_game_helper` is not active in the temporary autoload section;
- no Godot AI-managed Python server is spawned by the Pilot;
- no listener attributed to Base is created;
- no operation result is accepted from the legacy system.

If reliable temporary disabling cannot be proved, the Pilot fails `LEGACY_MUTATION_AUTHORITY_ACTIVE`.

### 8.3 Future migration

Permanent replacement, coexistence, or removal of Godot AI requires a separate project Decision and Program B design. Program A does not make that decision implicitly.

## 9. Project classifications and boundaries

### 9.1 Ten Paces: Hidden Moves

```yaml
classification: REAL_PROJECT_PILOT_WITH_LEGACY_MCP_CONFLICT
source_product_paths_mutable: false
main_scene_inspect: required
scratch_mutation: required
legacy_godot_ai_source_change: forbidden
```

The project is already in active vertical-slice work. The Pilot must not alter combat, route, reward, save, UI, or planning canon.

### 9.2 Blacksmith

```yaml
classification: REAL_PROJECT_PILOT_TEMP_COPY_ONLY
product_implementation: BLOCKED
source_protected_paths:
  - data/
  - scripts/
  - scenes/
  - assets/
  - addons/
  - project.godot
```

Only documentation, descriptor, contract tests, and CI wiring may be added to the source PR. Runtime mutation is disposable-workspace-only.

### 9.3 OMENWARD

```yaml
classification: REAL_PROJECT_PILOT_TEMP_COPY_ONLY
work_mode: TOTAL_PLANNING
product_code_authority: NONE
```

No product code, Scene, Resource, game data, or art asset change is authorized. The Pilot PR is an operational validation package, not product implementation.

### 9.4 urban-legend

```yaml
classification: REAL_PROJECT_PILOT_WITH_EXISTING_AUTOLOADS
existing_autoloads_must_be_preserved_in_source: true
```

Only `_mcp_game_helper` is disabled in the temporary copy. `UrbanLegendState`, `ValidationSession`, and `GameState` remain available unless the project fails to load, in which case evidence must identify the pre-existing dependency failure without editing source.

### 9.5 GRIMOIRE

```yaml
classification: PREPROJECT_READINESS_ONLY
product_project: NOT_CREATED
runtime_pilot: NOT_APPLICABLE
```

The project PR adds:

- adoption readiness document;
- descriptor with explicit `project_state: NOT_CREATED`;
- test that rejects runtime PASS or adapter installation claims;
- future adoption checklist tied to product-project creation approval.

It does not create `project.godot`.

### 9.6 Switchy Express

```yaml
classification: CLEAN_BASELINE_REAL_PROJECT_PILOT
legacy_godot_ai: absent
first_execution_order: true
```

It is the first project Pilot. Its PASS is required before running the four legacy-Godot-AI projects.

## 10. Execution order and PR topology

Eight Draft PRs are planned.

1. Base C0 — reusable runner, Schema, workflow, tests, source-integrity contract.
2. Switchy Express — clean real-project Pilot.
3. Ten Paces — legacy Godot AI temporary-disable Pilot.
4. Blacksmith — blocked-product temporary-copy Pilot.
5. OMENWARD — planning-only temporary-copy Pilot.
6. urban-legend — existing-autoload temporary-copy Pilot.
7. GRIMOIRE — preproject readiness contract.
8. Base C1 — integrate exact project evidence, record limitations, decide whether Program B design may start.

Project PRs 3–7 may proceed in parallel only after Switchy Express proves the Base C0 workflow. They must pin the same reviewed Base C0 merge SHA unless an explicit Base compatibility update is approved.

No project PR is merged automatically. Each requires exact-head CI, scope review, unresolved review thread count zero, and explicit user merge approval.

## 11. Project PR source scope

For existing Godot projects, default allowed source changes are:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Existing repository conventions may require a current status or documentation map reference. Such additions must be routing-only and must not claim product implementation.

Default forbidden source changes are:

```text
project.godot
addons/
scenes/
scripts/
src/
data/
assets/
game/
export_presets.cfg
save formats
Google Sheets
```

GRIMOIRE uses a preproject descriptor and readiness test instead of a runtime workflow.

## 12. Pilot data flow

```text
project PR exact HEAD
→ validate descriptor Schema
→ verify Base C0 immutable pin
→ hash source tree
→ copy to disposable workspace
→ verify project.godot and main Scene declaration
→ disable legacy mutation authority in workspace only
→ inject Base adapter and configured manifest
→ launch Godot Editor headless with bounded timeout
→ inspect actual edited main Scene
→ create runner scratch Scene
→ submit node.rename KEEP_DIRTY
→ verify changed state
→ Editor Undo
→ verify restored state
→ submit node.rename SAVE_CURRENT_SCENE
→ verify saved file bytes and SHA-256
→ verify STARTED and COMPLETED ledger
→ verify Base listener count is zero
→ run bounded project behavior contracts
→ discard workspace
→ rehash source tree
→ upload evidence manifest
```

## 13. Failure semantics

The runner fails closed with stable codes.

```yaml
DESCRIPTOR_SCHEMA_INVALID: descriptor structure or type invalid
BASE_PIN_UNRESOLVED: exact Base C0 commit unavailable
PROJECT_IDENTITY_MISMATCH: repository, project path, or manifest identity mismatch
PROJECT_FILE_MISSING: runtime project expected but project.godot absent
MAIN_SCENE_UNDECLARED: no approved main Scene source
MAIN_SCENE_MISSING: declared Scene absent
LEGACY_MUTATION_AUTHORITY_ACTIVE: legacy plugin or autoload remains active in workspace
BASE_NETWORK_LISTENER_DETECTED: Base-created listener observed
GODOT_VERSION_MISMATCH: executable outside declared contract
PROJECT_LOAD_FAILED: Editor cannot load project
MAIN_SCENE_INSPECT_FAILED: read-only real Scene inspection failed
SCRATCH_TRANSACTION_FAILED: Base mutation or Undo failed
SAVE_HASH_MISSING: physical saved bytes or SHA-256 absent
LEDGER_INVALID: STARTED or terminal ledger invalid
PROJECT_BEHAVIOR_REGRESSION: declared project contract failed
SOURCE_TREE_MUTATED: source checkout changed
EVIDENCE_INCOMPLETE: required bounded evidence missing
PREPROJECT_RUNTIME_CLAIM_REJECTED: runtime PASS claimed for absent product project
```

Timeout never becomes automatic success or blind replay authority.

## 14. Evidence contract

Each runtime Pilot uploads one bounded JSON manifest and referenced text logs.

Required evidence includes:

```yaml
repository_full_name: exact
project_head_sha: exact
base_c0_sha: exact
descriptor_sha256: exact
project_godot_sha256_before: exact
main_scene_path: exact
main_scene_sha256_before: exact
legacy_plugin_detected_in_source: boolean
legacy_plugin_disabled_in_workspace: boolean
legacy_autoload_disabled_in_workspace: boolean
base_network_listener_enabled: false
godot_version: exact
scene_inspect: PASS or stable failure
scratch_rename_dirty: PASS or stable failure
editor_undo: PASS or stable failure
scratch_rename_save: PASS or stable failure
saved_scratch_sha256: exact when PASS
ledger_states: bounded list
project_behavior_tests: bounded result list
source_tree_before_sha256: exact
source_tree_after_sha256: exact
source_tree_unchanged: true
human_usability: HUMAN_NOT_RUN
physical_input: NOT_RUN
production_ready: false
```

Logs must redact secrets, local account paths where avoidable, tokens, environment values, and unrelated project content.

## 15. Testing strategy

### 15.1 Base C0 TDD

RED tests are written before the runner and workflow.

Required test groups:

- descriptor Schema and `additionalProperties: false`;
- materialization confinement;
- exact Base pin enforcement;
- legacy plugin/autoload temporary disabling;
- clean-project path;
- missing project and preproject path;
- source-tree mutation detection;
- no-network-listener assertion;
- bounded timeout and evidence output;
- path traversal, symlink, oversized input, malformed JSON, duplicate identity, stale descriptor attacks;
- existing Base v2 adapter regression.

### 15.2 Project PR tests

Each project test validates:

- descriptor matches repository facts at exact HEAD;
- workflow pins exact Base C0 SHA;
- protected paths are absent from the PR diff;
- source `project.godot` is unchanged;
- legacy plugin declarations match actual source when applicable;
- GRIMOIRE cannot claim runtime PASS;
- evidence artifact is produced only by the runtime workflow.

### 15.3 Runtime sequence

1. Switchy Express clean Pilot.
2. Ten Paces legacy conflict Pilot.
3. urban-legend existing-autoload Pilot.
4. Blacksmith blocked-product Pilot.
5. OMENWARD planning-only Pilot.
6. GRIMOIRE readiness validation.

Order 3–5 may be adjusted after the clean Pilot, but every result remains project-specific.

## 16. Adversarial review matrix

Program A must attack at least the following.

- Base adapter and legacy Godot AI both active.
- Source `project.godot` edited by a supposedly temporary operation.
- Source addon deleted or upgraded without approval.
- Real main Scene mutated instead of read-only inspected.
- Scratch Scene path escaping runner workspace.
- Symlink writing back into source checkout.
- Descriptor pointing at a different repository or branch.
- Floating Base workflow ref.
- Evidence copied from another project or prior commit.
- Runtime PASS fabricated for GRIMOIRE.
- Missing Godot binary reported as PASS.
- Timeout followed by blind mutation replay.
- Network listener opened despite Program A boundary.
- Project contract test omitted after load succeeds.
- Existing project failure blamed on the adapter without bounded evidence.
- Product implementation unblocked by an operations-only PR.
- Google Sheet updated despite no planning Decision change.
- Human usability or production readiness inferred from CI.

## 17. Existing Base hardening dependency

Open Base PR #166 adversarially hardens the Editor transaction adapter. Before Base C0 implementation starts, its state must be resolved against then-current main.

```yaml
pr_166_state_check: REQUIRED
allowed_resolution:
  - MERGED_AND_C0_REBASED
  - SUPERSEDED_WITH_EQUIVALENT_MAIN_HARDENING_PROVEN
forbidden_resolution:
  - IGNORE_OPEN_HARDENING_FINDINGS
```

Base C0 cannot copy or assume stale adapter behavior from a pre-hardening branch.

## 18. Security and privacy

- Program A is listener-free.
- No external MCP server is started by Base.
- No credentials are required in project descriptors.
- Workflow permissions use least privilege and default read-only contents.
- Artifact upload contains only bounded evidence.
- Project source archives are not uploaded as evidence.
- Secrets and environment dumps are prohibited.
- Private repository evidence must remain within permitted GitHub Actions visibility.
- Current-user-only local execution does not imply authenticated external transport.

## 19. Readiness gates

Program A completion requires:

```yaml
base_c0_runner_and_workflow: MERGED
switchy_clean_pilot: RUNTIME_PASS
ten_paces_pilot: RUNTIME_PASS_OR_BOUNDED_PROJECT_BLOCKER
blacksmith_pilot: RUNTIME_PASS_OR_BOUNDED_PROJECT_BLOCKER
omenward_pilot: RUNTIME_PASS_OR_BOUNDED_PROJECT_BLOCKER
urban_legend_pilot: RUNTIME_PASS_OR_BOUNDED_PROJECT_BLOCKER
grimoire_preproject_contract: PASS
source_tree_unchanged_all_projects: PASS
base_listener_created: false
base_c1_evidence_integration: MERGED
program_b_design_authorization: USER_REQUIRED
production_adapter_ready: false
```

A bounded project blocker is not a project PASS. It is acceptable only when the failure is reproducible, source-preserving, and explicitly recorded for follow-up.

## 20. Rollback

### Base C0 rollback

Revert the runner, Schema, reusable workflow, tests, and descriptor template. No project data migration is needed.

### Project PR rollback

Revert the four operations-only files or repository-specific routing companion. Product files remain unchanged.

### Evidence rollback

Evidence records are historical audit artifacts. Incorrect evidence is superseded with a correction record; it is not silently rewritten.

## 21. Final design decisions

```yaml
approach: TEMPORARY_COPY_PILOT_THEN_TRANSPORT
first_real_project: Switchy-Express-Cargo-Puzzle
legacy_godot_ai_source_removal: FORBIDDEN_IN_PROGRAM_A
legacy_godot_ai_workspace_state: DISABLED_BEFORE_BASE_ADAPTER
source_project_mutation: FORBIDDEN
real_main_scene_mutation: FORBIDDEN
scratch_scene_mutation: REQUIRED
base_network_listener: FORBIDDEN
cross_repo_workflow_ref: EXACT_BASE_C0_COMMIT
project_prs: DRAFT_AND_INDEPENDENT
direct_main_write: FORBIDDEN
merge_authorization: USER_REQUIRED
program_b_stdio_mcp: SEPARATE_DESIGN_AFTER_PROGRAM_A_EVIDENCE
program_c_runtime_debugger: SEPARATE_DESIGN_AFTER_PROGRAM_B
production_adapter_ready: NOT_READY
```
