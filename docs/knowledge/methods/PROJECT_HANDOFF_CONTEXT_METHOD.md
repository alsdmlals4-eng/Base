# 프로젝트 인수인계·컨텍스트 설계 방법

- 상태: 공용 원칙·호환 경로
- 실행 Skill: `skills/maintaining-project-context-and-handoff/SKILL.md`
- 전체 운영 구조: `docs/OPERATING_MODEL.md`

이 문서는 콜드 스타트와 인수인계의 불변 원칙만 책임진다. Active Context 갱신과 Handoff 산출물의 단계형 실행은 Skill이 책임진다.

## 핵심 원칙

Active Context와 Handoff는 전체 기획서·Roadmap·과거 대화를 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업과 위험을 연결하는 압축 라우터**다.

방향, 수치, 용어, 범위, 구현 상태, 파일 경로 또는 작업 절차가 바뀌면 같은 작업 안에서 해당 책임 원본을 먼저 갱신한다. 인수인계 문서로 오래된 원본을 덮어쓰지 않는다.

`인수인계 진행`, `handoff`, `새 채팅으로 넘겨` 같은 사용자 요청은 단순 요약 요청이 아니라 **현재 bounded work를 안전한 checkpoint까지 닫고, 다음 세션이 과거 대화 없이 재개할 수 있게 만드는 종료 트랜잭션**으로 해석한다. 새 기능을 더 벌리는 대신 현재 작업의 정본·증거·미완료 경계를 먼저 닫는다.

Handoff는 **송신자가 만든 패킷**과 **수신자가 실제로 인수를 확인한 상태**를 구분한다. 송신 세션에서 패킷을 잘 만들었다는 이유만으로 실제 통제권 이전까지 완료됐다고 선언하지 않는다.

## 단일 현재 상태 원본

프로젝트는 `ACTIVE_CONTEXT.md`를 현재 상태의 기본 원본으로 사용한다.

```md
# Active Context
## Current State
## Recent Changes
## Next Work
## Risks and Unknowns
## Protected Scope
## Read Next
## Validation and Rollback
```

별도 Handoff는 세션·담당자·브랜치·마일스톤 경계에서 필요한 스냅샷으로 생성하며, 상시 두 번째 현재 상태 원본으로 유지하지 않는다.

## 상태 분리

- 승인
- 구현
- 검증
- 진행 중
- 미확정
- 보류
- 불일치
- `PACKET_READY`: 송신 측 Handoff 패킷이 재개에 필요한 정보를 갖춤
- `PENDING_RECEIVER_ACK`: 새 채팅/담당자가 아직 fresh-read와 readback을 완료하지 않음
- `TRANSFER_ACCEPTED`: 수신자가 최신 정본을 다시 읽고 현재 상태·다음 행동·보호 범위를 명시적으로 확인함

`승인`과 `구현`, `구현`과 `검증`, `PACKET_READY`와 `TRANSFER_ACCEPTED`를 같은 의미로 쓰지 않는다.

## 작성 규칙

- 현재 사실을 먼저 쓰고 역사적 배경은 링크로 보낸다.
- 같은 규칙의 전문을 여러 문서에 복제하지 않는다.
- 실제 확인하지 못한 결과는 `[미검증]`으로 남긴다.
- 프로젝트 방향·분야 본책·Roadmap·Skill을 먼저 갱신한다.
- Active Context에는 경로와 현재 차이만 기록한다.
- 먼저 읽을 책임 원본은 3~7개로 압축한다.
- 다음 작업의 선행 조건·완료 기준·롤백을 명시한다.
- raw tool log, 전체 대화 transcript, 반복된 CI 출력은 기본 Handoff 입력에서 제외한다.
- 예전 실패·기각·superseded 정보는 **다음 작업의 오류 재발 방지에 필요한 경우만** 간결하게 남긴다.

## 인수인계 패킷과 수신 ACK

현업의 명시적 command handoff 원칙을 적용해 **패킷 준비와 통제권 이전을 두 단계로 나눈다.**

