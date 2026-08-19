---
name: managing-game-project-operating-system
description: Use when installing, auditing, reconciling, migrating, or verifying a project repository operating system and its cold-start paths.
---

# Managing the Game Project Operating System

Base projects use the focused [project adapter and routing contract](references/project-adapter-and-routing-contract.md). Validate the canonical adapter and generated snapshot before shared-route execution; copied shared bodies or failed pins are blocking integrity failures.

## Core principle

신규 설치, 기존 구조 감사, 구형 파일 정리, 승인된 마이그레이션과 운영체계 검수는 같은 책임 원본·참조·복구 계약을 공유한다. `Work Mode`와 `Skill Mode`를 구분하며, 읽기 전용 조사와 승인된 쓰기 작업을 혼동하지 않는다.

프로젝트 사람이 보는 기본 운영면은 exact Project Notion이며, repository는 structured/runtime truth다.

```text
NOTION_HUMAN_FACING_CANON
↕ SYNC_BEFORE_IMPLEMENTATION
REPOSITORY_STRUCTURED_CANON
→ REPOSITORY_RUNTIME_TRUTH
```

Google Sheets는 신규 설치 항목이 아니다. 고유 미이관 정보가 실제로 남은 기존 프로젝트에서만 `RETIRED_MIGRATION_ONLY` source로 감사하고 `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`를 적용한다.

