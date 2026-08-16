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
platform_resolution_camera:
existing_approved_assets:
figma_visual_bible_status: CONFIGURED | NOT_CONFIGURED | AUTH_REQUIRED | ACCESS_DENIED | READ_ONLY | LINK_UNVERIFIED | UNVERIFIED
figma_file_url:
figma_approved_reference_ids: []
figma_approved_frame_or_node_ids: []
figma_wip_target:
figma_interpretation_record_id:
figma_sync_status: NOT_APPLICABLE | UNVERIFIED | WIP_SYNCED | INTERPRETATION_SYNCED | FLOW_SYNCED | APPROVED_REFERENCE_SYNCED | FINAL_VISUAL_SYNCED
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
primary_use_status: NOT_RUN | IN_REVIEW | ACCEPTED | REVISION_REQUIRED
harvest_status: NOT_REVIEWED | NO_REUSE_VALUE | CANDIDATES_FOUND | STRUCTURED | SECOND_USE_VALIDATED
reuse_classification: UNASSESSED | REUSE_AS_IS | VARIANT_SEED | STRUCTURE_PATTERN | STYLE_DNA | REBUILD_FOR_REUSE | ONE_OFF_KEEP | REJECT_REUSE
decomposition_method: NONE | SOURCE_LAYER | MASK_CUTOUT | MANUAL_OR_SEMANTIC_REBUILD | DERIVED_GENERATIVE_RECOVERY
asset_vault_harvest_record_id:
second_use_validation: NOT_RUN | PASS | FAIL | NOT_APPLICABLE
```

Figma Visual Bible이 `CONFIGURED`이면 이미지 생성·편집 전에 Visual Artifact Registry와 연결된 `APPROVED_VISUAL_REFERENCE`의 실제 frame/node를 확인하고 `Keep / Avoid / Do Not Drift`를 작업 계약에 반영한다. 접근할 수 없으면 `AUTH_REQUIRED / ACCESS_DENIED / READ_ONLY / LINK_UNVERIFIED / UNVERIFIED`를 유지하며 내용을 확인했다고 추정하지 않는다. 상세 절차는 `skills/designing-art-prompts-and-technique-cards/references/figma-visual-bible-continuity-gate.md`를 따른다.

보존소가 `ENABLED`이면 `GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE`는 기본적으로 `.asset-vault/library/`와 `assets/_vault_local/`의 local-only 후보로 유지한다. `PROJECT_ASSET_APPROVED` 뒤에만 `promotion_target`을 확정하고 `promote`를 실행하여 `promoted_path`를 만든다. Figma `04_FINAL`과 제품 자산 승격은 서로 다른 상태다.

`primary_use_status`는 이미지가 원래 목적을 달성했는지 기록하고, `harvest_status`와 `reuse_classification`은 그 뒤 재사용 가치를 별도로 판정한다. `asset_vault_harvest_record_id`는 local-only Harvest metadata를 연결하기 위한 ID일 뿐 `PROJECT_ASSET_APPROVED`나 tracked 자산 승격을 의미하지 않는다.

## 2. Image backlog

| Image ID | Screen/Flow ID | 분류 | 목적·사용처 | 관련 정본 | 핵심 전달 | 비율·해상도 | 유지 요소 | 변경 축 | Figma 승인 Reference | 해석 상태 | Runtime 비교 | 레퍼런스 | vault_source_key | promotion_target | promoted_path | 우선순위 | 구현 난이도 | 재사용성 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

우선순위: `S / A / B`. 상태는 `PLANNED / GENERATED_EXPLORATION / IN_REVIEW / REVISION_REQUIRED / REJECTED / APPROVED_CANDIDATE / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED`.

`Figma 승인 Reference`는 실제로 확인한 `APPROVED_VISUAL_REFERENCE` ID만 기록한다. `vault_source_key`는 local vault의 현재 후보를 가리키며 Repo 정본 경로가 아니다. `promoted_path`는 `PROJECT_ASSET_APPROVED` 후 실제 tracked 자산이 생성된 경우에만 채운다.

## 3. Prompt contract

```text
목적과 사용자 경험
→ 프로젝트 정체성·정본 고정
→ 승인된 Figma reference ID·Keep/Avoid/Do Not Drift (구성된 경우)
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

| Review ID | Image ID | 기획 일치 | Figma 승인 Reference 일관성 | 핵심 경험 전달 | 실제 화면 가독성 | 구현 가능성 | 일관성 | 재사용·편집 | 권리·유사성 | 오류 | 판정 | 수정 요청 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Figma 일관성은 비율·실루엣·palette·line/texture/material·lighting·camera/composition·UI hierarchy·icon/VFX visual grammar를 최소 비교한다. 정본과 Figma가 충돌하면 `VISUAL_CANONICAL_CONFLICT`, Figma를 확인할 수 없으면 `BLOCKED_UNVERIFIED` 또는 정확한 접근 상태로 분리한다.

### 4A. Reusable Visual Harvest Review

Primary Use Gate에서 원래 목적이 `ACCEPTED`된 결과만 Harvest 대상으로 본다. 이 표는 working review surface이며 `ASSET_MANIFEST.yml`, `PROJECT_ASSET_APPROVED`, `promote`를 대체하지 않는다.