```text
송신 세션
→ PACKET_READY
→ PENDING_RECEIVER_ACK
→ 새 채팅/담당자가 GitHub + Notion + 적용 지침 fresh-read
→ receiver_ack readback
→ TRANSFER_ACCEPTED
→ next_safe_action 실행
```

- 송신 세션은 새 채팅이 아직 존재하지 않으면 `PACKET_READY / PENDING_RECEIVER_ACK`까지 닫을 수 있다.
- 수신 세션은 첫 mutation 전에 프로젝트 목적, 현재 단계, 최신 commit, 다음 작업, 보호 범위, 미결 승인, 승인 Visual 상태를 자기 말로 다시 확인한다.
- 이 확인을 `receiver_ack`로 기록한다. 단순히 “읽었다”가 아니라 **무엇을 읽고 무엇을 다음에 할지**가 들어가야 한다.
- 수신자가 packet과 current canon의 불일치를 발견하면 ACK하지 않고 `CONTEXT_DRIFT_RECHECK_REQUIRED`로 전환한다.
- 실제 소유권 이전을 기록할 필요가 없는 단순 개인 메모 handoff는 `TRANSFER_ACCEPTED`를 강제하지 않아도 되지만, **새 채팅/다른 AI/다른 담당자에게 작업을 넘기는 경우에는 필수**다.

## 재개 체크포인트와 중복 실행 방지

Handoff는 “다음에 무엇을 할지”만 남기지 않고 **어디까지 안전하게 완료됐고 어떤 부작용이 이미 적용됐는지** 남긴다.

```yaml
last_safe_checkpoint:
next_safe_action:
side_effects_already_applied: []
idempotency:
  retry_safe: true | false | unknown
  verify_before_retry: []
```

- `last_safe_checkpoint`는 문서 작성 시점이 아니라 **실제로 검증된 마지막 완료 경계**다.
- `side_effects_already_applied`에는 commit/push/merge, Notion update/upload, 승인 상태 변경, Issue/PR mutation처럼 다시 실행하면 중복되거나 위험한 행위를 기록한다.
- 수신자는 같은 mutation을 재실행하기 전에 목적지 readback으로 이미 적용됐는지 확인한다.
- 재실행 안전성을 보장할 수 없으면 `retry_safe: unknown`으로 두고 추정하지 않는다.
- Handoff 때문에 같은 이미지가 다시 업로드되거나 같은 결정이 중복 기록되거나 같은 PR mutation이 반복되면 인수인계 품질 실패다.

## 적용 지침·정본 Freshness 재수화

새 채팅은 Handoff 텍스트 자체보다 **현재 작업 경로에 실제 적용되는 지침과 최신 정본**을 먼저 복원한다.

```yaml
instruction_surface_readback:
  root_agents:
  nearest_applicable_agents:
  project_instruction:
  path_specific_instruction:
  status: PASS | FAIL | NOT_APPLICABLE
prepared_from_main_sha:
resume_observed_main_sha:
canon_freshness: SAME_BASELINE | DRIFT_DETECTED | BLOCKED_UNVERIFIED
```

- 프로젝트 `AGENTS.md`가 있다면 읽고, 작업 경로 아래에 더 가까운 `AGENTS.md`가 있으면 그 범위를 우선 확인한다.
- 저장소 공용 지침·프로젝트 지침·분야 정본이 서로 충돌하면 Handoff 요약으로 임의 해결하지 않는다.
- GitHub main/branch, open PR, Notion current canon이 packet 작성 후 이동했는지 재조회한다.
- `prepared_from_main_sha != resume_observed_main_sha` 자체가 자동 실패는 아니지만, 변경이 현재 작업에 영향을 주는지 확인하기 전 mutation을 시작하지 않는다.
- 관련 정본 또는 적용 지침이 달라졌다면 `CONTEXT_DRIFT_RECHECK_REQUIRED`로 두고 현재 사실에 맞게 Active Context/Handoff locator를 재조정한다.

## 미결 사용자 결정 Gate

