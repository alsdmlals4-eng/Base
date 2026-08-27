# Work 프로젝트 로컬 Visual 자산 전달 프로필

> 이 파일은 사용자가 **로컬 GPT/컴퓨터가 프로젝트 파일에 직접 접근할 수 있으므로 이미지 바이너리를 Notion에 중복 업로드하지 않고 각 프로젝트가 소유하는 로컬·repository 자산으로 관리하라**고 명시한 경우에만 적용하는 선택형 adapter다. 기존 이미지 기획·승인·권리·실제 소비처·runtime 검증 owner를 대체하지 않는다.

```text
OPT_IN_LOCAL_VISUAL_DELIVERY_PROFILE
EXPLICIT_USER_DELEGATION_REQUIRED
PROJECT_LOCAL_VISUAL_BINARY_FIRST
NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY
NO_NOTION_BINARY_UPLOAD_REQUIRED
NOTION_BINARY_DELIVERY_OPTIONAL_BY_EXPLICIT_PROJECT_POLICY
COMPOSE_PROJECT_LOCAL_ASSET_VAULT_NOT_SECOND_CANON
CURRENT_PROJECT_AND_BASE_OWNER_WIN_ON_DRIFT
```

상세 owner:

- 이미지 필요성·생성·검수: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- 프로젝트 로컬 후보·승격: `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
- Art Direction·coverage·actual consumer: current Project Visual canon + current Base Visual owner
- Work↔Codex 최소 전환: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- 시작 정본 확인·선교정: `WORK_PROJECT_START_CANON_CHECKLIST.md`

이 adapter는 위 owner의 세부 절차를 복제하지 않는다. 충돌 시 사용자의 최신 지시 → Project canon/AGENTS → current Base owner → 이 adapter의 오래된 표현 순으로 판정한다.

## 1. 적용 범위와 Notion 역할

이 profile이 활성화되면 이미지 **바이너리의 작업·승인·구현 전달 경로**는 프로젝트 로컬 자산 경로와 repository가 소유한다.

```text
Notion
→ Project Home / Visual Bible / Asset Catalog / Flow / Production 구조와 Art Direction 참고
→ 사람이 보는 asset_id·의도·상태·consumer·repository locator 요약은 선택적으로 유지
→ image binary upload/attachment/readback은 완료 필수조건이 아님

Project local + repository
→ candidate bytes
→ SHA-256 / provenance / rights
→ approved tracked bytes
→ ASSET_MANIFEST.yml
→ Scene/Resource runtime consumer
→ test/runtime/build evidence
```

```text
NOTION_UPLOAD_NOT_RUN
NO_FALSE_NOTION_UPLOAD_CLAIM
```

- Notion에 실제 binary를 올리지 않았으면 `업로드 완료`, `attachment readback PASS`, `Notion 원본 보존 완료`라고 쓰지 않는다.
- Notion human canon을 수정했다면 해당 텍스트·상태·repository locator만 destination readback한다.
- Notion 구조와 승인된 Visual 방향은 계속 fresh-read한다. `Notion binary 생략`은 `Notion 기획·Visual canon 무시`가 아니다.
- 프로젝트가 별도로 Notion binary를 정본으로 요구하면 해당 Project 결정이 우선하며 이 profile을 `NOT_APPLICABLE_PROJECT_OVERRIDE`로 둔다.

## 2. 작업 시작 체크리스트 확장

`PROJECT_START_CANON_CHECKLIST`의 `visual_audio_asset_state`를 다음 receipt로 확장한다.

```yaml
PROJECT_START_VISUAL_ASSET_ROUTE_EXTENSION:
  product_implementation_baseline:
  latest_router_or_canon_sync:
  visual_asset_binary_owner: PROJECT_LOCAL_REPOSITORY | NOTION_BINARY | OTHER | UNKNOWN_UNVERIFIED
  notion_visual_reference_surface:
  project_local_candidate_root:
  tracked_asset_root:
  asset_manifest:
  current_candidate_identities: []
  runtime_promoted_assets: []
  visual_asset_durability_gap: []
  local_write_capability: CALLABLE | NOT_CALLABLE | UNKNOWN_UNVERIFIED
  codex_consumption_route:
  result: READY | CORRECTION_REQUIRED | BLOCKED_UNVERIFIED
