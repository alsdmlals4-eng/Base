# Work 실행 증거·후보·동기화 Identity 무결성

> 이 문서는 Work→Codex→Godot→CI→GitHub/Notion closeout에서 반복되는 **identity와 evidence 층 혼동**을 막는 프로젝트 중립 계약이다. 현재 Project canon·실제 구현·현재 Base 전문 owner를 대체하지 않는다.

```text
WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_BASE_OWNER_WINS_ON_DRIFT
PRODUCT_BASELINE_AND_ROUTER_SYNC_IDENTITY_SEPARATION
EXACT_CANDIDATE_FRESHNESS_RULE
CI_RESULT_CHAIN_INTEGRITY_REQUIRED
GENERATED_IMPORT_OUTPUT_CLASSIFICATION_REQUIRED
VISUAL_CANDIDATE_RUNTIME_PROMOTION_SEPARATION
REMOTE_SYNC_STATE_EXPLICIT_IN_CANON_LINKS
COMPLETED_AUTOMATION_HEARTBEAT_CLEANUP
PROJECT_SPECIFIC_VALUES_EXCLUDED
```

## 1. 적용 범위

다음 중 하나가 material할 때 적용한다.

- Work에서 확정한 입력을 Codex가 실제 제품 구현으로 소비하는 Playable Slice
- build/package/runtime/screenshot 후보의 최신성
- Godot import output과 tracked product source 구분
- local commit·asset과 remote durable locator 구분
- CI test logic·parser·artifact·required check 구분
- Visual 후보·승인 자산·runtime 소비 상태 구분
- current-task PR의 merge·post-merge·readback·heartbeat 정리

오탈자처럼 위 identity가 제품 결과에 영향을 주지 않는 L0 수정에서는 필요한 필드만 축소 사용한다.

## 2. 권위와 owner routing

```text
사용자의 최신 명시 지시
→ Project AGENTS / Active Context / 승인 Decision
→ Project GitHub·Notion 분야별 current owner
→ 실제 code/data/Scene/Resource/asset/test/runtime evidence
→ 현재 채택된 Base 전문 owner
→ 이 공용 identity interface
→ 과거 채팅·Memory·예전 handoff
```

이 문서는 다음 owner를 복제하지 않고 연결한다.

- 시작 정본 점검: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- Work↔Codex 최소 전환: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- 기본 진입: `WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md`
- 프로젝트 로컬 Visual: `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- 이미지 필요성·생성·검수: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- 프로젝트 자산 저장: `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
- Git·CI·Godot·IRG·완료: current Base/Project 전문 owner

```text
THIN_INTERFACE_NOT_SECOND_CANON
CURRENT_VISUAL_OWNER_WINS_ON_DRIFT
```

## 3. Identity ledger

material 실행에는 다음 identity를 하나의 current receipt로 구분한다.

```yaml
WORK_EXECUTION_IDENTITY_LEDGER:
  project:
  current_goal_or_slice:
  current_completed_product_main:
  latest_router_or_documentation_sync:
  current_validation_head:
  candidate_product_head:
  candidate_product_bytes_identity:
  export_or_package_identity:
  current_task_branch:
  local_head:
  remote_head:
  required_checks_identity:
  validator_or_workflow_identity:
  visual_candidate_identities: []
  runtime_promoted_asset_identities: []
  evidence_ceiling:
  observed_at:
```

한 필드가 다른 필드의 의미를 자동으로 대신하지 않는다.

## 4. 제품 기준선과 문서·router 동기화 분리

```text
PRODUCT_BASELINE_AND_ROUTER_SYNC_IDENTITY_SEPARATION
DOCUMENTATION_ONLY_MERGE_DOES_NOT_REWRITE_PRODUCT_BASELINE
```

- `current_completed_product_main`: 실제 player-facing 제품 구현의 최신 검증·병합 기준 SHA
- `latest_router_or_documentation_sync`: 그 뒤에 병합된 문서·router·handoff-only 동기화 SHA
- `current_validation_head`: 현재 test/CI/runtime 검증이 대상으로 삼은 exact HEAD
- `candidate_product_head`: build/package/runtime/screenshot 후보를 생성한 exact 제품 HEAD