| Harvest ID | Image ID | Primary Use | Candidate | Classification | Existing Reuse Conflict | Method | Derived Pixels | Target Reuse | Second Use | Decision |
|---|---|---|---|---|---|---|---|---|---|---|

- `Classification`: `REUSE_AS_IS / VARIANT_SEED / STRUCTURE_PATTERN / STYLE_DNA / REBUILD_FOR_REUSE / ONE_OFF_KEEP / REJECT_REUSE`.
- `Method`: `SOURCE_LAYER / MASK_CUTOUT / MANUAL_OR_SEMANTIC_REBUILD / DERIVED_GENERATIVE_RECOVERY`.
- `DERIVED_GENERATIVE_RECOVERY`는 원본에서 관측된 사실이 아닌 generated/derived pixel이므로 별도 provenance와 검토를 요구한다.
- `ONE_OFF_KEEP`는 재사용 실패가 아니라 타이틀 고유 장면·서사 composition을 보호하는 정상 판정이다.

### 4B. Screen Interpretation Review

중요한 AI 생성 화면은 이미지 자체와 별개로 해석 기록을 남긴다. Figma가 쓰기 가능하면 화면 옆 편집 가능한 text/annotation `INTERPRETATION_RECORD`로 동기화하고, 불가능하면 책임 GitHub 기록 또는 프로젝트 Sheet에 남긴 뒤 실제 접근 상태를 유지한다.

| Review ID | Screen ID | Flow ID | Figma Interpretation ID | 관련 Decision | `CONFIRMED` | `DISCOVERED_IDEA` | `AI_ASSUMPTION` | `MISSING_CANON` | `VISUAL_CANONICAL_CONFLICT` | 버린 표현 | 다음 Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 없이 정본·구현 요구로 승격하지 않는다.

### 4C. Flow registration

여러 화면이 연결되면 `FLOW_MAP`에 `screen_id / flow_id`, 진입점, primary path, 취소·복귀, 실패 복구를 연결한다. 실제 클릭·전환 검토가 필요한 경우에만 `PROTOTYPE_FLOW`를 추가한다. Prototype은 Godot runtime proof가 아니다.

### 4D. Runtime compare

`runtime_compare_required: YES`인 화면은 승인 시각 참조와 실제 구현 캡처를 비교한다.

| Compare ID | Screen ID | Approved Artifact | runtime_capture_path | source commit | drift_status | 관찰 차이 | 후속 Decision/Finding |
|---|---|---|---|---|---|---|---|

`drift_status`: `MATCHED / INTENDED_DIFFERENCE / IMPLEMENTATION_GAP / PLANNING_CHANGE_REQUIRED / AI_MOCKUP_ERROR / VISUAL_CANONICAL_CONFLICT / BLOCKED_UNVERIFIED`. 실제 runtime 캡처가 없으면 Prototype만으로 `MATCHED`를 주장하지 않는다.

## 5. Approval sync

- [ ] `CURRENT_CONFIRMED_DECISIONS` 반영
- [ ] 관련 세계관·인물·시스템·아트·UI 정본 반영
- [ ] GitHub Issue·PR·main 반영
- [ ] `71_이미지기획_생성목록` 반영 또는 `NOT_CONFIGURED`
- [ ] `72_이미지검수_승인로그` 반영 또는 `NOT_CONFIGURED`
- [ ] Asset License Ledger·Asset Registry 반영
- [ ] Figma가 구성된 경우 실제 `APPROVED_VISUAL_REFERENCE` frame/node를 확인했거나 정확한 접근 실패 상태를 기록
- [ ] 신규 결과를 먼저 `02_WIP`/review candidate로 두고 사용자 승인 전 `01_APPROVED_REFERENCE`·`04_FINAL` 자동 승격 금지
- [ ] 중요 AI 화면은 필요 시 `INTERPRETATION_RECORD`와 `screen_id / flow_id`를 연결
- [ ] 연결된 화면은 `FLOW_MAP`을 갱신하고 필요한 경우에만 `PROTOTYPE_FLOW` 사용
- [ ] 승인 시 Visual Artifact Registry의 file/page/frame/node·Decision·status·snapshot·interpretation/runtime compare 관계와 Figma 위치를 동기화
- [ ] Figma `04_FINAL`을 `PROJECT_ASSET_APPROVED`·tracked asset·Godot runtime proof로 간주하지 않음
- [ ] 보존소 사용 시 `vault_source_key` 현재 상태 확인 또는 `VAULT_LOCAL_STATE_UNVERIFIED` 기록
- [ ] Primary Use Gate 뒤 `harvest_status`와 `reuse_classification`을 별도로 검토하고, 재사용 가치가 없으면 `NO_REUSE_VALUE`/`ONE_OFF_KEEP`를 정상 기록
- [ ] 구조화 후보가 생긴 경우 local-only `asset_vault_harvest_record_id`를 연결하되 이 ID를 제품 자산 승인으로 해석하지 않음
- [ ] `APPROVED_CANDIDATE`까지 local-only 유지; tracked 자산 자동 생성 금지
- [ ] `PROJECT_ASSET_APPROVED` 후 `promotion_target` 확정·`promote` 실행·`promoted_path` 기록
- [ ] tracked Scene/Resource가 `assets/_vault_local/`을 참조하지 않는지 `project_asset_vault.py check` 실행
- [ ] 실제 적용·런타임 검증 상태 기록
- [ ] `repository-wide-audit` 재실행