“남은 작업”과 “사용자 결정을 기다리는 작업”을 분리한다. 미결 결정이 일반 next task 안에 묻히면 다음 세션이 임의 기본값으로 처리할 위험이 있다.

```yaml
pending_user_decisions:
  - decision_or_question:
    why_needed:
    options_or_constraints:
    safe_work_while_pending:
approval_required_before_resume: true | false
```

- 사용자가 이미 승인한 결정은 `CURRENT_CONFIRMED_DECISIONS`와 책임 원본을 가리키고 다시 묻지 않는다.
- 아직 승인이 필요한 핵심 선택은 `pending_user_decisions`에 별도로 남긴다.
- `approval_required_before_resume: true`라면 해당 결정을 필요로 하는 제품 변경을 새 채팅이 자동 실행하지 않는다.
- 단, 결정과 무관한 read-only 조사·검증·정본 freshness 확인은 계속할 수 있다.

## Context sanitation / budget

새 채팅의 품질은 더 많은 토큰을 넘기는 것이 아니라 **필요한 토큰만 정확하게 넘기는 것**으로 검증한다.

```yaml
context_sanitation:
  canonical_read_order_count: 3~7
  raw_tool_logs_included: false
  full_transcript_required: false
  superseded_material_included_only_if_needed: true
```

- 기본 읽기 순서는 3~7개의 책임 원본/locator로 압축한다.
- raw tool log와 전체 대화 transcript를 그대로 인수인계 입력으로 붙이지 않는다.
- 장문 evidence는 locator만 주고, 수신자가 필요한 범위만 fresh-read한다.
- 현재 판단에 직접 필요한 결정·위험·미검증·rollback만 Handoff 본문에 남긴다.
- 압축 때문에 보호 범위, 미결 승인, NOT_RUN, 실패 원인이 사라지면 과도한 compaction으로 보고 실패 처리한다.

## 인수인계 완료 프로토콜

사용자가 인수인계를 지시하면 다음 순서를 하나의 완료 Gate로 취급한다.

1. **현재 작업 checkpoint 완료**
   - 지금 진행 중인 작업 단위를 가능한 안전한 완료점까지 닫는다.
   - 새 범위를 시작하지 않는다.
   - 완료하지 못한 항목은 숨기지 않고 `IN_PROGRESS / BLOCKED / NOT_RUN / UNVERIFIED`로 남긴다.
2. **Resume checkpoint / side-effect ledger 기록**
   - `last_safe_checkpoint`, `next_safe_action`, `side_effects_already_applied`, `idempotency`를 기록한다.
   - 동일 mutation 재실행 위험을 먼저 제거한다.
3. **GitHub 정본 동기화**
   - 현재 branch/main, 정확한 commit, 변경 파일, Issue/PR, 실제 코드·데이터·Scene·Resource·Test 상태를 다시 읽는다.
   - 승인·구현·검증 상태를 분리하고 stale locator를 제거한다.
4. **Notion 정본 동기화**
   - 사람용 Home/Domain/Visual과 AI/System 상세 페이지가 현재 결정과 맞는지 다시 읽는다.
   - Home에는 사람이 알아야 할 결과·Flow·표·승인 Visual을, AI/System에는 운영 메타데이터·검증·handoff 세부를 둔다.
5. **Instruction surface / freshness snapshot**
   - 현재 작업에 적용되는 `AGENTS.md`, 프로젝트 지침, 분야 정본을 확인한다.
   - packet 작성 기준 main SHA와 resume 시점 비교를 위한 freshness locator를 남긴다.
6. **Pending user decision 분리**
   - 승인된 결정과 아직 사용자 결정을 기다리는 항목을 구분한다.
   - 결정 전 자동 진행 금지 범위를 명시한다.
7. **Active Context 갱신 후 Handoff 생성**
   - Handoff는 `현재 상태 → 이번 작업 결과 → 남은 작업 → 위험·미검증 → 다음 작업자의 첫 행동 → 검증·롤백` 순서로 압축한다.
   - 과거 대화가 없으면 복원할 수 없는 핵심 사실이 남아 있으면 인수인계 미완료다.