Standalone localhost project app, QA browser app, independent HTML dashboard/catalog도 신규 운영체계 기본 구성요소가 아니다. 고유 정보·원리 이관은 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`를 따른다.

Godot MCP/addon/CLI 공급자 도입·업데이트는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다. HiGodot (`hi-godot/godot-ai`)만 persistent Godot authoring 실행 권위이며 프로젝트는 `HIGODOT_ADOPTION_RECORD.json`에 **exact pin**, Godot 버전, host client, **canary**, regression, **rollback**과 미검증을 기록한다. GUT은 deterministic GDScript tests, Hera는 `LIVE_QA_AND_OBSERVABILITY_ONLY` 검증 역할로만 공존한다.

- `Work Mode`: `PLAN / BUILD / REVIEW`
- 이 문서의 `mode`: 운영체계 Skill 내부의 **Skill Mode**

## Skill Modes

- `install`: 신규/비어 있는 프로젝트에 project operating skeleton, Base adapter, Notion Project registration contract, required validation hooks를 설치한다.
- `audit`: 변경 없이 repository·Notion·provider·legacy surface·actual runtime evidence를 조사한다.
- `reconcile-legacy`: 구형/중복/retired surface를 `UPDATE_IN_PLACE / MERGE_TO_CANONICAL / COMPATIBILITY_STUB / ARCHIVE_HISTORY / DELETE_APPROVED / KEEP_UNRESOLVED`로 판정한다.
- `migrate`: 승인된 처리표 범위만 새 책임 구조로 재배치하며 destination readback을 요구한다.
- `verify`: 설치·정리·마이그레이션·provider upgrade·대규모 변경 뒤 전체 연결을 검증한다.

```text
신규·내용 거의 없음 → install
기존 운영 프로젝트 → audit
v2·final·latest·복제본·구형 파생본·retired surface → audit → reconcile-legacy
승인된 구조 이동표 있음 → migrate
설치·정리·마이그레이션·주요 게이트·HiGodot/GUT/Hera upgrade 후 → verify
```

`reconcile-legacy`는 별도 신규 Skill이 아니다.

## Required inputs

```yaml
target_repository:
work_mode: PLAN/BUILD/REVIEW
project_mode: new/existing/installed
requested_skill_mode: install/audit/reconcile-legacy/migrate/verify
base_version:
project_agents:
project_start_here:
documentation_map:
active_context:
current_confirmed_decisions:
project_notion_home:
project_notion_surfaces: []
related_open_and_recent_prs:
development_gates:
design_document_registry:
skill_registry:
project_base_adapter:
publications_and_manifests:
visual_and_asset_manifests:
roadmap_issues_plans_prs:
actual_code_data_assets_tests:
protected_paths_decisions_assets:
approved_migration_table:
legacy_migration_sources: []
provider_inventory: []
higodot_adoption_record:
validation_environment:
rollback_constraints:
```

## Read first

1. latest user decision.
2. project `AGENTS.md`, START_HERE, Active Context, Documentation Map, Development Gates.
3. `CURRENT_CONFIRMED_DECISIONS.md`, current Issue/Goal, same-goal open/recent PRs.
4. exact project GitHub main + actual code/data/Scene/Resource/asset/tests.
5. exact Project Notion Home + filtered Work/Asset/Core System/Visual/Reference surfaces.
6. project adapter, Base pin, generated snapshot, Skill Registry.
7. `docs/GPT_FIRST_PROJECT_WORKFLOW.md`, `docs/OPERATING_MODEL.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`.
8. `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md` when migration/legacy cleanup is in scope.
9. `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` when Godot authoring/provider work is in scope.

## Project operating integrity

`PROJECT_OPERATING_INTEGRITY` is fail-closed.

Check:

```text
project adapter exists and validates
→ Base release pin resolves
→ generated project Skill snapshot/router is current
→ required project paths exist
→ project Notion identity resolves to exactly one Project
→ repository structured owners resolve
→ current runtime evidence is not inferred from docs
→ retired surface is not current authority
```

Failure states include:

```text
MISSING_ADAPTER
STALE_ADAPTER
BROKEN_BASE_PIN
STALE_GENERATED_SNAPSHOT
MISSING_PROJECT_RELATION
CANON_CONFLICT
IMPLEMENTATION_CONFLICT
RETIRED_SURFACE_ACTIVE_REFERENCE
MIGRATION_PENDING
BLOCKED_UNVERIFIED
```

## Install

Install only the minimum current operating system:

```text
project AGENTS / START_HERE / ACTIVE_CONTEXT / DOCUMENTATION_MAP / DEVELOPMENT_GATES
→ CURRENT_CONFIRMED_DECISIONS / DESIGN_DOCUMENT_REGISTRY / SKILL_REGISTRY
→ project Base adapter + generated snapshot/router
→ GitHub workflow/governance hooks required by adopted contract
→ exact Project Notion registration / filtered human surfaces
→ project-specific runtime/test/engine setup when actually adopted
```

Do not install Google Sheets, standalone HTML dashboard, localhost project apps, Figma routes, or retired QA Studio as default project surfaces.

## Audit

Audit is read-only by default.

```yaml
current_structure:
canonical_owners:
notion_project_identity:
active_consumers:
providers:
retired_surfaces:
legacy_unique_material:
conflicts:
missing_sync:
verification_evidence:
```

Historical file age/name alone is not deletion evidence.

## Reconcile legacy / migrate

`DEPRECATED_SURFACE_ABSORB_THEN_DELETE`:

```text
inventory exact legacy surface
→ classify unique / duplicate / obsolete
→ human-facing unique meaning → exact Project Notion
→ structured/runtime unique meaning → repository-native owner
→ destination readback
→ active consumer/reference update
→ approved delete/archive/compatibility action
→ regression
```

Google Sheets uses `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`. Git history is rollback/audit, not active canon.

Do not create new archive copies if Git history already provides sufficient rollback and no policy requires a separate archive.

## Existing Solution First / provider inventory

Before adding MCP/addon/CLI/framework/Skill/Mode:

```text
inventory-current-environment
→ connected MCP / enabled addon / dependency / open and recently merged PR
→ external maintained alternatives
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
```

`BUILD_NEW` needs evidence and user approval.

For HiGodot:

```text
provider = hi-godot/godot-ai
→ exact pin
→ Godot compatibility
→ host client / network boundary
→ canary
→ destructive canary when required
→ project regression
→ rollback
→ production readiness evidence
```

Do not claim provider readiness from configuration existence alone.

## Verify

Verification separates evidence levels:

```text
static/schema
→ focused contract tests
→ project adapter / routing integrity
→ Notion project identity + destination readback when changed
→ Godot/runtime/build/render when applicable
→ accessibility/performance when applicable
→ regression
→ exact-head PR checks
→ postmerge readback
```

`NOT_RUN`, `BLOCKED_UNVERIFIED`, `DEFERRED_NOT_CONNECTED` are not PASS.

## GPT-first / optional Codex

Planning, audit synthesis, migration decision, UX/UI/art direction, visual review, and final operating-system review are GPT-primary.

Codex is `CODEX_OPTIONAL_SUB_EXECUTOR` only when actual repository/engine mutation or local reproduction is needed. If used, it must re-read actual repository state and follow the project authoring authority; GPT performs final review.

## Completion report

L1+ result includes:

- operating-system role.
- important rules / canonical owners.
- important Skills/Modes.
- module/responsibility map.
- current vs target structure.
- preserved / migrated / removed / intentionally not installed.
- exact tests/runtime/Notion readback/PR/main SHA.
- unverified, risks, rollback, revisit conditions.
- `REQUIRED_WORK_REMAINING`.

## References

- [project adapter and routing contract](references/project-adapter-and-routing-contract.md)
- `docs/GPT_FIRST_PROJECT_WORKFLOW.md`
- `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`
- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` — retirement/migration stub only
