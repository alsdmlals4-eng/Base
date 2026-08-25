# 프로젝트 인수인계·컨텍스트 설계 방법

- 상태: 공용 원칙·호환 경로
- 실행 Skill: `skills/maintaining-project-context-and-handoff/SKILL.md`
- 전체 운영 구조: `docs/OPERATING_MODEL.md`

이 문서는 콜드 스타트와 인수인계의 불변 원칙만 책임진다. Active Context 갱신과 Handoff 산출물의 단계형 실행은 Skill이 책임진다.

## 핵심 원칙

Active Context와 Handoff는 전체 기획서·Roadmap·과거 대화를 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업과 위험을 연결하는 압축 라우터**다.

방향, 수치, 용어, 범위, 구현 상태, 파일 경로 또는 작업 절차가 바뀌면 같은 작업 안에서 해당 책임 원본을 먼저 갱신한다. 인수인계 문서로 오래된 원본을 덮어쓰지 않는다.

`인수인계 진행`, `handoff`, `새 채팅으로 넘겨` 같은 사용자 요청은 단순 요약 요청이 아니라 **현재 bounded work를 안전한 checkpoint까지 닫고, 다음 세션이 과거 대화 없이 재개할 수 있게 만드는 종료 트랜잭션**으로 해석한다. 새 기능을 더 벌리는 대신 현재 작업의 정본·증거·미완료 경계를 먼저 닫는다.

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

`승인`과 `구현`, `구현`과 `검증`을 같은 의미로 쓰지 않는다.

## 작성 규칙

- 현재 사실을 먼저 쓰고 역사적 배경은 링크로 보낸다.
- 같은 규칙의 전문을 여러 문서에 복제하지 않는다.
- 실제 확인하지 못한 결과는 `[미검증]`으로 남긴다.
- 프로젝트 방향·분야 본책·Roadmap·Skill을 먼저 갱신한다.
- Active Context에는 경로와 현재 차이만 기록한다.
- 먼저 읽을 책임 원본은 3~7개로 압축한다.
- 다음 작업의 선행 조건·완료 기준·롤백을 명시한다.

## 인수인계 완료 프로토콜

사용자가 인수인계를 지시하면 다음 순서를 하나의 완료 Gate로 취급한다.

1. **현재 작업 checkpoint 완료**
   - 지금 진행 중인 작업 단위를 가능한 안전한 완료점까지 닫는다.
   - 새 범위를 시작하지 않는다.
   - 완료하지 못한 항목은 숨기지 않고 `IN_PROGRESS / BLOCKED / NOT_RUN / UNVERIFIED`로 남긴다.
2. **GitHub 정본 동기화**
   - 현재 branch/main, 정확한 commit, 변경 파일, Issue/PR, 실제 코드·데이터·Scene·Resource·Test 상태를 다시 읽는다.
   - 승인·구현·검증 상태를 분리하고 stale locator를 제거한다.
3. **Notion 정본 동기화**
   - 사람용 Home/Domain/Visual과 AI/System 상세 페이지가 현재 결정과 맞는지 다시 읽는다.
   - Home에는 사람이 알아야 할 결과·Flow·표·승인 Visual을, AI/System에는 운영 메타데이터·검증·handoff 세부를 둔다.
4. **Active Context 갱신 후 Handoff 생성**
   - Handoff는 `현재 상태 → 이번 작업 결과 → 남은 작업 → 위험·미검증 → 다음 작업자의 첫 행동 → 검증·롤백` 순서로 압축한다.
   - 과거 대화가 없으면 복원할 수 없는 핵심 사실이 남아 있으면 인수인계 미완료다.
5. **Fresh-chat resumability test**
   - 새 채팅이 이전 대화·기억 없이 **GitHub + Notion current canon만** 읽는다고 가정한다.
   - 아래 콜드 스타트 질문에 모두 답하고, 첫 작업 경로와 보호 범위를 찾을 수 있어야 한다.
   - 과거 대화를 다시 붙여 넣어야만 같은 품질로 이어갈 수 있으면 `HANDOFF_FAIL_CONTEXT_DEPENDENCY`다.
6. **Notion Visual delivery audit**
   - 이번 작업에 승인·참조·교체된 이미지가 있다면 올바른 프로젝트 Home/Visual/Asset 위치에 실제로 존재하는지 확인한다.
   - 링크/파일명/메타데이터 존재만으로 PASS하지 않는다. 가능한 transport 범위에서 upload/attach, destination readback, 이미지 block 또는 attachment content readback, 승인 상태·용도·supersession을 확인한다.
   - `READBACK_PASS`와 사용자가 실제로 보는 `HUMAN_VISIBLE_PASS`, 그리고 runtime product asset 승인을 구분한다.
   - 깨진 링크, placeholder, 이전 승인본이 현행인 것처럼 남은 상태는 인수인계 차단 사유다.
7. **문제 → 교훈 추출**
   - 작업 중 실제 발생한 문제, 원인, 해결/기각한 방법, 증거, 재발 방지 규칙을 기록한다.
   - `PROJECT_ONLY / PART_ONLY / BASE_PROMOTION_CANDIDATE / NO_NEW_REUSABLE_LESSON` 중 하나로 분류한다.
8. **Base 승격 검토**
   - 여러 프로젝트/Part에서 재사용 가치가 있거나 공용 운영 실패를 막는 교훈은 기존 Base canonical owner에 흡수하는 것을 우선한다.
   - 새 광역 Skill/중복 정책을 자동 생성하지 않는다.
   - 열린 PR이 같은 owner를 변경 중이면 그 PR을 흡수·수정·재작성하지 않고 evidence/candidate만 독립 경로에 남긴 뒤 안전한 Integration 시점으로 넘긴다.
9. **최종 인수인계 receipt**
   - GitHub locator, Notion locator, current commit, 남은 일, 첫 행동, Visual audit 결과, 문제/교훈 disposition, Base 승격 상태를 한 번에 확인 가능하게 남긴다.

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

위 조건 중 하나라도 과거 대화 추정에 의존하면 `HANDOFF_NOT_READY`다.

## 콜드 스타트 질문

새 작업자가 저장소만으로 다음에 답할 수 있어야 한다.

1. 무엇을 만드는가?
2. 현재 어디까지 결정·구현·검증됐는가?
3. 다음 작업과 선행 조건은 무엇인가?
4. 무엇을 변경하면 안 되는가?
5. 관련 책임 원본·Skill·실제 파일·검증은 어디인가?
6. 미확정·보류·위험은 무엇인가?
7. Notion에서 사람이 확인해야 할 핵심 Flow·표·승인 Visual은 어디인가?
8. 이번 작업에서 반복 방지 가치가 있는 문제·교훈과 Base 승격 상태는 무엇인가?

## 실패 조건

- Active Context가 분야 본책의 복제본이 됨
- 별도 Handoff가 두 번째 활성 현재 상태 원본이 됨
- 과거 대화나 도구 로그 전체를 필수 컨텍스트로 만듦
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김
- GitHub/Notion 중 한쪽만 갱신하고 동기화 완료로 선언함
- 이미지 URL이나 파일명만 보고 Notion Visual 전달을 완료로 간주함
- 작업 중 발견한 반복 가능한 문제를 프로젝트 로그에만 묻어 두고 Base promotion disposition을 생략함
- 새 채팅이 과거 대화를 요구하는데도 handoff PASS로 선언함