```

`product_implementation_baseline`은 현재 실제 기능·player-facing 구현 기준 SHA다. `latest_router_or_canon_sync`는 그 뒤의 문서·router·handoff-only 동기화 SHA일 수 있다. 두 의미를 하나의 `current_completed_main` 값으로 덮어써 구현 기준선이 순환하지 않게 한다.

시작 체크리스트에서 다음을 먼저 교정한다.

```text
Notion Visual/Asset 구조
↔ Project structured canon
↔ local candidate root
↔ tracked approved asset root
↔ ASSET_MANIFEST.yml
↔ actual Scene/Resource consumer
```

한 위치의 record가 다른 위치의 bytes·승인·runtime 소비를 자동 증명하지 않는다.

## 3. 로컬 GPT 직접 저장

```text
LOCAL_GPT_DIRECT_PROJECT_WRITE_WHEN_CALLABLE
EXACT_PROJECT_ROOT_REQUIRED
PROJECT_SCOPED_FILE_WRITE_ONLY
TOOL_NOT_CALLABLE_DO_NOT_CLAIM
```

현재 host가 exact project filesystem write capability를 실제로 제공하면 Work/local GPT는 이미지 결과를 브라우저 다운로드·Notion 경유 없이 다음과 같은 project-local 후보 위치에 직접 저장할 수 있다.

```text
<project-root>/.asset-vault/library/work-generated/<asset-id>/
```

저장 전 확인:

```yaml
LOCAL_VISUAL_WRITE_INPUT:
  exact_project_identity:
  exact_project_root:
  current_branch_or_worktree:
  requirement_id:
  asset_id:
  actual_consumer:
  current_art_direction:
  approved_brief_or_delegation:
  required_count:
  format_dimensions_alpha_crop:
  protected_identity: []
  excluded_scope: []
```

규칙:

- 다른 프로젝트 폴더·Downloads 전체·사용자 개인 폴더를 추측하지 않는다.
- 요구 수량은 독립 파일 수와 일치해야 한다. 명시되지 않은 collage·시트·패널 합성을 runtime asset으로 사용하지 않는다.
- 같은 `asset_id`의 기존 bytes를 명시적 replacement decision 없이 덮어쓰지 않는다.
- 파일 저장 뒤 실제 존재·format·dimensions·SHA-256을 readback한다.
- 현재 tool이 local write를 지원하지 않으면 `BLOCKED_NO_LOCAL_ASSET_WRITE`로 두고 기존 안전 전달 route 또는 user-only last resort를 사용한다. 저장했다고 추측하지 않는다.

기존 `.asset-vault`가 구성된 프로젝트에서는 current vault owner의 `sync`를 사용해 Godot-visible local candidate로 투영한다.

```text
.asset-vault/library/work-generated/
→ sync
→ assets/_vault_local/
→ LOCAL_VISUAL_CANDIDATE
```

프로젝트가 다른 approved local candidate path를 소유하면 그 경로를 사용하고 Base 기본 경로를 강제 migration하지 않는다.

## 4. Candidate와 제품 승격

```text
LOCAL_VISUAL_CANDIDATE
!= PROJECT_ASSET_APPROVED
!= RUNTIME_PROMOTED
!= HUMAN_USABILITY_PASS
!= PLAYER_EXPERIENCE_PASS
```

상태:

```text
GENERATED_EXPLORATION
→ LOCAL_VISUAL_CANDIDATE
→ PROJECT_ASSET_APPROVED
→ tracked project asset promote
→ Codex/runtime consumption
→ RUNTIME_PROMOTED
```

`LOCAL_CANDIDATE_NOT_CODEX_DURABLE_INPUT`:

- local-only candidate는 remote Codex, 새 Work, 다른 PC, GitHub Actions가 볼 수 있다고 가정하지 않는다.
- current Slice에서 실제 구현에 사용할 승인 자산은 Codex 인계 전에 project-owned tracked path로 `promote`한다.
- `ASSET_MANIFEST.yml` 또는 프로젝트가 채택한 동등 manifest를 갱신한다.
- 검증된 feature branch commit에 포함하고 remote HEAD readback까지 완료한다.

```text
COMMIT_AND_REMOTE_READBACK_BEFORE_REMOTE_CODEX
```

같은 로컬 worktree에서 callable한 Codex가 candidate를 볼 수 있더라도, current Slice의 승인 product input은 최종적으로 tracked project asset과 manifest identity로 정본화해야 한다. local-only 절대 경로를 Scene/Resource·handoff·CI dependency로 남기지 않는다.

### 4.1 Visual production packet override

이 profile이 활성화되면 generic minimum-transition profile의 Visual packet에서 `notion_destination`·Notion binary delivery를 다음 필드로 좁게 대체한다.

```yaml
VISUAL_PRODUCTION_PACKET_LOCAL_OVERRIDE:
  requirement_id:
  asset_id:
  actual_consumer:
  consumer_surface_and_slot:
  current_art_direction:
  approved_reference_or_style_anchor:
  required_count:
  independent_briefs: []
  format_dimensions_alpha_crop_import:
  protected_identity_and_canon: []
  excluded_scope: []
  objective_acceptance: []
  provenance_and_rights:
  project_local_candidate_path:
  project_owned_tracked_path:
  asset_manifest_path:
  sha256:
  durable_commit_or_artifact:
  notion_reference_surface:
  runtime_validation:
```

`notion_reference_surface`는 Art Direction·구조·사람용 상태를 읽기 위한 locator다. binary upload destination이 아니다.

### 4.2 Manifest 최소 필드

```yaml
PROJECT_VISUAL_ASSET_RECORD:
  asset_id:
  requirement_id:
  status: LOCAL_VISUAL_CANDIDATE | PROJECT_ASSET_APPROVED | RUNTIME_PROMOTED | SUPERSEDED
  sha256:
  dimensions:
  format:
  project_relative_source_path:
  tracked_asset_path:
  actual_consumer:
  runtime_slot:
  provenance_and_rights:
  approval_reference:
  exact_commit_or_artifact:
  replacement_policy:
  runtime_evidence:
```

사용자 PC 절대 경로, secret, browser download URL을 durable project record로 사용하지 않는다.

## 5. 구현 충실도와 가짜 UI 방지

```text
APPROVED_SCREEN_REFERENCE_IS_INFORMATION_ARCHITECTURE_NOT_FAKE_FEATURE_AUTHORITY
CURRENT_GAME_RULES_AND_ACTUAL_DATA_ONLY
```

- 승인 시안은 current runtime에 맞춘 정보 구조·시각적 우선순위의 구현 기준이다.
- 시안에 있어도 current canon·data·runtime에 없는 규칙·스킬·적 행동·두 번째 board·가짜 수치 등을 그럴듯한 UI로 추가하지 않는다.
- 화면과 시안이 다르면 **현재 게임 규칙과 실제 데이터에 기반한 범위 안에서** hierarchy·readability·feedback을 개선한다.
- runtime asset 사용 시 exact file, Scene/Node/Resource consumer, Atlas/slice/pivot, input blocking 여부를 기록한다.

## 6. Exact Candidate Freshness

```text
EXACT_CANDIDATE_FRESHNESS
EXACT_RUNTIME_CANDIDATE_FRESHNESS
CANDIDATE_FRESHNESS_FOLLOWS_PLAYER_FACING_BYTES
```

빌드·패키지·runtime screenshot·visual QA candidate는 생성 당시의 exact player-facing bytes에만 유효하다.

다음이 main 또는 current candidate branch에 반영되면 기존 candidate를:

```text
HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE
```

로 전환하고 영향받는 export/runtime/screenshot Gate를 다시 수행한다.

- player-facing GDScript/code
- Scene/Resource/game data/localization
- renderer/HUD/route/switch/feedback 표현
- 실제 소비 asset bytes 또는 asset path
- import setting·atlas·slice·pivot·filter/compression
- export/package setting

```text
TOOLING_TEST_DOC_ONLY_DOES_NOT_INVALIDATE_CANDIDATE
```

도구·테스트·문서만 바뀌고 product/package bytes와 실행 의미가 변하지 않으면 기존 candidate를 자동 무효화하지 않는다. 다만 그 변경이 build contents·validation protocol·candidate claim에 영향을 주면 해당 Gate만 재검토한다.

Candidate pointer는 repository의 단일 structured owner가 소유한다. Notion이 있다면 이를 사람용으로 요약할 수 있지만 별도 candidate truth를 만들지 않는다.

## 7. Godot import·생성물 경계

```text
IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF
NEVER_STAGE_GENERATED_IMPORT_NOISE
PROJECT_ENGINE_POLICY_DISCOVERY_REQUIRED
```

- `.godot/`과 내부 imported cache는 기본적으로 파생 상태이며 product source 변경과 분리한다.
- Godot 실행·import 전후 tracked source diff와 staged diff를 따로 확인한다.
- cache 생성만으로 자산 승격·runtime PASS를 주장하지 않는다.
- `*.import`과 `*.uid`는 Godot version·project policy·실제 tracked consumer에 따라 source-control 의미가 달라질 수 있으므로 공용 지시문에서 **일괄 금지**하거나 일괄 stage하지 않는다.
- 현재 프로젝트의 `.gitignore`, engine version, repository tracked state, 공식 current engine guidance를 확인해 필요한 source metadata만 포함한다.
- unrelated `.godot/`, editor cache, platform derivative, 임시 screenshot/log를 제품 변경에 섞지 않는다.

Godot 프로젝트 organization/import 원칙상 source asset은 project folder 안에 두며 import cache와 source-control 대상은 구분한다. 상세은 current Project engine owner와 공식 current Godot 문서를 따른다.

## 8. Git·LFS·Codex 전달

```text
PROJECT_GIT_POLICY_DISCOVERY_REQUIRED
GIT_LFS_NOT_GLOBAL_DEFAULT
ZERO_INCREMENTAL_COST_REQUIRED
```

- 일반 PNG/WebP 등은 current repository policy와 크기·history impact가 허용하면 normal Git tracked asset으로 관리한다.
- Git LFS는 repository가 이미 채택했거나 file size/history/clone 비용상 실제 필요하고, 권한·quota·추가비용·Codex/CI checkout 호환성을 확인한 경우에만 사용한다.
- `Git LFS가 존재한다`는 이유만으로 모든 이미지를 LFS로 migration하지 않는다.
- approved tracked bytes를 push한 뒤 remote branch에서 blob/LFS pointer와 expected SHA identity를 readback한다.
- Codex handoff는 local path가 아니라 project-relative path, manifest record, exact commit, consumer, acceptance를 전달한다.

```yaml
CODEX_VISUAL_ASSET_HANDOFF:
  asset_id:
  requirement_id:
  project_relative_path:
  manifest_path:
  exact_commit_or_artifact:
  expected_sha256:
  actual_consumer:
  runtime_slot:
  import_expectation:
  acceptance:
  forbidden_replacement_or_drift: []
