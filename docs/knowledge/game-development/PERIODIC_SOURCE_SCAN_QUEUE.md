# 주기 Source Scan Queue

```yaml
document_role: scheduled-source-review-queue-adapter
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
operational_state_owner: docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
specialty_source_owner: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
scheduler_runtime: GITHUB_ACTIONS
new_active_skill: false
independent_ledger: false
```

## 목적

`.github/workflows/periodic-source-scan-queue.yml`은 매주 월요일 10:17 KST와 수동 실행에서 현재 Ledger의 due Source를 읽어 열린 `[Periodic Source Scan Queue]` Issue 하나를 생성하거나 갱신한다. 이 문서는 두 번째 Watchlist·Evidence Method·Ledger가 아니다.

```text
주기 알림·작업 큐
!= Source scan 완료
!= Evidence 검증
!= Base 흡수
!= 프로젝트 Canon 반영
```

## 권한과 금지

```yaml
repository_permissions:
  contents: read
  issues: write
article_body_auto_ingestion: false
attachment_auto_download_or_execution: false
ledger_auto_update: false
project_canon_auto_write: false
content_pr_auto_create: false
auto_merge: false
```

- Schedule과 `workflow_dispatch`만 허용한다.
- 외부 PR 코드나 fork를 privileged token으로 실행하지 않는다.
- Article HTML·PDF·첨부 파일을 자동 다운로드·실행하지 않는다.
- Issue의 외부 문자열을 shell code로 평가하지 않는다.
- 공식 GitHub Action은 전체 commit SHA로 고정한다.
- Issue 생성·갱신 외의 repository write를 하지 않는다.

## 매 주기 필수 작업

Queue는 due Source가 없어도 다음 두 작업을 모두 요구한다.

```text
기존 Source의 새 글·수정 글 확인
+
신규 Source 사이트 탐색
```

### 기존 Source의 새 글·수정 글 확인

- Ledger의 due Source뿐 아니라 현재 Watchlist·Specialty Radar에 등록된 Source 표도 확인한다.
- 최근 추가된 Source가 아직 Ledger의 개별 cadence 상태를 갖지 않으면 Radar Source 표와 최신 `SOURCE_SCAN_CHECKPOINT_*.md`를 통해 재검토한다.
- last successful scan 또는 tracking start 이후의 새 글·수정 글을 구분한다.
- official recent/latest/archive/release surface와 원출처를 확인한다.
- 제목·snippet에서 멈추지 않고 `original source backtrace`를 수행한다.
- `published_or_updated_at`과 `checked_at`을 분리한다.
- Version·region·language·medium·sample·commercial interest를 기록한다.
- 성공 사례뿐 아니라 실패·혼합 결과·반례를 함께 찾는다.

### 신규 Source 사이트 탐색

- 현재 프로젝트·Base의 반복 실패와 비어 있는 Coverage에서 검색 질문을 만든다.
- 공식 기관·원자료·학술/현업·당사자/전문가 Source 후보를 추가 조사한다.
- 기존 Watchlist·Radar·Reference와 중복되는지, 더 권위 있는 원출처가 있는지 확인한다.
- 신규 사이트 수를 목표로 후보를 억지로 채우지 않는다.
- 지속적 material value가 불명확하면 `REFERENCE_ONLY` 또는 `BLOCKED_UNVERIFIED`로 닫는다.

## Scheduler 지속성

GitHub schedule은 기본 브랜치의 최신 Workflow에서 실행되지만 플랫폼 지연이나 비활성 저장소의 자동 비활성화가 발생할 수 있다. 따라서 schedule 존재만으로 지속 실행을 주장하지 않는다.

- `workflow_dispatch`를 수동 복구 경로로 유지한다.
- 월간 운영 검토에서 Workflow enabled 상태와 최근 성공 run을 확인한다.
- 예상 주기를 넘겨 성공 run이 없으면 `SCHEDULE_DRIFT`로 기록하고 수동 실행·원인 확인·재활성화를 수행한다.
- 예약 실행 시각이 지연되어도 같은 열린 Issue를 갱신하며 중복 Issue를 만들지 않는다.

## Evidence 경계

Issue의 링크·제목·snippet·요약은 원출처·날짜·버전·표본·권리·반례·consumer 검증 전까지 `UNVERIFIED_DISCOVERY`다.

```text
Queue 완료 != scan 완료
Issue 갱신 != Ledger timestamp 갱신
Issue check 표시 != Evidence 검증
Issue 존재 != 기존 owner 흡수
```

Workflow는 다음을 수정하지 않는다.

```text
last_successful_scan_at
last_material_candidate_at
material_candidate_count_since_tracking_start
last_base_contribution_at
last_base_contribution_ref
base_contribution_count_since_tracking_start
```

실제로 읽거나 조회한 Source만 weekly batch checkpoint에서 Ledger 갱신 후보가 된다. 기존 Source에서 파생된 변경이 `main`에 병합됐을 때만 contribution을 기록한다.

## Candidate Packet

```yaml
candidate_id:
source_name:
source_role:
original_url:
published_or_updated_at:
checked_at:
current_question_or_failure:
exact_era_region_language_medium_version:
sample_or_method:
commercial_or_creator_interest:
claim_or_practice:
original_source_backtrace:
current_base_owner:
current_project_consumer:
project_canon_conflict:
claim_ceiling:
failure_or_counterevidence:
rights_or_representation_risk:
validation_artifact:
rollback_or_discard_condition:
disposition: ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE
```

## 흡수·검증 Gate

```text
Existing Solution First
→ current Base owner
→ actual project consumer
→ smallest validation artifact
→ failure and rollback condition
→ adversarial attack
→ critique validation
→ bounded PR
→ exact-head regression
```

- 새 Skill·Guide보다 기존 owner의 Guide·Method·Reference·template·test 흡수를 먼저 판정한다.
- 실제로 바뀔 결정·파일·consumer가 없으면 링크 dump로 남기지 않는다.
- AI 추론, Source 주장, 프로젝트 사실, 실제 사람 관찰을 분리한다.
- 자동 Canon, 자동 PR, 자동 merge를 하지 않는다.
- 검증된 최소 개선만 기존 owner와 프로젝트 정본의 승인 경로로 보낸다.

## 완료·Rollback

Queue 자체 완료는 모든 candidate가 disposition으로 닫히고, 실제로 확인한 Source와 retained candidate가 weekly Ledger batch 후보로 분리됐을 때다. 이는 Base 변경·프로젝트 반영·사람 테스트 완료를 뜻하지 않는다.

Workflow를 제거하면 이후 Queue 갱신이 중단된다. Rollback 시 열린 Queue Issue를 닫고 본문에 `DISABLED_BY_ROLLBACK`을 기록한다. Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
