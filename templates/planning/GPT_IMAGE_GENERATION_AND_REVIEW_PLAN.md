# GPT Image Generation and Review Plan

## 1. Context

```yaml
project:
project_stage:
approval_bundle:
image_phase: PLANNING_VISUALIZATION | FINAL_VISUAL_CANDIDATE
related_decisions:
canonical_sources:
player_experience:
target_screen_or_use:
screen_id:
flow_id:
figma_artifact_id:
platform_resolution_camera:
existing_approved_assets:
interpretation_status: CONFIRMED | DISCOVERED_IDEA | AI_ASSUMPTION | MIXED | UNVERIFIED
runtime_compare_required: YES | NO
runtime_capture_path:
drift_status: NOT_RUN | MATCHED | INTENDED_DIFFERENCE | IMPLEMENTATION_GAP | PLANNING_CHANGE_REQUIRED | AI_MOCKUP_ERROR | VISUAL_CANONICAL_CONFLICT | BLOCKED_UNVERIFIED
project_sheet_status: PROJECT_SHEET_CONFIGURED | NOT_CONFIGURED
asset_vault_status: ENABLED | NOT_CONFIGURED | VAULT_LOCAL_STATE_UNVERIFIED
vault_source_key:
workspace_path:
promotion_target:
promoted_path:
```

보존소가 `ENABLED`이면 `GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE`는 기본적으로 `.asset-vault/library/`와 `assets/_vault_local/`의 local-only 후보로 유지한다. `PROJECT_ASSET_APPROVED` 뒤에만 `promotion_target`을 확정하고 `promote`를 실행하여 `promoted_path`를 만든다.

## 2. Image backlog

| Image ID | Screen/Flow ID | Figma Artifact ID | 분류 | 목적·사용처 | 관련 정본 | 핵심 전달 | 비율·해상도 | 유지 요소 | 변경 축 | 레퍼런스 | 해석 상태 | runtime 비교 필요 | vault_source_key | promotion_target | promoted_path | 우선순위 | 구현 난이도 | 재사용성 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

우선순위: `S / A / B`. 상태는 `PLANNED / GENERATED_EXPLORATION / IN_REVIEW / REVISION_REQUIRED / REJECTED / APPROVED_CANDIDATE / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED`.

`vault_source_key`는 local vault의 현재 후보를 가리키며 Repo 정본 경로가 아니다. `promoted_path`는 `PROJECT_ASSET_APPROVED` 후 실제 tracked 자산이 생성된 경우에만 채운다.

## 3. Prompt contract

```text
목적과 사용자 경험
→ 프로젝트 정체성·정본 고정
→ 화면 구성과 정보 위계
→ 캐릭터·환경·오브젝트·UI 요구
→ 형태·색·재질·광원
→ 실제 화면비·크롭·해상도
→ 유지 요소와 변경 축
→ 금지·보호 요소
→ 텍스트 없는 마스터·편집 레이어
→ QA와 재생성 기준
```

## 4. Review

| Review ID | Image ID | 기획 일치 | 핵심 경험 전달 | 실제 화면 가독성 | 구현 가능성 | 일관성 | 재사용·편집 | 권리·유사성 | 오류 | 판정 | 수정 요청 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### 4A. Screen Interpretation Review

AI 생성 화면이나 중요한 중간 시각화는 이미지 자체와 별개로 해석 기록을 남긴다. Figma 쓰기가 가능하면 화면 옆 `INTERPRETATION_RECORD` 패널/annotation으로 동기화하고, 불가능하면 책임 GitHub 문서 또는 프로젝트 Sheet에 기록한 뒤 `SYNC_PENDING`/`UNVERIFIED`를 유지한다.

| Review ID | Screen ID | Flow ID | Figma Artifact ID | 관련 Decision | `CONFIRMED` | `DISCOVERED_IDEA` | `AI_ASSUMPTION` | `MISSING_CANON` | `VISUAL_CANONICAL_CONFLICT` | 버린 표현 | 다음 Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 없이 정본·구현 요구로 승격하지 않는다.

### 4B. Runtime compare

`runtime_compare_required: YES`인 화면은 승인 시각 참조와 실제 구현 캡처를 비교한다.

| Compare ID | Screen ID | Approved Artifact | runtime_capture_path | source commit | drift_status | 관찰 차이 | 후속 Decision/Finding |
|---|---|---|---|---|---|---|---|

`drift_status`: `MATCHED / INTENDED_DIFFERENCE / IMPLEMENTATION_GAP / PLANNING_CHANGE_REQUIRED / AI_MOCKUP_ERROR / VISUAL_CANONICAL_CONFLICT / BLOCKED_UNVERIFIED`. Prototype은 runtime proof가 아니므로 실제 구현 캡처가 없으면 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.

## 5. Approval sync

- [ ] `CURRENT_CONFIRMED_DECISIONS` 반영
- [ ] 관련 세계관·인물·시스템·아트·UI 정본 반영
- [ ] GitHub Issue·PR·main 반영
- [ ] `71_이미지기획_생성목록` 반영 또는 `NOT_CONFIGURED`
- [ ] `72_이미지검수_승인로그` 반영 또는 `NOT_CONFIGURED`
- [ ] Visual Artifact Registry의 `screen_id`, `flow_id`, `interpretation_status`, `runtime_compare_status` 동기화 또는 `NOT_CONFIGURED`
- [ ] Asset License Ledger·Asset Registry 반영
- [ ] 보존소 사용 시 `vault_source_key` 현재 상태 확인 또는 `VAULT_LOCAL_STATE_UNVERIFIED` 기록
- [ ] `APPROVED_CANDIDATE`까지 local-only 유지; tracked 자산 자동 생성 금지
- [ ] `PROJECT_ASSET_APPROVED` 후 `promotion_target` 확정·`promote` 실행·`promoted_path` 기록
- [ ] tracked Scene/Resource가 `assets/_vault_local/`을 참조하지 않는지 `project_asset_vault.py check` 실행
- [ ] 실제 적용·런타임 검증 상태 기록
- [ ] `repository-wide-audit` 재실행
