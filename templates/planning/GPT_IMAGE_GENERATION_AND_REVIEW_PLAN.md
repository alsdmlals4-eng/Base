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
platform_resolution_camera:
existing_approved_assets:
project_sheet_status: PROJECT_SHEET_CONFIGURED | NOT_CONFIGURED
```

## 2. Image backlog

| Image ID | 분류 | 목적·사용처 | 관련 정본 | 핵심 전달 | 비율·해상도 | 유지 요소 | 변경 축 | 레퍼런스 | 우선순위 | 구현 난이도 | 재사용성 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

우선순위: `S / A / B`. 상태는 `PLANNED / GENERATED_EXPLORATION / IN_REVIEW / REVISION_REQUIRED / REJECTED / APPROVED_CANDIDATE / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED`.

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

## 5. Approval sync

- [ ] `CURRENT_CONFIRMED_DECISIONS` 반영
- [ ] 관련 세계관·인물·시스템·아트·UI 정본 반영
- [ ] GitHub Issue·PR·main 반영
- [ ] `71_이미지기획_생성목록` 반영 또는 `NOT_CONFIGURED`
- [ ] `72_이미지검수_승인로그` 반영 또는 `NOT_CONFIGURED`
- [ ] Asset License Ledger·Asset Registry 반영
- [ ] 실제 적용·런타임 검증 상태 기록
- [ ] `repository-wide-audit` 재실행