문서-only merge가 발생해도 player-facing bytes가 변하지 않았다면 제품 구현 기준선을 문서 SHA로 순환 갱신하지 않는다.

반대로 문서처럼 보이는 변경이 export contents·runtime data·localization·asset path·validation claim을 바꾸면 product-impact로 재분류한다.

## 5. Exact Candidate Freshness

```text
EXACT_CANDIDATE_FRESHNESS_RULE
PLAYER_FACING_BYTE_CHANGE_INVALIDATES_CANDIDATE
HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE
TOOLING_DOC_TEST_ONLY_CHANGE_DOES_NOT_AUTO_INVALIDATE
CANON_DRIFT_FAIL_CLOSED
CONTEXT_DRIFT_RECHECK_REQUIRED
```

후보는 생성 당시 exact product/package bytes와 설정에만 유효하다.

다음이 변경되면 영향 후보를 `HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE`로 내린다.

- player-facing code·GDScript
- Scene·Resource·game data·localization
- renderer·HUD·flow·route·feedback
- 실제 소비 asset bytes/path
- import·atlas·slice·pivot·filter·compression
- export/package setting

도구·테스트·문서만 바뀌고 product/package bytes와 candidate claim이 동일하면 자동 무효화하지 않는다.

다만 다음 identity가 서로 다르면 새 후보 생성·승격·current 표기를 fail-closed한다.

```text
Project AGENTS / current owner
↔ current product baseline
↔ candidate ID / exact commit
↔ quality gate
↔ actual consumer
↔ next action
```

불일치는 `CONTEXT_DRIFT_RECHECK_REQUIRED`로 되돌리고 현재 source를 교정한 뒤 재개한다.

## 6. CI 결과 체인

```text
TEST_LOGIC_PASS_IS_NOT_CI_GATE_PASS
TEST_LOGIC_PASS != CI_GATE_PASS
CI_RESULT_CHAIN_INTEGRITY_REQUIRED
EXACT_VALIDATOR_IDENTITY_REQUIRED
NO_TEST_OR_WORKFLOW_WEAKENING_TO_FORCE_GREEN
```

다음을 별도 evidence로 확인한다.

```text
test runner exit status
→ formal result / JUnit or equivalent
→ summary/parser compatibility
→ required diagnostic/build artifact
→ repository current required check
→ exact current HEAD
```

필수 receipt:

```yaml
CI_RESULT_CHAIN:
  exact_current_head:
  validator_or_workflow_identity:
  test_runner_exit_status:
  formal_result:
  summary_or_parser:
  required_artifacts: []
  repository_required_checks: []
  conclusions: []
  result: PASS | FAIL | BLOCKED_UNVERIFIED
```

로컬 test logic가 PASS여도 parser·summary·artifact·required check가 실패하면 merge-ready가 아니다.

CI를 녹색으로 만들기 위해 다음을 하지 않는다.

- 관련 test 삭제
- baseline 또는 acceptance 약화
- parser 실패 은폐
- artifact requirement 제거
- 다른 SHA의 GREEN 재사용
- required check·ruleset 우회

기존 main의 독립 회귀가 발견되면 current Slice 관련 증거와 분리하고, 별도 Issue/owner로 기록한 뒤 독립 안전 작업을 계속한다.

## 7. Godot 생성물과 source identity

```text
GENERATED_IMPORT_OUTPUT_CLASSIFICATION_REQUIRED
IMPORT_CACHE_DIFF_IS_NOT_PRODUCT_SOURCE_DIFF
IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF
NEVER_STAGE_GENERATED_IMPORT_NOISE
NO_BLANKET_UID_OR_ADOPTED_ADDON_IGNORE
```

Godot 실행·import 전후 다음을 분리한다.

```text
tracked product source diff
staged diff
untracked candidate/source asset
.godot/ import/cache output
platform/editor derivative
runtime/build evidence
```

규칙:

- `.godot/`과 내부 cache는 product source 변경과 분리한다.
- cache 생성만으로 import·runtime·제품 변경 PASS를 주장하지 않는다.
- `.import`·`.uid`는 exact engine version과 current Project tracking policy를 확인한다.
- modern Godot의 `.uid`가 source identity인 경우 blanket ignore/delete하지 않는다.
- `addons/gut`은 current adoption record·설치 방식·exact version을 확인한다.
- vendored source, submodule, package-managed dependency를 같은 방식으로 가정하지 않는다.
- unrelated cache·screenshot·log·temporary build residue를 제품 commit에 섞지 않는다.

```yaml
GODOT_GENERATED_OUTPUT_RECEIPT:
  exact_engine_version:
  project_tracking_policy:
  adoption_record:
  tracked_source_delta:
  generated_cache_delta:
  uid_classification:
  addons_gut_classification:
  staged_paths: []
  excluded_generated_noise: []
  runtime_evidence:
```

## 8. Visual 후보와 runtime promotion

```text
VISUAL_CANDIDATE_RUNTIME_PROMOTION_SEPARATION
NO_VISUAL_GENERATION_AUTHORITY_EXPANSION
```

프로젝트 로컬 Visual profile이 명시적으로 활성화된 경우 상세 절차는 다음 owner가 담당한다.

```text
WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md
```

상태 의미:

```text
LOCAL_VISUAL_CANDIDATE
!= PROJECT_ASSET_APPROVED
!= RUNTIME_PROMOTED
!= HUMAN_USABILITY_PASS
!= PLAYER_EXPERIENCE_PASS
```

최소 interface:

```yaml
VISUAL_IDENTITY_INTERFACE:
  asset_id:
  requirement_id:
  status:
  SHA-256:
  project_relative_path:
  tracked_asset_path:
  manifest_path:
  exact_commit_or_artifact:
  actual_consumer:
  runtime_slot:
  provenance_and_rights:
  runtime_evidence:
```

규칙:

- local-only 후보는 durable remote Codex input이 아니다.
- current Slice에서 사용할 승인 자산은 project-owned tracked bytes와 manifest로 승격한다.
- push와 remote HEAD readback 전에는 GitHub durable locator라고 주장하지 않는다.
- import·crop·가독성·actual consumer·runtime screen evidence 뒤에만 `RUNTIME_PROMOTED`로 올린다.
- 시안은 정보 구조·시각 우선순위 reference일 수 있지만 current canon에 없는 규칙·수치·기능을 가짜 UI로 만들 권한이 아니다.
- 기존 승인 asset을 replacement decision 없이 삭제·덮어쓰지 않는다.

explicit local profile에서는 다음이 적용될 수 있다.

```text
PROJECT_LOCAL_VISUAL_BINARY_FIRST
NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY
NO_NOTION_BINARY_UPLOAD_REQUIRED
```

이는 Notion 기획·Visual 구조를 무시한다는 뜻이 아니다. Notion human-facing 텍스트·상태를 실제로 수정했다면 해당 destination readback은 유지한다. binary를 업로드하지 않았으면 업로드했다고 주장하지 않는다.

다른 Project Visual owner가 binary delivery를 필수로 정하면 해당 current Project 결정이 우선한다.

## 9. Local과 remote 동기화 상태

```text
REMOTE_SYNC_STATE_EXPLICIT_IN_CANON_LINKS
LOCAL_ONLY_NOT_REMOTE_SYNCED
REMOTE_HEAD_READBACK_REQUIRED
```

다음 상태를 구분한다.

```text
LOCAL_WORKTREE_ONLY
LOCAL_COMMITTED_NOT_PUSHED
PUSHED_REMOTE_UNVERIFIED
REMOTE_HEAD_READBACK_VERIFIED
MERGED_MAIN_READBACK_VERIFIED
```

Notion·handoff·manifest·completion receipt가 local-only commit을 가리키면 `LOCAL_ONLY_NOT_REMOTE_SYNCED`라고 명시한다.

current-task feature branch를 push한 뒤:

```text
expected local head
→ remote branch head readback
→ exact SHA equality
→ PR head identity
```

를 확인한다.

remote readback 전에는 다른 Work·Codex·CI·PC가 해당 content를 소비할 수 있다고 가정하지 않는다.

## 10. 완료 자동화와 heartbeat 정리

