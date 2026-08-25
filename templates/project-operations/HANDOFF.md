# Handoff

공용 실행·동기화 기준: `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`
공용 콜드 스타트·재개 기준: `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`

> 사용자가 `인수인계 진행`을 지시한 경우 이 문서는 단순 세션 요약이 아니다. 현재 작업을 안전한 checkpoint까지 닫고 GitHub·Notion 정본을 동기화한 뒤, 새 채팅이 과거 대화 없이 재개할 수 있는지 검증한 **종료 스냅샷**이어야 한다. 송신 측 `PACKET_READY`와 수신 측 `TRANSFER_ACCEPTED`는 별도 상태다.

## 인수 시점 상태

- 현재 단계:
- 현재 branch:
- current commit SHA:
- 승인 상태:
- 구현 상태:
- 검증 상태:
- handoff packet status: `PACKET_READY | NOT_READY | BLOCKED`
- transfer status: `PREPARED | PENDING_RECEIVER_ACK | TRANSFER_ACCEPTED | CONTEXT_DRIFT_RECHECK_REQUIRED`

## 완료한 작업과 증거

## 미완료 작업·차단 요소

각 항목은 `IN_PROGRESS / BLOCKED / NOT_RUN / UNVERIFIED` 중 필요한 상태를 명시한다.

## Resume checkpoint · 중복 실행 방지

```yaml
last_safe_checkpoint:
next_safe_action:
side_effects_already_applied:
  - action:
    destination:
    evidence:
idempotency:
  retry_safe: true | false | unknown
  verify_before_retry: []
```

- `last_safe_checkpoint`는 실제 검증된 마지막 완료 경계다.
- commit/push/merge, Issue/PR mutation, Notion update/upload, 승인 상태 변경처럼 이미 적용된 side effect는 다시 실행하기 전에 목적지를 확인한다.
- 동일 action이 이미 적용됐는지 모르면 `retry_safe: unknown`으로 두고 추정하지 않는다.

## GitHub 정본 동기화

```yaml
repository:
branch:
commit SHA:
prepared_from_main_sha:
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

## 적용 지침·Instruction surface

```yaml
instruction_surface_readback:
  root_agents:
  nearest_applicable_agents:
  project_instruction:
  path_specific_instruction:
  status: PASS | FAIL | NOT_APPLICABLE
```

- 프로젝트 `AGENTS.md`와 작업 경로에 더 가까운 적용 가능한 `AGENTS.md`를 확인한다.
- Handoff 요약이 현재 instruction surface를 대체하지 않는다.
- 지침 간 충돌이 발견되면 임의로 합치지 않고 current authority와 범위를 재검토한다.

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

## Pending user decisions

```yaml
pending_user_decisions:
  - decision_or_question:
    why_needed:
    options_or_constraints:
    safe_work_while_pending:
approval_required_before_resume: true | false
```

- 이미 승인된 결정은 `CURRENT_CONFIRMED_DECISIONS`와 책임 원본을 가리키고 다시 질문하지 않는다.
- 새 채팅이 임의 기본값을 선택하면 안 되는 미결 결정만 여기에 남긴다.
- `approval_required_before_resume: true`이면 그 결정에 의존하는 mutation은 receiver가 자동 실행하지 않는다.

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
- `BASE_PROMOTION_CANDIDATE`는 실제 Base learning/evidence 경로에 write + readback하기 전에는 handoff를 `PACKET_READY`로 닫지 않는다.
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

## Context sanitation

```yaml
context_sanitation:
  canonical_read_order_count: 3~7
  raw_tool_logs_included: false
  full_transcript_required: false
  superseded_material_included_only_if_needed: true
```

- raw tool log와 전체 대화 transcript를 기본 Handoff payload로 사용하지 않는다.
- 장문 evidence는 locator로 전달하고 receiver가 필요한 부분만 fresh-read한다.
- 압축 과정에서 보호 범위, 미결 승인, NOT_RUN, 실패 원인, rollback을 제거하지 않는다.

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
- `last_safe_checkpoint`, `next_safe_action`, 이미 실행된 side effect를 구분할 수 있는가? `PASS | FAIL`
- `pending_user_decisions`와 승인 전 안전한 작업 범위를 알 수 있는가? `PASS | FAIL | NOT_APPLICABLE`
- 적용되는 `AGENTS.md`/프로젝트 instruction surface를 찾을 수 있는가? `PASS | FAIL`

`FAIL`이 하나라도 있거나 과거 대화를 다시 붙여 넣어야 같은 품질로 이어갈 수 있으면 `HANDOFF_NOT_READY`다.

## Receiver freshness + ACK

새 채팅/담당자가 실제로 재개할 때 작성한다.

```yaml
resume_observed_main_sha:
canon_freshness: SAME_BASELINE | DRIFT_DETECTED | BLOCKED_UNVERIFIED
receiver_ack:
  current_state_readback:
  next_safe_action_readback:
  protected_scope_readback:
  pending_decisions_readback:
  side_effects_readback:
  status: TRANSFER_ACCEPTED | CONTEXT_DRIFT_RECHECK_REQUIRED | BLOCKED
```

- `prepared_from_main_sha`와 `resume_observed_main_sha`가 다르면 관련 diff/Notion 변화가 현재 작업에 영향을 주는지 먼저 확인한다.
- packet과 current canon이 일치해야 `TRANSFER_ACCEPTED`다.
- 실제 receiver가 없는 송신 세션에서는 `PENDING_RECEIVER_ACK`가 정상 종료 상태다. 이를 `TRANSFER_ACCEPTED`로 과장하지 않는다.

## 실행·미실행 검증

## 최종 Handoff Receipt

```yaml
handoff_packet_status: PACKET_READY | NOT_READY | BLOCKED
transfer_status: PREPARED | PENDING_RECEIVER_ACK | TRANSFER_ACCEPTED | CONTEXT_DRIFT_RECHECK_REQUIRED
github_locator:
notion_locator:
prepared_from_main_sha:
current_commit:
last_safe_checkpoint:
next_safe_action:
visual_audit:
pending_user_decisions:
lesson_disposition:
base_evidence_locator:
base_write_readback:
base_promotion:
receiver_ack:
rollback:
```

장문 기획과 수치는 책임 원본에 남기고 이 문서에는 상태·위험·다음 행동만 기록한다. 패키징·export PASS는 실제 Project Play의 화면·입력·완주 PASS를 대체하지 않는다.
