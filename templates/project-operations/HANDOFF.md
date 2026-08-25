# Handoff

공용 실행·동기화 기준: `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`
공용 콜드 스타트·재개 기준: `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`

> 사용자가 `인수인계 진행`을 지시한 경우 이 문서는 단순 세션 요약이 아니다. 현재 작업을 안전한 checkpoint까지 닫고 GitHub·Notion 정본을 동기화한 뒤, 새 채팅이 과거 대화 없이 재개할 수 있는지 검증한 **종료 스냅샷**이어야 한다.

## 인수 시점 상태

- 현재 단계:
- 현재 branch:
- current commit SHA:
- 승인 상태:
- 구현 상태:
- 검증 상태:
- handoff readiness: `READY | NOT_READY | BLOCKED`

## 완료한 작업과 증거

## 미완료 작업·차단 요소

각 항목은 `IN_PROGRESS / BLOCKED / NOT_RUN / UNVERIFIED` 중 필요한 상태를 명시한다.

## GitHub 정본 동기화

```yaml
repository:
branch:
commit SHA:
working_tree_expectation: CLEAN | USER_CHANGES_PRESERVED
changed_files:
issues_prs:
runtime_truth_checked: true | false
stale_locator_removed: true | false
update_steps:
  - GitHub Desktop에서 올바른 repository·branch 선택
  - Fetch origin
  - Pull origin
  - 로컬 HEAD와 전달 commit SHA 일치 확인
```

`Fetch origin → Pull origin` 순서를 구분한다. Fetch만 수행한 상태는 로컬 파일 적용 완료가 아니다.

## Notion 정본 동기화

```yaml
project_home:
domain_pages:
ai_system_pages:
visual_pages:
current_decisions_readback: PASS | FAIL | NOT_RUN
human_home_readback: PASS | FAIL | NOT_RUN
system_metadata_leak_check: PASS | FAIL | NOT_RUN
```

- 사람용 Home에는 프로젝트 목적·핵심 Flow·표·승인 Visual·현재 상태를 남긴다.
- 운영 receipt, SHA/PR/CI, 세부 검증·handoff 데이터는 AI/System 쪽에 둔다.
- GitHub와 Notion 중 한쪽만 갱신한 상태를 `SYNC_COMPLETE`로 선언하지 않는다.

## Notion 이미지·Visual 전달 검증

이번 작업에서 이미지가 생성·승인·참조·교체되었다면 반드시 작성한다.

```yaml
visual_audit_required: true | false
approved_visual_locations: []
upload_attach: PASS | FAIL | NOT_RUN
page_destination_readback: PASS | FAIL | NOT_RUN
attachment_or_image_readback: PASS | FAIL | NOT_RUN
human_visible: PASS | FAIL | NOT_RUN | UNVERIFIED
approval_scope_confirmed: PASS | FAIL | NOT_RUN
supersession_checked: PASS | FAIL | NOT_RUN
runtime_product_asset_status: APPROVED | CANDIDATE | REFERENCE_ONLY | NOT_APPLICABLE | UNVERIFIED
```

- URL/파일명/Asset metadata 존재만으로 `Visual delivery PASS`를 선언하지 않는다.
- `READBACK_PASS`, `HUMAN_VISIBLE_PASS`, `runtime product asset 승인`은 서로 다른 상태다.
- 깨진 링크, placeholder, superseded 승인본이 현행처럼 남은 경우 `HANDOFF_NOT_READY`다.

## 기본 실행 인계

- 프로젝트 파일:
- 기본 실행: `Project Play`
- 기대 첫 화면:
- 대표 플레이 흐름: 시작 → 실제 gameplay → 성공·실패·복귀
- 핵심 조작:
- 별도 Scene 선택·편집기 수동 설정 필요 여부: `없음`이어야 함
- 자동 검증:
- 수동 검수: `NOT_RUN / PASS / FAIL · RETEST_REQUIRED / BLOCKED`
- 알려진 문제:

## 문제 → 교훈 → Base 승격

작업 중 실제로 발생한 문제를 회고문이 아니라 재사용 증거로 정리한다.

```yaml
problems:
  - symptom:
    cause:
    fix_or_rejected_approach:
    evidence:
reusable_lesson:
reuse_scope: PROJECT_ONLY | PART_ONLY | BASE_PROMOTION_CANDIDATE | NO_NEW_REUSABLE_LESSON
base_owner_candidate:
base_evidence_locator:
base_write_readback: PASS | FAIL | NOT_REQUIRED
base_promotion_status: NOT_REQUIRED | CANDIDATE_RECORDED | PROMOTED | DEFERRED_BY_CONCURRENT_OWNER | BLOCKED_UNVERIFIED
```

- Base 승격은 기존 canonical owner에 흡수하는 것을 우선한다.
- `BASE_PROMOTION_CANDIDATE`는 실제 Base learning/evidence 경로에 write + readback하기 전에는 handoff를 `READY`로 닫지 않는다.
- 같은 owner를 열린 PR이 수정 중이면 그 PR을 변경·흡수하지 않는다. 충돌하지 않는 Base evidence/candidate 파일을 실제 기록·readback하고 `DEFERRED_BY_CONCURRENT_OWNER`로 남긴다.
- `PROJECT_ONLY`는 프로젝트에 남기고 Base에 억지로 승격하지 않는다.
- 새 광역 Skill·중복 정책은 반복 재사용 가치와 owner 부재가 입증되기 전 만들지 않는다.

## 다음 작업자의 첫 행동

1.
2.
3.

## 변경하면 안 되는 결정·경로

## 읽기 순서

먼저 읽을 책임 원본은 3~7개로 압축한다.

1.
2.
3.

## Fresh-chat resumability test

새 채팅이 이전 대화·메모리 없이 GitHub + Notion current canon만 읽는다고 가정한다.

- 무엇을 만드는가? `PASS | FAIL`
- 어디까지 결정·구현·검증됐는가? `PASS | FAIL`
- 다음 작업과 선행 조건은 무엇인가? `PASS | FAIL`
- 무엇을 변경하면 안 되는가? `PASS | FAIL`
- 책임 원본·실제 파일·검증 위치를 찾을 수 있는가? `PASS | FAIL`
- 미확정·보류·위험을 알 수 있는가? `PASS | FAIL`
- 승인 Visual의 현재 위치·용도·교체 관계를 알 수 있는가? `PASS | FAIL | NOT_APPLICABLE`
- 문제·교훈과 Base 승격 상태를 알 수 있는가? `PASS | FAIL | NOT_APPLICABLE`
- Base 승격 후보의 실제 Base evidence/learning locator와 readback 결과를 찾을 수 있는가? `PASS | FAIL | NOT_APPLICABLE`

`FAIL`이 하나라도 있거나 과거 대화를 다시 붙여 넣어야 같은 품질로 이어갈 수 있으면 `HANDOFF_NOT_READY`다.

## 실행·미실행 검증

## 최종 Handoff Receipt

```yaml
handoff_status: READY | NOT_READY | BLOCKED
github_locator:
notion_locator:
current_commit:
next_action:
visual_audit:
lesson_disposition:
base_evidence_locator:
base_write_readback:
base_promotion:
rollback:
```

장문 기획과 수치는 책임 원본에 남기고 이 문서에는 상태·위험·다음 행동만 기록한다. 패키징·export PASS는 실제 Project Play의 화면·입력·완주 PASS를 대체하지 않는다.