```

## 9. Test·CI·artifact 증거층

```text
TEST_LOGIC_PASS != CI_GATE_PASS
CI_WORKFLOW_AND_ARTIFACT_CONTRACT_REQUIRED
```

로컬/GUT test logic가 통과해도 CI workflow·parser·summary·artifact·required check가 실패하면 merge-ready가 아니다.

다음을 분리한다.

```text
test runner exit status
→ GUT/JUnit/result consistency
→ workflow parser/summary compatibility
→ required artifact creation
→ exact-HEAD required checks
→ safe merge
```

CI가 summary parser·artifact upload·workflow contract 때문에 실패하면 실제 로그를 읽고 원인을 분리한다. check를 녹색으로 만들기 위해 test·workflow·baseline을 약화하거나 우회하지 않는다.

## 10. 완료·heartbeat·증거 한계

```text
COMPLETED_PR_HEARTBEAT_CLEANUP_WHEN_PRESENT
```

현재 프로젝트가 long-running PR heartbeat/scheduler를 실제로 채택한 경우에만, current-task PR merge·post-merge·required readback 완료 뒤 그 heartbeat를 삭제·비활성화하고 readback한다. heartbeat가 없는 프로젝트에는 새 시스템을 만들지 않는다.

완료 evidence:

```yaml
LOCAL_VISUAL_DELIVERY_EVIDENCE:
  exact_project:
  requirement_and_asset_id:
  notion_reference_read:
  local_write_invocation:
  local_candidate_readback:
  candidate_sha256:
  approval_reference:
  tracked_promotion:
  asset_manifest_readback:
  exact_commit_or_artifact:
  remote_readback:
  actual_consumer:
  runtime_visual_evidence:
  candidate_freshness:
  ci_and_artifact_evidence:
  notion_binary_upload: NOT_RUN | NOT_APPLICABLE_PROJECT_LOCAL_PROFILE | ACTUALLY_EXECUTED
  human_usability: NOT_RUN
  player_experience: NOT_RUN
```

```text
local file exists
!= tracked durable asset
!= Codex consumed
!= runtime imported
!= screen semantics PASS
!= Human usability PASS
!= Player Experience PASS
```

## 11. 프로젝트 전용 요청 흡수 경계

다른 프로젝트 작업에서 발견한 다음 종류의 값은 공용 Base로 복사하지 않는다.

```text
specific PR number
specific Task/Decision ID
specific SHA or worktree path
specific resolution or scene count
specific art-style token, palette, character default
specific faction/route/social-policy/content rule
specific protected file path
```

공용화 가능한 것은 그 값이 드러낸 최소 원리뿐이다.

```text
project evidence
→ project-neutral failure pattern
→ existing owner search
→ additive narrow rule
→ regression evidence
→ no project-specific value leakage
```

관련 공용 사례:

`docs/knowledge/cases/PROJECT_LOCAL_VISUAL_ASSET_WITHOUT_NOTION_BINARY_CASE.md`

## 12. 종료 조건

```text
NOTION_BINARY_IS_NOT_REQUIRED_FOR_PROJECT_OWNED_VISUAL_BYTES
LOCAL_ONLY_IS_NOT_DURABLE_HANDOFF
```

이 profile의 현재 Slice Visual 준비 완료 조건:

```text
actual consumer identified
+ approved/current Art Direction read
+ exact project-local candidate bytes and SHA readback
+ PROJECT_ASSET_APPROVED where implementation will consume it
+ tracked project-owned bytes
+ manifest/provenance/rights
+ exact commit or durable artifact
+ Codex-readable locator
+ import/runtime consumer verification plan
+ Notion binary omission truthfully recorded
```

runtime 연결 뒤에는 `RUNTIME_PROMOTED` evidence가 별도로 필요하다. Human/Player 검증은 실제 사용자가 플레이하기 전까지 `NOT_RUN`이다.