```text
COMPLETED_AUTOMATION_HEARTBEAT_CLEANUP
```

프로젝트가 실제 long-running heartbeat/monitor를 채택한 경우에만 적용한다.

```text
current-task implementation complete
→ exact-head required checks
→ merge
→ post-merge main readback
→ required GitHub/Notion readback
→ durable completion receipt
→ 해당 완료 PR heartbeat/monitor disable 또는 remove
→ cleanup readback
```

watcher를 종료해도 durable completion receipt, test evidence, merge SHA, incident/lesson을 삭제하지 않는다.

heartbeat가 없는 프로젝트에는 새 monitor system을 만들지 않는다.

## 11. Slice Issue/PR 소유 경계

GitHub Issues를 사용하는 프로젝트에서는 하나의 Playable Slice에 하나의 current implementation Issue/PR을 기본으로 한다.

독립적인 기반 enablement가 필요하면 별도 PR로 분리할 수 있다. enablement merge 뒤 Slice PR을 latest completed main 기준으로 다시 검증한다.

Issues를 사용하지 않는 프로젝트에 Issue 생성을 강제하지 않는다.

다른 open/draft/ready PR은 명시적으로 current-task로 지정되지 않는 한 read-only다.

## 12. 프로젝트 전용 값 제외

```text
PROJECT_SPECIFIC_VALUES_EXCLUDED
PROJECT_SPECIFIC_PR_AND_PATH_STAY_IN_PROJECT_CANON
```

다음을 Base 공용 계약에 복사하지 않는다.

- 프로젝트명·캐릭터·유파·세계관·기능명
- 특정 PR/Issue/Task/Decision 번호
- 특정 SHA·branch·worktree·로컬 절대 경로
- 특정 해상도·Scene 수·HUD 구성
- Art Style token·palette·기본 캐릭터
- 특정 프로젝트의 완료 목록·다음 우선순위
- 특정 플랫폼·콘텐츠에만 적용되는 Human gate

공용화하는 것은 반복 가능한 실패 패턴·identity·evidence 경계다.

## 13. Evidence ceiling과 위험 경계

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
NO_PUBLIC_RELEASE_AUTHORITY
ZERO_INCREMENTAL_COST_REQUIRED
```

다음을 분리한다.

```text
policy present
!= actual invocation
!= durable effect
!= remote readback
!= CI required-check PASS
!= runtime verified
!= Human usability PASS
!= Player Experience PASS
```

자동 test·GUT·Hera·screenshot·headless·build smoke는 machine evidence다. 사용자가 실제 플레이하기 전 Human/Player evidence를 PASS로 승격하지 않는다.

다음은 별도 고위험 결정으로 보류한다.

- 공개 Release·스토어 게시·외부 홍보
- 신규 유료 비용
- license/rights 불확실 자산 포함
- account/security 권한 확대
- 파괴적 data/save/schema migration
- direct main·force push·admin/ruleset bypass

## 14. Completion receipt

```yaml
WORK_EXECUTION_EVIDENCE_COMPLETION:
  project:
  slice_or_goal:
  current_completed_product_main:
  latest_router_or_documentation_sync:
  current_validation_head:
  candidate_product_head:
  candidate_freshness:
  ci_result_chain:
  godot_generated_output_classification:
  visual_identity_state:
  local_remote_sync_state:
  current_task_pr:
  exact_review_head:
  merge_sha:
  post_merge_main_readback:
  required_notion_or_human_canon_readback:
  heartbeat_cleanup: NOT_APPLICABLE | NOT_RUN | PASS
  human_usability: NOT_RUN
  player_experience: NOT_RUN
  remaining_machine_executable_work:
  blockers: []
```

`remaining_machine_executable_work = 0`은 completion candidate다. 실제 상태 재검사와 최소 5회 full-scope adversarial review 뒤 새 blocking finding이 0일 때만 종료한다.

## 15. Rollback

이 계약 자체가 잘못된 경우:

```text
implementation squash commit revert
→ current router에서 owner link 제거
→ focused regression
→ Base current owners readback
```

Project product code·Visual asset·engine baseline·CI workflow를 이 문서 rollback 때문에 자동 변경하지 않는다.