8. **Fresh-chat resumability test**
   - 새 채팅이 이전 대화·기억 없이 **GitHub + Notion current canon만** 읽는다고 가정한다.
   - 아래 콜드 스타트 질문에 모두 답하고, 첫 작업 경로와 보호 범위를 찾을 수 있어야 한다.
   - 과거 대화를 다시 붙여 넣어야만 같은 품질로 이어갈 수 있으면 `HANDOFF_FAIL_CONTEXT_DEPENDENCY`다.
9. **Notion Visual delivery audit**
   - 이번 작업에 승인·참조·교체된 이미지가 있다면 올바른 프로젝트 Home/Visual/Asset 위치에 실제로 존재하는지 확인한다.
   - 링크/파일명/메타데이터 존재만으로 PASS하지 않는다. 가능한 transport 범위에서 upload/attach, destination readback, 이미지 block 또는 attachment content readback, 승인 상태·용도·supersession을 확인한다.
   - `READBACK_PASS`와 사용자가 실제로 보는 `HUMAN_VISIBLE_PASS`, 그리고 runtime product asset 승인을 구분한다.
   - 깨진 링크, placeholder, 이전 승인본이 현행인 것처럼 남은 상태는 인수인계 차단 사유다.
10. **문제 → 교훈 추출**
   - 작업 중 실제 발생한 문제, 원인, 해결/기각한 방법, 증거, 재발 방지 규칙을 기록한다.
   - `PROJECT_ONLY / PART_ONLY / BASE_PROMOTION_CANDIDATE / NO_NEW_REUSABLE_LESSON` 중 하나로 분류한다.
11. **Base 승격 기록·readback**
   - `BASE_PROMOTION_CANDIDATE`라면 검토 문구만 남기고 끝내지 않는다. 기존 Base canonical owner의 Learning/Evidence 경로에 실제 기록하고 destination readback까지 수행한다.
   - 열린 PR이 같은 owner를 변경 중이면 그 PR을 흡수·수정·재작성하지 않는다. 대신 충돌하지 않는 Base evidence/candidate 경로에 실제 파일을 기록·readback하고 `DEFERRED_BY_CONCURRENT_OWNER`로 남긴다. 이후 Integration에서 기존 owner에 흡수한다.
   - `PROJECT_ONLY`는 프로젝트에 남기고 Base를 오염시키지 않는다. `PART_ONLY`는 해당 Part owner에만 기록한다.
   - 새 광역 Skill/중복 정책을 자동 생성하지 않는다. 여러 프로젝트/Part에서 반복 재사용 가치가 입증될 때 기존 owner 흡수를 우선한다.
   - Base에 기록해야 하는 교훈인데 write/readback 증거가 없으면 `HANDOFF_NOT_READY`다.
12. **송신 packet receipt**
   - GitHub locator, Notion locator, current commit, 남은 일, 첫 행동, Visual audit 결과, 문제/교훈 disposition, Base evidence locator와 readback 상태를 한 번에 확인 가능하게 남긴다.
   - 조건을 만족하면 `PACKET_READY / PENDING_RECEIVER_ACK`로 종료한다.
13. **수신자 fresh-read + receiver_ack**
   - 새 채팅/담당자는 mutation 전에 최신 GitHub·Notion·적용 지침을 다시 읽는다.
   - 현재 상태·다음 행동·보호 범위·미결 승인·이미 적용된 side effect를 readback한다.
   - packet과 현재 정본이 일치하면 `TRANSFER_ACCEPTED`, 불일치하면 `CONTEXT_DRIFT_RECHECK_REQUIRED`다.

## 동일 품질 재개 Gate

인수인계의 목표는 문서 개수를 늘리는 것이 아니라 **새 채팅이 같은 판단 품질을 재현하는 것**이다. 최소 조건은 다음과 같다.

- 프로젝트 목적·핵심 재미·현재 단계가 복원된다.
- 승인된 결정과 변경 금지 범위가 복원된다.
- 구현된 것과 아직 구현되지 않은 것이 구분된다.
- 검증 PASS와 NOT_RUN/UNVERIFIED가 구분된다.
- 다음 작업의 첫 행동·선행 조건·완료 기준이 명확하다.
- GitHub와 Notion 중 무엇이 어떤 사실의 정본인지 알 수 있다.
- 승인 Visual의 실제 위치·용도·현재성·교체 관계를 알 수 있다.
- 이번 작업의 문제와 재사용 가능한 교훈이 프로젝트에만 남을지 Base 후보인지 판단되어 있다.
- `BASE_PROMOTION_CANDIDATE`의 Base 기록 위치와 write/readback 결과를 새 채팅에서 찾을 수 있다.
- 마지막 안전 checkpoint와 이미 적용된 mutation을 구분할 수 있다.
- 미결 사용자 결정과 자동 진행 가능한 범위를 구분할 수 있다.
- 현재 작업 경로에 적용되는 instruction surface를 찾을 수 있다.
- packet 작성 이후 정본 drift가 있는지 확인할 수 있다.

위 조건 중 하나라도 과거 대화 추정에 의존하거나 필수 Base 기록이 누락되면 `HANDOFF_NOT_READY`다.

## 콜드 스타트 질문

새 작업자가 저장소와 적용 가능한 Notion current canon만으로 다음에 답할 수 있어야 한다.

1. 무엇을 만드는가?
2. 현재 어디까지 결정·구현·검증됐는가?
3. 다음 작업과 선행 조건은 무엇인가?
4. 무엇을 변경하면 안 되는가?
5. 관련 책임 원본·Skill·실제 파일·검증은 어디인가?
6. 미확정·보류·위험은 무엇인가?
7. Notion에서 사람이 확인해야 할 핵심 Flow·표·승인 Visual은 어디인가?
8. 이번 작업에서 반복 방지 가치가 있는 문제·교훈과 Base 승격 상태는 무엇인가?
9. Base 승격 후보라면 실제 Base evidence/learning 기록과 readback 위치는 어디인가?
10. `last_safe_checkpoint`와 `next_safe_action`은 무엇이며 이미 실행된 side effect는 무엇인가?
11. 아직 사용자 승인이 필요한 결정이 있는가?
12. 현재 작업에 실제 적용되는 `AGENTS.md`/프로젝트 지침은 무엇인가?
13. Handoff 작성 이후 GitHub/Notion 정본이 바뀌었는가?
14. 이 내용을 자기 말로 readback하고 `receiver_ack`할 수 있는가?

## 실패 조건

- Active Context가 분야 본책의 복제본이 됨
- 별도 Handoff가 두 번째 활성 현재 상태 원본이 됨
- 과거 대화나 도구 로그 전체를 필수 컨텍스트로 만듦
- raw tool log 또는 전체 transcript가 기본 인수인계 payload가 됨
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김
- GitHub/Notion 중 한쪽만 갱신하고 동기화 완료로 선언함
- 이미지 URL이나 파일명만 보고 Notion Visual 전달을 완료로 간주함
- 작업 중 발견한 반복 가능한 문제를 프로젝트 로그에만 묻어 두고 Base promotion disposition을 생략함
- `BASE_PROMOTION_CANDIDATE`를 실제 Base 기록·readback 없이 검토 완료로만 닫음
- 새 채팅이 과거 대화를 요구하는데도 handoff PASS로 선언함
- `PACKET_READY`를 실제 수신자의 `TRANSFER_ACCEPTED`로 과장함
- `side_effects_already_applied` 확인 없이 동일 mutation을 재실행함
- 승인 대기 결정을 일반 next task로 숨겨 새 채팅이 임의 결정함
- 적용되는 `AGENTS.md`/프로젝트 지침을 읽지 않고 Handoff 요약만 신뢰함
- packet 작성 후 main/Notion drift를 확인하지 않고 mutation을 시작함
